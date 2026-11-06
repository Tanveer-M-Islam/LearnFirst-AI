
"""Add persistent tutor chat history.

Revision ID: e20261106a1
Revises: d127c6c74125
"""

from alembic import op
import sqlalchemy as sa


revision = "e20261106a1"
down_revision = "d127c6c74125"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tutor_chat_messages",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            autoincrement=True,
        ),

        sa.Column(
            "session_id",
            sa.String(36),
            sa.ForeignKey(
                "learning_sessions.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),

        sa.Column(
            "student_id",
            sa.String(36),
            sa.ForeignKey(
                "student_profiles.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),

        sa.Column(
            "role",
            sa.String(12),
            nullable=False,
        ),

        sa.Column(
            "content",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "response_payload",
            sa.JSON(),
            nullable=True,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
    )

    op.create_index(
        "ix_tutor_chat_messages_student_id",
        "tutor_chat_messages",
        ["student_id"],
    )

    op.create_index(
        "ix_tutor_chat_messages_session_id_id",
        "tutor_chat_messages",
        ["session_id", "id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_tutor_chat_messages_session_id_id",
        table_name="tutor_chat_messages",
    )

    op.drop_index(
        "ix_tutor_chat_messages_student_id",
        table_name="tutor_chat_messages",
    )

    op.drop_table("tutor_chat_messages")
