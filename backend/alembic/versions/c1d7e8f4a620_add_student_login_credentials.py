"""add student login credentials

Revision ID: c1d7e8f4a620
Revises: a8c4d2f19e31
"""

from typing import (
    Sequence,
    Union,
)

from alembic import op
import sqlalchemy as sa


revision: str = (
    "c1d7e8f4a620"
)

down_revision: Union[
    str,
    Sequence[str],
    None,
] = "a8c4d2f19e31"

branch_labels = None

depends_on = None


def upgrade() -> None:

    op.add_column(
        "student_profiles",

        sa.Column(
            "login_name",
            sa.String(
                length=30
            ),
            nullable=True,
        ),
    )


    op.add_column(
        "student_profiles",

        sa.Column(
            "pin_salt",
            sa.String(
                length=64
            ),
            nullable=True,
        ),
    )


    op.add_column(
        "student_profiles",

        sa.Column(
            "pin_hash",
            sa.String(
                length=128
            ),
            nullable=True,
        ),
    )


    op.create_index(
        "ix_student_profiles_login_name",

        "student_profiles",

        [
            "login_name"
        ],

        unique=True,
    )


def downgrade() -> None:

    op.drop_index(
        "ix_student_profiles_login_name",

        table_name=(
            "student_profiles"
        ),
    )


    op.drop_column(
        "student_profiles",
        "pin_hash",
    )


    op.drop_column(
        "student_profiles",
        "pin_salt",
    )


    op.drop_column(
        "student_profiles",
        "login_name",
    )