from pathlib import Path

import chromadb

from app.core.config import (
    get_settings,
)
from app.rag.models import (
    KnowledgeChunk,
    RetrievedChunk,
)


class CurriculumVectorStore:

    def __init__(
        self,
    ) -> None:

        settings = (
            get_settings()
        )

        path = Path(
            settings
            .rag_vector_store_dir
        )

        path.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.collection_name = (
            settings
            .rag_collection_name
        )

        self.client = (
            chromadb.PersistentClient(
                path=str(
                    path
                )
            )
        )

        self.collection = (
            self.client
            .get_or_create_collection(
                name=(
                    self
                    .collection_name
                ),

                embedding_function=None,

                metadata={
                    "hnsw:space":
                        "cosine",

                    "description": (
                        "LearnFirst trusted "
                        "curriculum knowledge"
                    ),
                },
            )
        )


    def count(
        self,
    ) -> int:

        return (
            self.collection
            .count()
        )


    def reset(
        self,
    ) -> None:

        try:

            self.client.delete_collection(
                name=(
                    self
                    .collection_name
                )
            )

        except Exception:
            pass

        self.collection = (
            self.client
            .get_or_create_collection(
                name=(
                    self
                    .collection_name
                ),

                embedding_function=None,

                metadata={
                    "hnsw:space":
                        "cosine",

                    "description": (
                        "LearnFirst trusted "
                        "curriculum knowledge"
                    ),
                },
            )
        )


    def add_chunks(
        self,
        chunks: list[
            KnowledgeChunk
        ],
        embeddings: list[
            list[float]
        ],
    ) -> None:

        if not chunks:
            return

        if (
            len(chunks)
            != len(embeddings)
        ):

            raise ValueError(
                "Chunk and embedding "
                "counts do not match."
            )

        self.collection.add(
            ids=[
                chunk.chunk_id
                for chunk
                in chunks
            ],

            embeddings=(
                embeddings
            ),

            documents=[
                chunk.text
                for chunk
                in chunks
            ],

            metadatas=[
                {
                    "source_id": (
                        chunk
                        .source_id
                    ),

                    "title": (
                        chunk
                        .title
                    ),

                    "subject": (
                        chunk
                        .subject
                    ),

                    "concept_code": (
                        chunk
                        .concept_code
                    ),

                    "grade_band": (
                        chunk
                        .grade_band
                    ),

                    "source_type": (
                        chunk
                        .source_type
                    ),

                    "curriculum_profile": (
                        chunk
                        .curriculum_profile
                    ),

                    "chunk_index": (
                        chunk
                        .chunk_index
                    ),
                }

                for chunk
                in chunks
            ],
        )


    def query(
        self,
        query_embedding: (
            list[float]
        ),
        subject: (
            str | None
        ),
        concept_code: (
            str | None
        ),
        top_k: int,
    ) -> list[
        RetrievedChunk
    ]:

        collection_count = (
            self.count()
        )

        if (
            collection_count
            == 0
        ):
            return []


        where = None


        if (
            subject
            and concept_code
        ):

            where = {
                "$and": [
                    {
                        "subject":
                            subject
                    },

                    {
                        "concept_code":
                            concept_code
                    },
                ]
            }


        elif subject:

            where = {
                "subject":
                    subject
            }


        result_count = min(
            top_k,
            collection_count,
        )


        results = (
            self.collection
            .query(
                query_embeddings=[
                    query_embedding
                ],

                n_results=(
                    result_count
                ),

                where=where,

                include=[
                    "documents",
                    "metadatas",
                    "distances",
                ],
            )
        )


        ids_group = (
            results.get(
                "ids"
            )
            or [[]]
        )

        documents_group = (
            results.get(
                "documents"
            )
            or [[]]
        )

        metadata_group = (
            results.get(
                "metadatas"
            )
            or [[]]
        )

        distances_group = (
            results.get(
                "distances"
            )
            or [[]]
        )


        ids = (
            ids_group[0]
            if ids_group
            else []
        )

        documents = (
            documents_group[0]
            if documents_group
            else []
        )

        metadatas = (
            metadata_group[0]
            if metadata_group
            else []
        )

        distances = (
            distances_group[0]
            if distances_group
            else []
        )


        retrieved: list[
            RetrievedChunk
        ] = []


        for (
            chunk_id,
            document,
            metadata,
            distance,
        ) in zip(
            ids,
            documents,
            metadatas,
            distances,
        ):

            if (
                document is None
                or metadata is None
            ):
                continue


            numeric_distance = float(
                distance
                if distance
                is not None
                else 1.0
            )

            # Chroma cosine distance:
            #
            # distance = 1 - cosine_similarity
            #
            # therefore:
            #
            # similarity = 1 - distance

            score = (
                1.0
                - numeric_distance
            )

            score = max(
                0.0,
                min(
                    1.0,
                    score,
                ),
            )


            retrieved.append(
                RetrievedChunk(
                    chunk_id=str(
                        chunk_id
                    ),

                    source_id=str(
                        metadata[
                            "source_id"
                        ]
                    ),

                    title=str(
                        metadata[
                            "title"
                        ]
                    ),

                    subject=str(
                        metadata[
                            "subject"
                        ]
                    ),

                    concept_code=str(
                        metadata[
                            "concept_code"
                        ]
                    ),

                    text=str(
                        document
                    ),

                    score=(
                        score
                    ),
                )
            )


        return retrieved