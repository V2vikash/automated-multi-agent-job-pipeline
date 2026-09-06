from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class ScrapedJob(BaseModel):
    """Normalized structured job data extracted by Playwright scraper."""
    title: str = Field(..., max_length=255)
    company: str = Field(..., max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    url: Optional[str] = None
    description: str
    source: str = Field(default="web_scraper", max_length=100)
    external_id: Optional[str] = Field(None, max_length=255)


class BaseJobParser(ABC):
    """Abstract base class for site-specific job page parsers."""

    @abstractmethod
    def parse_html(self, html_content: str, url: str) -> ScrapedJob:
        """Parse raw HTML string into structured ScrapedJob object."""
        pass
