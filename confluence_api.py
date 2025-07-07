import requests
from bs4 import BeautifulSoup
import base64

# Replace these with your actual info
CONFLUENCE_BASE_URL = "https://yourcompany.atlassian.net/wiki"
CONFLUENCE_EMAIL = "vnkt5724@gmail.com"

def get_page_text(page_id):
    url = f"{CONFLUENCE_BASE_URL}/rest/api/content/{page_id}?expand=body.storage"
    auth = (CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN)
    
    response = requests.get(url, auth=auth)
    if response.status_code != 200:
        return f"Error fetching page: {response.status_code} - {response.text}"

    content = response.json()
    html = content["body"]["storage"]["value"]
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator="\n", strip=True)
