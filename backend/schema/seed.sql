-- schema/seed.sql

-- 0. Categorias base
INSERT OR IGNORE INTO categories (name) VALUES
('Plomeria'),
('Electricidad'),
('Limpieza'),
('Carpinteria'),
('Flete'),
('Pintura'),
('Jardineria'),
('Mudanzas'),
('Cerrajeria'),
('Gasista'),
('Albanileria');

-- 1. Insertar Administrador (Registro Manual)
INSERT INTO users (id, email, name, password_hash, role) 
VALUES (1, 'admin@rembiapo.com', 'Admin Rembiapo', 'pbkdf2:sha256:260000$examplehash', 'admin');

-- 2. Insertar Profesional Aprobado (Registro vía Google OAuth)
INSERT INTO users (id, email, name, google_sub, role, picture) 
VALUES (2, 'juan.perez@gmail.com', 'Juan Pérez', '10987654321', 'pro', 'https://api.dicebear.com/7.x/avataaars/svg?seed=Juan');

INSERT INTO profiles (user_id, category_id, bio, city, whatsapp, status) 
VALUES (2, 1, 'Plomero certificado. Especialista en instalaciones de alta presión y detección de fugas.', 'Asunción', '595981123456', 'approved');

-- 3. Insertar Profesional Pendiente (Registro Manual)
INSERT INTO users (id, email, name, password_hash, role) 
VALUES (3, 'marta.limpieza@mail.com', 'Marta Gómez', 'hash_marta_seguro', 'pro');

INSERT INTO profiles (user_id, category_id, bio, city, whatsapp, status) 
VALUES (3, 3, 'Limpieza profunda de oficinas y residencias particulares. Disponibilidad inmediata.', 'San Lorenzo', '595971987654', 'pending');

-- 4. Crear una Sesión de prueba para el Admin (Vence en el 2026)
INSERT INTO sessions (token, user_id, expires_at)
VALUES ('session_token_secreto_123', 1, '2026-12-31 23:59:59');
