from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class EventBase(BaseModel):
    event_id: str = Field(..., max_length=255)
    event_type: str = Field(..., max_length=100)
    correlation_id: Optional[str] = Field(None, max_length=255)
    pipeline_id: Optional[UUID] = None
    payload: Dict[str, Any]
    status: str = Field(default="pending", max_length=50)


class EventCreate(EventBase):
    pass


class EventResponse(EventBase):
    id: UUID
    created_at: datetime
    processed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
