from streamlit_multipage import MultiPage
import streamlit as st

st.set_page_config(
    page_title="VFarm Chatbot",
    page_icon="🌾",
)

st.title("VFarm Chatbot Main Page")
st.sidebar.success("Select a page above.")


if "my_input" not in st.session_state:
    st.session_state["my_input"] = ""

my_input = st.text_input("Enter something", st.session_state["my_input"])
submit = st.button("Submit")
if submit:
    st.session_state["my_input"] = my_input
    st.write(f"Input: {my_input}")
# if __name__ == "__main__":
#     app.run()
