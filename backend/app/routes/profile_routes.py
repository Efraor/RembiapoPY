from flask import Blueprint, request, jsonify
from app.db import get_db

profile_bp = Blueprint('profile',__name__)

#GET /api/profiles-Listar profesionales aprobados

@profile_bp.route('/api/profile', methods= ['GET'])
def get_profile():
    db = get_db()

    #Filtros opcional por ciudad o categoria via URB (?City=Asuncion)
    city = request.args.get('city')
    category_id = request.args.get('category_id')

    query= """
        SELECT u.name, u.picture, p.bio, p.city, p.whatsapp, c.name as category
        FROM profiles p
        JOIN users u ON p.user_id = u.id
        JOIN categories c ON p.category_id = c.id
        WHERE p.status = "approved"
    """
    params= []

    if city:
        query += "AND p.city = ?"
        params.append(city)
    if category_id:
        query += "AND p.category_id = ?"

    profiles = db.execute(query, params).fetchall()
    
    #Convertir de objetos ROW a lista de diccionarios para json 
    return jsonify ([dict(p)for p in profiles]), 200
# POST /api/profiles - Crear perfil profesional (Nuevo Pro)
@profile_bp.route('/api/profiles', methods=['POST'])
def create_profile():
    data = request.get_json()
    db = get_db()
    
    # Nota: Aquí deberías validar la sesión antes de permitir crear el perfil
    try:
        db.execute(
            """INSERT INTO profiles (user_id, category_id, bio, city, whatsapp)
               VALUES (?, ?, ?, ?, ?)""",
            (data['user_id'], data['category_id'], data['bio'], data['city'], data['whatsapp'])
        )
        db.commit()
        return jsonify({"message": "Perfil creado y pendiente de aprobación"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    #implementación de Moderación (Admin)

    # PUT /api/admin/approve-profile/<id>
@profile_bp.route('/api/admin/approve-profile/<int:profile_id>', methods=['PUT'])
def approve_profile(profile_id):
    db = get_db()
    # Aquí faltaría validar que el usuario que hace la petición sea 'admin'
    
    db.execute("UPDATE profiles SET status = 'approved' WHERE id = ?", (profile_id,))
    db.commit()
    
    return jsonify({"message": "Perfil aprobado exitosamente"}), 200