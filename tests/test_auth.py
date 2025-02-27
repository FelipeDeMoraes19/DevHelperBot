import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        register_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "123456"
        }
        r = await ac.post("/auth/register", json=register_data)
        assert r.status_code == 200

        login_data = {"email": "test@example.com", "password": "123456"}
        r = await ac.post("/auth/login", json=login_data)
        assert r.status_code == 200
        resp_json = r.json()
        assert "access_token" in resp_json
        assert resp_json["user_id"] is not None
