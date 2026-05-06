
def test_register_success(client):
    resp = client.post("/api/v1/auth/register", json={
        "email": "newuser@budgix.dev",
        "full_name": "New User",
        "password": "password123",
        "currency": "EUR",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "newuser@budgix.dev"
    assert data["role"] == "user"
    assert "hashed_password" not in data


def test_register_duplicate_email(client):
    payload = {"email": "dup@budgix.dev", "full_name": "Dup", "password": "pass1234", "currency": "EUR"}
    client.post("/api/v1/auth/register", json=payload)
    resp = client.post("/api/v1/auth/register", json=payload)
    assert resp.status_code == 409


def test_login_success(client):
    client.post("/api/v1/auth/register", json={
        "email": "login@budgix.dev", "full_name": "Login User",
        "password": "loginpass1", "currency": "EUR",
    })
    resp = client.post("/api/v1/auth/login", json={"email": "login@budgix.dev", "password": "loginpass1"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()
    assert "refresh_token" in resp.json()


def test_login_wrong_password(client):
    resp = client.post("/api/v1/auth/login", json={"email": "login@budgix.dev", "password": "wrongpass"})
    assert resp.status_code == 401


def test_get_me(client, auth_headers):
    resp = client.get("/api/v1/users/me", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "test@budgix.dev"


def test_me_unauthenticated(client):
    resp = client.get("/api/v1/users/me")
    assert resp.status_code == 403
