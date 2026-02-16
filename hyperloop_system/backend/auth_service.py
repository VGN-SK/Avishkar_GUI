import bcrypt
from backend.database import get_connection


# PASSWORD VERIFICATION
def verify_password(plain_password: str, stored_hash: str) -> bool:
    """
    Verifies a plaintext password against stored bcrypt hash.
    """
    return bcrypt.checkpw(
        plain_password.encode(),
        stored_hash.encode()
    )


# AUTHENTICATE USER
def authenticate_user(username: str, password: str):
    """
    Validates user credentials.
    Returns user dictionary if valid.
    Returns None if invalid.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    if user is None:
        return None

    if verify_password(password, user["password_hash"]):
        return dict(user)

    return None

