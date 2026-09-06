# REST & WebSocket API Reference — Job Intelligence Platform

## Base URL
`http://localhost:8000/api/v1`

## API Endpoints

### 1. Candidate Users (`/users`)
- `POST /users/`: Create candidate user profile.
- `GET /users/`: List candidate user profiles.
- `GET /users/{id}`: Get candidate user profile by UUID.
- `PUT /users/{id}`: Update candidate user profile.
- `DELETE /users/{id}`: Delete candidate user profile.

### 2. Job Postings (`/jobs`)
- `POST /jobs/`: Ingest job posting manually or from scraper.
- `GET /jobs/`: List jobs with optional company/source filters.
- `GET /jobs/{id}`: Get job posting details with keywords.
- `DELETE /jobs/{id}`: Delete job posting.
- `POST /jobs/{id}/keywords`: Associate extracted tech keyword.

### 3. Master Resumes & Variants (`/resumes`)
- `POST /resumes/`: Register candidate master resume.
- `GET /resumes/`: List master resumes.
- `GET /resumes/{id}`: Get master resume details.
- `POST /resumes/{id}/versions`: Create tailored resume variant.
- `GET /resumes/{id}/versions`: List tailored variants for resume.
- `GET /resumes/versions/{version_id}`: Get tailored variant details.

### 4. Pipeline Runs (`/pipelines`)
- `POST /pipelines/`: Trigger new job processing pipeline run.
- `GET /pipelines/`: List pipeline runs with filters.
- `GET /pipelines/{id}`: Get pipeline run execution history.
- `POST /pipelines/{id}/steps`: Record pipeline execution step.
- `PATCH /pipelines/{id}/status`: Update pipeline run status.

### 5. HITL Approvals (`/approvals`)
- `POST /approvals/`: Create HITL approval request.
- `GET /approvals/`: List approval requests.
- `GET /approvals/{id}`: Get approval request details.
- `PATCH /approvals/{id}`: Submit human reviewer decision (`APPROVED` or `REJECTED`).

### 6. Audit Events (`/events`)
- `POST /events/`: Log system audit event.
- `GET /events/`: Query audit event log by type/correlation.
- `GET /events/{event_id}`: Get audit event details.

### 7. Real-Time WebSockets (`/ws`)
- `WS /ws/pipeline/{pipeline_id}`: Stream real-time step progress for a specific pipeline.
- `WS /ws/notifications`: Global notification event stream.
