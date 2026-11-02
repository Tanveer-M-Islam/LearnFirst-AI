"""add learning telemetry

Revision ID: a8c4d2f19e31
Revises: 6f3a9c2e1b70
"""

from typing import (
    Sequence,
    Union,
)

from alembic import op
import sqlalchemy as sa


revision: str = (
    "a8c4d2f19e31"
)

down_revision: Union[
    str,
    Sequence[str],
    None,
] = "6f3a9c2e1b70"

branch_labels = None

depends_on = None


def upgrade() -> None:

    op.create_table(
        "learning_events",

        sa.Column(
            "id",
            sa.String(
                length=36
            ),
            nullable=False,
        ),

        sa.Column(
            "session_id",
            sa.String(
                length=36
            ),
            nullable=False,
        ),

        sa.Column(
            "student_id",
            sa.String(
                length=36
            ),
            nullable=False,
        ),

        sa.Column(
            "subject",
            sa.String(
                length=30
            ),
            nullable=False,
        ),

        sa.Column(
            "concept_code",
            sa.String(
                length=100
            ),
            nullable=True,
        ),

        sa.Column(
            "event_type",
            sa.String(
                length=40
            ),
            nullable=False,
        ),

        sa.Column(
            "response_latency_ms",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "tutor_latency_ms",
            sa.Float(),
            nullable=True,
        ),

        sa.Column(
            "detected_intent",
            sa.String(
                length=50
            ),
            nullable=True,
        ),

        sa.Column(
            "selected_action",
            sa.String(
                length=80
            ),
            nullable=True,
        ),

        sa.Column(
            "hint_level",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "event_metadata",
            sa.JSON(),
            nullable=True,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(
                timezone=True
            ),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            [
                "session_id"
            ],
            [
                "learning_sessions.id"
            ],
            ondelete="CASCADE",
        ),

        sa.ForeignKeyConstraint(
            [
                "student_id"
            ],
            [
                "student_profiles.id"
            ],
            ondelete="CASCADE",
        ),

        sa.PrimaryKeyConstraint(
            "id"
        ),
    )


    op.create_index(
        "ix_learning_events_session_id",
        "learning_events",
        [
            "session_id"
        ],
        unique=False,
    )


    op.create_index(
        "ix_learning_events_student_id",
        "learning_events",
        [
            "student_id"
        ],
        unique=False,
    )


    op.create_index(
        "ix_learning_events_subject",
        "learning_events",
        [
            "subject"
        ],
        unique=False,
    )


    op.create_index(
        "ix_learning_events_concept_code",
        "learning_events",
        [
            "concept_code"
        ],
        unique=False,
    )


    op.create_index(
        "ix_learning_events_event_type",
        "learning_events",
        [
            "event_type"
        ],
        unique=False,
    )


    op.create_index(
        "ix_learning_events_created_at",
        "learning_events",
        [
            "created_at"
        ],
        unique=False,
    )


def downgrade() -> None:

    op.drop_index(
        "ix_learning_events_created_at",
        table_name=(
            "learning_events"
        ),
    )

    op.drop_index(
        "ix_learning_events_event_type",
        table_name=(
            "learning_events"
        ),
    )

    op.drop_index(
        "ix_learning_events_concept_code",
        table_name=(
            "learning_events"
        ),
    )

    op.drop_index(
        "ix_learning_events_subject",
        table_name=(
            "learning_events"
        ),
    )

    op.drop_index(
        "ix_learning_events_student_id",
        table_name=(
            "learning_events"
        ),
    )

    op.drop_index(
        "ix_learning_events_session_id",
        table_name=(
            "learning_events"
        ),
    )

    op.drop_table(
        "learning_events"
    )