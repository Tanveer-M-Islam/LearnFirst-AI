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