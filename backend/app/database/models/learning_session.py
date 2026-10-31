from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


def utc_now():
    return datetime.now(timezone.utc)


class LearningSession(Base):
    __tablename__ = "learning_sessions"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
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

    mode: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    subject: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    topic: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    concept_code: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    current_problem: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    current_hint_level: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    attempt_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    direct_answer_requests: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    current_misconception: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    mastery_state: Mapped[str] = mapped_column(
        String(30),
        default="LEARNING",
        nullable=False,
    )

    last_tutor_action: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="ACTIVE",
        nullable=False,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    student = relationship(
        "StudentProfile",
        back_populates="learning_sessions",
    )