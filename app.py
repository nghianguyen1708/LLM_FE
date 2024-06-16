import streamlit as st
from dotenv import load_dotenv
import requests
import os
import shelve

load_dotenv()
st.title("ChatGPT-like Chatbot Demo")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"
BOT_ID = os.getenv("COZE_BOT_ID")
API_KEY = os.getenv("COZE_API_KEY")


def get_coze_response(messages, stream=False):
    url = 'https://api.coze.com/open_api/v2/chat'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Host': 'api.coze.com',
        'Connection': 'keep-alive'
    }
    data = {
        "conversation_id": "123",
        "bot_id": BOT_ID,
        "user": "29032201862555",
        "query": messages[-1]["content"],
        "stream": stream,
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


# Ensure openai_model is initialized in session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Load chat history from shelve file


def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])

# Save chat history to shelve file


def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages


# Initialize or load chat history
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# Sidebar with a button to delete chat history
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])

# Display chat messages
for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


def handle_button_click(selected_follow_up):
    """
    This function handles the logic for the "Ask Follow-Up" button click.

    Args:
        selected_follow_up (str): The selected follow-up question from the selectbox.
    """
    print("Running")
    st.session_state.messages.append(
        {"role": "user", "content": selected_follow_up})
    st.session_state.button_clicked = False  # Reset the state
    st.rerun()  # Rerun the app to update the chat interface


def handle_button_click(selected_follow_up):
    st.session_state.messages.append(
        {"role": "user", "content": selected_follow_up})
    st.session_state.button_clicked = True  # Set the button_clicked state to True
    st.experimental_rerun()  # Rerun the app to update the chat interface


if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

# Main chat interface
if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        message_placeholder = st.empty()
        full_response = ""

        if st.session_state.button_clicked:
            # The button has been clicked, so we can proceed with the follow-up logic
            st.session_state.button_clicked = False  # Reset the state
            response_data = get_coze_response(st.session_state.messages)

            if response_data.get("messages"):
                follow_ups = []
                for response in response_data["messages"]:
                    if response["type"] == "answer":
                        full_response += response["content"] + "\n\n"
                    elif response["type"] == "follow_up":
                        follow_ups.append(response["content"])
                message_placeholder.markdown(full_response)

                if follow_ups:
                    selected_follow_up = st.selectbox(
                        "Select a follow-up question:", follow_ups)
                    handle_button_click(selected_follow_up)
        else:
            # The button has not been clicked yet, so we can display the initial response
            response_data = get_coze_response(st.session_state.messages)

            if response_data.get("messages"):
                for response in response_data["messages"]:
                    if response["type"] == "answer":
                        full_response += response["content"] + "\n\n"
                message_placeholder.markdown(full_response)

            # Display the "Ask Follow-Up" button if there are follow-up questions
            follow_ups = [response["content"]
                          for response in response_data["messages"] if response["type"] == "follow_up"]
            if follow_ups:
                selected_follow_up = st.selectbox(
                    "Select a follow-up question:", follow_ups)
                if st.button("Ask Follow-Up"):
                    handle_button_click(selected_follow_up)
    print(st.session_state.button_clicked)
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response})

# Save chat history after each interaction
save_chat_history(st.session_state.messages)
