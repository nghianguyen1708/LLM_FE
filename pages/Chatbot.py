import streamlit as st
from api_calls import generate_response, load_chat_history, save_chat_history
from nav_pages import nav_page
from request.request import ChatMessageCreate
from menu import menu
from logger import logger
from cookie.cookie import cookie_controller

st.set_page_config(
    page_title="VFarm Chatbot",
    page_icon="🌾",
)

st.subheader("Chatbot")
access_token = str(cookie_controller.get("access_token"))
logger.info("Chatbot page " + access_token)
if access_token != "None":
    menu()
    token = access_token
    if st._get_query_params().get("id", None)[0] is None:
        st.error("Chatbox ID not found")
        nav_page("Homepage")
    chat_box_id = int(st._get_query_params().get("id", None)[0])
    # Implement chatbot UI here
    # Load chat history
    chatMessages = load_chat_history(token, chat_box_id)
    # Display chat history with roles
    with st.container():
        for message in chatMessages:
            if message.sender == "user":
                with st.chat_message(name="User"):
                    st.write(message.message)
            else:
                with st.chat_message(name="Assistant"):
                    st.write(message.message)
    # Implement chatbot UI here
    prompt = st.text_input("How can I help?")
    if st.button("Send"):
        # Get response from chatbot
        response = generate_response(prompt)
        # Save user message
        user_message = ChatMessageCreate(message=prompt, sender="user")
        with st.chat_message(name="User"):
            st.write(prompt)
        save_chat_history(user_message, chat_box_id, token)
        # Save assistant response
        assistant_message = ChatMessageCreate(message=response, sender="assistant")
        with st.chat_message(name="Assistant"):
            st.write(response)
        save_chat_history(assistant_message, chat_box_id, token)
else:
    st.error("You need to login first")
    menu()
    if st.button("Go to Login"):
        nav_page("Login")
