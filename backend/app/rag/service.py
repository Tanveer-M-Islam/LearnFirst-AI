from app.core.config import (
    get_settings,
)
from app.rag.embedder import (
    EmbeddingService,
)
from app.rag.models import (
    RAGContext,
    RetrievedChunk,
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

        if (
            self._embedder
            is None
        ):

            self._embedder = (
                EmbeddingService()
            )

        return (
            self._embedder
        )


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
        subject: (
            str | None
        ) = None,
        concept_code: (
            str | None
        ) = None,
    ) -> RAGContext:

        # ----------------------------------
        # 1. RAG disabled
        # ----------------------------------

        if (
            not self.settings
            .rag_enabled
        ):

            return RAGContext(
                query=query,
                chunks=[],
            )


        # ----------------------------------
        # 2. Empty vector database
        # ----------------------------------

        if (
            self.vector_store
            .count()
            == 0
        ):

            return RAGContext(
                query=query,
                chunks=[],
            )


        # ----------------------------------
        # 3. Embed learner query
        # ----------------------------------

        query_embedding = (
            self.embedder
            .embed_query(
                query
            )
        )


        # ----------------------------------
        # 4. Retrieve
        #
        # When a concept is selected,
        # remain STRICTLY inside that
        # concept.
        # ----------------------------------

        raw_chunks = (
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


        # ----------------------------------
        # 5. Relevance filtering
        # ----------------------------------

        relevant_chunks: list[
            RetrievedChunk
        ] = [
            chunk
            for chunk in raw_chunks
            if (
                chunk.score
                >= self.settings
                .rag_min_score
            )
        ]


        # Best result first.

        relevant_chunks.sort(
            key=lambda chunk:
                chunk.score,

            reverse=True,
        )


        # ----------------------------------
        # 6. Minimum result guard
        # ----------------------------------

        if (
            len(
                relevant_chunks
            )
            < self.settings
            .rag_min_results
        ):

            return RAGContext(
                query=query,
                chunks=[],
            )


        # ----------------------------------
        # IMPORTANT
        #
        # Do NOT broaden from:
        #
        # Photosynthesis
        #       ↓
        # all Science
        #
        # when a session already has
        # a concept_code.
        #
        # That would allow unrelated
        # material to enter a grounded
        # response.
        # ----------------------------------

        return RAGContext(
            query=query,
            chunks=(
                relevant_chunks
            ),
        )