import pytest

from app.english.evaluator import (
    EnglishEvaluator,
)
from app.english.question_bank import (
    ENGLISH_QUESTION_BANK,
    get_english_question,
)
from app.schemas.enums import (
    AttemptStatus,
    DifficultyLevel,
)


ENGLISH_CONCEPTS = [

    "ENG_VOCAB_FOUND_01",

    "ENG_SENT_SIMPLE_01",

    "ENG_GRAMMAR_POS_01",

    "ENG_GRAMMAR_TENSE_01",

    "ENG_READ_CORE_01",

    "ENG_SENT_STRUCTURE_01",

    "ENG_GRAMMAR_ADV_01",

    "ENG_READ_INFERENCE_01",
]


@pytest.mark.parametrize(
    "concept_code",
    ENGLISH_CONCEPTS,
)
def test_every_english_concept_has_questions(
    concept_code: str,
):

    assert (
        concept_code
        in ENGLISH_QUESTION_BANK
    )


    assert (
        len(
            ENGLISH_QUESTION_BANK[
                concept_code
            ]
        )
        == 3
    )


@pytest.mark.parametrize(
    "concept_code",
    ENGLISH_CONCEPTS,
)
def test_every_english_concept_has_three_difficulties(
    concept_code: str,
):

    questions = (
        ENGLISH_QUESTION_BANK[
            concept_code
        ]
    )


    difficulties = {
        question.difficulty

        for question
        in questions
    }


    assert (
        DifficultyLevel.EASY
        in difficulties
    )


    assert (
        DifficultyLevel.MODERATE
        in difficulties
    )


    assert (
        DifficultyLevel.CHALLENGING
        in difficulties
    )


def test_vocabulary_exact_answer():

    question = (
        get_english_question(
            concept_code=(
                "ENG_VOCAB_FOUND_01"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),
        )
    )


    assert (
        question is not None
    )


    result = (
        EnglishEvaluator
        .evaluate(
            concept_code=(
                "ENG_VOCAB_FOUND_01"
            ),

            question_prompt=(
                question.prompt
            ),

            student_message=(
                "Huge"
            ),
        )
    )


    assert (
        result.status
        == AttemptStatus.CORRECT
    )


    assert (
        result.score_percent
        == 100.0
    )


def test_wrong_vocabulary_answer():

    question = (
        get_english_question(
            concept_code=(
                "ENG_VOCAB_FOUND_01"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),
        )
    )


    assert (
        question is not None
    )


    result = (
        EnglishEvaluator
        .evaluate(
            concept_code=(
                "ENG_VOCAB_FOUND_01"
            ),

            question_prompt=(
                question.prompt
            ),

            student_message=(
                "tiny"
            ),
        )
    )


    assert (
        result.status
        == AttemptStatus.INCORRECT
    )


def test_simple_sentence_correct():

    question = (
        get_english_question(
            concept_code=(
                "ENG_SENT_SIMPLE_01"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),
        )
    )


    assert (
        question is not None
    )


    result = (
        EnglishEvaluator
        .evaluate(
            concept_code=(
                "ENG_SENT_SIMPLE_01"
            ),

            question_prompt=(
                question.prompt
            ),

            student_message=(
                "The cat is sleeping."
            ),
        )
    )


    assert (
        result.status
        == AttemptStatus.CORRECT
    )


def test_sentence_missing_capital_is_partial():

    question = (
        get_english_question(
            concept_code=(
                "ENG_SENT_SIMPLE_01"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),
        )
    )


    assert (
        question is not None
    )


    result = (
        EnglishEvaluator
        .evaluate(
            concept_code=(
                "ENG_SENT_SIMPLE_01"
            ),

            question_prompt=(
                question.prompt
            ),

            student_message=(
                "the cat is sleeping."
            ),
        )
    )


    assert (
        result.status
        == AttemptStatus
        .PARTIALLY_CORRECT
    )


def test_parts_of_speech():

    question = (
        get_english_question(
            concept_code=(
                "ENG_GRAMMAR_POS_01"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),
        )
    )


    assert (
        question is not None
    )


    result = (
        EnglishEvaluator
        .evaluate(
            concept_code=(
                "ENG_GRAMMAR_POS_01"
            ),

            question_prompt=(
                question.prompt
            ),

            student_message=(
                "dog"
            ),
        )
    )


    assert (
        result.status
        == AttemptStatus.CORRECT
    )


def test_tense_answer():

    question = (
        get_english_question(
            concept_code=(
                "ENG_GRAMMAR_TENSE_01"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),
        )
    )


    assert (
        question is not None
    )


    result = (
        EnglishEvaluator
        .evaluate(
            concept_code=(
                "ENG_GRAMMAR_TENSE_01"
            ),

            question_prompt=(
                question.prompt
            ),

            student_message=(
                "goes"
            ),
        )
    )


    assert (
        result.status
        == AttemptStatus.CORRECT
    )


def test_reading_comprehension():

    question = (
        get_english_question(
            concept_code=(
                "ENG_READ_CORE_01"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),
        )
    )


    assert (
        question is not None
    )


    result = (
        EnglishEvaluator
        .evaluate(
            concept_code=(
                "ENG_READ_CORE_01"
            ),

            question_prompt=(
                question.prompt
            ),

            student_message=(
                "She watered the plants."
            ),
        )
    )


    assert (
        result.status
        == AttemptStatus.CORRECT
    )


def test_sentence_structure():

    question = (
        get_english_question(
            concept_code=(
                "ENG_SENT_STRUCTURE_01"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),
        )
    )


    assert (
        question is not None
    )


    result = (
        EnglishEvaluator
        .evaluate(
            concept_code=(
                "ENG_SENT_STRUCTURE_01"
            ),

            question_prompt=(
                question.prompt
            ),

            student_message=(
                "She likes reading books."
            ),
        )
    )


    assert (
        result.status
        == AttemptStatus.CORRECT
    )


def test_intermediate_grammar():

    question = (
        get_english_question(
            concept_code=(
                "ENG_GRAMMAR_ADV_01"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),
        )
    )


    assert (
        question is not None
    )


    result = (
        EnglishEvaluator
        .evaluate(
            concept_code=(
                "ENG_GRAMMAR_ADV_01"
            ),

            question_prompt=(
                question.prompt
            ),

            student_message=(
                "He has finished his work."
            ),
        )
    )


    assert (
        result.status
        == AttemptStatus.CORRECT
    )


def test_reading_inference():

    question = (
        get_english_question(
            concept_code=(
                "ENG_READ_INFERENCE_01"
            ),

            difficulty=(
                DifficultyLevel.EASY
            ),
        )
    )


    assert (
        question is not None
    )


    result = (
        EnglishEvaluator
        .evaluate(
            concept_code=(
                "ENG_READ_INFERENCE_01"
            ),

            question_prompt=(
                question.prompt
            ),

            student_message=(
                "She probably expected rain."
            ),
        )
    )


    assert (
        result.status
        == AttemptStatus.CORRECT
    )


def test_unsupported_question():

    result = (
        EnglishEvaluator
        .evaluate(
            concept_code=(
                "ENG_READ_CORE_01"
            ),

            question_prompt=(
                "Unknown English question"
            ),

            student_message=(
                "answer"
            ),
        )
    )


    assert (
        result.supported
        is False
    )


def test_question_not_treated_as_answer():

    assert (
        EnglishEvaluator
        .looks_like_answer(
            "Can you explain this?"
        )
        is False
    )


def test_normal_response_looks_like_answer():

    assert (
        EnglishEvaluator
        .looks_like_answer(
            (
                "The answer is rainy "
                "because the road is wet."
            )
        )
        is True
    )