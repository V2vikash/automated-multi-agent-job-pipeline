from datetime import datetime, timezone
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_approvals_api(async_client: AsyncClient):
    # Setup User, Job, Resume, ResumeVersion, and PipelineRun
    u_resp = await async_client.post("/api/v1/users/", json={"name": "Charlie", "email": "charlie@example.com"})
    user_id = u_resp.json()["id"]

    j_resp = await async_client.post("/api/v1/jobs/", json={"title": "QA", "company": "TestCorp", "description": "QA Lead", "source": "direct"})
    job_id = j_resp.json()["id"]

    r_resp = await async_client.post("/api/v1/resumes/", json={"user_id": user_id, "title": "QA Resume"})
    resume_id = r_resp.json()["id"]

    v_resp = await async_client.post(f"/api/v1/resumes/{resume_id}/versions", json={"resume_id": resume_id, "job_id": job_id, "version_number": 1})
    version_id = v_resp.json()["id"]

    p_resp = await async_client.post("/api/v1/pipelines/", json={"user_id": user_id, "job_id": job_id, "correlation_id": "corr-app-1"})
    pipeline_id = p_resp.json()["id"]

    # 1. Create HITL Approval Request
    now_iso = datetime.now(timezone.utc).isoformat()
    app_payload = {
        "pipeline_run_id": pipeline_id,
        "resume_version_id": version_id,
        "status": "pending",
        "requested_at": now_iso
    }
    create_app_resp = await async_client.post("/api/v1/approvals/", json=app_payload)
    assert create_app_resp.status_code == 201
    approval_data = create_app_resp.json()
    approval_id = approval_data["id"]

    # Verify pipeline run status transitioned to waiting_approval
    p_check = await async_client.get(f"/api/v1/pipelines/{pipeline_id}")
    assert p_check.json()["status"] == "waiting_approval"

    # 2. List Approvals by Status
    list_resp = await async_client.get("/api/v1/approvals/?status=pending")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    # 3. Submit Decision: Approved
    patch_resp = await async_client.patch(f"/api/v1/approvals/{approval_id}?decision=approved&reviewer_note=Looks%20great!")
    assert patch_resp.status_code == 200
    assert patch_resp.json()["status"] == "approved"
    assert patch_resp.json()["reviewer_note"] == "Looks great!"

    # Verify pipeline run resumed to running
    p_check_after = await async_client.get(f"/api/v1/pipelines/{pipeline_id}")
    assert p_check_after.json()["status"] == "running"
