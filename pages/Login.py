import streamlit as st
from api_calls import login

st.title("Login")
st.write("You have entered the login page", st.session_state["my_input"])
username = st.text_input("Username")
password = st.text_input("Password", type="password")
if st.button("Login"):
    token = login(username, password)
    if token:
        st.session_state.token = token
        st.success("Logged in successfully")
        st.experimental_rerun()
