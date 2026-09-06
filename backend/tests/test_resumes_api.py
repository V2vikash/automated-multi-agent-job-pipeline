import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_resume_and_version_api(async_client: AsyncClient):
    # Setup User and Job
    user_resp = await async_client.post("/api/v1/users/", json={"name": "Alice", "email": "alice@example.com"})
    user_id = user_resp.json()["id"]

    job_resp = await async_client.post("/api/v1/jobs/", json={
        "title": "Backend Dev", "company": "Co", "description": "Desc", "source": "manual"
    })
    job_id = job_resp.json()["id"]

    # 1. Create Master Resume
    resume_payload = {
        "user_id": user_id,
        "title": "Software Engineer Master Resume",
        "original_filename": "resume.pdf",
        "storage_path": "uploads/resume.pdf",
        "parsed_content": {"skills": ["Python", "SQL"]}
    }
    create_resume_resp = await async_client.post("/api/v1/resumes/", json=resume_payload)
    assert create_resume_resp.status_code == 201
    resume_id = create_resume_resp.json()["id"]

    # 2. List Resumes
    list_res = await async_client.get(f"/api/v1/resumes/?user_id={user_id}")
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1

    # 3. Create Resume Version Variant
    version_payload = {
        "resume_id": resume_id,
        "job_id": job_id,
        "version_number": 1,
        "version_type": "tailored",
        "latex_source": "\\documentclass{article}\\begin{document}Resume\\end{document}",
        "status": "draft"
    }
    v_resp = await async_client.post(f"/api/v1/resumes/{resume_id}/versions", json=version_payload)
    assert v_resp.status_code == 201
    version_id = v_resp.json()["id"]

    # 4. List Resume Versions
    v_list_resp = await async_client.get(f"/api/v1/resumes/{resume_id}/versions")
    assert v_list_resp.status_code == 200
    assert len(v_list_resp.json()) == 1

    # 5. Get Resume Version by ID
    v_get = await async_client.get(f"/api/v1/resumes/versions/{version_id}")
    assert v_get.status_code == 200
    assert v_get.json()["id"] == version_id
