from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.database.models.pipeline import PipelineRunStatus, PipelineStepStatus


class PipelineStepBase(BaseModel):
    step_name: str = Field(..., max_length=100)
    status: PipelineStepStatus = PipelineStepStatus.PENDING
    attempt: int = Field(default=1, ge=1)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    metadata_: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class PipelineStepCreate(PipelineStepBase):
    pipeline_run_id: UUID


class PipelineStepResponse(PipelineStepBase):
    id: UUID
    pipeline_run_id: UUID
    created_at: datetime
    updated_at: datetime

    @model_validator(mode="before")
    @classmethod
    def extract_orm_metadata(cls, data: Any) -> Any:
        if hasattr(data, "metadata_"):
            return {
                "id": getattr(data, "id", None),
                "pipeline_run_id": getattr(data, "pipeline_run_id", None),
                "step_name": getattr(data, "step_name", None),
                "status": getattr(data, "status", None),
                "attempt": getattr(data, "attempt", None),
                "started_at": getattr(data, "started_at", None),
                "completed_at": getattr(data, "completed_at", None),
                "error_message": getattr(data, "error_message", None),
                "metadata_": getattr(data, "metadata_", None),
                "created_at": getattr(data, "created_at", None),
                "updated_at": getattr(data, "updated_at", None),
            }
        return data

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class PipelineRunBase(BaseModel):
    correlation_id: str = Field(..., max_length=255)
    status: PipelineRunStatus = PipelineRunStatus.PENDING
    current_step: Optional[str] = Field(None, max_length=100)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None


class PipelineRunCreate(PipelineRunBase):
    user_id: UUID
    job_id: UUID


class PipelineRunResponse(PipelineRunBase):
    id: UUID
    user_id: UUID
    job_id: UUID
    created_at: datetime
    updated_at: datetime
    steps: List[PipelineStepResponse] = []

    model_config = ConfigDict(from_attributes=True)
