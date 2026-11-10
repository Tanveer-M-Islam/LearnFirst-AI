
"""Apply the LearnFirst AI Math question-state fix.

Run from the LearnFirst-AI repository root.

Updates:
  backend/app/services/tutor_chat_service.py

Creates:
  backend/app/services/math_question_workflow.py

Makes a backup of the original tutor service.
"""

from pathlib import Path
import ast
import shutil


ROOT = Path(__file__).resolve().parent

SERVICE = (
    ROOT
    / "backend/app/services/tutor_chat_service.py"
)

HELPER = (
    ROOT
    / "backend/app/services/math_question_workflow.py"
)


HELPER_CODE = r'''"""State-aware Math question and answer classification."""

import re


class MathQuestionWorkflow:

    _NUMBER = (
        r"[+-]?\d+(?:\.\d+)?"
        r"(?:/\d+(?:\.\d+)?)?"
    )

    @staticmethod
    def is_new_problem_request(
        message: str,
    ) -> bool:

        text = " ".join(
            message.lower().strip().split()
        ).rstrip(".!?")

        patterns = (
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
                r"(?:please\s+)?(?:can|could)"
                r"\s+(?:you\s+)?"
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
        )

        return any(
            re.fullmatch(pattern, text)
            for pattern in patterns
        )

    @classmethod
    def is_natural_math_answer(
        cls,
        message: str,
    ) -> bool:

        text = " ".join(
            message.lower().strip().split()
        ).rstrip(".!?")

        number = cls._NUMBER

        prefixes = (
            (
                r"(?:the\s+)?"
                r"(?:answer|result|solution)"
                r"\s*(?:is|may\s+be|might\s+be|"
                r"could\s+be|maybe|[:=])?"
            ),
            (
                r"(?:i\s+(?:think|guess|believe)"
                r"|i\s+got)\s*"
                r"(?:(?:the|my)\s+)?"
                r"(?:answer|result)?\s*"
                r"(?:is|may\s+be|might\s+be|"
                r"could\s+be|it\s+is|it's|[:=])?"
            ),
            (
                r"(?:maybe|perhaps|probably|possibly)"
                r"(?:\s+(?:it\s+is|it's))?"
            ),
            r"(?:it\s+is|it's)",
        )

        return bool(
            re.fullmatch(number, text)
            or any(
                re.fullmatch(
                    prefix + r"\s*" + number,
                    text,
                )
                for prefix in prefixes
            )
        )
'''


def main():

    if not SERVICE.exists():
        raise SystemExit(
            "Run this script from the LearnFirst-AI "
            "repository root."
        )

    source = SERVICE.read_text(
        encoding="utf-8"
    )

    if (
        "from app.services.math_question_workflow "
        "import MathQuestionWorkflow"
        in source
    ):
        raise SystemExit(
            "The Math state fix is already installed. "
            "No files were modified."
        )

    def replace_once(
        old: str,
        new: str,
        label: str,
    ):
        nonlocal source

        count = source.count(old)

        if count != 1:
            raise SystemExit(
                f"Could not safely patch {label}. "
                f"Expected one matching section, "
                f"found {count}. Nothing was written."
            )

        source = source.replace(
            old,
            new,
            1,
        )

    # =====================================
    # 1. Import the Math workflow
    # =====================================

    replace_once(
        (
            "from app.services.tutor_service "
            "import TutorService"
        ),
        (
            "from app.services.math_question_workflow "
            "import MathQuestionWorkflow\n"
            "from app.services.tutor_service "
            "import TutorService"
        ),
        "imports",
    )

    # =====================================
    # 2. Recognize and save new questions
    # =====================================

    replace_once(
        """        intent = IntentRouter.classify(
            student_message
        )""",

        """        intent = IntentRouter.classify(
            student_message
        )

        # AI-07: A new problem must update the
        # saved learning session, not exist only
        # inside an LLM-generated chat reply.

        new_math_problem_request = (
            subject == Subject.MATH
            and intent not in {
                TutorIntent.SAFETY_SENSITIVE,
                TutorIntent.POLICY_BYPASS,
            }
            and MathQuestionWorkflow.is_new_problem_request(
                student_message
            )
        )

        new_math_problem_assigned = False

        if new_math_problem_request:

            previous_problem = (
                learning_session.current_problem
            )

            learning_session = (
                cls._assign_next_math_problem(
                    db=db,
                    learning_session=learning_session,
                )
            )

            new_math_problem_assigned = bool(
                learning_session.current_problem
                and learning_session.current_problem
                != previous_problem
            )

            intent = TutorIntent.PRACTICE_REQUEST

        elif (
            subject == Subject.MATH
            and intent == TutorIntent.LEARN_CONCEPT
            and MathQuestionWorkflow.is_natural_math_answer(
                student_message
            )
        ):
            # "I think the result is 13" must be
            # validated as a submitted answer.
            intent = TutorIntent.STUDENT_ATTEMPT""",

        "initial intent handling",
    )

    # =====================================
    # 3. Prevent assigning twice
    # =====================================

    replace_once(
        """        if intent == TutorIntent.PRACTICE_REQUEST:""",

        """        if (
            intent == TutorIntent.PRACTICE_REQUEST
            and not new_math_problem_request
        ):""",

        "practice assignment",
    )

    # =====================================
    # 4. Tell policy a new problem began
    # =====================================

    replace_once(
        """            decision_input=TutorDecisionInput(
                intent=intent,
                attempt_status=attempt_status,
            ),""",

        """            decision_input=TutorDecisionInput(
                intent=intent,
                attempt_status=attempt_status,
                new_problem=(
                    new_math_problem_request
                    and new_math_problem_assigned
                ),
            ),""",

        "tutor policy decision",
    )

    # =====================================
    # 5. Respond using the saved question
    # =====================================

    marker = """        if refreshed_session is None:
            raise ValueError(
                "Learning session could not be reloaded."
            )"""

    if marker not in source:
        raise SystemExit(
            "Cannot locate the session reload guard. "
            "Nothing was written."
        )

    new_question_response = """
        # AI-07: Respond with the database's
        # active problem, not an LLM invention.

        if new_math_problem_request:

            if new_math_problem_assigned:
                reply = (
                    "Here is your new problem: "
                    f"{refreshed_session.current_problem}. "
                    "Try it independently. "
                    "Tell me your answer or first step."
                )

            else:
                reply = (
                    "I could not find another verified "
                    "question for this concept. "
                    "Please choose a different concept "
                    "or difficulty."
                )

            return cls._response(
                session_id=session_id,
                student_message=student_message,
                intent=intent,
                decision=decision,
                reply=reply,
                provider="system",
                model=(
                    "adaptive-practice"
                    if new_math_problem_assigned
                    else "no-verified-next-problem"
                ),
            )
"""

    source = source.replace(
        marker,
        marker + new_question_response,
        1,
    )

    # =====================================
    # 6. Validate before writing
    # =====================================

    ast.parse(source)
    ast.parse(HELPER_CODE)

    backup = SERVICE.with_suffix(
        ".py.before_math_state_fix.bak"
    )

    if backup.exists():
        raise SystemExit(
            f"Backup already exists: {backup}. "
            "No files were modified."
        )

    shutil.copy2(
        SERVICE,
        backup,
    )

    SERVICE.write_text(
        source,
        encoding="utf-8",
    )

    HELPER.write_text(
        HELPER_CODE,
        encoding="utf-8",
    )

    print("Math question-state fix installed.")
    print("Updated:", SERVICE)
    print("Created:", HELPER)
    print("Backup:", backup)
    print("Python syntax validation passed.")


if __name__ == "__main__":
    main()
