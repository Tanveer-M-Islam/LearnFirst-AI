from enum import Enum

from pydantic import (
    BaseModel,
    Field,
)

from app.schemas.enums import (
    AgeGroup,
    DifficultyLevel,
    MasteryState,
)


class AdaptiveActivity(
    str,
    Enum,
):
    TAKE_DIAGNOSTIC = (
        "TAKE_DIAGNOSTIC"
    )

    GUIDED_PRACTICE = (
        "GUIDED_PRACTICE"
    )

    INDEPENDENT_PRACTICE = (
        "INDEPENDENT_PRACTICE"
    )

    REVIEW_FOUNDATION = (
        "REVIEW_FOUNDATION"
    )

    TAKE_MASTERY_CHECK = (
        "TAKE_MASTERY_CHECK"
    )

    CHALLENGE_PRACTICE = (
        "CHALLENGE_PRACTICE"
    )


class AdaptiveSupport(
    str,
    Enum,
):
    GENTLE = "GENTLE"

    GUIDED = "GUIDED"

    STRONG = "STRONG"


class ExplanationDepth(
    str,
    Enum,
):
    SIMPLE = "SIMPLE"

    BALANCED = "BALANCED"

    DEEP = "DEEP"


class ResponsePace(
    str,
    Enum,
):
    INSUFFICIENT_DATA = (
        "INSUFFICIENT_DATA"
    )

    FAST = "FAST"

    TYPICAL = "TYPICAL"

    SLOW = "SLOW"


class ResponsePaceSource(
    str,
    Enum,
):
    PERSONAL_BASELINE = (
        "PERSONAL_BASELINE"
    )

    AGE_GROUP_FALLBACK = (
        "AGE_GROUP_FALLBACK"
    )

    INSUFFICIENT_DATA = (
        "INSUFFICIENT_DATA"
    )


class AdaptiveProblemView(
    BaseModel
):
    problem_id: str

    prompt: str

    difficulty: (
        DifficultyLevel
    )


class AdaptivePlanResponse(
    BaseModel
):
    student_id: str

    concept_code: str

    age_group: AgeGroup

    mastery_state: (
        MasteryState
    )

    difficulty: (
        DifficultyLevel
    )

    support_level: (
        AdaptiveSupport
    )

    explanation_depth: (
        ExplanationDepth
    )

    next_activity: (
        AdaptiveActivity
    )

    latest_score_percent: (
        float | None
    ) = None

    independent_attempt_rate: float

    independent_success_rate: float

    average_hint_level: float

    direct_answer_requests: int

    retry_success_count: int


    # ----------------------------------
    # Phase 13 telemetry
    # ----------------------------------

    measured_response_count: int = 0

    average_response_latency_ms: (
        float | None
    ) = None

    response_pace: ResponsePace = (
        ResponsePace
        .INSUFFICIENT_DATA
    )


    # ----------------------------------
    # Phase 14 personal baseline
    # ----------------------------------

    baseline_ready: bool = False

    baseline_sample_count: int = 0

    recent_sample_count: int = 0

    baseline_response_latency_ms: (
        float | None
    ) = None

    recent_response_latency_ms: (
        float | None
    ) = None

    latency_change_percent: (
        float | None
    ) = None

    response_pace_source: (
        ResponsePaceSource
    ) = (
        ResponsePaceSource
        .INSUFFICIENT_DATA
    )


    reason_codes: list[str] = (
        Field(
            default_factory=list
        )
    )

    summary: str

    next_problem: (
        AdaptiveProblemView
        | None
    ) = None