from dataclasses import (
    dataclass,
)

from app.schemas.enums import (
    DifficultyLevel,
)


@dataclass(
    frozen=True
)
class AdaptiveProblem:

    problem_id: str

    prompt: str

    difficulty: (
        DifficultyLevel
    )


PROBLEM_BANK: dict[
    str,
    dict[
        DifficultyLevel,
        tuple[
            AdaptiveProblem,
            ...,
        ],
    ],
] = {


    # ======================================================
    # BASIC ARITHMETIC
    # ======================================================

    "MATH_ARITH_BASIC_01": {

        DifficultyLevel.EASY: (

            AdaptiveProblem(
                problem_id=(
                    "BASIC-A-E-01"
                ),

                prompt=(
                    "14 + 8"
                ),

                difficulty=(
                    DifficultyLevel.EASY
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "BASIC-A-E-02"
                ),

                prompt=(
                    "30 - 12"
                ),

                difficulty=(
                    DifficultyLevel.EASY
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "BASIC-A-E-03"
                ),

                prompt=(
                    "6 * 4"
                ),

                difficulty=(
                    DifficultyLevel.EASY
                ),
            ),
        ),


        DifficultyLevel.MODERATE: (

            AdaptiveProblem(
                problem_id=(
                    "BASIC-A-M-01"
                ),

                prompt=(
                    "48 / 6 + 7"
                ),

                difficulty=(
                    DifficultyLevel
                    .MODERATE
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "BASIC-A-M-02"
                ),

                prompt=(
                    "25 + 18 - 9"
                ),

                difficulty=(
                    DifficultyLevel
                    .MODERATE
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "BASIC-A-M-03"
                ),

                prompt=(
                    "7 * 5 - 12"
                ),

                difficulty=(
                    DifficultyLevel
                    .MODERATE
                ),
            ),
        ),


        DifficultyLevel.CHALLENGING: (

            AdaptiveProblem(
                problem_id=(
                    "BASIC-A-C-01"
                ),

                prompt=(
                    "(18 + 6) * 2 - 15"
                ),

                difficulty=(
                    DifficultyLevel
                    .CHALLENGING
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "BASIC-A-C-02"
                ),

                prompt=(
                    "72 / 8 + 6 * 5"
                ),

                difficulty=(
                    DifficultyLevel
                    .CHALLENGING
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "BASIC-A-C-03"
                ),

                prompt=(
                    "4 * (9 - 3) + 18 / 3"
                ),

                difficulty=(
                    DifficultyLevel
                    .CHALLENGING
                ),
            ),
        ),
    },


    # ======================================================
    # INTEGERS
    # ======================================================

    "MATH_ARITH_INT_01": {

        DifficultyLevel.EASY: (

            AdaptiveProblem(
                problem_id=(
                    "INT-A-E-01"
                ),

                prompt=(
                    "-5 + 12"
                ),

                difficulty=(
                    DifficultyLevel.EASY
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "INT-A-E-02"
                ),

                prompt=(
                    "9 - 14"
                ),

                difficulty=(
                    DifficultyLevel.EASY
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "INT-A-E-03"
                ),

                prompt=(
                    "-4 + 7"
                ),

                difficulty=(
                    DifficultyLevel.EASY
                ),
            ),
        ),


        DifficultyLevel.MODERATE: (

            AdaptiveProblem(
                problem_id=(
                    "INT-A-M-01"
                ),

                prompt=(
                    "-8 + 15 - 4"
                ),

                difficulty=(
                    DifficultyLevel
                    .MODERATE
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "INT-A-M-02"
                ),

                prompt=(
                    "6 - (-3)"
                ),

                difficulty=(
                    DifficultyLevel
                    .MODERATE
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "INT-A-M-03"
                ),

                prompt=(
                    "-4 * 5 + 27"
                ),

                difficulty=(
                    DifficultyLevel
                    .MODERATE
                ),
            ),
        ),


        DifficultyLevel.CHALLENGING: (

            AdaptiveProblem(
                problem_id=(
                    "INT-A-C-01"
                ),

                prompt=(
                    "(-6 + 14) * 3"
                ),

                difficulty=(
                    DifficultyLevel
                    .CHALLENGING
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "INT-A-C-02"
                ),

                prompt=(
                    "-5 * (-4) - 7"
                ),

                difficulty=(
                    DifficultyLevel
                    .CHALLENGING
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "INT-A-C-03"
                ),

                prompt=(
                    "18 / (-3) + 11"
                ),

                difficulty=(
                    DifficultyLevel
                    .CHALLENGING
                ),
            ),
        ),
    },


    # ======================================================
    # FRACTIONS
    # ======================================================

    "MATH_ARITH_FRAC_01": {

        DifficultyLevel.EASY: (

            AdaptiveProblem(
                problem_id=(
                    "FRAC-A-E-01"
                ),

                prompt=(
                    "1/2 + 1/4"
                ),

                difficulty=(
                    DifficultyLevel.EASY
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "FRAC-A-E-02"
                ),

                prompt=(
                    "3/5 + 1/5"
                ),

                difficulty=(
                    DifficultyLevel.EASY
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "FRAC-A-E-03"
                ),

                prompt=(
                    "3/4 - 1/2"
                ),

                difficulty=(
                    DifficultyLevel.EASY
                ),
            ),
        ),


        DifficultyLevel.MODERATE: (

            AdaptiveProblem(
                problem_id=(
                    "FRAC-A-M-01"
                ),

                prompt=(
                    "2/3 + 1/6"
                ),

                difficulty=(
                    DifficultyLevel
                    .MODERATE
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "FRAC-A-M-02"
                ),

                prompt=(
                    "3/5 * 10"
                ),

                difficulty=(
                    DifficultyLevel
                    .MODERATE
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "FRAC-A-M-03"
                ),

                prompt=(
                    "(3/4) / (1/2)"
                ),

                difficulty=(
                    DifficultyLevel
                    .MODERATE
                ),
            ),
        ),


        DifficultyLevel.CHALLENGING: (

            AdaptiveProblem(
                problem_id=(
                    "FRAC-A-C-01"
                ),

                prompt=(
                    "5/6 - 1/4"
                ),

                difficulty=(
                    DifficultyLevel
                    .CHALLENGING
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "FRAC-A-C-02"
                ),

                prompt=(
                    "2/3 * 9/4"
                ),

                difficulty=(
                    DifficultyLevel
                    .CHALLENGING
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "FRAC-A-C-03"
                ),

                prompt=(
                    "(1/2 + 1/3) * 6"
                ),

                difficulty=(
                    DifficultyLevel
                    .CHALLENGING
                ),
            ),
        ),
    },


    # ======================================================
    # ORDER OF OPERATIONS
    # ======================================================

    "MATH_ARITH_ORDER_01": {

        DifficultyLevel.EASY: (

            AdaptiveProblem(
                problem_id=(
                    "ORDER-A-E-01"
                ),

                prompt=(
                    "3 + 4 * 2"
                ),

                difficulty=(
                    DifficultyLevel.EASY
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "ORDER-A-E-02"
                ),

                prompt=(
                    "(8 + 4) / 3"
                ),

                difficulty=(
                    DifficultyLevel.EASY
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "ORDER-A-E-03"
                ),

                prompt=(
                    "18 - 2 * 5"
                ),

                difficulty=(
                    DifficultyLevel.EASY
                ),
            ),
        ),


        DifficultyLevel.MODERATE: (

            AdaptiveProblem(
                problem_id=(
                    "ORDER-A-M-01"
                ),

                prompt=(
                    "6 + 3 * (8 - 5)"
                ),

                difficulty=(
                    DifficultyLevel
                    .MODERATE
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "ORDER-A-M-02"
                ),

                prompt=(
                    "24 / (2 * 3) + 7"
                ),

                difficulty=(
                    DifficultyLevel
                    .MODERATE
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "ORDER-A-M-03"
                ),

                prompt=(
                    "5 * (4 + 2) - 9"
                ),

                difficulty=(
                    DifficultyLevel
                    .MODERATE
                ),
            ),
        ),


        DifficultyLevel.CHALLENGING: (

            AdaptiveProblem(
                problem_id=(
                    "ORDER-A-C-01"
                ),

                prompt=(
                    "3 + 2 * (5 + 7) - 4"
                ),

                difficulty=(
                    DifficultyLevel
                    .CHALLENGING
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "ORDER-A-C-02"
                ),

                prompt=(
                    "(18 - 6) / 3 + 5 * 2"
                ),

                difficulty=(
                    DifficultyLevel
                    .CHALLENGING
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "ORDER-A-C-03"
                ),

                prompt=(
                    "2 * (3 + 4 * 2) - 5"
                ),

                difficulty=(
                    DifficultyLevel
                    .CHALLENGING
                ),
            ),
        ),
    },


    # ======================================================
    # LINEAR EQUATIONS
    # ======================================================

    "MATH_ALG_LINEAR_01": {

        DifficultyLevel.EASY: (

            AdaptiveProblem(
                problem_id=(
                    "ALG-A-E-01"
                ),

                prompt=(
                    "x + 5 = 9"
                ),

                difficulty=(
                    DifficultyLevel.EASY
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "ALG-A-E-02"
                ),

                prompt=(
                    "3x = 15"
                ),

                difficulty=(
                    DifficultyLevel.EASY
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "ALG-A-E-03"
                ),

                prompt=(
                    "x - 7 = 4"
                ),

                difficulty=(
                    DifficultyLevel.EASY
                ),
            ),
        ),


        DifficultyLevel.MODERATE: (

            AdaptiveProblem(
                problem_id=(
                    "ALG-A-M-01"
                ),

                prompt=(
                    "2x + 5 = 17"
                ),

                difficulty=(
                    DifficultyLevel
                    .MODERATE
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "ALG-A-M-02"
                ),

                prompt=(
                    "4x - 3 = 21"
                ),

                difficulty=(
                    DifficultyLevel
                    .MODERATE
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "ALG-A-M-03"
                ),

                prompt=(
                    "5x + 7 = 32"
                ),

                difficulty=(
                    DifficultyLevel
                    .MODERATE
                ),
            ),
        ),


        DifficultyLevel.CHALLENGING: (

            AdaptiveProblem(
                problem_id=(
                    "ALG-A-C-01"
                ),

                prompt=(
                    "3(x + 2) = 24"
                ),

                difficulty=(
                    DifficultyLevel
                    .CHALLENGING
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "ALG-A-C-02"
                ),

                prompt=(
                    "2(x + 4) = 20"
                ),

                difficulty=(
                    DifficultyLevel
                    .CHALLENGING
                ),
            ),

            AdaptiveProblem(
                problem_id=(
                    "ALG-A-C-03"
                ),

                prompt=(
                    "5(x - 2) = 25"
                ),

                difficulty=(
                    DifficultyLevel
                    .CHALLENGING
                ),
            ),
        ),
    },
}


def get_adaptive_problem(
    concept_code: str,
    difficulty: DifficultyLevel,
    offset: int = 0,
) -> AdaptiveProblem | None:

    concept_bank = (
        PROBLEM_BANK.get(
            concept_code
        )
    )


    if (
        concept_bank
        is None
    ):

        return None


    problems = (
        concept_bank.get(
            difficulty,
            (),
        )
    )


    if (
        not problems
    ):

        return None


    index = (
        offset
        % len(
            problems
        )
    )


    return (
        problems[
            index
        ]
    )