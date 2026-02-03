from flask import Blueprint, request, jsonify, g
from app.db import get_db

admin_bp = Blueprint('admin', __name__)

# --- NOTA DE SENIOR ---
# En un sistema real, aquí usaríamos el token de la tabla 'sessions' 
# para saber quién es el usuario. Por ahora, para el MVP, 
# simularemos que recibimos un 'user_id' para validar.

def is_admin(user_id):
    db = get_db()
    user = db.execute('SELECT role FROM users WHERE id = ?', (user_id,)).fetchone()
    return user and user['role'] == 'admin'

# 1. GET /api/admin/profiles?status=pending
@admin_bp.route("/profiles", methods=["GET"])
def get_pending_profiles():
    # Validación básica de seguridad (MVP)
    admin_id = request.headers.get('X-Admin-ID') 
    if not is_admin(admin_id):
        return jsonify({"error": "No autorizado"}), 403

    status = request.args.get('status', 'pending')
    db = get_db()
    
    # Traemos los datos del perfil + datos del usuario para que el admin sepa quién es
    query = """
        SELECT p.id, u.name, u.email, p.city, p.whatsapp, p.status, p.updated_at
        FROM profiles p
        JOIN users u ON p.user_id = u.id
        WHERE p.status = ?
    """
    profiles = db.execute(query, (status,)).fetchall()
    return jsonify([dict(p) for p in profiles]), 200

# 2. PUT /api/admin/profiles/<id>/approve
@admin_bp.route("/profiles/<int:profile_id>/approve", methods=["PUT"])
def approve_profile(profile_id):
    admin_id = request.headers.get('X-Admin-ID')
    if not is_admin(admin_id):
        return jsonify({"error": "No autorizado"}), 403

    db = get_db()
    
    # Verificamos si existe el perfil
    profile = db.execute('SELECT id FROM profiles WHERE id = ?', (profile_id,)).fetchone()
    if not profile:
        return jsonify({"error": "Perfil no encontrado"}), 404

    # Actualizamos el estado
    db.execute('UPDATE profiles SET status = "approved" WHERE id = ?', (profile_id,))
    db.commit()
    
    return jsonify({"message": f"Perfil {profile_id} aprobado exitosamente"}), 200

# 3. (Opcional) /api/admin/dashboard - Estadísticas rápidas
@admin_bp.route('/dashboard', methods=['GET'])
def admin_dashboard():
    admin_id = request.headers.get('X-Admin-ID')
    if not is_admin(admin_id):
        return jsonify({"error": "No autorizado"}), 403

    db = get_db()
    stats = {
        "total_users": db.execute('SELECT COUNT(*) as count FROM users').fetchone()['count'],
        "pending_profiles": db.execute('SELECT COUNT(*) as count FROM profiles WHERE status="pending"').fetchone()['count'],
        "total_reports": db.execute('SELECT COUNT(*) as count FROM reports').fetchone()['count']
    }
    return jsonify(stats), 200
