import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class EventEnvelope(BaseModel):
    """Standardized event envelope across Kafka event stream."""
    event_id: str = Field(default_factory=lambda: f"evt-{uuid.uuid4()}")
    event_type: str = Field(..., max_length=100)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    correlation_id: str = Field(..., max_length=255)
    pipeline_id: Optional[str] = Field(None, max_length=255)
    payload: Dict[str, Any] = Field(default_factory=dict)
