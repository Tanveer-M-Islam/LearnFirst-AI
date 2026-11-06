from enum import Enum

from pydantic import BaseModel, Field

from app.schemas.enums import (
    AgeGroup,
    MasteryState,
    Subject,
)


# ======================================================
# Existing RAG curriculum topic
# ======================================================

class CurriculumTopicView(BaseModel):
    source_id: str

    title: str

    subject: str

    concept_code: str

    grade_band: str

    curriculum_profile: str


# ======================================================
# Curriculum progression
# ======================================================

class CurriculumConceptStatus(str, Enum):
    PLANNED = "PLANNED"

    FUTURE = "FUTURE"

    READY = "READY"

    IN_PROGRESS = "IN_PROGRESS"

    NEEDS_REVIEW = "NEEDS_REVIEW"

    MASTERED = "MASTERED"


class CurriculumPathConceptView(BaseModel):
    concept_code: str

    subject: Subject

    title: str

    description: str

    recommended_age: int

    min_age: int

    max_age: int

    min_grade: int

    max_grade: int

    sequence_order: int

    prerequisites: list[str] = Field(
        default_factory=list
    )

    implemented: bool

    curriculum_profile: str

    mastery_state: MasteryState

    mastery_score: float | None = None

    status: CurriculumConceptStatus

    age_appropriate: bool

    grade_appropriate: bool | None = None


class StudentCurriculumPathResponse(BaseModel):
    student_id: str

    subject: Subject

    learner_age: int

    learner_grade: str

    age_group: AgeGroup

    selection_policy: str = (
        "AGE_PRIMARY_GRADE_CONTEXT"
    )

    target_concept: (
        CurriculumPathConceptView
        | None
    )

    recommended_concept: (
        CurriculumPathConceptView
        | None
    )

    prerequisite_review_concept: (
        CurriculumPathConceptView
        | None
    )

    reason_codes: list[str] = Field(
        default_factory=list
    )

    concepts: list[
        CurriculumPathConceptView
    ] = Field(
        default_factory=list
    )