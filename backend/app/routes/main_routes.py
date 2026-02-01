from flask import Blueprint, jsonify

# Blueprint = "mini-app" de Flask para agrupar rutas relacionadas.
# Lo registramos luego en create_app() usando app.register_blueprint(...)
main_bp = Blueprint("main", __name__)

@main_bp.route("/api/health")
#  Endpoint de salud (health check).
def health():
    return jsonify({"status": "ok"})
