from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import query_one, execute

auth_bp = Blueprint("auth", __name__, url_prefix="/api")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json or {}
    name = data.get("name")
    username = data.get("username")
    password = data.get("password")

    if not all([name, username, password]):
        return jsonify({"error": "Missing fields"}), 400

    try:
        password_hash = generate_password_hash(password)
        execute(
            "INSERT INTO users (username, name, password_hash) VALUES (?, ?, ?)",
            (username.strip(), name.strip(), password_hash)
        )
        return jsonify({"success": True, "username": username}), 201
    except Exception as e:
        if "UNIQUE constraint" in str(e):
            return jsonify({"error": "Username already exists"}), 409
        return jsonify({"error": "Database error"}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")

    if not all([username, password]):
        return jsonify({"error": "Missing fields"}), 400

    user = query_one("SELECT * FROM users WHERE username=? LIMIT 1", (username.strip(),))
    if user and check_password_hash(user["password_hash"], password):
        return jsonify({"success": True, "name": user["name"], "username": user["username"]})
    return jsonify({"error": "Invalid credentials"}), 401