import streamlit as st
from api_calls import reset_password

def app():
    st.title("Reset Password")
    username = st.text_input("Username")
    password = st.text_input("New Password", type="password")
    if st.button("Reset Password"):
        reset_password(username, password)
    if st.button("Go to Login"):
        st.session_state.page = "Login"
        st.experimental_rerun()
