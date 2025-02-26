import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_chat_flow():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        await ac.post("/auth/register", json={
            "username": "testuser2",
            "email": "test2@example.com",
            "password": "123456"
        })
        login_resp = await ac.post("/auth/login", json={
            "email": "test2@example.com",
            "password": "123456"
        })
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Chamar /chat
        resp = await ac.post("/api/v1/chat", json={
            "user_input": "O que é SOLID?",
            "session_id": "abc123"
        }, headers=headers)
        assert resp.status_code == 200

        # Listar conversas
        conv_resp = await ac.get("/api/v1/conversations", headers=headers)
        assert conv_resp.status_code == 200
        conv_list = conv_resp.json()
        assert len(conv_list) > 0
        assert conv_list[0]["user_input"] == "O que é SOLID?"
