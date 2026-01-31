proyecto/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py              # create_app(), registra blueprints
│   │   ├── config.py                # configuración (SECRET_KEY, DB_PATH)
│   │   ├── db.py                    # conexión SQLite + helpers
│   │   ├── models/                  # lógica de acceso a datos (SQL)
│   │   │   ├── user_model.py
│   │   │   ├── profile_model.py
│   │   │   └── favorites_model.py   # opcional
│   │   ├── routes/                  # endpoints (blueprints)
│   │   │   ├── auth_routes.py
│   │   │   ├── profile_routes.py
│   │   │   └── main_routes.py
│   │   ├── services/                # lógica de negocio (no SQL directo)
│   │   │   ├── auth_service.py
│   │   │   └── profile_service.py
│   │   ├── utils/
│   │   │   ├── validators.py        # validaciones (whatsapp, etc.)
│   │   │   └── helpers.py
│   │   └── templates/               # HTML renderizado por Flask (si usan SSR)
│   │       └── (opcional)           # (recomendación: NO usar, front separado)
│   │
│   ├── instance/
│   │   └── app.sqlite3              # base de datos (se genera)
│   │
│   ├── migrations/                  # opcional si usan migraciones (no necesario)
│   │
│   ├── schema/
│   │   ├── schema.sql               # creación de tablas
│   │   └── seed.sql                 # datos de ejemplo para demo
│   │
│   ├── tests/                       # opcional
│   │
│   ├── run.py                       # entrypoint: flask run / python run.py
│   ├── requirements.txt
│   ├── .env                         # SECRET_KEY, etc.
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── index.html           # Home
│   │   │   ├── search.html          # Resultados
│   │   │   ├── profile.html         # Perfil profesional
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   │   ├── publish.html         # Crear/editar perfil
│   │   │   └── favorites.html       # opcional
│   │   │
│   │   ├── components/              # piezas reutilizables
│   │   │   ├── navbar.html
│   │   │   ├── bottom_nav.html
│   │   │   ├── pro_card.html
│   │   │   ├── category_card.html
│   │   │   └── modal_filters.html
│   │   │
│   │   ├── js/
│   │   │   ├── api.js               # fetch() centralizado
│   │   │   ├── auth.js              # login/register/logout
│   │   │   ├── profiles.js          # listar/buscar/detalle
│   │   │   ├── publish.js           # crear/editar perfil
│   │   │   ├── favorites.js         # opcional
│   │   │   └── ui.js                # helpers de UI (toasts, loaders)
│   │   │
│   │   └── css/
│   │       └── input.css            # tailwind input
│   │
│   ├── public/
│   │   ├── assets/
│   │   │   ├── icons/
│   │   │   └── images/
│   │   └── favicon.ico
│   │
│   ├── dist/
│   │   ├── css/styles.css           # salida compilada tailwind
│   │   └── (html copiados)          # salida final para servir
│   │
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── package.json
│   └── README.md
│
├── docs/
│   ├── pitch.md                     # guion demo/presentación
│   ├── api_contract.md              # endpoints + payloads
│   └── screenshots/                 # capturas para demo
│
├── .gitignore
└── README.md                        # README general del proyecto
