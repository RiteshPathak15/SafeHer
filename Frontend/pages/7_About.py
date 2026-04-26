import streamlit as st
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))
from components import render_sidebar_header

st.set_page_config(page_title="SafeHer - About", layout="wide")

st.markdown("""
<style>
body, .main, .block-container {
  background-color: #020617 !important;
  color: #e2e8f0 !important;
}
.page-title {
  color: #f8fafc;
}
.hero-box {
  background: linear-gradient(180deg, rgba(30,58,138,0.95), rgba(15,23,42,0.95));
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 24px;
  padding: 32px;
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.35);
}
.card {
  background: rgba(15, 23, 42, 0.88);
  border: 1px solid rgba(148, 163, 184, 0.18);
  border-radius: 18px;
  padding: 24px;
  margin-bottom: 22px;
}
.card h3 {
  color: #f8fafc;
}
.card p, .card li {
  color: #cbd5e1;
}
.badge {
  display: inline-block;
  background: #2563eb;
  color: white;
  padding: 6px 14px;
  border-radius: 999px;
  font-size: 0.8rem;
  margin-right: 8px;
  margin-bottom: 10px;
}
.feature-icon {
  font-size: 2rem;
  margin-right: 14px;
}
.feature-box {
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid rgba(148, 163, 184, 0.16);
  border-radius: 18px;
  padding: 18px;
  margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR WITH LOGOUT ----------
with st.sidebar:
    render_sidebar_header()

st.markdown(
    """
    <div class='hero-box'>
      <div style='display:flex; flex-wrap:wrap; gap:24px; align-items:center;'>
        <div style='flex:1; min-width:320px;'>
          <h1>SafeHer: Empowering Safety Through Data</h1>
          <p>SafeHer helps users explore crime insights, make safer choices, and connect with others via secure chat and location sharing.</p>
          <p>Built to combine easy-to-use analytics with practical safety tools, all in one responsive web app.</p>
        </div>
        <div style='flex:1; min-width:320px;'>
          <img src='https://images.unsplash.com/photo-1521334884684-d80222895322?auto=format&fit=crop&w=900&q=80' width='100%' style='border-radius:18px; border:1px solid rgba(148,163,184,0.2);' />
          <p style='color:#94a3b8; margin-top:12px; font-size:0.95rem;'>Community safety and awareness</p>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---- Quick Navigation Buttons (inside card styling) ----
st.markdown("<div style='margin: 16px 0;'></div>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

with col1:
    if st.button("🗺️ Women Safety", use_container_width=True, key="badge_safety"):
        st.switch_page("pages/5_Safety_Map.py")

with col2:
    if st.button("💬 Global Chat", use_container_width=True, key="badge_chat"):
        st.switch_page("pages/6_GlobalChat.py")

with col3:
    if st.button("📊 Data Insights", use_container_width=True, key="badge_data"):
        st.switch_page("pages/2_dashboard.py")


st.markdown("### What SafeHer Provides")
row1, row2 = st.columns(2)
with row1:
    st.markdown(
        """
        <div class='card'>
          <h3>Data-driven insights</h3>
          <p>Analyze crime trends, identify the highest risk areas, and understand the story behind state-level data.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class='card'>
          <h3>Secure chat experience</h3>
          <p>Send messages and share optional location details securely while keeping the chat experience fast and user-friendly.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
with row2:
    st.markdown(
        """
        <div class='card'>
          <h3>Emergency awareness</h3>
          <p>Quickly find key safety numbers and the highest/lowest risk states so you can respond faster.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class='card'>
          <h3>Clean modern design</h3>
          <p>A polished UI with responsive layouts that makes data exploration simple for every user.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

st.markdown("### How to use SafeHer")
with st.container():
    st.markdown(
        """
        <div class='feature-box'>
          <div><span class='feature-icon'>🔐</span><strong>Login securely</strong></div>
          <p>Register or login to access the full dashboard, datasets, and chat features.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class='feature-box'>
          <div><span class='feature-icon'>📊</span><strong>Explore crime data</strong></div>
          <p>Use the Dataset page to view trends, totals, and high-risk states clearly.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class='feature-box'>
          <div><span class='feature-icon'>💬</span><strong>Chat with others</strong></div>
          <p>Send messages, share optional location, and stay connected with other users.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

st.markdown(
    """
    <div class='card'>
      <h3>Built with</h3>
      <ul>
        <li><strong>Streamlit</strong> for the frontend UI.</li>
        <li><strong>Flask</strong> for backend APIs.</li>
        <li><strong>SQLite</strong> for lightweight storage.</li>
        <li><strong>Pandas</strong> for data analysis.</li>
        <li><strong>Cryptography</strong> for secure message handling.</li>
      </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

st.markdown("### More about the project")
st.write("SafeHer is designed to bring safety awareness to users through data, communication, and clear visual summaries. It's a learning-focused project that can evolve into a full safety platform with real-time alerts and secure user management.")

st.markdown("### Contact & extend")
st.write("If you want to improve this app, you can add a notification system, map-based incident reporting, or user authentication tokens for stronger security.")
