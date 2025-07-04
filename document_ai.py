import os
import streamlit as st
from config import MODE
from model_router import get_response
from utils import load_and_chunk_pdfs
from rag import add_documents_from_file, search_similar

st.set_page_config(page_title="📄 Document Chatbot", layout="centered")
st.title("🤖 Ask Your PDF")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

file_path = None
if uploaded_file:
    os.makedirs("data", exist_ok=True)
    file_path = f"data/{uploaded_file.name}"

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    # ✅ Now call with file path
    load_and_chunk_pdfs(file_path)
    add_documents_from_file(file_path)
    st.success("📄 Document indexed.")

query = st.text_input("Ask a question from the document:")

if query:
    context = search_similar(query)
    prompt = f"""Use this context to answer:

{context}

Question: {query}"""

    with st.spinner("🤖 Thinking..."):
        response = get_response(prompt)
        st.success(response.strip())
