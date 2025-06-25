import streamlit as st
from config import MODE
from model_router import get_response
from utils import extract_text_from_pdf
from rag import add_document, search_similar

st.set_page_config(page_title="📄 Document Chatbot", layout="centered")
st.title("🤖 Ask Your PDF")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    add_document(text, "doc1")
    st.success("📄 Document indexed.")

query = st.text_input("Ask a question from the document:")

if query:
    context = search_similar(query)
    prompt = f"""Use this context to answer:

{context}

Question: {query}"""
    with st.spinner("Thinking..."):
        response = get_response(prompt)
        st.success(response.strip())
