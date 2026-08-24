import streamlit as st
import os
from core.pdf_processor import extract_text_from_pdf
from core.chunker import chunk_pages
from core.vector_store import add_chunks
from core.rag_chain import answer_question
from config import UPLOAD_DIR

st.set_page_config(page_title="Study Assistant", page_icon="📚", layout="centered")

os.makedirs(UPLOAD_DIR, exist_ok=True)

# --- Session state setup ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "docs_processed" not in st.session_state:
    st.session_state.docs_processed = False

# --- Sidebar: document upload ---
with st.sidebar:
    st.header("📚 Study Assistant")
    st.caption("Upload your materials to get started")

    uploaded_files = st.file_uploader(
        "Upload PDFs (syllabus, notes, PYQs)",
        type="pdf",
        accept_multiple_files=True
    )

    if uploaded_files and st.button("Process Documents", use_container_width=True):
        with st.spinner("Reading and indexing your documents..."):
            for uploaded_file in uploaded_files:
                file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                pages = extract_text_from_pdf(file_path)
                chunks = chunk_pages(pages, source_name=uploaded_file.name)
                add_chunks(chunks)

        st.session_state.docs_processed = True
        st.success(f"{len(uploaded_files)} document(s) ready!")

    if st.session_state.docs_processed:
        st.info("✅ Documents loaded — ask me anything below")

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Main chat area ---
st.title("📚 Study Assistant")

if not st.session_state.messages:
    st.caption("Ask me anything about your uploaded study material.")

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📄 Sources"):
                for src in msg["sources"]:
                    st.caption(f"{src['source']} — Page {src['page']}")

# Chat input box (always pinned at the bottom)
if question := st.chat_input("Ask a question about your documents..."):
    # Show user's message immediately
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Generate and show assistant's response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = answer_question(question)
        st.markdown(result["answer"])
        if result["sources"]:
            with st.expander("📄 Sources"):
                for src in result["sources"]:
                    st.caption(f"{src['source']} — Page {src['page']}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result["sources"]
    })