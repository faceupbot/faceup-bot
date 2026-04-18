import sqlite3
from config import DATABASE_PATH


def get_conn():
    return sqlite3.connect(DATABASE_PATH)


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT,
                full_name TEXT,
                visit_type TEXT NOT NULL,
                proposed_datetime TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def create_booking(user_id, username, full_name, visit_type, proposed_datetime):
    with get_conn() as conn:
        cur = conn.execute(
            """INSERT INTO bookings (user_id, username, full_name, visit_type, proposed_datetime, status)
               VALUES (?, ?, ?, ?, ?, 'pending')""",
            (user_id, username, full_name, visit_type, proposed_datetime)
        )
        conn.commit()
        return cur.lastrowid


def get_booking_dict(booking_id):
    with get_conn() as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,)).fetchone()
        return dict(row) if row else None


def update_booking_status(booking_id, status):
    with get_conn() as conn:
        conn.execute(
            "UPDATE bookings SET status = ? WHERE id = ?", (status, booking_id)
        )
        conn.commit()


def get_user_active_bookings(user_id):
    with get_conn() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM bookings WHERE user_id = ? AND status IN ('pending', 'confirmed') ORDER BY proposed_datetime",
            (user_id,)
        ).fetchall()
        return [dict(r) for r in rows]
