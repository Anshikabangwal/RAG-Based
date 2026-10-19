import streamlit as st
import os
import json
import uuid
from datetime import datetime
from core.pdf_processor import extract_text_from_pdf
from core.chunker import chunk_pages
from core.vector_store import add_chunks
from core.rag_chain import answer_question
from config import UPLOAD_DIR
from style import apply_style, render_hero, render_hints

st.set_page_config(page_title="Study Assistant", page_icon="📚", layout="centered")
apply_style()

os.makedirs(UPLOAD_DIR, exist_ok=True)

HISTORY_FILE = "chat_history.json"


# --- Chat history helpers ---
def load_chats():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_chats():
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(st.session_state.chats, f, indent=2)


def new_chat():
    chat_id = str(uuid.uuid4())
    st.session_state.chats[chat_id] = {
        "title": "New chat",
        "created": datetime.now().isoformat(),
        "messages": [],
        "docs": [],
    }
    st.session_state.current_chat = chat_id
    save_chats()


# --- Session state setup ---
if "chats" not in st.session_state:
    st.session_state.chats = load_chats()

if "current_chat" not in st.session_state:
    new_chat()

chat = st.session_state.chats[st.session_state.current_chat]
chat.setdefault("docs", [])

# --- Sidebar ---
with st.sidebar:
    st.header("📚 Study Assistant")

    if st.button("➕ New chat", use_container_width=True):
        new_chat()
        st.rerun()

    st.caption("Upload your materials to get started")

    # key changes per chat so the uploader resets when you switch chats
    uploaded_files = st.file_uploader(
        "Upload PDFs (syllabus, notes, PYQs)",
        type="pdf",
        accept_multiple_files=True,
        key=f"uploader_{st.session_state.current_chat}",
    )

    if uploaded_files and st.button("Process Documents", use_container_width=True):
        with st.spinner("Reading and indexing your documents..."):
            for uploaded_file in uploaded_files:
                file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                pages = extract_text_from_pdf(file_path)
                chunks = chunk_pages(pages, source_name=uploaded_file.name)
                add_chunks(chunks, chat_id=st.session_state.current_chat)

                if uploaded_file.name not in chat["docs"]:
                    chat["docs"].append(uploaded_file.name)

        save_chats()
        st.success(f"{len(uploaded_files)} document(s) ready!")

    if chat["docs"]:
        st.info("✅ Documents loaded: " + ", ".join(chat["docs"]))

    if st.button("Clear Chat", use_container_width=True):
        chat["messages"] = []
        chat["title"] = "New chat"
        save_chats()
        st.rerun()

    st.divider()
    st.markdown("### History")
    for cid, c in sorted(
        st.session_state.chats.items(), key=lambda x: x[1]["created"], reverse=True
    ):
        is_current = cid == st.session_state.current_chat
        if st.button(
            c["title"][:30],
            key=f"chat_{cid}",
            use_container_width=True,
            type="primary" if is_current else "secondary",
        ):
            st.session_state.current_chat = cid
            st.rerun()

# --- Main chat area ---
render_hero()

if not chat["messages"]:
    render_hints()

# Display past messages
for msg in chat["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📄 Sources"):
                for src in msg["sources"]:
                    st.caption(f"{src['source']} — Page {src['page']}")

# Chat input box (always pinned at the bottom)
if question := st.chat_input("Ask a question about your documents..."):
    chat["messages"].append({"role": "user", "content": question})
    if chat["title"] == "New chat":
        chat["title"] = question[:40]

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = answer_question(question, chat_id=st.session_state.current_chat)
        st.markdown(result["answer"])
        if result["sources"]:
            with st.expander("📄 Sources"):
                for src in result["sources"]:
                    st.caption(f"{src['source']} — Page {src['page']}")

    chat["messages"].append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result["sources"],
    })
    save_chats()
    st.rerun()