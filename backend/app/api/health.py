from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()


@router.get("/health", tags=["Health"])
async def root_health_check():
    """Root health check endpoint."""
    return {
        "status": "ok",
        "service": "job-intelligence-platform",
        "environment": settings.APP_ENV
    }
