from flask import Blueprint, request, jsonify
from app.services.user_service import register_user_local, register_user_google, validate_user_local

user_bp = Blueprint("user", __name__, url_prefix="/api/users")


# Registro local
@user_bp.route("/register", methods=["POST"])
def register_local():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"ok": False, "error": "Faltan datos"}), 400

    result = register_user_local(email, password)
    status = 201 if result.get("ok") else 400
    return jsonify(result), status


# Login local
@user_bp.route("/login", methods=["POST"])
def login_local():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"ok": False, "error": "Faltan datos"}), 400

    result = validate_user_local(email, password)
    status = 200 if result.get("ok") else 401
    return jsonify(result), status


# Registro/login Google
@user_bp.route("/google", methods=["POST"])
def login_google_route():
    data = request.get_json() or {}
    email = data.get("email")
    google_sub = data.get("google_sub")
    if not email or not google_sub:
        return jsonify({"ok": False, "error": "Faltan datos"}), 400

    result = register_user_google(email, google_sub)
    return jsonify(result), 200
