from db.sqlite_db import get_connection

def save_message(user_id, role, content):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)",
        (user_id, role, content)
    )

    conn.commit()
    conn.close()

def get_messages(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role, content FROM messages WHERE user_id = ?",
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return [{"role": r[0], "content": r[1]} for r in rows]


def save_persona(user_id, persona):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM persona WHERE user_id = ?", (user_id,))

    cursor.execute(
        "INSERT INTO persona (user_id, type, risk, goal) VALUES (?, ?, ?, ?)",
        (user_id, persona["type"], persona["risk"], persona["goal"])
    )

    conn.commit()
    conn.close()


def get_persona(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT type, risk, goal FROM persona WHERE user_id = ?",
        (user_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if row:
        return {"type": row[0], "risk": row[1], "goal": row[2]}
    return None