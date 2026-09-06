import logging
import sys
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [resume_worker] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("resume_worker")


def main():
    logger.info("resume_worker started")
    # Placeholder loop for future LaTeX generation worker execution in Phase 7
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("resume_worker shutting down")


if __name__ == "__main__":
    main()
