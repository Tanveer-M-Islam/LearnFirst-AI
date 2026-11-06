from enum import Enum

from pydantic import (
    BaseModel,
    Field,
)

from app.schemas.enums import (
    AttemptStatus,
)


class EnglishEvaluationMode(
    str,
    Enum,
):

    EXACT = "EXACT"

    KEY_IDEAS = "KEY_IDEAS"

    SENTENCE_RULES = "SENTENCE_RULES"


class EnglishValidationResult(
    BaseModel,
):

    supported: bool

    concept_code: str

    question_id: (
        str | None
    ) = None

    evaluation_mode: (
        EnglishEvaluationMode
        | None
    ) = None

    status: AttemptStatus

    score_percent: float = Field(
        ge=0.0,
        le=100.0,
    )

    matched_ideas: list[
        str
    ] = Field(
        default_factory=list
    )

    missing_ideas: list[
        str
    ] = Field(
        default_factory=list
    )

    rule_feedback: list[
        str
    ] = Field(
        default_factory=list
    )

    feedback_summary: str


class EnglishValidationView(
    BaseModel,
):

    supported: bool

    concept_code: str

    question_id: (
        str | None
    ) = None

    evaluation_mode: (
        EnglishEvaluationMode
        | None
    ) = None

    status: AttemptStatus

    score_percent: float = Field(
        ge=0.0,
        le=100.0,
    )

    matched_ideas: list[
        str
    ] = Field(
        default_factory=list
    )

    rule_feedback: list[
        str
    ] = Field(
        default_factory=list
    )

    feedback_summary: str


def create_public_english_validation(
    result: EnglishValidationResult,
) -> EnglishValidationView:

    return EnglishValidationView(
        supported=(
            result.supported
        ),

        concept_code=(
            result.concept_code
        ),

        question_id=(
            result.question_id
        ),

        evaluation_mode=(
            result.evaluation_mode
        ),

        status=(
            result.status
        ),

        score_percent=(
            result.score_percent
        ),

        matched_ideas=(
            result.matched_ideas
        ),

        rule_feedback=(
            result.rule_feedback
        ),

        feedback_summary=(
            result.feedback_summary
        ),
    )