import bcrypt
from backend.database import get_connection


#  function to hash password
def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.
    Returns the hashed password as a string.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


# USER CREATION

def create_user(username: str, password: str, role: str):
    """
    Creates a new user with hashed password.
    """
    conn = get_connection()
    cursor = conn.cursor()

    password_hash = hash_password(password)

    cursor.execute("""
        INSERT INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
    """, (username, password_hash, role))

    conn.commit()
    conn.close()


# FETCH USER

def get_user_by_username(username: str):
    """
    Returns user row as dictionary or None.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return dict(user)

    return None


# ADDING SOME DEFAULT USER CREDENTIALS - REST CAN BE CREATED LATER .. MOSTLY VIA CONTROLLER UI

def seed_default_users():
    """
    Inserts default users if table is empty.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as count FROM users")
    count = cursor.fetchone()["count"]

    conn.close()

    if count == 0:
        create_user("viewer1", "viewerpass", "viewer")
        create_user("operator1", "operatorpass", "operator")
        create_user("controller1", "controllerpass", "controller")

