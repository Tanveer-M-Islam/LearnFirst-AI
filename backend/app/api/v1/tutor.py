from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.tutor_service import (
    TutorService,
)
from app.tutor.decision_models import (
    TutorDecisionInput,
    TutorDecisionResult,
)


router = APIRouter(
    prefix="/tutor",
    tags=["Tutor Policy"],
)


@router.post(
    "/sessions/{session_id}/decision",
    response_model=TutorDecisionResult,
)
def make_tutor_decision(
    session_id: str,
    data: TutorDecisionInput,
    db: Session = Depends(get_db),
):

    try:

        return TutorService.make_decision(
            db=db,
            session_id=session_id,
            decision_input=data,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc