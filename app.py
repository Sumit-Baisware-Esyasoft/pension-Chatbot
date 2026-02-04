import streamlit as st
from graph import chatbot

# Page config
st.set_page_config(page_title="🪔 पेंशन मित्र", page_icon="🪔", layout="wide")

# Header
st.markdown("""
<h1 style="text-align:center;">🪔 पेंशन मित्र</h1>
<p style="text-align:center;">
Pension se jude saari pareshaani, ab aapki yahin theek hongi
</p><hr>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🌐 भाषा / Language")
    if "language" not in st.session_state:
        st.session_state.language = "Hindi"
    st.session_state.language = st.radio(
        "", ["Hindi", "English", "Hinglish"],
        index=["Hindi","English","Hinglish"].index(st.session_state.language)
    )
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Messages
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Input
query = st.chat_input(
    "अपना सवाल लिखें…" if st.session_state.language=="Hindi" else "Type your question…"
)

if query:
    st.session_state.messages.append({"role":"user","content":query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("🪔 पेंशन मित्र सोच रहा है..."):
            answer = chatbot(query, st.session_state.language)
            st.markdown(answer)

    st.session_state.messages.append({"role":"assistant","content":answer})
