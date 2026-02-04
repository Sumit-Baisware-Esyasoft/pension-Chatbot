import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st


# ---------------------------
# 1. Graph State
# ---------------------------
class ChatState(TypedDict):
    question: str
    language: str
    documents: List[Document]
    response: str


# ---------------------------
# 2. Load Vector DB
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
# 3. Gemini LLM
# ---------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY") or st.secrets["GOOGLE_API_KEY"]
)


# ---------------------------
# 4. Retriever
# ---------------------------
def retrieve_docs(state: ChatState):
    docs = vector_db.similarity_search(state["question"], k=6)
    return {"documents": docs}


# ---------------------------
# 5. Generator (Deep Prompt)
# ---------------------------
def generate_response(state: ChatState):
    context = "\n\n".join(doc.page_content for doc in state["documents"])

    system_prompt = """
You are "पेंशन मित्र", an official pension guidance assistant for
MP Electricity Board / DISCOM pensioners and employees.

LANGUAGE RULES:
- If user mixes Hindi + English → reply in Hinglish
- If pure Hindi → reply in Hindi
- If pure English → reply in English

STRICT RULES:
- Answer ONLY from provided context
- Do NOT guess or hallucinate
- If info not found, clearly say so
- Use simple, step-by-step explanation
- Be citizen-friendly (government helpdesk tone)

SPECIAL RESPONSIBILITIES:
1. Explain pension rules in simple terms
2. Clearly tell:
   - कौन सा FORM भरना है
   - कब भरना है
   - किस office में देना है
3. Mention Rule / Section if available
4. If multiple cases possible, explain all briefly

FORM GUIDANCE EXAMPLES (use if relevant):
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
{state['question']}
"""

    result = llm.invoke(prompt)
    return {"response": result.content}


# ---------------------------
# 6. Build Graph
# ---------------------------
graph = StateGraph(ChatState)

graph.add_node("retrieve", retrieve_docs)
graph.add_node("generate", generate_response)

graph.set_entry_point("retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)

chatbot = graph.compile()
