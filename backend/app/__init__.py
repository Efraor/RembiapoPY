<<<<<<< HEAD
from flask import Flask
from app.routes.main_routes import main_bp

def create_app():
    app = Flask(__name__)

    # Registrar blueprints
    app.register_blueprint(main_bp)

    return app
=======
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from .config import Config
from .db import close_db, init_db, get_db

def create_app() -> Flask:
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app,resources={r"/api/*": {"origins": ["http://127.0.0.1:5500", "http://localhost:5500"]}},
    supports_credentials=True,)


    app.teardown_appcontext(close_db)

    from .routes.main_routes import main_bp
    app.register_blueprint(main_bp, url_prefix="/api")

    from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    @app.get("/api/health")
    def health():
        return jsonify({"ok": True})

    @app.cli.command("init-db")
    def init_db_command():
        init_db()
        print("✅ DB inicializada")

    @app.cli.command("migrate-user-fields")
    def migrate_user_fields():
        db = get_db()
        db.execute("ALTER TABLE users ADD COLUMN name TEXT NOT NULL DEFAULT ''")
        db.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'user'")
        db.commit()
        print("✅ Migración lista: users.name + users.role")

    return app
>>>>>>> diego/main
