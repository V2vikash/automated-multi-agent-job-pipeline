import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_job_crud_and_keyword_operations(async_client: AsyncClient):
    # 1. Create Job
    job_payload = {
        "external_id": "job-101",
        "title": "Senior Python Engineer",
        "company": "Acme Software",
        "location": "Remote",
        "url": "https://example.com/jobs/101",
        "description": "Looking for Python and FastAPI expert.",
        "source": "linkedin"
    }
    create_resp = await async_client.post("/api/v1/jobs/", json=job_payload)
    assert create_resp.status_code == 201
    job_data = create_resp.json()
    assert job_data["title"] == "Senior Python Engineer"
    job_id = job_data["id"]

    # 2. Duplicate External ID Conflict
    dup_resp = await async_client.post("/api/v1/jobs/", json=job_payload)
    assert dup_resp.status_code == 409

    # 3. Add Job Keyword
    kw_payload = {
        "keyword": "FastAPI",
        "normalized_keyword": "fastapi",
        "category": "framework",
        "source": "aho_corasick",
        "confidence": 0.95
    }
    kw_resp = await async_client.post(f"/api/v1/jobs/{job_id}/keywords", json=kw_payload)
    assert kw_resp.status_code == 201
    assert kw_resp.json()["normalized_keyword"] == "fastapi"

    # 4. Get Job with Keywords
    get_resp = await async_client.get(f"/api/v1/jobs/{job_id}")
    assert get_resp.status_code == 200
    retrieved = get_resp.json()
    assert len(retrieved["job_keywords"]) == 1
    assert retrieved["job_keywords"][0]["keyword"] == "FastAPI"

    # 5. List Jobs with Filter
    list_resp = await async_client.get("/api/v1/jobs/?company=Acme&source=linkedin")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    # 6. Delete Job
    del_resp = await async_client.delete(f"/api/v1/jobs/{job_id}")
    assert del_resp.status_code == 204
