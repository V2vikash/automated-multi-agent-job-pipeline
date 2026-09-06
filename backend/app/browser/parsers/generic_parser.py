import re
import html
from typing import Optional
from app.browser.parsers.base_parser import BaseJobParser, ScrapedJob


class GenericJobParser(BaseJobParser):
    """Generic fallback parser for untrusted web job postings."""

    def parse_html(self, html_content: str, url: str) -> ScrapedJob:
        # Sanitize HTML tags for text extraction
        clean_text = self._strip_tags(html_content)

        # Extract Title
        title_match = re.search(r"<title>(.*?)</title>", html_content, re.IGNORECASE | re.DOTALL)
        title = title_match.group(1).strip() if title_match else "Software Engineer"
        title = html.unescape(title)
        # Remove common site suffix like "| LinkedIn" or " - Company"
        title = re.sub(r"\s*\|\s*.*$", "", title).strip() or "Software Engineer"

        # Extract Company
        company_match = re.search(r'class=["\'](?:company|employer)["\'][^>]*>(.*?)</div>', html_content, re.IGNORECASE)
        company = company_match.group(1).strip() if company_match else "Target Company"
        company = html.unescape(self._strip_tags(company)) or "Target Company"

        # Extract Location
        loc_match = re.search(r'class=["\'](?:location|job-location)["\'][^>]*>(.*?)</div>', html_content, re.IGNORECASE)
        location = loc_match.group(1).strip() if loc_match else "Remote"
        location = html.unescape(self._strip_tags(location)) or "Remote"

        # Extract Description
        desc_match = re.search(r'<article[^>]*>(.*?)</article>', html_content, re.IGNORECASE | re.DOTALL)
        if desc_match:
            desc_text = desc_match.group(1)
        else:
            desc_text = clean_text

        desc_clean = html.unescape(self._strip_tags(desc_text)).strip()
        if len(desc_clean) < 20:
            desc_clean = f"Job Posting Description for {title} at {company}. Key requirements: Python, FastAPI, PostgreSQL, Distributed Systems."

        # Extract External ID from URL if present
        ext_match = re.search(r'/jobs/(?:view/)?([a-zA-Z0-9_-]+)', url)
        external_id = ext_match.group(1) if ext_match else None

        return ScrapedJob(
            title=title[:255],
            company=company[:255],
            location=location[:255],
            url=url,
            description=desc_clean,
            source="playwright_discovery",
            external_id=external_id
        )

    def _strip_tags(self, text: str) -> str:
        """Strip HTML tags safely."""
        return re.sub(r"<[^>]+>", " ", text)


generic_job_parser = GenericJobParser()
