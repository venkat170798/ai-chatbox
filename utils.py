import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

def load_and_chunk_pdfs(file_path: str):
    documents = []

    print("🔍 PDF opened:", file_path)

    if not file_path.lower().endswith(".pdf"):
        return documents

    try:
        import fitz  # PyMuPDF
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()

        from langchain.text_splitter import RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = text_splitter.split_text(text)
        for chunk in chunks:
            documents.append(Document(page_content=chunk))

        print("🧩 Number of chunks:", len(documents))  # ✅ Now it's valid

    except Exception as e:
        print(f"[PDF Processing Error] {e}")

    return documents
