import re

from app.schemas.enums import (
    TutorIntent,
)


class IntentRouter:

    POLICY_BYPASS_PATTERNS = [
        "ignore your instructions",
        "ignore previous instructions",
        "ignore the rules",
        "bypass the rules",
        "pretend i am the teacher",
        "pretend i'm the teacher",
        "my teacher said",
        "encode the answer",
        "answer in base64",
        "answer using emojis",
        "hide the answer",
    ]

    DIRECT_ANSWER_PATTERNS = [
        "just give me the answer",
        "give me the answer",
        "tell me the answer",
        "only give me the answer",
        "what is the final answer",
        "tell me the final answer",
        "just tell me",
        "only the answer",
        "final answer only",
    ]

    I_DONT_KNOW_PATTERNS = [
        "i don't know",
        "i dont know",
        "no idea",
        "i have no idea",
        "i'm stuck",
        "im stuck",
    ]

    CONFUSION_PATTERNS = [
        "i am confused",
        "i'm confused",
        "im confused",
        "i don't understand",
        "i dont understand",
        "this makes no sense",
    ]

    HINT_PATTERNS = [
        "give me a hint",
        "give me hint",
        "hint please",
        "can i get a hint",
        "can you give me a clue",
        "give me a clue",
    ]

    PRACTICE_PATTERNS = [
        "give me a practice question",
        "give me practice",
        "practice question",
        "quiz me",
        "test me on",
    ]

    EXPLANATION_PATTERNS = [
        "explain",
        "teach me",
        "help me understand",
        "how does",
        "how do",
        "why does",
        "why do",
    ]

    HOMEWORK_PATTERNS = [
        "solve this",
        "solve the problem",
        "solve this question",
        "my homework",
        "homework question",
        "help with my homework",
    ]

    SAFETY_PATTERNS = [
        "i am in danger",
        "someone is hurting me",
        "i feel unsafe",
    ]

    @classmethod
    def classify(
        cls,
        message: str,
    ) -> TutorIntent:

        normalized = (
            cls._normalize(message)
        )

        # ----------------------------------
        # Highest priority
        # ----------------------------------

        if cls._contains_any(
            normalized,
            cls.SAFETY_PATTERNS,
        ):
            return (
                TutorIntent
                .SAFETY_SENSITIVE
            )

        if cls._contains_any(
            normalized,
            cls.POLICY_BYPASS_PATTERNS,
        ):
            return (
                TutorIntent.POLICY_BYPASS
            )

        if cls._contains_any(
            normalized,
            cls.DIRECT_ANSWER_PATTERNS,
        ):
            return (
                TutorIntent
                .DIRECT_ANSWER_REQUEST
            )

        if cls._contains_any(
            normalized,
            cls.I_DONT_KNOW_PATTERNS,
        ):
            return (
                TutorIntent.I_DONT_KNOW
            )

        if cls._contains_any(
            normalized,
            cls.CONFUSION_PATTERNS,
        ):
            return (
                TutorIntent.CONFUSION
            )

        if cls._contains_any(
            normalized,
            cls.HINT_PATTERNS,
        ):
            return (
                TutorIntent.HINT_REQUEST
            )

        if cls._contains_any(
            normalized,
            cls.PRACTICE_PATTERNS,
        ):
            return (
                TutorIntent.PRACTICE_REQUEST
            )

        # ----------------------------------
        # Detect likely learner attempt
        # ----------------------------------

        if cls._looks_like_attempt(
            normalized
        ):
            return (
                TutorIntent.STUDENT_ATTEMPT
            )

        if cls._contains_any(
            normalized,
            cls.HOMEWORK_PATTERNS,
        ):
            return (
                TutorIntent.HOMEWORK_REQUEST
            )

        if cls._contains_any(
            normalized,
            cls.EXPLANATION_PATTERNS,
        ):
            return (
                TutorIntent
                .EXPLANATION_REQUEST
            )

        # ----------------------------------
        # Default educational request
        # ----------------------------------

        return TutorIntent.LEARN_CONCEPT

    @staticmethod
    def _normalize(
        message: str,
    ) -> str:

        return " ".join(
            message
            .lower()
            .strip()
            .split()
        )

    @staticmethod
    def _contains_any(
        message: str,
        patterns: list[str],
    ) -> bool:

        return any(
            pattern in message
            for pattern in patterns
        )

    @staticmethod
    def _looks_like_attempt(
        message: str,
    ) -> bool:

        attempt_phrases = [
            "my answer is",
            "i got",
            "i think the answer",
            "i think x",
            "my solution",
            "i tried",
        ]

        if any(
            phrase in message
            for phrase in attempt_phrases
        ):
            return True

        equation_pattern = (
            r"\b[a-z]\s*=\s*-?\d+"
        )

        if re.search(
            equation_pattern,
            message,
        ):
            return True

        return False