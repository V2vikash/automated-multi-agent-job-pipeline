import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.browser.parsers.generic_parser import generic_job_parser
from app.browser.job_scraper import job_scraper, JobScraper


def test_generic_job_parser_html_extraction():
    """Test HTML parsing and sanitization for scraped jobs."""
    raw_html = """
    <html>
        <head><title>Staff Software Engineer - AI Platforms | Acme Cloud</title></head>
        <body>
            <div class="company">Acme Cloud Systems</div>
            <div class="location">New York, NY</div>
            <article>
                <p>We are seeking a Staff Engineer to build distributed Python & Kafka microservices.</p>
            </article>
        </body>
    </html>
    """
    scraped = generic_job_parser.parse_html(raw_html, "https://careers.acme.com/jobs/view/staff-99")
    assert scraped.title == "Staff Software Engineer - AI Platforms"
    assert scraped.company == "Acme Cloud Systems"
    assert scraped.location == "New York, NY"
    assert "Python & Kafka" in scraped.description
    assert scraped.external_id == "staff-99"
    assert scraped.source == "playwright_discovery"


def test_sample_job_discovery_mode():
    """Test deterministic mock sample job discovery."""
    scraper = JobScraper()
    scraped = scraper.scrape_sample_job("https://example.com/test-job")
    assert scraped.title is not None
    assert scraped.company == "Enterprise AI Systems"
    assert "Kafka" in scraped.description
    assert scraped.external_id == "dev-501"


@pytest.mark.asyncio
async def test_save_job_to_db_and_deduplication(db_session: AsyncSession):
    """Test saving scraped job to database and duplicate prevention."""
    scraped = job_scraper.scrape_sample_job("https://example.com/job-1")

    # First Save
    job1 = await job_scraper.save_job_to_db(db_session, scraped)
    assert job1.id is not None
    assert job1.company == "Enterprise AI Systems"

    # Second Save with same external_id and source -> returns existing instance
    job2 = await job_scraper.save_job_to_db(db_session, scraped)
    assert job2.id == job1.id
