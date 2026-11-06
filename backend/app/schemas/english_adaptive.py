from enum import Enum

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


class EnglishAdaptiveActivity(
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


class EnglishQuestionView(
    BaseModel,
):
    question_id: str

    prompt: str

    difficulty: DifficultyLevel


class EnglishAdaptivePlanResponse(
    BaseModel,
):
    student_id: str

    concept_code: str

    age_group: AgeGroup

    mastery_state: MasteryState

    mastery_explanation: str

    difficulty: DifficultyLevel

    support_level: AdaptiveSupport

    explanation_depth: ExplanationDepth

    next_activity: EnglishAdaptiveActivity

    understanding_score_percent: float

    total_attempts: int

    correct_attempts: int

    partial_attempts: int

    independent_attempts: int

    independent_attempt_rate: float

    independent_success_rate: float

    average_hint_level: float

    direct_answer_requests: int

    measured_response_count: int = 0

    average_response_latency_ms: (
        float | None
    ) = None

    response_pace: ResponsePace = (
        ResponsePace.INSUFFICIENT_DATA
    )

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
        EnglishQuestionView
        | None
    ) = None