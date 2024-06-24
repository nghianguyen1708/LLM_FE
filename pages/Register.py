import streamlit as st
from api_calls import register


st.title("Register")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
email = st.text_input("Email")
if st.button("Go to Login"):
    st.session_state.page = "Login"
    st.experimental_rerun()
