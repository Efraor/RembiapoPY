from ..models.user_model import (
    find_user_by_email,
    find_user_by_google_sub,
    create_user_google,
    create_user_local,
)
from werkzeug.security import check_password_hash


def register_user_local(email: str, password: str) -> dict:
    """Registra usuario local, con hash de contraseÃ±a"""
    existing_user = find_user_by_email(email)
    if existing_user:
        return {"ok": False, "error": "Usuario ya existe"}

    user_id = create_user_local(email, password)
    return {"ok": True, "user_id": user_id}


def register_user_google(email: str, google_sub: str) -> dict:
    """Registra usuario vÃ­a Google OAuth"""
    existing_user = find_user_by_google_sub(google_sub)
    if existing_user:
        return {"ok": True, "user_id": existing_user["id"]}

    user_id = create_user_google(email, google_sub)
    return {"ok": True, "user_id": user_id}


def validate_user_local(email: str, password: str) -> dict:
    """Valida login local"""
    user = find_user_by_email(email)
    if not user or not check_password_hash(user["password_hash"], password):
        return {"ok": False, "error": "Credenciales invÃ¡lidas"}
    return {"ok": True, "user_id": user["id"]}
