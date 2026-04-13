import streamlit as st
import requests

API_BASE = "http://127.0.0.1:5000/api"

st.set_page_config(page_title="Login", layout="centered")

# ---------- CSS ----------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(90deg, #1f2a38, #0a0f1a);
}

/* Main container becomes card */
.block-container {
    max-width: 500px;
    margin-top: 100px;
    padding: 40px;
    border-radius: 10px;
    background: rgba(11, 22, 34, 0.9);
    border: 1px solid rgba(255,255,255,0.1);
}

/* Title */
h1 {
    text-align: center;
    color: white;
    font-size: 28px;
    margin-bottom: 30px;
}

/* Labels */
label {
    color: #bbb !important;
}

/* INPUT STYLE (underline only) */
.stTextInput > div > div {
    position: relative;
}

.stTextInput > div > div > input {
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid #555 !important;
    border-radius: 0 !important;
    color: white !important;
    padding-right: 40px !important;
}

/* Focus effect */
.stTextInput > div > div > input:focus {
    border-bottom: 1px solid #00f5d4 !important;
    box-shadow: none !important;
}

/* Password eye button */
.stTextInput > div > div > button {
    position: absolute !important;
    right: 4px;
    transform: translateY(-50%);     
    border: none !important;
    background: rgba(0, 245, 212, 0.08) !important;
    border-radius: 10% !important;
    color: #00f5d4 !important;
}

.stTextInput > div > div > button:hover {
    background: rgba(0, 245, 212, 0.16) !important;
}

.stTextInput > div > div > button svg {
    width: 18px !important;
    height: 18px !important;
    stroke: #00f5d4 !important;
    fill: none !important;
}

/* Remove default box safely (does NOT affect eye icon) */
[data-baseweb="input"] {
    background: transparent !important;
    border: none !important;
}

/* Button */
.stForm button {
    background: transparent;
    color: #00f5d4;
    border: 1px solid rgba(0,245,212,0.5);
    padding: 10px 22px;
    border-radius: 6px;
    margin-top: 20px;
    position: relative;
}

/* Button hover */
.stForm button:hover {  
    background: rgba(0,245,212,0.08);
       border-left: 3px solid #00f5d4;
    border-bottom: 3px solid #00f5d4;
}

/* Corner effect */
.stForm button::before:hover {
    content: "";
    position: absolute;
    width: 16px;
    height: 16px;
    left: 6px;
    bottom: 6px;
    border-left: 2px solid #00f5d4;
    border-bottom: 2px solid #00f5d4;
}

</style>
""", unsafe_allow_html=True)

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