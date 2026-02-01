
# Lógica de autenticación:
# - login con Google
# - creación de sesiones

import secrets
from datetime import datetime, timedelta, timezone
from flask import current_app

from werkzeug.security import generate_password_hash, check_password_hash

from ..db import get_db
from ..models.user_model import (
    find_user_by_google_sub,
    find_user_by_email,
    create_user_google,
    create_user_local,
)

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

SESSION_HOURS = 24

def _now_utc() -> datetime:
    return datetime.now(timezone.utc)

def _expires_at() -> str:
    return (_now_utc() + timedelta(hours=SESSION_HOURS)).isoformat()

def _create_session(user_id: int) -> str:
    
    # Crea una sesión y devuelve el token

    db = get_db()
    token = secrets.token_urlsafe(32)
    db.execute(
        "INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)",
        (token, user_id, _expires_at()),
    )
    db.commit()
    return token

# Autenticacion local (email + password)

def register_local(email: str, password: str) -> dict:
    email = (email or "").strip().lower()
    password = password or ""

    if not email or not password:
        return {"ok": False, "error": "Falta email o password."}

    if len(password) < 6:
        return {"ok": False, "error": "La contraseña debe tener al menos 6 caracteres."}

    if find_user_by_email(email):
        return {"ok": False, "error": "Email ya registrado."}

    password_hash = generate_password_hash(password)
    user_id = create_user_local(email, password_hash)

    token = _create_session(user_id)
    return {"ok": True, "token": token, "user": {"id": user_id, "email": email}}

def login_local(email: str, password: str) -> dict:
    email = (email or "").strip().lower()
    password = password or ""

    if not email or not password:
        return {"ok": False, "error": "Falta email o password."}

    user = find_user_by_email(email)
    if not user or not user.get("password_hash"):
        return {"ok": False, "error": "Credenciales inválidas."}

    if not check_password_hash(user["password_hash"], password):
        return {"ok": False, "error": "Credenciales inválidas."}

    token = _create_session(user["id"])
    return {"ok": True, "token": token, "user": {"id": user["id"], "email": user["email"]}}


# Autenticacion con Google


def login_google(id_token_str: str) -> dict:

    # Valida el token de Google y autentica o crea el usuario
    # Si el usuario ya existe, se reutiliza; si no, se crea uno nuevo

    client_id = current_app.config.get("GOOGLE_CLIENT_ID", "").strip()
    if not client_id:
        return {"ok": False, "error": "GOOGLE_CLIENT_ID no configurado en backend."}

    try:
        req = google_requests.Request()
        payload = id_token.verify_oauth2_token(id_token_str, req, client_id)
    except Exception:
        return {"ok": False, "error": "Token de Google inválido."}

    google_sub = payload.get("sub")
    email = (payload.get("email") or "").strip().lower()

    if not google_sub or not email:
        return {"ok": False, "error": "Token Google incompleto (sin sub/email)."}

    user = find_user_by_google_sub(google_sub)
    if user:
        token = _create_session(user["id"])
        return {"ok": True, "token": token, "user": {"id": user["id"], "email": user["email"]}}

    existing = find_user_by_email(email)
    if existing:
        token = _create_session(existing["id"])
        return {"ok": True, "token": token, "user": {"id": existing["id"], "email": existing["email"]}}

    user_id = create_user_google(email, google_sub)
    token = _create_session(user_id)
    return {"ok": True, "token": token, "user": {"id": user_id, "email": email}}