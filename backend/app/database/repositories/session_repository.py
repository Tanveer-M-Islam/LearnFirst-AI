from sqlalchemy.orm import Session

from app.database.models.learning_session import (
    LearningSession,
)


class LearningSessionRepository:

    @staticmethod
    def create(
        db: Session,
        learning_session: LearningSession,
    ) -> LearningSession:

        db.add(
            learning_session
        )

        db.commit()

        db.refresh(
            learning_session
        )

        return learning_session

    @staticmethod
    def get_by_id(
        db: Session,
        session_id: str,
    ) -> LearningSession | None:

        return (
            db.query(
                LearningSession
            )
            .filter(
                LearningSession.id
                == session_id
            )
            .first()
        )

    @staticmethod
    def list_by_student(
        db: Session,
        student_id: str,
    ) -> list[LearningSession]:

        return (
            db.query(
                LearningSession
            )
            .filter(
                LearningSession.student_id
                == student_id
            )
            .order_by(
                LearningSession.started_at
            )
            .all()
        )

    @staticmethod
    def save(
        db: Session,
        learning_session: LearningSession,
    ) -> LearningSession:

        db.add(
            learning_session
        )

        db.commit()

        db.refresh(
            learning_session
        )

        return learning_session