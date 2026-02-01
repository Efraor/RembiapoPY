import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    DB_PATH = os.getenv("DB_PATH", "instance/app.sqlite3")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")