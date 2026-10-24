import os
import re
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

def clean_text(text):
    """Remove print headers/footers added when saving the web pages as PDF:
    date+time stamps, 'Page X of Y' markers, and investor.gov URLs."""
    # Remove lines like "22/10/2026, 13:54" (date, time)
    text = re.sub(r"\d{2}/\d{2}/\d{4},\s*\d{1,2}:\d{2}", "", text)
    # Remove "Page X of Y"
    text = re.sub(r"Page \d+ of \d+", "", text)
    # Remove investor.gov URLs
    text = re.sub(r"https?://\S*investor\.gov\S*", "", text)
    # Collapse multiple spaces/newlines into single spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text

loader = PyPDFDirectoryLoader("documents/")
documents = loader.load()
print(f"Loaded {len(documents)} pages from the PDFs.")

for doc in documents:
    doc.page_content = clean_text(doc.page_content)
print("Cleaned headers/footers from the documents.")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,       # each chunk is ~1000 characters
    chunk_overlap=150,     # chunks overlap by 150 chars to avoid cutting ideas in half
)
chunks = text_splitter.split_documents(documents)
print(f"Split documents into {len(chunks)} chunks.")

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

print("Building the vector database... (this may take a moment)")
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db",   # saved in the chroma_db/ folder
)
print(f"Done! Vector database created with {len(chunks)} chunks in 'chroma_db/'.")