import streamlit as st
from model_confluence import ask_from_confluence
from model_router import get_response

st.set_page_config(page_title="AI Chatbot", layout="centered")

# 💅 Custom CSS
st.markdown("""
<style>
    .chat-message {
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        max-width: 75%;
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
        padding-bottom: 10rem;
    }
</style>
""", unsafe_allow_html=True)

# 🧠 App Title
st.markdown("<h1 style='text-align: center;'>🤖 AI Chatbot</h1>", unsafe_allow_html=True)

# 📜 Chat history state
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔁 Display chat history
for msg in st.session_state.messages:
    role_class = "chat-user" if msg["role"] == "user" else "chat-assistant"
    alignment = "flex-start" if msg["role"] == "user" else "flex-end"
    st.markdown(f"""
        <div style="display: flex; justify-content: {alignment};">
            <div class="chat-message {role_class}">{msg['content']}</div>
        </div>
    """, unsafe_allow_html=True)

# 📩 Chat input (BOTTOM input box)
prompt = st.chat_input("Ask from wiki...")

# ✅ After user submits a question
if prompt:
    # Show user message immediately
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"""
        <div style="display: flex; justify-content: flex-start;">
            <div class="chat-message chat-user">{prompt}</div>
        </div>
    """, unsafe_allow_html=True)

    with st.spinner("🤖 Thinking..."):
        try:
            answer = ask_from_confluence(prompt)
        except Exception:
            answer = get_response(prompt)

    # Show assistant message immediately
    st.markdown(f"""
        <div style="display: flex; justify-content: flex-end;">
            <div class="chat-message chat-assistant">{answer}</div>
        </div>
    """, unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": answer})
