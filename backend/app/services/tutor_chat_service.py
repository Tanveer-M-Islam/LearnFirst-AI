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
        # 1. Detect intent
        # ----------------------------------

        intent = IntentRouter.classify(
            student_message
        )

        # ----------------------------------
        # 2. Phase 4 cannot yet validate
        #    Math correctness.
        # ----------------------------------

        attempt_status = None

        if (
            intent
            == TutorIntent.STUDENT_ATTEMPT
        ):
            attempt_status = (
                AttemptStatus.UNCLEAR
            )

        decision_input = TutorDecisionInput(
            intent=intent,
            attempt_status=attempt_status,
        )

        # ----------------------------------
        # 3. Prepare provider
        # ----------------------------------

        gateway = LLMGateway()

        # ----------------------------------
        # 4. Tutor Policy
        # ----------------------------------

        decision = TutorService.make_decision(
            db=db,
            session_id=session_id,
            decision_input=decision_input,
            model_used=gateway.model_name,
        )

        # ----------------------------------
        # 5. Reconstruct current state
        # ----------------------------------

        refreshed_session = (
            LearningSessionRepository
            .get_by_id(
                db=db,
                session_id=session_id,
            )
        )

        state = TutorSessionState(
            session_id=(
                refreshed_session.id
            ),

            student_id=(
                refreshed_session.student_id
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
        # 6. High-control deterministic
        #    responses
        # ----------------------------------

        deterministic_reply = (
            cls._deterministic_response(
                decision.next_action
            )
        )

        if deterministic_reply is not None:

            return TutorMessageResponse(
                session_id=session_id,
                student_message=(
                    student_message
                ),
                detected_intent=intent,
                decision=decision,
                reply=deterministic_reply,
                provider="system",
                model="deterministic",
                latency_ms=0.0,
            )

        # ----------------------------------
        # 7. Build controlled LLM prompt
        # ----------------------------------

        request = (
            TutorPromptBuilder.build(
                student_message=(
                    student_message
                ),
                state=state,
                decision=decision,
            )
        )

        # ----------------------------------
        # 8. Generate tutor response
        # ----------------------------------

        result = gateway.generate(
            request
        )

        return TutorMessageResponse(
            session_id=session_id,

            student_message=(
                student_message
            ),

            detected_intent=intent,

            decision=decision,

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
            == TutorAction.ESCALATE_SAFETY
        ):
            return (
                "I can't handle this as a normal "
                "learning question. Please involve "
                "a trusted adult who can help."
            )

        return None