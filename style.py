import streamlit as st

CSS = """
<style>
/* ---------- Page background: soft tint instead of stark white ---------- */
.stApp {
    background: linear-gradient(180deg, #F5F6FD 0%, #EEF1FB 100%);
}
header[data-testid="stHeader"] {
    background: transparent;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #E9ECFA 0%, #E1E5F7 100%);
    border-right: 1px solid #D6DBF2;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #2B2F6B;
}

/* ---------- Hero (title + subtitle) ---------- */
.hero { padding: 1.2rem 0 0.4rem 0; }
.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 0;
    color: #1F2340;
}
/* gradient only on the text, so the emoji keeps its colour */
.hero-title .grad {
    background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    color: #6B7094;
    margin: 0.35rem 0 0 0;
    font-size: 1rem;
}

/* ---------- Empty-state hint cards ---------- */
.hint-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-top: 1.4rem;
}
.hint-card {
    background: #FFFFFF;
    border: 1px solid #E3E7F7;
    border-radius: 14px;
    padding: 14px 16px;
    box-shadow: 0 2px 10px rgba(79, 70, 229, .06);
    transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
}
.hint-card:hover {
    transform: translateY(-2px);
    border-color: #B9C0F3;
    box-shadow: 0 8px 20px rgba(79, 70, 229, .12);
}
.hint-card .ico { font-size: 1.3rem; }
.hint-card .ttl { font-weight: 700; color: #2B2F6B; margin: 6px 0 2px 0; font-size: .95rem; }
.hint-card .txt { color: #6B7094; font-size: .85rem; line-height: 1.35; }
@media (max-width: 700px) {
    .hint-grid { grid-template-columns: 1fr; }
}

/* ---------- File uploader card ---------- */
[data-testid="stFileUploader"] section {
    background: #FFFFFF;
    border: 1.5px dashed #A5B0F0;
    border-radius: 14px;
    transition: border-color .2s, box-shadow .2s;
}
[data-testid="stFileUploader"] section:hover {
    border-color: #6366F1;
    box-shadow: 0 4px 14px rgba(99, 102, 241, .15);
}

/* ---------- Buttons ---------- */
.stButton > button,
[data-testid="stFileUploader"] button {
    border-radius: 10px;
    border: 1px solid #C7CDF2;
    background: #FFFFFF;
    color: #3B3F8C;
    font-weight: 600;
    transition: all .2s ease;
}
.stButton > button:hover,
[data-testid="stFileUploader"] button:hover {
    background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%);
    color: #FFFFFF;
    border-color: transparent;
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(99, 102, 241, .28);
}

/* ---------- Chat messages ---------- */
[data-testid="stChatMessage"] {
    background: #FFFFFF;
    border: 1px solid #E3E7F7;
    border-radius: 16px;
    padding: 14px 18px;
    margin-bottom: 12px;
    box-shadow: 0 2px 10px rgba(79, 70, 229, .06);
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: #EEF0FF;
    border-color: #D5DAFB;
}

/* ---------- Chat input ---------- */
[data-testid="stChatInput"] {
    background: #FFFFFF;
    border: 1.5px solid #D5DAFB;
    border-radius: 16px;
    box-shadow: 0 4px 18px rgba(79, 70, 229, .10);
}
[data-testid="stChatInput"]:focus-within {
    border-color: #6366F1;
    box-shadow: 0 4px 22px rgba(99, 102, 241, .22);
}

/* ---------- Small touches ---------- */
hr { border-color: #D6DBF2; }
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-thumb { background: #C3C9EE; border-radius: 8px; }
</style>
"""

HERO = """
<div class="hero">
  <h1 class="hero-title">📚 <span class="grad">Study Assistant</span></h1>
  <p class="hero-sub">Ask me anything about your uploaded study material.</p>
</div>
"""

HINTS = """
<div class="hint-grid">
  <div class="hint-card">
    <div class="ico">📑</div>
    <div class="ttl">Summarise a topic</div>
    <div class="txt">Get a quick recap of any unit from your notes.</div>
  </div>
  <div class="hint-card">
    <div class="ico">🎯</div>
    <div class="ttl">Find PYQ patterns</div>
    <div class="txt">See which questions keep repeating in past papers.</div>
  </div>
  <div class="hint-card">
    <div class="ico">🧠</div>
    <div class="ttl">Quiz yourself</div>
    <div class="txt">Ask for practice questions on what you just studied.</div>
  </div>
</div>
"""


def apply_style():
    """Call once, right after st.set_page_config(...) in app.py."""
    st.markdown(CSS, unsafe_allow_html=True)


def render_hero():
    st.markdown(HERO, unsafe_allow_html=True)


def render_hints():
    st.markdown(HINTS, unsafe_allow_html=True)