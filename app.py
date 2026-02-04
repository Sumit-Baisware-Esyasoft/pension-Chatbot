import streamlit as st
from graph import chatbot

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(
    page_title="🪔 पेंशन मित्र",
    page_icon="🪔",
    layout="wide"
)

# ---------------------------
# Custom CSS (UI HEART)
# ---------------------------
st.markdown("""
<style>

/* Overall */
body {
    background-color: #f6f7f9;
}

/* Header */
.header {
    text-align: center;
    padding: 10px 0 0 0;
}
.header h1 {
    color: #1b5e20;
    font-weight: 700;
}
.header p {
    font-size: 16px;
    color: #444;
}

/* Chat bubbles */
.chat-user {
    background: #dcf8c6;
    padding: 10px 14px;
    border-radius: 12px;
    margin: 6px 0;
    width: fit-content;
    max-width: 80%;
    margin-left: auto;
}

.chat-bot {
    background: #ffffff;
    padding: 10px 14px;
    border-radius: 12px;
    margin: 6px 0;
    width: fit-content;
    max-width: 80%;
    border: 1px solid #e0e0e0;
}

/* Sidebar */
.sidebar-title {
    font-size: 18px;
    font-weight: 600;
    color: #1b5e20;
}

/* Footer */
.footer {
    text-align: center;
    font-size: 12px;
    color: #666;
    margin-top: 20px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# Sidebar (Control Panel)
# ---------------------------
with st.sidebar:
    st.markdown("<div class='sidebar-title'>🪔 पेंशन मित्र</div>", unsafe_allow_html=True)
    st.markdown("**Pension Guidance Assistant**")
    st.divider()

    if "language" not in st.session_state:
        st.session_state.language = "Hindi"

    st.markdown("### 🌐 भाषा / Language")
    st.session_state.language = st.radio(
        "",
        ["Hindi", "English", "Hinglish"],
        index=["Hindi", "English", "Hinglish"].index(st.session_state.language)
    )

    st.divider()
    st.markdown("### 📌 आप क्या पूछ सकते हैं?")
    st.markdown("""
    • Pension eligibility  
    • Family pension  
    • Kaunsa form kab bhare  
    • Gratuity / DCRG  
    • Commutation  
    • Nomination rules  
    """)

    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ---------------------------
# Header
# ---------------------------
st.markdown("""
<div class="header">
    <h1>🪔 पेंशन मित्र</h1>
    <p>Pension se jude saari pareshaani, ab aapki yahin theek hongi</p>
</div>
<hr>
""", unsafe_allow_html=True)

# ---------------------------
# Chat State
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------
# Chat Display Area
# ---------------------------
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-user'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bot'>{msg['content']}</div>", unsafe_allow_html=True)

# ---------------------------
# Input Box (WhatsApp style)
# ---------------------------
query = st.chat_input(
    "अपना सवाल लिखें…" if st.session_state.language == "Hindi"
    else "Type your question…"
)

if query:
    # User message
    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    # Bot response
    with st.spinner("🪔 पेंशन मित्र सोच रहा है..."):
        result = chatbot.invoke({
            "question": query,
            "language": st.session_state.language
        })
        answer = result["response"]

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    st.rerun()

# ---------------------------
# Footer
# ---------------------------
st.markdown("""
<div class="footer">
⚠️ यह सहायक केवल मार्गदर्शन हेतु है। अंतिम निर्णय संबंधित कार्यालय द्वारा लिया जाएगा।<br>
This assistant provides guidance only. Final authority rests with the department.
</div>
""", unsafe_allow_html=True)
