import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from theme import apply_global_theme

st.set_page_config(page_title="SafeHer", layout="wide")

# Apply global theme
apply_global_theme()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

