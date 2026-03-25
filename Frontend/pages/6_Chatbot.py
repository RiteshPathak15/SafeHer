import streamlit as st
import requests

API_BASE = "http://127.0.0.1:5000/api"

st.set_page_config(page_title="SafeHer - Chatbot", layout="wide")

# Minimal styling (clean look)
st.markdown("""
<style>
.stApp {
    background-color: #020617;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Auth check
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please login first")
    st.stop()

st.title("💬 SafeHer Chat")

username = st.session_state.get("username", "Anonymous")

# Fetch messages
def get_messages():
    try:
        r = requests.get(f"{API_BASE}/chat/messages")
        if r.status_code == 200:
            return r.json().get("messages", [])
    except:
        pass
    return []

messages = get_messages()

# Display chat using Streamlit native UI
for msg in messages:
    role = "user" if msg["username"] == username else "assistant"

    with st.chat_message(role):
        st.markdown(f"**{msg['username']}**: {msg['message']}")
        if msg.get("location"):
            st.caption(f"📍 {msg['location']} | {msg['timestamp']}")
        else:
            st.caption(msg['timestamp'])

# Chat input (clean + fixed automatically)
location = st.text_input("📍 Location (optional)", key="location", label_visibility="collapsed")
prompt = st.chat_input("Type your message...")

if prompt:
    try:
        payload = {
            "username": username,
            "message": prompt
        }
        if location.strip():
            payload["location"] = location.strip()

        r = requests.post(f"{API_BASE}/chat/send", json=payload)

        if r.status_code == 201:
            st.rerun()
        else:
            st.error("Failed to send message")

    except Exception as e:
        st.error(f"API error: {e}")