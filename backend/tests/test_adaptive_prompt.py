from app.schemas.adaptive import (
    AdaptiveSupport,
    ExplanationDepth,
)
from app.schemas.enums import (
    AgeGroup,
    DifficultyLevel,
    LearningMode,
    MasteryState,
    Subject,
    TutorAction,
    TutorIntent,
)
from app.tutor.decision_models import (
    TutorDecisionResult,
)
from app.tutor.prompt_builder import (
    TutorPromptBuilder,
)
from app.tutor.session_state import (
    TutorSessionState,
)


def test_adaptive_profile_is_added_to_prompt():

    state = TutorSessionState(
        session_id="session-1",

        student_id="student-1",

        age_group=(
            AgeGroup.DEVELOPING
        ),

        mode=(
            LearningMode.PRACTICE
        ),

        subject=(
            Subject.MATH
        ),

        topic=(
            "Linear Equations"
        ),

        concept_code=(
            "MATH_ALG_LINEAR_01"
        ),

        current_problem=(
            "2x + 5 = 17"
        ),

        attempt_count=1,

        hint_level=1,

        direct_answer_requests=0,

        mastery_state=(
            MasteryState.LEARNING
        ),
    )


    decision = TutorDecisionResult(
        session_id="session-1",

        student_id="student-1",

        subject=Subject.MATH,

        mode=LearningMode.PRACTICE,

        age_group=(
            AgeGroup.DEVELOPING
        ),

        intent=(
            TutorIntent.HINT_REQUEST
        ),

        next_action=(
            TutorAction
            .ASK_GUIDING_QUESTION
        ),

        hint_level=2,

        allow_final_answer=False,

        requires_rag=False,

        requires_validation=False,

        requires_mastery_check=False,

        policy_bypass_detected=False,

        reason="Adaptive test.",

        adaptive_difficulty=(
            DifficultyLevel.MODERATE
        ),

        adaptive_support=(
            AdaptiveSupport.GUIDED
        ),

        explanation_depth=(
            ExplanationDepth
            .BALANCED
        ),
    )


    request = (
        TutorPromptBuilder.build(
            student_message=(
                "Can I have a hint?"
            ),

            state=state,

            decision=decision,
        )
    )


    prompt = (
        request.messages[0]
        .content
    )


    assert (
        "ADAPTIVE DIFFICULTY:"
        in prompt
    )

    assert (
        "MODERATE"
        in prompt
    )

    assert (
        "GUIDED"
        in prompt
    )

    assert (
        "BALANCED"
        in prompt
    )