def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={"email": "newuser@test.com", "password": "password123", "full_name": "New User"}
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_register_duplicate_email(client, test_user):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@test.com",
            "full_name": "Another User",
            "password": "password123"
        }
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_login_success(client, test_user):
    response = client.post(
        "/auth/login",
        json={"email": "test@test.com", "password": "test123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    response = client.post(
        "/auth/login",
        json={"email": "test@test.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401

def test_login_nonexistent_user(client):
    response = client.post(
        "/auth/login",
        json={"email": "noexist@test.com", "password": "test123"}
    )
    assert response.status_code == 401

def test_get_current_user(client, user_token):
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@test.com"

def test_get_current_user_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401