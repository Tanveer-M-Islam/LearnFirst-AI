from dataclasses import dataclass

from app.schemas.enums import (
    DifficultyLevel,
)


@dataclass(frozen=True)
class AdaptiveProblem:
    problem_id: str

    prompt: str

    difficulty: DifficultyLevel


def _problems(
    prefix: str,
    difficulty: DifficultyLevel,
    prompts: tuple[str, ...],
) -> tuple[AdaptiveProblem, ...]:

    return tuple(
        AdaptiveProblem(
            problem_id=(
                f"{prefix}-"
                f"{difficulty.value[0]}-"
                f"{index:02d}"
            ),

            prompt=prompt,

            difficulty=difficulty,
        )

        for index, prompt
        in enumerate(
            prompts,
            start=1,
        )
    )


def _bank(
    prefix: str,
    easy: tuple[str, ...],
    moderate: tuple[str, ...],
    challenging: tuple[str, ...],
) -> dict[
    DifficultyLevel,
    tuple[AdaptiveProblem, ...],
]:

    return {
        DifficultyLevel.EASY:
            _problems(
                prefix=prefix,
                difficulty=(
                    DifficultyLevel.EASY
                ),
                prompts=easy,
            ),

        DifficultyLevel.MODERATE:
            _problems(
                prefix=prefix,
                difficulty=(
                    DifficultyLevel.MODERATE
                ),
                prompts=moderate,
            ),

        DifficultyLevel.CHALLENGING:
            _problems(
                prefix=prefix,
                difficulty=(
                    DifficultyLevel.CHALLENGING
                ),
                prompts=challenging,
            ),
    }


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

    # ==================================================
    # AGE 7
    # Basic Arithmetic
    # ==================================================

    "MATH_ARITH_BASIC_01":
        _bank(
            "BASIC",

            (
                "7 + 5",
                "14 - 6",
                "9 + 8",
            ),

            (
                "27 + 16",
                "42 - 19",
                "35 + 28",
            ),

            (
                "64 - 27 + 15",
                "38 + 26 - 19",
                "75 - 38 + 12",
            ),
        ),


    # ==================================================
    # AGE 8
    # Multiplication and Division
    # ==================================================

    "MATH_ARITH_MULTDIV_01":
        _bank(
            "MULTDIV",

            (
                "4 * 6",
                "24 / 6",
                "7 * 5",
            ),

            (
                "8 * 7",
                "54 / 6",
                "9 * 6",
            ),

            (
                "12 * 8",
                "96 / 12",
                "14 * 6",
            ),
        ),


    # ==================================================
    # AGE 9
    # Fractions
    # ==================================================

    "MATH_ARITH_FRAC_01":
        _bank(
            "FRAC",

            (
                "1/2 + 1/4",
                "3/5 + 1/5",
                "3/4 - 1/2",
            ),

            (
                "2/3 + 1/6",
                "3/5 * 10",
                "(3/4) / (1/2)",
            ),

            (
                "5/6 - 1/4",
                "2/3 * 9/4",
                "(1/2 + 1/3) * 6",
            ),
        ),


    # ==================================================
    # AGE 10
    # Integers
    # ==================================================

    "MATH_ARITH_INT_01":
        _bank(
            "INT",

            (
                "-5 + 12",
                "9 - 14",
                "-4 + 7",
            ),

            (
                "-8 + 15 - 4",
                "6 - (-3)",
                "-4 * 5 + 27",
            ),

            (
                "(-6 + 14) * 3",
                "-5 * (-4) - 7",
                "18 / (-3) + 11",
            ),
        ),


    # ==================================================
    # AGE 11
    # Order of Operations
    # ==================================================

    "MATH_ARITH_ORDER_01":
        _bank(
            "ORDER",

            (
                "3 + 4 * 2",
                "(8 + 4) / 3",
                "18 - 2 * 5",
            ),

            (
                "6 + 3 * (8 - 5)",
                "24 / (2 * 3) + 7",
                "5 * (4 + 2) - 9",
            ),

            (
                "3 + 2 * (5 + 7) - 4",
                "(18 - 6) / 3 + 5 * 2",
                "2 * (3 + 4 * 2) - 5",
            ),
        ),


    # ==================================================
    # AGE 12
    # Pre-Algebra
    # ==================================================

    "MATH_PREALG_EXPR_01":
        _bank(
            "PREALG",

            (
                "x + 4 when x = 3",
                "2x when x = 5",
                "x - 6 when x = 10",
            ),

            (
                "3x + 2 when x = 4",
                "5x - 7 when x = 3",
                "2x + 8 when x = -2",
            ),

            (
                "4(x + 2) when x = 3",
                "3x - 2(x - 1) when x = 5",
                "2(x + 3) - x when x = -4",
            ),
        ),


    # ==================================================
    # AGE 13
    # Linear Equations
    # ==================================================

    "MATH_ALG_LINEAR_01":
        _bank(
            "ALG",

            (
                "x + 5 = 9",
                "3x = 15",
                "x - 7 = 4",
            ),

            (
                "2x + 5 = 17",
                "4x - 3 = 21",
                "5x + 7 = 32",
            ),

            (
                "3(x + 2) = 24",
                "2(x + 4) = 20",
                "5(x - 2) = 25",
            ),
        ),


    # ==================================================
    # AGE 14
    # Linear Graphs
    # ==================================================

    "MATH_GRAPH_LINEAR_01":
        _bank(
            "GRAPH",

            (
                "y = x + 2 when x = 3",
                "y = 2x when x = 4",
                "y = x - 1 when x = 5",
            ),

            (
                "y = 2x + 3 when x = 4",
                "y = 3x - 2 when x = 5",
                "y = -x + 6 when x = 2",
            ),

            (
                "y = -3x + 5 when x = -2",
                "y = 4x - 7 when x = -3",
                "y = 5 - 2x when x = 6",
            ),
        ),
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
        concept_bank is None
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


    return problems[
        index
    ]