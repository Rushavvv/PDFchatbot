![bg](https://github.com/user-attachments/assets/59157b02-6b5e-48fd-9d99-c0e03563a04d)<img width="1440" height="820" alt="Screenshot 2025-11-04 at 3 30 44 PM" src="https://github.com/user-attachments/assets/edc73726-ad82-48c9-8c41-a49e5de78f4f" /># PDF Chatbot

A web-based chatbot that allows users to upload PDFs and ask questions about the document. The chatbot uses Google Vertex AI Generative API via LangChain to generate answers from PDF content. The frontend displays responses in a modern chat-bubble interface similar to WhatsApp or Instagram.

---

## Features

- Upload PDF documents and get a unique **Document ID**.
- View uploaded documents in a dropdown for easy selection.
- Ask questions about the PDF content.
- Chat responses appear as **bubbles**, providing a clean, modern chat interface.
- Handles API rate limits with retries.
  
<img width="1440" height="820" alt="image" src="https://github.com/user-attachments/assets/1c34936f-94dc-46b9-9ed2-263fddf0ce99" />


## Tech Stack

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** FastAPI  
- **PDF Processing & Chat:** Python, LangChain, Google Vertex AI Generative API  
- **Hosting / Local Development:** Runs locally on `http://127.0.0.1:8000/`

---
