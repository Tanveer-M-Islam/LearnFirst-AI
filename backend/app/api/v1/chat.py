import logging

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
from app.services.telemetry_service import (
    TelemetryService,
)
from app.services.tutor_chat_service import (
    TutorChatService,
)


logger = logging.getLogger(
    __name__
)


router = APIRouter(
    prefix="/tutor",
    tags=[
        "Tutor Chat"
    ],
)


@router.post(
    "/sessions/{session_id}/message",
    response_model=(
        TutorMessageResponse
    ),
)
def send_tutor_message(
    session_id: str,
    data: TutorMessageRequest,
    db: Session = Depends(
        get_db
    ),
):

    telemetry_event_id = None


    # ----------------------------------
    # Record when learner responds.
    #
    # Telemetry must never prevent
    # tutoring from functioning.
    # ----------------------------------

    try:

        telemetry_event = (
            TelemetryService
            .start_student_interaction(
                db=db,

                session_id=(
                    session_id
                ),

                student_message=(
                    data.message
                ),
            )
        )

        telemetry_event_id = (
            telemetry_event.id
        )

    except Exception:

        db.rollback()

        logger.exception(
            "Could not start "
            "learning telemetry."
        )


    try:

        response = (
            TutorChatService
            .process_message(
                db=db,

                session_id=(
                    session_id
                ),

                student_message=(
                    data.message
                ),
            )
        )


        # ----------------------------------
        # Complete telemetry
        # ----------------------------------

        if (
            telemetry_event_id
            is not None
        ):

            try:

                (
                    TelemetryService
                    .complete_interaction(
                        db=db,

                        student_event_id=(
                            telemetry_event_id
                        ),

                        response=(
                            response
                        ),
                    )
                )

            except Exception:

                db.rollback()

                logger.exception(
                    "Could not complete "
                    "learning telemetry."
                )


        return response


    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(
                exc
            ),
        ) from exc


    except RuntimeError as exc:

        raise HTTPException(
            status_code=503,
            detail=str(
                exc
            ),
        ) from exc