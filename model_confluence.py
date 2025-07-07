# model_confluence.py

from wiki_reader import get_confluence_text
from model_router import get_response  # use ask_local() directly if needed

def ask_from_confluence(question: str) -> str:
    # Hardcoded for testing; replace with dynamic URL input if needed
    url = "https://confluence.atlassian.com/bitbucketserver/basic-git-commands-776639767.html"

    content = get_confluence_text(url)

    if not content:
        return "Failed to retrieve content from Confluence."

    prompt = f"""Use the following Confluence content to answer the question:

{content}

Question: {question}"""

    return get_response(prompt)  # or ask_local(prompt) if you're bypassing the router
