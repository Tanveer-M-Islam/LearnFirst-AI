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

    "SCI_LIFE_BASIC_01",

    "SCI_MATERIAL_BASIC_01",

    "SCI_PHY_MATTER_01",

    "SCI_BIO_FOODCHAIN_01",

    "SCI_ECO_SYSTEMS_01",

    "SCI_BIO_PHOTO_01",

    "SCI_ENERGY_TRANSFER_01",

    "SCI_CELL_SYSTEMS_01",
]


@pytest.mark.parametrize(
    "concept_code",
    SCIENCE_CONCEPTS,
)
def test_every_science_age_has_question_bank(
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
        == 6
    )


def test_living_things_answer():

    question = (
        get_science_question(
            concept_code=(
                "SCI_LIFE_BASIC_01"
            ),

            offset=0,
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
                "SCI_LIFE_BASIC_01"
            ),

            question_prompt=(
                question.prompt
            ),

            student_message=(
                "Living things need "
                "water, air and food."
            ),
        )
    )


    assert (
        result.status
        == AttemptStatus.CORRECT
    )


def test_material_answer():

    question = (
        get_science_question(
            concept_code=(
                "SCI_MATERIAL_BASIC_01"
            ),

            offset=0,
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
                "SCI_MATERIAL_BASIC_01"
            ),

            question_prompt=(
                question.prompt
            ),

            student_message=(
                "Materials can be "
                "hard or soft and "
                "flexible or rigid."
            ),
        )
    )


    assert (
        result.status
        == AttemptStatus.CORRECT
    )


def test_ecosystem_answer():

    question = (
        get_science_question(
            concept_code=(
                "SCI_ECO_SYSTEMS_01"
            ),

            offset=0,
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
                "SCI_ECO_SYSTEMS_01"
            ),

            question_prompt=(
                question.prompt
            ),

            student_message=(
                "An ecosystem includes "
                "living organisms and "
                "their environment."
            ),
        )
    )


    assert (
        result.status
        == AttemptStatus.CORRECT
    )


def test_energy_transfer_answer():

    question = (
        get_science_question(
            concept_code=(
                "SCI_ENERGY_TRANSFER_01"
            ),

            offset=0,
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
                "SCI_ENERGY_TRANSFER_01"
            ),

            question_prompt=(
                question.prompt
            ),

            student_message=(
                "Energy transfer means "
                "energy moves from one "
                "system to another."
            ),
        )
    )


    assert (
        result.status
        == AttemptStatus.CORRECT
    )


def test_cell_system_answer():

    question = (
        get_science_question(
            concept_code=(
                "SCI_CELL_SYSTEMS_01"
            ),

            offset=2,
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
                "SCI_CELL_SYSTEMS_01"
            ),

            question_prompt=(
                question.prompt
            ),

            student_message=(
                "Cells form tissues "
                "and tissues form organs."
            ),
        )
    )


    assert (
        result.status
        == AttemptStatus.CORRECT
    )


@pytest.mark.parametrize(
    "concept_code",
    SCIENCE_CONCEPTS,
)
@pytest.mark.parametrize(
    "difficulty",
    (
        "EASY",
        "MODERATE",
        "CHALLENGING",
    ),
)
def test_every_science_concept_has_each_difficulty(
    concept_code: str,
    difficulty: str,
):

    questions = (
        SCIENCE_QUESTION_BANK[
            concept_code
        ]
    )


    found = any(
        question
        .difficulty
        .value
        == difficulty

        for question
        in questions
    )


    assert (
        found is True
    )