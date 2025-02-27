import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_feedback_flow():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        await ac.post("/auth/register", json={
            "username": "testfeedback",
            "email": "feedback@example.com",
            "password": "abc123"
        })
        login_resp = await ac.post("/auth/login", json={
            "email": "feedback@example.com",
            "password": "abc123"
        })
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        chat_resp = await ac.post("/api/v1/chat", json={
            "user_input": "Teste feedback",
            "session_id": "session-feedback"
        }, headers=headers)
        assert chat_resp.status_code == 200

        conv_resp = await ac.get("/api/v1/conversations", headers=headers)
        conv_data = conv_resp.json()
        assert len(conv_data) > 0
        conversation_id = conv_data[0]["id"]

        feed_resp = await ac.post("/api/v1/feedback/", json={
            "conversation_id": conversation_id,
            "rating": 1
        }, headers=headers)
        assert feed_resp.status_code == 201

        list_resp = await ac.get("/api/v1/feedback/", headers=headers)
        list_data = list_resp.json()
        assert len(list_data) == 1
        assert list_data[0]["conversation_id"] == conversation_id
        assert list_data[0]["rating"] == 1
