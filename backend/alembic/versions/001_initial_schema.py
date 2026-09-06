"""Initial schema migration for Phase 2 models

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-09-03 14:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. users
    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_users'))
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # 2. jobs
    op.create_table(
        'jobs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('external_id', sa.String(length=255), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('company', sa.String(length=255), nullable=False),
        sa.Column('location', sa.String(length=255), nullable=True),
        sa.Column('url', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('source', sa.String(length=100), nullable=False),
        sa.Column('discovered_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_jobs')),
        sa.UniqueConstraint('source', 'external_id', name='uq_jobs_source_external_id')
    )
    op.create_index(op.f('ix_jobs_external_id'), 'jobs', ['external_id'], unique=False)
    op.create_index(op.f('ix_jobs_company'), 'jobs', ['company'], unique=False)
    op.create_index(op.f('ix_jobs_source'), 'jobs', ['source'], unique=False)
    op.create_index('ix_jobs_company_source', 'jobs', ['company', 'source'], unique=False)

    # 3. job_keywords
    op.create_table(
        'job_keywords',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('job_id', sa.UUID(), nullable=False),
        sa.Column('keyword', sa.String(length=255), nullable=False),
        sa.Column('normalized_keyword', sa.String(length=255), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('source', sa.String(length=100), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], name=op.f('fk_job_keywords_job_id_jobs'), ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_job_keywords'))
    )
    op.create_index(op.f('ix_job_keywords_job_id'), 'job_keywords', ['job_id'], unique=False)
    op.create_index(op.f('ix_job_keywords_normalized_keyword'), 'job_keywords', ['normalized_keyword'], unique=False)

    # 4. resumes
    op.create_table(
        'resumes',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('original_filename', sa.String(length=255), nullable=True),
        sa.Column('storage_path', sa.String(length=512), nullable=True),
        sa.Column('parsed_content', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_resumes_user_id_users'), ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_resumes'))
    )
    op.create_index(op.f('ix_resumes_user_id'), 'resumes', ['user_id'], unique=False)

    # 5. resume_versions
    op.create_table(
        'resume_versions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('resume_id', sa.UUID(), nullable=False),
        sa.Column('job_id', sa.UUID(), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('version_type', sa.String(length=50), nullable=True),
        sa.Column('latex_source', sa.Text(), nullable=True),
        sa.Column('pdf_path', sa.String(length=512), nullable=True),
        sa.Column('status', sa.Enum('draft', 'generated', 'approved', 'rejected', 'failed', name='resume_version_status_enum'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], name=op.f('fk_resume_versions_job_id_jobs'), ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], name=op.f('fk_resume_versions_resume_id_resumes'), ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_resume_versions'))
    )
    op.create_index(op.f('ix_resume_versions_job_id'), 'resume_versions', ['job_id'], unique=False)
    op.create_index(op.f('ix_resume_versions_resume_id'), 'resume_versions', ['resume_id'], unique=False)
    op.create_index(op.f('ix_resume_versions_status'), 'resume_versions', ['status'], unique=False)

    # 6. pipeline_runs
    op.create_table(
        'pipeline_runs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('job_id', sa.UUID(), nullable=False),
        sa.Column('correlation_id', sa.String(length=255), nullable=False),
        sa.Column('status', sa.Enum('pending', 'running', 'waiting_approval', 'completed', 'failed', 'rejected', name='pipeline_run_status_enum'), nullable=False),
        sa.Column('current_step', sa.String(length=100), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], name=op.f('fk_pipeline_runs_job_id_jobs'), ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_pipeline_runs_user_id_users'), ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_pipeline_runs'))
    )
    op.create_index(op.f('ix_pipeline_runs_correlation_id'), 'pipeline_runs', ['correlation_id'], unique=True)
    op.create_index(op.f('ix_pipeline_runs_job_id'), 'pipeline_runs', ['job_id'], unique=False)
    op.create_index(op.f('ix_pipeline_runs_status'), 'pipeline_runs', ['status'], unique=False)
    op.create_index(op.f('ix_pipeline_runs_user_id'), 'pipeline_runs', ['user_id'], unique=False)

    # 7. pipeline_steps
    op.create_table(
        'pipeline_steps',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('pipeline_run_id', sa.UUID(), nullable=False),
        sa.Column('step_name', sa.String(length=100), nullable=False),
        sa.Column('status', sa.Enum('pending', 'running', 'completed', 'failed', 'skipped', name='pipeline_step_status_enum'), nullable=False),
        sa.Column('attempt', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['pipeline_run_id'], ['pipeline_runs.id'], name=op.f('fk_pipeline_steps_pipeline_run_id_pipeline_runs'), ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_pipeline_steps'))
    )
    op.create_index(op.f('ix_pipeline_steps_pipeline_run_id'), 'pipeline_steps', ['pipeline_run_id'], unique=False)

    # 8. approvals
    op.create_table(
        'approvals',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('pipeline_run_id', sa.UUID(), nullable=False),
        sa.Column('resume_version_id', sa.UUID(), nullable=False),
        sa.Column('status', sa.Enum('pending', 'approved', 'rejected', name='approval_status_enum'), nullable=False),
        sa.Column('requested_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('responded_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('reviewer_note', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['pipeline_run_id'], ['pipeline_runs.id'], name=op.f('fk_approvals_pipeline_run_id_pipeline_runs'), ondelete='RESTRICT'),
        sa.ForeignKeyConstraint(['resume_version_id'], ['resume_versions.id'], name=op.f('fk_approvals_resume_version_id_resume_versions'), ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_approvals'))
    )
    op.create_index(op.f('ix_approvals_pipeline_run_id'), 'approvals', ['pipeline_run_id'], unique=False)
    op.create_index(op.f('ix_approvals_resume_version_id'), 'approvals', ['resume_version_id'], unique=False)

    # 9. events
    op.create_table(
        'events',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('event_id', sa.String(length=255), nullable=False),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('correlation_id', sa.String(length=255), nullable=True),
        sa.Column('pipeline_id', sa.UUID(), nullable=True),
        sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('processed_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_events'))
    )
    op.create_index(op.f('ix_events_correlation_id'), 'events', ['correlation_id'], unique=False)
    op.create_index(op.f('ix_events_event_id'), 'events', ['event_id'], unique=True)
    op.create_index(op.f('ix_events_event_type'), 'events', ['event_type'], unique=False)
    op.create_index(op.f('ix_events_pipeline_id'), 'events', ['pipeline_id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse dependency order
    op.drop_table('events')
    op.drop_table('approvals')
    op.drop_table('pipeline_steps')
    op.drop_table('pipeline_runs')
    op.drop_table('resume_versions')
    op.drop_table('resumes')
    op.drop_table('job_keywords')
    op.drop_table('jobs')
    op.drop_table('users')

    # Drop custom Enum types
    sa.Enum(name='approval_status_enum').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='pipeline_step_status_enum').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='pipeline_run_status_enum').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='resume_version_status_enum').drop(op.get_bind(), checkfirst=True)
