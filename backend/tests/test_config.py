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


def test_kafka_bootstrap_servers_configuration():
    s_default = Settings()
    assert s_default.KAFKA_BOOTSTRAP_SERVERS == "localhost:9092"

    s_custom = Settings(KAFKA_BOOTSTRAP_SERVERS="kafka-prod.internal:9092")
    assert s_custom.KAFKA_BOOTSTRAP_SERVERS == "kafka-prod.internal:9092"

    s_alias = Settings(KAFKA_BOOTSTRAP_SERVER="kafka-server.internal:9092")
    assert s_alias.KAFKA_BOOTSTRAP_SERVERS == "kafka-server.internal:9092"


