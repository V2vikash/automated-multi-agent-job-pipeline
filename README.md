# Job Intelligence Platform

The **Job Intelligence Platform** is an enterprise-grade automated multi-agent job application and career intelligence pipeline designed to ingest, process, match, and tailor resumes to software job opportunities at scale.

> **Note:** This repository has completed **Phase 1: Project Foundation & Development Infrastructure** and **Phase 2: Database Data Models & Alembic Migrations**.

---

## 🏗️ Architecture Overview

The system architecture is structured as a decoupled monorepo containing:

- **Backend Service**: FastAPI REST API providing health endpoints, configuration management, database session management, and structured logging.
- **Database Layer**: PostgreSQL 16 + Async SQLAlchemy 2.0 ORM + Alembic database migrations.
- **Frontend App**: React 18 + TypeScript + Vite dashboard giving real-time operational status.
- **Worker Infrastructure**: Distributed worker scaffolding (`job_worker`, `keyword_worker`, `resume_worker`, `pipeline_worker`).
- **Data Persistence & Messaging**: PostgreSQL for relational storage, Apache Kafka (KRaft mode) for event stream processing, and Redis for caching/coordination.

---

## 🗄️ Database Architecture (Phase 2)

Phase 2 establishes the PostgreSQL relational schema and Async Alembic migration engine.

### Database Stack
- **Engine**: PostgreSQL 16
- **ORM**: Async SQLAlchemy 2.0 (`Mapped[]`, `mapped_column()`, `relationship()`)
- **Driver**: `asyncpg` (`postgresql+asyncpg://...`)
- **Migrations**: Alembic with async context support
- **Validation**: Pydantic v2 schemas (`app/schemas/`)

### Database Tables (9 Core Entities)
1. `users`: System users and candidate profiles (email uniqueness constraint, indexed).
2. `jobs`: Scraping target/discovered software job postings (`(source, external_id)` unique constraint, company/source indexes).
3. `job_keywords`: Normalized skill/tech keywords extracted for jobs (indexed on `job_id` and `normalized_keyword`).
4. `resumes`: User master resume documents with JSONB parsed content storage.
5. `resume_versions`: Tailored resume variants linked to specific job postings with status tracking (`draft`, `generated`, `approved`, `rejected`, `failed`).
6. `pipeline_runs`: Orchestration execution runs (`correlation_id` indexed, status tracking `pending`, `running`, `waiting_approval`, `completed`, `failed`, `rejected`).
7. `pipeline_steps`: Granular pipeline step execution history with JSONB metadata and attempt tracking.
8. `approvals`: Human-In-The-Loop approval requests linking pipeline runs and resume variants.
9. `events`: Persistent audit event log for Kafka events (`event_id` unique, `correlation_id` and `pipeline_id` indexed).

### Entity Relationships
```
User (1) ────< Resumes (N) ────< ResumeVersions (N) ────< Approvals (N)
  │                                     │                        │
  └──────────< PipelineRuns (N) ────────┼────────────────────────┘
                    │                   │
Job  (1) ───────────┴───────────────────┘
  ├───< JobKeywords (N)
  └───< ResumeVersions (N)

Events (Audit Log correlated via event_id, correlation_id, pipeline_id)
```

---

## ⚙️ Alembic Migration Operations

### Apply Migrations (Upgrade Schema)
```bash
cd backend
python -m alembic upgrade head
```

### Roll Back Last Migration (Downgrade)
```bash
cd backend
python -m alembic downgrade -1
```

### Roll Back to Base Schema
```bash
cd backend
python -m alembic downgrade base
```

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.12+, FastAPI, Uvicorn, SQLAlchemy 2.0, Asyncpg, Alembic, Pydantic v2, Pytest |
| **Frontend** | React, TypeScript, Vite, Vanilla CSS |
| **Database** | PostgreSQL 16 |
| **Message Broker** | Apache Kafka (KRaft mode, no Zookeeper required) |
| **Cache/Store** | Redis 7 |
| **Containerization** | Docker, Docker Compose |

---

## 📂 Project Structure

```
job-intelligence-platform/
├── backend/
│   ├── alembic/
│   │   ├── versions/
│   │   │   └── 001_initial_schema.py
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── health.py
│   │   │   │   └── router.py
│   │   │   └── health.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── exceptions.py
│   │   │   └── logging.py
│   │   ├── database/
│   │   │   ├── models/
│   │   │   │   ├── user.py
│   │   │   │   ├── job.py
│   │   │   │   ├── keyword.py
│   │   │   │   ├── resume.py
│   │   │   │   ├── resume_version.py
│   │   │   │   ├── pipeline.py
│   │   │   │   ├── approval.py
│   │   │   │   ├── event.py
│   │   │   │   └── __init__.py
│   │   │   ├── base.py
│   │   │   ├── connection.py
│   │   │   └── __init__.py
│   │   ├── schemas/
│   │   │   ├── user.py
│   │   │   ├── job.py
│   │   │   ├── resume.py
│   │   │   ├── pipeline.py
│   │   │   ├── approval.py
│   │   │   ├── event.py
│   │   │   └── __init__.py
│   │   └── main.py
│   ├── tests/
│   │   ├── test_config.py
│   │   ├── test_health.py
│   │   ├── test_db_models.py
│   │   ├── test_db_connection.py
│   │   ├── test_alembic_migrations.py
│   │   └── test_main.py
│   ├── alembic.ini
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── requirements.txt
├── docker-compose.yml
├── Makefile
└── README.md
```

---

## ⚡ Prerequisites

- **Python**: 3.12 or higher
- **Node.js**: v18+ and npm v9+
- **Docker**: Docker Engine 24.0+ and Docker Compose v2+

---

## 🚀 Quick Start & Environment Setup

### 1. Copy Environment File
```bash
cp .env.example .env
```

### 2. Docker Compose
Start all services (PostgreSQL, Kafka, Redis, Backend, Frontend):
```bash
docker compose up -d --build
```

### 3. Run Database Migrations
```bash
cd backend
python -m alembic upgrade head
```

---

## 🧪 Testing

Run backend unit tests:
```bash
cd backend
python -m pytest -v
```

---

## 📋 Phase Roadmap

- [x] **Phase 1**: Project Foundation & Infrastructure
- [x] **Phase 2**: Database Data Models & Alembic Migrations
- [x] **Phase 3**: FastAPI API Implementation
- [x] **Phase 4**: Playwright Job Discovery
- [x] **Phase 5**: Kafka Event System
- [x] **Phase 6**: Aho-Corasick Keyword Engine
- [x] **Phase 7**: LangGraph Pipeline
- [x] **Phase 8**: Master Resume Processing
- [x] **Phase 9**: Tailored LaTeX + PDF Generation
- [x] **Phase 10**: WebSocket + Human-In-The-Loop (HITL)
- [x] **Phase 11**: Frontend Dashboard
- [x] **Phase 12**: Fault Tolerance + Recovery
- [x] **Phase 13**: Complete Testing
- [x] **Phase 14**: Final Integration & Documentation
