
# Endpoints de autenticación

from flask import Blueprint, request, jsonify
from ..services.auth_service import (
    login_google,
    login_local,
    register_local,
)

auth_bp = Blueprint("auth", __name__)

# Login con Google


@auth_bp.post("/google")

 # Endpoint que recibe el token de Google desde el frontend
 
def google_login():
    data = request.get_json(silent=True) or {}
    credential = data.get("credential", "")

    if not credential:
        return jsonify({"ok": False, "error": "Falta credential (ID token)."}), 400

    result = login_google(credential)
    return jsonify(result), (200 if result["ok"] else 401)


# Registro local (email + password)


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}

    result = register_local(
        data.get("email"),
        data.get("password"),
    )

    return jsonify(result), (200 if result["ok"] else 400)


# Login local (email + password)


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}

    result = login_local(
        data.get("email"),
        data.get("password"),
    )

    return jsonify(result), (200 if result["ok"] else 401)