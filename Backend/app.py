from flask import Flask, jsonify
from flask_cors import CORS
from config import FLASK_DEBUG, FLASK_HOST, FLASK_PORT
from db import init_db
from routes.auth import auth_bp
from routes.chat import chat_bp

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)

    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok"})

    init_db()
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)