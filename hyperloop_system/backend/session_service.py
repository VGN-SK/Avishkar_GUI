import uuid
from backend.database import get_connection



# CHECK IF POD IS LOCKED - BEFORE ASSIGNING IT TO AN OPERATOR

def is_pod_locked(pod_id: int) -> bool:
    """
    Returns True if pod currently has an active operator session.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM operator_sessions
        WHERE pod_id = ? AND is_active = 1
    """, (pod_id,))

    session = cursor.fetchone()
    conn.close()

    return session is not None


# CREATE OPERATOR SESSION

def create_operator_session(operator_id: int, pod_id: int):
    """
    Creates a new session if pod is not already locked.
    Returns session token if successful.
    Returns None if pod is already locked.
    """
    if is_pod_locked(pod_id):
        return None

    conn = get_connection()
    cursor = conn.cursor()

    session_token = str(uuid.uuid4())

    cursor.execute("""
        INSERT INTO operator_sessions
        (operator_id, pod_id, session_token, is_active)
        VALUES (?, ?, ?, 1)
    """, (operator_id, pod_id, session_token))

    conn.commit()
    conn.close()

    return session_token


# END OPERATOR SESSION

def end_operator_session(session_token: str):
    """
    Deactivates an operator session.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE operator_sessions
        SET is_active = 0
        WHERE session_token = ?
    """, (session_token,))

    conn.commit()
    conn.close()


# GET CURRENT ACTIVE SESSION OF AN OPERATOR 

def get_active_session(operator_id: int):
    """
    Returns active session for operator if exists.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM operator_sessions
        WHERE operator_id = ? AND is_active = 1
    """, (operator_id,))

    session = cursor.fetchone()
    conn.close()

    if session:
        return dict(session)

    return None

