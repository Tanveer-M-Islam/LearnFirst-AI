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