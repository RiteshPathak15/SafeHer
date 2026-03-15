import streamlit as st
import random
import string
import requests

st.set_page_config(page_title="SafeHer - Register", layout="wide")

st.title("SafeHer User Registration")
st.write("Fill in your details and generate a random username.")

if "users" not in st.session_state:
    st.session_state.users = {}

with st.form("register_form"):
    full_name = st.text_input("Full Name")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    submit = st.form_submit_button("Register")

if submit:
    if not full_name.strip() or not password:
        st.error("Name and password are required")
    elif password != confirm_password:
        st.error("Passwords do not match")
    else:
        # force alpha+numeric mix by generating a random prefix with at least one digit and one letter
        letters = ''.join(random.choice(string.ascii_lowercase) for _ in range(2))
        digits = ''.join(random.choice(string.digits) for _ in range(2))
        random_prefix = ''.join(random.sample(letters + digits, 4))
        username = f"{random_prefix}{full_name.split()[0].lower()}"
        # ensure unique
        i = 0
        base_username = username
        while username in st.session_state.users:
            i += 1
            username = f"{base_username}{i}"

        st.session_state.users[username] = {
            "name": full_name,
            "password": password
        }
        user_payload = {"name": full_name, "username": username, "password": password}
        r = requests.post("http://127.0.0.1:5000/api/register", json=user_payload, timeout=5)
        if r.ok:
            st.success(f"Registered: {username}")
        else:
            st.error(r.json().get("error", "Failed"))
        st.info("Use this username on login page.")

if st.session_state.users:
    st.markdown("### Registered users (names hidden)")
    st.write([u for u in st.session_state.users.keys()])
