import os
import fitz  # PyMuPDF

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

PDF_PATH = "WHO/who_basic_emergency.pdf"
INDEX_PATH = "who_index"

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    return splitter.split_text(text)

def build_index():
    print("Extracting WHO PDF text...")
    text = extract_text_from_pdf(PDF_PATH)

    print("Chunking text...")
    chunks = chunk_text(text)
    print(f"Total chunks created: {len(chunks)}")

    print("Creating OpenAI embeddings...")
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key=os.getenv("OPENAI_API_KEY")
    )

    print("Building FAISS index...")
    vector_store = FAISS.from_texts(chunks, embeddings)

    print("Saving index...")
    vector_store.save_local(INDEX_PATH)

    print("WHO RAG index built successfully!")

if __name__ == "__main__":
    build_index()