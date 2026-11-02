from sqlalchemy.orm import (
    Session,
)

from app.adaptive.problem_bank import (
    get_adaptive_problem,
)
from app.database.repositories.session_repository import (
    LearningSessionRepository,
)
from app.database.repositories.student_attempt_repository import (
    StudentAttemptRepository,
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
from app.rag.models import (
    RAGContext,
)
from app.rag.service import (
    RAGService,
)
from app.schemas.chat import (
    TutorMessageResponse,
)
from app.schemas.enums import (
    AgeGroup,
    AttemptStatus,
    DifficultyLevel,
    LearningMode,
    MasteryState,
    Subject,
    TutorAction,
    TutorIntent,
)
from app.services.adaptive_learning_service import (
    AdaptiveLearningService,
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


        student = (
            StudentRepository
            .get_by_id(
                db=db,

                student_id=(
                    learning_session
                    .student_id
                ),
            )
        )


        if (
            student
            is None
        ):

            raise ValueError(
                "Student not found."
            )


        intent = (
            IntentRouter.classify(
                student_message
            )
        )


        mode = (
            LearningMode(
                learning_session
                .mode
            )
        )


        subject = (
            Subject(
                learning_session
                .subject
            )
        )


        # ==================================
        # Practice-question request
        #
        # Practice and Learn Mode both use
        # a real stored problem from the
        # deterministic problem bank.
        # ==================================

        if (
            subject
            == Subject.MATH

            and mode
            in {
                LearningMode.PRACTICE,
                LearningMode.LEARN,
            }

            and intent
            == TutorIntent
            .PRACTICE_REQUEST
        ):

            learning_session = (
                cls
                ._assign_next_math_problem(
                    db=db,

                    learning_session=(
                        learning_session
                    ),
                )
            )


        # ==================================
        # Math validation
        # ==================================

        math_validation: (
            MathValidationResult
            | None
        ) = None


        attempt_status: (
            AttemptStatus
            | None
        ) = None


        hint_level_before = (
            learning_session
            .current_hint_level
        )


        if (
            intent
            == TutorIntent
            .STUDENT_ATTEMPT
        ):

            if (
                learning_session
                .subject
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
                    math_validation
                    .status
                )


            else:

                attempt_status = (
                    AttemptStatus
                    .UNCLEAR
                )


        # ==================================
        # Tutor policy decision
        # ==================================

        decision_input = (
            TutorDecisionInput(
                intent=intent,

                attempt_status=(
                    attempt_status
                ),
            )
        )


        gateway = (
            LLMGateway()
        )


        decision = (
            TutorService
            .make_decision(
                db=db,

                session_id=(
                    session_id
                ),

                decision_input=(
                    decision_input
                ),

                model_used=(
                    gateway
                    .model_name
                ),
            )
        )


        refreshed_session = (
            LearningSessionRepository
            .get_by_id(
                db=db,

                session_id=(
                    session_id
                ),
            )
        )


        if (
            refreshed_session
            is None
        ):

            raise ValueError(
                "Learning session "
                "could not be "
                "reloaded."
            )


        # ==================================
        # Record deterministic Math attempt
        # ==================================

        if (
            math_validation
            is not None
        ):

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


            refreshed_session = (
                LearningSessionRepository
                .get_by_id(
                    db=db,

                    session_id=(
                        session_id
                    ),
                )
            )


            if (
                refreshed_session
                is None
            ):

                raise ValueError(
                    "Learning session "
                    "could not be "
                    "reloaded."
                )


        # ==================================
        # Automatic next problem
        #
        # After a correct Practice/Learn
        # attempt, assign the next actual
        # problem in the database.
        # ==================================

        next_problem_after_success = None


        if (
            math_validation
            is not None

            and math_validation.status
            == AttemptStatus.CORRECT

            and LearningMode(
                refreshed_session.mode
            )
            in {
                LearningMode.PRACTICE,
                LearningMode.LEARN,
            }
        ):

            previous_problem = (
                refreshed_session
                .current_problem
            )


            refreshed_session = (
                cls
                ._assign_next_math_problem(
                    db=db,

                    learning_session=(
                        refreshed_session
                    ),
                )
            )


            if (
                refreshed_session
                .current_problem

                and refreshed_session
                .current_problem
                != previous_problem
            ):

                next_problem_after_success = (
                    refreshed_session
                    .current_problem
                )


        # ==================================
        # Build current tutor state
        # ==================================

        state = (
            TutorSessionState(
                session_id=(
                    refreshed_session
                    .id
                ),

                student_id=(
                    refreshed_session
                    .student_id
                ),

                age_group=(
                    AgeGroup(
                        student
                        .age_group
                    )
                ),

                mode=(
                    LearningMode(
                        refreshed_session
                        .mode
                    )
                ),

                subject=(
                    Subject(
                        refreshed_session
                        .subject
                    )
                ),

                topic=(
                    refreshed_session
                    .topic
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

                mastery_state=(
                    MasteryState(
                        refreshed_session
                        .mastery_state
                    )
                ),

                adaptive_difficulty=(
                    decision
                    .adaptive_difficulty
                ),

                adaptive_support=(
                    decision
                    .adaptive_support
                ),

                explanation_depth=(
                    decision
                    .explanation_depth
                ),
            )
        )


        public_validation = (
            create_public_validation(
                math_validation
            )

            if math_validation
            is not None

            else None
        )


        # ==================================
        # Successful practice:
        # deterministic next problem
        # ==================================

        if (
            next_problem_after_success
            is not None
        ):

            if (
                state.mode
                == LearningMode.PRACTICE
            ):

                reply = (
                    "Correct — nice work. "
                    "Let's keep practicing. "
                    "Try this next problem: "
                    f"{next_problem_after_success}. "
                    "Try it independently first."
                )


            else:

                reply = (
                    "Correct. Now let's "
                    "check that the idea "
                    "is becoming independent. "
                    "Try this next problem: "
                    f"{next_problem_after_success}."
                )


            return (
                TutorMessageResponse(
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

                    rag_used=False,

                    rag_sources=[],

                    reply=reply,

                    provider="system",

                    model=(
                        "adaptive-practice"
                    ),

                    latency_ms=0.0,
                )
            )


        # ==================================
        # Other deterministic responses
        # ==================================

        deterministic_reply = (
            cls._deterministic_response(
                action=(
                    decision
                    .next_action
                ),

                state=state,
            )
        )


        if (
            deterministic_reply
            is not None
        ):

            return (
                TutorMessageResponse(
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

                    rag_used=False,

                    rag_sources=[],

                    reply=(
                        deterministic_reply
                    ),

                    provider="system",

                    model=(
                        "deterministic"
                    ),

                    latency_ms=0.0,
                )
            )


        # ==================================
        # RAG
        # ==================================

        rag_context: (
            RAGContext
            | None
        ) = None


        if (
            decision.requires_rag
        ):

            rag_service = (
                RAGService()
            )


            rag_context = (
                rag_service.retrieve(
                    query=(
                        student_message
                    ),

                    subject=(
                        state.subject.value
                    ),

                    concept_code=(
                        state.concept_code
                    ),
                )
            )


            if (
                not rag_context
                .has_context
            ):

                return (
                    TutorMessageResponse(
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

                        rag_used=False,

                        rag_sources=[],

                        reply=(
                            "I don't have enough "
                            "verified curriculum "
                            "material for this "
                            "question yet. Let's "
                            "choose another topic "
                            "or ask a trusted "
                            "teacher or learning "
                            "resource."
                        ),

                        provider="system",

                        model=(
                            "rag-grounding-guard"
                        ),

                        latency_ms=0.0,
                    )
                )


        # ==================================
        # LLM response
        # ==================================

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

                rag_context=(
                    rag_context
                ),
            )
        )


        result = (
            gateway.generate(
                request
            )
        )


        return (
            TutorMessageResponse(
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

                rag_used=bool(
                    rag_context
                    and rag_context
                    .has_context
                ),

                rag_sources=(
                    rag_context
                    .public_sources()

                    if rag_context
                    is not None

                    else []
                ),

                reply=(
                    result.content
                ),

                provider=(
                    result.provider
                ),

                model=(
                    result.model
                ),

                latency_ms=(
                    result.latency_ms
                ),
            )
        )


    # ======================================================
    # Assign deterministic adaptive problem
    # ======================================================

    @classmethod
    def _assign_next_math_problem(
        cls,
        db: Session,
        learning_session,
    ):

        concept_code = (
            learning_session
            .concept_code
        )


        if (
            concept_code
            is None
        ):

            return learning_session


        # ----------------------------------
        # Get current adaptive difficulty
        # ----------------------------------

        difficulty = (
            DifficultyLevel.EASY
        )


        try:

            plan = (
                AdaptiveLearningService
                .get_plan(
                    db=db,

                    student_id=(
                        learning_session
                        .student_id
                    ),

                    concept_code=(
                        concept_code
                    ),
                )
            )


            difficulty = (
                plan.difficulty
            )


        except (
            LookupError,
            ValueError,
        ):

            difficulty = (
                DifficultyLevel.EASY
            )


        # ----------------------------------
        # Use total historical attempts
        # so the problem sequence does
        # not reset every session.
        # ----------------------------------

        attempts = [
            attempt

            for attempt
            in (
                StudentAttemptRepository
                .list_by_student(
                    db=db,

                    student_id=(
                        learning_session
                        .student_id
                    ),
                )
            )

            if (
                attempt.problem_ref
                == concept_code
            )
        ]


        offset = (
            len(
                attempts
            )
        )


        problem = (
            get_adaptive_problem(
                concept_code=(
                    concept_code
                ),

                difficulty=(
                    difficulty
                ),

                offset=(
                    offset
                ),
            )
        )


        # ----------------------------------
        # Avoid immediately repeating
        # the same equation.
        # ----------------------------------

        if (
            problem
            is not None

            and problem.prompt
            == (
                learning_session
                .current_problem
            )
        ):

            problem = (
                get_adaptive_problem(
                    concept_code=(
                        concept_code
                    ),

                    difficulty=(
                        difficulty
                    ),

                    offset=(
                        offset + 1
                    ),
                )
            )


        if (
            problem
            is None
        ):

            return learning_session


        learning_session.current_problem = (
            problem.prompt
        )


        learning_session.current_hint_level = 0


        learning_session.attempt_count = 0


        learning_session.current_misconception = (
            None
        )


        return (
            LearningSessionRepository
            .save(
                db=db,

                learning_session=(
                    learning_session
                ),
            )
        )


    # ======================================================
    # Deterministic tutor messages
    # ======================================================

    @staticmethod
    def _deterministic_response(
        action: TutorAction,
        state: TutorSessionState,
    ) -> str | None:

        if (
            action
            == TutorAction
            .GENERATE_PRACTICE_QUESTION

            and state.current_problem
        ):

            return (
                "Here is your practice "
                "problem: "
                f"{state.current_problem}. "
                "Try it first and show "
                "me your answer or "
                "next step."
            )


        if (
            action
            == TutorAction
            .REFUSE_POLICY_BYPASS
        ):

            return (
                "I can help you work "
                "through the problem, "
                "but I won't skip the "
                "learning steps just "
                "to reveal the answer."
            )


        if (
            action
            == TutorAction
            .CLARIFY_TEST_INSTRUCTION
        ):

            return (
                "This is Mock Test "
                "Mode, so I can't give "
                "hints or solutions "
                "during the test."
            )


        if (
            action
            == TutorAction
            .ESCALATE_SAFETY
        ):

            return (
                "I can't handle this "
                "as a normal learning "
                "question. Please "
                "involve a trusted "
                "adult who can help."
            )


        return None