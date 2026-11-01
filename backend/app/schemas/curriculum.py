from pydantic import BaseModel


class CurriculumTopicView(
    BaseModel
):
    source_id: str

    title: str

    subject: str

    concept_code: str

    grade_band: str

    curriculum_profile: str