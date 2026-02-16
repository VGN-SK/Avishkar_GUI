import sqlite3
from pathlib import Path


# Path to SQLite database file
DB_PATH = Path("data/users.db")


def get_connection():
    """
    Creates and returns a database connection.
    Row factory allows dictionary-style access.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    """
    Creates all required tables if they do not exist.
    Safe to run multiple times.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # USERS TABLE

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('viewer', 'operator', 'controller')),
            assigned_pod TEXT
        )
    """)


    # PODS TABLE
 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            track_id TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('running', 'stopped', 'maintenance'))
        )
    """)

    # OPERATOR SESSIONS TABLE

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS operator_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operator_id INTEGER NOT NULL,
            pod_id INTEGER NOT NULL,
            session_token TEXT NOT NULL,
            is_active INTEGER NOT NULL CHECK(is_active IN (0,1)),
            FOREIGN KEY(operator_id) REFERENCES users(id),
            FOREIGN KEY(pod_id) REFERENCES pods(id)
        )
    """)

    conn.commit()
    conn.close()

