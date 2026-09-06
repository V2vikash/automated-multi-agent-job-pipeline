import uuid
from datetime import datetime, timezone
from typing import Optional, Any
from sqlalchemy import DateTime, String, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    event_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    event_type: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=False
    )
    correlation_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        index=True,
        nullable=True
    )
    pipeline_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        index=True,
        nullable=True
    )
    payload: Mapped[dict[str, Any]] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=False
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    processed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
