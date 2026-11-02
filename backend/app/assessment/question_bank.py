from dataclasses import (
    dataclass,
)

from app.schemas.enums import (
    AssessmentType,
    DifficultyLevel,
)


@dataclass(
    frozen=True
)
class AssessmentQuestion:

    question_id: str

    prompt: str

    difficulty: (
        DifficultyLevel
    )

    bloom_level: str


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


    # ======================================================
    # BASIC ARITHMETIC
    # ======================================================

    (
        "MATH_ARITH_BASIC_01",
        AssessmentType.DIAGNOSTIC,
    ): (

        AssessmentQuestion(
            question_id="BASIC-D-01",
            prompt="12 + 9",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="BASIC-D-02",
            prompt="25 - 8",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="BASIC-D-03",
            prompt="7 * 6",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="BASIC-D-04",
            prompt="48 / 6 + 5",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="BASIC-D-05",
            prompt="4 * (8 - 3) + 6",
            difficulty=(
                DifficultyLevel.CHALLENGING
            ),
            bloom_level="APPLY",
        ),
    ),


    (
        "MATH_ARITH_BASIC_01",
        AssessmentType.MASTERY,
    ): (

        AssessmentQuestion(
            question_id="BASIC-M-01",
            prompt="16 + 7",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="BASIC-M-02",
            prompt="31 - 14",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="BASIC-M-03",
            prompt="8 * 7",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="BASIC-M-04",
            prompt="63 / 7 + 8",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="BASIC-M-05",
            prompt="3 * (9 + 2) - 7",
            difficulty=(
                DifficultyLevel.CHALLENGING
            ),
            bloom_level="APPLY",
        ),
    ),


    # ======================================================
    # INTEGERS
    # ======================================================

    (
        "MATH_ARITH_INT_01",
        AssessmentType.DIAGNOSTIC,
    ): (

        AssessmentQuestion(
            question_id="INT-D-01",
            prompt="-4 + 9",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="INT-D-02",
            prompt="7 - 12",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="INT-D-03",
            prompt="-5 + 13 - 4",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="INT-D-04",
            prompt="-3 * 4 + 18",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="INT-D-05",
            prompt="(-7 + 12) * 3",
            difficulty=(
                DifficultyLevel.CHALLENGING
            ),
            bloom_level="APPLY",
        ),
    ),


    (
        "MATH_ARITH_INT_01",
        AssessmentType.MASTERY,
    ): (

        AssessmentQuestion(
            question_id="INT-M-01",
            prompt="-6 + 10",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="INT-M-02",
            prompt="5 - 13",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="INT-M-03",
            prompt="8 - (-4)",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="INT-M-04",
            prompt="-5 * 3 + 22",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="INT-M-05",
            prompt="-4 * (-5) - 8",
            difficulty=(
                DifficultyLevel.CHALLENGING
            ),
            bloom_level="APPLY",
        ),
    ),


    # ======================================================
    # FRACTIONS
    # ======================================================

    (
        "MATH_ARITH_FRAC_01",
        AssessmentType.DIAGNOSTIC,
    ): (

        AssessmentQuestion(
            question_id="FRAC-D-01",
            prompt="1/2 + 1/4",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="FRAC-D-02",
            prompt="3/4 - 1/4",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="FRAC-D-03",
            prompt="2/3 + 1/6",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="FRAC-D-04",
            prompt="3/5 * 10",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="FRAC-D-05",
            prompt="5/6 - 1/4",
            difficulty=(
                DifficultyLevel.CHALLENGING
            ),
            bloom_level="APPLY",
        ),
    ),


    (
        "MATH_ARITH_FRAC_01",
        AssessmentType.MASTERY,
    ): (

        AssessmentQuestion(
            question_id="FRAC-M-01",
            prompt="1/3 + 1/3",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="FRAC-M-02",
            prompt="5/6 - 1/6",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="FRAC-M-03",
            prompt="3/4 + 1/8",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="FRAC-M-04",
            prompt="2/5 * 15",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="FRAC-M-05",
            prompt="2/3 * 9/4",
            difficulty=(
                DifficultyLevel.CHALLENGING
            ),
            bloom_level="APPLY",
        ),
    ),


    # ======================================================
    # ORDER OF OPERATIONS
    # ======================================================

    (
        "MATH_ARITH_ORDER_01",
        AssessmentType.DIAGNOSTIC,
    ): (

        AssessmentQuestion(
            question_id="ORDER-D-01",
            prompt="2 + 3 * 4",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ORDER-D-02",
            prompt="18 - 2 * 5",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ORDER-D-03",
            prompt="4 * (3 + 2)",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ORDER-D-04",
            prompt="24 / (2 * 3) + 6",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ORDER-D-05",
            prompt="3 + 2 * (5 + 4) - 6",
            difficulty=(
                DifficultyLevel.CHALLENGING
            ),
            bloom_level="APPLY",
        ),
    ),


    (
        "MATH_ARITH_ORDER_01",
        AssessmentType.MASTERY,
    ): (

        AssessmentQuestion(
            question_id="ORDER-M-01",
            prompt="4 + 2 * 5",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ORDER-M-02",
            prompt="20 - 3 * 4",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ORDER-M-03",
            prompt="5 * (6 - 2) + 3",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ORDER-M-04",
            prompt="36 / (3 * 2) + 8",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ORDER-M-05",
            prompt="2 * (3 + 4 * 2) - 5",
            difficulty=(
                DifficultyLevel.CHALLENGING
            ),
            bloom_level="APPLY",
        ),
    ),


    # ======================================================
    # LINEAR EQUATIONS
    # ======================================================

    (
        "MATH_ALG_LINEAR_01",
        AssessmentType.DIAGNOSTIC,
    ): (

        AssessmentQuestion(
            question_id="ALG-D-01",
            prompt="x + 3 = 7",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ALG-D-02",
            prompt="2x = 10",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ALG-D-03",
            prompt="2x + 3 = 11",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ALG-D-04",
            prompt="4x - 5 = 19",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ALG-D-05",
            prompt="3(x + 2) = 18",
            difficulty=(
                DifficultyLevel.CHALLENGING
            ),
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
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ALG-M-02",
            prompt="5x = 20",
            difficulty=(
                DifficultyLevel.EASY
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ALG-M-03",
            prompt="3x + 2 = 17",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ALG-M-04",
            prompt="6x - 7 = 23",
            difficulty=(
                DifficultyLevel.MODERATE
            ),
            bloom_level="APPLY",
        ),

        AssessmentQuestion(
            question_id="ALG-M-05",
            prompt="2(x + 3) = 14",
            difficulty=(
                DifficultyLevel.CHALLENGING
            ),
            bloom_level="APPLY",
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