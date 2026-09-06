import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from app.core.config import settings


class StructuredJSONFormatter(logging.Formatter):
    """
    Structured JSON log formatter for production and development logging.
    Formats logs with timestamp, level, service name, message, and extra contextual fields.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": settings.APP_NAME,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Extensible context fields for tracking request/pipeline flow across services
        for key in ("pipeline_id", "correlation_id", "event_id", "error"):
            if hasattr(record, key):
                log_data[key] = getattr(record, key)

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_logging() -> logging.Logger:
    """Configures structured application logging."""
    logger = logging.getLogger("job_platform")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(StructuredJSONFormatter())
        logger.addHandler(handler)

    return logger


logger = setup_logging()
