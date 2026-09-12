from app.core.config import Settings


def test_settings_defaults():
    settings = Settings()
    assert settings.APP_NAME == "Job Intelligence Platform"
    assert settings.APP_ENV in ["development", "testing", "production"]
    assert isinstance(settings.CORS_ORIGINS, list)
    assert len(settings.CORS_ORIGINS) > 0


def test_cors_origins_parsing():
    settings = Settings(CORS_ORIGINS="http://localhost:5173,http://localhost:3000")
    assert settings.CORS_ORIGINS == ["http://localhost:5173", "http://localhost:3000"]


def test_database_url_normalization():
    s1 = Settings(DATABASE_URL="postgres://user:pass@localhost:5432/testdb")
    assert s1.DATABASE_URL == "postgresql+asyncpg://user:pass@localhost:5432/testdb"

    s2 = Settings(DATABASE_URL="postgresql://user:pass@localhost:5432/testdb")
    assert s2.DATABASE_URL == "postgresql+asyncpg://user:pass@localhost:5432/testdb"

    s3 = Settings(DATABASE_URL="postgresql+psycopg2://user:pass@localhost:5432/testdb")
    assert s3.DATABASE_URL == "postgresql+asyncpg://user:pass@localhost:5432/testdb"

