from fastapi import APIRouter
from app.api.v1 import health
from app.api.v1.endpoints import users, jobs, resumes, pipelines, approvals, events, websocket

api_v1_router = APIRouter(prefix="/v1")
api_v1_router.include_router(health.router)
api_v1_router.include_router(users.router, prefix="/users", tags=["Users"])
api_v1_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
api_v1_router.include_router(resumes.router, prefix="/resumes", tags=["Resumes"])
api_v1_router.include_router(pipelines.router, prefix="/pipelines", tags=["Pipelines"])
api_v1_router.include_router(approvals.router, prefix="/approvals", tags=["Approvals"])
api_v1_router.include_router(events.router, prefix="/events", tags=["Events"])
api_v1_router.include_router(websocket.router, tags=["WebSocket"])
