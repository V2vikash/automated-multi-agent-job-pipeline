import enum
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional, List
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

if TYPE_CHECKING:
    from app.database.models.resume import Resume
    from app.database.models.job import Job
    from app.database.models.approval import Approval


class ResumeVersionStatus(str, enum.Enum):
    DRAFT = "draft"
    GENERATED = "generated"
    APPROVED = "approved"
    REJECTED = "rejected"
    FAILED = "failed"


class ResumeVersion(Base):
    __tablename__ = "resume_versions"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    resume_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("resumes.id", ondelete="RESTRICT"),
        index=True,
        nullable=False
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("jobs.id", ondelete="RESTRICT"),
        index=True,
        nullable=False
    )
    version_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    version_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    latex_source: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    pdf_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    status: Mapped[ResumeVersionStatus] = mapped_column(
        Enum(
            ResumeVersionStatus,
            name="resume_version_status_enum",
            values_callable=lambda obj: [e.value for e in obj]
        ),
        default=ResumeVersionStatus.DRAFT,
        index=True,
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    resume: Mapped["Resume"] = relationship("Resume", back_populates="versions")
    job: Mapped["Job"] = relationship("Job", back_populates="resume_versions")
    approvals: Mapped[List["Approval"]] = relationship(
        "Approval",
        back_populates="resume_version",
        passive_deletes=True
    )
