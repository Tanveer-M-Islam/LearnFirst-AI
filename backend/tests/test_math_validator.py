from app.math.validator import (
    MathValidator,
)
from app.schemas.enums import (
    AttemptStatus,
)


def test_correct_linear_equation():

    result = (
        MathValidator.validate(
            problem="3x + 5 = 20",
            student_message=(
                "I think x = 5."
            ),
        )
    )

    assert result.supported is True

    assert (
        result.status
        == AttemptStatus.CORRECT
    )

    assert result.is_correct is True

    assert (
        result.student_answer
        == "5"
    )


def test_wrong_linear_answer():

    result = (
        MathValidator.validate(
            problem="3x + 5 = 20",
            student_message=(
                "I think x = 6."
            ),
        )
    )

    assert result.supported is True

    assert (
        result.status
        == AttemptStatus.INCORRECT
    )

    assert (
        result.is_correct
        is False
    )


def test_partial_solution_detected():

    result = (
        MathValidator.validate(
            problem="3x + 6 = 18",
            student_message=(
                "3x = 12; x = 12"
            ),
        )
    )

    assert (
        result.status
        == AttemptStatus
        .PARTIALLY_CORRECT
    )

    assert (
        "3x = 12"
        in result.correct_steps
    )

    assert (
        result.first_error_step
        == "x = 12"
    )

    assert (
        result.misconception_code
        == "MATH_DIVIDE_COEFFICIENT"
    )


def test_correct_arithmetic():

    result = (
        MathValidator.validate(
            problem="12 + 7",
            student_message=(
                "My answer is 19."
            ),
        )
    )

    assert (
        result.status
        == AttemptStatus.CORRECT
    )

    assert result.is_correct is True


def test_wrong_arithmetic():

    result = (
        MathValidator.validate(
            problem="12 + 7",
            student_message=(
                "My answer is 20."
            ),
        )
    )

    assert (
        result.status
        == AttemptStatus.INCORRECT
    )

    assert (
        result.is_correct
        is False
    )


def test_unclear_math_attempt():

    result = (
        MathValidator.validate(
            problem="3x + 5 = 20",
            student_message=(
                "I tried but I am not sure."
            ),
        )
    )

    assert (
        result.status
        == AttemptStatus.UNCLEAR
    )


def test_inverse_operation_error():

    result = (
        MathValidator.validate(
            problem="x + 5 = 12",
            student_message=(
                "x = 17"
            ),
        )
    )

    assert (
        result.status
        == AttemptStatus.INCORRECT
    )

    assert (
        result.misconception_code
        == "MATH_INVERSE_OPERATION"
    )