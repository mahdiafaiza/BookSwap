import pytest
from server import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def test_register_and_login(client):
    # Test register
    res = client.post("/api/auth/register", json={
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "testpass"
    })
    assert res.status_code in (200, 201)

    # Test login
    res = client.post("/api/auth/login", json={
        "email": "testuser@example.com",
        "password": "testpass"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert "token" in data
