import sympy as sp

from app.math.parser import (
    X,
    extract_isolated_x_answer,
    parse_equation,
    solve_linear_equation,
    values_equal,
)


MATH_DIVIDE_COEFFICIENT = (
    "MATH_DIVIDE_COEFFICIENT"
)

MATH_INVERSE_OPERATION = (
    "MATH_INVERSE_OPERATION"
)

MATH_ALGEBRA_PROCESS_ERROR = (
    "MATH_ALGEBRA_PROCESS_ERROR"
)


def detect_misconception(
    problem: str,
    steps: list[str],
) -> str | None:
    """
    Detect selected algebra misconceptions.

    This is intentionally conservative.

    If we cannot confidently identify a known
    misconception, we return a generic process
    error instead of pretending certainty.
    """

    if not steps:
        return None

    final_answer = (
        extract_isolated_x_answer(
            steps[-1]
        )
    )

    if final_answer is None:
        return None

    divide_error = (
        _detect_divide_coefficient(
            steps=steps,
            final_answer=final_answer,
        )
    )

    if divide_error:
        return divide_error

    inverse_error = (
        _detect_inverse_operation(
            problem=problem,
            final_answer=final_answer,
        )
    )

    if inverse_error:
        return inverse_error

    return MATH_ALGEBRA_PROCESS_ERROR


def _detect_divide_coefficient(
    steps: list[str],
    final_answer,
) -> str | None:
    """
    Detect:

        3x = 12
        x = 12

    The learner copied 12 instead of dividing
    both sides by 3.
    """

    if len(steps) < 2:
        return None

    previous_step = steps[-2]

    try:

        equation = parse_equation(
            previous_step
        )

    except ValueError:
        return None

    left = sp.expand(
        equation.lhs
    )

    right = sp.expand(
        equation.rhs
    )

    # ----------------------------------
    # Example:
    # 3x = 12
    # ----------------------------------

    if (
        left.has(X)
        and not right.has(X)
    ):

        coefficient = left.coeff(X)

        remainder = sp.simplify(
            left - coefficient * X
        )

        if (
            remainder == 0
            and coefficient not in {
                0,
                1,
                -1,
            }
            and values_equal(
                final_answer,
                right,
            )
        ):
            return (
                MATH_DIVIDE_COEFFICIENT
            )

    # ----------------------------------
    # Reverse:
    # 12 = 3x
    # ----------------------------------

    if (
        right.has(X)
        and not left.has(X)
    ):

        coefficient = right.coeff(X)

        remainder = sp.simplify(
            right - coefficient * X
        )

        if (
            remainder == 0
            and coefficient not in {
                0,
                1,
                -1,
            }
            and values_equal(
                final_answer,
                left,
            )
        ):
            return (
                MATH_DIVIDE_COEFFICIENT
            )

    return None


def _detect_inverse_operation(
    problem: str,
    final_answer,
) -> str | None:
    """
    Detect a simple inverse-operation error.

    Example:

        x + 5 = 12

    learner incorrectly thinks:

        x = 17

    instead of undoing +5 using subtraction.
    """

    try:

        equation = parse_equation(
            problem
        )

        correct_answer = (
            solve_linear_equation(
                problem
            )
        )

    except ValueError:
        return None

    left = sp.expand(
        equation.lhs
    )

    right = sp.expand(
        equation.rhs
    )

    if (
        left.has(X)
        and not right.has(X)
    ):

        coefficient = left.coeff(X)

        constant = sp.simplify(
            left.subs(
                X,
                0,
            )
        )

        if (
            coefficient == 1
            and constant != 0
        ):

            incorrect_inverse = (
                right + constant
            )

            if (
                values_equal(
                    final_answer,
                    incorrect_inverse,
                )
                and not values_equal(
                    final_answer,
                    correct_answer,
                )
            ):
                return (
                    MATH_INVERSE_OPERATION
                )

    return None