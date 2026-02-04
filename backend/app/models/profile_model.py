
# Funciones de acceso a datos para perfiles

from typing import Optional, List
from ..db import get_db


def upsert_profile(user_id: int, data: dict) -> dict:
    db = get_db()

    fields = {
        "full_name": data.get("full_name", "") or "",
        "role": data.get("role", "user") or "user",
        "category": data.get("category", "") or "",
        "service_title": data.get("service_title", "") or "",
        "phone": data.get("phone", "") or "",
        "whatsapp": data.get("whatsapp", "") or "",
        "email": data.get("email", "") or "",
        "city": data.get("city", "") or "",
        "bio": data.get("bio", "") or "",
        "photo_url": data.get("photo_url", "") or "",
    }

    db.execute(
        """
        INSERT INTO profiles (
            user_id, full_name, role, category, service_title,
            phone, whatsapp, email, city, bio, photo_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            full_name=excluded.full_name,
            role=excluded.role,
            category=excluded.category,
            service_title=excluded.service_title,
            phone=excluded.phone,
            whatsapp=excluded.whatsapp,
            email=excluded.email,
            city=excluded.city,
            bio=excluded.bio,
            photo_url=excluded.photo_url,
            updated_at=datetime('now')
        """,
        (
            user_id,
            fields["full_name"],
            fields["role"],
            fields["category"],
            fields["service_title"],
            fields["phone"],
            fields["whatsapp"],
            fields["email"],
            fields["city"],
            fields["bio"],
            fields["photo_url"],
        ),
    )
    db.commit()
    return get_profile_by_user_id(user_id) or {}


def get_profile_by_user_id(user_id: int) -> Optional[dict]:
    db = get_db()
    row = db.execute(
        "SELECT * FROM profiles WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    return dict(row) if row else None


def list_profiles(category: str = "", limit: int = 20) -> List[dict]:
    db = get_db()

    # Solo perfiles profesionales (role = 'pro')
    category = (category or "").strip().lower()
    limit = max(1, min(int(limit or 20), 100))

    if category:
        rows = db.execute(
            """
            SELECT * FROM profiles
            WHERE role = 'pro' AND lower(category) = ?
            ORDER BY updated_at DESC
            LIMIT ?
            """,
            (category, limit),
        ).fetchall()
    else:
        rows = db.execute(
            """
            SELECT * FROM profiles
            WHERE role = 'pro'
            ORDER BY updated_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(r) for r in rows]
