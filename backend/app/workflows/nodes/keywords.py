from app.core.logging import logger
from app.workflows.state import PipelineState
from app.keyword_engine.aho_corasick import keyword_automaton
from app.kafka.producer import kafka_producer
from app.kafka.events import EventEnvelope
from app.kafka.topics import KafkaTopics


async def extract_keywords(state: PipelineState) -> PipelineState:
    """LangGraph node: Extract tech keywords via Aho-Corasick Engine."""
    logger.info(f"Executing workflow step 'extract_keywords' for pipeline '{state.get('pipeline_id')}'")
    desc = state.get("job_description") or ""

    extracted = keyword_automaton.search(desc)
    keyword_list = [k.keyword for k in extracted]

    evt = EventEnvelope(
        event_type=KafkaTopics.KEYWORDS_EXTRACTED.value,
        correlation_id=state.get("correlation_id", "corr-unknown"),
        pipeline_id=state.get("pipeline_id"),
        payload={"keywords": keyword_list, "count": len(keyword_list)}
    )
    await kafka_producer.send_event(KafkaTopics.KEYWORDS_EXTRACTED.value, evt)

    return {
        **state,
        "keyword_results": keyword_list,
        "current_step": "extract_keywords",
        "status": "IN_PROGRESS"
    }
