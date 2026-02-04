"""User data access and local auth helpers."""
from typing import Optional
from werkzeug.security import generate_password_hash
from ..db import get_db


def find_user_by_email(email: str) -> Optional[dict]:
    """Busca un usuario por email"""
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    return dict(row) if row else None


def find_user_by_google_sub(google_sub: str) -> Optional[dict]:
    """Busca un usuario asociado a Google"""
    db = get_db()
    row = db.execute("SELECT * FROM users WHERE google_sub = ?", (google_sub,)).fetchone()
    return dict(row) if row else None


def create_user_google(email: str, google_sub: str) -> int:
    """Crea un usuario nuevo con autenticacion Google"""
    db = get_db()
    cur = db.execute(
        "INSERT INTO users (email, google_sub) VALUES (?, ?)",
        (email, google_sub),
    )
    db.commit()
    return cur.lastrowid


def create_user_local(email: str, password: str, name: str = "", role: str = "client") -> int:
    """Crea un usuario nuevo con email/password (hashea antes de guardar)."""
    db = get_db()
    password_hash = generate_password_hash(password)
    cur = db.execute(
        "INSERT INTO users (email, password_hash, name, role) VALUES (?, ?, ?, ?)",
        (email, password_hash, name or "", role or "client"),
    )
    db.commit()
    return cur.lastrowid
