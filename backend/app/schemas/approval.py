from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.database.models.approval import ApprovalStatus


class ApprovalBase(BaseModel):
    status: ApprovalStatus = ApprovalStatus.PENDING
    requested_at: datetime
    responded_at: Optional[datetime] = None
    reviewer_note: Optional[str] = None


class ApprovalCreate(ApprovalBase):
    pipeline_run_id: UUID
    resume_version_id: UUID


class ApprovalResponse(ApprovalBase):
    id: UUID
    pipeline_run_id: UUID
    resume_version_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
