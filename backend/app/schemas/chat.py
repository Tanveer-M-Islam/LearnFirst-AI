from pydantic import (
    BaseModel,
    Field,
)

from app.schemas.enums import (
    TutorIntent,
)
from app.tutor.decision_models import (
    TutorDecisionResult,
)


class TutorMessageRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=4000,
    )


class TutorMessageResponse(BaseModel):
    session_id: str

    student_message: str

    detected_intent: TutorIntent

    decision: TutorDecisionResult

    reply: str

    provider: str

    model: str

    latency_ms: float