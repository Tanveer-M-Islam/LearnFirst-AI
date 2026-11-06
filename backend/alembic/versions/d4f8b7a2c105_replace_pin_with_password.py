"""replace pin with password

Revision ID: d4f8b7a2c105
Revises: c1d7e8f4a620
"""

from typing import (
    Sequence,
    Union,
)

from alembic import op
import sqlalchemy as sa


revision: str = (
    "d4f8b7a2c105"
)

down_revision: Union[
    str,
    Sequence[str],
    None,
] = "c1d7e8f4a620"

branch_labels = None

depends_on = None


TABLE_NAME = (
    "student_profiles"
)


OLD_INDEX = (
    "ix_student_profiles_login_name"
)


NEW_INDEX = (
    "ix_student_profiles_username"
)


def _column_names() -> set[str]:

    bind = (
        op.get_bind()
    )


    inspector = (
        sa.inspect(
            bind
        )
    )


    return {
        column[
            "name"
        ]

        for column
        in inspector.get_columns(
            TABLE_NAME
        )
    }


def _index_names() -> set[str]:

    bind = (
        op.get_bind()
    )


    inspector = (
        sa.inspect(
            bind
        )
    )


    return {
        index[
            "name"
        ]

        for index
        in inspector.get_indexes(
            TABLE_NAME
        )

        if index.get(
            "name"
        )
    }


def upgrade() -> None:

    bind = (
        op.get_bind()
    )


    dialect = (
        bind.dialect.name
    )


    # ==================================
    # Clean up possible temporary table
    # left by the failed batch migration.
    # ==================================

    if (
        dialect
        == "sqlite"
    ):

        op.execute(
            (
                "DROP TABLE IF EXISTS "
                "_alembic_tmp_student_profiles"
            )
        )


    columns = (
        _column_names()
    )


    # ==================================
    # login_name -> username
    # ==================================

    if (
        "login_name"
        in columns

        and "username"
        not in columns
    ):

        if (
            dialect
            == "sqlite"
        ):

            op.execute(
                (
                    "ALTER TABLE "
                    "student_profiles "
                    "RENAME COLUMN "
                    "login_name "
                    "TO username"
                )
            )


        else:

            op.alter_column(
                TABLE_NAME,

                "login_name",

                new_column_name=(
                    "username"
                ),

                existing_type=(
                    sa.String(
                        length=30
                    )
                ),
            )


    # Refresh reflected column names.

    columns = (
        _column_names()
    )


    # ==================================
    # pin_salt -> password_salt
    # ==================================

    if (
        "pin_salt"
        in columns

        and "password_salt"
        not in columns
    ):

        if (
            dialect
            == "sqlite"
        ):

            op.execute(
                (
                    "ALTER TABLE "
                    "student_profiles "
                    "RENAME COLUMN "
                    "pin_salt "
                    "TO password_salt"
                )
            )


        else:

            op.alter_column(
                TABLE_NAME,

                "pin_salt",

                new_column_name=(
                    "password_salt"
                ),

                existing_type=(
                    sa.String(
                        length=64
                    )
                ),
            )


    columns = (
        _column_names()
    )


    # ==================================
    # pin_hash -> password_hash
    # ==================================

    if (
        "pin_hash"
        in columns

        and "password_hash"
        not in columns
    ):

        if (
            dialect
            == "sqlite"
        ):

            op.execute(
                (
                    "ALTER TABLE "
                    "student_profiles "
                    "RENAME COLUMN "
                    "pin_hash "
                    "TO password_hash"
                )
            )


        else:

            op.alter_column(
                TABLE_NAME,

                "pin_hash",

                new_column_name=(
                    "password_hash"
                ),

                existing_type=(
                    sa.String(
                        length=128
                    )
                ),
            )


    # ==================================
    # Rebuild username index cleanly
    # ==================================

    indexes = (
        _index_names()
    )


    if (
        OLD_INDEX
        in indexes
    ):

        op.drop_index(
            OLD_INDEX,

            table_name=(
                TABLE_NAME
            ),
        )


    indexes = (
        _index_names()
    )


    if (
        NEW_INDEX
        not in indexes
    ):

        op.create_index(
            NEW_INDEX,

            TABLE_NAME,

            [
                "username"
            ],

            unique=True,
        )


def downgrade() -> None:

    bind = (
        op.get_bind()
    )


    dialect = (
        bind.dialect.name
    )


    indexes = (
        _index_names()
    )


    # ==================================
    # Remove username index
    # ==================================

    if (
        NEW_INDEX
        in indexes
    ):

        op.drop_index(
            NEW_INDEX,

            table_name=(
                TABLE_NAME
            ),
        )


    columns = (
        _column_names()
    )


    # ==================================
    # username -> login_name
    # ==================================

    if (
        "username"
        in columns

        and "login_name"
        not in columns
    ):

        if (
            dialect
            == "sqlite"
        ):

            op.execute(
                (
                    "ALTER TABLE "
                    "student_profiles "
                    "RENAME COLUMN "
                    "username "
                    "TO login_name"
                )
            )


        else:

            op.alter_column(
                TABLE_NAME,

                "username",

                new_column_name=(
                    "login_name"
                ),

                existing_type=(
                    sa.String(
                        length=30
                    )
                ),
            )


    columns = (
        _column_names()
    )


    # ==================================
    # password_salt -> pin_salt
    # ==================================

    if (
        "password_salt"
        in columns

        and "pin_salt"
        not in columns
    ):

        if (
            dialect
            == "sqlite"
        ):

            op.execute(
                (
                    "ALTER TABLE "
                    "student_profiles "
                    "RENAME COLUMN "
                    "password_salt "
                    "TO pin_salt"
                )
            )


        else:

            op.alter_column(
                TABLE_NAME,

                "password_salt",

                new_column_name=(
                    "pin_salt"
                ),

                existing_type=(
                    sa.String(
                        length=64
                    )
                ),
            )


    columns = (
        _column_names()
    )


    # ==================================
    # password_hash -> pin_hash
    # ==================================

    if (
        "password_hash"
        in columns

        and "pin_hash"
        not in columns
    ):

        if (
            dialect
            == "sqlite"
        ):

            op.execute(
                (
                    "ALTER TABLE "
                    "student_profiles "
                    "RENAME COLUMN "
                    "password_hash "
                    "TO pin_hash"
                )
            )


        else:

            op.alter_column(
                TABLE_NAME,

                "password_hash",

                new_column_name=(
                    "pin_hash"
                ),

                existing_type=(
                    sa.String(
                        length=128
                    )
                ),
            )


    # ==================================
    # Restore old index
    # ==================================

    indexes = (
        _index_names()
    )


    if (
        OLD_INDEX
        not in indexes
    ):

        op.create_index(
            OLD_INDEX,

            TABLE_NAME,

            [
                "login_name"
            ],

            unique=True,
        )