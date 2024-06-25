from dotenv import load_dotenv
import requests
import streamlit as st
from typing import List
from logger import logger
from request.request import ChatMessageCreate
from request.reponse import ChatMessage, ChatBox
import datetime
# Load environment variables
load_dotenv()

# FastAPI endpoint
api_url = "http://127.0.0.1:8888"

def register(username, password, email, full_name=""):
    response = requests.post(f"{api_url}/users/", json={"username": username, "password": password, "email": email, "full_name": full_name})
    if response.status_code == 200:
        st.success("Registered successfully")
    else:
        st.error(response.json().get("detail", "Registration failed"))

def login(username, password):
    try:
        response = requests.post(f"{api_url}/token", json={"username": username, "password": password})
        response.raise_for_status()  # Raise an error for bad status codes
        st.session_state.token = response.json()["access_token"]
        logger.info(f"Response: {response.json()}")
        return response.json()["access_token"]
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")  # HTTP error
    except requests.exceptions.RequestException as err:
        st.error(f"Error occurred: {err}")  # Other errors
    except ValueError:
        st.error(f"Invalid response: {response.text}")  # JSON decode error
    return None

def reset_password(username, password):
    response = requests.post(f"{api_url}/reset-password", json={"username": username, "password": password})
    if response.status_code == 200:
        st.success("Password reset successfully")
    else:
        st.error(response.json().get("detail", "Password reset failed"))

def get_all_chatboxes(token) -> List[ChatBox]:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{api_url}/chatboxes/", headers=headers)
    if response.status_code == 200:
        logger.info(f"Chatboxes: {response.json()}")
        chat_boxes = []
        for chat_box_data in response.json():
            chat_box = ChatBox(
                id=chat_box_data['id'],
                user_id=chat_box_data['user_id'],
                name=chat_box_data['name'],
                created_at=datetime.datetime.fromisoformat(chat_box_data['created_at'])
            )
            chat_boxes.append(chat_box)
        return chat_boxes
    else:
        st.error("Failed to fetch secure data")
        return []

def generate_response(prompt_input):
    # This is a placeholder for integrating your chatbot logic
    # You can replace this with actual chatbot API calls
    return f"Bot response to: {prompt_input}"

def load_chat_history(token, chat_box_id) -> List[ChatMessage]:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{api_url}/chatboxes/{chat_box_id}/messages/", headers=headers)

    if response.status_code == 200:
        logger.info(f"Chat history: {response.json()}")
        chat_messages = []
        for message_data in response.json():
            chat_message = ChatMessage(
                id=message_data['id'],
                chat_box_id=message_data['chat_box_id'],
                message=message_data['message'],
                sender=message_data['sender'],
                timestamp=datetime.datetime.fromisoformat(message_data['timestamp'])
            )
            chat_messages.append(chat_message)
        return chat_messages
    else:
        st.error("Failed to load chat history")
        return []

def save_chat_history(message: ChatMessageCreate, chat_box_id: int, token: str):
    url = f"{api_url}/chatboxes/{chat_box_id}/messages/"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    data = {
        "message": message.message,
        "sender": message.sender
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to save message: {response.json()}")