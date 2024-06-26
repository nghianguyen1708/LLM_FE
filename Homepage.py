import streamlit as st
from menu import menu
st.set_page_config(
    page_title="VFarm Chatbot",
    page_icon="🌾",
)

st.title("VFarm Chatbot Main Page")

menu()

