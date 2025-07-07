# wiki_reader.py

import requests
from bs4 import BeautifulSoup

def get_confluence_text(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text(separator="\n")
        
        # Optionally trim or clean further
        cleaned_text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
        
        return cleaned_text

    except Exception as e:
        print(f"[Confluence Error] {e}")
        return ""
