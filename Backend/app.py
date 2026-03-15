from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from pathlib import Path

app = Flask(__name__)
DB = Path(__file__).resolve().parent / "users.db"

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            name TEXT,
            password_hash TEXT
        )""")
init_db()

def query_db(query, args=(), one=False):
    with sqlite3.connect(DB) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute(query, args)
        rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json or {}
    name = data.get("name")
    username = data.get("username")
    password = data.get("password")
    if not name or not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    try:
        password_hash = generate_password_hash(password)
        with sqlite3.connect(DB) as conn:
            conn.execute(
                "INSERT INTO users (username, name, password_hash) VALUES (?, ?, ?)",
                (username, name, password_hash)
            )
        return jsonify({"success": True, "username": username}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username exists"}), 409

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    user = query_db("SELECT * FROM users WHERE username=?", (username,), one=True)
    if user and check_password_hash(user["password_hash"], password):
        return jsonify({"success": True, "name": user["name"]})
    return jsonify({"error": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(debug=True, port=5000)