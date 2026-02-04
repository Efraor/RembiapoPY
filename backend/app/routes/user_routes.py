"""User routes: local auth and user helpers."""
from flask import Blueprint, request, jsonify, make_response
from app.services.auth_service import register_local as register_local_service, login_local as login_local_service, login_google
from app.utils.session_utils import set_session_cookie

user_bp = Blueprint("user", __name__, url_prefix="/api/users")


# Registro local
@user_bp.route("/register", methods=["POST"])
def register_local():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"ok": False, "error": "Faltan datos"}), 400

    result = register_local_service(email, password)
    status = 201 if result.get("ok") else 400
    resp = make_response(jsonify(result), status)
    if result.get("ok"):
        set_session_cookie(resp, result.get("token", ""))
    return resp


# Login local
@user_bp.route("/login", methods=["POST"])
def login_local():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"ok": False, "error": "Faltan datos"}), 400

    result = login_local_service(email, password)
    status = 200 if result.get("ok") else 401
    resp = make_response(jsonify(result), status)
    if result.get("ok"):
        set_session_cookie(resp, result.get("token", ""))
    return resp


# Login Google
@user_bp.route("/google", methods=["POST"])
def login_google_route():
    data = request.get_json(silent=True) or {}
    credential = data.get("credential", "")
    if not credential:
        return jsonify({"ok": False, "error": "Falta credential (ID token)."}), 400

    result = login_google(credential)
    status = 200 if result.get("ok") else 401
    resp = make_response(jsonify(result), status)
    if result.get("ok"):
        set_session_cookie(resp, result.get("token", ""))
    return resp