from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.database.models.pipeline import PipelineRun, PipelineRunStatus
from app.database.models.resume_version import ResumeVersion
from app.database.models.approval import Approval, ApprovalStatus
from app.schemas.approval import (
    ApprovalCreate, ApprovalResponse
)

router = APIRouter()


@router.post("/", response_model=ApprovalResponse, status_code=status.HTTP_201_CREATED)
async def create_approval_request(
    app_in: ApprovalCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a Human-In-The-Loop (HITL) approval request."""
    # Verify pipeline run exists
    p_stmt = select(PipelineRun).where(PipelineRun.id == app_in.pipeline_run_id)
    p_res = await db.execute(p_stmt)
    pipeline_run = p_res.scalar_one_or_none()
    if not pipeline_run:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pipeline run '{app_in.pipeline_run_id}' not found."
        )

    # Verify resume version exists
    rv_stmt = select(ResumeVersion).where(ResumeVersion.id == app_in.resume_version_id)
    rv_res = await db.execute(rv_stmt)
    if not rv_res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume version '{app_in.resume_version_id}' not found."
        )

    approval = Approval(
        pipeline_run_id=app_in.pipeline_run_id,
        resume_version_id=app_in.resume_version_id,
        status=app_in.status,
        requested_at=app_in.requested_at,
        responded_at=app_in.responded_at,
        reviewer_note=app_in.reviewer_note
    )
    db.add(approval)

    # Update pipeline run status to waiting_approval
    pipeline_run.status = PipelineRunStatus.WAITING_APPROVAL
    await db.flush()
    await db.refresh(approval)
    return approval


@router.get("/", response_model=List[ApprovalResponse])
async def list_approvals(
    status_filter: Optional[ApprovalStatus] = Query(None, alias="status"),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """List approval requests with status filter and pagination."""
    stmt = select(Approval)
    if status_filter:
        stmt = stmt.where(Approval.status == status_filter)
    stmt = stmt.offset(offset).limit(limit).order_by(Approval.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{approval_id}", response_model=ApprovalResponse)
async def get_approval(
    approval_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Retrieve approval request details by UUID."""
    stmt = select(Approval).where(Approval.id == approval_id)
    result = await db.execute(stmt)
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Approval request '{approval_id}' not found."
        )
    return app


@router.patch("/{approval_id}", response_model=ApprovalResponse)
async def respond_approval(
    approval_id: UUID,
    decision: ApprovalStatus = Query(..., description="Decision: approved or rejected"),
    reviewer_note: Optional[str] = Query(None, description="Optional notes from human reviewer"),
    db: AsyncSession = Depends(get_db)
):
    """Submit a human reviewer decision on an approval request."""
    if decision not in (ApprovalStatus.APPROVED, ApprovalStatus.REJECTED):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Decision status must be 'approved' or 'rejected'."
        )

    stmt = select(Approval).where(Approval.id == approval_id)
    result = await db.execute(stmt)
    app = result.scalar_one_or_none()
    if not app:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Approval request '{approval_id}' not found."
        )

    app.status = decision
    app.responded_at = datetime.now(timezone.utc)
    if reviewer_note:
        app.reviewer_note = reviewer_note

    # Update associated pipeline run status
    pipeline_stmt = select(PipelineRun).where(PipelineRun.id == app.pipeline_run_id)
    pipeline_res = await db.execute(pipeline_stmt)
    pipeline_run = pipeline_res.scalar_one_or_none()
    if pipeline_run:
        if decision == ApprovalStatus.APPROVED:
            pipeline_run.status = PipelineRunStatus.RUNNING
        elif decision == ApprovalStatus.REJECTED:
            pipeline_run.status = PipelineRunStatus.REJECTED

    await db.flush()
    await db.refresh(app)
    return app
