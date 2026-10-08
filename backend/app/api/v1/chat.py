from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.database.session import (
    get_db,
)
from app.schemas.chat import (
    TutorMessageRequest,
    TutorMessageResponse,
)
from app.services.tutor_chat_service import (
    TutorChatService,
)


router = APIRouter(
    prefix="/tutor",
    tags=["Tutor Chat"],
)


@router.post(
    "/sessions/{session_id}/message",
    response_model=TutorMessageResponse,
)
def send_tutor_message(
    session_id: str,
    data: TutorMessageRequest,
    db: Session = Depends(get_db),
):

    try:

        return (
            TutorChatService
            .process_message(
                db=db,
                session_id=session_id,
                student_message=(
                    data.message
                ),
            )
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:

        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc