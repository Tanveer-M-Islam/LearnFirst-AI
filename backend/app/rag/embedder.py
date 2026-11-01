from functools import (
    lru_cache,
)

from sentence_transformers import (
    SentenceTransformer,
)

from app.core.config import (
    get_settings,
)


class EmbeddingService:

    def __init__(
        self,
    ) -> None:

        settings = (
            get_settings()
        )

        self.model_name = (
            settings
            .rag_embedding_model
        )

        self.model = (
            self._load_model(
                self.model_name
            )
        )

    @staticmethod
    @lru_cache(
        maxsize=2
    )
    def _load_model(
        model_name: str,
    ) -> SentenceTransformer:

        return SentenceTransformer(
            model_name,
            device="cpu",
        )

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[
        list[float]
    ]:

        if not texts:

            return []

        embeddings = (
            self.model
            .encode_document(
                texts,
                convert_to_numpy=True,
                normalize_embeddings=True,
                show_progress_bar=False,
            )
        )

        return (
            embeddings
            .astype(
                "float32"
            )
            .tolist()
        )

    def embed_query(
        self,
        query: str,
    ) -> list[float]:

        embedding = (
            self.model
            .encode_query(
                query,
                convert_to_numpy=True,
                normalize_embeddings=True,
                show_progress_bar=False,
            )
        )

        return (
            embedding
            .astype(
                "float32"
            )
            .tolist()
        )