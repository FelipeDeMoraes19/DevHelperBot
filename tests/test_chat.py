import pytest
import uuid

@pytest.mark.anyio
async def test_chat_flow(async_client):
    unique = str(uuid.uuid4())[:8]
    register_data = {
        "username": f"testuser_{unique}",
        "email": f"test_{unique}@example.com",
        "password": "123456"
    }
    r = await async_client.post("/auth/register", json=register_data)
    assert r.status_code == 200, f"Error registering: {r.text}"

    login_resp = await async_client.post("/auth/login", json={
        "email": f"test_{unique}@example.com",
        "password": "123456"
    })
    assert login_resp.status_code == 200, f"login failed: {login_resp.text}"
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = await async_client.post(
        "/api/v1/chat",
        json={
            "user_input": "O que é SOLID?",
            "session_id": "abc123"
        },
        headers=headers
    )
    assert resp.status_code == 200, f"chat request failed: {resp.text}"

    conv_resp = await async_client.get("/api/v1/conversations", headers=headers)
    assert conv_resp.status_code == 200, f"conversations failed: {conv_resp.text}"
    conv_list = conv_resp.json()
    assert len(conv_list) > 0
    assert conv_list[0]["user_input"] == "O que é SOLID?"
