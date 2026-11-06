from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)

from sqlalchemy.orm import (
    Session,
)

from app.database.session import (
    get_db,
)
from app.schemas.curriculum import (
    CurriculumTopicView,
    StudentCurriculumPathResponse,
)
from app.schemas.enums import (
    Subject,
)
from app.services.curriculum_service import (
    CurriculumService,
)


router = APIRouter(
    prefix="/curriculum",

    tags=[
        "Curriculum",
    ],
)


# ======================================================
# Existing RAG topics
# ======================================================

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


# ======================================================
# Development catalog
# ======================================================

@router.get(
    "/catalog",
)
def get_curriculum_catalog(
    subject: Subject,

    include_planned: bool = True,
):

    concepts = (
        CurriculumService
        .list_catalog(
            subject=(
                subject
            ),

            include_planned=(
                include_planned
            ),
        )
    )


    return [
        {
            "concept_code":
                concept.concept_code,

            "subject":
                concept.subject.value,

            "title":
                concept.title,

            "description":
                concept.description,

            "recommended_age":
                concept
                .recommended_age,

            "min_age":
                concept.min_age,

            "max_age":
                concept.max_age,

            "min_grade":
                concept.min_grade,

            "max_grade":
                concept.max_grade,

            "sequence_order":
                concept
                .sequence_order,

            "prerequisites":
                list(
                    concept.prerequisites
                ),

            "implemented":
                concept.implemented,

            "curriculum_profile":
                concept
                .curriculum_profile,
        }

        for concept
        in concepts
    ]


# ======================================================
# Student progression
# ======================================================

@router.get(
    (
        "/students/{student_id}"
        "/path"
    ),

    response_model=(
        StudentCurriculumPathResponse
    ),
)
def get_student_curriculum_path(
    student_id: str,

    subject: Subject,

    db: Session = Depends(
        get_db
    ),
):

    try:

        return (
            CurriculumService
            .get_student_path(
                db=db,

                student_id=(
                    student_id
                ),

                subject=(
                    subject
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