from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.database.session import (
    get_db,
)
from app.schemas.assessment import (
    AssessmentResult,
    AssessmentStartRequest,
    AssessmentStartResponse,
    AssessmentSubmitRequest,
    ConceptProgressResponse,
)
from app.services.assessment_service import (
    AssessmentService,
)


router = APIRouter(
    prefix="/assessments",
    tags=["Assessments"],
)


@router.post(
    "/start",
    response_model=(
        AssessmentStartResponse
    ),
    status_code=(
        status.HTTP_201_CREATED
    ),
)
def start_assessment(
    data: AssessmentStartRequest,
    db: Session = Depends(get_db),
):

    try:

        return (
            AssessmentService
            .start_assessment(
                db=db,
                data=data,
            )
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
def submit_assessment(
    assessment_id: str,
    data: AssessmentSubmitRequest,
    db: Session = Depends(get_db),
):

    try:

        return (
            AssessmentService
            .submit_assessment(
                db=db,
                assessment_id=(
                    assessment_id
                ),
                answers=data.answers,
            )
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


@router.get(
    (
        "/students/{student_id}"
        "/concepts/{concept_code}"
        "/progress"
    ),
    response_model=(
        ConceptProgressResponse
    ),
)
def get_concept_progress(
    student_id: str,
    concept_code: str,
    db: Session = Depends(get_db),
):

    try:

        return (
            AssessmentService
            .get_concept_progress(
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
            detail=str(exc),
        ) from exc