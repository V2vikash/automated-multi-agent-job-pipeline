import json
import asyncio
from typing import Callable, Dict, List, Optional, Awaitable
from app.core.config import settings
from app.core.logging import logger
from app.kafka.events import EventEnvelope

try:
    from aiokafka import AIOKafkaConsumer
    AIOKAFKA_AVAILABLE = True
except ImportError:
    AIOKAFKA_AVAILABLE = False
    AIOKafkaConsumer = None

EventHandler = Callable[[EventEnvelope], Awaitable[None]]


class KafkaConsumerManager:
    """Consumer abstraction for handling incoming Kafka topic events."""

    def __init__(self, group_id: str = "multi-agent-job-pipeline-consumer-group", bootstrap_servers: Optional[str] = None):
        self.group_id = group_id
        self._bootstrap_servers = bootstrap_servers
        self._consumer: Optional[AIOKafkaConsumer] = None
        self._handlers: Dict[str, List[EventHandler]] = {}
        self._running = False

    @property
    def bootstrap_servers(self) -> str:
        return self._bootstrap_servers or settings.KAFKA_BOOTSTRAP_SERVERS

    def register_handler(self, topic: str, handler: EventHandler):
        """Register an async event handler for a specific topic."""
        if topic not in self._handlers:
            self._handlers[topic] = []
        self._handlers[topic].append(handler)

    async def dispatch_event(self, topic: str, event: EventEnvelope):
        """Dispatch event envelope to registered handlers."""
        handlers = self._handlers.get(topic, [])
        for handler in handlers:
            try:
                await handler(event)
            except Exception as e:
                logger.error(f"Error executing handler for event '{event.event_id}' on topic '{topic}': {e}")

    async def start(self, topics: List[str]) -> bool:
        """Start consumer loop for target topics."""
        if not AIOKAFKA_AVAILABLE:
            logger.warning("aiokafka not installed. Consumer operating in mock mode.")
            return False

        try:
            self._consumer = AIOKafkaConsumer(
                *topics,
                bootstrap_servers=self.bootstrap_servers,
                group_id=self.group_id,
                value_deserializer=lambda v: json.loads(v.decode("utf-8")),
                auto_offset_reset="earliest"
            )
            await self._consumer.start()
            self._running = True
            logger.info(f"Kafka Consumer connected to '{self.bootstrap_servers}' for topics {topics}")
            return True
        except Exception as e:
            logger.warning(f"Unable to connect Kafka Consumer to '{self.bootstrap_servers}': {e}")
            self._consumer = None
            return False

    async def stop(self):
        """Stop consumer loop."""
        self._running = False
        if self._consumer:
            try:
                await self._consumer.stop()
            except Exception as e:
                logger.error(f"Error stopping Kafka consumer: {e}")
            self._consumer = None


kafka_consumer = KafkaConsumerManager()
