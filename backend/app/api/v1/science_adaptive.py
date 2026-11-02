from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import (
    Session,
)

from app.database.session import (
    get_db,
)
from app.schemas.science_adaptive import (
    ScienceAdaptivePlanResponse,
)
from app.services.science_adaptive_learning_service import (
    ScienceAdaptiveLearningService,
)


router = APIRouter(
    prefix="/science/adaptive",
    tags=[
        "Science Adaptive Learning",
    ],
)


@router.get(
    (
        "/students/{student_id}"
        "/concepts/{concept_code}"
        "/plan"
    ),

    response_model=(
        ScienceAdaptivePlanResponse
    ),
)
def get_science_adaptive_plan(
    student_id: str,
    concept_code: str,
    db: Session = Depends(
        get_db
    ),
):

    try:

        return (
            ScienceAdaptiveLearningService
            .get_plan(
                db=db,

                student_id=(
                    student_id
                ),

                concept_code=(
                    concept_code
                ),
            )
        )


    except LookupError as exc:

        raise HTTPException(
            status_code=404,

            detail=str(
                exc
            ),
        ) from exc