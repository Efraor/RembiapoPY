from app.db import get_db


def test_health_ok(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}


def test_me_unauthorized(client):
    res = client.get("/api/me")
    assert res.status_code == 401
    data = res.get_json()
    assert data["ok"] is False


def test_profiles_list_empty(client):
    res = client.get("/api/profile")
    assert res.status_code == 401
    data = res.get_json()
    assert data.get("ok") is False


def test_profiles_create_missing_fields(client):
    res = client.post("/api/profiles", json={"user_id": 1})
    assert res.status_code == 400
    data = res.get_json()
    assert "error" in data


def test_profiles_create_and_list(client, app):
    with app.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            ("pro@example.com", "hash"),
        )
        user_id = db.execute("SELECT id FROM users WHERE email = ?", ("pro@example.com",)).fetchone()["id"]
        db.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", ("Plomería",))
        category_id = db.execute(
            "SELECT id FROM categories WHERE name = ?",
            ("Plomería",),
        ).fetchone()["id"]
        db.commit()

    res = client.post(
        "/api/profiles",
        json={
            "user_id": user_id,
            "category_id": category_id,
            "bio": "Bio",
            "city": "Asuncion",
            "whatsapp": "0991000000",
        },
    )
    assert res.status_code == 201

    res_list = client.get("/api/profile")
    assert res_list.status_code == 401
    data = res_list.get_json()
    assert data.get("ok") is False
