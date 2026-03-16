import streamlit as st
import requests

API_BASE = "http://127.0.0.1:5000/api"

st.title("SafeHer - Login")
with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Login")

if submit:
    if not username or not password:
        st.error("Enter both username and password")
    else:
        try:
            r = requests.post(f"{API_BASE}/login", json={"username": username, "password": password}, timeout=5)
            if r.status_code == 200 and r.json().get("success"):
                st.success(f"Welcome {r.json().get('name')}")
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
            else:
                st.error(r.json().get("error", "Invalid credentials"))
        except Exception as e:
            st.error(f"API error: {e}")