import streamlit as st
import random
import string
import requests
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from theme import apply_global_theme, auth_page_setup

st.set_page_config(page_title="Rakshika-Ai - Register", layout="centered")

# Apply theme
auth_page_setup("Register")
apply_global_theme()


if "users" not in st.session_state:
    st.session_state.users = {}

API_BASE = "http://127.0.0.1:5000/api"

# ---------- HELPER ----------
def generate_username():
    """Generate a fully random username independent of the entered name."""
    letters = ''.join(random.choice(string.ascii_lowercase) for _ in range(4))
    digits = ''.join(random.choice(string.digits) for _ in range(4))
    return f"user{letters}{digits}"

def validate_full_name(name):
    """Validate that full name contains only letters and spaces."""
    if not name:
        return False, "Full name is required"
    
    # Check if name contains only letters and spaces
    if not all(char.isalpha() or char.isspace() for char in name):
        return False, "Full name should contain only letters (no numbers, special characters, or keywords allowed)"
    
    # Check if name has at least one letter
    if not any(char.isalpha() for char in name):
        return False, "Full name must contain at least one letter"
    
    return True, "Valid"

# ---------- UI ----------
st.title("Rakshika-Ai Registration")
st.markdown('<p style="text-align:center; color:#aaa; font-size:14px;">Create your account to join Rakshika-Ai</p>', unsafe_allow_html=True)

with st.form("register_form"):
    full_name = st.text_input("Full Name")
    
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    submit = st.form_submit_button("REGISTER")

# ---------- LOGIC ----------
if submit:
    # Validate full name
    is_valid, validation_msg = validate_full_name(full_name)
    if not is_valid:
        st.error(validation_msg)
    elif not password or not confirm_password:
        st.error("Enter password and confirm password")
    elif password != confirm_password:
        st.error("Passwords do not match")
    else:
        # Auto-generate username
        final_username = generate_username()

        payload = {"name": full_name, "username": final_username, "password": password}
        try:
            r = requests.post(f"{API_BASE}/register", json=payload, timeout=5)
            if r.status_code == 201:
                st.success(f"✓ Registered as {final_username}. Go to Login to sign in.")
            else:
                st.error(r.json().get("error", "Failed to register"))
        except Exception as e:
            st.error(f"Error: {e}")


