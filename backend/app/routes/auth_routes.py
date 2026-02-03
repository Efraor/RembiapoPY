import secrets
import requests
from flask import Blueprint, request, jsonify, current_app, redirect, make_response

from ..services.auth_service import login_google
from ..models.session_models import delete_session
from ..utils.session_utils import (
    set_session_cookie,
    clear_session_cookie,
    get_session_token_from_cookie,
)

auth_bp = Blueprint("auth", __name__)


# ---------- Google login (POST) ----------

@auth_bp.post("/google")
def google_login_post():
    data = request.get_json(silent=True) or {}
    credential = data.get("credential", "")

    if not credential:
        return jsonify({"ok": False, "error": "Falta credential (ID token)."}), 400

    result = login_google(credential)
    if not result["ok"]:
        return jsonify(result), 401

    resp = make_response(jsonify(result), 200)
    set_session_cookie(resp, result["token"])
    return resp


# ---------- OAuth redirect ----------

@auth_bp.get("/google/login")
def google_login():
    client_id = current_app.config.get("GOOGLE_CLIENT_ID", "").strip()
    redirect_uri = current_app.config.get("GOOGLE_REDIRECT_URI", "").strip()

    if not client_id or not redirect_uri:
        return jsonify({"ok": False, "error": "Falta config Google"}), 500

    state = secrets.token_urlsafe(24)

    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&scope=openid%20email%20profile"
        f"&state={state}"
        f"&prompt=select_account"
    )

    resp = make_response(redirect(auth_url))
    resp.set_cookie("oauth_state", state, httponly=True, samesite="Lax", max_age=600)
    return resp


@auth_bp.get("/google/callback")
def google_callback():
    code = request.args.get("code", "")
    state = request.args.get("state", "")
    saved_state = request.cookies.get("oauth_state", "")

    if not code:
        return jsonify({"ok": False, "error": "Falta code"}), 400

    if state != saved_state:
        return jsonify({"ok": False, "error": "State inválido"}), 400

    client_id = current_app.config.get("GOOGLE_CLIENT_ID", "")
    client_secret = current_app.config.get("GOOGLE_CLIENT_SECRET", "")
    redirect_uri = current_app.config.get("GOOGLE_REDIRECT_URI", "")

    token_res = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        },
        timeout=10,
    )

    if token_res.status_code != 200:
        return jsonify({"ok": False, "error": "Error al obtener token"}), 401

    id_token_str = token_res.json().get("id_token", "")
    result = login_google(id_token_str)

    if not result["ok"]:
        return jsonify(result), 401

    front_url = current_app.config.get(
        "FRONTEND_REDIRECT_URL",
        "http://127.0.0.1:5500/frontend/src/pages/login.html"
    )

    resp = make_response(redirect(front_url))
    set_session_cookie(resp, result["token"])
    resp.set_cookie("oauth_state", "", expires=0)
    return resp


# ---------- Logout ----------

@auth_bp.post("/logout")
def logout():
    token = get_session_token_from_cookie()
    delete_session(token)

    resp = make_response(jsonify({"ok": True}), 200)
    clear_session_cookie(resp)
    return resp
