def test_user_register_and_login(client):
    register_res = client.post(
        "/api/users/register",
        json={"email": "user@example.com", "password": "secret123"},
    )
    assert register_res.status_code == 201
    register_data = register_res.get_json()
    assert register_data["ok"] is True
    assert register_data.get("token")
    assert register_data.get("user", {}).get("email") == "user@example.com"

    login_res = client.post(
        "/api/users/login",
        json={"email": "user@example.com", "password": "secret123"},
    )
    assert login_res.status_code == 200
    login_data = login_res.get_json()
    assert login_data["ok"] is True
    assert login_data.get("token")
    assert login_data.get("user", {}).get("email") == "user@example.com"


def test_user_login_invalid_password(client):
    client.post(
        "/api/users/register",
        json={"email": "badpass@example.com", "password": "secret123"},
    )

    res = client.post(
        "/api/users/login",
        json={"email": "badpass@example.com", "password": "wrongpass"},
    )
    assert res.status_code == 401
    data = res.get_json()
    assert data["ok"] is False
