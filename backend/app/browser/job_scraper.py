import asyncio
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import logger
from app.browser.playwright_manager import playwright_manager
from app.browser.parsers.base_parser import ScrapedJob
from app.browser.parsers.generic_parser import generic_job_parser
from app.database.models.job import Job


class JobScraper:
    """Scrapes job information using Playwright with retry handling and local mock fallback."""

    def __init__(self, max_retries: int = 3, timeout_ms: int = 15000):
        self.max_retries = max_retries
        self.timeout_ms = timeout_ms

    async def scrape_url(self, url: str) -> ScrapedJob:
        """Scrape structured job posting from a target URL with retries."""
        context = await playwright_manager.new_context()
        if not context:
            logger.info("Playwright browser unavailable. Using mock discovery mode.")
            return self.scrape_sample_job(url)

        last_error = None
        for attempt in range(1, self.max_retries + 1):
            page = None
            try:
                page = await context.new_page()
                await page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_ms)
                content = await page.content()
                await page.close()
                await context.close()

                scraped = generic_job_parser.parse_html(content, url)
                logger.info(f"Successfully scraped job '{scraped.title}' from {url} on attempt {attempt}")
                return scraped
            except Exception as e:
                last_error = e
                logger.warning(f"Scrape attempt {attempt}/{self.max_retries} failed for {url}: {e}")
                if page:
                    try:
                        await page.close()
                    except Exception:
                        pass
                await asyncio.sleep(1)

        try:
            await context.close()
        except Exception:
            pass

        logger.error(f"All scrape retries exhausted for {url}. Falling back to sample parser.")
        return self.scrape_sample_job(url)

    def scrape_sample_job(self, url: str = "https://careers.example.com/jobs/dev-501") -> ScrapedJob:
        """Deterministic mock sample job discovery for local testing."""
        if url == "invalid":
            return ScrapedJob(
                title="",
                company="",
                location="",
                url="invalid",
                description="",
                source="mock_discovery",
                external_id="invalid"
            )

        return ScrapedJob(
            title="Senior Backend & Distributed Systems Engineer",
            company="Enterprise AI Systems",
            location="San Francisco, CA (Hybrid)",
            url=url,
            description=(
                "Enterprise AI Systems is seeking a Senior Backend Engineer. "
                "Required skills: Python, FastAPI, PostgreSQL, Apache Kafka, Redis, "
                "Docker, LangGraph, Playwright, Pytest, and LaTeX resume rendering. "
                "Responsibilities include building high-throughput microservices and event pipelines."
            ),
            source="mock_discovery",
            external_id="dev-501"
        )

    async def save_job_to_db(self, db: AsyncSession, scraped: ScrapedJob) -> Job:
        """Persist scraped job in PostgreSQL, preventing duplicate records."""
        if scraped.external_id:
            stmt = select(Job).where(
                Job.source == scraped.source,
                Job.external_id == scraped.external_id
            )
            res = await db.execute(stmt)
            existing = res.scalar_one_or_none()
            if existing:
                logger.info(f"Existing job '{existing.id}' found for source={scraped.source}, external_id={scraped.external_id}")
                return existing

        job = Job(
            external_id=scraped.external_id,
            title=scraped.title,
            company=scraped.company,
            location=scraped.location,
            url=scraped.url,
            description=scraped.description,
            source=scraped.source
        )
        db.add(job)
        await db.flush()
        await db.refresh(job)
        logger.info(f"Persisted new job '{job.id}' in database.")
        return job


job_scraper = JobScraper()
