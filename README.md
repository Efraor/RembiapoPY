# RembiapoPY

Marketplace de servicios: los usuarios buscan profesionales (electricistas,
plomeros, tecnicos, etc.) y los profesionales publican su perfil.

## Funcionalidades principales

- Login local (email/password)
- Login con Google (OAuth 2.0)
- Sesion con token en DB + cookie HttpOnly
- Perfil editable (cliente/profesional)
- Listado de profesionales por categoria
- Buscador con autocompletado de categorias
- Frontend responsive

## Stack

Backend:
- Python + Flask
- SQLite
- Google OAuth (google-auth)

Frontend:
- HTML + CSS + JS
- Google Identity Services

## Estructura

```
backend/
  app/
    routes/       # Endpoints HTTP
    models/       # Acceso a datos (SQLite)
    services/     # Logica de negocio
  schema/         # schema.sql y seed.sql
frontend/
  src/
    pages/        # HTML
    js/           # JS (api, auth, profiles, listings)
    css/          # estilos
```

## Configuracion

Variables (opcional) en `.env`:
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REDIRECT_URI`
- `FRONTEND_REDIRECT_URL`
- `DB_PATH` (default: `instance/app.sqlite3`)

## Base de datos

Crear DB y cargar seed:
```
python backend/setup_db.py
sqlite3 backend/instance/app.sqlite3 ".read backend/schema/seed.sql"
```

## Ejecutar

Backend:
```
python backend/run.py
```

Frontend:
- Abrir `frontend/src/pages/login.html` o `menu_basico.html`

## Endpoints clave

- `GET /api/me` -> usuario de la sesion
- `POST /api/auth/google` -> login Google
- `POST /api/users/login` -> login local
- `POST /api/users/register` -> registro local
- `GET /api/profiles` -> lista profesionales (opcional `category`, `limit`)
- `GET /api/profile` -> perfil del usuario
- `POST /api/profile` -> guarda perfil
- `GET /api/categories` -> categorias disponibles

## Flujo (alto nivel)

1. Usuario inicia sesion (local o Google).
2. Se crea sesion en DB y se setea cookie.
3. El frontend usa `/api/me` para validar sesion.
4. En perfil, el usuario edita y guarda con `/api/profile`.
5. El home lista profesionales y categorias.
