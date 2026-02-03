from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from .config import Config
from .db import close_db, init_db, get_db

def create_app() -> Flask:
    # Cargar variables de entorno desde .env
    load_dotenv()

    # Crear app
    app = Flask(__name__)
    app.config.from_object(Config)

    # CORS (necesario si el frontend corre en 5500 y usÃ¡s cookies/sesiÃ³n)
    CORS(
        app,
        resources={r"/api/*": {"origins": ["http://127.0.0.1:5500", "http://localhost:5500"]}},
        supports_credentials=True,
    )

    # Cerrar DB al final de cada request
    app.teardown_appcontext(close_db)

    # -------- Blueprints --------
    from .routes.main_routes import main_bp
    app.register_blueprint(main_bp, url_prefix="/api")

    from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    from .routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    from .routes.profiles_routes import profile_bp
    app.register_blueprint(profile_bp)

    from .routes.admin_routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    # -------- CLI Commands --------
    @app.cli.command("init-db")
    def init_db_command():
        """Inicializa la base de datos (schema.sql)."""
        init_db()
        print("âœ… DB inicializada")

    @app.cli.command("migrate-user-fields")
    def migrate_user_fields():
        """Agrega columnas name y role a users (si no existen)."""
        db = get_db()
        db.execute("ALTER TABLE users ADD COLUMN name TEXT NOT NULL DEFAULT ''")
        db.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'user'")
        db.commit()
        print("âœ… MigraciÃ³n lista: users.name + users.role")

    return app