import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class WebSocketEvent(BaseModel):
    """Event envelope transmitted over real-time WebSocket connection."""
    event_id: str = Field(default_factory=lambda: f"ws-evt-{uuid.uuid4()}")
    event_type: str = Field(..., max_length=100)
    pipeline_id: Optional[str] = None
    correlation_id: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    data: Dict[str, Any] = Field(default_factory=dict)
