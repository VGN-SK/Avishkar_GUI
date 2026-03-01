import sqlite3
import time
from backend.database import get_connection


def lock_pod(pod_name: str, operator: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pod_locks WHERE pod_name = ?", (pod_name,))
    existing = cursor.fetchone()

    if existing:
        conn.close()
        return False, existing[1]  # locked_by

    cursor.execute(
        "INSERT INTO pod_locks VALUES (?, ?, ?)",
        (pod_name, operator, time.time())
    )

    conn.commit()
    conn.close()

    return True, operator


def unlock_pod(pod_name: str, operator: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT locked_by FROM pod_locks WHERE pod_name = ?",
        (pod_name,)
    )

    row = cursor.fetchone()

    if row and row[0] == operator:
        cursor.execute(
            "DELETE FROM pod_locks WHERE pod_name = ?",
            (pod_name,)
        )
        conn.commit()
        conn.close()
        return True

    conn.close()
    return False


def get_lock_status(pod_name: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT locked_by FROM pod_locks WHERE pod_name = ?",
        (pod_name,)
    )

    row = cursor.fetchone()
    conn.close()

    if row:
        return True, row[0]

    return False, None
