
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.schemas.chat_history import (
    SavedChatMessage,
    SessionHistorySummary,
)

from app.services.chat_history_service import (
    ChatHistoryService,
)


router = APIRouter(
    prefix="/history",
    tags=["Tutor History"],
)


@router.get(
    "/students/{student_id}/sessions",
    response_model=list[SessionHistorySummary],
)
def list_student_sessions(
    student_id: str,
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    try:
        return ChatHistoryService.list_student_sessions(
            db=db,
            student_id=student_id,
            limit=limit,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.get(
    "/sessions/{session_id}/messages",
    response_model=list[SavedChatMessage],
)
def get_session_messages(
    session_id: str,
    student_id: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    try:
        return ChatHistoryService.list_session_messages(
            db=db,
            session_id=session_id,
            student_id=student_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
    except PermissionError as exc:
        raise HTTPException(
            status_code=403,
            detail=str(exc),
        ) from exc
