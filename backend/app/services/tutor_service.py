from sqlalchemy.orm import Session

from app.database.models.tutor_decision import (
    TutorDecision,
)
from app.database.repositories.session_repository import (
    LearningSessionRepository,
)
from app.database.repositories.student_repository import (
    StudentRepository,
)
from app.database.repositories.tutor_decision_repository import (
    TutorDecisionRepository,
)
from app.schemas.enums import (
    AgeGroup,
    LearningMode,
    MasteryState,
    Subject,
    TutorIntent,
)
from app.services.adaptive_learning_service import (
    AdaptiveLearningService,
)
from app.services.english_adaptive_learning_service import (
    EnglishAdaptiveLearningService,
)
from app.services.science_adaptive_learning_service import (
    ScienceAdaptiveLearningService,
)
from app.tutor.decision_models import (
    TutorDecisionInput,
    TutorDecisionResult,
)
from app.tutor.policy_engine import (
    TutorPolicyEngine,
)
from app.tutor.session_state import (
    TutorSessionState,
)


class TutorService:

    policy_engine = (
        TutorPolicyEngine()
    )


    @classmethod
    def make_decision(
        cls,
        db: Session,
        session_id: str,
        decision_input: TutorDecisionInput,
        model_used: str | None = None,
    ) -> TutorDecisionResult:

        learning_session = (
            LearningSessionRepository.get_by_id(
                db=db,
                session_id=session_id,
            )
        )


        if (
            learning_session is None
        ):
            raise ValueError(
                "Learning session not found."
            )


        student = (
            StudentRepository.get_by_id(
                db=db,
                student_id=(
                    learning_session.student_id
                ),
            )
        )


        if (
            student is None
        ):
            raise ValueError(
                "Student not found."
            )


        subject = Subject(
            learning_session.subject
        )


        adaptive_plan = None


        # ==================================
        # Math adaptive plan
        # ==================================

        if (
            subject == Subject.MATH

            and learning_session.concept_code
        ):

            try:

                adaptive_plan = (
                    AdaptiveLearningService
                    .get_plan(
                        db=db,

                        student_id=student.id,

                        concept_code=(
                            learning_session
                            .concept_code
                        ),
                    )
                )

            except (
                LookupError,
                ValueError,
            ):

                adaptive_plan = None


        # ==================================
        # Science adaptive plan
        # ==================================

        elif (
            subject == Subject.SCIENCE

            and learning_session.concept_code
        ):

            try:

                adaptive_plan = (
                    ScienceAdaptiveLearningService
                    .get_plan(
                        db=db,

                        student_id=student.id,

                        concept_code=(
                            learning_session
                            .concept_code
                        ),
                    )
                )


                learning_session.mastery_state = (
                    adaptive_plan
                    .mastery_state
                    .value
                )

            except (
                LookupError,
                ValueError,
            ):

                adaptive_plan = None


        # ==================================
        # English adaptive plan
        # ==================================

        elif (
            subject == Subject.ENGLISH

            and learning_session.concept_code
        ):

            try:

                adaptive_plan = (
                    EnglishAdaptiveLearningService
                    .get_plan(
                        db=db,

                        student_id=student.id,

                        concept_code=(
                            learning_session
                            .concept_code
                        ),
                    )
                )


                learning_session.mastery_state = (
                    adaptive_plan
                    .mastery_state
                    .value
                )

            except (
                LookupError,
                ValueError,
            ):

                adaptive_plan = None


        mastery_state = MasteryState(
            learning_session.mastery_state
        )


        if (
            adaptive_plan is not None

            and subject
            in {
                Subject.SCIENCE,
                Subject.ENGLISH,
            }
        ):

            mastery_state = (
                adaptive_plan.mastery_state
            )


        state = (
            TutorSessionState(
                session_id=(
                    learning_session.id
                ),

                student_id=(
                    learning_session.student_id
                ),

                age_group=(
                    AgeGroup(
                        student.age_group
                    )
                ),

                mode=(
                    LearningMode(
                        learning_session.mode
                    )
                ),

                subject=subject,

                topic=(
                    learning_session.topic
                ),

                concept_code=(
                    learning_session.concept_code
                ),

                current_problem=(
                    learning_session.current_problem
                ),

                attempt_count=(
                    learning_session.attempt_count
                ),

                hint_level=(
                    learning_session.current_hint_level
                ),

                direct_answer_requests=(
                    learning_session
                    .direct_answer_requests
                ),

                current_misconception=(
                    learning_session
                    .current_misconception
                ),

                mastery_state=(
                    mastery_state
                ),

                adaptive_difficulty=(
                    adaptive_plan.difficulty

                    if adaptive_plan
                    is not None

                    else None
                ),

                adaptive_support=(
                    adaptive_plan.support_level

                    if adaptive_plan
                    is not None

                    else None
                ),

                explanation_depth=(
                    adaptive_plan
                    .explanation_depth

                    if adaptive_plan
                    is not None

                    else None
                ),
            )
        )


        result = (
            cls.policy_engine.decide(
                state=state,
                decision_input=(
                    decision_input
                ),
            )
        )


        cls._update_session_state(
            learning_session=(
                learning_session
            ),

            decision_input=(
                decision_input
            ),

            result=result,
        )


        LearningSessionRepository.save(
            db=db,

            learning_session=(
                learning_session
            ),
        )


        cls._save_decision(
            db=db,

            result=result,

            decision_input=(
                decision_input
            ),

            model_used=(
                model_used
            ),
        )


        return result


    @staticmethod
    def _update_session_state(
        learning_session,
        decision_input: TutorDecisionInput,
        result: TutorDecisionResult,
    ) -> None:

        if (
            decision_input.new_problem
        ):

            learning_session.attempt_count = 0

            learning_session.current_hint_level = 0


        else:

            learning_session.current_hint_level = (
                result.hint_level
            )


        if (
            decision_input.intent
            == TutorIntent.DIRECT_ANSWER_REQUEST
        ):

            learning_session.direct_answer_requests += 1


        if (
            decision_input.intent
            == TutorIntent.STUDENT_ATTEMPT
        ):

            learning_session.attempt_count += 1


        learning_session.last_tutor_action = (
            result.next_action.value
        )


    @staticmethod
    def _save_decision(
        db: Session,
        result: TutorDecisionResult,
        decision_input: TutorDecisionInput,
        model_used: str | None = None,
    ) -> None:

        decision = (
            TutorDecision(
                session_id=(
                    result.session_id
                ),

                student_id=(
                    result.student_id
                ),

                detected_intent=(
                    result.intent.value
                ),

                subject=(
                    result.subject.value
                ),

                attempt_status=(
                    decision_input
                    .attempt_status
                    .value

                    if decision_input
                    .attempt_status

                    else None
                ),

                selected_action=(
                    result.next_action.value
                ),

                selected_hint_level=(
                    result.hint_level
                ),

                allow_final_answer=(
                    result.allow_final_answer
                ),

                requires_rag=(
                    result.requires_rag
                ),

                requires_validation=(
                    result.requires_validation
                ),

                requires_mastery_check=(
                    result.requires_mastery_check
                ),

                policy_bypass_detected=(
                    result.policy_bypass_detected
                ),

                model_used=(
                    model_used
                ),
            )
        )


        TutorDecisionRepository.create(
            db=db,
            decision=decision,
        )