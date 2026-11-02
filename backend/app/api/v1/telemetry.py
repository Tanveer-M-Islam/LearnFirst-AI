from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import (
    Session,
)

from app.database.session import (
    get_db,
)
from app.schemas.telemetry import (
    TelemetrySummaryResponse,
)
from app.services.telemetry_service import (
    TelemetryService,
)


router = APIRouter(
    prefix="/telemetry",
    tags=[
        "Learning Telemetry"
    ],
)


@router.get(
    (
        "/students/"
        "{student_id}/"
        "concepts/"
        "{concept_code}/summary"
    ),
    response_model=(
        TelemetrySummaryResponse
    ),
)
def get_telemetry_summary(
    student_id: str,
    concept_code: str,
    db: Session = Depends(
        get_db
    ),
):

    return (
        TelemetryService
        .get_summary(
            db=db,

            student_id=(
                student_id
            ),

            concept_code=(
                concept_code
            ),
        )
    )