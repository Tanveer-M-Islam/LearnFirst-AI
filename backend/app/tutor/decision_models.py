from pydantic import BaseModel

from app.schemas.enums import (
    AgeGroup,
    AttemptStatus,
    LearningMode,
    Subject,
    TutorAction,
    TutorIntent,
)


class TutorDecisionInput(BaseModel):
    intent: TutorIntent

    attempt_status: AttemptStatus | None = None

    repeated_confusion: bool = False

    prerequisite_gap: bool = False

    new_problem: bool = False


class TutorDecisionResult(BaseModel):
    session_id: str

    student_id: str

    subject: Subject

    mode: LearningMode

    age_group: AgeGroup

    intent: TutorIntent

    next_action: TutorAction

    hint_level: int

    allow_final_answer: bool

    requires_rag: bool

    requires_validation: bool

    requires_mastery_check: bool

    policy_bypass_detected: bool

    reason: str