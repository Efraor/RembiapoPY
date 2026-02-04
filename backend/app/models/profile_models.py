from app.db import get_db


def get_approved_profiles(city=None, category_id=None):
    db = get_db()

    query = """
        SELECT u.name, u.picture, p.bio, p.city, p.whatsapp, c.name AS category
        FROM profiles p
        JOIN users u ON p.user_id = u.id
        JOIN categories c ON p.category_id = c.id
        WHERE p.status = 'approved'
    """
    params = []

    if city:
        query += " AND p.city = ?"
        params.append(city)

    if category_id:
        query += " AND p.category_id = ?"
        params.append(category_id)

    return db.execute(query, params).fetchall()


def create_profile(user_id, category_id, bio, city, whatsapp):
    db = get_db()
    db.execute(
        """
        INSERT INTO profiles (user_id, category_id, bio, city, whatsapp)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, category_id, bio, city, whatsapp)
    )
    db.commit()


def approve_profile(profile_id):
    db = get_db()
    db.execute(
        "UPDATE profiles SET status = 'approved' WHERE id = ?",
        (profile_id,)
    )
    db.commit()


def list_categories():
    db = get_db()
    rows = db.execute(
        "SELECT name FROM categories ORDER BY name ASC"
    ).fetchall()
    return [row["name"] for row in rows]
