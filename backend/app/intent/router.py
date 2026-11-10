
import re

from app.schemas.enums import TutorIntent


class IntentRouter:
    """
    Classifies learner messages into tutoring intents.

    Important:
    A tentative answer such as "Maybe 14" is still
    a student attempt and should be validated.
    """

    POLICY_BYPASS_PATTERNS = [
        "ignore your instructions",
        "ignore previous instructions",
        "ignore the rules",
        "bypass the rules",
        "pretend i am the teacher",
        "pretend i'm the teacher",
        "my teacher said you must",
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
        "just give me the final answer",
        "give me the final answer",
        "only give me the final answer",
        "just tell me the final answer",
        "show me the final answer",
        "what's the final answer",
        "just give the final answer",
        "give the final answer",
        "only the answer",
        "final answer only",
        "just tell me",
        "give answer",
        "give the answer",
        "tell the answer",
        "what is the answer",
        "what's the answer",
        "answer this question",
        "answer the question",
        "answer of this question",
        "answer this",
        "give me solution",
        "give me the solution",
        "tell me the solution",
        "show me the solution",
        "solve it for me",
        "show me the answer",
        "show the answer",
        "give correct answer",
        "give me correct answer",
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
        "can you give me a hint",
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

    # =========================================
    # MAIN CLASSIFIER
    # =========================================

    @classmethod
    def classify(
        cls,
        message: str,
    ) -> TutorIntent:

        normalized = cls._normalize(message)

        # Safety remains highest priority.
        if cls._contains_any(
            normalized,
            cls.SAFETY_PATTERNS,
        ):
            return TutorIntent.SAFETY_SENSITIVE

        # Never let a numeric answer bypass
        # policy-bypass detection.
        if cls._contains_any(
            normalized,
            cls.POLICY_BYPASS_PATTERNS,
        ):
            return TutorIntent.POLICY_BYPASS

        # Requests for the tutor's answer are
        # different from submitting an answer.
        if cls._contains_any(
            normalized,
            cls.DIRECT_ANSWER_PATTERNS,
        ):
            return TutorIntent.DIRECT_ANSWER_REQUEST

        # NEW:
        # Recognize explicit numerical guesses,
        # including tentative answers such as
        # "The answer maybe 14".
        #
        # Check these before confusion so that
        # "I don't know, maybe 14" can be evaluated.
        if cls._looks_like_numeric_answer(
            normalized
        ):
            return TutorIntent.STUDENT_ATTEMPT

        if cls._contains_any(
            normalized,
            cls.I_DONT_KNOW_PATTERNS,
        ):
            return TutorIntent.I_DONT_KNOW

        if cls._contains_any(
            normalized,
            cls.CONFUSION_PATTERNS,
        ):
            return TutorIntent.CONFUSION

        if cls._contains_any(
            normalized,
            cls.HINT_PATTERNS,
        ):
            return TutorIntent.HINT_REQUEST

        if cls._contains_any(
            normalized,
            cls.PRACTICE_PATTERNS,
        ):
            return TutorIntent.PRACTICE_REQUEST

        if cls._looks_like_attempt(normalized):
            return TutorIntent.STUDENT_ATTEMPT

        if cls._contains_any(
            normalized,
            cls.HOMEWORK_PATTERNS,
        ):
            return TutorIntent.HOMEWORK_REQUEST

        if cls._contains_any(
            normalized,
            cls.EXPLANATION_PATTERNS,
        ):
            return TutorIntent.EXPLANATION_REQUEST

        return TutorIntent.LEARN_CONCEPT

    # =========================================
    # NORMALIZATION
    # =========================================

    @staticmethod
    def _normalize(message: str) -> str:

        return " ".join(
            message.lower().strip().split()
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

    # =========================================
    # NEW: NATURAL NUMERIC ANSWER DETECTION
    # =========================================

    @staticmethod
    def _looks_like_numeric_answer(
        message: str,
    ) -> bool:
        """
        Detect a learner's numeric answer.

        Examples:
        - 14
        - The answer maybe 14
        - The answer is 14
        - I think it's 14
        - Maybe 14
        - I guess 14
        - My answer is 14
        - Answer: 14

        Does not interpret:
        - Give me the answer
        - I think multiplication
        - What is the final answer?
        as numeric attempts.
        """

        number = (
            r"[+-]?\d+(?:\.\d+)?"
            r"(?:/\d+(?:\.\d+)?)?"
        )

        # Bare number, with optional punctuation.
        if re.fullmatch(
            rf"{number}[.!?]?",
            message,
        ):
            return True

        # Allow a student to express uncertainty
        # without losing the answer attempt.
        text = re.sub(
            (
                r"^i\s+(?:don't|dont)\s+know"
                r"[\s,.\-]*"
            ),
            "",
            message,
        ).strip()

        prefixes = (
            r"(?:"
            r"(?:the|my)\s+answer"
            r"(?:\s+(?:is|may\s+be|might\s+be|"
            r"could\s+be|maybe))?"
            r"|answer\s*[:=]?"
            r"|i\s+(?:think|guess|believe|got)"
            r"(?:\s+(?:it(?:\s+is|'s)|"
            r"the\s+answer(?:\s+is)?))?"
            r"|it(?:\s+is|'s)"
            r"|maybe(?:\s+it(?:\s+is|'s))?"
            r"|perhaps"
            r"|probably"
            r"|possibly"
            r"|i(?:'d|\s+would)\s+say"
            r")"
        )

        pattern = (
            rf"{prefixes}"
            rf"\s*[:=]?\s*"
            rf"{number}"
            rf"(?:\s*,?\s*right)?"
            rf"[.!?]?"
        )

        return bool(
            re.fullmatch(pattern, text)
        )

    # =========================================
    # EXISTING STUDENT ATTEMPT DETECTION
    # =========================================

    @staticmethod
    def _looks_like_attempt(
        message: str,
    ) -> bool:

        attempt_phrases = [
            "my answer is",
            "my answer",
            "i got",
            "i think the answer",
            "i think x",
            "my solution",
            "i tried",
            "i think it is",
            "i think it's",
        ]

        if any(
            phrase in message
            for phrase in attempt_phrases
        ):
            return True

        # Algebra: x = 5
        equation_answer_pattern = (
            r"\b[a-z]\s*=\s*"
            r"-?\d+(?:\.\d+)?"
            r"(?:/\d+(?:\.\d+)?)?"
        )

        if re.search(
            equation_answer_pattern,
            message,
        ):
            return True

        # Algebraic working: 3x = 12
        if re.search(
            r"[0-9x]+\s*=\s*[0-9x\-+*/]+",
            message,
        ):
            return True

        return False
