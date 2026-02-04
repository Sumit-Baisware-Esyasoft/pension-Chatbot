import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

# ---------------------------
# Load Vector DB
# ---------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

vector_db = FAISS.load_local(
    "vector_db",
    embeddings,
    allow_dangerous_deserialization=True
)

# ---------------------------
# Gemini LLM
# ---------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# ---------------------------
# Chat Function (Plan-B Core)
# ---------------------------
def chatbot(query: str, language: str) -> str:
    docs = vector_db.similarity_search(query, k=6)
    context = "\n\n".join(d.page_content for d in docs)

    system_prompt = """
You are "पेंशन मित्र", an official pension guidance assistant for
MP Electricity Board / DISCOM.

LANGUAGE RULES:
- Hindi + English mix → Hinglish
- Pure Hindi → Hindi
- Pure English → English

STRICT RULES:
- Answer ONLY from provided context
- No guessing or hallucination
- Explain eligibility, steps, and FORMS clearly
- If info not found, say so clearly

FORM GUIDANCE (use if relevant):
- Pension sanction → Form 6
- Family pension → Form 17
- Nomination → Form 1 / Form 2
- Commutation → Commutation Form
- Gratuity → DCRG Form
"""

    prompt = f"""
{system_prompt}

REFERENCE DOCUMENTS:
{context}

USER QUESTION:
{query}
"""

    result = llm.invoke(prompt)
    return result.content
