from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


def utc_now():
    return datetime.now(timezone.utc)


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4()),
    )

    parent_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey(
            "parent_accounts.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    display_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    grade: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    age_group: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    preferred_language: Mapped[str] = mapped_column(
        String(10),
        default="en",
        nullable=False,
    )

    curriculum_profile: Mapped[str] = mapped_column(
        String(100),
        default="bangladesh_english_v1",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
        nullable=False,
    )

    parent = relationship(
        "ParentAccount",
        back_populates="students",
    )

    learning_sessions = relationship(
        "LearningSession",
        back_populates="student",
        cascade="all, delete-orphan",
    )