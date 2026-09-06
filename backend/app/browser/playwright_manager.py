import asyncio
from typing import Optional, Any
from app.core.logging import logger

try:
    from playwright.async_api import async_playwright, Playwright, Browser, BrowserContext, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Playwright = None
    Browser = None
    BrowserContext = None
    Page = None


class PlaywrightManager:
    """Manages Playwright browser lifecycle and contexts safely."""

    def __init__(self, headless: bool = True, timeout_ms: int = 30000):
        self.headless = headless
        self.timeout_ms = timeout_ms
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None

    async def initialize(self) -> bool:
        """Initialize Playwright and launch Chromium browser instance."""
        if not PLAYWRIGHT_AVAILABLE:
            logger.warning("Playwright is not installed. Browser discovery will operate in mock/sample mode.")
            return False

        try:
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(
                headless=self.headless,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
            )
            logger.info("Playwright Chromium browser initialized successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Playwright browser: {e}")
            await self.close()
            return False

    async def new_context(self) -> Optional[BrowserContext]:
        """Create a isolated browser context."""
        if not self._browser:
            return None
        context = await self._browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        context.set_default_timeout(self.timeout_ms)
        return context

    async def close(self):
        """Close browser instance and stop Playwright process cleanly."""
        if self._browser:
            try:
                await self._browser.close()
            except Exception as e:
                logger.error(f"Error closing browser: {e}")
            self._browser = None

        if self._playwright:
            try:
                await self._playwright.stop()
            except Exception as e:
                logger.error(f"Error stopping Playwright: {e}")
            self._playwright = None

        logger.info("Playwright manager shut down.")


playwright_manager = PlaywrightManager()
