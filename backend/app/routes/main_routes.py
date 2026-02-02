<<<<<<< HEAD
from flask import Blueprint, jsonify

# Blueprint = "mini-app" de Flask para agrupar rutas relacionadas.
# Lo registramos luego en create_app() usando app.register_blueprint(...)
main_bp = Blueprint("main", __name__)

@main_bp.route("/api/health")
#  Endpoint de salud (health check).
def health():
    return jsonify({"status": "ok"})
=======
from datetime import datetime, timezone
from flask import Blueprint, jsonify, request, current_app

from ..db import get_db

main_bp = Blueprint("main", __name__)

def _cookie_name() -> str:
    return current_app.config.get("SESSION_COOKIE_NAME", "rembiapy_session")

def _get_user_by_session_token(token: str):
    if not token:
        return None

    db = get_db()
    row = db.execute(

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

@main_bp.get("/me")
def me():
    token = request.cookies.get(_cookie_name(), "") or ""
    user = _get_user_by_session_token(token)

    if not user:
        return jsonify({"ok": False, "error": "No autorizado"}), 401

    
    return jsonify(user), 200
>>>>>>> diego/main
