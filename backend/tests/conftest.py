import os
import sys
import types

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if "flask_cors" not in sys.modules:
    cors_stub = types.ModuleType("flask_cors")
    cors_stub.CORS = lambda *args, **kwargs: None
    sys.modules["flask_cors"] = cors_stub

if "google" not in sys.modules:
    google_stub = types.ModuleType("google")
    oauth2_stub = types.ModuleType("google.oauth2")
    id_token_stub = types.ModuleType("google.oauth2.id_token")
    id_token_stub.verify_oauth2_token = lambda *args, **kwargs: {}

    auth_stub = types.ModuleType("google.auth")
    transport_stub = types.ModuleType("google.auth.transport")
    requests_stub = types.ModuleType("google.auth.transport.requests")

    class DummyRequest:
        pass

    requests_stub.Request = DummyRequest
    transport_stub.requests = requests_stub
    auth_stub.transport = transport_stub

    google_stub.oauth2 = oauth2_stub
    oauth2_stub.id_token = id_token_stub

    sys.modules["google"] = google_stub
    sys.modules["google.oauth2"] = oauth2_stub
    sys.modules["google.oauth2.id_token"] = id_token_stub
    sys.modules["google.auth"] = auth_stub
    sys.modules["google.auth.transport"] = transport_stub
    sys.modules["google.auth.transport.requests"] = requests_stub

from app import create_app
from app.db import init_db


@pytest.fixture()
def app(tmp_path):
    app = create_app()
    app.config["TESTING"] = True
    app.config["DB_PATH"] = str(tmp_path / "test.sqlite3")
    with app.app_context():
        init_db()
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
