import os
import streamlit as st
from model_router import get_response
from rag import add_documents_from_file, search_similar
from utils import load_and_chunk_pdfs

st.set_page_config(page_title="AI Chatbot", layout="wide")
st.markdown("""
<style>
    [data-testid="stChatInput"] {
        position: fixed;
        bottom: 2.5rem;
        width: 40%;
        left: 50%;
        transform: translateX(-50%);
        z-index: 9999;
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 0.5rem;
        box-shadow: 0 0 10px rgba(0,0,0,0.5);
    }

    .block-container {
        padding-bottom: 8rem;  /* Prevents chat input from overlapping bottom content */
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

# Store previous text if needed
if "query_input" not in st.session_state:
    st.session_state.query_input = ""



st.title("🤖 AI Chatbot")

# Initialize chat history
if "chat" not in st.session_state:
    st.session_state.chat = []

# Display past chat
for msg in st.session_state.chat:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-message chat-user">{msg["content"]}</div>', unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f'<div class="chat-message chat-assistant">{msg["content"]}</div>', unsafe_allow_html=True)


# Upload PDF
uploaded_file = st.file_uploader("📎 Upload PDF", type=["pdf"])
file_path = None

# ⛔ Only process once
if uploaded_file and "indexed" not in st.session_state:
    os.makedirs("data", exist_ok=True)
    file_path = f"data/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    add_documents_from_file(file_path)
    st.session_state["indexed"] = True
    st.success(f"✅ {uploaded_file.name} has been indexed.")
elif uploaded_file:
    file_path = f"data/{uploaded_file.name}"  # Reuse path


# Chat input (Enter or Send)
col1, col2 = st.columns([9, 1])
with col1:
    user_input = st.chat_input("Ask your question here")
with col2:
    send = st.button("📤", use_container_width=True)

# Process user input
if (user_input or send) and user_input:
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat.append({"role": "user", "content": user_input})

    with st.spinner("🤖 Thinking..."):
        if file_path:
            context = search_similar(user_input)
            full_prompt = f"""Use the following document context to answer:

{context}

Question: {user_input}"""
        else:
            full_prompt = user_input

        response = get_response(full_prompt)

    with st.chat_message("assistant"):
        st.markdown(response.strip())
    st.session_state.chat.append({"role": "assistant", "content": response.strip()})
