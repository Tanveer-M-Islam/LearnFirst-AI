from app.core.config import (
    get_settings,
)
from app.rag.embedder import (
    EmbeddingService,
)
from app.rag.loader import (
    KnowledgeLoader,
)
from app.rag.models import (
    KnowledgeChunk,
)
from app.rag.vector_store import (
    CurriculumVectorStore,
)


class CurriculumIndexer:

    def __init__(
        self,
    ) -> None:

        self.settings = (
            get_settings()
        )

        self.embedder = (
            EmbeddingService()
        )

        self.vector_store = (
            CurriculumVectorStore()
        )

    def rebuild(
        self,
    ) -> dict[str, int]:

        documents = (
            KnowledgeLoader
            .load_directory(
                self.settings
                .rag_knowledge_dir
            )
        )

        all_chunks: list[
            KnowledgeChunk
        ] = []

        for document in (
            documents
        ):

            chunks = (
                KnowledgeLoader
                .chunk_document(
                    document
                )
            )

            all_chunks.extend(
                chunks
            )

        self.vector_store.reset()

        if all_chunks:

            embeddings = (
                self.embedder
                .embed_documents(
                    [
                        chunk.text
                        for chunk
                        in all_chunks
                    ]
                )
            )

            self.vector_store.add_chunks(
                chunks=all_chunks,
                embeddings=embeddings,
            )

        return {
            "documents": (
                len(documents)
            ),

            "chunks": (
                len(all_chunks)
            ),

            "indexed": (
                self.vector_store
                .count()
            ),
        }