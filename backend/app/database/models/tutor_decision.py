from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


def utc_now():
    return datetime.now(timezone.utc)


class TutorDecision(Base):
    __tablename__ = "tutor_decisions"

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

    detected_intent: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    subject: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    attempt_status: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    selected_action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    selected_hint_level: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    allow_final_answer: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    requires_rag: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    requires_validation: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    requires_mastery_check: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    policy_bypass_detected: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    model_used: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )