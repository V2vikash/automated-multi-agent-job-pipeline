from enum import Enum


class KafkaTopics(str, Enum):
    JOBS_DISCOVERED = "jobs.discovered"
    JOBS_PROCESSING = "jobs.processing"
    JOBS_PROCESSED = "jobs.processed"
    KEYWORDS_EXTRACTED = "keywords.extracted"
    RESUME_REQUESTED = "resume.requested"
    RESUME_GENERATED = "resume.generated"
    APPROVAL_REQUESTED = "approval.requested"
    APPROVAL_COMPLETED = "approval.completed"
    PIPELINE_COMPLETED = "pipeline.completed"
    PIPELINE_FAILED = "pipeline.failed"
