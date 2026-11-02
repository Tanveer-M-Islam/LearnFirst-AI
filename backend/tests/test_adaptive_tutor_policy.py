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
    TutorDecisionInput,
)
from app.tutor.policy_engine import (
    TutorPolicyEngine,
)
from app.tutor.session_state import (
    TutorSessionState,
)


def make_state(
    support: AdaptiveSupport,
) -> TutorSessionState:

    return TutorSessionState(
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

        hint_level=0,

        direct_answer_requests=0,

        current_misconception=None,

        mastery_state=(
            MasteryState.LEARNING
        ),

        adaptive_difficulty=(
            DifficultyLevel
            .MODERATE
        ),

        adaptive_support=(
            support
        ),

        explanation_depth=(
            ExplanationDepth
            .BALANCED
        ),
    )


def test_gentle_support_starts_small():

    engine = TutorPolicyEngine()

    result = engine.decide(
        state=make_state(
            AdaptiveSupport.GENTLE
        ),

        decision_input=(
            TutorDecisionInput(
                intent=(
                    TutorIntent
                    .HINT_REQUEST
                )
            )
        ),
    )

    assert result.hint_level == 1

    assert (
        result.next_action
        == TutorAction.GIVE_HINT
    )


def test_guided_support_starts_with_guidance():

    engine = TutorPolicyEngine()

    result = engine.decide(
        state=make_state(
            AdaptiveSupport.GUIDED
        ),

        decision_input=(
            TutorDecisionInput(
                intent=(
                    TutorIntent
                    .HINT_REQUEST
                )
            )
        ),
    )

    assert result.hint_level == 2

    assert (
        result.next_action
        == TutorAction
        .ASK_GUIDING_QUESTION
    )


def test_strong_support_reaches_example_faster():

    engine = TutorPolicyEngine()

    result = engine.decide(
        state=make_state(
            AdaptiveSupport.STRONG
        ),

        decision_input=(
            TutorDecisionInput(
                intent=(
                    TutorIntent
                    .HINT_REQUEST
                )
            )
        ),
    )

    assert result.hint_level == 4

    assert (
        result.next_action
        == TutorAction
        .GIVE_SIMILAR_EXAMPLE
    )


def test_strong_support_does_not_break_answer_policy():

    engine = TutorPolicyEngine()

    state = make_state(
        AdaptiveSupport.STRONG
    )

    state.attempt_count = 0

    result = engine.decide(
        state=state,

        decision_input=(
            TutorDecisionInput(
                intent=(
                    TutorIntent
                    .DIRECT_ANSWER_REQUEST
                )
            )
        ),
    )

    assert (
        result.allow_final_answer
        is False
    )

    assert (
        result.next_action
        == TutorAction.ASK_ATTEMPT
    )