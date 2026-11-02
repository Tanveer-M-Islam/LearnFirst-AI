from datetime import (
    datetime,
    timezone,
)
from uuid import uuid4

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import (
    Base,
)


def utc_now():
    return datetime.now(
        timezone.utc
    )


class LearningEvent(Base):
    __tablename__ = (
        "learning_events"
    )

    id: Mapped[str] = (
        mapped_column(
            String(36),

            primary_key=True,

            default=lambda:
                str(
                    uuid4()
                ),
        )
    )

    session_id: Mapped[str] = (
        mapped_column(
            String(36),

            ForeignKey(
                "learning_sessions.id",
                ondelete="CASCADE",
            ),

            nullable=False,

            index=True,
        )
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

    subject: Mapped[str] = (
        mapped_column(
            String(30),

            nullable=False,

            index=True,
        )
    )

    concept_code: Mapped[
        str | None
    ] = mapped_column(
        String(100),

        nullable=True,

        index=True,
    )

    event_type: Mapped[str] = (
        mapped_column(
            String(40),

            nullable=False,

            index=True,
        )
    )

    response_latency_ms: Mapped[
        int | None
    ] = mapped_column(
        Integer,

        nullable=True,
    )

    tutor_latency_ms: Mapped[
        float | None
    ] = mapped_column(
        Float,

        nullable=True,
    )

    detected_intent: Mapped[
        str | None
    ] = mapped_column(
        String(50),

        nullable=True,
    )

    selected_action: Mapped[
        str | None
    ] = mapped_column(
        String(80),

        nullable=True,
    )

    hint_level: Mapped[
        int | None
    ] = mapped_column(
        Integer,

        nullable=True,
    )

    event_metadata: Mapped[
        dict | None
    ] = mapped_column(
        JSON,

        nullable=True,
    )

    created_at: Mapped[
        datetime
    ] = mapped_column(
        DateTime(
            timezone=True
        ),

        default=utc_now,

        nullable=False,

        index=True,
    )