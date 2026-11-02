from app.adaptive.engine import (
    AdaptiveLearningEngine,
    AdaptiveSignals,
)
from app.schemas.adaptive import (
    AdaptiveActivity,
    AdaptiveSupport,
    ResponsePace,
)
from app.schemas.enums import (
    AgeGroup,
    DifficultyLevel,
    MasteryState,
)


def make_signals(
    **overrides,
) -> AdaptiveSignals:

    values = {
        "age_group":
            AgeGroup.DEVELOPING,

        "mastery_state":
            MasteryState.LEARNING,

        "recommended_difficulty":
            DifficultyLevel.MODERATE,

        "diagnostic_score":
            60.0,

        "mastery_score":
            None,

        "total_attempts":
            4,

        "independent_attempts":
            3,

        "independent_attempt_rate":
            75.0,

        "independent_success_rate":
            70.0,

        "average_hint_level":
            1.0,

        "direct_answer_requests":
            0,

        "retry_success_count":
            1,

        "measured_response_count":
            3,

        "average_response_latency_ms":
            25_000.0,
    }


    values.update(
        overrides
    )


    return AdaptiveSignals(
        **values
    )


def test_typical_latency_does_not_change_plan():

    result = (
        AdaptiveLearningEngine
        .decide(
            make_signals(
                average_response_latency_ms=(
                    24_000.0
                )
            )
        )
    )


    assert (
        result.response_pace
        == ResponsePace.TYPICAL
    )


    assert (
        "SLOW_RESPONSE_WITH_STRUGGLE"
        not in result.reason_codes
    )


    assert (
        "FAST_RESPONSE_WITH_STRONG_PERFORMANCE"
        not in result.reason_codes
    )


def test_slow_response_alone_does_not_penalize():

    result = (
        AdaptiveLearningEngine
        .decide(
            make_signals(
                average_response_latency_ms=(
                    55_000.0
                ),

                independent_success_rate=(
                    90.0
                ),

                average_hint_level=(
                    1.0
                ),
            )
        )
    )


    assert (
        result.response_pace
        == ResponsePace.SLOW
    )


    assert (
        "SLOW_RESPONSE_WITH_STRUGGLE"
        not in result.reason_codes
    )


def test_slow_and_struggling_gets_more_support():

    result = (
        AdaptiveLearningEngine
        .decide(
            make_signals(
                average_response_latency_ms=(
                    55_000.0
                ),

                independent_success_rate=(
                    60.0
                ),

                average_hint_level=(
                    3.0
                ),
            )
        )
    )


    assert (
        result.response_pace
        == ResponsePace.SLOW
    )


    assert (
        "SLOW_RESPONSE_WITH_STRUGGLE"
        in result.reason_codes
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


    assert (
        result.difficulty
        == DifficultyLevel.EASY
    )


def test_fast_with_good_performance_can_advance():

    result = (
        AdaptiveLearningEngine
        .decide(
            make_signals(
                average_response_latency_ms=(
                    10_000.0
                ),

                independent_attempt_rate=(
                    75.0
                ),

                independent_success_rate=(
                    75.0
                ),

                average_hint_level=(
                    1.0
                ),
            )
        )
    )


    assert (
        result.response_pace
        == ResponsePace.FAST
    )


    assert (
        "FAST_RESPONSE_WITH_STRONG_PERFORMANCE"
        in result.reason_codes
    )


    assert (
        result.difficulty
        == DifficultyLevel
        .CHALLENGING
    )


def test_latency_requires_minimum_samples():

    result = (
        AdaptiveLearningEngine
        .decide(
            make_signals(
                measured_response_count=2,

                average_response_latency_ms=(
                    8_000.0
                ),
            )
        )
    )


    assert (
        result.response_pace
        == ResponsePace
        .INSUFFICIENT_DATA
    )


    assert (
        "FAST_RESPONSE_WITH_STRONG_PERFORMANCE"
        not in result.reason_codes
    )