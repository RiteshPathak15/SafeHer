import streamlit as st


def render_sidebar_header():
   
    try:
        col1, col2 = st.sidebar.columns([3, 1])
        with col2:
            if st.sidebar.button("Logout ❎", help="Logout", key="sidebar_logout"):
                st.session_state.logged_in = False
                st.session_state.clear()
                st.success("Logged out successfully!")
                st.switch_page("pages/1_login.py")
                return True
        with col1:
            username = st.session_state.get('username', 'User')
            st.sidebar.write(f"👤 {username}")
        
        st.sidebar.divider()
        return False
    except Exception as e:
        st.error(f"Sidebar error: {str(e)}")
        return False


def sidebar_filter_section(title="🔍 Filters"):
    try:
        st.sidebar.header(title)
    except Exception as e:
        st.error(f"Filter section error: {str(e)}")


def check_authentication():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.warning("Please login first in Login page")
        st.stop()
        return False
    return True


def get_current_username():
    return st.session_state.get('username', 'User')

