from typing import List, Union
from pydantic import Field, AliasChoices, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = Field(default="Job Intelligence Platform", description="Application Name")
    APP_ENV: str = Field(default="development", description="Application Environment")
    LOG_LEVEL: str = Field(default="INFO", description="Logging Level")
    SECRET_KEY: str = Field(default="dev-secret-key-change-in-production-32-chars", description="Secret Key")

    HOST: str = Field(default="0.0.0.0", description="Server Host")
    PORT: int = Field(default=8000, description="Server Port")

    # Security / CORS
    CORS_ORIGINS: Union[List[str], str] = Field(
        default=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
        description="Allowed CORS origins"
    )

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/job_intelligence_db",
        description="Database Connection URL"
    )

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = Field(
        default="localhost:9092",
        validation_alias=AliasChoices(
            "KAFKA_BOOTSTRAP_SERVERS",
            "KAFKA_BOOTSTRAP_SERVER",
            "KAFKA_URL",
            "KAFKA_BROKER_URL",
            "KAFKA_SERVERS",
            "kafka_bootstrap_servers",
            "kafka_bootstrap_server",
        ),
        description="Kafka Bootstrap Servers"
    )
    KAFKA_CLIENT_ID: str = Field(
        default="job-intelligence-platform",
        description="Kafka Client Identifier"
    )

    # Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis Connection URL"
    )

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def validate_database_url(cls, v: Union[str, None]) -> str:
        if isinstance(v, str):
            if v.startswith("postgres://"):
                return v.replace("postgres://", "postgresql+asyncpg://", 1)
            elif v.startswith("postgresql://"):
                return v.replace("postgresql://", "postgresql+asyncpg://", 1)
            elif v.startswith("postgres+asyncpg://"):
                return v.replace("postgres+asyncpg://", "postgresql+asyncpg://", 1)
            elif v.startswith("postgresql+psycopg2://"):
                return v.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)
            elif v.startswith("postgresql+psycopg://"):
                return v.replace("postgresql+psycopg://", "postgresql+asyncpg://", 1)
        return v

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                import json
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True
    )


settings = Settings()
