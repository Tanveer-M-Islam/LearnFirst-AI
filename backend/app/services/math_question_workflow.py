
"""LearnFirst AI — Math question workflow.

Responsible for:
1. Recognizing requests for a new Math problem.
2. Recognizing natural-language Math answers.

The Math validator, not this class, decides whether
a submitted answer is correct.
"""

import re


class MathQuestionWorkflow:

    NUMBER = (
        r"[+-]?"
        r"(?:\d+(?:\.\d+)?|\.\d+)"
        r"(?:\s*/\s*\d+(?:\.\d+)?)?"
    )

    # =========================================
    # NEW PROBLEM REQUESTS
    # =========================================

    @staticmethod
    def is_new_problem_request(
        message: str,
    ) -> bool:

        text = " ".join(
            message.lower().strip().split()
        ).rstrip(".!?")

        patterns = [
            (
                r"(?:please\s+)?"
                r"(?:give|show|create|generate|ask)"
                r"\s+(?:me\s+)?"
                r"(?:another|a\s+new|new|"
                r"the\s+next|next|one\s+more)"
                r"\s+(?:math\s+)?(?:practice\s+)?"
                r"(?:problem|question|exercise)"
            ),
            (
                r"(?:please\s+)?"
                r"(?:can|could)\s+(?:you\s+)?"
                r"(?:give|show|create|generate)"
                r"\s+me\s+"
                r"(?:another|a\s+new|next)"
                r"\s+(?:math\s+)?(?:practice\s+)?"
                r"(?:problem|question|exercise)"
            ),
            (
                r"(?:another|new|next|one\s+more)"
                r"\s+(?:math\s+)?(?:practice\s+)?"
                r"(?:problem|question|exercise)"
                r"(?:\s+please)?"
            ),
            r"(?:give|show)\s+me\s+another\s+one",
            (
                r"(?:can|could)\s+i"
                r"\s+(?:have|get|try)"
                r"\s+(?:another|a\s+new|next)"
                r"\s+(?:problem|question|exercise)"
            ),
        ]

        return any(
            re.fullmatch(pattern, text)
            for pattern in patterns
        )

    # =========================================
    # NATURAL-LANGUAGE MATH ANSWERS
    # =========================================

    @classmethod
    def is_natural_math_answer(
        cls,
        message: str,
    ) -> bool:
        """
        Determine whether the learner is
        submitting a numerical answer.

        Examples:
            4
            The answer is 4
            The answer is maybe 4
            The answer may be 4
            I think the result is 13
            I think it's 14
            Maybe 4
            I guess 4
            I don't know, maybe 4

        This does NOT determine correctness.
        """

        text = " ".join(
            message.lower().strip().split()
        )

        # Ignore ordinary sentence-ending
        # punctuation.
        text = re.sub(
            r"[.!?]+$",
            "",
            text,
        ).strip()

        if not text:
            return False

        # Allow tentative guesses by unsure
        # students to count as attempts.
        text = re.sub(
            (
                r"^i\s+(?:don't|dont)\s+know"
                r"[,;]?\s*"
            ),
            "",
            text,
        ).strip()

        number = cls.NUMBER

        # Examples:
        # "is 4"
        # "maybe 4"
        # "is maybe 4"
        # "may be 4"
        modifiers = (
            r"(?:(?:is|was)\s+)?"
            r"(?:(?:maybe|perhaps|probably|"
            r"possibly|may\s+be|might\s+be|"
            r"could\s+be)\s+)?"
        )

        patterns = [

            # Bare numeric result:
            # 4, -2, 2.5, 3/4
            rf"{number}",

            # The answer is maybe 4
            # My answer is 4
            # The result may be 13
            # Answer: 4
            (
                r"(?:(?:the|my)\s+)?"
                r"(?:answer|result|solution)"
                r"\s*(?::|=)?\s*"
                + modifiers
                + number
            ),

            # I think 4
            # I think the result is 13
            # I guess the answer is maybe 4
            # I think it's 14
            (
                r"i\s+(?:think|guess|believe)\s+"
                r"(?:(?:(?:the|my)\s+)?"
                r"(?:answer|result|solution)\s+)?"
                r"(?:it\s+is\s+|it's\s+)?"
                + modifiers
                + number
            ),

            # I got 4
            rf"i\s+got\s+{number}",

            # Maybe 4
            # Perhaps it is 4
            (
                r"(?:maybe|perhaps|probably|possibly)"
                r"\s+(?:it\s+is\s+|it's\s+)?"
                + number
            ),

            # It is 4
            # It should be 4
            # It could be 4
            (
                r"(?:it\s+is|it's|"
                r"it\s+should\s+be|"
                r"it\s+could\s+be)\s+"
                + number
            ),

            # Is it 4?
            # Could it be 4?
            (
                r"(?:is\s+it|could\s+it\s+be)"
                r"\s+"
                + number
            ),
        ]

        return any(
            re.fullmatch(pattern, text)
            for pattern in patterns
        )
