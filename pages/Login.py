import streamlit as st
from api_calls import login
from nav_pages import nav_page
from menu import menu
from cookie.cookie import cookie_controller

st.title("Login")
menu()
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    token = login(username, password)
    if token:
        # JavaScript code to set the cookie
        cookie_controller.set("access_token", token)
        st.success("Logged in successfully")
        nav_page("Homepage")

if st.button("Go to Register"):
    nav_page("Register")