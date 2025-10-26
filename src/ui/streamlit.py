import streamlit as st
from src.chat.conversations import handle_user_input
from src.utils.config import GOOGLE_API_KEY

def run_app():
    st.set_page_config(page_title="Your Own PDF ChatBot!", page_icon="🤖")
    st.header("Chat using PDFs 💬")

    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    api_key = st.sidebar.text_input("Enter your Google API Key:", value=GOOGLE_API_KEY or "")
    st.sidebar.markdown("[Get your API key here](https://ai.google.dev/)")

    pdf_docs = st.file_uploader("Upload your PDF files", accept_multiple_files=True)
    st.sidebar.button("Reset", on_click=lambda: st.session_state.clear())

    user_question = st.text_input("Ask a question about the PDFs:")
    if user_question:
        handle_user_input(user_question, api_key, pdf_docs, st.session_state.conversation_history)
