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
from app.schemas.science_assessment import (
    ScienceAssessmentProgress,
    ScienceAssessmentResult,
    ScienceAssessmentStartRequest,
    ScienceAssessmentStartResponse,
    ScienceAssessmentSubmitRequest,
)
from app.services.science_assessment_service import (
    ScienceAssessmentService,
)


router = APIRouter(
    prefix="/science/assessments",

    tags=[
        "Science Assessments",
    ],
)


@router.post(
    "/start",

    response_model=(
        ScienceAssessmentStartResponse
    ),
)
def start_science_assessment(
    data: ScienceAssessmentStartRequest,

    db: Session = Depends(
        get_db
    ),
):

    try:

        return (
            ScienceAssessmentService
            .start(
                db=db,

                data=(
                    data
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


    except ValueError as exc:

        raise HTTPException(
            status_code=400,

            detail=str(
                exc
            ),
        ) from exc


@router.post(
    "/{assessment_id}/submit",

    response_model=(
        ScienceAssessmentResult
    ),
)
def submit_science_assessment(
    assessment_id: str,

    data: ScienceAssessmentSubmitRequest,

    db: Session = Depends(
        get_db
    ),
):

    try:

        return (
            ScienceAssessmentService
            .submit(
                db=db,

                assessment_id=(
                    assessment_id
                ),

                answers=(
                    data.answers
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


    except ValueError as exc:

        raise HTTPException(
            status_code=400,

            detail=str(
                exc
            ),
        ) from exc


@router.get(
    (
        "/students/{student_id}"
        "/concepts/{concept_code}"
        "/progress"
    ),

    response_model=(
        ScienceAssessmentProgress
    ),
)
def science_assessment_progress(
    student_id: str,
    concept_code: str,

    db: Session = Depends(
        get_db
    ),
):

    return (
        ScienceAssessmentService
        .get_progress(
            db=db,

            student_id=(
                student_id
            ),

            concept_code=(
                concept_code
            ),
        )
    )