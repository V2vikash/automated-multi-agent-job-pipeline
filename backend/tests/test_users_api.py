import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_user_crud_operations(async_client: AsyncClient):
    # 1. Create User
    user_payload = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "phone": "+1987654321"
    }
    create_resp = await async_client.post("/api/v1/users/", json=user_payload)
    assert create_resp.status_code == 201
    created_data = create_resp.json()
    assert created_data["name"] == "Jane Doe"
    assert created_data["email"] == "jane@example.com"
    user_id = created_data["id"]

    # 2. Duplicate Email Conflict
    dup_resp = await async_client.post("/api/v1/users/", json=user_payload)
    assert dup_resp.status_code == 409

    # 3. List Users
    list_resp = await async_client.get("/api/v1/users/")
    assert list_resp.status_code == 200
    users_list = list_resp.json()
    assert len(users_list) == 1
    assert users_list[0]["id"] == user_id

    # 4. Get User by ID
    get_resp = await async_client.get(f"/api/v1/users/{user_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == user_id

    # 5. Update User
    update_payload = {"name": "Jane Smith", "phone": "+1112223333"}
    update_resp = await async_client.put(f"/api/v1/users/{user_id}", json=update_payload)
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Jane Smith"

    # 6. Delete User
    del_resp = await async_client.delete(f"/api/v1/users/{user_id}")
    assert del_resp.status_code == 204

    # 7. Verify Not Found after deletion
    get_again = await async_client.get(f"/api/v1/users/{user_id}")
    assert get_again.status_code == 404
