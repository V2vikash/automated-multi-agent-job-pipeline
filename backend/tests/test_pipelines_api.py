import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_pipeline_runs_and_steps_api(async_client: AsyncClient):
    # Setup User and Job
    u_resp = await async_client.post("/api/v1/users/", json={"name": "Bob", "email": "bob@example.com"})
    user_id = u_resp.json()["id"]

    j_resp = await async_client.post("/api/v1/jobs/", json={
        "title": "DevOps Lead", "company": "CloudInc", "description": "K8s & CI/CD", "source": "linkedin"
    })
    job_id = j_resp.json()["id"]

    # 1. Create Pipeline Run
    run_payload = {
        "user_id": user_id,
        "job_id": job_id,
        "correlation_id": "corr-uuid-9999",
        "status": "pending",
        "current_step": "init"
    }
    create_run_resp = await async_client.post("/api/v1/pipelines/", json=run_payload)
    assert create_run_resp.status_code == 201
    run_data = create_run_resp.json()
    run_id = run_data["id"]

    # 2. Duplicate Correlation ID Conflict
    dup_resp = await async_client.post("/api/v1/pipelines/", json=run_payload)
    assert dup_resp.status_code == 409

    # 3. Add Pipeline Step
    step_payload = {
        "step_name": "keyword_matching",
        "status": "completed",
        "attempt": 1,
        "metadata": {"matched_count": 12}
    }
    step_resp = await async_client.post(f"/api/v1/pipelines/{run_id}/steps", json=step_payload)
    assert step_resp.status_code == 201
    assert step_resp.json()["step_name"] == "keyword_matching"

    # 4. Get Pipeline Run Details with Steps
    get_run_resp = await async_client.get(f"/api/v1/pipelines/{run_id}")
    assert get_run_resp.status_code == 200
    run_details = get_run_resp.json()
    assert run_details["current_step"] == "keyword_matching"
    assert len(run_details["steps"]) == 1

    # 5. Patch Pipeline Status
    patch_resp = await async_client.patch(f"/api/v1/pipelines/{run_id}/status?status=completed")
    assert patch_resp.status_code == 200
    assert patch_resp.json()["status"] == "completed"

    # 6. List Pipeline Runs by Filter
    list_resp = await async_client.get(f"/api/v1/pipelines/?status=completed&user_id={user_id}")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1
