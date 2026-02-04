import os
import sqlite3
from flask import g, current_app


def get_db() -> sqlite3.Connection:

    # Devuelve una conexión SQLite reutilizable por request
    # Nos aseguramos de que exista la carpeta instance/ para la base de datos
    # SQLite no aplica foreign keys por defecto, se activan manualmente

    if "db" not in g:
        db_path = current_app.config["DB_PATH"]

        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")

        g.db = conn

    return g.db

def close_db(_=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_db():
    
     # Inicializa la base de datos ejecutando el schema.sql

    db = get_db()

    backend_root = os.path.abspath(os.path.join(current_app.root_path, ".."))
    schema_path = os.path.join(backend_root, "schema", "schema.sql")

    with open(schema_path, "r", encoding="utf-8") as f:
        db.executescript(f.read())

    db.commit()