import streamlit as st
from model_router import get_response

st.set_page_config(page_title="AI Chatbot", layout="centered")
st.markdown("<h1 style='text-align: center;'>🤖 AI Chatbot</h1>", unsafe_allow_html=True)


# ✅ CSS for floating input and bubbles
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
    padding-bottom: 10rem;
}
.chat-container {
    display: flex;
    flex-direction: column;
    margin-top: 1rem;
}
.chat-bubble.user {
    align-self: flex-start;
    background-color: #f1f1f1;
    color: #000;
    padding: 0.75rem 1rem;
    border-radius: 10px;
    max-width: 75%;
    word-wrap: break-word;
    border: 1px solid #ccc;
    margin-bottom: 0.5rem;
}
.chat-bubble.bot {
    align-self: flex-end;
    background-color: #4a90e2;
    color: white;
    padding: 0.75rem 1rem;
    border-radius: 10px;
    max-width: 75%;
    word-wrap: break-word;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ✅ Session state for chat messages
if "chat" not in st.session_state:
    st.session_state.chat = []

# 👇 Floating input at bottom
prompt = st.chat_input("Ask anything...")

# ✅ If user enters a question
if prompt:
    # Add user message to history
    st.session_state.chat.append({"role": "user", "content": prompt})

    # Display bubbles up to this point (user + spinner)
    for msg in st.session_state.chat[:-1]:
        bubble_class = "user" if msg["role"] == "user" else "bot"
        st.markdown(f"""
        <div class="chat-container">
            <div class="chat-bubble {bubble_class}">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

    # 👉 Show current user message
    st.markdown(f"""
    <div class="chat-container">
        <div class="chat-bubble user">{prompt}</div>
    </div>
    """, unsafe_allow_html=True)

    # 🤖 Thinking response
    with st.spinner("🤖 Thinking..."):
        response = get_response(prompt).strip()

    # Save assistant response
    st.session_state.chat.append({"role": "bot", "content": response})

    # 👇 Show bot message
    st.markdown(f"""
    <div class="chat-container">
        <div class="chat-bubble bot">{response}</div>
    </div>
    """, unsafe_allow_html=True)

    st.rerun()  # rerun to rebuild full chat thread
else:
    # 👇 Display all past chat messages (no new prompt)
    for msg in st.session_state.chat:
        bubble_class = "user" if msg["role"] == "user" else "bot"
        st.markdown(f"""
        <div class="chat-container">
            <div class="chat-bubble {bubble_class}">{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
