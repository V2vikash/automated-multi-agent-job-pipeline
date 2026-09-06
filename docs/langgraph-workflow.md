# LangGraph Workflow Architecture — Job Intelligence Platform

## Stateful StateGraph Workflow
The job orchestration system uses **LangGraph** (`StateGraph`) for stateful execution tracking and conditional routing.

```
START
  ↓
discover_job
  ↓
validate_job (Conditional: FAILED -> END)
  ↓
process_job
  ↓
extract_keywords
  ↓
process_candidate_resume
  ↓
generate_tailored_resume
  ↓
validate_generated_resume (Conditional: FAILED -> END)
  ↓
request_human_approval
  ↓
wait_for_approval
  ↓
approval_router
  ├── REJECT → END
  └── APPROVE → complete_pipeline → END
```

## State Schema (`PipelineState`)
- `pipeline_id`: Unique identifier for the pipeline run.
- `correlation_id`: Correlation identifier for event tracing across microservices.
- `job_url`: Target job posting URL.
- `job_title`: Extracted role title.
- `company`: Employer company name.
- `job_description`: Full job description text.
- `keyword_results`: List of extracted tech keywords (Aho-Corasick).
- `resume_content`: Master resume text.
- `tailored_resume_content`: Customized resume text.
- `approval_status`: `PENDING`, `APPROVED`, or `REJECTED`.
- `current_step`: Active node step name.
- `status`: Overall status (`IN_PROGRESS`, `COMPLETED`, `FAILED`).
