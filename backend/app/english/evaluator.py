import re

from app.english.models import (
    EnglishEvaluationMode,
    EnglishValidationResult,
)
from app.english.question_bank import (
    EnglishIdea,
    find_english_question,
)
from app.schemas.enums import (
    AttemptStatus,
)


class EnglishEvaluator:

    @classmethod
    def evaluate(
        cls,
        concept_code: str,
        question_prompt: str,
        student_message: str,
    ) -> EnglishValidationResult:

        question = (
            find_english_question(
                concept_code=(
                    concept_code
                ),

                prompt=(
                    question_prompt
                ),
            )
        )


        if (
            question is None
        ):

            return (
                EnglishValidationResult(
                    supported=False,

                    concept_code=(
                        concept_code
                    ),

                    question_id=None,

                    evaluation_mode=None,

                    status=(
                        AttemptStatus
                        .UNCLEAR
                    ),

                    score_percent=0.0,

                    matched_ideas=[],

                    missing_ideas=[],

                    rule_feedback=[],

                    feedback_summary=(
                        "This English question "
                        "is not supported by "
                        "the current evaluator."
                    ),
                )
            )


        if (
            question.evaluation_mode
            == EnglishEvaluationMode.EXACT
        ):

            return (
                cls._evaluate_exact(
                    concept_code=(
                        concept_code
                    ),

                    question=(
                        question
                    ),

                    student_message=(
                        student_message
                    ),
                )
            )


        if (
            question.evaluation_mode
            == EnglishEvaluationMode
            .KEY_IDEAS
        ):

            return (
                cls._evaluate_key_ideas(
                    concept_code=(
                        concept_code
                    ),

                    question=(
                        question
                    ),

                    student_message=(
                        student_message
                    ),
                )
            )


        return (
            cls._evaluate_sentence(
                concept_code=(
                    concept_code
                ),

                question=(
                    question
                ),

                student_message=(
                    student_message
                ),
            )
        )


    # ==================================================
    # Exact-answer evaluation
    # ==================================================

    @classmethod
    def _evaluate_exact(
        cls,
        concept_code: str,
        question,
        student_message: str,
    ) -> EnglishValidationResult:

        normalized = (
            cls._normalize(
                student_message
            )
        )


        if (
            not normalized
        ):

            return (
                cls._unclear(
                    concept_code=(
                        concept_code
                    ),

                    question=(
                        question
                    ),
                )
            )


        accepted = {
            cls._normalize(
                answer
            )

            for answer
            in question.accepted_answers
        }


        correct = (
            normalized
            in accepted
        )


        return (
            EnglishValidationResult(
                supported=True,

                concept_code=(
                    concept_code
                ),

                question_id=(
                    question.question_id
                ),

                evaluation_mode=(
                    question
                    .evaluation_mode
                ),

                status=(
                    AttemptStatus.CORRECT

                    if correct

                    else (
                        AttemptStatus
                        .INCORRECT
                    )
                ),

                score_percent=(
                    100.0
                    if correct
                    else 0.0
                ),

                matched_ideas=(
                    ["accepted answer"]
                    if correct
                    else []
                ),

                missing_ideas=(
                    []
                    if correct
                    else [
                        "correct answer"
                    ]
                ),

                rule_feedback=[],

                feedback_summary=(
                    (
                        "The answer is correct."
                    )

                    if correct

                    else (
                        "The answer does not "
                        "match the expected "
                        "English form."
                    )
                ),
            )
        )


    # ==================================================
    # Reading / key-idea evaluation
    # ==================================================

    @classmethod
    def _evaluate_key_ideas(
        cls,
        concept_code: str,
        question,
        student_message: str,
    ) -> EnglishValidationResult:

        normalized = (
            cls._normalize(
                student_message
            )
        )


        if (
            not normalized
        ):

            return (
                cls._unclear(
                    concept_code=(
                        concept_code
                    ),

                    question=(
                        question
                    ),
                )
            )


        matched: list[str] = []

        missing: list[str] = []


        for idea in (
            question.required_ideas
        ):

            if (
                cls._idea_matches(
                    normalized_message=(
                        normalized
                    ),

                    idea=(
                        idea
                    ),
                )
            ):

                matched.append(
                    idea.label
                )


            else:

                missing.append(
                    idea.label
                )


        total = len(
            question.required_ideas
        )


        matched_count = len(
            matched
        )


        score = (
            round(
                (
                    matched_count
                    / total
                    * 100
                )

                if total
                else 0.0,

                1,
            )
        )


        if (
            matched_count
            >= question
            .minimum_correct_ideas
        ):

            status = (
                AttemptStatus.CORRECT
            )


        elif (
            matched_count > 0
        ):

            status = (
                AttemptStatus
                .PARTIALLY_CORRECT
            )


        elif (
            len(
                normalized.split()
            )
            < 2
        ):

            status = (
                AttemptStatus.UNCLEAR
            )


        else:

            status = (
                AttemptStatus.INCORRECT
            )


        return (
            EnglishValidationResult(
                supported=True,

                concept_code=(
                    concept_code
                ),

                question_id=(
                    question.question_id
                ),

                evaluation_mode=(
                    question
                    .evaluation_mode
                ),

                status=(
                    status
                ),

                score_percent=(
                    score
                ),

                matched_ideas=(
                    matched
                ),

                missing_ideas=(
                    missing
                ),

                rule_feedback=[],

                feedback_summary=(
                    cls._idea_feedback(
                        status=(
                            status
                        ),

                        matched_count=(
                            matched_count
                        ),

                        total=(
                            total
                        ),
                    )
                ),
            )
        )


    # ==================================================
    # Sentence-rule evaluation
    # ==================================================

    @classmethod
    def _evaluate_sentence(
        cls,
        concept_code: str,
        question,
        student_message: str,
    ) -> EnglishValidationResult:

        raw = (
            student_message.strip()
        )


        normalized = (
            cls._normalize(
                raw
            )
        )


        if (
            not normalized
        ):

            return (
                cls._unclear(
                    concept_code=(
                        concept_code
                    ),

                    question=(
                        question
                    ),
                )
            )


        matched: list[str] = []

        missing: list[str] = []


        for idea in (
            question.required_ideas
        ):

            if (
                cls._idea_matches(
                    normalized_message=(
                        normalized
                    ),

                    idea=(
                        idea
                    ),
                )
            ):

                matched.append(
                    idea.label
                )


            else:

                missing.append(
                    idea.label
                )


        rule_feedback: list[str] = []


        checks = 0

        passed_checks = 0


        # ----------------------------------
        # Required ideas
        # ----------------------------------

        for idea in (
            question.required_ideas
        ):

            checks += 1


            if (
                idea.label
                in matched
            ):

                passed_checks += 1


        # ----------------------------------
        # Minimum words
        # ----------------------------------

        if (
            question.minimum_words > 0
        ):

            checks += 1


            word_count = len(
                normalized.split()
            )


            if (
                word_count
                >= question.minimum_words
            ):

                passed_checks += 1

                rule_feedback.append(
                    "Sentence length is sufficient."
                )


            else:

                rule_feedback.append(
                    (
                        "Use at least "
                        f"{question.minimum_words} "
                        "words."
                    )
                )


        # ----------------------------------
        # Capital letter
        # ----------------------------------

        if (
            question
            .require_capital_letter
        ):

            checks += 1


            if (
                raw
                and raw[0].isupper()
            ):

                passed_checks += 1

                rule_feedback.append(
                    (
                        "The sentence begins "
                        "with a capital letter."
                    )
                )


            else:

                rule_feedback.append(
                    (
                        "Begin the sentence "
                        "with a capital letter."
                    )
                )


        # ----------------------------------
        # End punctuation
        # ----------------------------------

        if (
            question
            .require_end_punctuation
        ):

            checks += 1


            if (
                raw.endswith(
                    (
                        ".",
                        "!",
                        "?",
                    )
                )
            ):

                passed_checks += 1

                rule_feedback.append(
                    (
                        "The sentence has "
                        "ending punctuation."
                    )
                )


            else:

                rule_feedback.append(
                    (
                        "Add suitable punctuation "
                        "at the end."
                    )
                )


        score = (
            round(
                (
                    passed_checks
                    / checks
                    * 100
                )

                if checks
                else 0.0,

                1,
            )
        )


        enough_ideas = (
            len(
                matched
            )
            >= question
            .minimum_correct_ideas
        )


        all_rules_passed = (
            passed_checks
            == checks
        )


        if (
            enough_ideas
            and all_rules_passed
        ):

            status = (
                AttemptStatus.CORRECT
            )


        elif (
            passed_checks > 0
        ):

            status = (
                AttemptStatus
                .PARTIALLY_CORRECT
            )


        elif (
            len(
                normalized.split()
            )
            < 2
        ):

            status = (
                AttemptStatus.UNCLEAR
            )


        else:

            status = (
                AttemptStatus.INCORRECT
            )


        return (
            EnglishValidationResult(
                supported=True,

                concept_code=(
                    concept_code
                ),

                question_id=(
                    question.question_id
                ),

                evaluation_mode=(
                    question
                    .evaluation_mode
                ),

                status=(
                    status
                ),

                score_percent=(
                    score
                ),

                matched_ideas=(
                    matched
                ),

                missing_ideas=(
                    missing
                ),

                rule_feedback=(
                    rule_feedback
                ),

                feedback_summary=(
                    cls._sentence_feedback(
                        status
                    )
                ),
            )
        )


    # ==================================================
    # Natural-language answer detection
    # ==================================================

    @classmethod
    def looks_like_answer(
        cls,
        message: str,
    ) -> bool:

        normalized = (
            cls._normalize(
                message
            )
        )


        if (
            not normalized
        ):

            return False


        if (
            "?"
            in message
        ):

            return False


        question_starters = (
            "what ",
            "why ",
            "how ",
            "when ",
            "where ",
            "who ",
            "can ",
            "could ",
            "would ",
            "should ",
            "explain ",
            "tell me ",
            "help me ",
            "teach me ",
        )


        if (
            normalized.startswith(
                question_starters
            )
        ):

            return False


        return True


    # ==================================================
    # Helpers
    # ==================================================

    @classmethod
    def _idea_matches(
        cls,
        normalized_message: str,
        idea: EnglishIdea,
    ) -> bool:

        return any(
            cls._contains_phrase(
                normalized_message,
                alternative,
            )

            for alternative
            in idea.alternatives
        )


    @staticmethod
    def _normalize(
        text: str,
    ) -> str:

        normalized = (
            text
            .lower()
            .strip()
        )


        normalized = re.sub(
            r"[^\w\s']",
            " ",
            normalized,
        )


        normalized = re.sub(
            r"\s+",
            " ",
            normalized,
        )


        return (
            normalized.strip()
        )


    @classmethod
    def _contains_phrase(
        cls,
        normalized_message: str,
        phrase: str,
    ) -> bool:

        normalized_phrase = (
            cls._normalize(
                phrase
            )
        )


        if (
            not normalized_phrase
        ):

            return False


        if (
            " "
            in normalized_phrase
        ):

            return (
                normalized_phrase
                in normalized_message
            )


        pattern = (
            r"\b"
            + re.escape(
                normalized_phrase
            )
            + r"\b"
        )


        return bool(
            re.search(
                pattern,
                normalized_message,
            )
        )


    # ==================================================
    # Feedback
    # ==================================================

    @staticmethod
    def _idea_feedback(
        status: AttemptStatus,
        matched_count: int,
        total: int,
    ) -> str:

        if (
            status
            == AttemptStatus.CORRECT
        ):

            return (
                "The response includes "
                "the main idea expected "
                "for this question."
            )


        if (
            status
            == AttemptStatus
            .PARTIALLY_CORRECT
        ):

            return (
                "The response includes "
                f"{matched_count} of "
                f"{total} useful ideas, "
                "but needs more evidence."
            )


        if (
            status
            == AttemptStatus.INCORRECT
        ):

            return (
                "The response does not yet "
                "show enough evidence for "
                "the expected answer."
            )


        return (
            "The response is too short "
            "or unclear to evaluate."
        )


    @staticmethod
    def _sentence_feedback(
        status: AttemptStatus,
    ) -> str:

        if (
            status
            == AttemptStatus.CORRECT
        ):

            return (
                "The sentence meets the "
                "required structure."
            )


        if (
            status
            == AttemptStatus
            .PARTIALLY_CORRECT
        ):

            return (
                "The sentence has useful "
                "parts, but one or more "
                "English rules still need "
                "attention."
            )


        if (
            status
            == AttemptStatus.INCORRECT
        ):

            return (
                "The sentence does not yet "
                "meet the required English "
                "structure."
            )


        return (
            "The response is too short "
            "or unclear to evaluate."
        )


    @staticmethod
    def _unclear(
        concept_code: str,
        question,
    ) -> EnglishValidationResult:

        return (
            EnglishValidationResult(
                supported=True,

                concept_code=(
                    concept_code
                ),

                question_id=(
                    question.question_id
                ),

                evaluation_mode=(
                    question
                    .evaluation_mode
                ),

                status=(
                    AttemptStatus.UNCLEAR
                ),

                score_percent=0.0,

                matched_ideas=[],

                missing_ideas=[],

                rule_feedback=[],

                feedback_summary=(
                    "The response is too short "
                    "or unclear to evaluate."
                ),
            )
        )