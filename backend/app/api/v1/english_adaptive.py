from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.database.session import (
    get_db,
)
from app.schemas.english_adaptive import (
    EnglishAdaptivePlanResponse,
)
from app.services.english_adaptive_learning_service import (
    EnglishAdaptiveLearningService,
)


router = APIRouter(
    prefix="/english/adaptive",

    tags=[
        "English Adaptive Learning",
    ],
)


@router.get(
    (
        "/students/{student_id}"
        "/concepts/{concept_code}"
        "/plan"
    ),

    response_model=(
        EnglishAdaptivePlanResponse
    ),
)
def get_english_adaptive_plan(
    student_id: str,
    concept_code: str,
    db: Session = Depends(
        get_db
    ),
):

    try:
        return (
            EnglishAdaptiveLearningService
            .get_plan(
                db=db,
                student_id=student_id,
                concept_code=concept_code,
            )
        )


    except LookupError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(
                exc
            ),
        ) from exc