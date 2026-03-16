import streamlit as st
import random
import string
import requests

st.set_page_config(page_title="SafeHer - Register", layout="wide")

st.title("SafeHer User Registration")
st.write("Fill in your details and generate a random username.")

if "users" not in st.session_state:
    st.session_state.users = {}

API_BASE = "http://127.0.0.1:5000/api"

with st.form("register_form"):
    full_name = st.text_input("Full Name")
    username_requested = st.text_input("Desired Username (optional)")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    submit = st.form_submit_button("Register")

if submit:
    if not full_name or not password or not confirm_password:
        st.error("Enter name/password and confirm password")
    elif password != confirm_password:
        st.error("Passwords do not match")
    else:
        if not username_requested:
            letters = ''.join(random.choice(string.ascii_lowercase) for _ in range(2))
            digits = ''.join(random.choice(string.digits) for _ in range(2))
            username_requested = f"{letters}{digits}{full_name.split()[0].lower()}"

        payload = {"name": full_name, "username": username_requested, "password": password}
        try:
            r = requests.post(f"{API_BASE}/register", json=payload, timeout=5)
            if r.status_code == 201:
                st.success(f"Registered user {username_requested}. Login now.")
            else:
                st.error(r.json().get("error", "Failed to register"))
        except Exception as e:
            st.error(f"Error contacting API: {e}")

if st.session_state.users:
    st.markdown("### Registered users (names hidden)")
    st.write([u for u in st.session_state.users.keys()])
