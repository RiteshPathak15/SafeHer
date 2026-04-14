import streamlit as st
import streamlit.components.v1 as components
import requests
import textwrap
from datetime import datetime
import time

API_BASE = "http://127.0.0.1:5000/api"

st.set_page_config(page_title="SafeHer Global Chat", layout="wide")

# ---------- STYLING ----------
st.markdown("""
<style>

/* ---------- GLOBAL ---------- */
body {
    background: linear-gradient(135deg, #e5ddd5, #d1dbe6);
    font-family: 'Segoe UI', sans-serif;
}

/* ---------- CHAT CONTAINER ---------- */
.chat-container {
    max-height: 520px;
    overflow-y: auto;
    padding: 18px 14px 10px;
    display: flex;
    flex-direction: column;
    gap: 14px;
    scroll-behavior: smooth;
}

/* Scrollbar */
.chat-container::-webkit-scrollbar {
    width: 6px;
}
.chat-container::-webkit-scrollbar-thumb {
    background: rgba(0,0,0,0.2);
    border-radius: 999px;
}

/* ---------- CHAT ROW ---------- */
.chat-row {
    display: flex;
    align-items: flex-end;
    gap: 10px;
    animation: fadeIn 0.25s ease-in-out;
}

.chat-row.own {
    justify-content: flex-end;
}

.chat-row.other {
    justify-content: flex-start;
}

/* ✅ NEW: CENTER EMERGENCY */
.chat-row.emergency-center {
    justify-content: center !important;
}

/* ---------- AVATAR ---------- */
.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg, #34b7f1, #0ea5e9);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 600;
    font-size: 0.85rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}

.avatar.own {
    background: linear-gradient(135deg, #25d366, #16a34a);
}

/* ---------- CHAT BUBBLE ---------- */
.chat-bubble {
    width: fit-content;
    max-width: 60%;
    min-width: 120px;
    padding: 12px 14px;
    border-radius: 16px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    transition: transform 0.1s ease;
}

.chat-bubble:hover {
    transform: scale(1.01);
}

/* Own */
.chat-bubble.own {
    background: #dcf8c6;
    border-bottom-right-radius: 6px;
}

/* Other */
.chat-bubble.other {
    background: #ffffff;
    border-bottom-left-radius: 6px;
}

/* ---------- TEXT ---------- */
.chat-bubble .username {
    font-size: 0.78rem;
    color: #6b7280;
    font-weight: 600;
}

.chat-bubble.own .username {
    color: #15803d;
}

.chat-text {
    font-size: 0.95rem;
    line-height: 1.4;
    color: #111827;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ---------- META ---------- */
.meta-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.72rem;
    color: #6b7280;
}

/* ---------- EMERGENCY ---------- */
.chat-emergency {
    background: linear-gradient(135deg, #ffe3e3, #ffb4b4);
    border-left: 5px solid #ff1e1e;
    color: #991b1b;
    animation: pulse 1.5s infinite;
}

/* ---------- SIDEBAR ---------- */
.sidebar-box {
    padding: 18px;
    border-radius: 18px;
    background: #ffffff;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
}

/* ---------- BUTTON IMPROVEMENT ---------- */
button[kind="primary"] {
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* ---------- ANIMATIONS ---------- */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(6px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(255,0,0,0.4); }
    70% { box-shadow: 0 0 0 10px rgba(255,0,0,0); }
    100% { box-shadow: 0 0 0 0 rgba(255,0,0,0); }
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
    user_initials = "".join([part[0] for part in msg.get("username", "?").split()][:2]).upper()

    # ✅ CENTER EMERGENCY
    if is_emergency:
        row_class = "chat-row emergency-center"
    else:
        row_class = "chat-row own" if is_me else "chat-row other"

    bubble_class = "chat-bubble own" if is_me else "chat-bubble other"
    if is_emergency:
        bubble_class = "chat-bubble chat-emergency"

    location_text = f"📍 {msg['location']}" if msg.get("location") else ""

    html = textwrap.dedent(f"""
    <div class="{row_class}">
        {'' if is_me or is_emergency else f'<div class="avatar">{user_initials}</div>'}
        <div class="{bubble_class}">
            <div class="username">{msg.get('username')}</div>
            <div class="chat-text">{msg.get('message')}</div>
            <div class="meta-row">
                <span>{location_text}</span>
                <span>🕒 {format_time(msg.get('timestamp',''))}</span>
            </div>
        </div>
        {'' if not is_me or is_emergency else f'<div class="avatar own">{user_initials}</div>'}
    </div>
    """)
    html = "".join(line.strip() for line in html.splitlines())
    st.markdown(html, unsafe_allow_html=True)

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

        if st.session_state.location:
            try:
                lat, lon = st.session_state.location.split(",")
                st.success(f"📍 Location: {lat}, {lon}")
                st.caption("This location will be attached to your message.")
            except:
                st.warning("Invalid location format")

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