import logging
import sys
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [keyword_worker] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("keyword_worker")


def main():
    logger.info("keyword_worker started")
    # Placeholder loop for future Kafka keyword extraction consumer execution in Phase 3
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("keyword_worker shutting down")


if __name__ == "__main__":
    main()
