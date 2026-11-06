
from fastapi import (
    APIRouter,
)

from app.api.v1.adaptive import (
    router as adaptive_router,
)
from app.api.v1.assessments import (
    router as assessments_router,
)
from app.api.v1.auth import (
    router as auth_router,
)
from app.api.v1.chat import (
    router as chat_router,
)
from app.api.v1.curriculum import (
    router as curriculum_router,
)
from app.api.v1.english_adaptive import (
    router as english_adaptive_router,
)
from app.api.v1.english_progress import (
    router as english_progress_router,
)
from app.api.v1.health import (
    router as health_router,
)
from app.api.v1.history import (
    router as history_router,
)
from app.api.v1.science_adaptive import (
    router as science_adaptive_router,
)
from app.api.v1.science_assessments import (
    router as science_assessments_router,
)
from app.api.v1.sessions import (
    router as sessions_router,
)
from app.api.v1.students import (
    router as students_router,
)
from app.api.v1.telemetry import (
    router as telemetry_router,
)
from app.api.v1.tutor import (
    router as tutor_router,
)


api_router = APIRouter()


api_router.include_router(
    health_router
)


api_router.include_router(
    auth_router
)


api_router.include_router(
    students_router
)


api_router.include_router(
    sessions_router
)


api_router.include_router(
    tutor_router
)


api_router.include_router(
    chat_router
)


api_router.include_router(
    history_router
)


api_router.include_router(
    assessments_router
)


api_router.include_router(
    science_assessments_router
)


api_router.include_router(
    curriculum_router
)


api_router.include_router(
    adaptive_router
)


api_router.include_router(
    science_adaptive_router
)


api_router.include_router(
    english_adaptive_router
)


# api_router.include_router(
#     english_adaptive_router
# ) if False else None


api_router.include_router(
    english_progress_router
)


api_router.include_router(
    telemetry_router
)
