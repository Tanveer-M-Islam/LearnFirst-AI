from app.math.misconceptions import (
    detect_misconception,
)
from app.math.models import (
    MathProblemType,
    MathValidationResult,
)
from app.math.parser import (
    evaluate_arithmetic,
    evaluate_substitution_problem,
    extract_equation_candidates,
    extract_isolated_x_answer,
    extract_numeric_answer,
    format_math_value,
    solve_linear_equation,
    values_equal,
)
from app.schemas.enums import (
    AttemptStatus,
)


class MathValidator:

    @classmethod
    def validate(
        cls,
        problem: str,
        student_message: str,
    ) -> MathValidationResult:

        if (
            not problem.strip()
        ):

            return (
                cls._unsupported(
                    (
                        "No Math problem is "
                        "stored in the "
                        "learning session."
                    )
                )
            )


        normalized_problem = (
            problem
            .lower()
            .strip()
        )


        # ----------------------------------
        # Check substitution BEFORE normal
        # equation detection.
        #
        # Example:
        # y = 2x + 3 when x = 4
        # ----------------------------------

        if (
            "when x"
            in normalized_problem
        ):

            return (
                cls._validate_substitution(
                    problem=(
                        problem
                    ),

                    student_message=(
                        student_message
                    ),
                )
            )


        if (
            "=" in problem

            and "x"
            in problem.lower()
        ):

            return (
                cls._validate_linear_equation(
                    problem=(
                        problem
                    ),

                    student_message=(
                        student_message
                    ),
                )
            )


        return (
            cls._validate_arithmetic(
                problem=(
                    problem
                ),

                student_message=(
                    student_message
                ),
            )
        )


    # ==================================================
    # Substitution
    # ==================================================

    @classmethod
    def _validate_substitution(
        cls,
        problem: str,
        student_message: str,
    ) -> MathValidationResult:

        try:

            expected = (
                evaluate_substitution_problem(
                    problem
                )
            )


        except Exception:

            return (
                cls._unsupported(
                    (
                        "This substitution "
                        "problem is not "
                        "supported."
                    )
                )
            )


        student_answer = (
            extract_numeric_answer(
                student_message
            )
        )


        if (
            student_answer is None
        ):

            return (
                MathValidationResult(
                    supported=True,

                    problem_type=(
                        MathProblemType
                        .SUBSTITUTION
                    ),

                    status=(
                        AttemptStatus
                        .UNCLEAR
                    ),

                    is_correct=False,

                    normalized_problem=(
                        problem
                    ),

                    expected_answer=(
                        format_math_value(
                            expected
                        )
                    ),

                    feedback_summary=(
                        "A numerical result "
                        "could not be found."
                    ),
                )
            )


        is_correct = (
            values_equal(
                student_answer,
                expected,
            )
        )


        return (
            MathValidationResult(
                supported=True,

                problem_type=(
                    MathProblemType
                    .SUBSTITUTION
                ),

                status=(
                    AttemptStatus.CORRECT

                    if is_correct

                    else (
                        AttemptStatus
                        .INCORRECT
                    )
                ),

                is_correct=(
                    is_correct
                ),

                normalized_problem=(
                    problem
                ),

                student_answer=(
                    format_math_value(
                        student_answer
                    )
                ),

                expected_answer=(
                    format_math_value(
                        expected
                    )
                ),

                feedback_summary=(
                    (
                        "The substituted "
                        "value is correct."
                    )

                    if is_correct

                    else (
                        "The substituted "
                        "value is incorrect."
                    )
                ),
            )
        )


    # ==================================================
    # Linear equations
    # ==================================================

    @classmethod
    def _validate_linear_equation(
        cls,
        problem: str,
        student_message: str,
    ) -> MathValidationResult:

        try:

            expected = (
                solve_linear_equation(
                    problem
                )
            )


        except Exception:

            return (
                cls._unsupported(
                    (
                        "This equation type "
                        "is not supported by "
                        "the current Math "
                        "validator."
                    )
                )
            )


        steps = (
            extract_equation_candidates(
                student_message
            )
        )


        if (
            not steps
        ):

            return (
                MathValidationResult(
                    supported=True,

                    problem_type=(
                        MathProblemType
                        .LINEAR_EQUATION
                    ),

                    status=(
                        AttemptStatus
                        .UNCLEAR
                    ),

                    is_correct=False,

                    normalized_problem=(
                        problem
                    ),

                    expected_answer=(
                        format_math_value(
                            expected
                        )
                    ),

                    feedback_summary=(
                        "A clear equation "
                        "step or x-value "
                        "could not be found."
                    ),
                )
            )


        correct_steps: list[
            str
        ] = []


        first_error_step: (
            str | None
        ) = None


        for step in (
            steps
        ):

            try:

                step_solution = (
                    solve_linear_equation(
                        step
                    )
                )


            except Exception:

                if (
                    first_error_step
                    is None
                ):

                    first_error_step = (
                        step
                    )


                continue


            if (
                values_equal(
                    step_solution,
                    expected,
                )
            ):

                correct_steps.append(
                    step
                )


            elif (
                first_error_step
                is None
            ):

                first_error_step = (
                    step
                )


        final_answer = (
            extract_isolated_x_answer(
                steps[-1]
            )
        )


        if (
            final_answer
            is not None

            and values_equal(
                final_answer,
                expected,
            )
        ):

            return (
                MathValidationResult(
                    supported=True,

                    problem_type=(
                        MathProblemType
                        .LINEAR_EQUATION
                    ),

                    status=(
                        AttemptStatus
                        .CORRECT
                    ),

                    is_correct=True,

                    normalized_problem=(
                        problem
                    ),

                    student_answer=(
                        format_math_value(
                            final_answer
                        )
                    ),

                    expected_answer=(
                        format_math_value(
                            expected
                        )
                    ),

                    correct_steps=(
                        correct_steps
                    ),

                    feedback_summary=(
                        "The learner reached "
                        "the correct value "
                        "of x."
                    ),
                )
            )


        misconception = (
            detect_misconception(
                problem=(
                    problem
                ),

                steps=(
                    steps
                ),
            )
        )


        if (
            correct_steps
        ):

            return (
                MathValidationResult(
                    supported=True,

                    problem_type=(
                        MathProblemType
                        .LINEAR_EQUATION
                    ),

                    status=(
                        AttemptStatus
                        .PARTIALLY_CORRECT
                    ),

                    is_correct=False,

                    normalized_problem=(
                        problem
                    ),

                    student_answer=(
                        (
                            format_math_value(
                                final_answer
                            )
                        )

                        if final_answer
                        is not None

                        else None
                    ),

                    expected_answer=(
                        format_math_value(
                            expected
                        )
                    ),

                    correct_steps=(
                        correct_steps
                    ),

                    first_error_step=(
                        first_error_step
                    ),

                    misconception_code=(
                        misconception
                    ),

                    feedback_summary=(
                        "At least one valid "
                        "algebraic step was "
                        "found, but the final "
                        "answer is not correct."
                    ),
                )
            )


        return (
            MathValidationResult(
                supported=True,

                problem_type=(
                    MathProblemType
                    .LINEAR_EQUATION
                ),

                status=(
                    AttemptStatus
                    .INCORRECT
                ),

                is_correct=False,

                normalized_problem=(
                    problem
                ),

                student_answer=(
                    (
                        format_math_value(
                            final_answer
                        )
                    )

                    if final_answer
                    is not None

                    else None
                ),

                expected_answer=(
                    format_math_value(
                        expected
                    )
                ),

                correct_steps=[],

                first_error_step=(
                    first_error_step
                ),

                misconception_code=(
                    misconception
                ),

                feedback_summary=(
                    "The submitted solution "
                    "is not algebraically "
                    "equivalent to the "
                    "original equation."
                ),
            )
        )


    # ==================================================
    # Arithmetic
    # ==================================================

    @classmethod
    def _validate_arithmetic(
        cls,
        problem: str,
        student_message: str,
    ) -> MathValidationResult:

        try:

            expected = (
                evaluate_arithmetic(
                    problem
                )
            )


        except Exception:

            return (
                cls._unsupported(
                    (
                        "This Math problem "
                        "is not supported by "
                        "the current validator."
                    )
                )
            )


        student_answer = (
            extract_numeric_answer(
                student_message
            )
        )


        if (
            student_answer is None
        ):

            return (
                MathValidationResult(
                    supported=True,

                    problem_type=(
                        MathProblemType
                        .ARITHMETIC
                    ),

                    status=(
                        AttemptStatus
                        .UNCLEAR
                    ),

                    is_correct=False,

                    normalized_problem=(
                        problem
                    ),

                    expected_answer=(
                        format_math_value(
                            expected
                        )
                    ),

                    feedback_summary=(
                        "A numeric answer "
                        "could not be "
                        "identified."
                    ),
                )
            )


        is_correct = (
            values_equal(
                student_answer,
                expected,
            )
        )


        return (
            MathValidationResult(
                supported=True,

                problem_type=(
                    MathProblemType
                    .ARITHMETIC
                ),

                status=(
                    AttemptStatus.CORRECT

                    if is_correct

                    else (
                        AttemptStatus
                        .INCORRECT
                    )
                ),

                is_correct=(
                    is_correct
                ),

                normalized_problem=(
                    problem
                ),

                student_answer=(
                    format_math_value(
                        student_answer
                    )
                ),

                expected_answer=(
                    format_math_value(
                        expected
                    )
                ),

                feedback_summary=(
                    (
                        "The arithmetic "
                        "answer is correct."
                    )

                    if is_correct

                    else (
                        "The arithmetic "
                        "answer is incorrect."
                    )
                ),
            )
        )


    @staticmethod
    def _unsupported(
        message: str,
    ) -> MathValidationResult:

        return (
            MathValidationResult(
                supported=False,

                problem_type=(
                    MathProblemType
                    .UNSUPPORTED
                ),

                status=(
                    AttemptStatus
                    .UNCLEAR
                ),

                is_correct=False,

                feedback_summary=(
                    message
                ),
            )
        )