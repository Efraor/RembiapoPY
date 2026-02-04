"""Admin routes: admin stats and moderation."""
from flask import Blueprint, request, jsonify
from app.models.admin_models import (
    is_admin,
    get_profiles_by_status,
    profile_exists,
    approve_profile,
    get_admin_dashboard_stats,
)

admin_bp = Blueprint('admin', __name__)


def _validate_admin():
    admin_id = request.headers.get('X-Admin-ID')
    if not admin_id or not is_admin(admin_id):
        return False
    return True


# 1. GET /api/admin/profiles?status=pending
@admin_bp.route("/profiles", methods=["GET"])
def get_pending_profiles():
    if not _validate_admin():
        return jsonify({"error": "No autorizado"}), 403

    status = request.args.get('status', 'pending')
    profiles = get_profiles_by_status(status)
    return jsonify([dict(p) for p in profiles]), 200


# 2. PUT /api/admin/profiles/<id>/approve
@admin_bp.route("/profiles/<int:profile_id>/approve", methods=["PUT"])
def approve_profile_route(profile_id):
    if not _validate_admin():
        return jsonify({"error": "No autorizado"}), 403

    if not profile_exists(profile_id):
        return jsonify({"error": "Perfil no encontrado"}), 404

    approve_profile(profile_id)
    return jsonify(
        {"message": f"Perfil {profile_id} aprobado exitosamente"}
    ), 200


# 3. GET /api/admin/dashboard
@admin_bp.route('/dashboard', methods=['GET'])
def admin_dashboard():
    if not _validate_admin():
        return jsonify({"error": "No autorizado"}), 403

    stats = get_admin_dashboard_stats()
    return jsonify(stats), 200
