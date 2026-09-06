from app.core.logging import logger
from app.workflows.state import PipelineState
from app.kafka.producer import kafka_producer
from app.kafka.events import EventEnvelope
from app.kafka.topics import KafkaTopics


async def validate_job(state: PipelineState) -> PipelineState:
    """LangGraph node: Validate scraped job posting data integrity."""
    logger.info(f"Executing workflow step 'validate_job' for pipeline '{state.get('pipeline_id')}'")
    desc = state.get("job_description")
    title = state.get("job_title")

    if not desc or len(desc.strip()) < 10 or not title:
        logger.error(f"Job validation failed for pipeline '{state.get('pipeline_id')}'")
        return {
            **state,
            "status": "FAILED",
            "current_step": "validate_job",
            "error_message": "Invalid job description or missing title"
        }

    return {
        **state,
        "current_step": "validate_job",
        "status": "IN_PROGRESS"
    }


async def process_job(state: PipelineState) -> PipelineState:
    """LangGraph node: Process and structure raw job text."""
    logger.info(f"Executing workflow step 'process_job' for pipeline '{state.get('pipeline_id')}'")

    evt = EventEnvelope(
        event_type=KafkaTopics.JOBS_PROCESSED.value,
        correlation_id=state.get("correlation_id", "corr-unknown"),
        pipeline_id=state.get("pipeline_id"),
        payload={"job_title": state.get("job_title"), "company": state.get("company")}
    )
    await kafka_producer.send_event(KafkaTopics.JOBS_PROCESSED.value, evt)

    return {
        **state,
        "current_step": "process_job",
        "status": "IN_PROGRESS"
    }
