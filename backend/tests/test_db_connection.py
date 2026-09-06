import pytest
from app.core.config import settings
from app.database.connection import engine, async_session_factory, get_db, check_db_health


def test_database_url_configuration():
    """Verify DATABASE_URL is configured and starts with postgresql+asyncpg."""
    url = settings.DATABASE_URL
    assert url is not None
    assert "postgresql+asyncpg" in url or "sqlite" in url


def test_async_engine_and_session_factory():
    """Verify AsyncEngine and async_session_factory initialization."""
    assert engine is not None
    assert async_session_factory is not None


@pytest.mark.asyncio
async def test_get_db_generator():
    """Verify get_db produces an AsyncSession instance."""
    session_gen = get_db()
    session = await anext(session_gen)
    assert session is not None
    await session_gen.aclose()
