from app.schemas.enums import (
    Subject,
)


class RAGQueryBuilder:

    @staticmethod
    def build(
        student_message: str,
        subject: Subject,
        topic: str | None = None,
        concept_code: str | None = None,
        current_problem: (
            str | None
        ) = None,
    ) -> str:

        learner_text = (
            student_message
            .strip()
        )


        # ==================================
        # Non-Science requests
        #
        # Keep existing behavior.
        # ==================================

        if (
            subject
            != Subject.SCIENCE
        ):

            return learner_text


        # ==================================
        # Science retrieval
        #
        # Generic requests such as:
        #
        # "Explain simply"
        # "Give me a hint"
        # "I don't understand"
        #
        # do not contain enough semantic
        # information by themselves.
        #
        # Therefore we enrich retrieval
        # using the ACTIVE learning context.
        # ==================================

        parts: list[str] = [
            (
                "Active Science "
                "learning context."
            )
        ]


        if topic:

            parts.append(
                (
                    "Science topic: "
                    + topic
                )
            )


        if concept_code:

            parts.append(
                (
                    "Concept code: "
                    + concept_code
                )
            )


        if current_problem:

            parts.append(
                (
                    "Current learning "
                    "question: "
                    + current_problem
                )
            )


        parts.append(
            (
                "Learner request or "
                "response: "
                + learner_text
            )
        )


        return (
            "\n".join(
                parts
            )
        )