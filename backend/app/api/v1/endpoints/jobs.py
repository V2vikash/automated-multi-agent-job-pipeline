from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import get_db
from app.database.models.job import Job
from app.database.models.keyword import JobKeyword
from app.schemas.job import (
    JobCreate, JobResponse, JobKeywordBase, JobKeywordResponse
)

router = APIRouter()


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_in: JobCreate,
    db: AsyncSession = Depends(get_db)
):
    """Ingest or create a new job posting."""
    if job_in.external_id:
        existing_stmt = select(Job).where(
            Job.source == job_in.source,
            Job.external_id == job_in.external_id
        )
        res = await db.execute(existing_stmt)
        if res.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Job from source '{job_in.source}' with external_id '{job_in.external_id}' already exists."
            )

    job = Job(
        external_id=job_in.external_id,
        title=job_in.title,
        company=job_in.company,
        location=job_in.location,
        url=job_in.url,
        description=job_in.description,
        source=job_in.source,
        discovered_at=job_in.discovered_at
    )
    db.add(job)
    await db.flush()

    # Refresh with empty keywords relationship loaded
    stmt = select(Job).options(selectinload(Job.job_keywords)).where(Job.id == job.id)
    res = await db.execute(stmt)
    return res.scalar_one()


@router.get("/", response_model=List[JobResponse])
async def list_jobs(
    company: Optional[str] = Query(None, description="Filter by company name"),
    source: Optional[str] = Query(None, description="Filter by job source"),
    location: Optional[str] = Query(None, description="Filter by job location"),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """List job postings with search and pagination filters."""
    stmt = select(Job).options(selectinload(Job.job_keywords))
    if company:
        stmt = stmt.where(Job.company.ilike(f"%{company}%"))
    if source:
        stmt = stmt.where(Job.source == source)
    if location:
        stmt = stmt.where(Job.location.ilike(f"%{location}%"))

    stmt = stmt.offset(offset).limit(limit).order_by(Job.created_at.desc())
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Retrieve job posting details by UUID."""
    stmt = select(Job).options(selectinload(Job.job_keywords)).where(Job.id == job_id)
    result = await db.execute(stmt)
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job posting '{job_id}' not found."
        )
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete a job posting."""
    stmt = select(Job).where(Job.id == job_id)
    result = await db.execute(stmt)
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job posting '{job_id}' not found."
        )

    await db.delete(job)
    await db.flush()


@router.post("/{job_id}/keywords", response_model=JobKeywordResponse, status_code=status.HTTP_201_CREATED)
async def add_job_keyword(
    job_id: UUID,
    keyword_in: JobKeywordBase,
    db: AsyncSession = Depends(get_db)
):
    """Associate an extracted skill keyword with a job posting."""
    stmt = select(Job).where(Job.id == job_id)
    result = await db.execute(stmt)
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job posting '{job_id}' not found."
        )

    kw = JobKeyword(
        job_id=job_id,
        keyword=keyword_in.keyword,
        normalized_keyword=keyword_in.normalized_keyword,
        category=keyword_in.category,
        source=keyword_in.source,
        confidence=keyword_in.confidence
    )
    db.add(kw)
    await db.flush()
    await db.refresh(kw)
    return kw
