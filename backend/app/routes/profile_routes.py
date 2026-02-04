from flask import Blueprint, jsonify, request
from ..models.profile_model import (
    upsert_profile,
    get_profile_by_user_id,
    list_profiles,
    list_categories,
    create_profile,
    approve_profile,
    get_approved_profiles,
)
from ..models.session_models import get_user_by_session_token
from ..utils.session_utils import get_session_token_from_cookie

profile_bp = Blueprint("profiles", __name__)


@profile_bp.get("/profiles")
def get_profiles():
    category = request.args.get("category", "")
    city = request.args.get("city", "")
    limit = request.args.get("limit", "20")

    items = list_profiles(category=category, city=city, limit=limit)
    return jsonify({"ok": True, "profiles": items}), 200


@profile_bp.get("/categories")
def get_categories():
    categories = list_categories()
    return jsonify({"ok": True, "categories": categories}), 200


@profile_bp.get("/profile")
def get_profile():
    token = get_session_token_from_cookie()
    user = get_user_by_session_token(token)

    if not user:
        return jsonify({"ok": False, "error": "No autorizado"}), 401

    profile = get_profile_by_user_id(user["id"])
    return jsonify({"ok": True, "profile": profile}), 200


@profile_bp.post("/profile")
def save_profile():
    token = get_session_token_from_cookie()
    user = get_user_by_session_token(token)

    if not user:
        return jsonify({"ok": False, "error": "No autorizado"}), 401

    data = request.get_json(silent=True) or {}

    role = (data.get("role") or user.get("role") or "client").strip().lower()
    if role not in ("client", "pro", "admin"):
        role = "client"
    data["role"] = role

    if not data.get("email"):
        data["email"] = user.get("email", "")

    if not data.get("full_name") and user.get("name"):
        data["full_name"] = user.get("name")

    profile = upsert_profile(user["id"], data)
    return jsonify({"ok": True, "profile": profile}), 200


# POST /api/profiles (compatibilidad)
@profile_bp.post("/profiles")
def create_profile_route():
    data = request.get_json() or {}

    required_fields = ["user_id", "category_id", "bio", "city", "whatsapp"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    try:
        create_profile(
            data["user_id"],
            data["category_id"],
            data["bio"],
            data["city"],
            data["whatsapp"],
        )
        return jsonify({"message": "Perfil creado y pendiente de aprobación"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# PUT /api/admin/approve-profile/<id> (compatibilidad)
@profile_bp.put("/admin/approve-profile/<int:profile_id>")
def approve_profile_route(profile_id):
    approve_profile(profile_id)
    return jsonify({"message": "Perfil aprobado exitosamente"}), 200


# GET /api/profiles/approved (compatibilidad)
@profile_bp.get("/profiles/approved")
def get_approved_profiles_route():
    city = request.args.get("city")
    category_id = request.args.get("category_id")
    profiles = get_approved_profiles(city, category_id)
    return jsonify([dict(p) for p in profiles]), 200