import streamlit as st
from api_calls import get_all_chatboxes, create_chatbox
from cookie.cookie import cookie_controller
from logger import logger
from streamlit_cookies_controller import CookieController
def authenticated_menu(access_token):
    # Show a navigation menu for authenticated users
    st.sidebar.title("Chatboxes List")
    chatBoxes = get_all_chatboxes(access_token)
    for chatBox in chatBoxes:
        st.sidebar.html(f'''
    <div class="row-widget stPageLink" data-testid="stPageLink" style="width: 288px;">
        <div class="st-emotion-cache-j7qwjs e11k5jya2">
            <a data-testid="stPageLink-NavLink" href="./Chatbot?id={chatBox.id}" target="" rel="noreferrer" class="st-emotion-cache-15ddw4g e11k5jya1">
            <span class="st-emotion-cache-1dj0hjr e11k5jya0">
                <div data-testid="stMarkdownContainer" class="st-emotion-cache-d18qoy e1nzilvr4">
                    <p>{chatBox.name}</p>
                </div>
            </span>
            </a>
        </div>
    </div>
    ''')
    # Form to create a new chatbox
    st.sidebar.subheader("Create New Chatbox")
    chatbox_name = st.sidebar.text_input("Chatbox Name")
    if st.sidebar.button("Create Chatbox"):
        if chatbox_name:
            response = create_chatbox(access_token, chatbox_name)
            if response:
                st.sidebar.success("Chatbox created successfully!")
                # Reload the page to reflect new chatbox
                st.experimental_rerun()
            else:
                st.sidebar.error("Failed to create chatbox.")
        else:
            st.sidebar.error("Chatbox name cannot be empty.")
    st.sidebar.page_link("Homepage.py", label="Homepage")
    st.sidebar.page_link("pages/Logout.py", label="Logout")


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("Homepage.py", label="Homepage")
    st.sidebar.page_link("pages/Login.py", label="Login")
    st.sidebar.page_link("pages/Register.py", label="Register")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    # Get all cookies
    if "access_token" not in st.session_state:
        access_token = str(cookie_controller.get("access_token"))
    else:
        access_token = st.session_state.access_token
    if access_token == "None":
        unauthenticated_menu()
        return
    logger.info("Menu page " + access_token)
    if access_token == "None":
        unauthenticated_menu()
        return
    authenticated_menu(access_token)

def menu_chatbox_pages(access_token):
    # Show a navigation menu for chatbox pages
    st.sidebar.title("Chatboxes List")
    chatBoxes = get_all_chatboxes(access_token)
    for chatBox in chatBoxes:
        st.sidebar.html(f'''
    <div data-stale="false" width="288" class="element-container st-emotion-cache-aejzcr e1f1d6gn4" data-testid="element-container">
        <div class="row-widget stPageLink" data-testid="stPageLink" style="width: 288px;">
            <div class="st-emotion-cache-j7qwjs e11k5jya2">
                <a data-testid="stPageLink-NavLink" href="./Chatbot?id={chatBox.id}" target="" rel="noreferrer" class="st-emotion-cache-ndn75s e11k5jya1">
                    <span class="st-emotion-cache-1dj0hjr e11k5jya0">
                        <div data-testid="stMarkdownContainer" class="st-emotion-cache-4d1onx e1nzilvr4">
                            <p>{chatBox.name}</p>
                        </div>
                    </span>
                </a>
            </div>
        </div>
    </div>
    ''')
    # Form to create a new chatbox
    st.sidebar.subheader("Create New Chatbox")
    chatbox_name = st.sidebar.text_input("Chatbox Name")
    if st.sidebar.button("Create Chatbox"):
        if chatbox_name:
            response = create_chatbox(access_token, chatbox_name)
            if response:
                st.sidebar.success("Chatbox created successfully!")
                # Reload the page to reflect new chatbox
                st.experimental_rerun()
            else:
                st.sidebar.error("Failed to create chatbox.")
        else:
            st.sidebar.error("Chatbox name cannot be empty.")
    st.sidebar.page_link("Homepage.py", label="Homepage")
    st.sidebar.page_link("pages/Logout.py", label="Logout")