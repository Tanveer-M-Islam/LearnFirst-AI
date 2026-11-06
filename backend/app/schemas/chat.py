from pydantic import (
    BaseModel,
    Field,
)

from app.english.models import (
    EnglishValidationView,
)
from app.math.models import (
    MathValidationView,
)
from app.rag.models import (
    RAGSourceView,
)
from app.science.models import (
    ScienceValidationView,
)
from app.schemas.enums import (
    TutorIntent,
)
from app.tutor.decision_models import (
    TutorDecisionResult,
)


class TutorMessageRequest(
    BaseModel
):
    message: str = Field(
        min_length=1,
        max_length=4000,
    )


class TutorMessageResponse(
    BaseModel
):
    session_id: str

    student_message: str

    detected_intent: TutorIntent

    decision: TutorDecisionResult

    math_validation: (
        MathValidationView
        | None
    ) = None

    science_validation: (
        ScienceValidationView
        | None
    ) = None

    english_validation: (
        EnglishValidationView
        | None
    ) = None

    rag_used: bool = False

    rag_sources: list[
        RAGSourceView
    ] = Field(
        default_factory=list
    )

    reply: str

    provider: str

    model: str

    latency_ms: float