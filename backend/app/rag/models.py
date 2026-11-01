from pydantic import (
    BaseModel,
    Field,
)


class KnowledgeDocument(
    BaseModel
):
    source_id: str

    title: str

    subject: str

    concept_code: str

    grade_band: str

    source_type: str

    curriculum_profile: str

    content: str

    file_path: str


class KnowledgeChunk(
    BaseModel
):
    chunk_id: str

    source_id: str

    title: str

    subject: str

    concept_code: str

    grade_band: str

    source_type: str

    curriculum_profile: str

    text: str

    chunk_index: int

    file_path: str


class RetrievedChunk(
    BaseModel
):
    chunk_id: str

    source_id: str

    title: str

    subject: str

    concept_code: str

    text: str

    score: float = Field(
        ge=0.0,
    )


class RAGSourceView(
    BaseModel
):
    source_id: str

    title: str

    subject: str

    concept_code: str

    score: float


class RAGContext(
    BaseModel
):
    query: str

    chunks: list[
        RetrievedChunk
    ] = Field(
        default_factory=list
    )

    @property
    def has_context(
        self,
    ) -> bool:

        return bool(
            self.chunks
        )

    def as_prompt_text(
        self,
    ) -> str:

        if not self.chunks:

            return (
                "No verified curriculum "
                "context was retrieved."
            )

        sections: list[str] = []

        for index, chunk in (
            enumerate(
                self.chunks,
                start=1,
            )
        ):

            sections.append(
                (
                    f"[SOURCE {index}]\n"
                    f"Title: "
                    f"{chunk.title}\n"
                    f"Concept: "
                    f"{chunk.concept_code}\n"
                    f"Content:\n"
                    f"{chunk.text}"
                )
            )

        return "\n\n".join(
            sections
        )

    def public_sources(
        self,
    ) -> list[RAGSourceView]:

        seen: set[str] = set()

        sources: list[
            RAGSourceView
        ] = []

        for chunk in self.chunks:

            if (
                chunk.source_id
                in seen
            ):
                continue

            seen.add(
                chunk.source_id
            )

            sources.append(
                RAGSourceView(
                    source_id=(
                        chunk.source_id
                    ),

                    title=(
                        chunk.title
                    ),

                    subject=(
                        chunk.subject
                    ),

                    concept_code=(
                        chunk.concept_code
                    ),

                    score=round(
                        chunk.score,
                        4,
                    ),
                )
            )

        return sources