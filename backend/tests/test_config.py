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
