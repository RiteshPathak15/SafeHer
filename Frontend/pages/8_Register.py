import streamlit as st
import random
import string
import requests

st.set_page_config(page_title="SafeHer - Register", layout="centered")

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
    margin-top: 60px;
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
    margin-bottom: 10px;
}

/* Subtitle */
.stMarkdown {
    color: #aaa !important;
    text-align: center;
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
    right: 6px !important;
    transform: translateY(-50%) !important;
    width: 32px !important;
    height: 32px !important;
    min-width: 32px !important;
    min-height: 32px !important;
    padding: 0 !important;
    border: none !important;
    background: rgba(0, 245, 212, 0.12) !important;
    border-radius: 50% !important;
    color: #00f5d4 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    overflow: hidden !important;
}

.stTextInput > div > div > button:hover {
    background: rgba(0, 245, 212, 0.24) !important;
}

.stTextInput > div > div > button svg {
    width: 18px !important;
    height: 18px !important;
    stroke: #00f5d4 !important;
    fill: none !important;
}

.stTextInput > div > div > button span {
    display: none !important;
}

/* Remove default box safely */
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
.stForm button::before {
    content: "";
    position: absolute;
    width: 16px;
    height: 16px;
    left: 6px;
    bottom: 6px;
}

</style>
""", unsafe_allow_html=True)


if "users" not in st.session_state:
    st.session_state.users = {}

API_BASE = "http://127.0.0.1:5000/api"

# ---------- HELPER ----------
def generate_username():
    """Generate a fully random username independent of the entered name."""
    letters = ''.join(random.choice(string.ascii_lowercase) for _ in range(4))
    digits = ''.join(random.choice(string.digits) for _ in range(4))
    return f"user{letters}{digits}"

# ---------- UI ----------
st.title("SafeHer Registration")
st.markdown('<p style="text-align:center; color:#aaa; font-size:14px;">Create your account to join SafeHer</p>', unsafe_allow_html=True)

with st.form("register_form"):
    full_name = st.text_input("Full Name")
    
    # Show auto-generated username preview
    auto_username = generate_username()
    username_requested = st.text_input(
        "Username (leave blank for auto-generated)",
        placeholder=f"Auto: {auto_username}"
    )
    
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    submit = st.form_submit_button("REGISTER")

# ---------- LOGIC ----------
if submit:
    if not full_name or not password or not confirm_password:
        st.error("Enter name and password")
    elif password != confirm_password:
        st.error("Passwords do not match")
    else:
        # Use provided username or auto-generate
        final_username = username_requested.strip() if username_requested.strip() else generate_username()

        payload = {"name": full_name, "username": final_username, "password": password}
        try:
            r = requests.post(f"{API_BASE}/register", json=payload, timeout=5)
            if r.status_code == 201:
                st.success(f"✓ Registered as {final_username}. Go to Login to sign in.")
            else:
                st.error(r.json().get("error", "Failed to register"))
        except Exception as e:
            st.error(f"Error: {e}")


