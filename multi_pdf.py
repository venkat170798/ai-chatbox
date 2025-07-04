# app_day3.py
import streamlit as st
import os
from rag import add_documents_from_folder, search_similar
from model_router import get_response

st.set_page_config(page_title="AI Chatbot (Multi PDF)", layout="wide")

st.title("📄 AI Chatbot - Multi PDF Support")

# Upload PDFs
uploaded_files = st.file_uploader("Upload PDF(s)", type="pdf", accept_multiple_files=True)

if uploaded_files:
    os.makedirs("data", exist_ok=True)
    for file in uploaded_files:
        file_path = os.path.join("data", file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())
    st.success(f"{len(uploaded_files)} file(s) uploaded.")
    add_documents_from_folder("data")

# Chat interface
prompt = st.text_input("Ask a question about the uploaded documents:")
if prompt:
    context = search_similar(prompt)
    full_prompt = f"Use this context to answer the question:\n\n{context}\n\nQuestion: {prompt}"
    response = get_response(full_prompt)
    st.markdown(f"**Answer:** {response}")
