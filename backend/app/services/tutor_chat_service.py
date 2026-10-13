from sqlalchemy.orm import Session

from app.database.repositories.session_repository import (
    LearningSessionRepository,
)
from app.database.repositories.student_repository import (
    StudentRepository,
)
from app.intent.router import (
    IntentRouter,
)
from app.llm.gateway import (
    LLMGateway,
)
from app.math.attempt_service import (
    MathAttemptService,
)
from app.math.models import (
    MathValidationResult,
    create_public_validation,
)
from app.schemas.chat import (
    TutorMessageResponse,
)
from app.schemas.enums import (
    AgeGroup,
    AttemptStatus,
    LearningMode,
    MasteryState,
    Subject,
    TutorAction,
    TutorIntent,
)
from app.services.tutor_service import (
    TutorService,
)
from app.tutor.decision_models import (
    TutorDecisionInput,
)
from app.tutor.prompt_builder import (
    TutorPromptBuilder,
)
from app.tutor.session_state import (
    TutorSessionState,
)


class TutorChatService:

    @classmethod
    def process_message(
        cls,
        db: Session,
        session_id: str,
        student_message: str,
    ) -> TutorMessageResponse:

        # ----------------------------------
        # 1. Load Learning Session
        # ----------------------------------

        learning_session = (
            LearningSessionRepository
            .get_by_id(
                db=db,
                session_id=session_id,
            )
        )

        if learning_session is None:

            raise ValueError(
                "Learning session not found."
            )

        # ----------------------------------
        # 2. Load Student
        # ----------------------------------

        student = (
            StudentRepository.get_by_id(
                db=db,
                student_id=(
                    learning_session
                    .student_id
                ),
            )
        )

        if student is None:

            raise ValueError(
                "Student not found."
            )

        # ----------------------------------
        # 3. Detect learner intent
        # ----------------------------------

        intent = IntentRouter.classify(
            student_message
        )

        math_validation: (
            MathValidationResult | None
        ) = None

        attempt_status: (
            AttemptStatus | None
        ) = None

        hint_level_before = (
            learning_session
            .current_hint_level
        )

        # ----------------------------------
        # 4. Deterministic Math validation
        # ----------------------------------

        if (
            intent
            == TutorIntent.STUDENT_ATTEMPT
        ):

            if (
                learning_session.subject
                == Subject.MATH.value
                and learning_session
                .current_problem
            ):

                math_validation = (
                    MathAttemptService
                    .analyze(
                        problem=(
                            learning_session
                            .current_problem
                        ),
                        student_message=(
                            student_message
                        ),
                    )
                )

                attempt_status = (
                    math_validation.status
                )

            else:

                attempt_status = (
                    AttemptStatus.UNCLEAR
                )

        # ----------------------------------
        # 5. Construct Tutor Decision Input
        # ----------------------------------

        decision_input = (
            TutorDecisionInput(
                intent=intent,
                attempt_status=(
                    attempt_status
                ),
            )
        )

        # ----------------------------------
        # 6. Load configured LLM provider
        # ----------------------------------

        gateway = LLMGateway()

        # ----------------------------------
        # 7. Run Tutor Policy
        # ----------------------------------

        decision = (
            TutorService.make_decision(
                db=db,
                session_id=session_id,
                decision_input=(
                    decision_input
                ),
                model_used=(
                    gateway.model_name
                ),
            )
        )

        # TutorService may update:
        #
        # attempt_count
        # hint_level
        # direct_answer_requests
        # last_tutor_action
        #
        # Reload it.

        refreshed_session = (
            LearningSessionRepository
            .get_by_id(
                db=db,
                session_id=session_id,
            )
        )

        if refreshed_session is None:

            raise ValueError(
                "Learning session could not "
                "be reloaded."
            )

        # ----------------------------------
        # 8. Save Math attempt
        # ----------------------------------

        if math_validation is not None:

            MathAttemptService.record(
                db=db,

                learning_session=(
                    refreshed_session
                ),

                student_message=(
                    student_message
                ),

                validation=(
                    math_validation
                ),

                hint_level_before=(
                    hint_level_before
                ),
            )

            # Reload because recording can
            # update current_misconception.

            refreshed_session = (
                LearningSessionRepository
                .get_by_id(
                    db=db,
                    session_id=session_id,
                )
            )

        # ----------------------------------
        # 9. Build current Tutor State
        # ----------------------------------

        state = TutorSessionState(
            session_id=(
                refreshed_session.id
            ),

            student_id=(
                refreshed_session
                .student_id
            ),

            age_group=AgeGroup(
                student.age_group
            ),

            mode=LearningMode(
                refreshed_session.mode
            ),

            subject=Subject(
                refreshed_session.subject
            ),

            topic=(
                refreshed_session.topic
            ),

            concept_code=(
                refreshed_session
                .concept_code
            ),

            current_problem=(
                refreshed_session
                .current_problem
            ),

            attempt_count=(
                refreshed_session
                .attempt_count
            ),

            hint_level=(
                refreshed_session
                .current_hint_level
            ),

            direct_answer_requests=(
                refreshed_session
                .direct_answer_requests
            ),

            current_misconception=(
                refreshed_session
                .current_misconception
            ),

            mastery_state=MasteryState(
                refreshed_session
                .mastery_state
            ),
        )

        # ----------------------------------
        # 10. Create safe public validation
        # ----------------------------------

        public_validation = (
            create_public_validation(
                math_validation
            )
            if math_validation
            is not None
            else None
        )

        # ----------------------------------
        # 11. High-control deterministic
        #     responses
        # ----------------------------------

        deterministic_reply = (
            cls._deterministic_response(
                decision.next_action
            )
        )

        if (
            deterministic_reply
            is not None
        ):

            return TutorMessageResponse(
                session_id=(
                    session_id
                ),

                student_message=(
                    student_message
                ),

                detected_intent=(
                    intent
                ),

                decision=(
                    decision
                ),

                math_validation=(
                    public_validation
                ),

                reply=(
                    deterministic_reply
                ),

                provider="system",

                model="deterministic",

                latency_ms=0.0,
            )

        # ----------------------------------
        # 12. Build controlled LLM prompt
        # ----------------------------------

        request = (
            TutorPromptBuilder.build(
                student_message=(
                    student_message
                ),

                state=state,

                decision=decision,

                math_validation=(
                    math_validation
                ),
            )
        )

        # ----------------------------------
        # 13. Generate natural response
        # ----------------------------------

        result = gateway.generate(
            request
        )

        # ----------------------------------
        # 14. Return API response
        # ----------------------------------

        return TutorMessageResponse(
            session_id=session_id,

            student_message=(
                student_message
            ),

            detected_intent=(
                intent
            ),

            decision=(
                decision
            ),

            math_validation=(
                public_validation
            ),

            reply=result.content,

            provider=result.provider,

            model=result.model,

            latency_ms=(
                result.latency_ms
            ),
        )

    @staticmethod
    def _deterministic_response(
        action: TutorAction,
    ) -> str | None:
        """
        High-control actions should not rely
        on the generative model.
        """

        if (
            action
            == TutorAction
            .REFUSE_POLICY_BYPASS
        ):

            return (
                "I can help you work through "
                "the problem, but I won't skip "
                "the learning steps just to "
                "reveal the answer."
            )

        if (
            action
            == TutorAction
            .CLARIFY_TEST_INSTRUCTION
        ):

            return (
                "This is Mock Test Mode, so "
                "I can't give hints or solutions "
                "during the test."
            )

        if (
            action
            == TutorAction
            .ESCALATE_SAFETY
        ):

            return (
                "I can't handle this as a "
                "normal learning question. "
                "Please involve a trusted adult "
                "who can help."
            )

        return None