import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_events_api(async_client: AsyncClient):
    # 1. Log Event
    event_payload = {
        "event_id": "evt-001-abc",
        "event_type": "job_discovered",
        "correlation_id": "corr-evt-100",
        "payload": {"source": "linkedin", "title": "AI Engineer"},
        "status": "pending"
    }
    create_resp = await async_client.post("/api/v1/events/", json=event_payload)
    assert create_resp.status_code == 201
    evt_data = create_resp.json()
    assert evt_data["event_id"] == "evt-001-abc"

    # 2. Duplicate Event ID Conflict
    dup_resp = await async_client.post("/api/v1/events/", json=event_payload)
    assert dup_resp.status_code == 409

    # 3. Get Event by event_id
    get_resp = await async_client.get("/api/v1/events/evt-001-abc")
    assert get_resp.status_code == 200
    assert get_resp.json()["event_type"] == "job_discovered"

    # 4. List Events with Filters
    list_resp = await async_client.get("/api/v1/events/?event_type=job_discovered&correlation_id=corr-evt-100")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1
