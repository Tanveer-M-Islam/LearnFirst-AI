import re

from app.science.models import (
    ScienceValidationResult,
)
from app.science.question_bank import (
    ScienceIdea,
    ScienceMisconception,
    find_science_question,
)
from app.schemas.enums import (
    AttemptStatus,
)


class ScienceUnderstandingEvaluator:

    @classmethod
    def evaluate(
        cls,
        concept_code: str,
        question_prompt: str,
        student_message: str,
    ) -> ScienceValidationResult:

        question = (
            find_science_question(
                concept_code=(
                    concept_code
                ),

                prompt=(
                    question_prompt
                ),
            )
        )


        if (
            question
            is None
        ):

            return (
                ScienceValidationResult(
                    supported=False,

                    concept_code=(
                        concept_code
                    ),

                    question_id=None,

                    status=(
                        AttemptStatus
                        .UNCLEAR
                    ),

                    coverage_score=0.0,

                    matched_ideas=[],

                    missing_ideas=[],

                    misconception_code=None,

                    feedback_summary=(
                        "This Science question "
                        "is not supported by "
                        "the current structured "
                        "understanding evaluator."
                    ),
                )
            )


        normalized = (
            cls._normalize(
                student_message
            )
        )


        matched_ideas: list[str] = []

        missing_ideas: list[str] = []


        for idea in (
            question
            .required_ideas
        ):

            if (
                cls._idea_matches(
                    normalized,
                    idea,
                )
            ):

                matched_ideas.append(
                    idea.label
                )

            else:

                missing_ideas.append(
                    idea.label
                )


        misconception_code = (
            cls._find_misconception(
                normalized=(
                    normalized
                ),

                misconceptions=(
                    question
                    .misconceptions
                ),
            )
        )


        total_ideas = (
            len(
                question
                .required_ideas
            )
        )


        matched_count = (
            len(
                matched_ideas
            )
        )


        coverage_score = (
            round(
                (
                    matched_count
                    / total_ideas
                    * 100
                )
                if total_ideas
                else 0.0,

                1,
            )
        )


        word_count = (
            len(
                normalized.split()
            )
        )


        # ==================================
        # Status
        # ==================================

        if (
            matched_count == 0

            and word_count < 3
        ):

            status = (
                AttemptStatus
                .UNCLEAR
            )


        elif (
            misconception_code
            is not None
        ):

            status = (
                AttemptStatus
                .INCORRECT

                if matched_count
                < question
                .minimum_correct_ideas

                else (
                    AttemptStatus
                    .PARTIALLY_CORRECT
                )
            )


        elif (
            matched_count
            >= question
            .minimum_correct_ideas
        ):

            status = (
                AttemptStatus
                .CORRECT
            )


        elif (
            matched_count
            > 0
        ):

            status = (
                AttemptStatus
                .PARTIALLY_CORRECT
            )


        else:

            status = (
                AttemptStatus
                .INCORRECT
            )


        feedback_summary = (
            cls._feedback_summary(
                status=(
                    status
                ),

                matched_count=(
                    matched_count
                ),

                total_ideas=(
                    total_ideas
                ),

                misconception_code=(
                    misconception_code
                ),
            )
        )


        return (
            ScienceValidationResult(
                supported=True,

                concept_code=(
                    concept_code
                ),

                question_id=(
                    question
                    .question_id
                ),

                status=(
                    status
                ),

                coverage_score=(
                    coverage_score
                ),

                matched_ideas=(
                    matched_ideas
                ),

                missing_ideas=(
                    missing_ideas
                ),

                misconception_code=(
                    misconception_code
                ),

                feedback_summary=(
                    feedback_summary
                ),
            )
        )


    # ======================================================
    # Natural-language answer detection
    # ======================================================

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


        words = (
            normalized.split()
        )


        if (
            len(
                words
            )
            < 2
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
            "does ",
            "do ",
            "is ",
            "are ",
            "explain ",
            "tell me ",
            "teach me ",
            "help me ",
        )


        if (
            normalized.startswith(
                question_starters
            )
        ):

            return False


        return True


    # ======================================================
    # Idea matching
    # ======================================================

    @classmethod
    def _idea_matches(
        cls,
        normalized_message: str,
        idea: ScienceIdea,
    ) -> bool:

        return any(
            cls._contains_phrase(
                normalized_message,
                alternative,
            )

            for alternative
            in idea.alternatives
        )


    @classmethod
    def _find_misconception(
        cls,
        normalized: str,
        misconceptions: tuple[
            ScienceMisconception,
            ...,
        ],
    ) -> str | None:

        for misconception in (
            misconceptions
        ):

            for pattern in (
                misconception
                .patterns
            ):

                if (
                    cls._contains_phrase(
                        normalized,
                        pattern,
                    )
                ):

                    return (
                        misconception.code
                    )


        return None


    # ======================================================
    # Text helpers
    # ======================================================

    @staticmethod
    def _normalize(
        text: str,
    ) -> str:

        normalized = (
            text
            .lower()
            .strip()
            .replace(
                "co₂",
                "co2",
            )
            .replace(
                "o₂",
                "o2",
            )
            .replace(
                "h₂o",
                "h2o",
            )
        )


        normalized = re.sub(
            r"[^\w\s\-]",
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


    # ======================================================
    # Feedback
    # ======================================================

    @staticmethod
    def _feedback_summary(
        status: AttemptStatus,
        matched_count: int,
        total_ideas: int,
        misconception_code: (
            str | None
        ),
    ) -> str:

        if (
            status
            == AttemptStatus.CORRECT
        ):

            return (
                "The explanation includes "
                "the main scientific ideas "
                "expected for this question."
            )


        if (
            status
            == AttemptStatus
            .PARTIALLY_CORRECT
        ):

            if (
                misconception_code
                is not None
            ):

                return (
                    "The explanation contains "
                    "useful ideas, but it also "
                    "contains a misconception "
                    "that should be corrected."
                )


            return (
                "The explanation contains "
                f"{matched_count} of "
                f"{total_ideas} expected "
                "concept ideas. More reasoning "
                "is needed."
            )


        if (
            status
            == AttemptStatus.INCORRECT
        ):

            if (
                misconception_code
                is not None
            ):

                return (
                    "The explanation currently "
                    "contains a scientific "
                    "misconception and needs "
                    "another look."
                )


            return (
                "The response does not yet "
                "show enough of the expected "
                "scientific idea."
            )


        return (
            "The response is too short "
            "or unclear to evaluate "
            "confidently."
        )