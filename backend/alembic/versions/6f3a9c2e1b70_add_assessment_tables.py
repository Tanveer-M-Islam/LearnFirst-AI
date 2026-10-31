"""add assessment tables

Revision ID: 6f3a9c2e1b70
Revises: 49daaae7a91d
"""

from typing import (
    Sequence,
    Union,
)

from alembic import op
import sqlalchemy as sa


revision: str = (
    "6f3a9c2e1b70"
)

down_revision: Union[
    str,
    Sequence[str],
    None,
] = "49daaae7a91d"

branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "assessment_runs",

        sa.Column(
            "id",
            sa.String(length=36),
            nullable=False,
        ),

        sa.Column(
            "student_id",
            sa.String(length=36),
            nullable=False,
        ),

        sa.Column(
            "session_id",
            sa.String(length=36),
            nullable=True,
        ),

        sa.Column(
            "subject",
            sa.String(length=30),
            nullable=False,
        ),

        sa.Column(
            "concept_code",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "assessment_type",
            sa.String(length=30),
            nullable=False,
        ),

        sa.Column(
            "status",
            sa.String(length=30),
            nullable=False,
        ),

        sa.Column(
            "total_questions",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "correct_answers",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "score_percent",
            sa.Float(),
            nullable=True,
        ),

        sa.Column(
            "difficulty_recommendation",
            sa.String(length=30),
            nullable=True,
        ),

        sa.Column(
            "started_at",
            sa.DateTime(
                timezone=True
            ),
            nullable=False,
        ),

        sa.Column(
            "completed_at",
            sa.DateTime(
                timezone=True
            ),
            nullable=True,
        ),

        sa.ForeignKeyConstraint(
            ["student_id"],
            ["student_profiles.id"],
            ondelete="CASCADE",
        ),

        sa.ForeignKeyConstraint(
            ["session_id"],
            ["learning_sessions.id"],
            ondelete="SET NULL",
        ),

        sa.PrimaryKeyConstraint(
            "id"
        ),
    )

    op.create_index(
        "ix_assessment_runs_student_id",
        "assessment_runs",
        ["student_id"],
        unique=False,
    )

    op.create_index(
        "ix_assessment_runs_session_id",
        "assessment_runs",
        ["session_id"],
        unique=False,
    )

    op.create_index(
        "ix_assessment_runs_concept_code",
        "assessment_runs",
        ["concept_code"],
        unique=False,
    )

    op.create_table(
        "assessment_answers",

        sa.Column(
            "id",
            sa.String(length=36),
            nullable=False,
        ),

        sa.Column(
            "assessment_id",
            sa.String(length=36),
            nullable=False,
        ),

        sa.Column(
            "question_id",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "problem_text",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "response_text",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "status",
            sa.String(length=30),
            nullable=False,
        ),

        sa.Column(
            "is_correct",
            sa.Boolean(),
            nullable=False,
        ),

        sa.Column(
            "expected_answer",
            sa.String(length=100),
            nullable=True,
        ),

        sa.Column(
            "misconception_code",
            sa.String(length=100),
            nullable=True,
        ),

        sa.Column(
            "validator_result",
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
            ["assessment_id"],
            ["assessment_runs.id"],
            ondelete="CASCADE",
        ),

        sa.PrimaryKeyConstraint(
            "id"
        ),

        sa.UniqueConstraint(
            "assessment_id",
            "question_id",
            name=(
                "uq_assessment_question"
            ),
        ),
    )

    op.create_index(
        "ix_assessment_answers_assessment_id",
        "assessment_answers",
        ["assessment_id"],
        unique=False,
    )


def downgrade() -> None:

    op.drop_index(
        "ix_assessment_answers_assessment_id",
        table_name=(
            "assessment_answers"
        ),
    )

    op.drop_table(
        "assessment_answers"
    )

    op.drop_index(
        "ix_assessment_runs_concept_code",
        table_name="assessment_runs",
    )

    op.drop_index(
        "ix_assessment_runs_session_id",
        table_name="assessment_runs",
    )

    op.drop_index(
        "ix_assessment_runs_student_id",
        table_name="assessment_runs",
    )

    op.drop_table(
        "assessment_runs"
    )