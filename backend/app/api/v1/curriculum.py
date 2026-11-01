from fastapi import (
    APIRouter,
    Query,
)

from app.schemas.curriculum import (
    CurriculumTopicView,
)
from app.schemas.enums import (
    Subject,
)
from app.services.curriculum_service import (
    CurriculumService,
)


router = APIRouter(
    prefix="/curriculum",
    tags=["Curriculum"],
)


@router.get(
    "/topics",
    response_model=list[
        CurriculumTopicView
    ],
)
def list_curriculum_topics(
    subject: Subject = (
        Subject.SCIENCE
    ),

    curriculum_profile: str = Query(
        default=(
            "bangladesh_english_v1"
        ),
        min_length=1,
    ),
):

    return (
        CurriculumService
        .list_topics(
            subject=(
                subject.value
            ),

            curriculum_profile=(
                curriculum_profile
            ),
        )
    )