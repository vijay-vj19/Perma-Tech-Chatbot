# auth.py
import streamlit as st
import hashlib

users = {
    "admin": hashlib.sha256("admin123".encode()).hexdigest(),
    "user": hashlib.sha256("userpass".encode()).hexdigest(),
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    if username in users and users[username] == hash_password(password):
        return True
    return False

def rerun():
    # Compatibility layer for rerun
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    else:
        st.rerun()

def login_form():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if authenticate(username, password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            rerun()
        else:
            st.error("Invalid username or password")

def logout_button():
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.session_state.pop("username", None)
        rerun()