
def test_register_user(client):
    response = client.post(
        "/api/auth/register",
        json={"username": "newuser", "password": "password", "role": "author"}
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["username"] == "newuser"

def test_register_existing_user(client):
    # First registration
    client.post(
        "/api/auth/register",
        json={"username": "existinguser", "password": "password", "role": "author"}
    )
    # Second registration
    response = client.post(
        "/api/auth/register",
        json={"username": "existinguser", "password": "password", "role": "author"}
    )
    assert response.status_code == 400
    assert response.json()["success"] is False

def test_login_user(client):
    # Create user first
    client.post(
        "/api/auth/register",
        json={"username": "loginuser", "password": "password", "role": "author"}
    )
    # Login
    response = client.post(
        "/api/auth/login",
        json={"username": "loginuser", "password": "password"}
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "access_token" in response.json()["data"]

def test_login_invalid(client):
    response = client.post(
        "/api/auth/login",
        json={"username": "wronguser", "password": "password"}
    )
    assert response.status_code == 401
    assert response.json()["success"] is False

def test_get_me(client, author_token):
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {author_token}"}
    )
    assert response.status_code == 200
    assert response.json()["data"]["username"] == "author_test"

def test_get_me_unauthorized(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401
