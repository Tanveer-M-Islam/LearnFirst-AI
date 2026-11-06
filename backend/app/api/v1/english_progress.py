from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.database.session import (
    get_db,
)
from app.schemas.english_progress import (
    EnglishProgressResponse,
)
from app.services.english_progress_service import (
    EnglishProgressService,
)


router = APIRouter(
    prefix="/english/progress",
    tags=[
        "English Progress",
    ],
)


@router.get(
    "/students/{student_id}/concepts/{concept_code}",
    response_model=EnglishProgressResponse,
)
def get_english_progress(
    student_id: str,
    concept_code: str,
    db: Session = Depends(
        get_db
    ),
):

    try:

        return (
            EnglishProgressService
            .get_progress(
                db=db,
                student_id=student_id,
                concept_code=concept_code,
            )
        )

    except LookupError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc