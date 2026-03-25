from flask import Blueprint, request, jsonify
from models.chat import Message

chat_bp = Blueprint("chat", __name__, url_prefix="/api")

@chat_bp.route("/chat/messages", methods=["GET"])
def get_messages():
    try:
        messages = Message.get_all()
        return jsonify({"messages": messages}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@chat_bp.route("/chat/send", methods=["POST"])
def send_message():
    data = request.json or {}
    username = data.get("username")
    message = data.get("message")
    location = data.get("location")

    if not username or not message:
        return jsonify({"error": "Missing username or message"}), 400

    try:
        Message.add(username, message, location)
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500