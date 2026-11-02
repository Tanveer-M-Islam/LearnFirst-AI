from pydantic import (
    BaseModel,
    Field,
)

from app.schemas.enums import (
    AttemptStatus,
)


class ScienceValidationResult(
    BaseModel
):
    """
    Internal Science understanding
    evaluation.

    missing_ideas is kept internally
    so the tutor can choose an
    appropriate next question without
    directly revealing every missing
    concept to the learner.
    """

    supported: bool

    concept_code: str

    question_id: (
        str | None
    ) = None

    status: AttemptStatus

    coverage_score: float = Field(
        ge=0.0,
        le=100.0,
    )

    matched_ideas: list[str] = Field(
        default_factory=list
    )

    missing_ideas: list[str] = Field(
        default_factory=list
    )

    misconception_code: (
        str | None
    ) = None

    feedback_summary: str


class ScienceValidationView(
    BaseModel
):
    """
    Public learner-facing version.

    The complete missing-idea list
    is intentionally not exposed.
    """

    supported: bool

    concept_code: str

    question_id: (
        str | None
    ) = None

    status: AttemptStatus

    coverage_score: float = Field(
        ge=0.0,
        le=100.0,
    )

    matched_ideas: list[str] = Field(
        default_factory=list
    )

    misconception_code: (
        str | None
    ) = None

    feedback_summary: str


def create_public_science_validation(
    result: ScienceValidationResult,
) -> ScienceValidationView:

    return (
        ScienceValidationView(
            supported=(
                result.supported
            ),

            concept_code=(
                result.concept_code
            ),

            question_id=(
                result.question_id
            ),

            status=(
                result.status
            ),

            coverage_score=(
                result.coverage_score
            ),

            matched_ideas=(
                result.matched_ideas
            ),

            misconception_code=(
                result
                .misconception_code
            ),

            feedback_summary=(
                result
                .feedback_summary
            ),
        )
    )