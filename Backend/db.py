import sqlite3
from pathlib import Path
from config import DB_PATH

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                password_hash TEXT NOT NULL
            );
        """)
        conn.commit()

def query_one(query, args=()):
    conn = get_conn()
    conn.row_factory = sqlite3.Row
    cur = conn.execute(query, args)
    row = cur.fetchone()
    conn.close()
    return row

def execute(query, args=()):
    with get_conn() as conn:
        cur = conn.execute(query, args)
        conn.commit()
        return cur.lastrowid