from dataclasses import dataclass

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
    difficulty: (
        DifficultyLevel
    ),
    offset: int = 0,
) -> AdaptiveProblem | None:

    concept_bank = (
        PROBLEM_BANK.get(
            concept_code
        )
    )

    if concept_bank is None:

        return None

    problems = (
        concept_bank.get(
            difficulty,
            (),
        )
    )

    if not problems:

        return None

    index = (
        offset
        % len(problems)
    )

    return problems[index]