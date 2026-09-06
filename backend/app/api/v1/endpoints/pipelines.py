from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.database.models.user import User
from app.database.models.job import Job
from app.database.models.pipeline import PipelineRun, PipelineStep, PipelineRunStatus, PipelineStepStatus
from app.schemas.pipeline import (
    PipelineRunCreate, PipelineRunResponse, PipelineStepBase, PipelineStepResponse
)

router = APIRouter()


@router.post("/", response_model=PipelineRunResponse, status_code=status.HTTP_201_CREATED)
async def create_pipeline_run(
    run_in: PipelineRunCreate,
    db: AsyncSession = Depends(get_db)
):
    """Trigger / create a new pipeline orchestration run."""
    # Check correlation uniqueness
    corr_stmt = select(PipelineRun).where(PipelineRun.correlation_id == run_in.correlation_id)
    c_res = await db.execute(corr_stmt)
    if c_res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Pipeline run with correlation_id '{run_in.correlation_id}' already exists."
        )

    # Verify user & job exist
    u_res = await db.execute(select(User).where(User.id == run_in.user_id))
    if not u_res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User '{run_in.user_id}' not found."
        )

    j_res = await db.execute(select(Job).where(Job.id == run_in.job_id))
    if not j_res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job posting '{run_in.job_id}' not found."
        )

    run = PipelineRun(
        user_id=run_in.user_id,
        job_id=run_in.job_id,
        correlation_id=run_in.correlation_id,
        status=run_in.status,
        current_step=run_in.current_step,
        started_at=run_in.started_at,
        completed_at=run_in.completed_at,
        error_message=run_in.error_message
    )
    db.add(run)
    await db.flush()

    stmt = select(PipelineRun).options(selectinload(PipelineRun.steps)).where(PipelineRun.id == run.id)
    res = await db.execute(stmt)
    return res.scalar_one()


@router.get("/", response_model=List[PipelineRunResponse])
async def list_pipeline_runs(
    status_filter: Optional[PipelineRunStatus] = Query(None, alias="status"),
    user_id: Optional[UUID] = Query(None),
    job_id: Optional[UUID] = Query(None),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """List pipeline runs with filters and pagination."""
    stmt = select(PipelineRun).options(selectinload(PipelineRun.steps))
    if status_filter:
        stmt = stmt.where(PipelineRun.status == status_filter)
    if user_id:
        stmt = stmt.where(PipelineRun.user_id == user_id)
    if job_id:
        stmt = stmt.where(PipelineRun.job_id == job_id)

    stmt = stmt.offset(offset).limit(limit).order_by(PipelineRun.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{pipeline_id}", response_model=PipelineRunResponse)
async def get_pipeline_run(
    pipeline_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Retrieve pipeline run details with step execution history."""
    stmt = select(PipelineRun).options(selectinload(PipelineRun.steps)).where(PipelineRun.id == pipeline_id)
    result = await db.execute(stmt)
    run = result.scalar_one_or_none()
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pipeline run '{pipeline_id}' not found."
        )
    return run


@router.post("/{pipeline_id}/steps", response_model=PipelineStepResponse, status_code=status.HTTP_201_CREATED)
async def record_pipeline_step(
    pipeline_id: UUID,
    step_in: PipelineStepBase,
    db: AsyncSession = Depends(get_db)
):
    """Record an execution step for a pipeline run."""
    stmt = select(PipelineRun).where(PipelineRun.id == pipeline_id)
    res = await db.execute(stmt)
    run = res.scalar_one_or_none()
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pipeline run '{pipeline_id}' not found."
        )

    step = PipelineStep(
        pipeline_run_id=pipeline_id,
        step_name=step_in.step_name,
        status=step_in.status,
        attempt=step_in.attempt,
        started_at=step_in.started_at,
        completed_at=step_in.completed_at,
        error_message=step_in.error_message,
        metadata_=step_in.metadata_
    )
    db.add(step)

    # Update current_step on pipeline run
    run.current_step = step_in.step_name
    await db.flush()
    await db.refresh(step)
    return step


@router.patch("/{pipeline_id}/status", response_model=PipelineRunResponse)
async def update_pipeline_status(
    pipeline_id: UUID,
    new_status: PipelineRunStatus = Query(..., alias="status"),
    error_message: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Update status of an active or completed pipeline run."""
    stmt = select(PipelineRun).options(selectinload(PipelineRun.steps)).where(PipelineRun.id == pipeline_id)
    res = await db.execute(stmt)
    run = res.scalar_one_or_none()
    if not run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pipeline run '{pipeline_id}' not found."
        )

    run.status = new_status
    if error_message:
        run.error_message = error_message

    await db.flush()
    await db.refresh(run)
    return run
