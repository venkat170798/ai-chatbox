import os
import chromadb
import streamlit as st
from chromadb.config import Settings
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from langchain.docstore.document import Document
from utils import load_and_chunk_pdfs
from chromadb import PersistentClient

@st.cache_resource
def get_vectorstore():
    settings = Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="./chroma_store"
    )

    try:
        client = PersistentClient(path="./chroma_store")
        collection_name = "pdf-qa"

        if collection_name not in [c.name for c in client.list_collections()]:
            client.create_collection(name=collection_name, embedding_function=DefaultEmbeddingFunction())

        return client.get_collection(name=collection_name, embedding_function=DefaultEmbeddingFunction())

    except ValueError as e:
        print(f"[Chroma Warning Suppressed] {e}")
        st.stop()

def search_similar(query, top_k=3):
    collection = get_vectorstore()

    print("🔎 Searching for:", query)

    try:
        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )
        matches = results.get("documents", [[]])[0]
        print("🔎 Matches returned:", matches)

        if not matches:
            return "No relevant context found in the document."

        return "\n".join(matches)

    except Exception as e:
        print("❌ Chroma Search Error:", e)
        return "Context could not be retrieved from the document."


def add_documents_from_file(file_path: str):
    documents = load_and_chunk_pdfs(file_path)
    if documents:
        collection = get_vectorstore()
        texts = [doc.page_content for doc in documents]
        ids = [f"doc_{i}" for i in range(len(texts))]

        collection.add(
            documents=texts,
            ids=ids
        )
