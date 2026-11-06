
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


class SavedChatMessage(BaseModel):
    id: int
    session_id: str
    student_id: str

    role: Literal["user", "assistant"]
    content: str

    response_payload: dict[str, Any] | None = None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class SessionHistorySummary(BaseModel):
    session_id: str
    subject: str
    topic: str | None
    mode: str

    message_count: int
    last_message_preview: str
    last_message_at: datetime
