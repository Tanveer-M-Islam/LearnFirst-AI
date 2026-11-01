from pathlib import Path

from app.services.curriculum_service import (
    CurriculumService,
)


def test_curriculum_topics_are_loaded(
    tmp_path: Path,
):

    science_dir = (
        tmp_path
        / "science"
    )

    science_dir.mkdir()

    file_path = (
        science_dir
        / "plants.md"
    )

    file_path.write_text(
        """
---
source_id: TEST_SCI_PLANTS
title: Plants
subject: SCIENCE
concept_code: SCI_TEST_PLANTS
grade_band: 6-8
source_type: TEST
curriculum_profile: test_profile
---

# Plants

Plants need water and light.
""".strip(),
        encoding="utf-8",
    )

    topics = (
        CurriculumService
        .list_topics(
            subject="SCIENCE",

            curriculum_profile=(
                "test_profile"
            ),

            root=tmp_path,
        )
    )

    assert len(
        topics
    ) == 1

    assert (
        topics[0].title
        == "Plants"
    )

    assert (
        topics[0]
        .concept_code
        == "SCI_TEST_PLANTS"
    )