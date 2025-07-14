# rag.py
import os
import streamlit as st
import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from utils import load_and_chunk_pdfs, load_and_chunk_word_docs

# ✅ Updated: Use persistent client with DuckDB+Parquet backend
@st.cache_resource
def get_vectorstore():
    try:
        client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./chroma_store"  # ✅ Persistent local directory
        ))
        collection_name = "doc-collection"
        if collection_name not in [c.name for c in client.list_collections()]:
            client.create_collection(
                name=collection_name,
                embedding_function=DefaultEmbeddingFunction()
            )
        return client.get_collection(name=collection_name, embedding_function=DefaultEmbeddingFunction())
    except Exception as e:
        st.warning(f"⚠️ ChromaDB error: {e}")
        st.stop()

# ✅ Search top matches
def search_similar(query: str, top_k: int = 3):
    collection = get_vectorstore()
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    documents = results.get("documents", [[]])[0]
    return "\n".join(documents)

# ✅ Add chunks from PDF
def add_documents_from_pdf_folder(folder_path: str):
    pdf_docs = load_and_chunk_pdfs(folder_path)
    if not pdf_docs:
        st.warning("No PDF documents found.")
        return
    collection = get_vectorstore()
    for i, doc in enumerate(pdf_docs):
        collection.add(
            documents=[doc.page_content],
            ids=[f"pdf-{i}"]
        )
    st.success(f"📄 Indexed {len(pdf_docs)} PDF chunks.")

# ✅ Add chunks from Word files
def add_word_documents_from_folder(folder_path: str):
    word_docs = load_and_chunk_word_docs(folder_path)
    if not word_docs:
        st.warning("No Word documents found.")
        return
    collection = get_vectorstore()
    for i, doc in enumerate(word_docs):
        collection.add(
            documents=[doc.page_content],
            ids=[f"word-{i}"]
        )
    st.success(f"📄 Indexed {len(word_docs)} Word chunks.")
