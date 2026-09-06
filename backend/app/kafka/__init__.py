from typing import Optional
from app.core.config import settings
from app.core.logging import logger
from app.kafka.topics import KafkaTopics
from app.kafka.events import EventEnvelope
from app.kafka.producer import KafkaProducerManager, kafka_producer
from app.kafka.consumer import KafkaConsumerManager, kafka_consumer


async def check_kafka_health() -> bool:
    """Check Kafka broker connectivity for system health checks."""
    try:
        from aiokafka import AIOKafkaProducer
        producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            request_timeout_ms=3000
        )
        await producer.start()
        await producer.stop()
        return True
    except Exception as e:
        logger.debug(f"Kafka health check unavailable: {e}")
        return False


__all__ = [
    "KafkaTopics",
    "EventEnvelope",
    "KafkaProducerManager",
    "kafka_producer",
    "KafkaConsumerManager",
    "kafka_consumer",
    "check_kafka_health",
]
