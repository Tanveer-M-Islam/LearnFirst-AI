
import logging

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.database.session import get_db


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


# ======================================
# API liveness
# ======================================

@router.get("")
async def health_check():
    return {
        "status": "ok",
        "service": "learnfirst-api",
    }


# ======================================
# API information
# ======================================

@router.get("/version")
async def version():
    settings = get_settings()

    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }


# ======================================
# Database readiness
# ======================================

@router.get("/ready")
def readiness_check(
    db: Session = Depends(get_db),
):
    try:
        db.execute(
            text("SELECT 1")
        );

    except SQLAlchemyError as exc:
        logger.exception(
            "Database readiness check failed."
        )

        raise HTTPException(
            status_code=503,
            detail="Database is unavailable.",
        ) from exc

    return {
        "status": "ready",
        "database": "ok",
    }
