import os
from langchain_community.document_loaders import Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# -----------------------------
# 1. File paths (DOCX files)
# -----------------------------
FILES = [
    "Revised FAQ - Hindi.docx",
    "Revised FAQ's - English.docx",
    "पेंशन बुक - मार्गदर्शिका - 2025.docx"
]

VECTOR_DB_PATH = "vector_db"

# -----------------------------
# 2. Load documents
# -----------------------------
documents = []

for file in FILES:
    if os.path.exists(file):
        loader = Docx2txtLoader(file)
        docs = loader.load()
        documents.extend(docs)
        print(f"Loaded: {file}")
    else:
        print(f"File not found: {file}")

# -----------------------------
# 3. Split text into chunks
# -----------------------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)

chunks = text_splitter.split_documents(documents)
print(f"Total chunks created: {len(chunks)}")

# -----------------------------
# 4. Create embeddings
# (Multilingual – Hindi + English)
# -----------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# -----------------------------
# 5. Create FAISS vector DB
# -----------------------------
vector_db = FAISS.from_documents(chunks, embeddings)

# -----------------------------
# 6. Save vector DB to disk
# -----------------------------
vector_db.save_local(VECTOR_DB_PATH)

print("✅ Vector database created and saved successfully!")
print(f"📂 Saved at: {os.path.abspath(VECTOR_DB_PATH)}")
