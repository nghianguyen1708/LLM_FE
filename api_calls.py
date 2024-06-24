# helpers.py
from dotenv import load_dotenv
import requests
import os
import streamlit as st
import shelve

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

def get_secure_data(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{api_url}/chatboxes/", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch secure data")
        return None

def generate_response(prompt_input):
    # This is a placeholder for integrating your chatbot logic
    # You can replace this with actual chatbot API calls
    return f"Bot response to: {prompt_input}"

def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])

def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages
