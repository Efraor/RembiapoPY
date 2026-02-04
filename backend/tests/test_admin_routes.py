from app.db import get_db


def test_admin_dashboard_unauthorized(client):
    res = client.get("/api/admin/dashboard")
    assert res.status_code == 403
    data = res.get_json()
    assert "error" in data


def test_admin_profiles_unauthorized(client):
    res = client.get("/api/admin/profiles")
    assert res.status_code == 403
    data = res.get_json()
    assert "error" in data


def test_admin_profiles_authorized_flow(client, app):
    with app.app_context():
        db = get_db()
        db.execute(
            "INSERT INTO users (email, role, password_hash) VALUES (?, ?, ?)",
            ("admin@example.com", "admin", "hash"),
        )
        admin_id = db.execute("SELECT id FROM users WHERE email = ?", ("admin@example.com",)).fetchone()["id"]
        db.execute(
            "INSERT INTO users (email, password_hash) VALUES (?, ?)",
            ("pro@example.com", "hash"),
        )
        user_id = db.execute("SELECT id FROM users WHERE email = ?", ("pro@example.com",)).fetchone()["id"]
        db.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", ("Electricidad",))
        category_id = db.execute(
            "SELECT id FROM categories WHERE name = ?",
            ("Electricidad",),
        ).fetchone()["id"]
        db.execute(
            """
            INSERT INTO profiles (user_id, category_id, bio, city, whatsapp, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, category_id, "Bio", "Asuncion", "0991000000", "pending"),
        )
        profile_id = db.execute("SELECT id FROM profiles WHERE user_id = ?", (user_id,)).fetchone()["id"]
        db.commit()

    headers = {"X-Admin-ID": str(admin_id)}

    res_list = client.get("/api/admin/profiles?status=pending", headers=headers)
    assert res_list.status_code == 200
    data = res_list.get_json()
    assert isinstance(data, list)
    assert any(p["id"] == profile_id for p in data)

    res_approve = client.put(f"/api/admin/profiles/{profile_id}/approve", headers=headers)
    assert res_approve.status_code == 200
