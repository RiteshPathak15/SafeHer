import streamlit as st
import requests
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from theme import apply_global_theme, auth_page_setup

API_BASE = "http://127.0.0.1:5000/api"

st.set_page_config(page_title="Login", layout="centered")

# Apply theme
auth_page_setup("Login")
apply_global_theme()

# ---------- REDIRECT ----------
if st.session_state.get("logged_in"):
    st.switch_page("pages/2_dashboard.py")

# ---------- UI ----------
st.title("Login")

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("SUBMIT")

# ---------- LOGIC ----------
if submit:
    if not username or not password:
        st.error("Enter both username and password")
    else:
        try:
            r = requests.post(
                f"{API_BASE}/login",
                json={"username": username, "password": password},
                timeout=5
            )
            if r.status_code == 200 and r.json().get("success"):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success(f"Welcome {r.json().get('name')}!")
                st.switch_page("pages/2_dashboard.py")
            else:
                st.error(r.json().get("error", "Invalid credentials"))
        except Exception as e:
            st.error(f"API error: {e}")