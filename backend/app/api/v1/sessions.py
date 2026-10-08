from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.session import (
    LearningSessionCreate,
    LearningSessionRead,
)
from app.services.session_service import (
    LearningSessionService,
)


router = APIRouter(
    prefix="/sessions",
    tags=["Learning Sessions"],
)


@router.post(
    "",
    response_model=LearningSessionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_session(
    data: LearningSessionCreate,
    db: Session = Depends(get_db),
):
    try:
        return (
            LearningSessionService
            .create_session(
                db=db,
                data=data,
            )
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.get(
    "/{session_id}",
    response_model=LearningSessionRead,
)
def get_session(
    session_id: str,
    db: Session = Depends(get_db),
):
    learning_session = (
        LearningSessionService
        .get_session(
            db=db,
            session_id=session_id,
        )
    )

    if learning_session is None:
        raise HTTPException(
            status_code=404,
            detail="Learning session not found.",
        )

    return learning_session