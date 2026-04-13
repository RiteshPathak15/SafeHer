import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import datetime
import time

API_BASE = "http://127.0.0.1:5000/api"

st.set_page_config(page_title="SafeHer Global Chat", layout="wide")

# ---------- STYLING ----------
st.markdown("""
<style>
body { background-color: #f6f9fc; }

.chat-card {
    padding: 16px;
    border-radius: 18px;
    margin-bottom: 12px;
    max-width: 700px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.chat-own {
    margin-left: auto;
    background: linear-gradient(135deg, #d1fae5, #a7f3d0);
    color: #065f46;
}

.chat-other {
    background: #ffffff;
    color: #374151;
}

.chat-emergency {
    background: linear-gradient(135deg, #ffe3e3, #ffc9c9);
    border-left: 6px solid #ff4d4f;
    color: #b91c1c;
}

.username {
    font-weight: 700;
    margin-bottom: 6px;
}

.sidebar-box {
    padding: 18px;
    border-radius: 16px;
    background: #ffffff;
    box-shadow: 0 6px 20px rgba(0,0,0,0.05);
}

.chat-container {
    max-height: 500px;
    overflow-y: auto;
    padding-right: 10px;
}

.chat-container::-webkit-scrollbar {
    display: none;
}

</style>
""", unsafe_allow_html=True)

# ---------- AUTH ----------
if not st.session_state.get("logged_in"):
    st.warning("Please login first.")
    st.stop()

username = st.session_state.get("username", "Anonymous")

# ---------- STATE ----------
if "location" not in st.session_state:
    st.session_state.location = ""

if "share_location" not in st.session_state:
    st.session_state.share_location = False

# ---------- GEO ----------
geo_val = st.query_params.get("geo")

if geo_val:
    if isinstance(geo_val, list):
        geo_val = geo_val[0]

    if geo_val != st.session_state.location:
        st.session_state.location = geo_val
        st.session_state.share_location = True
        st.toast("📍 Location captured")

# ---------- API ----------
@st.cache_data(ttl=5)
def fetch_messages():
    try:
        r = requests.get(f"{API_BASE}/global-chat/messages", timeout=5)
        if r.status_code == 200:
            return r.json().get("messages", [])
    except:
        pass
    return []

def send_message(payload):
    try:
        r = requests.post(f"{API_BASE}/global-chat/send", json=payload, timeout=5)
        return r.status_code == 201
    except:
        return False

def format_time(ts):
    try:
        return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S").strftime("%I:%M %p")
    except:
        return ts

# ---------- MESSAGE UI ----------
def render_message(msg):
    is_me = msg.get("username") == username
    is_emergency = msg.get("emergency")

    css = "chat-card "
    if is_emergency:
        css += "chat-emergency"
    elif is_me:
        css += "chat-own"
    else:
        css += "chat-other"

    st.markdown(f"""
    <div class="{css}">
        <div class="username">{msg.get('username')}</div>
        <div>{msg.get('message')}</div>
    </div>
    """, unsafe_allow_html=True)

    if msg.get("location"):
        st.caption(f"📍 {msg['location']}")

    st.caption(f"🕒 {format_time(msg.get('timestamp',''))}")

# ---------- HEADER ----------
st.title("💬 SafeHer Global Chat")

# ---------- LAYOUT ----------
chat_col, side_col = st.columns([3, 1])

# ---------- CHAT ----------
with chat_col:
    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()

    messages = fetch_messages()

    if not messages:
        st.info("No messages yet")
    else:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for m in messages:
            render_message(m)
        st.markdown('</div>', unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with side_col:
    st.markdown('<div class="sidebar-box">', unsafe_allow_html=True)

    st.subheader("Send Message")

    share_location = st.toggle("📍 Share Location", value=st.session_state.share_location)

    if share_location:

        # Detect button with preview
        components.html("""
        <div>
            <button onclick="getLocation()" style="
                padding:10px 14px;
                background:#3b82f6;
                color:white;
                border:none;
                border-radius:10px;
                cursor:pointer;
            ">
                📍 Detect Location
            </button>

            <p id="status" style="margin-top:8px;font-size:13px;color:gray;"></p>
        </div>

        <script>
        function getLocation() {
            const status = document.getElementById("status");
            status.innerText = "Fetching location...";

            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    const lat = pos.coords.latitude.toFixed(5);
                    const lon = pos.coords.longitude.toFixed(5);

                    status.innerHTML = "Captured: " + lat + ", " + lon;

                    setTimeout(() => {
                        window.top.location.href = '?geo=' + lat + ',' + lon;
                    }, 800);
                },
                (err) => {
                    status.innerText = "Permission denied or failed.";
                }
            );
        }
        </script>
        """, height=120)

        # SHOW LOCATION AFTER CAPTURE ✅ FIX
        if st.session_state.location:
            try:
                lat, lon = st.session_state.location.split(",")

                st.success(f"📍 Location: {lat}, {lon}")
                st.caption("This location will be attached to your message.")

            except:
                st.warning("Invalid location format")

        # Manual input
        manual = st.text_input("Enter manually (lat,lon)")
        if manual:
            st.session_state.location = manual

    emergency = st.toggle("🚨 Emergency")

    msg = st.text_area("Message", height=120)

    if st.button("Send", use_container_width=True):
        if msg.strip():

            payload = {
                "username": username,
                "message": msg.strip(),
                "emergency": emergency
            }

            if share_location and st.session_state.location:
                payload["location"] = st.session_state.location

            if send_message(payload):
                st.toast("Message sent")
                st.cache_data.clear()
                time.sleep(0.3)
                st.rerun()
            else:
                st.error("Failed to send")

        else:
            st.warning("Enter a message")

    st.markdown('</div>', unsafe_allow_html=True)