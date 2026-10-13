from enum import Enum

from pydantic import BaseModel, Field

from app.schemas.enums import AttemptStatus


class MathProblemType(str, Enum):
    LINEAR_EQUATION = "LINEAR_EQUATION"
    ARITHMETIC = "ARITHMETIC"
    UNSUPPORTED = "UNSUPPORTED"


class MathValidationResult(BaseModel):
    """
    Internal Math validation result.

    expected_answer may exist here because this
    object is used internally by the backend.

    It must NOT automatically be exposed to
    the learner.
    """

    supported: bool

    problem_type: MathProblemType

    status: AttemptStatus

    is_correct: bool

    normalized_problem: str | None = None

    student_answer: str | None = None

    expected_answer: str | None = None

    correct_steps: list[str] = Field(
        default_factory=list
    )

    first_error_step: str | None = None

    misconception_code: str | None = None

    feedback_summary: str


class MathValidationView(BaseModel):
    """
    Public learner-facing version.

    The expected answer is intentionally excluded.
    """

    supported: bool

    problem_type: MathProblemType

    status: AttemptStatus

    is_correct: bool

    student_answer: str | None = None

    correct_steps: list[str] = Field(
        default_factory=list
    )

    first_error_step: str | None = None

    misconception_code: str | None = None

    feedback_summary: str


def create_public_validation(
    result: MathValidationResult,
) -> MathValidationView:

    return MathValidationView(
        supported=result.supported,
        problem_type=result.problem_type,
        status=result.status,
        is_correct=result.is_correct,
        student_answer=result.student_answer,
        correct_steps=result.correct_steps,
        first_error_step=result.first_error_step,
        misconception_code=(
            result.misconception_code
        ),
        feedback_summary=(
            result.feedback_summary
        ),
    )