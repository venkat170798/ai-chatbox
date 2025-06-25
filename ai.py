import streamlit as st
from model_router import get_response

st.set_page_config(page_title="ai-Chatbot", layout="centered")
st.title("🤖 AI Chatbot")

query = st.text_input("Ask anything:")
if query:
    with st.spinner("Thinking..."):
        response = get_response(query)
        st.success(response.strip())