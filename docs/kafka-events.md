# Kafka Event Specification — Job Intelligence Platform

## Overview
All asynchronous events in the system follow a standardized `EventEnvelope` format published over Apache Kafka topics.

## Event Envelope Format
```json
{
  "event_id": "evt-f0239b66-e3ab-4494-870d-c093ea64ced2",
  "event_type": "jobs.discovered",
  "timestamp": "2026-09-04T00:58:16.123456+00:00",
  "correlation_id": "corr-123456",
  "pipeline_id": "pipe-789012",
  "payload": {}
}
```

## Configured Event Topics
| Topic Name | Purpose | Producer | Consumers |
|---|---|---|---|
| `jobs.discovered` | Emitted when Playwright discovers a new job posting | Playwright Scraper | LangGraph Orchestrator |
| `jobs.processing` | Emitted when job text normalization starts | Orchestrator | Process Worker |
| `jobs.processed` | Emitted when raw job content is structured | Process Worker | Keyword Engine |
| `keywords.extracted` | Emitted when Aho-Corasick matches tech keywords | Aho-Corasick Engine | Resume Tailoring Service |
| `resume.requested` | Emitted when resume tailoring is requested | Orchestrator | Resume Tailoring Service |
| `resume.generated` | Emitted when LaTeX resume variant is compiled | Resume Generator | HITL Approval Service |
| `approval.requested` | Emitted when HITL human review is required | Orchestrator | WebSocket Gateway / UI |
| `approval.completed` | Emitted when human reviewer submits APPROVE/REJECT decision | Human Reviewer / API | Orchestrator |
| `pipeline.completed` | Emitted when pipeline run succeeds | Orchestrator | Notification Gateway |
| `pipeline.failed` | Emitted when pipeline run encounters unrecoverable error | Orchestrator | Notification Gateway |
