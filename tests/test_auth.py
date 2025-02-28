import pytest
import uuid

@pytest.mark.anyio
async def test_register_and_login(async_client):
    unique = str(uuid.uuid4())[:8]
    register_data = {
        "username": f"testuser_{unique}",
        "email": f"test_{unique}@example.com",
        "password": "123456"
    }
    
    r = await async_client.post("/auth/register", json=register_data)
    assert r.status_code == 200
    
    login_data = {"email": f"test_{unique}@example.com", "password": "123456"}
    r = await async_client.post("/auth/login", json=login_data)
    assert r.status_code == 200
    
    await async_client.aclose()

