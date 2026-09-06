from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.database.models.resume_version import ResumeVersionStatus


class ResumeBase(BaseModel):
    title: str = Field(..., max_length=255)
    original_filename: Optional[str] = Field(None, max_length=255)
    storage_path: Optional[str] = Field(None, max_length=512)
    parsed_content: Optional[Dict[str, Any]] = None


class ResumeCreate(ResumeBase):
    user_id: UUID


class ResumeResponse(ResumeBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResumeVersionBase(BaseModel):
    version_number: int = Field(default=1, ge=1)
    version_type: Optional[str] = Field(None, max_length=50)
    latex_source: Optional[str] = None
    pdf_path: Optional[str] = Field(None, max_length=512)
    status: ResumeVersionStatus = ResumeVersionStatus.DRAFT


class ResumeVersionCreate(ResumeVersionBase):
    resume_id: UUID
    job_id: UUID


class ResumeVersionResponse(ResumeVersionBase):
    id: UUID
    resume_id: UUID
    job_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
