import streamlit as st
import streamlit.components.v1 as components
import requests
from datetime import datetime
import time
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from components import render_sidebar_header
from theme import apply_global_theme

API_BASE = "http://127.0.0.1:5000/api"

st.set_page_config(page_title="Rakshika-Ai Global Chat", layout="wide")

# Apply global theme
apply_global_theme()

# ---------- CHAT-SPECIFIC STYLING ----------
st.markdown("""
<style>
/* ===== CHAT CONTAINER ===== */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 12px;
    padding: 20px;
    background: linear-gradient(135deg, #F9FAFB 0%, #F3F4F6 100%);
    border-radius: 16px;
    max-height: 600px;
    overflow-y: auto;
}

/* ===== CHAT ROW ===== */
.chat-row {
    display: flex;
    align-items: flex-end;
    gap: 10px;
    margin-bottom: 8px;
    animation: fadeIn 0.3s ease-out;
}

.chat-row.own {
    justify-content: flex-end;
}

.chat-row.other {
    justify-content: flex-start;
}

.chat-row.emergency-center {
    justify-content: center !important;
}

/* ===== AVATAR ===== */
.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6B46C1, #8B5CF6);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
    font-size: 0.85rem;
    box-shadow: 0 4px 12px rgba(107, 70, 193, 0.25);
    flex-shrink: 0;
}

.avatar.own {
    background: linear-gradient(135deg, #10B981, #34D399);
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
}

/* ===== CHAT BUBBLE ===== */
.chat-bubble {
    max-width: 70%;
    min-width: 80px;
    padding: 14px 16px;
    border-radius: 18px;
    display: flex;
    flex-direction: column;
    gap: 6px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    word-wrap: break-word;
    animation: slideInUp 0.3s ease-out;
}

/* Own Message - Green (WhatsApp style) */
.chat-bubble.own {
    background: linear-gradient(135deg, #6B46C1, #8B5CF6);
    color: white;
    border-bottom-right-radius: 4px;
    margin-left: auto;
}

/* Other Message - White */
.chat-bubble.other {
    background: white;
    color: #111827;
    border-bottom-left-radius: 4px;
    margin-right: auto;
    border: 1px solid rgba(107, 70, 193, 0.1);
}

/* Emergency Message - Red */
.chat-bubble.chat-emergency {
    background: linear-gradient(135deg, #DC2626, #EF4444);
    color: white;
    border-radius: 18px;
    animation: pulse 1.5s infinite;
    box-shadow: 0 8px 24px rgba(220, 38, 38, 0.25);
    font-weight: 600;
}

/* ===== USERNAME ===== */
.chat-bubble .username {
    font-size: 0.8rem;
    font-weight: 700;
    opacity: 0.9;
    letter-spacing: 0.3px;
}

.chat-bubble.own .username {
    opacity: 0.95;
}

.chat-bubble.other .username {
    color: #6B46C1;
}

/* ===== CHAT TEXT ===== */
.chat-text {
    font-size: 0.95rem;
    line-height: 1.5;
    white-space: pre-wrap;
    word-break: break-word;
    font-weight: 500;
}

/* ===== META ROW (Time & Location) ===== */
.meta-row {
    display: flex;
    justify-content: space-between;
    font-size: 0.75rem;
    opacity: 0.85;
    margin-top: 4px;
    font-weight: 500;
}

.chat-bubble.own .meta-row {
    opacity: 0.9;
}

/* ===== SIDEBAR BOX ===== */
.sidebar-box {
    padding: 24px;
    border-radius: 16px;
    background: linear-gradient(135deg, #F9FAFB, #F3F4F6);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(107, 70, 193, 0.1);
}

.sidebar-box h3 {
    color: #111827;
    margin-bottom: 16px;
    font-size: 1.1rem;
}

/* ===== INPUT STYLING ===== */
.stTextArea textarea {
    background: white !important;
    border: 2px solid #E5E7EB !important;
    border-radius: 12px !important;
    padding: 12px !important;
    font-size: 0.95rem !important;
    resize: none !important;
}

.stTextArea textarea:focus {
    border-color: #6B46C1 !important;
    box-shadow: 0 0 0 4px rgba(107, 70, 193, 0.1) !important;
}

/* ===== TOGGLE STYLING ===== */
.stCheckbox label {
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

/* ===== BUTTON IMPROVEMENT ===== */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    width: 100%;
}

/* ===== ANIMATIONS ===== */
@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

@keyframes pulse {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: 0.9;
    }
}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
    .chat-bubble {
        max-width: 85%;
        padding: 12px 14px;
        font-size: 0.9rem;
    }
    
    .sidebar-box {
        padding: 16px;
    }
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

    # Determine styles
    if is_emergency:
        row_class = "chat-row emergency-center"
        bubble_class = "chat-bubble chat-emergency"
        show_avatar = False
    elif is_me:
        row_class = "chat-row own"
        bubble_class = "chat-bubble own"
        show_avatar = True
        avatar_position = "after"
    else:
        row_class = "chat-row other"
        bubble_class = "chat-bubble other"
        show_avatar = True
        avatar_position = "before"

    location_text = f"📍 {msg['location']}" if msg.get("location") else ""
    timestamp = format_time(msg.get('timestamp', ''))

    # Build HTML
    if show_avatar:
        if avatar_position == "before":
            html = f'<div class="{row_class}"><div class="avatar">{user_initials}</div><div class="{bubble_class}"><div class="username">{msg.get("username")}</div><div class="chat-text">{msg.get("message")}</div><div class="meta-row"><span>{location_text}</span><span>🕒 {timestamp}</span></div></div></div>'
        else:
            html = f'<div class="{row_class}"><div class="{bubble_class}"><div class="username">{msg.get("username")}</div><div class="chat-text">{msg.get("message")}</div><div class="meta-row"><span>{location_text}</span><span>🕒 {timestamp}</span></div></div><div class="avatar own">{user_initials}</div></div>'
    else:
        html = f'<div class="{row_class}"><div class="{bubble_class}"><div class="username">{msg.get("username")}</div><div class="chat-text">{msg.get("message")}</div><div class="meta-row"><span>{location_text}</span><span>🕒 {timestamp}</span></div></div></div>'

    st.markdown(html, unsafe_allow_html=True)

# ---------- HEADER ----------
st.title("💬 Rakshika-Ai Global Chat")
st.markdown("**Connect safely with the community • Real-time chat & support**")

# ---------- SIDEBAR WITH LOGOUT ----------
with st.sidebar:
    render_sidebar_header()

# ---------- LAYOUT ----------
chat_col, side_col = st.columns([3, 1])

# ---------- CHAT ----------
with chat_col:
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔄 Refresh Messages", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    with col2:
        if st.button("🗑️ Clear Cache", use_container_width=True):
            st.cache_data.clear()
            st.info("Cache cleared!")

    messages = fetch_messages()

    # Display chat
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if not messages:
        st.markdown("""
        <div style="text-align: center; padding: 40px 20px; color: #6B7280;">
            <div style="font-size: 3rem; margin-bottom: 16px;">💬</div>
            <h3 style="color: #111827;">No messages yet</h3>
            <p>Be the first to send a message in this safe space!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for m in messages:
            render_message(m)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with side_col:
    st.markdown('<div class="sidebar-box">', unsafe_allow_html=True)

    st.subheader("✍️ Send Message")

    share_location = st.toggle("📍 Share Location", value=st.session_state.share_location)

    if share_location:

        components.html("""
        <div>
            <button onclick="getLocation()" style="
                padding: 12px 16px;
                background: linear-gradient(135deg, #6B46C1, #8B5CF6);
                color: white;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                font-weight: 600;
                width: 100%;
                transition: all 0.3s ease;
            " onmouseover="this.style.transform='scale(1.02)'; this.style.boxShadow='0 6px 20px rgba(107, 70, 193, 0.3)';" 
               onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='none';">
                📍 Detect Location
            </button>

            <p id="status" style="margin-top: 12px; font-size: 13px; color: #6B7280; text-align: center;"></p>
        </div>

        <script>
        function getLocation() {
            const status = document.getElementById("status");
            status.innerText = "🔍 Fetching location...";

            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    const lat = pos.coords.latitude.toFixed(5);
                    const lon = pos.coords.longitude.toFixed(5);

                    status.innerHTML = "✅ Captured: " + lat + ", " + lon;

                    setTimeout(() => {
                        window.top.location.href = '?geo=' + lat + ',' + lon;
                    }, 800);
                },
                (err) => {
                    status.innerText = "❌ Permission denied or failed.";
                    status.style.color = '#DC2626';
                }
            );
        }
        </script>
        """, height=140)

        if st.session_state.location:
            try:
                lat, lon = st.session_state.location.split(",")
                st.success(f"✅ Location: {lat}, {lon}")
                st.caption("📌 This location will be attached to your message.")
            except:
                st.warning("⚠️ Invalid location format")

        st.divider()
        
        manual = st.text_input("📍 Or enter manually (lat,lon)", placeholder="e.g. 28.6139, 77.2090")
        if manual:
            st.session_state.location = manual

    st.divider()
    
    emergency = st.toggle("🚨 Mark as Emergency", value=False)
    if emergency:
        st.warning("⚠️ This message will be highlighted as an emergency alert!")
    
    msg = st.text_area("💬 Your message", height=100, placeholder="Type your message here...", key="chat_input")

    if st.button("📤 Send Message", use_container_width=True, type="primary"):
        if msg.strip():
            payload = {
                "username": username,
                "message": msg.strip(),
                "emergency": emergency
            }

            if share_location and st.session_state.location:
                payload["location"] = st.session_state.location

            if send_message(payload):
                st.success("✅ Message sent!", icon="✔️")
                st.cache_data.clear()
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ Failed to send message. Please try again.", icon="⚠️")
        else:
            st.warning("⚠️ Please enter a message", icon="⚠️")

    st.markdown('</div>', unsafe_allow_html=True)