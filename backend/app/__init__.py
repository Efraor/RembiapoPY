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

    from .routes.profile_routes import profile_bp
    app.register_blueprint(profile_bp, url_prefix="/api")

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
        print("Migracion lista: users.name + users.role")

    @app.cli.command("migrate-profiles")
    def migrate_profiles():
        db = get_db()
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS profiles (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER NOT NULL UNIQUE,
              full_name TEXT NOT NULL DEFAULT '',
              role TEXT NOT NULL DEFAULT 'user',
              category TEXT NOT NULL DEFAULT '',
              service_title TEXT NOT NULL DEFAULT '',
              phone TEXT NOT NULL DEFAULT '',
              whatsapp TEXT NOT NULL DEFAULT '',
              email TEXT NOT NULL DEFAULT '',
              city TEXT NOT NULL DEFAULT '',
              bio TEXT NOT NULL DEFAULT '',
              photo_url TEXT NOT NULL DEFAULT '',
              created_at TEXT NOT NULL DEFAULT (datetime('now')),
              updated_at TEXT NOT NULL DEFAULT (datetime('now')),
              FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """
        )
        db.commit()
        print("Migracion lista: profiles")

    return app
