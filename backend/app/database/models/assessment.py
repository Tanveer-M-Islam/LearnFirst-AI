import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import Base


def utc_now() -> datetime:
    return datetime.now(
        timezone.utc
    )


class AssessmentRun(Base):

    __tablename__ = "assessment_runs"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(
            uuid.uuid4()
        ),
    )

    student_id: Mapped[str] = (
        mapped_column(
            String(36),
            ForeignKey(
                "student_profiles.id",
                ondelete="CASCADE",
            ),
            nullable=False,
            index=True,
        )
    )

    session_id: Mapped[
        str | None
    ] = mapped_column(
        String(36),
        ForeignKey(
            "learning_sessions.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    subject: Mapped[str] = (
        mapped_column(
            String(30),
            nullable=False,
        )
    )

    concept_code: Mapped[str] = (
        mapped_column(
            String(100),
            nullable=False,
            index=True,
        )
    )

    assessment_type: Mapped[str] = (
        mapped_column(
            String(30),
            nullable=False,
        )
    )

    status: Mapped[str] = (
        mapped_column(
            String(30),
            nullable=False,
            default="IN_PROGRESS",
        )
    )

    total_questions: Mapped[int] = (
        mapped_column(
            Integer,
            nullable=False,
        )
    )

    correct_answers: Mapped[int] = (
        mapped_column(
            Integer,
            nullable=False,
            default=0,
        )
    )

    score_percent: Mapped[
        float | None
    ] = mapped_column(
        Float,
        nullable=True,
    )

    difficulty_recommendation: Mapped[
        str | None
    ] = mapped_column(
        String(30),
        nullable=True,
    )

    started_at: Mapped[datetime] = (
        mapped_column(
            DateTime(timezone=True),
            nullable=False,
            default=utc_now,
        )
    )

    completed_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


class AssessmentAnswer(Base):

    __tablename__ = (
        "assessment_answers"
    )

    __table_args__ = (
        UniqueConstraint(
            "assessment_id",
            "question_id",
            name=(
                "uq_assessment_question"
            ),
        ),
    )

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(
            uuid.uuid4()
        ),
    )

    assessment_id: Mapped[str] = (
        mapped_column(
            String(36),
            ForeignKey(
                "assessment_runs.id",
                ondelete="CASCADE",
            ),
            nullable=False,
            index=True,
        )
    )

    question_id: Mapped[str] = (
        mapped_column(
            String(100),
            nullable=False,
        )
    )

    problem_text: Mapped[str] = (
        mapped_column(
            Text,
            nullable=False,
        )
    )

    response_text: Mapped[str] = (
        mapped_column(
            Text,
            nullable=False,
        )
    )

    status: Mapped[str] = (
        mapped_column(
            String(30),
            nullable=False,
        )
    )

    is_correct: Mapped[bool] = (
        mapped_column(
            Boolean,
            nullable=False,
        )
    )

    expected_answer: Mapped[
        str | None
    ] = mapped_column(
        String(100),
        nullable=True,
    )

    misconception_code: Mapped[
        str | None
    ] = mapped_column(
        String(100),
        nullable=True,
    )

    validator_result: Mapped[
        dict | None
    ] = mapped_column(
        JSON,
        nullable=True,
    )

    created_at: Mapped[datetime] = (
        mapped_column(
            DateTime(timezone=True),
            nullable=False,
            default=utc_now,
        )
    )