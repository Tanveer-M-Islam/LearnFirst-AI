from datetime import (
    datetime,
    timezone,
)
from statistics import (
    mean,
    median,
)

from sqlalchemy.orm import (
    Session,
)

from app.database.models.learning_event import (
    LearningEvent,
)
from app.database.repositories.learning_event_repository import (
    LearningEventRepository,
)
from app.database.repositories.session_repository import (
    LearningSessionRepository,
)
from app.schemas.chat import (
    TutorMessageResponse,
)
from app.schemas.telemetry import (
    LearningEventType,
    TelemetrySummaryResponse,
)


class TelemetryService:

    MAX_RESPONSE_LATENCY_MS = (
        60 * 60 * 1000
    )


    @classmethod
    def start_student_interaction(
        cls,
        db: Session,
        session_id: str,
        student_message: str,
    ) -> LearningEvent:

        learning_session = (
            LearningSessionRepository
            .get_by_id(
                db=db,

                session_id=(
                    session_id
                ),
            )
        )


        if (
            learning_session
            is None
        ):

            raise ValueError(
                "Learning session "
                "not found."
            )


        previous_tutor_event = (
            LearningEventRepository
            .latest_tutor_response(
                db=db,

                session_id=(
                    session_id
                ),
            )
        )


        response_latency_ms = None


        if (
            previous_tutor_event
            is not None
        ):

            previous_time = (
                cls._aware_datetime(
                    previous_tutor_event
                    .created_at
                )
            )


            now = datetime.now(
                timezone.utc
            )


            elapsed_ms = int(
                (
                    now
                    - previous_time
                )
                .total_seconds()
                * 1000
            )


            if (
                0
                <= elapsed_ms
                <= cls
                .MAX_RESPONSE_LATENCY_MS
            ):

                response_latency_ms = (
                    elapsed_ms
                )


        event = LearningEvent(
            session_id=(
                learning_session.id
            ),

            student_id=(
                learning_session
                .student_id
            ),

            subject=(
                learning_session
                .subject
            ),

            concept_code=(
                learning_session
                .concept_code
            ),

            event_type=(
                LearningEventType
                .STUDENT_MESSAGE
                .value
            ),

            response_latency_ms=(
                response_latency_ms
            ),

            event_metadata={
                "message_length": (
                    len(
                        student_message
                    )
                )
            },
        )


        return (
            LearningEventRepository
            .create(
                db=db,

                event=(
                    event
                ),
            )
        )


    @classmethod
    def complete_interaction(
        cls,
        db: Session,
        student_event_id: str,
        response: TutorMessageResponse,
    ) -> None:

        student_event = (
            LearningEventRepository
            .get_by_id(
                db=db,

                event_id=(
                    student_event_id
                ),
            )
        )


        if (
            student_event
            is None
        ):

            return


        student_event.detected_intent = (
            response
            .detected_intent
            .value
        )


        student_event.selected_action = (
            response
            .decision
            .next_action
            .value
        )


        student_event.hint_level = (
            response
            .decision
            .hint_level
        )


        (
            LearningEventRepository
            .save(
                db=db,

                event=(
                    student_event
                ),
            )
        )


        tutor_event = LearningEvent(
            session_id=(
                response
                .session_id
            ),

            student_id=(
                response
                .decision
                .student_id
            ),

            subject=(
                response
                .decision
                .subject
                .value
            ),

            concept_code=(
                student_event
                .concept_code
            ),

            event_type=(
                LearningEventType
                .TUTOR_RESPONSE
                .value
            ),

            tutor_latency_ms=(
                response
                .latency_ms
            ),

            detected_intent=(
                response
                .detected_intent
                .value
            ),

            selected_action=(
                response
                .decision
                .next_action
                .value
            ),

            hint_level=(
                response
                .decision
                .hint_level
            ),

            event_metadata={
                "provider": (
                    response.provider
                ),

                "model": (
                    response.model
                ),

                "rag_used": (
                    response.rag_used
                ),

                "rag_source_count": (
                    len(
                        response
                        .rag_sources
                    )
                ),
            },
        )


        (
            LearningEventRepository
            .create(
                db=db,

                event=(
                    tutor_event
                ),
            )
        )


    # ======================================================
    # Phase 14
    # Raw ordered response latency history
    # ======================================================

    @classmethod
    def get_response_latencies(
        cls,
        db: Session,
        student_id: str,
        concept_code: str,
    ) -> list[int]:

        events = (
            LearningEventRepository
            .list_by_student_concept(
                db=db,

                student_id=(
                    student_id
                ),

                concept_code=(
                    concept_code
                ),
            )
        )


        latencies: list[int] = []


        for event in events:

            if (
                event.event_type
                != (
                    LearningEventType
                    .STUDENT_MESSAGE
                    .value
                )
            ):

                continue


            latency = (
                event
                .response_latency_ms
            )


            if (
                latency is None
            ):

                continue


            if (
                latency <= 0

                or latency
                > cls
                .MAX_RESPONSE_LATENCY_MS
            ):

                continue


            latencies.append(
                int(
                    latency
                )
            )


        return latencies


    @classmethod
    def get_summary(
        cls,
        db: Session,
        student_id: str,
        concept_code: str,
    ) -> TelemetrySummaryResponse:

        events = (
            LearningEventRepository
            .list_by_student_concept(
                db=db,

                student_id=(
                    student_id
                ),

                concept_code=(
                    concept_code
                ),
            )
        )


        student_events = [
            event

            for event
            in events

            if event.event_type
            == (
                LearningEventType
                .STUDENT_MESSAGE
                .value
            )
        ]


        tutor_events = [
            event

            for event
            in events

            if event.event_type
            == (
                LearningEventType
                .TUTOR_RESPONSE
                .value
            )
        ]


        response_latencies = [
            event
            .response_latency_ms

            for event
            in student_events

            if event
            .response_latency_ms
            is not None
        ]


        tutor_latencies = [
            event
            .tutor_latency_ms

            for event
            in tutor_events

            if event
            .tutor_latency_ms
            is not None
        ]


        hint_intents = {
            "HINT_REQUEST",
            "CONFUSION",
            "I_DONT_KNOW",
        }


        hint_requests = sum(
            1

            for event
            in student_events

            if event.detected_intent
            in hint_intents
        )


        direct_answer_requests = sum(
            1

            for event
            in student_events

            if event.detected_intent
            == "DIRECT_ANSWER_REQUEST"
        )


        rag_grounded = sum(
            1

            for event
            in tutor_events

            if (
                event.event_metadata
                or {}
            ).get(
                "rag_used",
                False,
            )
        )


        average_response = (
            round(
                mean(
                    response_latencies
                ),
                1,
            )

            if response_latencies

            else None
        )


        median_response = (
            round(
                median(
                    response_latencies
                ),
                1,
            )

            if response_latencies

            else None
        )


        average_tutor = (
            round(
                mean(
                    tutor_latencies
                ),
                1,
            )

            if tutor_latencies

            else None
        )


        return (
            TelemetrySummaryResponse(
                student_id=(
                    student_id
                ),

                concept_code=(
                    concept_code
                ),

                student_messages=(
                    len(
                        student_events
                    )
                ),

                tutor_responses=(
                    len(
                        tutor_events
                    )
                ),

                measured_student_responses=(
                    len(
                        response_latencies
                    )
                ),

                average_response_latency_ms=(
                    average_response
                ),

                median_response_latency_ms=(
                    median_response
                ),

                average_tutor_latency_ms=(
                    average_tutor
                ),

                hint_requests=(
                    hint_requests
                ),

                direct_answer_requests=(
                    direct_answer_requests
                ),

                rag_grounded_responses=(
                    rag_grounded
                ),
            )
        )


    @staticmethod
    def _aware_datetime(
        value: datetime,
    ) -> datetime:

        if (
            value.tzinfo
            is None
        ):

            return value.replace(
                tzinfo=(
                    timezone.utc
                )
            )


        return value