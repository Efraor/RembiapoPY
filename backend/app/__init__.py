from flask import Flask
from app.routes.main_routes import main_bp

def create_app():
    app = Flask(__name__)

    # Registrar blueprints
    app.register_blueprint(main_bp)

    return app
