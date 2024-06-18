import streamlit as st
from dotenv import load_dotenv
import requests
import os
import shelve
import requests

# FastAPI endpoint
api_url = "http://127.0.0.1:8000"


def register(username, password):
    response = requests.post(
        f"{api_url}/register", json={"username": username, "password": password})
    if response.status_code == 200:
        st.success("Registered successfully")
    else:
        st.error(response.json().get("detail", "Registration failed"))


def login(username, password):
    response = requests.post(
        f"{api_url}/token", data={"username": username, "password": password})
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        st.error("Invalid username or password")
        return None


def reset_password(username, password):
    response = requests.post(
        f"{api_url}/reset-password", json={"username": username, "password": password})
    if response.status_code == 200:
        st.success("Password reset successfully")
    else:
        st.error(response.json().get("detail", "Password reset failed"))


def get_secure_data(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{api_url}/secure-data", headers=headers)
    if response.status_code == 200:
        return response.json()["message"]
    else:
        st.error("Failed to fetch secure data")
        return None


def generate_response(prompt_input):
    # This is a placeholder for integrating your chatbot logic
    # You can replace this with actual chatbot API calls
    return f"Bot response to: {prompt_input}"


def main():
    st.set_page_config(page_title="🤗💬 HugChat")

    if "page" not in st.session_state:
        st.session_state.page = "login"
    if "token" not in st.session_state:
        st.session_state.token = None

    def show_register():
        st.session_state.page = "register"

    def show_login():
        st.session_state.page = "login"

    def show_reset_password():
        st.session_state.page = "reset_password"

    if st.session_state.token is not None:
        with st.sidebar:
            if st.session_state.page == "register":
                st.title("Register")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                if st.button("Register"):
                    register(username, password)
                if st.button("Go to Login"):
                    show_login()
            elif st.session_state.page == "reset_password":
                st.title("Reset Password")
                username = st.text_input("Username")
                password = st.text_input("New Password", type="password")
                if st.button("Reset Password"):
                    reset_password(username, password)
                if st.button("Go to Login"):
                    show_login()
            else:
                st.title("Login")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                if st.button("Login"):
                    token = login(username, password)
                    if token:
                        st.session_state.token = token
                        st.session_state.page = "chatbot"
                        st.success("Logged in successfully")
                if st.button("Go to Register"):
                    show_register()
                if st.button("Forgot Password?"):
                    show_reset_password()
    else:
        st.subheader("Chatbot")

        USER_AVATAR = "👤"
        BOT_AVATAR = "🤖"
        BOT_ID = os.getenv("COZE_BOT_ID")
        API_KEY = os.getenv("COZE_API_KEY")
        print(BOT_ID, API_KEY)

        def get_coze_response(messages, stream=True):
            url = 'https://api.coze.com/open_api/v2/chat'
            headers = {
                'Authorization': f'Bearer pat_6qiCbDtySD2KgqCgfyUOnfBPhDEHaqIlUETNn6WEOQBwTND2oYmLvUrFwaTsG3Wk',
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Host': 'api.coze.com',
                'Connection': 'keep-alive'
            }
            data = {
                "conversation_id": "123",
                "bot_id": "7380535583082758145",
                "user": "123312312312312",
                "query": messages[-1]["content"],
                "stream": False,
            }
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            print(response.content)
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
            # data = get_secure_data(st.session_state.token)
            if True:
                st.write("True")
            if st.button("Logout"):
                st.session_state.token = None
                st.success("Logged out successfully")

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
            st.session_state.messages.append(
                {"role": "user", "content": prompt})
            with st.chat_message("user", avatar=USER_AVATAR):
                st.markdown(prompt)

            with st.chat_message("assistant", avatar=BOT_AVATAR):
                message_placeholder = st.empty()
                full_response = ""

                if st.session_state.button_clicked:
                    # The button has been clicked, so we can proceed with the follow-up logic
                    st.session_state.button_clicked = False  # Reset the state
                    response_data = get_coze_response(
                        st.session_state.messages)

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
                    response_data = get_coze_response(
                        st.session_state.messages)

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


if __name__ == "__main__":
    main()
