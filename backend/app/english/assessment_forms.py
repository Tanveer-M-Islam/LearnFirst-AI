
from app.english.models import EnglishEvaluationMode
from app.english.question_bank import (
    EnglishIdea,
    EnglishQuestion,
    get_english_questions,
)
from app.schemas.enums import (
    AssessmentType,
    DifficultyLevel,
)


E = DifficultyLevel.EASY
M = DifficultyLevel.MODERATE
C = DifficultyLevel.CHALLENGING

EXACT = EnglishEvaluationMode.EXACT
KEY_IDEAS = EnglishEvaluationMode.KEY_IDEAS
SENTENCE = EnglishEvaluationMode.SENTENCE_RULES


def exact(
    question_id: str,
    prompt: str,
    *answers: str,
    difficulty: DifficultyLevel = M,
) -> EnglishQuestion:
    return EnglishQuestion(
        question_id=question_id,
        prompt=prompt,
        difficulty=difficulty,
        evaluation_mode=EXACT,
        accepted_answers=answers,
    )


def idea(
    label: str,
    *alternatives: str,
) -> EnglishIdea:
    return EnglishIdea(
        code=label.upper().replace(" ", "_"),
        label=label,
        alternatives=alternatives,
    )


def reading(
    question_id: str,
    prompt: str,
    required_idea: EnglishIdea,
    difficulty: DifficultyLevel = M,
) -> EnglishQuestion:
    return EnglishQuestion(
        question_id=question_id,
        prompt=prompt,
        difficulty=difficulty,
        evaluation_mode=KEY_IDEAS,
        required_ideas=(required_idea,),
        minimum_correct_ideas=1,
    )


def sentence(
    question_id: str,
    prompt: str,
    *words: str,
    minimum_words: int = 4,
    difficulty: DifficultyLevel = M,
) -> EnglishQuestion:
    return EnglishQuestion(
        question_id=question_id,
        prompt=prompt,
        difficulty=difficulty,
        evaluation_mode=SENTENCE,
        required_ideas=tuple(
            idea(word, word)
            for word in words
        ),
        minimum_correct_ideas=len(words),
        minimum_words=minimum_words,
        require_capital_letter=True,
        require_end_punctuation=True,
    )


# Diagnostics reuse the existing English
# question bank, whose questions are already
# recognized by the deterministic evaluator.
#
# Mastery uses separate questions.


MASTERY_FORMS: dict[
    str,
    tuple[EnglishQuestion, ...],
] = {

    # Age 7 — Everyday Vocabulary
    "ENG_VOCAB_FOUND_01": (
        exact(
            "VOCAB-MAST-01",
            "What is the opposite of cold?",
            "hot",
            difficulty=E,
        ),
        exact(
            "VOCAB-MAST-02",
            "Which means very small: tiny, enormous, or loud?",
            "tiny",
        ),
        exact(
            "VOCAB-MAST-03",
            "What is the opposite of slow?",
            "fast",
            "quick",
            difficulty=C,
        ),
    ),

    # Age 8 — Simple Sentences
    "ENG_SENT_SIMPLE_01": (
        sentence(
            "SIMPLE-MAST-01",
            "Write a complete sentence using the word 'fish'.",
            "fish",
            minimum_words=3,
            difficulty=E,
        ),
        sentence(
            "SIMPLE-MAST-02",
            "Write a sentence using 'girl' and 'reads'.",
            "girl",
            "reads",
        ),
        sentence(
            "SIMPLE-MAST-03",
            "Write a complete sentence about a teacher helping students.",
            "teacher",
            "students",
            minimum_words=5,
            difficulty=C,
        ),
    ),

    # Age 9 — Parts of Speech
    "ENG_GRAMMAR_POS_01": (
        exact(
            "POS-MAST-01",
            "In 'The bright moon shines', which word is the adjective?",
            "bright",
            difficulty=E,
        ),
        exact(
            "POS-MAST-02",
            "In 'Birds sing softly', which word is the verb?",
            "sing",
        ),
        exact(
            "POS-MAST-03",
            "In 'Mina spoke quietly', which word is the adverb?",
            "quietly",
            difficulty=C,
        ),
    ),

    # Age 10 — Core Tenses
    "ENG_GRAMMAR_TENSE_01": (
        exact(
            "TENSE-MAST-01",
            "Complete: They ___ to class every day. Use walk.",
            "walk",
            difficulty=E,
        ),
        exact(
            "TENSE-MAST-02",
            "Complete: Yesterday she ___ a letter. Use write.",
            "wrote",
        ),
        exact(
            "TENSE-MAST-03",
            "Complete: Tomorrow he ___ his uncle. Use visit.",
            "will visit",
            difficulty=C,
        ),
    ),

    # Age 11 — Reading Comprehension
    "ENG_READ_CORE_01": (
        reading(
            "READ-MAST-01",
            "Farah carried an umbrella to school. What did she carry?",
            idea("umbrella", "umbrella"),
            difficulty=E,
        ),
        reading(
            "READ-MAST-02",
            "Heavy rain flooded the playground. Why could the children not play there?",
            idea(
                "rain and flooding",
                "rain",
                "flooded",
                "flood",
                "raining",
            ),
        ),
        reading(
            "READ-MAST-03",
            "After running, Sara drank water and rested. Why might she have wanted water?",
            idea(
                "thirst",
                "thirsty",
                "thirst",
                "needed water",
                "hydration",
            ),
            difficulty=C,
        ),
    ),

    # Age 12 — Sentence Structure
    "ENG_SENT_STRUCTURE_01": (
        sentence(
            "STRUCT-MAST-01",
            "Write a sentence about a dog sleeping under a tree.",
            "dog",
            "tree",
            minimum_words=5,
            difficulty=E,
        ),
        sentence(
            "STRUCT-MAST-02",
            "Write a sentence using 'because' and 'study'.",
            "because",
            "study",
            minimum_words=5,
        ),
        sentence(
            "STRUCT-MAST-03",
            "Write a sentence about rain using the word 'because'.",
            "rain",
            "because",
            minimum_words=7,
            difficulty=C,
        ),
    ),

    # Age 13 — Intermediate Grammar
    "ENG_GRAMMAR_ADV_01": (
        exact(
            "GRAM-MAST-01",
            "Complete: He has already ___ his homework. Use finish.",
            "finished",
            difficulty=E,
        ),
        exact(
            "GRAM-MAST-02",
            "Complete: If I ___ you, I would apologize. Use be.",
            "were",
        ),
        exact(
            "GRAM-MAST-03",
            "Complete: Neither of the answers ___ correct. Use be.",
            "is",
            difficulty=C,
        ),
    ),

    # Age 14 — Reading and Inference
    "ENG_READ_INFERENCE_01": (
        reading(
            "INFER-MAST-01",
            "People opened umbrellas under dark clouds. What weather did they expect?",
            idea(
                "rain",
                "rain",
                "raining",
                "rainy",
            ),
            difficulty=E,
        ),
        reading(
            "INFER-MAST-02",
            "Rafi heard the school bell and ran toward his classroom. Why did he run?",
            idea(
                "class was starting",
                "late",
                "hurry",
                "class started",
                "bell rang",
                "on time",
            ),
        ),
        reading(
            "INFER-MAST-03",
            "After a performance, everyone applauded and smiled. What can we infer about the audience?",
            idea(
                "enjoyed the performance",
                "enjoyed",
                "liked",
                "happy",
                "impressed",
                "appreciated",
            ),
            difficulty=C,
        ),
    ),
}


def get_english_assessment_form(
    concept_code: str,
    assessment_type: AssessmentType,
) -> tuple[EnglishQuestion, ...]:

    if assessment_type == AssessmentType.DIAGNOSTIC:
        return get_english_questions(concept_code)

    if assessment_type == AssessmentType.MASTERY:
        return MASTERY_FORMS.get(concept_code, ())

    return ()
