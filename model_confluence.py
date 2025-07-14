# model_confluence.py

from wiki_reader import get_confluence_text
from model_router import get_response  # or ask_local

def ask_from_confluence(question: str) -> str:
    url = "https://confluence.atlassian.com/bitbucketserver/basic-git-commands-776639767.html"
    content = get_confluence_text(url)

    if not content or content.strip() == "":
        return None  # allow fallback

    prompt = f"""Use the following content to answer the question.
If it is irrelevant or unrelated, say "NO_MATCH":
    
{content}

Question: {question}"""

    response = get_response(prompt)

    # 👇 Detect keyword in answer to fallback
    if "NO_MATCH" in response:
        return None
    return response
