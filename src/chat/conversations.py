import streamlit as st
import pandas as pd
import base64
from datetime import datetime
from bs4 import BeautifulSoup
import google.generativeai as genai
from src.ingestion.loader import get_pdf_text

def handle_user_input(user_question, api_key, pdf_docs, conversation_history):
    """Main logic for handling user questions."""
    if not api_key:
        st.warning("⚠️ Please enter your Google API Key before asking questions.")
        st.stop()

    if not pdf_docs:
        st.warning("⚠️ Please upload PDF files before asking questions.")
        st.stop()

    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        st.error(f"Failed to configure Google API: {e}")
        st.stop()

    text = get_pdf_text(pdf_docs)

    prompt = f"""
    You are a helpful assistant named Apex. Begin your reply with "Hi! this is Apex your personal pdf chatbot" and a line break.
    Use only the information from the uploaded PDFs to answer.

    Context:
    {text}

    Question: {user_question}

    If the answer is not present, say: "The answer is not available in the PDF."
    """

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        with st.spinner("🤖Generating an answer for you..."):
            response = model.generate_content(prompt)
        answer = response.text
    except Exception as e:
        st.error(f"❌ Gemini request has failed: {e}")
        st.stop()

    # Update conversation history
    pdf_names = [pdf.name for pdf in pdf_docs]
    conversation_history.append((
        user_question,
        answer,
        "Google AI",
        datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        ", ".join(pdf_names)
    ))

    # Display formatted chat
    clean_answer = BeautifulSoup(answer, "html.parser").get_text()
    show_chat_ui(user_question, clean_answer)
    allow_download(conversation_history)

def show_chat_ui(question, answer):
    st.markdown("""
        <style>
            .chat-message {padding:1rem;border-radius:0.5rem;margin-bottom:1rem;display:flex;gap:1rem;}
            .chat-message.user {background-color:#2b313e;border:1px solid #3b4252;color:white;}
            .chat-message.bot {background-color:#475063;border:1px solid #586174;color:white;}
            .chat-message .avatar img {width:40px;height:40px;border-radius:50%;object-fit:cover;}
            .chat-message .message {flex:1;word-wrap:break-word;}
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="chat-message user">
            <div class="avatar"><img src="https://i.ibb.co/CKpTnWr/user-icon-2048x2048-ihoxz4vq.png"></div>
            <div class="message">{question}</div>
        </div>
        <div class="chat-message bot">
            <div class="avatar"><img src="https://i.ibb.co/wNmYHsx/langchain-logo.webp"></div>
            <div class="message">{answer}</div>
        </div>
    """, unsafe_allow_html=True)
    st.balloons()

def allow_download(conversation_history):
    if len(conversation_history) > 0:
        df = pd.DataFrame(
            conversation_history,
            columns=["Question", "Answer", "Model", "Timestamp", "PDF Name"]
        )
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="conversation_history.csv"><button>📥 Download Your Conversation</button></a>'
        st.sidebar.markdown(href, unsafe_allow_html=True)
