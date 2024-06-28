import streamlit as st
from api_calls import register
from nav_pages import nav_page
from logger import logger
from menu import menu
import re

st.set_page_config(
    page_title="Register Page",
    page_icon="🔒",
)

def is_valid_email(email):
    # Simple regex for validating an email address
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_password(password):
    # Check if password length is at least 8 characters
    return len(password) >= 8
st.title("Register")
menu()
username = st.text_input("Username")
password = st.text_input("Password", type="password")
email = st.text_input("Email")
if st.button("Register"):
    if not username:
        st.error("Username is required")
    elif not password:
        st.error("Password is required")
    elif not email:
        st.error("Email is required")
    elif not is_valid_email(email):
        st.error("Invalid email format")
    elif not is_valid_password(password):
        st.error("Password must be at least 8 characters long")
    else:
        response = register(username, password, email)
        if response:
            st.session_state.page = "Login"
            st.success("Registered successfully")
            logger.info(f"User {username} registered successfully")
            nav_page("Login")
        else:
            st.error("Failed to register")

if st.button("Go to Login"):
    nav_page("Login")
