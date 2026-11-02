from app.science.adaptive_engine import (
    ScienceAdaptiveEngine,
    ScienceAdaptiveSignals,
)
from app.schemas.adaptive import (
    AdaptiveSupport,
    ResponsePace,
)
from app.schemas.enums import (
    AgeGroup,
    DifficultyLevel,
    MasteryState,
)
from app.schemas.science_adaptive import (
    ScienceAdaptiveActivity,
)


def test_new_science_learner_starts_easy():

    signals = (
        ScienceAdaptiveSignals(
            age_group=(
                AgeGroup.DEVELOPING
            ),

            total_attempts=0,

            correct_attempts=0,

            partial_attempts=0,

            understanding_score_percent=0.0,

            independent_attempt_rate=0.0,

            independent_success_rate=0.0,

            average_hint_level=0.0,

            misconception_count=0,

            direct_answer_requests=0,
        )
    )


    result = (
        ScienceAdaptiveEngine
        .decide(
            signals
        )
    )


    assert (
        result.mastery_state
        == MasteryState.NOT_STARTED
    )


    assert (
        result.difficulty
        == DifficultyLevel.EASY
    )


    assert (
        result.next_activity
        == (
            ScienceAdaptiveActivity
            .START_LEARNING
        )
    )


def test_low_independent_success_is_struggle():

    signals = (
        ScienceAdaptiveSignals(
            age_group=(
                AgeGroup.DEVELOPING
            ),

            total_attempts=3,

            correct_attempts=1,

            partial_attempts=1,

            understanding_score_percent=50.0,

            independent_attempt_rate=66.7,

            independent_success_rate=0.0,

            average_hint_level=0.67,

            misconception_count=0,

            direct_answer_requests=0,

            measured_response_count=8,

            average_response_latency_ms=(
                32_140.2
            ),

            baseline_ready=True,

            personalized_response_pace=(
                ResponsePace.FAST
            ),
        )
    )


    result = (
        ScienceAdaptiveEngine
        .decide(
            signals
        )
    )


    assert (
        result.mastery_state
        == MasteryState.DEVELOPING
    )


    assert (
        result.response_pace
        == ResponsePace.FAST
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
        == (
            ScienceAdaptiveActivity
            .REVIEW_CONCEPT
        )
    )


    assert (
        "LOW_INDEPENDENT_SUCCESS"
        in result.reason_codes
    )


def test_repeated_science_struggle_gets_strong_support():

    signals = (
        ScienceAdaptiveSignals(
            age_group=(
                AgeGroup.DEVELOPING
            ),

            total_attempts=4,

            correct_attempts=0,

            partial_attempts=1,

            understanding_score_percent=12.5,

            independent_attempt_rate=75.0,

            independent_success_rate=0.0,

            average_hint_level=3.0,

            misconception_count=2,

            direct_answer_requests=1,
        )
    )


    result = (
        ScienceAdaptiveEngine
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
        == (
            ScienceAdaptiveActivity
            .REVIEW_CONCEPT
        )
    )


def test_strong_science_performance_advances():

    signals = (
        ScienceAdaptiveSignals(
            age_group=(
                AgeGroup.DEVELOPING
            ),

            total_attempts=5,

            correct_attempts=5,

            partial_attempts=0,

            understanding_score_percent=100.0,

            independent_attempt_rate=80.0,

            independent_success_rate=100.0,

            average_hint_level=1.0,

            misconception_count=0,

            direct_answer_requests=0,
        )
    )


    result = (
        ScienceAdaptiveEngine
        .decide(
            signals
        )
    )


    assert (
        result.mastery_state
        == MasteryState.STRONG
    )


    assert (
        result.difficulty
        == (
            DifficultyLevel
            .CHALLENGING
        )
    )


    assert (
        result.support_level
        == AdaptiveSupport.GENTLE
    )


    assert (
        result.next_activity
        == (
            ScienceAdaptiveActivity
            .CHALLENGE_QUESTION
        )
    )


def test_slow_response_alone_does_not_penalize():

    signals = (
        ScienceAdaptiveSignals(
            age_group=(
                AgeGroup.DEVELOPING
            ),

            total_attempts=5,

            correct_attempts=5,

            partial_attempts=0,

            understanding_score_percent=100.0,

            independent_attempt_rate=80.0,

            independent_success_rate=100.0,

            average_hint_level=1.0,

            misconception_count=0,

            direct_answer_requests=0,

            measured_response_count=5,

            average_response_latency_ms=(
                50_000.0
            ),
        )
    )


    result = (
        ScienceAdaptiveEngine
        .decide(
            signals
        )
    )


    assert (
        result.response_pace
        == ResponsePace.SLOW
    )


    assert (
        result.difficulty
        == (
            DifficultyLevel
            .CHALLENGING
        )
    )


    assert (
        result.next_activity
        == (
            ScienceAdaptiveActivity
            .CHALLENGE_QUESTION
        )
    )


def test_slow_response_plus_struggle_increases_support():

    signals = (
        ScienceAdaptiveSignals(
            age_group=(
                AgeGroup.DEVELOPING
            ),

            total_attempts=4,

            correct_attempts=1,

            partial_attempts=1,

            understanding_score_percent=37.5,

            independent_attempt_rate=75.0,

            independent_success_rate=25.0,

            average_hint_level=3.0,

            misconception_count=1,

            direct_answer_requests=0,

            measured_response_count=4,

            average_response_latency_ms=(
                55_000.0
            ),
        )
    )


    result = (
        ScienceAdaptiveEngine
        .decide(
            signals
        )
    )


    assert (
        result.response_pace
        == ResponsePace.SLOW
    )


    assert (
        result.support_level
        == AdaptiveSupport.STRONG
    )


    assert (
        result.difficulty
        == DifficultyLevel.EASY
    )


    assert (
        result.next_activity
        == (
            ScienceAdaptiveActivity
            .REVIEW_CONCEPT
        )
    )