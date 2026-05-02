"""
app.py — Entry point. Streamlit UI for the PDF-Constrained Conversational Agent.
Run with: streamlit run app.py
"""

import streamlit as st
import os
from dotenv import load_dotenv
from agent.core import PDFAgent

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PDF Agent",
    page_icon="📄",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.refusal-box {
    background: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 10px 14px;
    border-radius: 4px;
    margin-top: 4px;
    font-size: 14px;
}
.citation-footer {
    color: #6c757d;
    font-size: 12px;
    margin-top: 4px;
}
.status-ready {
    background: #d4edda;
    color: #155724;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 13px;
    font-weight: 500;
}
.status-waiting {
    background: #e2e3e5;
    color: #383d41;
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "agent" not in st.session_state:
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            api_key = ""
    st.session_state.agent = PDFAgent(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_loaded" not in st.session_state:
    st.session_state.pdf_loaded = False

if "page_count" not in st.session_state:
    st.session_state.page_count = 0

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📄 PDF Agent")
    st.caption("Ask questions about any PDF. All answers are grounded to the document.")

    st.divider()

    # API Key input (fallback if not in env)
    if not os.getenv("GEMINI_API_KEY"):
        api_key_input = st.text_input(
            "Gemini API Key", type="password", placeholder="Paste your key here"
        )
        if api_key_input:
            st.session_state.agent = PDFAgent(api_key=api_key_input)

    # PDF Upload
    uploaded_file = st.file_uploader(
        "Upload a PDF", type=["pdf"], help="Upload any PDF to start chatting"
    )

    if uploaded_file:
        if st.button("Load PDF", type="primary", use_container_width=True):
            with st.spinner("Extracting pages..."):
                try:
                    page_count = st.session_state.agent.load_pdf(uploaded_file.read())
                    st.session_state.pdf_loaded = True
                    st.session_state.page_count = page_count
                    st.session_state.messages = []
                    st.success(f"✅ Loaded {page_count} pages")
                except Exception as e:
                    st.error(f"Failed to load PDF: {e}")

    # Status indicator
    st.divider()
    if st.session_state.pdf_loaded:
        st.markdown(
            f'<span class="status-ready">● Ready — {st.session_state.page_count} pages</span>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<span class="status-waiting">○ No PDF loaded</span>',
            unsafe_allow_html=True,
        )

    st.divider()
    if st.button("🗑 Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.agent.memory.clear()
        st.rerun()

# ── Main chat area ─────────────────────────────────────────────────────────────
st.header("Chat with your PDF")

if not st.session_state.pdf_loaded:
    st.info("👈 Upload a PDF in the sidebar to get started.")
else:
    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("citation"):
                st.markdown(
                    f'<div class="citation-footer">{msg["citation"]}</div>',
                    unsafe_allow_html=True,
                )
            if msg.get("is_refusal"):
                st.markdown(
                    '<div class="refusal-box">⚠️ This answer was not found in the document.</div>',
                    unsafe_allow_html=True,
                )

    # Chat input
    if question := st.chat_input("Ask a question about the document..."):
        # Show user message
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Searching document..."):
                answer, citation, refused = st.session_state.agent.ask(question)

            st.markdown(answer)

            if citation:
                st.markdown(
                    f'<div class="citation-footer">{citation}</div>',
                    unsafe_allow_html=True,
                )
            if refused:
                st.markdown(
                    '<div class="refusal-box">⚠️ This answer was not found in the document.</div>',
                    unsafe_allow_html=True,
                )

        # Save to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "citation": citation,
            "is_refusal": refused,
        })
