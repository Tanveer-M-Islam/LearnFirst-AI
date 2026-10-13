from sqlalchemy.orm import Session

from app.database.models.attempt import (
    StudentAttempt,
)


class StudentAttemptRepository:

    @staticmethod
    def create(
        db: Session,
        attempt: StudentAttempt,
    ) -> StudentAttempt:

        db.add(
            attempt
        )

        db.commit()

        db.refresh(
            attempt
        )

        return attempt

    @staticmethod
    def list_by_session(
        db: Session,
        session_id: str,
    ) -> list[StudentAttempt]:

        return (
            db.query(
                StudentAttempt
            )
            .filter(
                StudentAttempt.session_id
                == session_id
            )
            .order_by(
                StudentAttempt
                .attempt_number
            )
            .all()
        )