from app.core.logging import logger
from app.workflows.state import PipelineState
from app.kafka.producer import kafka_producer
from app.kafka.events import EventEnvelope
from app.kafka.topics import KafkaTopics


async def request_human_approval(state: PipelineState) -> PipelineState:
    """LangGraph node: Pause workflow and emit HITL approval.requested event."""
    logger.info(f"Executing workflow step 'request_human_approval' for pipeline '{state.get('pipeline_id')}'")

    approval_status = state.get("approval_status") or "PENDING"

    evt = EventEnvelope(
        event_type=KafkaTopics.APPROVAL_REQUESTED.value,
        correlation_id=state.get("correlation_id", "corr-unknown"),
        pipeline_id=state.get("pipeline_id"),
        payload={
            "job_title": state.get("job_title"),
            "company": state.get("company"),
            "approval_status": approval_status
        }
    )
    await kafka_producer.send_event(KafkaTopics.APPROVAL_REQUESTED.value, evt)

    return {
        **state,
        "approval_status": approval_status,
        "current_step": "request_human_approval",
        "status": "IN_PROGRESS"
    }


async def wait_for_approval(state: PipelineState) -> PipelineState:
    """LangGraph node: Check human reviewer approval state."""
    logger.info(f"Executing workflow step 'wait_for_approval' for pipeline '{state.get('pipeline_id')}'")
    return {
        **state,
        "current_step": "wait_for_approval"
    }


async def complete_pipeline(state: PipelineState) -> PipelineState:
    """LangGraph node: Finalize pipeline execution upon approval."""
    logger.info(f"Executing workflow step 'complete_pipeline' for pipeline '{state.get('pipeline_id')}'")

    evt = EventEnvelope(
        event_type=KafkaTopics.PIPELINE_COMPLETED.value,
        correlation_id=state.get("correlation_id", "corr-unknown"),
        pipeline_id=state.get("pipeline_id"),
        payload={"status": "COMPLETED", "job_title": state.get("job_title")}
    )
    await kafka_producer.send_event(KafkaTopics.PIPELINE_COMPLETED.value, evt)

    return {
        **state,
        "current_step": "complete_pipeline",
        "status": "COMPLETED"
    }
