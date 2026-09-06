from app.core.logging import logger
from app.workflows.state import PipelineState
from app.kafka.producer import kafka_producer
from app.kafka.events import EventEnvelope
from app.kafka.topics import KafkaTopics


async def process_candidate_resume(state: PipelineState) -> PipelineState:
    """LangGraph node: Parse master resume content for candidate."""
    logger.info(f"Executing workflow step 'process_candidate_resume' for pipeline '{state.get('pipeline_id')}'")
    resume_content = state.get("resume_content") or (
        "John Doe - Senior Software Engineer\n"
        "Experience: 6 years building distributed Python web APIs, PostgreSQL databases, and Docker microservices.\n"
        "Skills: Python, FastAPI, PostgreSQL, Docker, Git, CI/CD, Pytest."
    )

    return {
        **state,
        "resume_content": resume_content,
        "current_step": "process_candidate_resume",
        "status": "IN_PROGRESS"
    }


async def generate_tailored_resume(state: PipelineState) -> PipelineState:
    """LangGraph node: Tailor resume bullet points using target job keywords."""
    logger.info(f"Executing workflow step 'generate_tailored_resume' for pipeline '{state.get('pipeline_id')}'")
    keywords = state.get("keyword_results") or ["Python", "FastAPI", "PostgreSQL"]
    base_resume = state.get("resume_content") or "Candidate Master Resume"

    kw_summary = ", ".join(keywords)
    tailored_text = (
        f"{base_resume}\n\n"
        f"[TAILORED RELEVANCE HIGHLIGHTS FOR {state.get('job_title', 'TARGET ROLE')}]\n"
        f"Demonstrated mastery aligned with key job requirements: {kw_summary}."
    )

    evt = EventEnvelope(
        event_type=KafkaTopics.RESUME_GENERATED.value,
        correlation_id=state.get("correlation_id", "corr-unknown"),
        pipeline_id=state.get("pipeline_id"),
        payload={"job_title": state.get("job_title"), "keywords_applied": len(keywords)}
    )
    await kafka_producer.send_event(KafkaTopics.RESUME_GENERATED.value, evt)

    return {
        **state,
        "tailored_resume_content": tailored_text,
        "current_step": "generate_tailored_resume",
        "status": "IN_PROGRESS"
    }


async def validate_generated_resume(state: PipelineState) -> PipelineState:
    """LangGraph node: Validate generated tailored resume integrity."""
    logger.info(f"Executing workflow step 'validate_generated_resume' for pipeline '{state.get('pipeline_id')}'")
    tailored = state.get("tailored_resume_content")

    if not tailored or len(tailored.strip()) < 20:
        logger.error(f"Tailored resume validation failed for pipeline '{state.get('pipeline_id')}'")
        return {
            **state,
            "status": "FAILED",
            "current_step": "validate_generated_resume",
            "error_message": "Empty or truncated tailored resume output"
        }

    return {
        **state,
        "current_step": "validate_generated_resume",
        "status": "IN_PROGRESS"
    }
