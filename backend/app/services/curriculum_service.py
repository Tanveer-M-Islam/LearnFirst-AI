from pathlib import Path

from app.core.config import (
    get_settings,
)
from app.rag.loader import (
    KnowledgeLoader,
)
from app.schemas.curriculum import (
    CurriculumTopicView,
)


class CurriculumService:

    @classmethod
    def list_topics(
        cls,
        subject: str,
        curriculum_profile: (
            str | None
        ) = None,
        root: str | Path | None = None,
    ) -> list[
        CurriculumTopicView
    ]:

        settings = get_settings()

        knowledge_root = (
            root
            if root is not None
            else settings
            .rag_knowledge_dir
        )

        documents = (
            KnowledgeLoader
            .load_directory(
                knowledge_root
            )
        )

        normalized_subject = (
            subject
            .strip()
            .upper()
        )

        topics: list[
            CurriculumTopicView
        ] = []

        seen: set[str] = set()

        for document in documents:

            if (
                document.subject
                != normalized_subject
            ):
                continue

            if (
                curriculum_profile
                is not None
                and document
                .curriculum_profile
                != curriculum_profile
            ):
                continue

            if (
                document.concept_code
                in seen
            ):
                continue

            seen.add(
                document.concept_code
            )

            topics.append(
                CurriculumTopicView(
                    source_id=(
                        document
                        .source_id
                    ),

                    title=(
                        document.title
                    ),

                    subject=(
                        document.subject
                    ),

                    concept_code=(
                        document
                        .concept_code
                    ),

                    grade_band=(
                        document
                        .grade_band
                    ),

                    curriculum_profile=(
                        document
                        .curriculum_profile
                    ),
                )
            )

        return sorted(
            topics,
            key=lambda item:
                item.title,
        )