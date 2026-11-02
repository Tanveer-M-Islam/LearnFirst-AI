from enum import (
    Enum,
)

from pydantic import (
    BaseModel,
    Field,
)

from app.schemas.adaptive import (
    AdaptiveSupport,
    ExplanationDepth,
    ResponsePace,
    ResponsePaceSource,
)
from app.schemas.enums import (
    AgeGroup,
    DifficultyLevel,
    MasteryState,
)


class ScienceAdaptiveActivity(
    str,
    Enum,
):

    START_LEARNING = (
        "START_LEARNING"
    )

    GUIDED_QUESTION = (
        "GUIDED_QUESTION"
    )

    INDEPENDENT_QUESTION = (
        "INDEPENDENT_QUESTION"
    )

    REVIEW_CONCEPT = (
        "REVIEW_CONCEPT"
    )

    CHALLENGE_QUESTION = (
        "CHALLENGE_QUESTION"
    )


class ScienceQuestionView(
    BaseModel
):

    question_id: str

    prompt: str

    difficulty: (
        DifficultyLevel
    )


class ScienceAdaptivePlanResponse(
    BaseModel
):

    student_id: str

    concept_code: str

    age_group: AgeGroup

    mastery_state: (
        MasteryState
    )


    # ==================================
    # Clear mastery explanation
    # ==================================

    mastery_explanation: str


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
        ScienceAdaptiveActivity
    )


    # ==================================
    # Understanding evidence
    # ==================================

    understanding_score_percent: float

    total_attempts: int

    correct_attempts: int

    partial_attempts: int

    independent_attempts: int

    misconception_count: int

    independent_attempt_rate: float

    independent_success_rate: float

    average_hint_level: float

    direct_answer_requests: int


    # ==================================
    # Latency
    # ==================================

    measured_response_count: int = 0

    average_response_latency_ms: (
        float | None
    ) = None

    response_pace: ResponsePace = (
        ResponsePace
        .INSUFFICIENT_DATA
    )


    # ==================================
    # Personal baseline
    # ==================================

    baseline_ready: bool = False

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


    reason_codes: list[str] = Field(
        default_factory=list
    )

    summary: str

    next_question: (
        ScienceQuestionView
        | None
    ) = None