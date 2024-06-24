import streamlit as st
from api_calls import generate_response, get_secure_data, load_chat_history, save_chat_history

def app():
    st.subheader("Chatbot")
    if st.session_state.token:
        token = st.session_state.token
        data = get_secure_data(token)
        st.write(data)
        # Implement chatbot UI here
        prompt = st.text_input("How can I help?")
        if st.button("Send"):
            response = generate_response(prompt)
            st.write(response)
        # Load chat history
        if "messages" not in st.session_state:
            st.session_state.messages = load_chat_history()
        for message in st.session_state.messages:
            st.write(message)
        save_chat_history(st.session_state.messages)
    else:
        st.error("You need to login first")
        st.session_state.page = "Login"
        st.experimental_rerun()
