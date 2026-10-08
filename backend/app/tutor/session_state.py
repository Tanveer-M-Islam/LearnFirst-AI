from pydantic import BaseModel

from app.schemas.enums import (
    AgeGroup,
    LearningMode,
    MasteryState,
    Subject,
)


class TutorSessionState(BaseModel):
    session_id: str

    student_id: str

    age_group: AgeGroup

    mode: LearningMode

    subject: Subject

    topic: str | None = None

    concept_code: str | None = None

    attempt_count: int = 0

    hint_level: int = 0

    direct_answer_requests: int = 0

    current_misconception: str | None = None

    mastery_state: MasteryState