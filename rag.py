import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection("chatbot")

def add_document(text, doc_id):
    collection.add(documents=[text], ids=[doc_id])

def search_similar(query):
    results = collection.query(query_texts=[query], n_results=1)
    if results["documents"]:
        return results["documents"][0][0]
    return ""