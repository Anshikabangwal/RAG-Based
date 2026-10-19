import streamlit as st

CSS = """
<style>
/* ---------- Calm, spacious study workspace ---------- */
.stApp {
    background:
        radial-gradient(ellipse at 80% 0%, rgba(124, 58, 237, .08), transparent 32rem),
        linear-gradient(180deg, #F7F8FC 0%, #F0F2F9 100%);
    color: #20243A;
}
.block-container {
    max-width: 1180px;
    padding-top: 2.2rem;
    padding-bottom: 7rem;
}
header[data-testid="stHeader"] {
    background: transparent;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #F0F1FB 0%, #E9EBF7 100%);
    border-right: 1px solid #DFE2F0;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #27294F;
}
section[data-testid="stSidebar"] [data-testid="stFileUploader"] section {
    background: rgba(255, 255, 255, .78);
}

/* ---------- Hero (title + subtitle) ---------- */
.hero { padding: .25rem 0 1rem 0; }
.hero-title {
    font-size: clamp(2.2rem, 5vw, 3.1rem);
    font-weight: 800;
    letter-spacing: -1.2px;
    margin: 0;
    color: #20243A;
}
/* gradient only on the text, so the emoji keeps its colour */
.hero-title .grad {
    background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    color: #737895;
    margin: 0.55rem 0 0 0;
    font-size: 1rem;
}

/* ---------- Status cards ---------- */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, .82);
    border: 1px solid #E5E7F1;
    border-radius: 14px;
    padding: .85rem 1rem;
    box-shadow: 0 4px 16px rgba(35, 40, 84, .04);
}
[data-testid="stMetricLabel"] {
    color: #777C98;
    font-size: .82rem;
}
[data-testid="stMetricValue"] {
    color: #34316F;
    font-size: 1.5rem;
    font-weight: 750;
}

/* ---------- Empty-state hint cards ---------- */
.hint-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-top: 1.15rem;
}
.hint-card {
    background: rgba(255, 255, 255, .88);
    border: 1px solid #E4E6F1;
    border-radius: 16px;
    padding: 17px 18px;
    box-shadow: 0 5px 18px rgba(45, 49, 94, .05);
    transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
}
.hint-card:hover {
    transform: translateY(-2px);
    border-color: #B9C0F3;
    box-shadow: 0 8px 20px rgba(79, 70, 229, .12);
}
.hint-card .ico { font-size: 1.3rem; }
.hint-card .ttl { font-weight: 700; color: #34316F; margin: 6px 0 2px 0; font-size: .95rem; }
.hint-card .txt { color: #737895; font-size: .85rem; line-height: 1.45; }
@media (max-width: 700px) {
    .hint-grid { grid-template-columns: 1fr; }
}

/* ---------- File uploader card ---------- */
[data-testid="stFileUploader"] section {
    background: #FFFFFF;
    border: 1.5px dashed #A9ADE0;
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
    border-radius: 11px;
    border: 1px solid #D8D9EC;
    background: #FFFFFF;
    color: #403D83;
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
    background: rgba(255, 255, 255, .94);
    border: 1px solid #E6E7F0;
    border-radius: 18px;
    padding: 16px 20px;
    margin-bottom: 14px;
    box-shadow: 0 5px 18px rgba(41, 45, 87, .045);
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: #F0F0FF;
    border-color: #DCDDF5;
}
[data-testid="stChatMessage"] p {
    line-height: 1.7;
}

/* ---------- Chat input ---------- */
[data-testid="stChatInput"] {
    background: #FFFFFF;
    border: 1.5px solid #DCDDF0;
    border-radius: 17px;
    box-shadow: 0 5px 22px rgba(56, 52, 126, .09);
}
[data-testid="stChatInput"]:focus-within {
    border-color: #7773D6;
    box-shadow: 0 5px 24px rgba(99, 92, 194, .18);
}

/* ---------- Source and settings panels ---------- */
[data-testid="stExpander"] {
    background: rgba(255, 255, 255, .68);
    border: 1px solid #E5E6F0;
    border-radius: 13px;
}

/* ---------- Small touches ---------- */
hr { border-color: #E0E2ED; }
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-thumb { background: #C9CBE0; border-radius: 8px; }
</style>
"""

HERO = """
<div class="hero">
  <h1 class="hero-title">📚 <span class="grad">Study Assistant</span></h1>
  <p class="hero-sub">Grounded answers from your notes, with optional web research for missing details.</p>
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