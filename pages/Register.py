import streamlit as st
from api_calls import register
from nav_pages import nav_page
from logger import logger
from menu import menu


st.title("Register")
menu()
username = st.text_input("Username")
password = st.text_input("Password", type="password")
email = st.text_input("Email")
if st.button("Register"):
    response = register(username, password, email)
    if response.status_code == 200:
        st.session_state.page = "Login"
        st.success("Registered successfully")
        logger.info(f"User {username} registered successfully")
        nav_page("Login")
    else:
        st.error("Failed to register")

if st.button("Go to Login"):
    nav_page("Login")
