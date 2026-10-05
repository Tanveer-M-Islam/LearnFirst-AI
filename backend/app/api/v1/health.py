from fastapi import APIRouter

from app.core.config import get_settings


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
async def health_check():
    return {
        "status": "ok",
        "service": "learnfirst-api",
    }


@router.get("/version")
async def version():
    settings = get_settings()

    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }