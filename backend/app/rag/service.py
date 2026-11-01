from app.core.config import (
    get_settings,
)
from app.rag.embedder import (
    EmbeddingService,
)
from app.rag.models import (
    RAGContext,
)
from app.rag.vector_store import (
    CurriculumVectorStore,
)


class RAGService:

    def __init__(
        self,
    ) -> None:

        self.settings = (
            get_settings()
        )

        self._embedder: (
            EmbeddingService
            | None
        ) = None

        self._vector_store: (
            CurriculumVectorStore
            | None
        ) = None

    @property
    def embedder(
        self,
    ) -> EmbeddingService:

        if self._embedder is None:

            self._embedder = (
                EmbeddingService()
            )

        return self._embedder

    @property
    def vector_store(
        self,
    ) -> CurriculumVectorStore:

        if (
            self._vector_store
            is None
        ):

            self._vector_store = (
                CurriculumVectorStore()
            )

        return (
            self._vector_store
        )

    def retrieve(
        self,
        query: str,
        subject: str | None = None,
        concept_code: (
            str | None
        ) = None,
    ) -> RAGContext:

        if (
            not self.settings
            .rag_enabled
        ):

            return RAGContext(
                query=query,
                chunks=[],
            )

        if (
            self.vector_store
            .count()
            == 0
        ):

            return RAGContext(
                query=query,
                chunks=[],
            )

        query_embedding = (
            self.embedder
            .embed_query(
                query
            )
        )

        chunks = (
            self.vector_store
            .query(
                query_embedding=(
                    query_embedding
                ),

                subject=(
                    subject
                ),

                concept_code=(
                    concept_code
                ),

                top_k=(
                    self.settings
                    .rag_top_k
                ),
            )
        )

        # If the concept-specific
        # search found nothing,
        # broaden to subject-level
        # retrieval.

        if (
            not chunks
            and subject
            and concept_code
        ):

            chunks = (
                self.vector_store
                .query(
                    query_embedding=(
                        query_embedding
                    ),

                    subject=(
                        subject
                    ),

                    concept_code=None,

                    top_k=(
                        self.settings
                        .rag_top_k
                    ),
                )
            )

        return RAGContext(
            query=query,
            chunks=chunks,
        )