
from datetime import datetime, timezone
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    Integer,
    JSON,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


def utc_now():
    return datetime.now(timezone.utc)


class TutorChatMessage(Base):
    __tablename__ = "tutor_chat_messages"

    __table_args__ = (
        Index(
            "ix_tutor_chat_messages_session_id_id",
            "session_id",
            "id",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "learning_sessions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    student_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "student_profiles.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    role: Mapped[str] = mapped_column(
        String(12),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    response_payload: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )
