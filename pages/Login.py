import streamlit as st
from api_calls import login, api_url
from nav_pages import nav_page
from menu import menu
from cookie.cookie import cookie_controller
import requests

GOOGLE_LOGIN_URL = f"{api_url}/auth/google"
st.set_page_config(
    page_title="Login Page",
    page_icon="🔒",
)
st.title("Login")
menu()
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if str(cookie_controller.get("access_token")) != "None":
    nav_page("Homepage")

if st.button("Login"):
    token = login(username, password)
    if token:
        # JavaScript code to set the cookie
        st.session_state.access_token = token
        cookie_controller.set("access_token", token)
        st.success("Logged in successfully")
        nav_page("Homepage")

# # Check if we have an authorization code
# auth_code = st._get_query_params().get("code")
# if auth_code:
#     # Exchange the authorization code for a token
#     response = requests.get(f"{api_url}/auth/google/callback?code={auth_code[0]}")
#     if response.status_code == 200:
#         user_info = response.json()
#         st.success("Successfully logged in!")
#         st.write(user_info)
#     else:
#         st.error("Login failed")
# else:
#     # Provide a button to initiate Google OAuth
#     if st.button("Login with Google"):
#         # Redirect user to the OAuth authorization URL
#         response = requests.get(f"{api_url}/auth/google")
#         if response.status_code == 200:
#             oauth_url = response.url
#             st.write("Redirecting to:", oauth_url)
#             st.experimental_set_query_params()  # Clear query params
#             st.experimental_rerun()  # Rerun to trigger redirection
#         else:
#             st.error("Failed to initiate login")

if st.button("Go to Register"):
    nav_page("Register")