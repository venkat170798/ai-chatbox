import os
import streamlit as st
from rag import search_similar, add_word_documents_from_folder
from model_router import get_response

st.set_page_config(page_title="📄 Document Chatbot", layout="centered")

# 💬 UI Styling
st.markdown("""
<style>
    [data-testid="stChatInput"] {
        position: fixed;
        bottom: 2.5rem;
        width: 50%;
        left: 50%;
        transform: translateX(-50%);
        z-index: 9999;
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 0.5rem;
        box-shadow: 0 0 10px rgba(0,0,0,0.5);
    }

    .block-container {
        padding-bottom: 8rem;
    }

    .chat-message {
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        max-width: 70%;
        font-size: 1rem;
        display: inline-block;
        word-wrap: break-word;
    }

    .chat-user {
        background-color: #f0f0f0;
        color: #000;
        text-align: left;
        margin-right: auto;
        border: 1px solid #ccc;
    }

    .chat-assistant {
        background-color: #4a90e2;
        color: white;
        text-align: left;
        margin-left: auto;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>📁 AI Chatbot from Documents</h2>", unsafe_allow_html=True)

# 🔁 Load and index docs from folder
doc_folder = "data"
if not os.path.exists(doc_folder):
    os.makedirs(doc_folder)

# ✅ Index all PDFs and DOCX in 'data/' folder
for filename in os.listdir(doc_folder):
    file_path = os.path.join(doc_folder, filename)
    if filename.lower().endswith(".pdf"):
        add_documents_from_file(file_path)
    elif filename.lower().endswith(".docx"):
        add_word_documents_from_folder(doc_folder)

# 🧠 Chat UI
if "doc_chat" not in st.session_state:
    st.session_state.doc_chat = []

def handle_query():
    user_query = st.session_state.get("query", "").strip()
    if not user_query:
        return

    # 1️⃣ Show user's question
    st.markdown(f'<div class="chat-message chat-user">{user_query}</div>', unsafe_allow_html=True)
    st.session_state.doc_chat.append({"role": "user", "content": user_query})

    # 2️⃣ Show "thinking..." before answer
    with st.spinner("🤖 Thinking..."):
        context = search_similar(user_query)
        prompt = f"Use this context to answer:\n\n{context}\n\nQuestion: {user_query}"
        answer = get_response(prompt).strip()

    # 3️⃣ Display assistant's answer
    st.markdown(f'<div class="chat-message chat-assistant">{answer}</div>', unsafe_allow_html=True)
    st.session_state.doc_chat.append({"role": "assistant", "content": answer})

# 🔁 Replay history
for msg in st.session_state.doc_chat:
    role_class = "chat-user" if msg["role"] == "user" else "chat-assistant"
    st.markdown(f'<div class="chat-message {role_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# 🔤 Input at bottom
st.chat_input("Ask from your document:", key="query", on_submit=handle_query)
