import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_root_health_endpoint():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "job-intelligence-platform"


@pytest.mark.asyncio
async def test_v1_health_endpoint():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "job-intelligence-platform"
    assert data["version"] == "v1"


@pytest.mark.asyncio
async def test_v1_health_endpoint_kafka_offline(monkeypatch):
    """Verify v1 health check handles offline Kafka gracefully."""
    async def mock_offline_kafka():
        return False

    async def mock_online_db():
        return True

    monkeypatch.setattr("app.api.v1.health.check_kafka_health", mock_offline_kafka)
    monkeypatch.setattr("app.api.v1.health.check_db_health", mock_online_db)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/health")

    assert response.status_code == 200
    data = response.json()
    assert data["kafka"] == "offline"
    assert data["database"] == "online"
    assert data["status"] == "ok"

