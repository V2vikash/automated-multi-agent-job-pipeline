from fastapi import APIRouter
from app.core.config import settings
from app.database.connection import check_db_health
from app.kafka import check_kafka_health

router = APIRouter()


@router.get("/health", tags=["Health"])
async def v1_health_check():
    """Version 1 API health check endpoint with real DB and Kafka checks."""
    db_online = await check_db_health()
    kafka_online = await check_kafka_health()

    return {
        "status": "ok" if (db_online or settings.APP_ENV in ["testing", "development"]) else "degraded",
        "service": "job-intelligence-platform",
        "version": "v1",
        "environment": settings.APP_ENV,
        "database": "online" if db_online else "offline",
        "kafka": "online" if kafka_online else "offline"
    }
