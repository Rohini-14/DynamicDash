import streamlit as st
from db import verify_user

SESSION_KEY = "current_user"

def is_logged_in():
    return SESSION_KEY in st.session_state and st.session_state[SESSION_KEY] is not None

def get_current_user():
    return st.session_state.get(SESSION_KEY)

def login_form():
    st.subheader("🔐 Login")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log in")
    if submitted:
        u = verify_user(email, password)
        if u:
            st.session_state[SESSION_KEY] = {"email": u["email"], "name": u["name"], "role": u["role"]}
            st.success(f"Welcome, {u['name']}!")
            st.rerun()   # ✅ updated from experimental_rerun()
        else:
            st.error("Invalid credentials")
    return is_logged_in()

def logout_button():
    if st.sidebar.button("🚪 Log out"):
        st.session_state.pop(SESSION_KEY, None)
        st.rerun()

def require_login():
    if not is_logged_in():
        st.info("Please log in to continue.")
        login_form()
        st.stop()

def require_role(role: str):
    require_login()
    user = get_current_user()
    if user["role"] != role:
        st.error(f"This page requires **{role}** role.")
        st.stop()
