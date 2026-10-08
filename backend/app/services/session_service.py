from sqlalchemy.orm import Session

from app.database.models.learning_session import (
    LearningSession,
)
from app.database.repositories.session_repository import (
    LearningSessionRepository,
)
from app.database.repositories.student_repository import (
    StudentRepository,
)
from app.schemas.enums import (
    MasteryState,
    SessionStatus,
)
from app.schemas.session import (
    LearningSessionCreate,
)


class LearningSessionService:

    @staticmethod
    def create_session(
        db: Session,
        data: LearningSessionCreate,
    ) -> LearningSession:

        student = StudentRepository.get_by_id(
            db=db,
            student_id=data.student_id,
        )

        if student is None:
            raise ValueError(
                "Student not found."
            )

        learning_session = LearningSession(
            student_id=data.student_id,
            mode=data.mode.value,
            subject=data.subject.value,
            topic=data.topic,
            concept_code=data.concept_code,
            current_problem=(
                data.current_problem
            ),
            current_hint_level=0,
            attempt_count=0,
            direct_answer_requests=0,
            mastery_state=(
                MasteryState.LEARNING.value
            ),
            status=SessionStatus.ACTIVE.value,
        )

        return (
            LearningSessionRepository.create(
                db=db,
                learning_session=(
                    learning_session
                ),
            )
        )

    @staticmethod
    def get_session(
        db: Session,
        session_id: str,
    ) -> LearningSession | None:

        return (
            LearningSessionRepository.get_by_id(
                db=db,
                session_id=session_id,
            )
        )