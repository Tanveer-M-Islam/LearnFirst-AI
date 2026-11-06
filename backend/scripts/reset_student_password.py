import sys
from pathlib import Path


# ============================================================
# Add backend folder to Python path
# ============================================================

BACKEND_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

sys.path.insert(
    0,
    str(BACKEND_DIR),
)


# ============================================================
# App imports
# ============================================================

from app.database.session import (  # noqa: E402
    SessionLocal,
)

from app.database.models.student import (  # noqa: E402
    StudentProfile,
)

from app.services.student_service import (  # noqa: E402
    hash_password,
)


# ============================================================
# Credentials to reset
# ============================================================

USERNAME = "tanveer"

NEW_PASSWORD = "test123"


# ============================================================
# Reset password
# ============================================================


def main():

    db = SessionLocal()


    try:

        username = (
            USERNAME
            .strip()
            .lower()
        )


        student = (
            db.query(
                StudentProfile
            )
            .filter(
                StudentProfile.username
                == username
            )
            .first()
        )


        if (
            student is None
        ):

            print(
                "No student found "
                f"with username: {username}"
            )

            return


        print()
        print(
            "Student found"
        )

        print(
            "-------------"
        )

        print(
            f"ID: {student.id}"
        )

        print(
            f"Name: {student.display_name}"
        )

        print(
            f"Username: {student.username}"
        )


        if (
            student.password_hash
        ):

            print(
                "Old password hash: present"
            )

        else:

            print(
                "Old password hash: NULL"
            )


        student.password_hash = (
            hash_password(
                NEW_PASSWORD
            )
        )


        db.commit()

        db.refresh(
            student
        )


        print()
        print(
            "Password successfully reset."
        )

        print(
            f"Username: {username}"
        )

        print(
            f"New password: {NEW_PASSWORD}"
        )


    except Exception as exc:

        db.rollback()

        print()
        print(
            "Password reset failed:"
        )

        print(
            str(exc)
        )


    finally:

        db.close()


if __name__ == "__main__":
    main()