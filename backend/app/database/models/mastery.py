from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


def utc_now():
    return datetime.now(timezone.utc)


class MasteryRecord(Base):
    __tablename__ = "mastery_records"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "concept_code",
            name="uq_student_concept_mastery",
        ),
    )

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

    subject: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    concept_code: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    mastery_state: Mapped[str] = mapped_column(
        String(30),
        default="NOT_STARTED",
        nullable=False,
    )

    mastery_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    independent_successes: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    assisted_successes: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    failed_attempts: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    follow_up_successes: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    explain_back_successes: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    last_practiced_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )