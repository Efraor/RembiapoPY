"""Profile data access: categories, profiles, and listing queries."""
from typing import Optional, List
from ..db import get_db


def _get_category_id(category_name: str) -> Optional[int]:
    if not category_name:
        return None
    db = get_db()
    name = category_name.strip()
    row = db.execute(
        "SELECT id FROM categories WHERE name = ?",
        (name,),
    ).fetchone()
    if row:
        return row["id"]
    cur = db.execute(
        "INSERT INTO categories (name) VALUES (?)",
        (name,),
    )
    db.commit()
    return cur.lastrowid


def upsert_profile(user_id: int, data: dict) -> dict:
    db = get_db()

    full_name = data.get("full_name", "") or ""
    role = data.get("role", "client") or "client"
    email = data.get("email", "") or ""

    category_name = data.get("category", "") or ""
    city = data.get("city", "") or ""
    whatsapp = data.get("whatsapp", "") or ""
    bio = data.get("bio", "") or ""

    category_id = _get_category_id(category_name) if category_name else None

    # Actualiza datos del usuario
    db.execute(
        "UPDATE users SET name = COALESCE(?, name), role = COALESCE(?, role), email = COALESCE(?, email) WHERE id = ?",
        (full_name or None, role or None, email or None, user_id),
    )

    # Inserta/actualiza perfil (schema actual con category_id/status)
    db.execute(
        """
        INSERT INTO profiles (user_id, category_id, bio, city, whatsapp, status)
        VALUES (
            ?, ?, ?, ?, ?,
            CASE
                WHEN ? = 'pro' THEN 'approved'
                ELSE COALESCE((SELECT status FROM profiles WHERE user_id = ?), 'pending')
            END
        )
        ON CONFLICT(user_id) DO UPDATE SET
            category_id=excluded.category_id,
            bio=excluded.bio,
            city=excluded.city,
            whatsapp=excluded.whatsapp,
            status=CASE
                WHEN excluded.status = 'approved' THEN 'approved'
                ELSE profiles.status
            END,
            updated_at=datetime('now')
        """,
        (
            user_id,
            category_id,
            bio,
            city,
            whatsapp,
            role,
            user_id,
        ),
    )
    db.commit()
    return get_profile_by_user_id(user_id) or {}


def get_profile_by_user_id(user_id: int) -> Optional[dict]:
    db = get_db()
    row = db.execute(
        """
        SELECT u.name as full_name, u.email, u.role,
               p.bio, p.city, p.whatsapp, p.updated_at,
               c.name as category
        FROM users u
        LEFT JOIN profiles p ON p.user_id = u.id
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE u.id = ?
        """,
        (user_id,),
    ).fetchone()
    return dict(row) if row else None


def list_profiles(category: str = "", city: str = "", limit: int = 20) -> List[dict]:
    db = get_db()

    category = (category or "").strip()
    city = (city or "").strip()
    limit = max(1, min(int(limit or 20), 100))

    query = """
        SELECT u.name as full_name,
               u.picture as photo_url,
               u.email,
               p.bio as bio,
               p.bio as service_title,
               p.city,
               p.whatsapp,
               c.name as category
        FROM profiles p
        JOIN users u ON p.user_id = u.id
        JOIN categories c ON p.category_id = c.id
        WHERE p.status = 'approved'
    """
    params = []

    if category:
        query += " AND c.name = ?"
        params.append(category)
    if city:
        query += " AND p.city = ?"
        params.append(city)

    query += " ORDER BY p.updated_at DESC LIMIT ?"
    params.append(limit)

    rows = db.execute(query, params).fetchall()
    return [dict(r) for r in rows]


def get_approved_profiles(city=None, category_id=None) -> List[dict]:
    db = get_db()

    query = """
        SELECT u.name as full_name, u.picture as photo_url,
               p.bio, p.city, p.whatsapp, c.name AS category
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

    return [dict(r) for r in db.execute(query, params).fetchall()]


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
