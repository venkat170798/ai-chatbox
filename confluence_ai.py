import streamlit as st
from model_confluence import ask_local
from wiki_reader import get_public_confluence_text

st.set_page_config(page_title="📘 Wiki Chatbot", layout="centered")
st.title("🤖 Ask a Wiki")

query = st.text_input("Ask something from the wiki:")

# ✅ Use public wiki for development
wiki_url = "https://confluence.atlassian.com/bitbucketserver/basic-git-commands-776639767.html"

if query:
    with st.spinner("📄 Reading wiki..."):
        wiki_text = get_public_confluence_text(wiki_url)

    prompt = f"Use this wiki content to answer:\n\n{wiki_text}\n\nQuestion: {query}"
    with st.spinner("🤖 Thinking..."):
        answer = ask_local(prompt)

    st.markdown("**Answer:**")
    st.success(answer.strip())
