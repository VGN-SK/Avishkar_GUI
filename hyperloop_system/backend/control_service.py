import sqlite3
from backend.database import get_connection


def set_control_state(pod_name, velocity, brake_state):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pod_controls (pod_name, desired_velocity, brake_state)
        VALUES (?, ?, ?)
        ON CONFLICT(pod_name)
        DO UPDATE SET
            desired_velocity = excluded.desired_velocity,
            brake_state = excluded.brake_state
    """, (pod_name, velocity, brake_state))

    conn.commit()
    conn.close()


def get_control_state(pod_name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT desired_velocity
        FROM pod_controls
        WHERE pod_name = ?
    """, (pod_name,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return row[0]

    return None
    
def set_desired_velocity(pod_name, velocity):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pod_controls (pod_name, desired_velocity)
        VALUES (?, ?)
        ON CONFLICT(pod_name)
        DO UPDATE SET
            desired_velocity = excluded.desired_velocity
    """, (pod_name, velocity))

    conn.commit()
    conn.close()
