import streamlit as st
from menu import menu
st.set_page_config(
    page_title="VFarm Chatbot",
    page_icon="🌾",
)
st.title("VFarm Chatbot Main Page")

menu()

# Welcome message
st.markdown("""
## Welcome to VFarm Chatbot! 🌾

VFarm Chatbot is your reliable assistant for all things agriculture. Whether you're a farmer looking for advice on crop management, an agronomist seeking the latest research, or just someone interested in learning more about sustainable farming practices, VFarm Chatbot is here to help.

### Features:
- **Expert Advice:** Get insights and recommendations from our virtual agricultural expert.
- **Sustainable Practices:** Learn about sustainable farming techniques and how to implement them.
- **Resource Management:** Tips on managing soil, water, and other essential resources efficiently.
- **Pest and Disease Management:** Identify and manage common pests and diseases affecting your crops.
- **Latest Innovations:** Stay updated with the latest advancements in agricultural technology.

### How to Use:
1. **Login or Register:** Before you can access the chatbot, please log in or register for an account.
   - Navigate to the **Login** or **Register** page from the left sidebar.
   - Complete the registration form or log in with your existing credentials.
2. **Access Chatboxes:** After logging in, navigate to the **Chatboxes List** on the left sidebar.
3. **Select or Create a Chatbox:** Select an existing chatbox or create a new one to start a conversation.
4. **Ask Questions:** Ask any agriculture-related questions, and our chatbot will provide detailed, accurate, and actionable responses.

We are committed to helping you achieve better yields and more sustainable farming practices. Happy farming!
""")

# Encourage user interaction
st.markdown("""
---
If you have any questions or need further assistance, don't hesitate to reach out. Let's grow together!
""")