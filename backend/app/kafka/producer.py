import json
import asyncio
from typing import Optional, List
from app.core.config import settings
from app.core.logging import logger
from app.kafka.events import EventEnvelope

try:
    from aiokafka import AIOKafkaProducer
    AIOKAFKA_AVAILABLE = True
except ImportError:
    AIOKAFKA_AVAILABLE = False
    AIOKafkaProducer = None


class KafkaProducerManager:
    """Producer abstraction for publishing validated EventEnvelopes to Kafka."""

    def __init__(self, bootstrap_servers: Optional[str] = None):
        self.bootstrap_servers = bootstrap_servers or settings.KAFKA_BOOTSTRAP_SERVERS
        self._producer: Optional[AIOKafkaProducer] = None
        self._mock_published_events: List[EventEnvelope] = []

    async def start(self) -> bool:
        if not AIOKAFKA_AVAILABLE:
            logger.warning("aiokafka is not installed. Producer operating in mock mode.")
            return False

        try:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                client_id=settings.KAFKA_CLIENT_ID,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            await self._producer.start()
            logger.info(f"Kafka Producer connected to bootstrap servers: {self.bootstrap_servers}")
            return True
        except Exception as e:
            logger.warning(f"Unable to connect Kafka Producer to '{self.bootstrap_servers}': {e}. Operating in fallback mode.")
            self._producer = None
            return False

    async def send_event(self, topic: str, event: EventEnvelope) -> bool:
        """Publish an EventEnvelope to a specified Kafka topic."""
        self._mock_published_events.append(event)
        payload_bytes = json.dumps(event.model_dump()).encode("utf-8")

        if self._producer:
            try:
                await self._producer.send_and_wait(
                    topic,
                    value=event.model_dump(),
                    key=event.correlation_id.encode("utf-8") if event.correlation_id else None
                )
                logger.info(f"Published event '{event.event_id}' ({event.event_type}) to topic '{topic}'")
                return True
            except Exception as e:
                logger.error(f"Failed to publish event '{event.event_id}' to Kafka topic '{topic}': {e}")
                return False
        else:
            logger.info(f"[Mock Bus] Published event '{event.event_id}' ({event.event_type}) to topic '{topic}'")
            return True

    async def stop(self):
        """Stop Kafka producer instance."""
        if self._producer:
            try:
                await self._producer.stop()
            except Exception as e:
                logger.error(f"Error stopping Kafka producer: {e}")
            self._producer = None

    def get_published_events(self) -> List[EventEnvelope]:
        """Return list of published events (for unit testing and verification)."""
        return list(self._mock_published_events)

    def clear_published_events(self):
        """Clear mock event list."""
        self._mock_published_events.clear()


kafka_producer = KafkaProducerManager()
