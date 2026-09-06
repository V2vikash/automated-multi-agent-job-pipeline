# System Architecture - Job Intelligence Platform

## Overview
The **Job Intelligence Platform** is an automated end-to-end multi-agent system designed to discover job postings, extract key skills using deterministic Aho-Corasick matching, orchestrate workflow execution using LangGraph, tailor LaTeX resumes, and manage Human-In-The-Loop (HITL) approval prior to submission.

## Overall Architecture Flow
```
Playwright Scraping
    ↓
Job Discovery
    ↓
Kafka Event Bus
    ↓
LangGraph Orchestrator
    ↓
Aho-Corasick Keyword Engine
    ↓
Job/Candidate Matching
    ↓
Tailored Resume Generation
    ↓
LaTeX → PDF Rendering
    ↓
WebSocket HITL
    ↓
Human Approval
```

## Phase 2: PostgreSQL Persistence Layer Architecture

### Stack
- **Database**: PostgreSQL 16
- **ORM**: Async SQLAlchemy 2.0 (`Mapped[]`, `mapped_column()`, `relationship()`)
- **Driver**: `asyncpg` (`postgresql+asyncpg://...`)
- **Migrations**: Async Alembic
- **Validation**: Pydantic v2

### Tables & Schema Specs

#### 1. `users`
- `id` (UUID, Primary Key)
- `name` (VARCHAR(255), NOT NULL)
- `email` (VARCHAR(255), UNIQUE, NOT NULL, Index)
- `phone` (VARCHAR(50), NULLABLE)
- `created_at` (TIMESTAMPTZ, NOT NULL)
- `updated_at` (TIMESTAMPTZ, NOT NULL)

#### 2. `jobs`
- `id` (UUID, Primary Key)
- `external_id` (VARCHAR(255), NULLABLE, Index)
- `title` (VARCHAR(255), NOT NULL)
- `company` (VARCHAR(255), NOT NULL, Index)
- `location` (VARCHAR(255), NULLABLE)
- `url` (TEXT, NULLABLE)
- `description` (TEXT, NOT NULL)
- `source` (VARCHAR(100), NOT NULL, Index)
- `discovered_at` (TIMESTAMPTZ, NULLABLE)
- `created_at` (TIMESTAMPTZ, NOT NULL)
- `updated_at` (TIMESTAMPTZ, NOT NULL)
- Constraint: `UniqueConstraint("source", "external_id")`
- Index: `Index("ix_jobs_company_source", "company", "source")`

#### 3. `job_keywords`
- `id` (UUID, Primary Key)
- `job_id` (UUID, FK -> `jobs.id`, RESTRICT, Index)
- `keyword` (VARCHAR(255), NOT NULL)
- `normalized_keyword` (VARCHAR(255), NOT NULL, Index)
- `category` (VARCHAR(100), NULLABLE)
- `source` (VARCHAR(100), NULLABLE)
- `confidence` (FLOAT, NULLABLE)
- `created_at` (TIMESTAMPTZ, NOT NULL)

#### 4. `resumes`
- `id` (UUID, Primary Key)
- `user_id` (UUID, FK -> `users.id`, RESTRICT, Index)
- `title` (VARCHAR(255), NOT NULL)
- `original_filename` (VARCHAR(255), NULLABLE)
- `storage_path` (VARCHAR(512), NULLABLE)
- `parsed_content` (JSONB, NULLABLE)
- `created_at` (TIMESTAMPTZ, NOT NULL)
- `updated_at` (TIMESTAMPTZ, NOT NULL)

#### 5. `resume_versions`
- `id` (UUID, Primary Key)
- `resume_id` (UUID, FK -> `resumes.id`, RESTRICT, Index)
- `job_id` (UUID, FK -> `jobs.id`, RESTRICT, Index)
- `version_number` (INTEGER, DEFAULT 1)
- `version_type` (VARCHAR(50), NULLABLE)
- `latex_source` (TEXT, NULLABLE)
- `pdf_path` (VARCHAR(512), NULLABLE)
- `status` (Enum: `draft`, `generated`, `approved`, `rejected`, `failed`, Index)
- `created_at` (TIMESTAMPTZ, NOT NULL)
- `updated_at` (TIMESTAMPTZ, NOT NULL)

#### 6. `pipeline_runs`
- `id` (UUID, Primary Key)
- `user_id` (UUID, FK -> `users.id`, RESTRICT, Index)
- `job_id` (UUID, FK -> `jobs.id`, RESTRICT, Index)
- `correlation_id` (VARCHAR(255), UNIQUE, Index)
- `status` (Enum: `pending`, `running`, `waiting_approval`, `completed`, `failed`, `rejected`, Index)
- `current_step` (VARCHAR(100), NULLABLE)
- `started_at` (TIMESTAMPTZ, NULLABLE)
- `completed_at` (TIMESTAMPTZ, NULLABLE)
- `error_message` (TEXT, NULLABLE)
- `created_at` (TIMESTAMPTZ, NOT NULL)
- `updated_at` (TIMESTAMPTZ, NOT NULL)

#### 7. `pipeline_steps`
- `id` (UUID, Primary Key)
- `pipeline_run_id` (UUID, FK -> `pipeline_runs.id`, RESTRICT, Index)
- `step_name` (VARCHAR(100), NOT NULL)
- `status` (Enum: `pending`, `running`, `completed`, `failed`, `skipped`)
- `attempt` (INTEGER, DEFAULT 1)
- `started_at` (TIMESTAMPTZ, NULLABLE)
- `completed_at` (TIMESTAMPTZ, NULLABLE)
- `error_message` (TEXT, NULLABLE)
- `metadata` (JSONB, NULLABLE)
- `created_at` (TIMESTAMPTZ, NOT NULL)
- `updated_at` (TIMESTAMPTZ, NOT NULL)

#### 8. `approvals`
- `id` (UUID, Primary Key)
- `pipeline_run_id` (UUID, FK -> `pipeline_runs.id`, RESTRICT, Index)
- `resume_version_id` (UUID, FK -> `resume_versions.id`, RESTRICT, Index)
- `status` (Enum: `pending`, `approved`, `rejected`)
- `requested_at` (TIMESTAMPTZ, NOT NULL)
- `responded_at` (TIMESTAMPTZ, NULLABLE)
- `reviewer_note` (TEXT, NULLABLE)
- `created_at` (TIMESTAMPTZ, NOT NULL)
- `updated_at` (TIMESTAMPTZ, NOT NULL)

#### 9. `events`
- `id` (UUID, Primary Key)
- `event_id` (VARCHAR(255), UNIQUE, Index)
- `event_type` (VARCHAR(100), Index)
- `correlation_id` (VARCHAR(255), NULLABLE, Index)
- `pipeline_id` (UUID, NULLABLE, Index)
- `payload` (JSONB, NOT NULL)
- `status` (VARCHAR(50), DEFAULT 'pending')
- `created_at` (TIMESTAMPTZ, NOT NULL)
- `processed_at` (TIMESTAMPTZ, NULLABLE)

## Migration Lifecycle Commands
```bash
# Upgrade database to head revision
python -m alembic upgrade head

# Rollback single revision
python -m alembic downgrade -1

# Rollback to initial empty state
python -m alembic downgrade base
```
