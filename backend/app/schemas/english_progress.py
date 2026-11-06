from pydantic import BaseModel

from app.schemas.enums import (
    MasteryState,
)


class EnglishAssessmentSummary(
    BaseModel,
):
    score_percent: float

    total_questions: int

    correct_answers: int


class EnglishProgressResponse(
    BaseModel,
):
    student_id: str

    concept_code: str

    mastery_state: MasteryState

    understanding_score_percent: float

    total_attempts: int

    correct_attempts: int

    partial_attempts: int

    independent_attempts: int

    diagnostic: (
        EnglishAssessmentSummary
        | None
    ) = None

    mastery: (
        EnglishAssessmentSummary
        | None
    ) = None