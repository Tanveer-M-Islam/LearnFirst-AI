import hashlib
from pathlib import Path

from app.rag.models import (
    KnowledgeChunk,
    KnowledgeDocument,
)


class KnowledgeLoader:

    REQUIRED_METADATA = {
        "source_id",
        "title",
        "subject",
        "concept_code",
        "grade_band",
        "source_type",
        "curriculum_profile",
    }

    @classmethod
    def load_directory(
        cls,
        root: str | Path,
    ) -> list[KnowledgeDocument]:

        root_path = Path(
            root
        )

        if not root_path.exists():

            return []

        documents: list[
            KnowledgeDocument
        ] = []

        for file_path in sorted(
            root_path.rglob(
                "*.md"
            )
        ):

            if (
                "vector_store"
                in file_path.parts
            ):
                continue

            documents.append(
                cls.load_file(
                    file_path
                )
            )

        return documents

    @classmethod
    def load_file(
        cls,
        file_path: str | Path,
    ) -> KnowledgeDocument:

        path = Path(
            file_path
        )

        raw = path.read_text(
            encoding="utf-8"
        )

        metadata, content = (
            cls._parse_frontmatter(
                raw
            )
        )

        missing = (
            cls.REQUIRED_METADATA
            - set(
                metadata.keys()
            )
        )

        if missing:

            raise ValueError(
                (
                    "Missing knowledge "
                    "metadata in "
                    f"{path}: "
                    + ", ".join(
                        sorted(
                            missing
                        )
                    )
                )
            )

        return KnowledgeDocument(
            source_id=(
                metadata[
                    "source_id"
                ]
            ),

            title=(
                metadata[
                    "title"
                ]
            ),

            subject=(
                metadata[
                    "subject"
                ]
                .strip()
                .upper()
            ),

            concept_code=(
                metadata[
                    "concept_code"
                ]
            ),

            grade_band=(
                metadata[
                    "grade_band"
                ]
            ),

            source_type=(
                metadata[
                    "source_type"
                ]
            ),

            curriculum_profile=(
                metadata[
                    "curriculum_profile"
                ]
            ),

            content=(
                content.strip()
            ),

            file_path=str(
                path
            ),
        )

    @staticmethod
    def _parse_frontmatter(
        raw: str,
    ) -> tuple[
        dict[str, str],
        str,
    ]:

        lines = (
            raw
            .replace(
                "\r\n",
                "\n",
            )
            .split("\n")
        )

        if (
            not lines
            or lines[0].strip()
            != "---"
        ):

            raise ValueError(
                "Knowledge document "
                "must begin with "
                "frontmatter."
            )

        metadata: dict[
            str,
            str,
        ] = {}

        closing_index = None

        for index in range(
            1,
            len(lines),
        ):

            line = lines[
                index
            ]

            if (
                line.strip()
                == "---"
            ):

                closing_index = (
                    index
                )

                break

            if ":" not in line:

                continue

            key, value = (
                line.split(
                    ":",
                    1,
                )
            )

            metadata[
                key.strip()
            ] = (
                value.strip()
            )

        if closing_index is None:

            raise ValueError(
                "Knowledge document "
                "frontmatter is not "
                "closed."
            )

        content = "\n".join(
            lines[
                closing_index + 1:
            ]
        )

        return (
            metadata,
            content,
        )

    @classmethod
    def chunk_document(
        cls,
        document: KnowledgeDocument,
        max_chars: int = 1100,
    ) -> list[KnowledgeChunk]:

        sections = (
            cls._split_sections(
                document.content
            )
        )

        chunks: list[
            KnowledgeChunk
        ] = []

        buffer = ""

        chunk_index = 0

        def flush() -> None:
            nonlocal buffer
            nonlocal chunk_index

            text = buffer.strip()

            if not text:
                return

            chunk_id = (
                cls._make_chunk_id(
                    source_id=(
                        document
                        .source_id
                    ),

                    index=(
                        chunk_index
                    ),

                    text=text,
                )
            )

            chunks.append(
                KnowledgeChunk(
                    chunk_id=(
                        chunk_id
                    ),

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

                    source_type=(
                        document
                        .source_type
                    ),

                    curriculum_profile=(
                        document
                        .curriculum_profile
                    ),

                    text=text,

                    chunk_index=(
                        chunk_index
                    ),

                    file_path=(
                        document
                        .file_path
                    ),
                )
            )

            chunk_index += 1

            buffer = ""

        for section in sections:

            if (
                buffer
                and (
                    len(buffer)
                    + len(section)
                    + 2
                    > max_chars
                )
            ):

                flush()

            if buffer:

                buffer += (
                    "\n\n"
                    + section
                )

            else:

                buffer = (
                    section
                )

        flush()

        return chunks

    @staticmethod
    def _split_sections(
        content: str,
    ) -> list[str]:

        blocks = [
            block.strip()
            for block in (
                content
                .replace(
                    "\r\n",
                    "\n",
                )
                .split("\n\n")
            )
            if block.strip()
        ]

        return blocks

    @staticmethod
    def _make_chunk_id(
        source_id: str,
        index: int,
        text: str,
    ) -> str:

        digest = (
            hashlib.sha1(
                (
                    f"{source_id}:"
                    f"{index}:"
                    f"{text}"
                )
                .encode(
                    "utf-8"
                )
            )
            .hexdigest()[:12]
        )

        return (
            f"{source_id}-"
            f"{index}-"
            f"{digest}"
        )