from flask import Blueprint, request, jsonify, render_template_string
from models.message_model import Message
from datetime import datetime, timedelta

global_chat_bp = Blueprint("global_chat", __name__, url_prefix="/api")

@global_chat_bp.route("/global-chat/messages", methods=["GET"])
def get_messages():
    try:
        messages = Message.get_all()
        return jsonify({"messages": messages}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@global_chat_bp.route("/location", methods=["GET"])
def capture_location():
    return_url = request.args.get("return_url", "http://127.0.0.1:8501")
    html = """
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>SafeHer Location Capture</title>
        <style>
          body { background: #121212; color: #fff; font-family: Arial, sans-serif; display:flex; align-items:center; justify-content:center; height:100vh; margin:0; }
          .card { max-width: 420px; width: 100%; padding: 24px; border-radius: 16px; background: rgba(255,255,255,0.05); box-shadow: 0 20px 50px rgba(0,0,0,0.35); text-align:center; }
          .status { margin-top: 18px; color: #f5f5f5; }
        </style>
      </head>
      <body>
        <div class="card">
          <h1>Capture your location</h1>
          <p>Requesting browser permission to get your latitude and longitude.</p>
          <p class="status" id="status">Waiting for permission...</p>
        </div>
        <script>
          const returnUrl = {{ return_url|tojson }};
          const status = document.getElementById('status');

          if (!navigator.geolocation) {
            status.textContent = 'Geolocation is not supported by your browser.';
          } else {
            navigator.geolocation.getCurrentPosition(
              function(pos) {
                const lat = pos.coords.latitude.toFixed(5);
                const lon = pos.coords.longitude.toFixed(5);
                const target = new URL(returnUrl);
                target.searchParams.set('geo', lat + ',' + lon);
                window.location.href = target.href;
              },
              function(err) {
                status.textContent = 'Error: ' + err.message + '. Please allow location access and try again.';
              }
            );
          }
        </script>
      </body>
    </html>
    """
    return render_template_string(html, return_url=return_url)

@global_chat_bp.route("/global-chat/send", methods=["POST"])
def send_message():
    data = request.json or {}
    username = data.get("username")
    message = data.get("message")
    location = data.get("location")
    emergency = data.get("emergency", False)

    if not username or not message:
        return jsonify({"error": "Missing username or message"}), 400

    print("Received:", username, message, location, emergency)

    try:
        Message.add(username, message, location, emergency)
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@global_chat_bp.route("/global-chat/cleanup", methods=["DELETE"])
def cleanup_old_messages():
    try:
        days = int(request.args.get("days", 1))  # Default to 1 day
        cutoff_date = datetime.now() - timedelta(days=days)

        # Get all messages and filter old ones
        all_messages = Message.get_all()
        old_messages = []

        for msg in all_messages:
            try:
                msg_time = datetime.strptime(msg["timestamp"], "%Y-%m-%d %H:%M:%S")
                if msg_time < cutoff_date:
                    old_messages.append(msg["id"])
            except:
                continue

        # Delete old messages
        deleted_count = 0
        for msg_id in old_messages:
            if Message.delete_by_id(msg_id):
                deleted_count += 1

        return jsonify({
            "success": True,
            "deleted_count": deleted_count,
            "message": f"Deleted {deleted_count} messages older than {days} days"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500