import pytest

from app.science.evaluator import (
    ScienceUnderstandingEvaluator,
)
from app.science.question_bank import (
    SCIENCE_QUESTION_BANK,
    get_science_question,
)
from app.schemas.enums import (
    AttemptStatus,
)


SCIENCE_CONCEPTS = [
    "SCI_BIO_PHOTO_01",
    "SCI_PHY_MATTER_01",
    "SCI_BIO_FOODCHAIN_01",
]


@pytest.mark.parametrize(
    "concept_code",
    SCIENCE_CONCEPTS,
)
def test_each_science_concept_has_questions(
    concept_code: str,
):

    assert (
        concept_code
        in SCIENCE_QUESTION_BANK
    )


    assert (
        len(
            SCIENCE_QUESTION_BANK[
                concept_code
            ]
        )
        >= 3
    )


def test_photosynthesis_complete_answer():

    question = (
        get_science_question(
            "SCI_BIO_PHOTO_01",
            0,
        )
    )


    assert (
        question
        is not None
    )


    result = (
        ScienceUnderstandingEvaluator
        .evaluate(
            concept_code=(
                "SCI_BIO_PHOTO_01"
            ),

            question_prompt=(
                question.prompt
            ),

            student_message=(
                "Plants use sunlight, "
                "water and carbon dioxide "
                "to make glucose and "
                "release oxygen."
            ),
        )
    )


    assert (
        result.status
        == AttemptStatus.CORRECT
    )


    assert (
        result.coverage_score
        >= 80.0
    )


def test_photosynthesis_partial_answer():

    question = (
        get_science_question(
            "SCI_BIO_PHOTO_01",
            0,
        )
    )


    assert (
        question
        is not None
    )


    result = (
        ScienceUnderstandingEvaluator
        .evaluate(
            concept_code=(
                "SCI_BIO_PHOTO_01"
            ),

            question_prompt=(
                question.prompt
            ),

            student_message=(
                "Plants need sunlight "
                "and water."
            ),
        )
    )


    assert (
        result.status
        == (
            AttemptStatus
            .PARTIALLY_CORRECT
        )
    )


def test_photosynthesis_misconception():

    question = (
        get_science_question(
            "SCI_BIO_PHOTO_01",
            0,
        )
    )


    assert (
        question
        is not None
    )


    result = (
        ScienceUnderstandingEvaluator
        .evaluate(
            concept_code=(
                "SCI_BIO_PHOTO_01"
            ),

            question_prompt=(
                question.prompt
            ),

            student_message=(
                "Plants get their "
                "food from soil."
            ),
        )
    )


    assert (
        result.status
        == AttemptStatus.INCORRECT
    )


    assert (
        result.misconception_code
        == (
            "SCI_PHOTO_FOOD_FROM_SOIL"
        )
    )


def test_states_of_matter_answer():

    question = (
        get_science_question(
            "SCI_PHY_MATTER_01",
            1,
        )
    )


    assert (
        question
        is not None
    )


    result = (
        ScienceUnderstandingEvaluator
        .evaluate(
            concept_code=(
                "SCI_PHY_MATTER_01"
            ),

            question_prompt=(
                question.prompt
            ),

            student_message=(
                "When heated, ice "
                "changes from solid "
                "to liquid. When water "
                "boils it changes from "
                "liquid to gas."
            ),
        )
    )


    assert (
        result.status
        == AttemptStatus.CORRECT
    )


def test_food_chain_producer_answer():

    question = (
        get_science_question(
            "SCI_BIO_FOODCHAIN_01",
            1,
        )
    )


    assert (
        question
        is not None
    )


    result = (
        ScienceUnderstandingEvaluator
        .evaluate(
            concept_code=(
                "SCI_BIO_FOODCHAIN_01"
            ),

            question_prompt=(
                question.prompt
            ),

            student_message=(
                "Green plants are "
                "producers because they "
                "make their own food "
                "using photosynthesis."
            ),
        )
    )


    assert (
        result.status
        == AttemptStatus.CORRECT
    )


def test_short_answer_can_be_unclear():

    question = (
        get_science_question(
            "SCI_BIO_PHOTO_01",
            0,
        )
    )


    assert (
        question
        is not None
    )


    result = (
        ScienceUnderstandingEvaluator
        .evaluate(
            concept_code=(
                "SCI_BIO_PHOTO_01"
            ),

            question_prompt=(
                question.prompt
            ),

            student_message="maybe",
        )
    )


    assert (
        result.status
        == AttemptStatus.UNCLEAR
    )


def test_natural_explanation_looks_like_answer():

    assert (
        ScienceUnderstandingEvaluator
        .looks_like_answer(
            (
                "Plants use sunlight "
                "and water to make food."
            )
        )
        is True
    )


def test_question_does_not_look_like_answer():

    assert (
        ScienceUnderstandingEvaluator
        .looks_like_answer(
            (
                "Why do plants "
                "need sunlight?"
            )
        )
        is False
    )


def test_explanation_request_is_not_answer():

    assert (
        ScienceUnderstandingEvaluator
        .looks_like_answer(
            (
                "Explain photosynthesis "
                "to me."
            )
        )
        is False
    )
    