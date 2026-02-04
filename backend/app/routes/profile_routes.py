from datetime import datetime, timezone
from flask import Blueprint, jsonify, request, current_app

from ..db import get_db
from ..models.profile_model import upsert_profile, get_profile_by_user_id, list_profiles

profile_bp = Blueprint("profiles", __name__)


def _cookie_name() -> str:
    return current_app.config.get("SESSION_COOKIE_NAME", "rembiapy_session")


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

    try:
        exp_dt = datetime.fromisoformat(row["expires_at"])
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


@profile_bp.get("/profiles")
def get_profiles():
    category = request.args.get("category", "")
    limit = request.args.get("limit", "20")

    items = list_profiles(category=category, limit=limit)
    return jsonify({"ok": True, "profiles": items}), 200


@profile_bp.get("/profile")
def get_profile():
    token = request.cookies.get(_cookie_name(), "") or ""
    user = _get_user_by_session_token(token)

    if not user:
        return jsonify({"ok": False, "error": "No autorizado"}), 401

    profile = get_profile_by_user_id(user["id"])
    return jsonify({"ok": True, "profile": profile}), 200


@profile_bp.post("/profile")
def save_profile():
    token = request.cookies.get(_cookie_name(), "") or ""
    user = _get_user_by_session_token(token)

    if not user:
        return jsonify({"ok": False, "error": "No autorizado"}), 401

    data = request.get_json(silent=True) or {}

    role = (data.get("role") or user.get("role") or "user").strip().lower()
    if role not in ("user", "client", "pro"):
        role = "user"
    data["role"] = role

    if not data.get("email"):
        data["email"] = user.get("email", "")

    if not data.get("full_name") and user.get("name"):
        data["full_name"] = user.get("name")

    profile = upsert_profile(user["id"], data)
    return jsonify({"ok": True, "profile": profile}), 200
