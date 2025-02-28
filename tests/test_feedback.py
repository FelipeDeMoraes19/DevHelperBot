import pytest
import uuid

@pytest.mark.anyio
async def test_feedback_flow(async_client):
    unique = str(uuid.uuid4())[:8]
    r = await async_client.post("/auth/register", json={
        "username": f"testfeedback_{unique}",
        "email": f"feedback_{unique}@example.com",
        "password": "abc123"
    })
    assert r.status_code == 200, f"register failed: {r.text}"

    login_resp = await async_client.post("/auth/login", json={
        "email": f"feedback_{unique}@example.com",
        "password": "abc123"
    })
    assert login_resp.status_code == 200, f"login failed: {login_resp.text}"
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    chat_resp = await async_client.post("/api/v1/chat", json={
        "user_input": "Teste feedback",
        "session_id": "session-feedback"
    }, headers=headers)
    assert chat_resp.status_code == 200, f"chat failed: {chat_resp.text}"

    conv_resp = await async_client.get("/api/v1/conversations", headers=headers)
    assert conv_resp.status_code == 200
    conv_data = conv_resp.json()
    assert len(conv_data) > 0
    conversation_id = conv_data[0]["id"]

    feed_resp = await async_client.post("/api/v1/feedback/", json={
        "conversation_id": conversation_id,
        "rating": 1
    }, headers=headers)
    assert feed_resp.status_code == 201, f"feedback failed: {feed_resp.text}"

    list_resp = await async_client.get("/api/v1/feedback/", headers=headers)
    list_data = list_resp.json()
    assert len(list_data) == 1
    assert list_data[0]["conversation_id"] == conversation_id
    assert list_data[0]["rating"] == 1
