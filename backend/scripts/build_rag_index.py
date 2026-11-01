from app.rag.indexer import (
    CurriculumIndexer,
)


def main() -> None:

    print(
        "Building LearnFirst "
        "curriculum RAG index..."
    )

    indexer = (
        CurriculumIndexer()
    )

    result = (
        indexer.rebuild()
    )

    print()

    print(
        "RAG index completed."
    )

    print(
        "Documents:",
        result["documents"],
    )

    print(
        "Chunks:",
        result["chunks"],
    )

    print(
        "Indexed:",
        result["indexed"],
    )


if __name__ == "__main__":
    main()