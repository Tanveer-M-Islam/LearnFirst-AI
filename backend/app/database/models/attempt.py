from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


def utc_now():
    return datetime.now(timezone.utc)


class StudentAttempt(Base):
    __tablename__ = "student_attempts"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    session_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey(
            "learning_sessions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
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

    problem_ref: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    response_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    attempt_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    is_independent: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    hint_level_before: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    misconception_code: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    validator_result: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )