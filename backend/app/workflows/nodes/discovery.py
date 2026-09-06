from app.core.logging import logger
from app.workflows.state import PipelineState
from app.browser.job_scraper import job_scraper
from app.kafka.producer import kafka_producer
from app.kafka.events import EventEnvelope
from app.kafka.topics import KafkaTopics


async def discover_job(state: PipelineState) -> PipelineState:
    """LangGraph node: Discover/scrape job posting via Playwright."""
    logger.info(f"Executing workflow step 'discover_job' for pipeline '{state.get('pipeline_id')}'")
    job_url = state.get("job_url") or "https://careers.example.com/jobs/dev-501"

    scraped = await job_scraper.scrape_url(job_url)

    # Emit Kafka event
    evt = EventEnvelope(
        event_type=KafkaTopics.JOBS_DISCOVERED.value,
        correlation_id=state.get("correlation_id", "corr-unknown"),
        pipeline_id=state.get("pipeline_id"),
        payload={
            "title": scraped.title,
            "company": scraped.company,
            "url": scraped.url,
            "source": scraped.source
        }
    )
    await kafka_producer.send_event(KafkaTopics.JOBS_DISCOVERED.value, evt)

    return {
        **state,
        "job_title": scraped.title,
        "company": scraped.company,
        "job_description": scraped.description,
        "current_step": "discover_job",
        "status": "IN_PROGRESS"
    }
