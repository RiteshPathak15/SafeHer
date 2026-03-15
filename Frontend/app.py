import streamlit as st

st.set_page_config(page_title="SafeHer", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


