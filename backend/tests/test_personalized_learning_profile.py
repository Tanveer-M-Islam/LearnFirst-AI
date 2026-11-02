from app.adaptive.engine import (
    AdaptiveLearningEngine,
    AdaptiveSignals,
)
from app.adaptive.profile import (
    LearningProfileAnalyzer,
)
from app.schemas.adaptive import (
    ResponsePace,
    ResponsePaceSource,
)
from app.schemas.enums import (
    AgeGroup,
    DifficultyLevel,
    MasteryState,
)


def test_profile_requires_enough_history():

    profile = (
        LearningProfileAnalyzer
        .analyze(
            [
                24000,
                25000,
                23000,
            ]
        )
    )


    assert (
        profile.baseline_ready
        is False
    )


    assert (
        profile.personalized_response_pace
        == ResponsePace
        .INSUFFICIENT_DATA
    )


def test_personal_profile_detects_faster_recent_pace():

    profile = (
        LearningProfileAnalyzer
        .analyze(
            [
                30000,
                32000,
                29000,
                31000,
                30000,

                18000,
                19000,
                17000,
            ]
        )
    )


    assert (
        profile.baseline_ready
        is True
    )


    assert (
        profile.personalized_response_pace
        == ResponsePace.FAST
    )


    assert (
        profile.latency_change_percent
        is not None
    )


    assert (
        profile.latency_change_percent
        < 0
    )


def test_personal_profile_detects_slower_recent_pace():

    profile = (
        LearningProfileAnalyzer
        .analyze(
            [
                20000,
                21000,
                19000,
                20500,
                20000,

                30000,
                31000,
                32000,
            ]
        )
    )


    assert (
        profile.baseline_ready
        is True
    )


    assert (
        profile.personalized_response_pace
        == ResponsePace.SLOW
    )


def test_personal_profile_detects_typical_recent_pace():

    profile = (
        LearningProfileAnalyzer
        .analyze(
            [
                24000,
                25000,
                23000,
                24500,
                24000,

                25000,
                26000,
                24000,
            ]
        )
    )


    assert (
        profile.baseline_ready
        is True
    )


    assert (
        profile.personalized_response_pace
        == ResponsePace.TYPICAL
    )


def test_engine_prefers_personal_baseline():

    signals = AdaptiveSignals(
        age_group=(
            AgeGroup.DEVELOPING
        ),

        mastery_state=(
            MasteryState
            .DEVELOPING
        ),

        recommended_difficulty=(
            DifficultyLevel.MODERATE
        ),

        diagnostic_score=60.0,

        mastery_score=None,

        total_attempts=4,

        independent_attempts=3,

        independent_attempt_rate=75.0,

        independent_success_rate=75.0,

        average_hint_level=1.0,

        direct_answer_requests=0,

        retry_success_count=1,

        measured_response_count=8,

        # Age-group logic would consider
        # this roughly typical.
        average_response_latency_ms=(
            24000.0
        ),

        baseline_ready=True,

        # But the learner is currently
        # fast relative to their own
        # historical baseline.
        personalized_response_pace=(
            ResponsePace.FAST
        ),
    )


    result = (
        AdaptiveLearningEngine
        .decide(
            signals
        )
    )


    assert (
        result.response_pace
        == ResponsePace.FAST
    )


    assert (
        result.response_pace_source
        == (
            ResponsePaceSource
            .PERSONAL_BASELINE
        )
    )


    assert (
        "PERSONAL_BASELINE_USED"
        in result.reason_codes
    )


def test_engine_falls_back_before_baseline_ready():

    signals = AdaptiveSignals(
        age_group=(
            AgeGroup.DEVELOPING
        ),

        mastery_state=(
            MasteryState.LEARNING
        ),

        recommended_difficulty=(
            DifficultyLevel.MODERATE
        ),

        diagnostic_score=60.0,

        mastery_score=None,

        total_attempts=4,

        independent_attempts=3,

        independent_attempt_rate=75.0,

        independent_success_rate=70.0,

        average_hint_level=1.0,

        direct_answer_requests=0,

        retry_success_count=1,

        measured_response_count=3,

        average_response_latency_ms=(
            24000.0
        ),

        baseline_ready=False,

        personalized_response_pace=(
            ResponsePace
            .INSUFFICIENT_DATA
        ),
    )


    result = (
        AdaptiveLearningEngine
        .decide(
            signals
        )
    )


    assert (
        result.response_pace
        == ResponsePace.TYPICAL
    )


    assert (
        result.response_pace_source
        == (
            ResponsePaceSource
            .AGE_GROUP_FALLBACK
        )
    )