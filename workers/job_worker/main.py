import logging
import sys
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [job_worker] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("job_worker")


def main():
    logger.info("job_worker started")
    # Placeholder loop for future Kafka event consumer execution in Phase 3
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("job_worker shutting down")


if __name__ == "__main__":
    main()
