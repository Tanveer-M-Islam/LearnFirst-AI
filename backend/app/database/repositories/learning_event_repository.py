from sqlalchemy.orm import (
    Session,
)

from app.database.models.learning_event import (
    LearningEvent,
)
from app.schemas.telemetry import (
    LearningEventType,
)


class LearningEventRepository:

    @staticmethod
    def create(
        db: Session,
        event: LearningEvent,
    ) -> LearningEvent:

        db.add(
            event
        )

        db.commit()

        db.refresh(
            event
        )

        return event


    @staticmethod
    def save(
        db: Session,
        event: LearningEvent,
    ) -> LearningEvent:

        db.add(
            event
        )

        db.commit()

        db.refresh(
            event
        )

        return event


    @staticmethod
    def get_by_id(
        db: Session,
        event_id: str,
    ) -> LearningEvent | None:

        return (
            db.query(
                LearningEvent
            )
            .filter(
                LearningEvent.id
                == event_id
            )
            .first()
        )


    @staticmethod
    def latest_tutor_response(
        db: Session,
        session_id: str,
    ) -> LearningEvent | None:

        return (
            db.query(
                LearningEvent
            )
            .filter(
                LearningEvent
                .session_id
                == session_id,

                LearningEvent
                .event_type
                == (
                    LearningEventType
                    .TUTOR_RESPONSE
                    .value
                ),
            )
            .order_by(
                LearningEvent
                .created_at
                .desc()
            )
            .first()
        )


    @staticmethod
    def list_by_student_concept(
        db: Session,
        student_id: str,
        concept_code: str,
    ) -> list[
        LearningEvent
    ]:

        return (
            db.query(
                LearningEvent
            )
            .filter(
                LearningEvent
                .student_id
                == student_id,

                LearningEvent
                .concept_code
                == concept_code,
            )
            .order_by(
                LearningEvent
                .created_at
            )
            .all()
        )