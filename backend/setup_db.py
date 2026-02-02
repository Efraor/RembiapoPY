import sqlite3
import os

# Definimos las rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(BASE_DIR, 'schema', 'schema.sql')
DB_PATH = os.path.join(BASE_DIR, 'instance', 'app.sqlite3')
INSTANCE_DIR = os.path.join(BASE_DIR, 'instance')

def create_db():
    # 1. Asegurarnos de que la carpeta 'instance' exista
    if not os.path.exists(INSTANCE_DIR):
        os.makedirs(INSTANCE_DIR)
        print(f"✅ Carpeta creada: {INSTANCE_DIR}")

    # 2. Conectar a la base de datos (se crea el archivo si no existe)
    try:
        conn = sqlite3.connect(DB_PATH)
        print(f"✅ Archivo de base de datos listo.")

        # 3. Leer y ejecutar el archivo schema.sql
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            sql_script = f.read()
            conn.executescript(sql_script)
        
        conn.commit()
        print("🚀 ¡Tablas creadas exitosamente!")

    except Exception as e:
        print(f"❌ Error al crear la base de datos: {e}")
    
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_db()