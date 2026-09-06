from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class JobKeywordBase(BaseModel):
    keyword: str = Field(..., max_length=255)
    normalized_keyword: str = Field(..., max_length=255)
    category: Optional[str] = Field(None, max_length=100)
    source: Optional[str] = Field(None, max_length=100)
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)


class JobKeywordCreate(JobKeywordBase):
    job_id: UUID


class JobKeywordResponse(JobKeywordBase):
    id: UUID
    job_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class JobBase(BaseModel):
    external_id: Optional[str] = Field(None, max_length=255)
    title: str = Field(..., max_length=255)
    company: str = Field(..., max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    url: Optional[str] = None
    description: str
    source: str = Field(..., max_length=100)
    discovered_at: Optional[datetime] = None


class JobCreate(JobBase):
    pass


class JobResponse(JobBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    job_keywords: List[JobKeywordResponse] = []

    model_config = ConfigDict(from_attributes=True)
