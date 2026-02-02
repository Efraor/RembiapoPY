import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    DB_PATH = os.getenv("DB_PATH", "instance/app.sqlite3")

    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "")
    FRONTEND_REDIRECT_URL = os.getenv("FRONTEND_REDIRECT_URL", "http://127.0.0.1:5500/")

    # cookie de sesión (nombre único)
    SESSION_COOKIE_NAME = "rembiapy_session"