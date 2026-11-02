from app.adaptive.engine import (
    AdaptiveLearningEngine,
    AdaptiveSignals,
)
from app.schemas.adaptive import (
    AdaptiveActivity,
    AdaptiveSupport,
    ExplanationDepth,
)
from app.schemas.enums import (
    AgeGroup,
    DifficultyLevel,
    MasteryState,
)


def test_new_learner_gets_diagnostic():

    signals = AdaptiveSignals(
        age_group=(
            AgeGroup.DEVELOPING
        ),

        mastery_state=(
            MasteryState
            .NOT_STARTED
        ),

        recommended_difficulty=(
            DifficultyLevel.EASY
        ),

        diagnostic_score=None,

        mastery_score=None,

        total_attempts=0,

        independent_attempts=0,

        independent_attempt_rate=0,

        independent_success_rate=0,

        average_hint_level=0,

        direct_answer_requests=0,

        retry_success_count=0,
    )

    result = (
        AdaptiveLearningEngine
        .decide(
            signals
        )
    )

    assert (
        result.next_activity
        == AdaptiveActivity
        .TAKE_DIAGNOSTIC
    )

    assert (
        result.difficulty
        == DifficultyLevel.EASY
    )


def test_struggling_learner_gets_more_support():

    signals = AdaptiveSignals(
        age_group=(
            AgeGroup.DEVELOPING
        ),

        mastery_state=(
            MasteryState.LEARNING
        ),

        recommended_difficulty=(
            DifficultyLevel
            .MODERATE
        ),

        diagnostic_score=40,

        mastery_score=None,

        total_attempts=4,

        independent_attempts=2,

        independent_attempt_rate=50,

        independent_success_rate=0,

        average_hint_level=4.5,

        direct_answer_requests=2,

        retry_success_count=0,
    )

    result = (
        AdaptiveLearningEngine
        .decide(
            signals
        )
    )

    assert (
        result.difficulty
        == DifficultyLevel.EASY
    )

    assert (
        result.support_level
        == AdaptiveSupport.STRONG
    )

    assert (
        result.next_activity
        == AdaptiveActivity
        .REVIEW_FOUNDATION
    )


def test_ready_learner_gets_mastery_check():

    signals = AdaptiveSignals(
        age_group=(
            AgeGroup.DEVELOPING
        ),

        mastery_state=(
            MasteryState
            .DEVELOPING
        ),

        recommended_difficulty=(
            DifficultyLevel
            .MODERATE
        ),

        diagnostic_score=60,

        mastery_score=None,

        total_attempts=4,

        independent_attempts=3,

        independent_attempt_rate=75,

        independent_success_rate=70,

        average_hint_level=1.5,

        direct_answer_requests=0,

        retry_success_count=1,
    )

    result = (
        AdaptiveLearningEngine
        .decide(
            signals
        )
    )

    assert (
        result.next_activity
        == AdaptiveActivity
        .TAKE_MASTERY_CHECK
    )


def test_strong_mastery_gets_challenge():

    signals = AdaptiveSignals(
        age_group=(
            AgeGroup.INDEPENDENT
        ),

        mastery_state=(
            MasteryState.STRONG
        ),

        recommended_difficulty=(
            DifficultyLevel
            .CHALLENGING
        ),

        diagnostic_score=60,

        mastery_score=90,

        total_attempts=5,

        independent_attempts=5,

        independent_attempt_rate=100,

        independent_success_rate=100,

        average_hint_level=0.5,

        direct_answer_requests=0,

        retry_success_count=1,
    )

    result = (
        AdaptiveLearningEngine
        .decide(
            signals
        )
    )

    assert (
        result.next_activity
        == AdaptiveActivity
        .CHALLENGE_PRACTICE
    )

    assert (
        result.difficulty
        == DifficultyLevel
        .CHALLENGING
    )

    assert (
        result.explanation_depth
        == ExplanationDepth.DEEP
    )