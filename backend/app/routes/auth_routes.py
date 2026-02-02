import uuid
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from app.db import get_db

auth_bp = Blueprint('auth', _name_)

@auth_bp.route('/api/auth/google', methods=['POST'])
def google_login():
    data = request.get_json()
    db = get_db()
    
    # Datos que vienen de Google tras el login en el Frontend
    email = data.get('email')
    google_sub = data.get('sub')
    name = data.get('name')
    picture = data.get('picture')

    # 1. Buscar si el usuario ya existe
    user = db.execute('SELECT id, role FROM users WHERE google_sub = ? OR email = ?', 
                     (google_sub, email)).fetchone()

    if not user:
        # 2. Si no existe, lo creamos (Registro automático)
        cursor = db.execute(
            'INSERT INTO users (email, google_sub, name, picture, role) VALUES (?, ?, ?, ?, ?)',
            (email, google_sub, name, picture, 'client')
        )
        db.commit()
        user_id = cursor.lastrowid
        role = 'client'
    else:
        user_id = user['id']
        role = user['role']

    # 3. Crear una Sesión en la tabla 'sessions'
    token = str(uuid.uuid4()) # Genera un token único aleatorio
    expires_at = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')

    db.execute(
        'INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)',
        (token, user_id, expires_at)
    )
    db.commit()

    # 4. Responder al frontend con el token y datos básicos
    return jsonify({
        "token": token,
        "user": {
            "id": user_id,
            "name": name,
            "role": role,
            "picture": picture
        }
    }), 200