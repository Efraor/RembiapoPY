from datetime import datetime, timezone
from ..db import get_db


def get_user_by_session_token(token: str):
    if not token:
        return None

    db = get_db()
    row = db.execute(
        """
        SELECT u.id, u.name, u.email, u.role, s.expires_at
        FROM sessions s
        JOIN users u ON u.id = s.user_id
        WHERE s.token = ?
        """,
        (token,),
    ).fetchone()

    if not row:
        return None

    try:
        exp_dt = datetime.fromisoformat(row["expires_at"])
        if exp_dt.tzinfo is None:
            exp_dt = exp_dt.replace(tzinfo=timezone.utc)
    except Exception:
        return None

    if exp_dt <= datetime.now(timezone.utc):
        return None

    return {
        "id": row["id"],
        "name": row["name"] or "",
        "email": row["email"],
        "role": row["role"] or "user",
    }


def delete_session(token: str):
    if not token:
        return

    db = get_db()
    db.execute("DELETE FROM sessions WHERE token = ?", (token,))
    db.commit()
