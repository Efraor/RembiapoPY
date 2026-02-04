from werkzeug.security import check_password_hash

from app.db import get_db
from app.models.user_model import create_user_local, find_user_by_email


def test_create_user_local_hashes_password(app):
    with app.app_context():
        user_id = create_user_local("test@example.com", "secret123")
        assert user_id is not None

        user = find_user_by_email("test@example.com")
        assert user is not None
        assert user["password_hash"] != "secret123"
        assert check_password_hash(user["password_hash"], "secret123")
