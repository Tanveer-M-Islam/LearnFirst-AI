from sqlalchemy.orm import Session

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
from app.english.attempt_service import (
    EnglishAttemptService,
)
from app.english.evaluator import (
    EnglishEvaluator,
)
from app.english.models import (
    EnglishValidationResult,
    create_public_english_validation,
)
from app.english.question_bank import (
    get_english_question,
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
from app.rag.query_builder import (
    RAGQueryBuilder,
)
from app.rag.service import (
    RAGService,
)
from app.science.attempt_service import (
    ScienceAttemptService,
)
from app.science.evaluator import (
    ScienceUnderstandingEvaluator,
)
from app.science.models import (
    ScienceValidationResult,
    create_public_science_validation,
)
from app.science.question_bank import (
    get_science_question,
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
from app.services.english_adaptive_learning_service import (
    EnglishAdaptiveLearningService,
)
from app.services.science_adaptive_learning_service import (
    ScienceAdaptiveLearningService,
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


        mode = LearningMode(
            learning_session.mode
        )


        intent = (
            IntentRouter.classify(
                student_message
            )
        )


        # ==================================
        # New practice request
        # ==================================

        if (
            intent
            == TutorIntent.PRACTICE_REQUEST
        ):

            if (
                subject == Subject.MATH

                and mode
                in {
                    LearningMode.PRACTICE,
                    LearningMode.LEARN,
                }
            ):

                learning_session = (
                    cls._assign_next_math_problem(
                        db=db,

                        learning_session=(
                            learning_session
                        ),
                    )
                )


            elif (
                subject == Subject.SCIENCE
            ):

                learning_session = (
                    cls._assign_next_science_question(
                        db=db,

                        learning_session=(
                            learning_session
                        ),
                    )
                )


            elif (
                subject == Subject.ENGLISH
            ):

                learning_session = (
                    cls._assign_next_english_question(
                        db=db,

                        learning_session=(
                            learning_session
                        ),
                    )
                )


        # ==================================
        # Natural Science response
        # ==================================

        if (
            subject == Subject.SCIENCE

            and learning_session.current_problem

            and (
                intent
                == TutorIntent.LEARN_CONCEPT
            )

            and (
                ScienceUnderstandingEvaluator
                .looks_like_answer(
                    student_message
                )
            )
        ):

            intent = (
                TutorIntent.STUDENT_ATTEMPT
            )


        # ==================================
        # Natural English response
        #
        # "goes", "dog", complete sentences,
        # reading explanations, etc. should
        # count as attempts.
        # ==================================

        if (
            subject == Subject.ENGLISH

            and learning_session.current_problem

            and (
                intent
                == TutorIntent.LEARN_CONCEPT
            )

            and (
                EnglishEvaluator.looks_like_answer(
                    student_message
                )
            )
        ):

            intent = (
                TutorIntent.STUDENT_ATTEMPT
            )


        # ==================================
        # Validation
        # ==================================

        math_validation: (
            MathValidationResult
            | None
        ) = None


        science_validation: (
            ScienceValidationResult
            | None
        ) = None


        english_validation: (
            EnglishValidationResult
            | None
        ) = None


        attempt_status: (
            AttemptStatus
            | None
        ) = None


        hint_level_before = (
            learning_session.current_hint_level
        )


        if (
            intent == TutorIntent.STUDENT_ATTEMPT
        ):

            if (
                subject == Subject.MATH

                and learning_session.current_problem
            ):

                math_validation = (
                    MathAttemptService.analyze(
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


            elif (
                subject == Subject.SCIENCE

                and learning_session.current_problem

                and learning_session.concept_code
            ):

                science_validation = (
                    ScienceAttemptService.analyze(
                        concept_code=(
                            learning_session
                            .concept_code
                        ),

                        question_prompt=(
                            learning_session
                            .current_problem
                        ),

                        student_message=(
                            student_message
                        ),
                    )
                )


                attempt_status = (
                    science_validation.status
                )


            elif (
                subject == Subject.ENGLISH

                and learning_session.current_problem

                and learning_session.concept_code
            ):

                english_validation = (
                    EnglishAttemptService.analyze(
                        concept_code=(
                            learning_session
                            .concept_code
                        ),

                        question_prompt=(
                            learning_session
                            .current_problem
                        ),

                        student_message=(
                            student_message
                        ),
                    )
                )


                attempt_status = (
                    english_validation.status
                )


            else:

                attempt_status = (
                    AttemptStatus.UNCLEAR
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


        gateway = LLMGateway()


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


        refreshed_session = (
            LearningSessionRepository.get_by_id(
                db=db,
                session_id=session_id,
            )
        )


        if (
            refreshed_session is None
        ):

            raise ValueError(
                "Learning session could "
                "not be reloaded."
            )


        # ==================================
        # Record Math
        # ==================================

        if (
            math_validation is not None
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


        # ==================================
        # Record Science
        # ==================================

        if (
            science_validation is not None
        ):

            ScienceAttemptService.record(
                db=db,

                learning_session=(
                    refreshed_session
                ),

                student_message=(
                    student_message
                ),

                validation=(
                    science_validation
                ),

                hint_level_before=(
                    hint_level_before
                ),
            )


        # ==================================
        # Record English
        # ==================================

        if (
            english_validation is not None
        ):

            EnglishAttemptService.record(
                db=db,

                learning_session=(
                    refreshed_session
                ),

                student_message=(
                    student_message
                ),

                validation=(
                    english_validation
                ),

                hint_level_before=(
                    hint_level_before
                ),
            )


        refreshed_session = (
            LearningSessionRepository.get_by_id(
                db=db,
                session_id=session_id,
            )
        )


        if (
            refreshed_session is None
        ):

            raise ValueError(
                "Learning session could "
                "not be reloaded."
            )


        # ==================================
        # Automatic next Math problem
        # ==================================

        next_math_problem = None


        if (
            math_validation is not None

            and (
                math_validation.status
                == AttemptStatus.CORRECT
            )

            and (
                LearningMode(
                    refreshed_session.mode
                )
                in {
                    LearningMode.PRACTICE,
                    LearningMode.LEARN,
                }
            )
        ):

            previous_problem = (
                refreshed_session.current_problem
            )


            refreshed_session = (
                cls._assign_next_math_problem(
                    db=db,

                    learning_session=(
                        refreshed_session
                    ),
                )
            )


            if (
                refreshed_session.current_problem

                and (
                    refreshed_session
                    .current_problem
                    != previous_problem
                )
            ):

                next_math_problem = (
                    refreshed_session
                    .current_problem
                )


        # ==================================
        # Automatic next Science question
        # ==================================

        next_science_question = None


        if (
            science_validation is not None

            and (
                science_validation.status
                == AttemptStatus.CORRECT
            )
        ):

            previous_question = (
                refreshed_session.current_problem
            )


            refreshed_session = (
                cls._assign_next_science_question(
                    db=db,

                    learning_session=(
                        refreshed_session
                    ),
                )
            )


            if (
                refreshed_session.current_problem

                and (
                    refreshed_session
                    .current_problem
                    != previous_question
                )
            ):

                next_science_question = (
                    refreshed_session
                    .current_problem
                )


        # ==================================
        # Automatic next English question
        # ==================================

        next_english_question = None


        if (
            english_validation is not None

            and (
                english_validation.status
                == AttemptStatus.CORRECT
            )
        ):

            previous_question = (
                refreshed_session.current_problem
            )


            refreshed_session = (
                cls._assign_next_english_question(
                    db=db,

                    learning_session=(
                        refreshed_session
                    ),
                )
            )


            if (
                refreshed_session.current_problem

                and (
                    refreshed_session
                    .current_problem
                    != previous_question
                )
            ):

                next_english_question = (
                    refreshed_session
                    .current_problem
                )


        # ==================================
        # Tutor state
        # ==================================

        state = (
            TutorSessionState(
                session_id=(
                    refreshed_session.id
                ),

                student_id=(
                    refreshed_session.student_id
                ),

                age_group=(
                    AgeGroup(
                        student.age_group
                    )
                ),

                mode=(
                    LearningMode(
                        refreshed_session.mode
                    )
                ),

                subject=(
                    Subject(
                        refreshed_session.subject
                    )
                ),

                topic=(
                    refreshed_session.topic
                ),

                concept_code=(
                    refreshed_session.concept_code
                ),

                current_problem=(
                    refreshed_session.current_problem
                ),

                attempt_count=(
                    refreshed_session.attempt_count
                ),

                hint_level=(
                    refreshed_session.current_hint_level
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
                        refreshed_session.mastery_state
                    )
                ),

                adaptive_difficulty=(
                    decision.adaptive_difficulty
                ),

                adaptive_support=(
                    decision.adaptive_support
                ),

                explanation_depth=(
                    decision.explanation_depth
                ),
            )
        )


        public_math_validation = (
            create_public_validation(
                math_validation
            )

            if math_validation is not None

            else None
        )


        public_science_validation = (
            create_public_science_validation(
                science_validation
            )

            if science_validation is not None

            else None
        )


        public_english_validation = (
            create_public_english_validation(
                english_validation
            )

            if english_validation is not None

            else None
        )


        # ==================================
        # Correct Math → next problem
        # ==================================

        if (
            next_math_problem is not None
        ):

            reply = (
                "Correct. Now try this "
                "next problem: "
                f"{next_math_problem}"
            )


            return (
                TutorMessageResponse(
                    session_id=session_id,

                    student_message=(
                        student_message
                    ),

                    detected_intent=intent,

                    decision=decision,

                    math_validation=(
                        public_math_validation
                    ),

                    science_validation=None,

                    english_validation=None,

                    rag_used=False,

                    rag_sources=[],

                    reply=reply,

                    provider="system",

                    model="adaptive-practice",

                    latency_ms=0.0,
                )
            )


        # ==================================
        # Correct Science → next question
        # ==================================

        if (
            next_science_question is not None

            and science_validation is not None
        ):

            recognized = ", ".join(
                science_validation.matched_ideas[
                    :3
                ]
            )


            if recognized:

                reply = (
                    "Your explanation included "
                    "the important ideas about "
                    f"{recognized}. "
                    "Now try this next question: "
                    f"{next_science_question}"
                )

            else:

                reply = (
                    "Your explanation shows "
                    "the main idea. "
                    "Now try this next question: "
                    f"{next_science_question}"
                )


            return (
                TutorMessageResponse(
                    session_id=session_id,

                    student_message=(
                        student_message
                    ),

                    detected_intent=intent,

                    decision=decision,

                    math_validation=None,

                    science_validation=(
                        public_science_validation
                    ),

                    english_validation=None,

                    rag_used=False,

                    rag_sources=[],

                    reply=reply,

                    provider="system",

                    model="science-rubric",

                    latency_ms=0.0,
                )
            )


        # ==================================
        # Correct English → next question
        # ==================================

        if (
            next_english_question is not None

            and english_validation is not None
        ):

            recognized = ", ".join(
                english_validation.matched_ideas[
                    :2
                ]
            )


            if recognized:

                reply = (
                    "Good. Your response "
                    "included "
                    f"{recognized}. "
                    "Now try this next "
                    "English question: "
                    f"{next_english_question}"
                )

            else:

                reply = (
                    "That response is correct. "
                    "Now try this next "
                    "English question: "
                    f"{next_english_question}"
                )


            return (
                TutorMessageResponse(
                    session_id=session_id,

                    student_message=(
                        student_message
                    ),

                    detected_intent=intent,

                    decision=decision,

                    math_validation=None,

                    science_validation=None,

                    english_validation=(
                        public_english_validation
                    ),

                    rag_used=False,

                    rag_sources=[],

                    reply=reply,

                    provider="system",

                    model="english-rubric",

                    latency_ms=0.0,
                )
            )


        # ==================================
        # Deterministic system responses
        # ==================================

        deterministic_reply = (
            cls._deterministic_response(
                action=(
                    decision.next_action
                ),

                state=state,
            )
        )


        if (
            deterministic_reply is not None
        ):

            return (
                TutorMessageResponse(
                    session_id=session_id,

                    student_message=(
                        student_message
                    ),

                    detected_intent=intent,

                    decision=decision,

                    math_validation=(
                        public_math_validation
                    ),

                    science_validation=(
                        public_science_validation
                    ),

                    english_validation=(
                        public_english_validation
                    ),

                    rag_used=False,

                    rag_sources=[],

                    reply=(
                        deterministic_reply
                    ),

                    provider="system",

                    model="deterministic",

                    latency_ms=0.0,
                )
            )


        # ==================================
        # RAG
        #
        # Currently used for Science.
        # English RAG will be a future
        # extension if we need curriculum
        # passages/documents.
        # ==================================

        rag_context: (
            RAGContext
            | None
        ) = None


        if (
            decision.requires_rag
        ):

            rag_service = RAGService()


            rag_query = (
                RAGQueryBuilder.build(
                    student_message=(
                        student_message
                    ),

                    subject=(
                        state.subject
                    ),

                    topic=(
                        state.topic
                    ),

                    concept_code=(
                        state.concept_code
                    ),

                    current_problem=(
                        state.current_problem
                    ),
                )
            )


            rag_context = (
                rag_service.retrieve(
                    query=rag_query,

                    subject=(
                        state.subject.value
                    ),

                    concept_code=(
                        state.concept_code
                    ),
                )
            )


            if (
                not rag_context.has_context
            ):

                return (
                    TutorMessageResponse(
                        session_id=session_id,

                        student_message=(
                            student_message
                        ),

                        detected_intent=intent,

                        decision=decision,

                        math_validation=(
                            public_math_validation
                        ),

                        science_validation=(
                            public_science_validation
                        ),

                        english_validation=(
                            public_english_validation
                        ),

                        rag_used=False,

                        rag_sources=[],

                        reply=(
                            "I don't have enough "
                            "verified curriculum "
                            "material for this "
                            "question yet."
                        ),

                        provider="system",

                        model=(
                            "rag-grounding-guard"
                        ),

                        latency_ms=0.0,
                    )
                )


        # ==================================
        # LLM Tutor
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

                science_validation=(
                    science_validation
                ),

                english_validation=(
                    english_validation
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
                session_id=session_id,

                student_message=(
                    student_message
                ),

                detected_intent=intent,

                decision=decision,

                math_validation=(
                    public_math_validation
                ),

                science_validation=(
                    public_science_validation
                ),

                english_validation=(
                    public_english_validation
                ),

                rag_used=bool(
                    rag_context
                    and rag_context.has_context
                ),

                rag_sources=(
                    rag_context.public_sources()

                    if rag_context is not None

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


    # ======================================
    # Math next problem
    # ======================================

    @classmethod
    def _assign_next_math_problem(
        cls,
        db: Session,
        learning_session,
    ):

        concept_code = (
            learning_session.concept_code
        )


        if (
            concept_code is None
        ):
            return learning_session


        difficulty = (
            DifficultyLevel.EASY
        )


        try:

            plan = (
                AdaptiveLearningService.get_plan(
                    db=db,

                    student_id=(
                        learning_session.student_id
                    ),

                    concept_code=concept_code,
                )
            )


            difficulty = plan.difficulty

        except (
            LookupError,
            ValueError,
        ):

            pass


        attempts = [
            attempt

            for attempt
            in (
                StudentAttemptRepository
                .list_by_student(
                    db=db,

                    student_id=(
                        learning_session.student_id
                    ),
                )
            )

            if (
                attempt.problem_ref
                == concept_code
            )
        ]


        offset = len(
            attempts
        )


        problem = (
            get_adaptive_problem(
                concept_code=concept_code,

                difficulty=difficulty,

                offset=offset,
            )
        )


        if (
            problem is not None

            and (
                problem.prompt
                == learning_session.current_problem
            )
        ):

            problem = (
                get_adaptive_problem(
                    concept_code=concept_code,

                    difficulty=difficulty,

                    offset=offset + 1,
                )
            )


        if (
            problem is None
        ):
            return learning_session


        learning_session.current_problem = (
            problem.prompt
        )

        learning_session.current_hint_level = 0

        learning_session.attempt_count = 0

        learning_session.current_misconception = None


        return (
            LearningSessionRepository.save(
                db=db,

                learning_session=(
                    learning_session
                ),
            )
        )


    # ======================================
    # Science next question
    # ======================================

    @classmethod
    def _assign_next_science_question(
        cls,
        db: Session,
        learning_session,
    ):

        concept_code = (
            learning_session.concept_code
        )


        if (
            concept_code is None
        ):
            return learning_session


        difficulty = (
            DifficultyLevel.EASY
        )


        try:

            plan = (
                ScienceAdaptiveLearningService
                .get_plan(
                    db=db,

                    student_id=(
                        learning_session.student_id
                    ),

                    concept_code=concept_code,
                )
            )


            difficulty = plan.difficulty

        except (
            LookupError,
            ValueError,
        ):

            pass


        attempts = [
            attempt

            for attempt
            in (
                StudentAttemptRepository
                .list_by_student(
                    db=db,

                    student_id=(
                        learning_session.student_id
                    ),
                )
            )

            if (
                attempt.problem_ref
                == concept_code
            )
        ]


        offset = len(
            attempts
        )


        question = (
            get_science_question(
                concept_code=concept_code,

                offset=offset,

                difficulty=difficulty,
            )
        )


        if (
            question is not None

            and (
                question.prompt
                == learning_session.current_problem
            )
        ):

            question = (
                get_science_question(
                    concept_code=concept_code,

                    offset=offset + 1,

                    difficulty=difficulty,
                )
            )


        if (
            question is None
        ):
            return learning_session


        learning_session.current_problem = (
            question.prompt
        )

        learning_session.current_hint_level = 0

        learning_session.attempt_count = 0

        learning_session.current_misconception = None


        return (
            LearningSessionRepository.save(
                db=db,

                learning_session=(
                    learning_session
                ),
            )
        )


    # ======================================
    # English next question
    # ======================================

    @classmethod
    def _assign_next_english_question(
        cls,
        db: Session,
        learning_session,
    ):

        concept_code = (
            learning_session.concept_code
        )


        if (
            concept_code is None
        ):
            return learning_session


        difficulty = (
            DifficultyLevel.EASY
        )


        try:

            plan = (
                EnglishAdaptiveLearningService
                .get_plan(
                    db=db,

                    student_id=(
                        learning_session.student_id
                    ),

                    concept_code=concept_code,
                )
            )


            difficulty = plan.difficulty

        except (
            LookupError,
            ValueError,
        ):

            pass


        attempts = [
            attempt

            for attempt
            in (
                StudentAttemptRepository
                .list_by_student(
                    db=db,

                    student_id=(
                        learning_session.student_id
                    ),
                )
            )

            if (
                attempt.problem_ref
                == concept_code
            )
        ]


        offset = len(
            attempts
        )


        question = (
            get_english_question(
                concept_code=concept_code,

                offset=offset,

                difficulty=difficulty,
            )
        )


        if (
            question is not None

            and (
                question.prompt
                == learning_session.current_problem
            )
        ):

            question = (
                get_english_question(
                    concept_code=concept_code,

                    offset=offset + 1,

                    difficulty=difficulty,
                )
            )


        if (
            question is None
        ):
            return learning_session


        learning_session.current_problem = (
            question.prompt
        )

        learning_session.current_hint_level = 0

        learning_session.attempt_count = 0

        learning_session.current_misconception = None


        return (
            LearningSessionRepository.save(
                db=db,

                learning_session=(
                    learning_session
                ),
            )
        )


    # ======================================
    # Deterministic responses
    # ======================================

    @staticmethod
    def _deterministic_response(
        action: TutorAction,
        state: TutorSessionState,
    ) -> str | None:

        if (
            action
            == TutorAction.GENERATE_PRACTICE_QUESTION

            and state.current_problem
        ):

            if (
                state.subject
                == Subject.SCIENCE
            ):

                return (
                    "Here is your Science "
                    "question: "
                    f"{state.current_problem} "
                    "Explain the idea in "
                    "your own words."
                )


            if (
                state.subject
                == Subject.ENGLISH
            ):

                return (
                    "Here is your English "
                    "question: "
                    f"{state.current_problem} "
                    "Try it independently first."
                )


            return (
                "Here is your practice "
                "problem: "
                f"{state.current_problem}. "
                "Try it first and show "
                "me your answer or next step."
            )


        if (
            action
            == TutorAction.REFUSE_POLICY_BYPASS
        ):

            return (
                "I can help you work "
                "through the task, but "
                "I won't skip the learning "
                "steps just to reveal "
                "the answer."
            )


        if (
            action
            == TutorAction.CLARIFY_TEST_INSTRUCTION
        ):

            return (
                "This is Mock Test Mode, "
                "so I can't give hints "
                "or solutions during "
                "the test."
            )


        if (
            action
            == TutorAction.ESCALATE_SAFETY
        ):

            return (
                "I can't handle this "
                "as a normal learning "
                "question. Please involve "
                "a trusted adult who "
                "can help."
            )


        return None