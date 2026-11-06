from dataclasses import dataclass

from app.english.models import (
    EnglishEvaluationMode,
)
from app.schemas.enums import (
    DifficultyLevel,
)


@dataclass(frozen=True)
class EnglishIdea:
    code: str

    label: str

    alternatives: tuple[
        str,
        ...,
    ]


@dataclass(frozen=True)
class EnglishQuestion:
    question_id: str

    prompt: str

    difficulty: DifficultyLevel

    evaluation_mode: EnglishEvaluationMode

    accepted_answers: tuple[
        str,
        ...,
    ] = ()

    required_ideas: tuple[
        EnglishIdea,
        ...,
    ] = ()

    minimum_correct_ideas: int = 0

    minimum_words: int = 0

    require_capital_letter: bool = False

    require_end_punctuation: bool = False


E = DifficultyLevel.EASY

M = DifficultyLevel.MODERATE

C = DifficultyLevel.CHALLENGING


ENGLISH_QUESTION_BANK: dict[
    str,
    tuple[
        EnglishQuestion,
        ...,
    ],
] = {

    # ==================================================
    # AGE 7 — EVERYDAY VOCABULARY
    # ==================================================

    "ENG_VOCAB_FOUND_01": (

        EnglishQuestion(
            question_id=(
                "VOCAB-E-01"
            ),

            prompt=(
                "Which word means "
                "'very big': tiny, "
                "huge, or quiet?"
            ),

            difficulty=E,

            evaluation_mode=(
                EnglishEvaluationMode.EXACT
            ),

            accepted_answers=(
                "huge",
            ),
        ),


        EnglishQuestion(
            question_id=(
                "VOCAB-M-01"
            ),

            prompt=(
                "What is the opposite "
                "of 'hot'?"
            ),

            difficulty=M,

            evaluation_mode=(
                EnglishEvaluationMode.EXACT
            ),

            accepted_answers=(
                "cold",
            ),
        ),


        EnglishQuestion(
            question_id=(
                "VOCAB-C-01"
            ),

            prompt=(
                "Which word best means "
                "'happy': joyful, angry, "
                "or empty?"
            ),

            difficulty=C,

            evaluation_mode=(
                EnglishEvaluationMode.EXACT
            ),

            accepted_answers=(
                "joyful",
            ),
        ),
    ),


    # ==================================================
    # AGE 8 — SIMPLE SENTENCES
    # ==================================================

    "ENG_SENT_SIMPLE_01": (

        EnglishQuestion(
            question_id=(
                "SIMPLE-E-01"
            ),

            prompt=(
                "Write a complete sentence "
                "using the word 'cat'."
            ),

            difficulty=E,

            evaluation_mode=(
                EnglishEvaluationMode
                .SENTENCE_RULES
            ),

            required_ideas=(

                EnglishIdea(
                    code="CAT",

                    label=(
                        "uses the word cat"
                    ),

                    alternatives=(
                        "cat",
                    ),
                ),
            ),

            minimum_correct_ideas=1,

            minimum_words=3,

            require_capital_letter=True,

            require_end_punctuation=True,
        ),


        EnglishQuestion(
            question_id=(
                "SIMPLE-M-01"
            ),

            prompt=(
                "Write a sentence using "
                "'boy' and 'runs'."
            ),

            difficulty=M,

            evaluation_mode=(
                EnglishEvaluationMode
                .SENTENCE_RULES
            ),

            required_ideas=(

                EnglishIdea(
                    code="BOY",

                    label=(
                        "uses boy"
                    ),

                    alternatives=(
                        "boy",
                        "the boy",
                    ),
                ),

                EnglishIdea(
                    code="RUNS",

                    label=(
                        "uses runs"
                    ),

                    alternatives=(
                        "runs",
                        "is running",
                    ),
                ),
            ),

            minimum_correct_ideas=2,

            minimum_words=3,

            require_capital_letter=True,

            require_end_punctuation=True,
        ),


        EnglishQuestion(
            question_id=(
                "SIMPLE-C-01"
            ),

            prompt=(
                "Write a complete sentence "
                "about a bird flying "
                "in the sky."
            ),

            difficulty=C,

            evaluation_mode=(
                EnglishEvaluationMode
                .SENTENCE_RULES
            ),

            required_ideas=(

                EnglishIdea(
                    code="BIRD",

                    label=(
                        "mentions a bird"
                    ),

                    alternatives=(
                        "bird",
                    ),
                ),

                EnglishIdea(
                    code="FLY",

                    label=(
                        "describes flying"
                    ),

                    alternatives=(
                        "fly",
                        "flies",
                        "flying",
                    ),
                ),

                EnglishIdea(
                    code="SKY",

                    label=(
                        "mentions the sky"
                    ),

                    alternatives=(
                        "sky",
                    ),
                ),
            ),

            minimum_correct_ideas=2,

            minimum_words=5,

            require_capital_letter=True,

            require_end_punctuation=True,
        ),
    ),


    # ==================================================
    # AGE 9 — PARTS OF SPEECH
    # ==================================================

    "ENG_GRAMMAR_POS_01": (

        EnglishQuestion(
            question_id=(
                "POS-E-01"
            ),

            prompt=(
                "In the sentence "
                "'The dog runs fast', "
                "which word is the noun?"
            ),

            difficulty=E,

            evaluation_mode=(
                EnglishEvaluationMode.EXACT
            ),

            accepted_answers=(
                "dog",
                "the dog",
            ),
        ),


        EnglishQuestion(
            question_id=(
                "POS-M-01"
            ),

            prompt=(
                "In the sentence "
                "'Mina reads a book', "
                "which word is the verb?"
            ),

            difficulty=M,

            evaluation_mode=(
                EnglishEvaluationMode.EXACT
            ),

            accepted_answers=(
                "reads",
            ),
        ),


        EnglishQuestion(
            question_id=(
                "POS-C-01"
            ),

            prompt=(
                "In the sentence "
                "'The bright sun shines', "
                "which word is the adjective?"
            ),

            difficulty=C,

            evaluation_mode=(
                EnglishEvaluationMode.EXACT
            ),

            accepted_answers=(
                "bright",
            ),
        ),
    ),


    # ==================================================
    # AGE 10 — CORE TENSES
    # ==================================================

    "ENG_GRAMMAR_TENSE_01": (

        EnglishQuestion(
            question_id=(
                "TENSE-E-01"
            ),

            prompt=(
                "Complete the sentence: "
                "'She ___ to school "
                "every day.' "
                "Use the correct form "
                "of 'go'."
            ),

            difficulty=E,

            evaluation_mode=(
                EnglishEvaluationMode.EXACT
            ),

            accepted_answers=(
                "goes",
            ),
        ),


        EnglishQuestion(
            question_id=(
                "TENSE-M-01"
            ),

            prompt=(
                "Correct the sentence: "
                "'Yesterday, he go "
                "to the market.'"
            ),

            difficulty=M,

            evaluation_mode=(
                EnglishEvaluationMode.EXACT
            ),

            accepted_answers=(
                (
                    "yesterday he went "
                    "to the market"
                ),

                (
                    "yesterday, he went "
                    "to the market."
                ),

                (
                    "he went to the market "
                    "yesterday"
                ),

                (
                    "he went to the market "
                    "yesterday."
                ),
            ),
        ),


        EnglishQuestion(
            question_id=(
                "TENSE-C-01"
            ),

            prompt=(
                "Complete the sentence: "
                "'Tomorrow, they ___ "
                "the project.' "
                "Use the future form "
                "of 'finish'."
            ),

            difficulty=C,

            evaluation_mode=(
                EnglishEvaluationMode.EXACT
            ),

            accepted_answers=(
                "will finish",
            ),
        ),
    ),


    # ==================================================
    # AGE 11 — READING COMPREHENSION
    # ==================================================

    "ENG_READ_CORE_01": (

        EnglishQuestion(
            question_id=(
                "READ-E-01"
            ),

            prompt=(
                "Read: 'Rina woke up early "
                "and watered the plants "
                "before school.' "
                "What did Rina do before "
                "school?"
            ),

            difficulty=E,

            evaluation_mode=(
                EnglishEvaluationMode
                .KEY_IDEAS
            ),

            required_ideas=(

                EnglishIdea(
                    code="WATERED",

                    label=(
                        "watered the plants"
                    ),

                    alternatives=(
                        "watered the plants",
                        "water the plants",
                        "watering the plants",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        EnglishQuestion(
            question_id=(
                "READ-M-01"
            ),

            prompt=(
                "Read: 'The road was wet "
                "and people carried umbrellas. "
                "Dark clouds covered the sky.' "
                "What was the weather probably "
                "like?"
            ),

            difficulty=M,

            evaluation_mode=(
                EnglishEvaluationMode
                .KEY_IDEAS
            ),

            required_ideas=(

                EnglishIdea(
                    code="RAIN",

                    label=(
                        "rainy or raining"
                    ),

                    alternatives=(
                        "rainy",
                        "raining",
                        "rain",
                        "it had rained",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        EnglishQuestion(
            question_id=(
                "READ-C-01"
            ),

            prompt=(
                "Read: 'Arif studied every "
                "evening for a week. On Friday, "
                "he smiled when the teacher "
                "returned his test.' "
                "Why was Arif probably smiling?"
            ),

            difficulty=C,

            evaluation_mode=(
                EnglishEvaluationMode
                .KEY_IDEAS
            ),

            required_ideas=(

                EnglishIdea(
                    code="GOOD_RESULT",

                    label=(
                        "he probably received "
                        "a good test result"
                    ),

                    alternatives=(
                        "good result",
                        "good grade",
                        "good score",
                        "did well",
                        "passed",
                    ),
                ),

                EnglishIdea(
                    code="STUDIED",

                    label=(
                        "his studying helped"
                    ),

                    alternatives=(
                        "studied",
                        "worked hard",
                        "prepared",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),
    ),


    # ==================================================
    # AGE 12 — SENTENCE STRUCTURE
    # ==================================================

    "ENG_SENT_STRUCTURE_01": (

        EnglishQuestion(
            question_id=(
                "STRUCT-E-01"
            ),

            prompt=(
                "Correct the sentence: "
                "'She like reading books.'"
            ),

            difficulty=E,

            evaluation_mode=(
                EnglishEvaluationMode.EXACT
            ),

            accepted_answers=(
                "she likes reading books",
                "she likes reading books.",
            ),
        ),


        EnglishQuestion(
            question_id=(
                "STRUCT-M-01"
            ),

            prompt=(
                "Join these ideas into "
                "one correct sentence: "
                "'I was tired. I finished "
                "my homework.'"
            ),

            difficulty=M,

            evaluation_mode=(
                EnglishEvaluationMode
                .KEY_IDEAS
            ),

            required_ideas=(

                EnglishIdea(
                    code="TIRED",

                    label=(
                        "mentions being tired"
                    ),

                    alternatives=(
                        "i was tired",
                        "although i was tired",
                        "even though i was tired",
                    ),
                ),

                EnglishIdea(
                    code="HOMEWORK",

                    label=(
                        "mentions finishing "
                        "homework"
                    ),

                    alternatives=(
                        "finished my homework",
                        "i finished my homework",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),


        EnglishQuestion(
            question_id=(
                "STRUCT-C-01"
            ),

            prompt=(
                "Write one complete sentence "
                "using 'because' to explain "
                "why a student studied."
            ),

            difficulty=C,

            evaluation_mode=(
                EnglishEvaluationMode
                .SENTENCE_RULES
            ),

            required_ideas=(

                EnglishIdea(
                    code="BECAUSE",

                    label=(
                        "uses because"
                    ),

                    alternatives=(
                        "because",
                    ),
                ),

                EnglishIdea(
                    code="STUDY",

                    label=(
                        "mentions studying"
                    ),

                    alternatives=(
                        "study",
                        "studied",
                        "studying",
                    ),
                ),
            ),

            minimum_correct_ideas=2,

            minimum_words=6,

            require_capital_letter=True,

            require_end_punctuation=True,
        ),
    ),


    # ==================================================
    # AGE 13 — INTERMEDIATE GRAMMAR
    # ==================================================

    "ENG_GRAMMAR_ADV_01": (

        EnglishQuestion(
            question_id=(
                "GRAMMAR-E-01"
            ),

            prompt=(
                "Correct the sentence: "
                "'He have finished "
                "his work.'"
            ),

            difficulty=E,

            evaluation_mode=(
                EnglishEvaluationMode.EXACT
            ),

            accepted_answers=(
                "he has finished his work",
                "he has finished his work.",
            ),
        ),


        EnglishQuestion(
            question_id=(
                "GRAMMAR-M-01"
            ),

            prompt=(
                "Correct the sentence: "
                "'If I was you, I would "
                "study more.'"
            ),

            difficulty=M,

            evaluation_mode=(
                EnglishEvaluationMode.EXACT
            ),

            accepted_answers=(
                (
                    "if i were you i would "
                    "study more"
                ),

                (
                    "if i were you, i would "
                    "study more."
                ),
            ),
        ),


        EnglishQuestion(
            question_id=(
                "GRAMMAR-C-01"
            ),

            prompt=(
                "Correct the sentence: "
                "'Neither the teacher nor "
                "the students was ready.'"
            ),

            difficulty=C,

            evaluation_mode=(
                EnglishEvaluationMode.EXACT
            ),

            accepted_answers=(
                (
                    "neither the teacher "
                    "nor the students "
                    "were ready"
                ),

                (
                    "neither the teacher "
                    "nor the students "
                    "were ready."
                ),
            ),
        ),
    ),


    # ==================================================
    # AGE 14 — READING & INFERENCE
    # ==================================================

    "ENG_READ_INFERENCE_01": (

        EnglishQuestion(
            question_id=(
                "INFER-E-01"
            ),

            prompt=(
                "Read: 'Nadia looked at "
                "the dark clouds and quickly "
                "closed all the windows.' "
                "What did Nadia probably "
                "expect?"
            ),

            difficulty=E,

            evaluation_mode=(
                EnglishEvaluationMode
                .KEY_IDEAS
            ),

            required_ideas=(

                EnglishIdea(
                    code="RAIN",

                    label=(
                        "rain or a storm"
                    ),

                    alternatives=(
                        "rain",
                        "raining",
                        "storm",
                        "bad weather",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        EnglishQuestion(
            question_id=(
                "INFER-M-01"
            ),

            prompt=(
                "Read: 'The classroom became "
                "silent when the principal "
                "entered. Several students "
                "quickly put their phones away.' "
                "What can you infer about "
                "the situation?"
            ),

            difficulty=M,

            evaluation_mode=(
                EnglishEvaluationMode
                .KEY_IDEAS
            ),

            required_ideas=(

                EnglishIdea(
                    code="RULE",

                    label=(
                        "students may have been "
                        "breaking a rule"
                    ),

                    alternatives=(
                        "breaking a rule",
                        "phones were not allowed",
                        "not allowed",
                        "should not use phones",
                    ),
                ),

                EnglishIdea(
                    code="AUTHORITY",

                    label=(
                        "they reacted to "
                        "the principal"
                    ),

                    alternatives=(
                        "principal entered",
                        "afraid of principal",
                        "principal might see",
                        "authority",
                    ),
                ),
            ),

            minimum_correct_ideas=1,
        ),


        EnglishQuestion(
            question_id=(
                "INFER-C-01"
            ),

            prompt=(
                "Read: 'Rahim had practiced "
                "his presentation many times. "
                "Before entering the room, "
                "he took a deep breath and "
                "checked his notes once more.' "
                "What can you infer about "
                "Rahim's feelings and why?"
            ),

            difficulty=C,

            evaluation_mode=(
                EnglishEvaluationMode
                .KEY_IDEAS
            ),

            required_ideas=(

                EnglishIdea(
                    code="NERVOUS",

                    label=(
                        "Rahim was nervous "
                        "or anxious"
                    ),

                    alternatives=(
                        "nervous",
                        "anxious",
                        "worried",
                        "tense",
                    ),
                ),

                EnglishIdea(
                    code="EVIDENCE",

                    label=(
                        "uses evidence "
                        "from the passage"
                    ),

                    alternatives=(
                        "deep breath",
                        "checked his notes",
                        "checking his notes",
                        "practiced many times",
                    ),
                ),
            ),

            minimum_correct_ideas=2,
        ),
    ),
}


def get_english_questions(
    concept_code: str,
) -> tuple[
    EnglishQuestion,
    ...,
]:

    return (
        ENGLISH_QUESTION_BANK.get(
            concept_code,
            (),
        )
    )


def find_english_question(
    concept_code: str,
    prompt: str,
) -> EnglishQuestion | None:

    normalized_prompt = (
        prompt
        .strip()
        .lower()
    )


    for question in (
        get_english_questions(
            concept_code
        )
    ):

        if (
            question.prompt
            .strip()
            .lower()
            == normalized_prompt
        ):

            return question


    return None


def get_english_question(
    concept_code: str,
    offset: int = 0,
    difficulty: (
        DifficultyLevel
        | None
    ) = None,
) -> EnglishQuestion | None:

    questions = list(
        get_english_questions(
            concept_code
        )
    )


    if (
        difficulty is not None
    ):

        questions = [
            question

            for question
            in questions

            if (
                question.difficulty
                == difficulty
            )
        ]


    if (
        not questions
    ):

        return None


    index = (
        offset
        % len(
            questions
        )
    )


    return questions[
        index
    ]