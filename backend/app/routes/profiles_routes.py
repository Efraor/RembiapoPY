from flask import Blueprint, request, jsonify
from app.models.profile_models import (
    get_approved_profiles,
    create_profile,
    approve_profile,
    list_categories,
)

profile_bp = Blueprint('profile', __name__)


# GET /api/profile
# Listar profesionales aprobados (con filtros)
@profile_bp.route('/api/profile', methods=['GET'])
def get_profiles():
    city = request.args.get('city')
    category_id = request.args.get('category_id')

    profiles = get_approved_profiles(city, category_id)
    return jsonify([dict(p) for p in profiles]), 200


# GET /api/categories
@profile_bp.route('/api/categories', methods=['GET'])
def get_categories():
    categories = list_categories()
    return jsonify({"ok": True, "categories": categories}), 200


# POST /api/profiles
# Crear perfil profesional (pendiente de aprobación)
@profile_bp.route('/api/profiles', methods=['POST'])
def create_profile_route():
    data = request.get_json() or {}

    required_fields = ['user_id', 'category_id', 'bio', 'city', 'whatsapp']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    try:
        create_profile(
            data['user_id'],
            data['category_id'],
            data['bio'],
            data['city'],
            data['whatsapp'],
        )
        return jsonify(
            {"message": "Perfil creado y pendiente de aprobación"}
        ), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# PUT /api/admin/approve-profile/<id>
@profile_bp.route('/api/admin/approve-profile/<int:profile_id>', methods=['PUT'])
def approve_profile_route(profile_id):
    # ⚠️ aquí debería validarse admin (más adelante)
    approve_profile(profile_id)
    return jsonify({"message": "Perfil aprobado exitosamente"}), 200
