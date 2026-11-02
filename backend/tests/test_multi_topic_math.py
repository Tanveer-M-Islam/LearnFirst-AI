import pytest

from app.adaptive.problem_bank import (
    PROBLEM_BANK,
    get_adaptive_problem,
)
from app.assessment.question_bank import (
    get_assessment_questions,
)
from app.math.validator import (
    MathValidator,
)
from app.schemas.enums import (
    AssessmentType,
    DifficultyLevel,
)


MATH_CONCEPTS = [
    "MATH_ARITH_BASIC_01",
    "MATH_ARITH_INT_01",
    "MATH_ARITH_FRAC_01",
    "MATH_ARITH_ORDER_01",
    "MATH_ALG_LINEAR_01",
]


@pytest.mark.parametrize(
    "concept_code",
    MATH_CONCEPTS,
)
def test_every_math_topic_has_adaptive_bank(
    concept_code: str,
):

    assert (
        concept_code
        in PROBLEM_BANK
    )


    for difficulty in (
        DifficultyLevel.EASY,
        DifficultyLevel.MODERATE,
        DifficultyLevel.CHALLENGING,
    ):

        problems = (
            PROBLEM_BANK[
                concept_code
            ][
                difficulty
            ]
        )


        assert (
            len(
                problems
            )
            >= 3
        )


@pytest.mark.parametrize(
    "concept_code",
    MATH_CONCEPTS,
)
def test_every_math_topic_has_diagnostic(
    concept_code: str,
):

    questions = (
        get_assessment_questions(
            concept_code=(
                concept_code
            ),

            assessment_type=(
                AssessmentType
                .DIAGNOSTIC
            ),
        )
    )


    assert (
        len(
            questions
        )
        == 5
    )


@pytest.mark.parametrize(
    "concept_code",
    MATH_CONCEPTS,
)
def test_every_math_topic_has_mastery_check(
    concept_code: str,
):

    questions = (
        get_assessment_questions(
            concept_code=(
                concept_code
            ),

            assessment_type=(
                AssessmentType
                .MASTERY
            ),
        )
    )


    assert (
        len(
            questions
        )
        == 5
    )


@pytest.mark.parametrize(
    "concept_code",
    MATH_CONCEPTS,
)
def test_adaptive_problems_are_supported(
    concept_code: str,
):

    for difficulty in (
        DifficultyLevel.EASY,
        DifficultyLevel.MODERATE,
        DifficultyLevel.CHALLENGING,
    ):

        for offset in range(
            3
        ):

            problem = (
                get_adaptive_problem(
                    concept_code=(
                        concept_code
                    ),

                    difficulty=(
                        difficulty
                    ),

                    offset=(
                        offset
                    ),
                )
            )


            assert (
                problem
                is not None
            )


            student_message = (
                "x = 0"

                if "x"
                in problem.prompt.lower()

                else "0"
            )


            result = (
                MathValidator
                .validate(
                    problem=(
                        problem.prompt
                    ),

                    student_message=(
                        student_message
                    ),
                )
            )


            assert (
                result.supported
                is True
            )


@pytest.mark.parametrize(
    "concept_code",
    MATH_CONCEPTS,
)
@pytest.mark.parametrize(
    "assessment_type",
    [
        AssessmentType
        .DIAGNOSTIC,

        AssessmentType
        .MASTERY,
    ],
)
def test_assessment_questions_are_supported(
    concept_code: str,
    assessment_type: AssessmentType,
):

    questions = (
        get_assessment_questions(
            concept_code=(
                concept_code
            ),

            assessment_type=(
                assessment_type
            ),
        )
    )


    for question in questions:

        student_message = (
            "x = 0"

            if "x"
            in question.prompt.lower()

            else "0"
        )


        result = (
            MathValidator
            .validate(
                problem=(
                    question.prompt
                ),

                student_message=(
                    student_message
                ),
            )
        )


        assert (
            result.supported
            is True
        )