from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.database.models.event import Event
from app.schemas.event import (
    EventCreate, EventResponse
)

router = APIRouter()


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_in: EventCreate,
    db: AsyncSession = Depends(get_db)
):
    """Log an audit event payload."""
    # Check event_id uniqueness
    existing_stmt = select(Event).where(Event.event_id == event_in.event_id)
    res = await db.execute(existing_stmt)
    if res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Event with event_id '{event_in.event_id}' already exists."
        )

    event = Event(
        event_id=event_in.event_id,
        event_type=event_in.event_type,
        correlation_id=event_in.correlation_id,
        pipeline_id=event_in.pipeline_id,
        payload=event_in.payload,
        status=event_in.status
    )
    db.add(event)
    await db.flush()
    await db.refresh(event)
    return event


@router.get("/", response_model=List[EventResponse])
async def list_events(
    event_type: Optional[str] = Query(None, description="Filter by event type"),
    correlation_id: Optional[str] = Query(None, description="Filter by correlation ID"),
    pipeline_id: Optional[UUID] = Query(None, description="Filter by Pipeline UUID"),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """Query audit events with filters and pagination."""
    stmt = select(Event)
    if event_type:
        stmt = stmt.where(Event.event_type == event_type)
    if correlation_id:
        stmt = stmt.where(Event.correlation_id == correlation_id)
    if pipeline_id:
        stmt = stmt.where(Event.pipeline_id == pipeline_id)

    stmt = stmt.offset(offset).limit(limit).order_by(Event.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Retrieve audit event details by event_id."""
    stmt = select(Event).where(Event.event_id == event_id)
    result = await db.execute(stmt)
    event = result.scalar_one_or_none()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event '{event_id}' not found."
        )
    return event
