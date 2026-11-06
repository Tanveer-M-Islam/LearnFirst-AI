from dataclasses import dataclass

from app.schemas.enums import (
    AssessmentType,
)


@dataclass(frozen=True)
class EnglishAssessmentQuestion:
    question_id: str
    concept_code: str
    assessment_type: AssessmentType
    prompt: str


QUESTIONS = [

    # ==================================
    # Age 7
    # ==================================

    EnglishAssessmentQuestion(
        "ENG-VOC-D-01",
        "ENG_VOCAB_FOUND_01",
        AssessmentType.DIAGNOSTIC,
        "What is the opposite of hot?",
    ),

    EnglishAssessmentQuestion(
        "ENG-VOC-D-02",
        "ENG_VOCAB_FOUND_01",
        AssessmentType.DIAGNOSTIC,
        "Which word means very big: tiny, huge, or quiet?",
    ),

    EnglishAssessmentQuestion(
        "ENG-VOC-D-03",
        "ENG_VOCAB_FOUND_01",
        AssessmentType.DIAGNOSTIC,
        "What is the opposite of happy?",
    ),

    EnglishAssessmentQuestion(
        "ENG-VOC-D-04",
        "ENG_VOCAB_FOUND_01",
        AssessmentType.DIAGNOSTIC,
        "Which word means fast: quick, slow, or small?",
    ),

    EnglishAssessmentQuestion(
        "ENG-VOC-D-05",
        "ENG_VOCAB_FOUND_01",
        AssessmentType.DIAGNOSTIC,
        "What word means not difficult?",
    ),


    # ==================================
    # Age 10 example
    # Core Tenses
    # ==================================

    EnglishAssessmentQuestion(
        "ENG-TENSE-D-01",
        "ENG_GRAMMAR_TENSE_01",
        AssessmentType.DIAGNOSTIC,
        "Complete: She ___ to school every day. Use go.",
    ),

    EnglishAssessmentQuestion(
        "ENG-TENSE-D-02",
        "ENG_GRAMMAR_TENSE_01",
        AssessmentType.DIAGNOSTIC,
        "Correct: Yesterday he go to the market.",
    ),

    EnglishAssessmentQuestion(
        "ENG-TENSE-D-03",
        "ENG_GRAMMAR_TENSE_01",
        AssessmentType.DIAGNOSTIC,
        "Complete: Tomorrow they ___ the project. Use finish.",
    ),

    EnglishAssessmentQuestion(
        "ENG-TENSE-D-04",
        "ENG_GRAMMAR_TENSE_01",
        AssessmentType.DIAGNOSTIC,
        "Complete: Mina ___ a book every night. Use read.",
    ),

    EnglishAssessmentQuestion(
        "ENG-TENSE-D-05",
        "ENG_GRAMMAR_TENSE_01",
        AssessmentType.DIAGNOSTIC,
        "Correct: Last week I visit my grandmother.",
    ),


    # ==================================
    # Mastery — Core Tenses
    # ==================================

    EnglishAssessmentQuestion(
        "ENG-TENSE-M-01",
        "ENG_GRAMMAR_TENSE_01",
        AssessmentType.MASTERY,
        "Complete: He ___ football every Friday. Use play.",
    ),

    EnglishAssessmentQuestion(
        "ENG-TENSE-M-02",
        "ENG_GRAMMAR_TENSE_01",
        AssessmentType.MASTERY,
        "Correct: Yesterday she walk to school.",
    ),

    EnglishAssessmentQuestion(
        "ENG-TENSE-M-03",
        "ENG_GRAMMAR_TENSE_01",
        AssessmentType.MASTERY,
        "Complete: Tomorrow I ___ my homework. Use finish.",
    ),

    EnglishAssessmentQuestion(
        "ENG-TENSE-M-04",
        "ENG_GRAMMAR_TENSE_01",
        AssessmentType.MASTERY,
        "Correct: He eat breakfast every morning.",
    ),

    EnglishAssessmentQuestion(
        "ENG-TENSE-M-05",
        "ENG_GRAMMAR_TENSE_01",
        AssessmentType.MASTERY,
        "Correct: Last night they watch a movie.",
    ),
]


def get_english_assessment_questions(
    concept_code: str,
    assessment_type: AssessmentType,
) -> list[EnglishAssessmentQuestion]:

    return [
        question
        for question in QUESTIONS
        if (
            question.concept_code
            == concept_code
            and question.assessment_type
            == assessment_type
        )
    ]