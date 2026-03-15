import streamlit as st
import requests

st.set_page_config(page_title="SafeHer - Login", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.title("SafeHer - Login")
st.write("Please sign in to access SafeHer modules.")

users = {
    "admin": "1234",
    "user": "pass"
}

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

def safe_rerun():
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        try:
            from streamlit.runtime.scriptrunner import RerunException
            raise RerunException
        except Exception:
            st.warning("Page refresh required: reload manually.")

if submitted:
    r = requests.post("http://127.0.0.1:5000/api/login", json={"username": username, "password": password}, timeout=5)
    if r.ok and r.json().get("success"):
        st.session_state.logged_in = True
        st.success("Login successful")
        safe_rerun()
    else:
        st.error("Invalid username or password")

if st.session_state.logged_in:
    st.success("You are already logged in.")
    if st.button("Logout"):
        st.session_state.logged_in = False
        safe_rerun()

st.write("\n")
if st.button("Go to Register"):
    st.info("Switch to Register using sidebar for now.")