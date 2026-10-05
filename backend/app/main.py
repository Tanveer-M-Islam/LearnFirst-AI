import logging

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging_config import configure_logging
from app.middleware.request_id import request_id_middleware


configure_logging()

logger = logging.getLogger(__name__)

settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    description=(
        "Backend API for LearnFirst AI, "
        "an age-adaptive guided learning system."
    ),
)


app.middleware("http")(request_id_middleware)


app.include_router(
    api_router,
    prefix=settings.api_v1_prefix,
)


@app.get("/", tags=["Root"])
async def root():
    return {
        "name": settings.app_name,
        "message": "LearnFirst AI API is running.",
        "docs": "/docs",
    }


@app.on_event("startup")
async def startup_event():
    logger.info(
        "Starting %s v%s",
        settings.app_name,
        settings.app_version,
    )