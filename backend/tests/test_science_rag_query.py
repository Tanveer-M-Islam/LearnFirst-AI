from app.rag.query_builder import (
    RAGQueryBuilder,
)
from app.schemas.enums import (
    Subject,
)


def test_generic_science_explanation_gets_context():

    query = (
        RAGQueryBuilder
        .build(
            student_message=(
                "Explain this "
                "concept simply."
            ),

            subject=(
                Subject.SCIENCE
            ),

            topic=(
                "Photosynthesis"
            ),

            concept_code=(
                "SCI_BIO_PHOTO_01"
            ),

            current_problem=None,
        )
    )


    assert (
        "Photosynthesis"
        in query
    )


    assert (
        "SCI_BIO_PHOTO_01"
        in query
    )


    assert (
        "Explain this concept simply."
        in query
    )


def test_generic_hint_gets_active_question():

    question = (
        "What does a plant need "
        "for photosynthesis, and "
        "what does it make?"
    )


    query = (
        RAGQueryBuilder
        .build(
            student_message=(
                "Can you give me "
                "a hint?"
            ),

            subject=(
                Subject.SCIENCE
            ),

            topic=(
                "Photosynthesis"
            ),

            concept_code=(
                "SCI_BIO_PHOTO_01"
            ),

            current_problem=(
                question
            ),
        )
    )


    assert (
        "Photosynthesis"
        in query
    )


    assert (
        question
        in query
    )


    assert (
        "Can you give me a hint?"
        in query
    )


def test_math_query_is_not_modified():

    message = (
        "Can you give me a hint?"
    )


    query = (
        RAGQueryBuilder
        .build(
            student_message=(
                message
            ),

            subject=(
                Subject.MATH
            ),

            topic=(
                "Linear Equations"
            ),

            concept_code=(
                "MATH_ALG_LINEAR_01"
            ),

            current_problem=(
                "2x + 5 = 17"
            ),
        )
    )


    assert (
        query
        == message
    )