def _mock_google_payload(aud="test-client", iss="accounts.google.com"):
    return {
        "aud": aud,
        "iss": iss,
        "email": "google@example.com",
        "sub": "google-sub-123",
        "email_verified": True,
    }


def test_auth_google_login_success(client, app, monkeypatch):
    app.config["GOOGLE_CLIENT_ID"] = "test-client"

    from app.services import auth_service

    monkeypatch.setattr(
        auth_service.id_token,
        "verify_oauth2_token",
        lambda *args, **kwargs: _mock_google_payload(),
    )

    res = client.post("/api/auth/google", json={"credential": "dummy"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["ok"] is True
    assert data.get("token")
    assert data.get("user", {}).get("email") == "google@example.com"


def test_users_google_login_success(client, app, monkeypatch):
    app.config["GOOGLE_CLIENT_ID"] = "test-client"

    from app.services import auth_service

    monkeypatch.setattr(
        auth_service.id_token,
        "verify_oauth2_token",
        lambda *args, **kwargs: _mock_google_payload(),
    )

    res = client.post("/api/users/google", json={"credential": "dummy"})
    assert res.status_code == 200
    data = res.get_json()
    assert data["ok"] is True
    assert data.get("token")
    assert data.get("user", {}).get("email") == "google@example.com"
