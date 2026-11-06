from statistics import mean

from sqlalchemy.orm import Session

from app.adaptive.profile import (
    LearningProfileAnalyzer,
)
from app.database.repositories.student_attempt_repository import (
    StudentAttemptRepository,
)
from app.database.repositories.student_repository import (
    StudentRepository,
)
from app.english.adaptive_engine import (
    EnglishAdaptiveEngine,
    EnglishAdaptiveSignals,
)
from app.english.question_bank import (
    get_english_question,
    get_english_questions,
)
from app.schemas.english_adaptive import (
    EnglishAdaptivePlanResponse,
    EnglishQuestionView,
)
from app.schemas.enums import (
    AgeGroup,
    AttemptStatus,
    MasteryState,
)
from app.services.telemetry_service import (
    TelemetryService,
)


class EnglishAdaptiveLearningService:

    @classmethod
    def get_plan(
        cls,
        db: Session,
        student_id: str,
        concept_code: str,
    ) -> EnglishAdaptivePlanResponse:

        student = (
            StudentRepository
            .get_by_id(
                db=db,
                student_id=student_id,
            )
        )


        if (
            student is None
        ):
            raise LookupError(
                "Student not found."
            )


        # ==================================
        # Validate English concept
        # ==================================

        available_questions = (
            get_english_questions(
                concept_code
            )
        )


        if (
            not available_questions
        ):
            raise LookupError(
                "English concept not found."
            )


        # ==================================
        # Student attempts
        # ==================================

        all_attempts = (
            StudentAttemptRepository
            .list_by_student(
                db=db,
                student_id=student_id,
            )
        )


        attempts = [
            attempt

            for attempt
            in all_attempts

            if (
                attempt.problem_ref
                == concept_code
            )
        ]


        total_attempts = len(
            attempts
        )


        correct_attempts = sum(
            1

            for attempt
            in attempts

            if (
                attempt.status
                == AttemptStatus.CORRECT.value
            )
        )


        partial_attempts = sum(
            1

            for attempt
            in attempts

            if (
                attempt.status
                == (
                    AttemptStatus
                    .PARTIALLY_CORRECT
                    .value
                )
            )
        )


        # ==================================
        # Independent evidence
        # ==================================

        independent_attempts = [
            attempt

            for attempt
            in attempts

            if attempt.is_independent
        ]


        independent_attempt_count = len(
            independent_attempts
        )


        independent_correct = sum(
            1

            for attempt
            in independent_attempts

            if (
                attempt.status
                == AttemptStatus.CORRECT.value
            )
        )


        independent_attempt_rate = (
            round(
                (
                    independent_attempt_count
                    / total_attempts
                    * 100
                )

                if total_attempts
                else 0.0,

                1,
            )
        )


        independent_success_rate = (
            round(
                (
                    independent_correct
                    / independent_attempt_count
                    * 100
                )

                if independent_attempt_count
                else 0.0,

                1,
            )
        )


        # ==================================
        # Hint usage
        # ==================================

        average_hint_level = (
            round(
                mean(
                    [
                        attempt
                        .hint_level_before

                        for attempt
                        in attempts
                    ]
                ),
                2,
            )

            if attempts

            else 0.0
        )


        # ==================================
        # Understanding signal
        #
        # Correct = 1.0
        # Partial = 0.5
        #
        # Internal LearnFirst signal.
        # Not a school grade.
        # ==================================

        weighted_score = (
            correct_attempts
            + (
                partial_attempts
                * 0.5
            )
        )


        understanding_score = (
            round(
                (
                    weighted_score
                    / total_attempts
                    * 100
                )

                if total_attempts
                else 0.0,

                1,
            )
        )


        # ==================================
        # Telemetry
        # ==================================

        telemetry = (
            TelemetryService
            .get_summary(
                db=db,
                student_id=student_id,
                concept_code=concept_code,
            )
        )


        latencies = (
            TelemetryService
            .get_response_latencies(
                db=db,
                student_id=student_id,
                concept_code=concept_code,
            )
        )


        personal_profile = (
            LearningProfileAnalyzer
            .analyze(
                latencies
            )
        )


        # ==================================
        # Adaptive decision
        # ==================================

        signals = (
            EnglishAdaptiveSignals(
                age_group=(
                    AgeGroup(
                        student.age_group
                    )
                ),

                total_attempts=(
                    total_attempts
                ),

                correct_attempts=(
                    correct_attempts
                ),

                partial_attempts=(
                    partial_attempts
                ),

                understanding_score_percent=(
                    understanding_score
                ),

                independent_attempt_rate=(
                    independent_attempt_rate
                ),

                independent_success_rate=(
                    independent_success_rate
                ),

                average_hint_level=(
                    average_hint_level
                ),

                direct_answer_requests=(
                    telemetry
                    .direct_answer_requests
                ),

                measured_response_count=(
                    telemetry
                    .measured_student_responses
                ),

                average_response_latency_ms=(
                    telemetry
                    .average_response_latency_ms
                ),

                baseline_ready=(
                    personal_profile
                    .baseline_ready
                ),

                personalized_response_pace=(
                    personal_profile
                    .personalized_response_pace
                ),
            )
        )


        decision = (
            EnglishAdaptiveEngine
            .decide(
                signals
            )
        )


        # ==================================
        # Next question
        # ==================================

        question = (
            get_english_question(
                concept_code=concept_code,

                offset=(
                    total_attempts
                ),

                difficulty=(
                    decision.difficulty
                ),
            )
        )


        next_question = None


        if (
            question is not None
        ):
            next_question = (
                EnglishQuestionView(
                    question_id=(
                        question.question_id
                    ),

                    prompt=(
                        question.prompt
                    ),

                    difficulty=(
                        question.difficulty
                    ),
                )
            )


        mastery_explanation = (
            cls._mastery_explanation(
                mastery_state=(
                    decision.mastery_state
                ),

                total_attempts=(
                    total_attempts
                ),

                understanding_score=(
                    understanding_score
                ),

                independent_attempt_rate=(
                    independent_attempt_rate
                ),

                independent_success_rate=(
                    independent_success_rate
                ),
            )
        )


        return (
            EnglishAdaptivePlanResponse(
                student_id=student_id,

                concept_code=concept_code,

                age_group=(
                    AgeGroup(
                        student.age_group
                    )
                ),

                mastery_state=(
                    decision.mastery_state
                ),

                mastery_explanation=(
                    mastery_explanation
                ),

                difficulty=(
                    decision.difficulty
                ),

                support_level=(
                    decision.support_level
                ),

                explanation_depth=(
                    decision
                    .explanation_depth
                ),

                next_activity=(
                    decision.next_activity
                ),

                understanding_score_percent=(
                    understanding_score
                ),

                total_attempts=(
                    total_attempts
                ),

                correct_attempts=(
                    correct_attempts
                ),

                partial_attempts=(
                    partial_attempts
                ),

                independent_attempts=(
                    independent_attempt_count
                ),

                independent_attempt_rate=(
                    independent_attempt_rate
                ),

                independent_success_rate=(
                    independent_success_rate
                ),

                average_hint_level=(
                    average_hint_level
                ),

                direct_answer_requests=(
                    telemetry
                    .direct_answer_requests
                ),

                measured_response_count=(
                    telemetry
                    .measured_student_responses
                ),

                average_response_latency_ms=(
                    telemetry
                    .average_response_latency_ms
                ),

                response_pace=(
                    decision.response_pace
                ),

                baseline_ready=(
                    personal_profile
                    .baseline_ready
                ),

                baseline_response_latency_ms=(
                    personal_profile
                    .baseline_response_latency_ms
                ),

                recent_response_latency_ms=(
                    personal_profile
                    .recent_response_latency_ms
                ),

                latency_change_percent=(
                    personal_profile
                    .latency_change_percent
                ),

                response_pace_source=(
                    decision
                    .response_pace_source
                ),

                reason_codes=list(
                    decision.reason_codes
                ),

                summary=(
                    decision.summary
                ),

                next_question=(
                    next_question
                ),
            )
        )


    @staticmethod
    def _mastery_explanation(
        mastery_state: MasteryState,
        total_attempts: int,
        understanding_score: float,
        independent_attempt_rate: float,
        independent_success_rate: float,
    ) -> str:

        if (
            mastery_state
            == MasteryState.NOT_STARTED
        ):
            return (
                "No structured English "
                "attempts have been "
                "evaluated yet."
            )


        if (
            mastery_state
            == MasteryState.STRONG
        ):
            return (
                "LearnFirst sees a strong "
                "English mastery signal "
                "because the learner has "
                "multiple successful attempts "
                "with strong independent "
                "performance."
            )


        if (
            mastery_state
            == MasteryState.DEVELOPING
        ):
            return (
                "English understanding is "
                "developing. LearnFirst has "
                f"evaluated {total_attempts} "
                "attempts with an internal "
                f"understanding signal of "
                f"{understanding_score}%."
            )


        return (
            "The learner is still building "
            "this English concept. "
            f"Current understanding evidence "
            f"is {understanding_score}%, "
            f"independent attempt rate is "
            f"{independent_attempt_rate}%, "
            f"and independent success is "
            f"{independent_success_rate}%."
        )