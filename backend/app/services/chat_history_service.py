
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database.models.chat_message import TutorChatMessage
from app.database.models.learning_session import LearningSession
from app.database.models.student import StudentProfile

from app.llm.models import LLMMessage, LLMRequest
from app.schemas.chat import TutorMessageResponse
from app.schemas.chat_history import SessionHistorySummary


class ChatHistoryService:

    @staticmethod
    def get_session(
        db: Session,
        session_id: str,
    ) -> LearningSession:

        session = db.get(LearningSession, session_id)

        if session is None:
            raise ValueError("Learning session not found.")

        return session

    @classmethod
    def save_exchange(
        cls,
        db: Session,
        session_id: str,
        student_message: str,
        response: TutorMessageResponse,
    ) -> None:

        session = cls.get_session(db, session_id)

        if response.session_id != session.id:
            raise ValueError(
                "Response belongs to another session."
            )

        student_turn = TutorChatMessage(
            session_id=session.id,
            student_id=session.student_id,
            role="user",
            content=student_message,
        )

        tutor_turn = TutorChatMessage(
            session_id=session.id,
            student_id=session.student_id,
            role="assistant",
            content=response.reply,
            response_payload=response.model_dump(
                mode="json"
            ),
        )

        db.add_all([student_turn, tutor_turn])

        session.updated_at = datetime.now(timezone.utc)
        db.add(session)

        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_recent_messages(
        db: Session,
        session_id: str,
        limit: int = 12,
    ) -> list[TutorChatMessage]:

        messages = (
            db.query(TutorChatMessage)
            .filter(
                TutorChatMessage.session_id == session_id
            )
            .order_by(
                TutorChatMessage.id.desc()
            )
            .limit(limit)
            .all()
        )

        return list(reversed(messages))

    @classmethod
    def add_recent_context(
        cls,
        db: Session,
        session_id: str,
        request: LLMRequest,
        max_messages: int = 12,
    ) -> LLMRequest:

        history = cls.get_recent_messages(
            db,
            session_id,
            max_messages,
        )

        if not history or len(request.messages) < 2:
            return request

        context_messages = [
            LLMMessage(
                role=item.role,
                content=item.content,
            )
            for item in history
        ]

        # System policy first; current question last.
        return request.model_copy(
            update={
                "messages": [
                    request.messages[0],
                    *context_messages,
                    *request.messages[1:],
                ]
            }
        )

    @classmethod
    def list_session_messages(
        cls,
        db: Session,
        session_id: str,
        student_id: str,
    ) -> list[TutorChatMessage]:

        session = cls.get_session(db, session_id)

        if session.student_id != student_id:
            raise PermissionError(
                "Session belongs to another learner."
            )

        return (
            db.query(TutorChatMessage)
            .filter(
                TutorChatMessage.session_id == session_id,
                TutorChatMessage.student_id == student_id,
            )
            .order_by(TutorChatMessage.id.asc())
            .all()
        )

    @staticmethod
    def list_student_sessions(
        db: Session,
        student_id: str,
        limit: int = 50,
    ) -> list[SessionHistorySummary]:

        student = db.get(StudentProfile, student_id)

        if student is None:
            raise ValueError("Student not found.")

        sessions = (
            db.query(LearningSession)
            .join(
                TutorChatMessage,
                TutorChatMessage.session_id
                == LearningSession.id,
            )
            .filter(
                LearningSession.student_id == student_id
            )
            .distinct()
            .order_by(
                LearningSession.updated_at.desc()
            )
            .limit(limit)
            .all()
        )

        summaries = []

        for session in sessions:
            messages = (
                db.query(TutorChatMessage)
                .filter(
                    TutorChatMessage.session_id
                    == session.id
                )
                .order_by(
                    TutorChatMessage.id.desc()
                )
                .all()
            )

            if not messages:
                continue

            latest = messages[0]

            summaries.append(
                SessionHistorySummary(
                    session_id=session.id,
                    subject=session.subject,
                    topic=session.topic,
                    mode=session.mode,
                    message_count=len(messages),
                    last_message_preview=latest.content[:160],
                    last_message_at=latest.created_at,
                )
            )

        return summaries
