from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.database.models.user import User
from app.database.models.job import Job
from app.database.models.resume import Resume
from app.database.models.resume_version import ResumeVersion
from app.schemas.resume import (
    ResumeCreate, ResumeResponse, ResumeVersionCreate, ResumeVersionResponse
)

router = APIRouter()


@router.post("/", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def create_resume(
    resume_in: ResumeCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new candidate master resume."""
    user_stmt = select(User).where(User.id == resume_in.user_id)
    user_res = await db.execute(user_stmt)
    if not user_res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User '{resume_in.user_id}' not found."
        )

    resume = Resume(
        user_id=resume_in.user_id,
        title=resume_in.title,
        original_filename=resume_in.original_filename,
        storage_path=resume_in.storage_path,
        parsed_content=resume_in.parsed_content
    )
    db.add(resume)
    await db.flush()
    await db.refresh(resume)
    return resume


@router.get("/", response_model=List[ResumeResponse])
async def list_resumes(
    user_id: Optional[UUID] = Query(None, description="Filter by User UUID"),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """List candidate master resumes with user filter and pagination."""
    stmt = select(Resume)
    if user_id:
        stmt = stmt.where(Resume.user_id == user_id)
    stmt = stmt.offset(offset).limit(limit).order_by(Resume.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Retrieve master resume details by UUID."""
    stmt = select(Resume).where(Resume.id == resume_id)
    result = await db.execute(stmt)
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Master resume '{resume_id}' not found."
        )
    return resume


@router.post("/{resume_id}/versions", response_model=ResumeVersionResponse, status_code=status.HTTP_201_CREATED)
async def create_resume_version(
    resume_id: UUID,
    version_in: ResumeVersionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a tailored resume variant for a specific job posting."""
    # Verify master resume exists
    r_stmt = select(Resume).where(Resume.id == resume_id)
    r_res = await db.execute(r_stmt)
    if not r_res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Master resume '{resume_id}' not found."
        )

    # Verify job posting exists
    j_stmt = select(Job).where(Job.id == version_in.job_id)
    j_res = await db.execute(j_stmt)
    if not j_res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job posting '{version_in.job_id}' not found."
        )

    version = ResumeVersion(
        resume_id=resume_id,
        job_id=version_in.job_id,
        version_number=version_in.version_number,
        version_type=version_in.version_type,
        latex_source=version_in.latex_source,
        pdf_path=version_in.pdf_path,
        status=version_in.status
    )
    db.add(version)
    await db.flush()
    await db.refresh(version)
    return version


@router.get("/{resume_id}/versions", response_model=List[ResumeVersionResponse])
async def list_resume_versions(
    resume_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """List tailored variants for a master resume."""
    stmt = select(ResumeVersion).where(ResumeVersion.resume_id == resume_id).order_by(ResumeVersion.version_number.asc())
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/versions/{version_id}", response_model=ResumeVersionResponse)
async def get_resume_version(
    version_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Retrieve details of a specific tailored resume variant."""
    stmt = select(ResumeVersion).where(ResumeVersion.id == version_id)
    result = await db.execute(stmt)
    version = result.scalar_one_or_none()
    if not version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume version '{version_id}' not found."
        )
    return version
