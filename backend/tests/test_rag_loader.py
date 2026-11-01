from pathlib import Path

from app.rag.loader import (
    KnowledgeLoader,
)


def test_load_curriculum_document(
    tmp_path: Path,
):

    file_path = (
        tmp_path
        / "sample.md"
    )

    file_path.write_text(
        """
---
source_id: TEST_SCI_01
title: Test Science
subject: SCIENCE
concept_code: TEST_CONCEPT
grade_band: 6-8
source_type: TEST
curriculum_profile: test_profile
---

# Test Topic

Plants need light.

They also need water.
""".strip(),
        encoding="utf-8",
    )

    document = (
        KnowledgeLoader.load_file(
            file_path
        )
    )

    assert (
        document.source_id
        == "TEST_SCI_01"
    )

    assert (
        document.subject
        == "SCIENCE"
    )

    assert (
        document.concept_code
        == "TEST_CONCEPT"
    )

    assert (
        "Plants need light"
        in document.content
    )


def test_chunk_document(
    tmp_path: Path,
):

    file_path = (
        tmp_path
        / "sample.md"
    )

    file_path.write_text(
        """
---
source_id: TEST_SCI_02
title: Test Topic
subject: SCIENCE
concept_code: TEST_TOPIC
grade_band: 6-8
source_type: TEST
curriculum_profile: test_profile
---

# Topic

First learning point.

Second learning point.

Third learning point.
""".strip(),
        encoding="utf-8",
    )

    document = (
        KnowledgeLoader.load_file(
            file_path
        )
    )

    chunks = (
        KnowledgeLoader
        .chunk_document(
            document,
            max_chars=50,
        )
    )

    assert (
        len(chunks)
        >= 2
    )

    assert all(
        chunk.source_id
        == "TEST_SCI_02"
        for chunk
        in chunks
    )


def test_missing_frontmatter_fails(
    tmp_path: Path,
):

    file_path = (
        tmp_path
        / "bad.md"
    )

    file_path.write_text(
        "# No metadata",
        encoding="utf-8",
    )

    try:

        KnowledgeLoader.load_file(
            file_path
        )

        assert False

    except ValueError:

        assert True