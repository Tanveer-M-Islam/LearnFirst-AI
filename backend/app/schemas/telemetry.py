from enum import Enum

from pydantic import (
    BaseModel,
)


class LearningEventType(
    str,
    Enum,
):
    STUDENT_MESSAGE = (
        "STUDENT_MESSAGE"
    )

    TUTOR_RESPONSE = (
        "TUTOR_RESPONSE"
    )


class TelemetrySummaryResponse(
    BaseModel
):
    student_id: str

    concept_code: str

    student_messages: int

    tutor_responses: int

    measured_student_responses: int

    average_response_latency_ms: (
        float | None
    ) = None

    median_response_latency_ms: (
        float | None
    ) = None

    average_tutor_latency_ms: (
        float | None
    ) = None

    hint_requests: int

    direct_answer_requests: int

    rag_grounded_responses: int