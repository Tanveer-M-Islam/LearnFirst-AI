from sqlalchemy.orm import (
    Session,
)

from app.database.models.student import (
    StudentProfile,
)


class StudentRepository:

    @staticmethod
    def create(
        db: Session,
        student: StudentProfile,
    ) -> StudentProfile:

        db.add(
            student
        )

        db.commit()

        db.refresh(
            student
        )

        return student


    @staticmethod
    def save(
        db: Session,
        student: StudentProfile,
    ) -> StudentProfile:

        db.add(
            student
        )

        db.commit()

        db.refresh(
            student
        )

        return student


    @staticmethod
    def get_by_id(
        db: Session,
        student_id: str,
    ) -> StudentProfile | None:

        return (
            db.query(
                StudentProfile
            )
            .filter(
                StudentProfile.id
                == student_id
            )
            .first()
        )


    @staticmethod
    def get_by_username(
        db: Session,
        username: str,
    ) -> StudentProfile | None:

        normalized_username = (
            username
            .strip()
            .lower()
        )


        return (
            db.query(
                StudentProfile
            )
            .filter(
                StudentProfile.username
                == normalized_username
            )
            .first()
        )