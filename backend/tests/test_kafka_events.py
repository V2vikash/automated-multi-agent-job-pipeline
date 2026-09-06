import pytest
from app.kafka.topics import KafkaTopics
from app.kafka.events import EventEnvelope
from app.kafka.producer import KafkaProducerManager
from app.kafka.consumer import KafkaConsumerManager


def test_event_envelope_validation():
    """Verify EventEnvelope fields and defaults."""
    evt = EventEnvelope(
        event_type=KafkaTopics.JOBS_DISCOVERED.value,
        correlation_id="corr-12345",
        pipeline_id="pipe-67890",
        payload={"url": "https://example.com/job/1"}
    )
    assert evt.event_id.startswith("evt-")
    assert evt.event_type == "jobs.discovered"
    assert evt.correlation_id == "corr-12345"
    assert evt.payload["url"] == "https://example.com/job/1"


@pytest.mark.asyncio
async def test_kafka_producer_and_consumer_dispatch():
    """Test producer sending events and consumer handler registration."""
    producer = KafkaProducerManager(bootstrap_servers="localhost:9092")
    consumer = KafkaConsumerManager()

    received_events = []

    async def sample_handler(event: EventEnvelope):
        received_events.append(event)

    consumer.register_handler(KafkaTopics.KEYWORDS_EXTRACTED.value, sample_handler)

    test_evt = EventEnvelope(
        event_type=KafkaTopics.KEYWORDS_EXTRACTED.value,
        correlation_id="corr-kw-100",
        payload={"keywords": ["Python", "FastAPI", "Kafka"]}
    )

    # 1. Send event
    success = await producer.send_event(KafkaTopics.KEYWORDS_EXTRACTED.value, test_evt)
    assert success is True
    assert len(producer.get_published_events()) == 1

    # 2. Dispatch event locally
    await consumer.dispatch_event(KafkaTopics.KEYWORDS_EXTRACTED.value, test_evt)
    assert len(received_events) == 1
    assert received_events[0].payload["keywords"] == ["Python", "FastAPI", "Kafka"]
