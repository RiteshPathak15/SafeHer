import sqlite3
from db import get_conn, execute
from cryptography.fernet import Fernet
from config import ENCRYPTION_KEY

try:
    cipher = Fernet(ENCRYPTION_KEY.encode())
except Exception:
    cipher = None  # Fallback to no encryption if key is invalid

class Message:
    @staticmethod
    def get_all():
        conn = get_conn()
        conn.row_factory = sqlite3.Row
        cur = conn.execute("SELECT * FROM messages ORDER BY timestamp ASC")
        rows = cur.fetchall()
        conn.close()
        messages = []
        for row in rows:
            msg = dict(row)
            if cipher:
                try:
                    msg["message"] = cipher.decrypt(msg["message"].encode()).decode()
                except Exception:
                    pass
                if msg.get("location"):
                    try:
                        msg["location"] = cipher.decrypt(msg["location"].encode()).decode()
                    except Exception:
                        pass
            messages.append(msg)
        return messages

    @staticmethod
    def add(username, message, location=None, emergency=False):
        if cipher:
            encrypted_message = cipher.encrypt(message.encode()).decode()
            encrypted_location = cipher.encrypt(location.encode()).decode() if location else None
        else:
            encrypted_message = message
            encrypted_location = location
        execute(
            "INSERT INTO messages (username, message, location, emergency) VALUES (?, ?, ?, ?)",
            (username, encrypted_message, encrypted_location, int(emergency))
        )

    @staticmethod
    def delete_by_id(message_id):
        """Delete a message by its ID"""
        try:
            execute("DELETE FROM messages WHERE id = ?", (message_id,))
            return True
        except Exception:
            return False

    @staticmethod
    def get_by_id(message_id):
        """Get a specific message by ID"""
        conn = get_conn()
        conn.row_factory = sqlite3.Row
        cur = conn.execute("SELECT * FROM messages WHERE id = ?", (message_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            msg = dict(row)
            if cipher:
                try:
                    msg["message"] = cipher.decrypt(msg["message"].encode()).decode()
                except Exception:
                    pass
                if msg.get("location"):
                    try:
                        msg["location"] = cipher.decrypt(msg["location"].encode()).decode()
                    except Exception:
                        pass
            return msg
        return None