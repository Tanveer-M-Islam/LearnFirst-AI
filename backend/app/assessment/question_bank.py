from dataclasses import dataclass

from app.schemas.enums import (
    AssessmentType,
    DifficultyLevel,
)


@dataclass(frozen=True)
class AssessmentQuestion:
    question_id: str

    prompt: str

    difficulty: DifficultyLevel

    bloom_level: str


E = DifficultyLevel.EASY

M = DifficultyLevel.MODERATE

C = DifficultyLevel.CHALLENGING


def _questions(
    prefix: str,
    items: tuple[
        tuple[
            str,
            DifficultyLevel,
        ],
        ...,
    ],
) -> tuple[
    AssessmentQuestion,
    ...,
]:

    return tuple(
        AssessmentQuestion(
            question_id=(
                f"{prefix}-"
                f"{index:02d}"
            ),

            prompt=prompt,

            difficulty=difficulty,

            bloom_level="APPLY",
        )

        for index, (
            prompt,
            difficulty,
        )
        in enumerate(
            items,
            start=1,
        )
    )


QUESTION_BANK: dict[
    tuple[
        str,
        AssessmentType,
    ],
    tuple[
        AssessmentQuestion,
        ...,
    ],
] = {

    # ==================================================
    # AGE 7 — BASIC ARITHMETIC
    # ==================================================

    (
        "MATH_ARITH_BASIC_01",
        AssessmentType.DIAGNOSTIC,
    ):
        _questions(
            "BASIC-D",

            (
                ("8 + 7", E),
                ("15 - 6", E),
                ("23 + 14", M),
                ("41 - 17", M),
                ("36 + 19 - 12", C),
            ),
        ),


    (
        "MATH_ARITH_BASIC_01",
        AssessmentType.MASTERY,
    ):
        _questions(
            "BASIC-M",

            (
                ("9 + 6", E),
                ("18 - 9", E),
                ("28 + 17", M),
                ("53 - 26", M),
                ("47 - 18 + 21", C),
            ),
        ),


    # ==================================================
    # AGE 8 — MULTIPLICATION / DIVISION
    # ==================================================

    (
        "MATH_ARITH_MULTDIV_01",
        AssessmentType.DIAGNOSTIC,
    ):
        _questions(
            "MULTDIV-D",

            (
                ("4 * 5", E),
                ("18 / 3", E),
                ("7 * 8", M),
                ("56 / 7", M),
                ("12 * 6", C),
            ),
        ),


    (
        "MATH_ARITH_MULTDIV_01",
        AssessmentType.MASTERY,
    ):
        _questions(
            "MULTDIV-M",

            (
                ("6 * 4", E),
                ("35 / 5", E),
                ("8 * 9", M),
                ("72 / 8", M),
                ("14 * 7", C),
            ),
        ),


    # ==================================================
    # AGE 9 — FRACTIONS
    # ==================================================

    (
        "MATH_ARITH_FRAC_01",
        AssessmentType.DIAGNOSTIC,
    ):
        _questions(
            "FRAC-D",

            (
                ("1/2 + 1/4", E),
                ("3/5 - 1/5", E),
                ("2/3 + 1/6", M),
                ("3/4 * 2", M),
                ("(5/6 - 1/3) * 2", C),
            ),
        ),


    (
        "MATH_ARITH_FRAC_01",
        AssessmentType.MASTERY,
    ):
        _questions(
            "FRAC-M",

            (
                ("1/3 + 1/3", E),
                ("4/5 - 2/5", E),
                ("3/4 + 1/8", M),
                ("2/5 * 10", M),
                ("(2/3 + 1/6) * 3", C),
            ),
        ),


    # ==================================================
    # AGE 10 — INTEGERS
    # ==================================================

    (
        "MATH_ARITH_INT_01",
        AssessmentType.DIAGNOSTIC,
    ):
        _questions(
            "INT-D",

            (
                ("-4 + 9", E),
                ("7 - 12", E),
                ("-8 + 14 - 3", M),
                ("5 - (-4)", M),
                ("-3 * (-6) - 8", C),
            ),
        ),


    (
        "MATH_ARITH_INT_01",
        AssessmentType.MASTERY,
    ):
        _questions(
            "INT-M",

            (
                ("-6 + 11", E),
                ("8 - 15", E),
                ("-9 + 17 - 5", M),
                ("4 - (-7)", M),
                ("-5 * (-3) + 4", C),
            ),
        ),


    # ==================================================
    # AGE 11 — ORDER OF OPERATIONS
    # ==================================================

    (
        "MATH_ARITH_ORDER_01",
        AssessmentType.DIAGNOSTIC,
    ):
        _questions(
            "ORDER-D",

            (
                ("3 + 4 * 2", E),
                ("12 / 3 + 5", E),
                ("4 * (6 - 2)", M),
                ("18 - 2 * 5 + 3", M),
                ("2 * (3 + 4 * 2) - 5", C),
            ),
        ),


    (
        "MATH_ARITH_ORDER_01",
        AssessmentType.MASTERY,
    ):
        _questions(
            "ORDER-M",

            (
                ("5 + 3 * 2", E),
                ("16 / 4 + 7", E),
                ("3 * (7 - 2)", M),
                ("24 / (2 * 3) + 8", M),
                ("3 + 2 * (5 + 6) - 4", C),
            ),
        ),


    # ==================================================
    # AGE 12 — PRE-ALGEBRA
    # ==================================================

    (
        "MATH_PREALG_EXPR_01",
        AssessmentType.DIAGNOSTIC,
    ):
        _questions(
            "PREALG-D",

            (
                ("x + 3 when x = 4", E),
                ("2x when x = 6", E),
                ("3x + 2 when x = 5", M),
                ("4x - 7 when x = 3", M),
                ("2(x + 4) - x when x = 5", C),
            ),
        ),


    (
        "MATH_PREALG_EXPR_01",
        AssessmentType.MASTERY,
    ):
        _questions(
            "PREALG-M",

            (
                ("x + 5 when x = 2", E),
                ("3x when x = 4", E),
                ("2x - 3 when x = 7", M),
                ("5x + 1 when x = -2", M),
                ("3(x + 2) - x when x = 4", C),
            ),
        ),


    # ==================================================
    # AGE 13 — LINEAR EQUATIONS
    #
    # Existing IDs are preserved because
    # existing assessment regression tests
    # depend on ALG-D-* and ALG-M-*.
    # ==================================================

    (
        "MATH_ALG_LINEAR_01",
        AssessmentType.DIAGNOSTIC,
    ): (

        AssessmentQuestion(
            question_id="ALG-D-01",

            prompt="x + 3 = 7",

            difficulty=E,

            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ALG-D-02",

            prompt="2x = 10",

            difficulty=E,

            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ALG-D-03",

            prompt="2x + 3 = 11",

            difficulty=M,

            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ALG-D-04",

            prompt="4x - 5 = 19",

            difficulty=M,

            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ALG-D-05",

            prompt="3(x + 2) = 18",

            difficulty=C,

            bloom_level="APPLY",
        ),
    ),


    (
        "MATH_ALG_LINEAR_01",
        AssessmentType.MASTERY,
    ): (

        AssessmentQuestion(
            question_id="ALG-M-01",

            prompt="x + 4 = 10",

            difficulty=E,

            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ALG-M-02",

            prompt="5x = 20",

            difficulty=E,

            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ALG-M-03",

            prompt="3x + 2 = 17",

            difficulty=M,

            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ALG-M-04",

            prompt="6x - 7 = 23",

            difficulty=M,

            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ALG-M-05",

            prompt="2(x + 3) = 14",

            difficulty=C,

            bloom_level="APPLY",
        ),
    ),


    # ==================================================
    # AGE 14 — LINEAR GRAPHS
    # ==================================================

    (
        "MATH_GRAPH_LINEAR_01",
        AssessmentType.DIAGNOSTIC,
    ):
        _questions(
            "GRAPH-D",

            (
                (
                    "y = x + 2 when x = 3",
                    E,
                ),

                (
                    "y = 2x when x = 4",
                    E,
                ),

                (
                    "y = 2x + 1 when x = 5",
                    M,
                ),

                (
                    "y = 3x - 4 when x = 3",
                    M,
                ),

                (
                    "y = -2x + 5 when x = -3",
                    C,
                ),
            ),
        ),


    (
        "MATH_GRAPH_LINEAR_01",
        AssessmentType.MASTERY,
    ):
        _questions(
            "GRAPH-M",

            (
                (
                    "y = x + 4 when x = 2",
                    E,
                ),

                (
                    "y = 3x when x = 3",
                    E,
                ),

                (
                    "y = 2x - 3 when x = 6",
                    M,
                ),

                (
                    "y = -x + 7 when x = 4",
                    M,
                ),

                (
                    "y = -3x + 2 when x = -4",
                    C,
                ),
            ),
        ),
}


def get_assessment_questions(
    concept_code: str,
    assessment_type: AssessmentType,
) -> tuple[
    AssessmentQuestion,
    ...,
]:

    return (
        QUESTION_BANK.get(
            (
                concept_code,
                assessment_type,
            ),

            (),
        )
    )