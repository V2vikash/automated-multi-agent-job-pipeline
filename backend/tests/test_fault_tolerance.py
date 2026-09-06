import pytest
from app.browser.job_scraper import JobScraper
from app.kafka.producer import KafkaProducerManager
from app.kafka.events import EventEnvelope
from app.resume.pdf_compiler import PDFCompiler
from app.workflows.graph import job_pipeline_graph
from app.workflows.state import PipelineState


@pytest.mark.asyncio
async def test_browser_failure_fallback_mode():
    """Verify scraper handles invalid/offline URLs gracefully via fallback."""
    scraper = JobScraper(max_retries=1, timeout_ms=500)
    scraped = await scraper.scrape_url("http://invalid-non-existent-domain-999.xyz/job")
    assert scraped is not None
    assert scraped.company is not None


@pytest.mark.asyncio
async def test_kafka_producer_offline_resilience():
    """Verify Kafka producer handles missing broker gracefully without crashing."""
    producer = KafkaProducerManager(bootstrap_servers="localhost:9999")
    evt = EventEnvelope(
        event_type="test.resilience",
        correlation_id="corr-res-1",
        payload={"data": "sample"}
    )
    success = await producer.send_event("test.resilience", evt)
    assert success is True
    assert len(producer.get_published_events()) == 1


def test_pdf_compiler_invalid_latex_handling():
    """Verify PDF compiler captures errors cleanly on invalid markup."""
    compiler = PDFCompiler()
    success, path, err = compiler.compile_latex("invalid text without document tag")
    assert success is False
    assert err is not None


@pytest.mark.asyncio
async def test_pipeline_recovery_and_step_tracing():
    """Verify pipeline state is preserved on failure step."""
    initial_state: PipelineState = {
        "pipeline_id": "pipe-res-999",
        "correlation_id": "corr-res-999",
        "job_url": "invalid",
        "status": "PENDING"
    }
    state = await job_pipeline_graph.ainvoke(initial_state)
    assert state["status"] == "FAILED"
    assert state["current_step"] == "validate_job"
