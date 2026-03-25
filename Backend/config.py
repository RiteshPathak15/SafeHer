from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "users.db"

load_dotenv(BASE_DIR / ".env")

FLASK_DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"
FLASK_HOST = os.getenv("FLASK_HOST", "127.0.0.1")
FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))

# Encryption key for chat messages
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    try:
        from cryptography.fernet import Fernet
        ENCRYPTION_KEY = Fernet.generate_key().decode()
    except ImportError:
        ENCRYPTION_KEY = None  # No encryption if cryptography not available
