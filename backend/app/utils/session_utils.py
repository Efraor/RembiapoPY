"""Session cookie helpers."""
from flask import current_app, request


def session_cookie_name() -> str:
    return current_app.config.get("SESSION_COOKIE_NAME", "rembiapy_session")


def set_session_cookie(resp, token: str):
    resp.set_cookie(
        session_cookie_name(),
        token,
        httponly=True,
        samesite="Lax",
        secure=False,
        max_age=60 * 60 * 24,
        path="/",
    )


def clear_session_cookie(resp):
    resp.set_cookie(session_cookie_name(), "", expires=0, path="/")


def get_session_token_from_cookie() -> str:
    return request.cookies.get(session_cookie_name(), "") or ""