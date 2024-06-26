import streamlit as st
from api_calls import register
from nav_pages import nav_page
from logger import logger
from menu import menu
from cookie.cookie import cookie_controller
st.title("Logout")
menu()

st.info("Are you sure you want to logout?")
if st.button("Logout"):
    # Remove a cookie
    cookie_controller.erase_cookie_js("access_token")
    if "access_token" in st.session_state:
        del st.session_state.access_token
    st.success("Logged out successfully")
    nav_page("Homepage")
