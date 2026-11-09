
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.assessment import (
    AssessmentResult,
    AssessmentStartRequest,
    AssessmentStartResponse,
    AssessmentSubmitRequest,
)
from app.services.english_assessment_service import (
    EnglishAssessmentService,
)


router = APIRouter(
    prefix="/english/assessments",
    tags=["English Assessments"],
)


@router.post(
    "/start",
    response_model=AssessmentStartResponse,
    status_code=status.HTTP_201_CREATED,
)
def start_english_assessment(
    data: AssessmentStartRequest,
    db: Session = Depends(get_db),
):
    try:
        return EnglishAssessmentService.start(
            db=db,
            data=data,
        )

    except LookupError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.post(
    "/{assessment_id}/submit",
    response_model=AssessmentResult,
)
def submit_english_assessment(
    assessment_id: str,
    data: AssessmentSubmitRequest,
    db: Session = Depends(get_db),
):
    try:
        return EnglishAssessmentService.submit(
            db=db,
            assessment_id=assessment_id,
            answers=data.answers,
        )

    except LookupError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
