-- schema/schema.sql

-- 1. Tabla de Usuarios (Soporte Google y Manual)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    google_sub TEXT UNIQUE,
    password_hash TEXT,
    name TEXT NOT NULL,
    picture TEXT,
    role TEXT CHECK(role IN ('client', 'pro', 'admin')) DEFAULT 'client',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_auth_method CHECK (google_sub IS NOT NULL OR password_hash IS NOT NULL)
);

-- 2. Tabla de Categorías
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

-- 3. Tabla de Perfiles Profesionales
CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    category_id INTEGER NOT NULL,
    bio TEXT,
    city TEXT NOT NULL,
    whatsapp TEXT NOT NULL,
    status TEXT CHECK(status IN ('pending', 'approved')) DEFAULT 'pending',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- 4. Tabla de Reportes
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reporter_id INTEGER NOT NULL,
    profile_id INTEGER NOT NULL,
    reason TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reporter_id) REFERENCES users(id),
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);

-- 5. Tabla de Sessiones
CREATE TABLE IF NOT EXISTS sessions (
  token TEXT PRIMARY KEY,
  user_id INTEGER NOT NULL,
  expires_at TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Datos iniciales obligatorios
INSERT OR IGNORE INTO categories (name) VALUES 
('Plomería'), ('Electricidad'), ('Limpieza'), ('Carpintería'), ('Flete');