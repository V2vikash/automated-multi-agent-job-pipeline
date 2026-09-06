import pytest
from sqlalchemy import Index, UniqueConstraint
from app.database.base import Base
from app.database.models import (
    User, Job, JobKeyword, Resume, ResumeVersion,
    PipelineRun, PipelineStep, Approval, Event,
    ResumeVersionStatus, PipelineRunStatus, PipelineStepStatus, ApprovalStatus
)
from app.schemas import (
    UserCreate, UserResponse,
    JobCreate, JobResponse,
    ResumeCreate, ResumeResponse,
    PipelineRunCreate, PipelineRunResponse,
    ApprovalCreate, ApprovalResponse,
    EventCreate, EventResponse
)


def test_base_metadata_tables_exist():
    """Verify all 9 Phase 2 tables are properly registered in SQLAlchemy metadata."""
    expected_tables = {
        "users",
        "jobs",
        "job_keywords",
        "resumes",
        "resume_versions",
        "pipeline_runs",
        "pipeline_steps",
        "approvals",
        "events",
    }
    registered_tables = set(Base.metadata.tables.keys())
    assert expected_tables.issubset(registered_tables), f"Missing tables: {expected_tables - registered_tables}"


def test_user_model_attributes_and_relationships():
    """Verify User model attributes, columns, and relationships."""
    table = User.__table__
    assert "id" in table.columns
    assert "email" in table.columns
    assert table.columns["email"].unique is True or any(
        idx.unique for idx in table.indexes if "email" in idx.columns.keys()
    )
    assert hasattr(User, "resumes")
    assert hasattr(User, "pipeline_runs")


def test_job_model_indexes_and_constraints():
    """Verify Job model indexes and unique constraints."""
    table = Job.__table__
    assert "external_id" in table.columns
    assert "company" in table.columns
    assert "source" in table.columns

    # Verify unique constraint on source & external_id
    uq_names = [c.name for c in table.constraints if isinstance(c, UniqueConstraint)]
    assert "uq_jobs_source_external_id" in uq_names or any(
        set(c.columns.keys()) == {"source", "external_id"} for c in table.constraints if isinstance(c, UniqueConstraint)
    )

    # Verify relationships
    assert hasattr(Job, "job_keywords")
    assert hasattr(Job, "resume_versions")
    assert hasattr(Job, "pipeline_runs")


def test_job_keyword_model():
    """Verify JobKeyword table and foreign keys."""
    table = JobKeyword.__table__
    assert "job_id" in table.columns
    assert "normalized_keyword" in table.columns
    assert len(table.columns["job_id"].foreign_keys) > 0


def test_resume_and_version_models():
    """Verify Resume and ResumeVersion models and statuses."""
    assert ResumeVersionStatus.DRAFT.value == "draft"
    assert ResumeVersionStatus.GENERATED.value == "generated"
    assert ResumeVersionStatus.APPROVED.value == "approved"

    table = ResumeVersion.__table__
    assert "resume_id" in table.columns
    assert "job_id" in table.columns
    assert "status" in table.columns


def test_pipeline_run_and_step_models():
    """Verify PipelineRun and PipelineStep models."""
    assert PipelineRunStatus.PENDING.value == "pending"
    assert PipelineStepStatus.COMPLETED.value == "completed"

    run_table = PipelineRun.__table__
    assert "correlation_id" in run_table.columns
    assert run_table.columns["correlation_id"].unique is True

    step_table = PipelineStep.__table__
    assert "pipeline_run_id" in step_table.columns
    assert "metadata" in step_table.columns


def test_approval_and_event_models():
    """Verify Approval and Event models."""
    assert ApprovalStatus.PENDING.value == "pending"

    event_table = Event.__table__
    assert "event_id" in event_table.columns
    assert "payload" in event_table.columns


def test_pydantic_schemas_instantiation():
    """Verify Pydantic schemas can be instantiated and validated."""
    user_schema = UserCreate(name="John Doe", email="john@example.com", phone="+1234567890")
    assert user_schema.name == "John Doe"
    assert user_schema.email == "john@example.com"

    job_schema = JobCreate(
        title="Software Engineer",
        company="TechCorp",
        description="Great role",
        source="linkedin"
    )
    assert job_schema.title == "Software Engineer"
    assert job_schema.source == "linkedin"
