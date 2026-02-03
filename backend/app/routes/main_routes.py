from flask import Blueprint, jsonify
from ..models.session_models import get_user_by_session_token
from ..utils.session_utils import get_session_token_from_cookie

main_bp = Blueprint("main", __name__, url_prefix="/api")


# ----------------
# Health check
# ----------------
@main_bp.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


# ----------------
# Usuario actual
# ----------------
@main_bp.get("/me")
def me():
    token = get_session_token_from_cookie()
    user = get_user_by_session_token(token)

    if not user:
        return jsonify({"ok": False, "error": "No autorizado"}), 401

    return jsonify(user), 200
