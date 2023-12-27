from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def get_user_token():
    # Login to get token
    response = client.post("/token", data={
        "username": "testuser",
        "password": "testpassword"
    })
    return response.json().get("access_token")


def test_login_for_access_token():
    response = client.post("/token", data={
        "username": "testuser",
        "password": "testpassword"
    })
    print(response.json())
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "TerraSync"}
