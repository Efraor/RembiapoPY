import secrets
import requests
from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, current_app, redirect, make_response

from ..db import get_db
from ..services.auth_service import login_google, register_local, login_local
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

auth_bp = Blueprint("auth", __name__)

# Ayudantes de sesión (cookie + DB)

def _cookie_name() -> str:
    return current_app.config.get("SESSION_COOKIE_NAME", "rembiapy_session")

def _set_session_cookie(resp, token: str):
    
    resp.set_cookie(
        _cookie_name(),
        token,
        httponly=True,
        samesite="Lax",
        secure=False,   
        max_age=60 * 60 * 24,
        path="/",
    )

def _clear_session_cookie(resp):
    resp.set_cookie(_cookie_name(), "", expires=0, path="/")

def _get_session_token_from_cookie() -> str:
    return request.cookies.get(_cookie_name(), "") or ""

def _get_user_by_session_token(token: str):
    if not token:
        return None

    db = get_db()
    row = db.execute(
    """
    SELECT u.id, u.email, u.name, u.role, s.expires_at
    FROM sessions s
    JOIN users u ON u.id = s.user_id
    WHERE s.token = ?
    """,
    (token,),
).fetchone()


    if not row:
        return None

    expires_at = row["expires_at"]
    try:
        exp_dt = datetime.fromisoformat(expires_at)
        if exp_dt.tzinfo is None:
            exp_dt = exp_dt.replace(tzinfo=timezone.utc)
    except Exception:
        return None

    if exp_dt <= datetime.now(timezone.utc):
        return None

    return {
        "id": row["id"],
        "name": row["name"] or "",
        "email": row["email"],
        "role": row["role"] or "user",
    }

def _delete_session(token: str):
    if not token:
        return
    db = get_db()
    db.execute("DELETE FROM sessions WHERE token = ?", (token,))
    db.commit()


 # Tu login Google actual por POST

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
    _set_session_cookie(resp, result["token"])
    return resp

@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "")
    password = data.get("password", "")
    name = data.get("name", "")
    role = data.get("role", "user")

    result = register_local(email, password, name=name, role=role)
    if not result["ok"]:
        return jsonify(result), 400

    resp = make_response(jsonify(result), 200)
    _set_session_cookie(resp, result["token"])
    return resp


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    email = data.get("email", "")
    password = data.get("password", "")

    result = login_local(email, password)
    if not result["ok"]:
        return jsonify(result), 401

    resp = make_response(jsonify(result), 200)
    _set_session_cookie(resp, result["token"])
    return resp

 # OAuth redirect flow


@auth_bp.get("/google/login")
def google_login():
    client_id = current_app.config.get("GOOGLE_CLIENT_ID", "").strip()
    redirect_uri = current_app.config.get("GOOGLE_REDIRECT_URI", "").strip()

    if not client_id or not redirect_uri:
        return jsonify({"ok": False, "error": "Falta config GOOGLE_CLIENT_ID/GOOGLE_REDIRECT_URI"}), 500

    
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
    resp.set_cookie("oauth_state", state, httponly=True, samesite="Lax", max_age=600, path="/")
    return resp


@auth_bp.get("/google/callback")
def google_callback():
    code = request.args.get("code", "")
    state = request.args.get("state", "")
    saved_state = request.cookies.get("oauth_state", "")

    if not code:
        return jsonify({"ok": False, "error": "Falta code"}), 400

    if not state or state != saved_state:
        return jsonify({"ok": False, "error": "State inválido"}), 400

    client_id = current_app.config.get("GOOGLE_CLIENT_ID", "").strip()
    client_secret = current_app.config.get("GOOGLE_CLIENT_SECRET", "").strip()
    redirect_uri = current_app.config.get("GOOGLE_REDIRECT_URI", "").strip()

    if not client_id or not client_secret or not redirect_uri:
        return jsonify({"ok": False, "error": "Falta config de Google (id/secret/redirect)"}), 500
    
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
        return jsonify({"ok": False, "error": "No se pudo intercambiar code por token"}), 401

    token_data = token_res.json()
    id_token_str = token_data.get("id_token", "")

    if not id_token_str:
        return jsonify({"ok": False, "error": "No vino id_token"}), 401

   
    result = login_google(id_token_str)
    if not result["ok"]:
        return jsonify(result), 401

   
    front_url = current_app.config.get(
        "FRONTEND_REDIRECT_URL",
        "http://127.0.0.1:5500/frontend/src/pages/login.html"
    )

    resp = make_response(redirect(front_url))
    _set_session_cookie(resp, result["token"])
    resp.set_cookie("oauth_state", "", expires=0, path="/")
    return resp


@auth_bp.post("/logout")
def logout():
    token = _get_session_token_from_cookie()
    _delete_session(token)

    resp = make_response(jsonify({"ok": True}), 200)
    _clear_session_cookie(resp)
    return resp
