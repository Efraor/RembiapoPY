from app.db import get_db


def get_user_role(user_id):
    db = get_db()
    user = db.execute(
        'SELECT role FROM users WHERE id = ?',
        (user_id,)
    ).fetchone()
    return user['role'] if user else None


def is_admin(user_id):
    return get_user_role(user_id) == 'admin'


def get_profiles_by_status(status):
    db = get_db()
    query = """
        SELECT p.id, u.name, u.email, p.city, p.whatsapp, p.status, p.updated_at
        FROM profiles p
        JOIN users u ON p.user_id = u.id
        WHERE p.status = ?
    """
    return db.execute(query, (status,)).fetchall()


def profile_exists(profile_id):
    db = get_db()
    profile = db.execute(
        'SELECT id FROM profiles WHERE id = ?',
        (profile_id,)
    ).fetchone()
    return profile is not None


def approve_profile(profile_id):
    db = get_db()
    db.execute(
        'UPDATE profiles SET status = "approved" WHERE id = ?',
        (profile_id,)
    )
    db.commit()


def get_admin_dashboard_stats():
    db = get_db()
    return {
        "total_users": db.execute(
            'SELECT COUNT(*) AS count FROM users'
        ).fetchone()['count'],
        "pending_profiles": db.execute(
            'SELECT COUNT(*) AS count FROM profiles WHERE status = "pending"'
        ).fetchone()['count'],
        "total_reports": db.execute(
            'SELECT COUNT(*) AS count FROM reports'
        ).fetchone()['count'],
    }
