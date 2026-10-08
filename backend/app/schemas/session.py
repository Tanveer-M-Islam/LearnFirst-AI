from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.enums import (
    LearningMode,
    MasteryState,
    SessionStatus,
    Subject,
)


class LearningSessionCreate(BaseModel):
    student_id: str

    mode: LearningMode

    subject: Subject

    topic: str | None = None

    concept_code: str | None = None

    current_problem: str | None = None


class LearningSessionRead(BaseModel):
    id: str

    student_id: str

    mode: LearningMode

    subject: Subject

    topic: str | None

    concept_code: str | None

    current_problem: str | None

    current_hint_level: int

    attempt_count: int

    direct_answer_requests: int

    current_misconception: str | None

    mastery_state: MasteryState

    last_tutor_action: str | None

    status: SessionStatus

    started_at: datetime

    ended_at: datetime | None

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )