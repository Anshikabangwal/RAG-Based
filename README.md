# 📚 Multi-PDF Student Preparation Assistant

A RAG (Retrieval-Augmented Generation) based AI study assistant. Upload your syllabus, lecture notes, textbooks, and previous-year question papers (PYQs) — the system answers your questions using your own study material, and analyzes PYQs to highlight high-priority topics.

---

## 🔄 What it does

1. **Upload documents** — syllabus, notes, textbooks, PYQs
2. **Ask questions** — get answers grounded in your uploaded material (not generic AI knowledge)
3. **PYQ analysis** — automatically detects frequently repeated questions/topics across years and tells you what to prioritize

---

## 🧠 Tech Stack

| Piece | Tool |
|---|---|
| Language | Python |
| UI | Streamlit |
| PDF extraction | PyMuPDF |
| RAG orchestration | LangChain |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Vector database | ChromaDB |
| LLM | Groq API (`openai/gpt-oss-20b`) |

---

## ⚙️ Setup Instructions

Follow these steps exactly, in order, the first time you set up the project on your machine.

### 1. Clone the repository

\`\`\`bash
git clone https://github.com/Anshikabangwal/RAG-Based.git
cd RAG-Based
\`\`\`

### 2. Create a virtual environment

This keeps this project's Python packages separate from everything else on your system.

\`\`\`bash
python -m venv venv
\`\`\`

Activate it:

- **Windows (PowerShell):**
  \`\`\`powershell
  .\\venv\\Scripts\\Activate.ps1
  \`\`\`
- **Windows (cmd):**
  \`\`\`cmd
  venv\\Scripts\\activate.bat
  \`\`\`
- **Mac/Linux:**
  \`\`\`bash
  source venv/bin/activate
  \`\`\`

You'll know it worked when you see `(venv)` at the start of your terminal line. **Do this every time** you open a new terminal to work on this project.

### 3. Install dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

This may take a few minutes — some packages (like `torch`, used by sentence-transformers) are large.

### 4. Set up your Groq API key

Each teammate needs their **own** free Groq API key.

1. Go to [console.groq.com](https://console.groq.com) and sign up (free, no credit card)
2. Left sidebar → **API Keys** → **Create API Key**
3. Copy the key immediately — Groq only shows it once

Create a file called `.env` in the project root (same folder as `app.py`) and add:

\`\`\`
GROQ_API_KEY=your_actual_key_here
\`\`\`

> ⚠️ **Never commit `.env` to GitHub.** It's already in `.gitignore`, so this should happen automatically — but double-check before pushing if you ever see it listed in `git status`.

### 5. Verify your setup works

Run the test script:

\`\`\`bash
python test.py
\`\`\`

If it prints back a short sentence from the model, your setup is complete and working.

### 6. Run the app

\`\`\`bash
streamlit run app.py
\`\`\`

This opens the app in your browser automatically (usually at `http://localhost:8501`).

---

## 📁 Project Structure

\`\`\`
RAG-Based/
├── app.py                     # Main Streamlit app (entry point)
├── config.py                  # Settings — model names, chunk size, paths
├── requirements.txt           # Python dependencies
├── .env                       # Your API key (not committed — create this yourself)
│
├── core/
│   ├── pdf_processor.py       # Extract text from PDFs
│   ├── chunker.py             # Split text into chunks
│   ├── embeddings.py          # Generate embeddings
│   ├── vector_store.py        # ChromaDB setup, add/query
│   ├── rag_chain.py           # Retrieval + LLM → final answer
│   │
│   └── pyq_analysis/          # PYQ analysis — the project's key differentiator
│       ├── question_extractor.py   # Pull questions out of PYQ PDFs
│       ├── topic_classifier.py     # Map questions → syllabus units
│       └── frequency_analyzer.py   # Count repeats, generate insights
│
├── data/
│   ├── uploads/                # Uploaded PDFs (local only, gitignored)
│   └── chroma_db/               # Vector DB storage (local only, gitignored)
│
├── utils/
│   └── helpers.py               # Shared helper functions
│
└── tests/                       # Test files
\`\`\`

**Note:** `data/uploads/` and `data/chroma_db/` are intentionally excluded from Git. They're generated locally when you use the app — every teammate will have their own local copies with their own test PDFs.

---

## 🔧 Common Issues

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` after install | Make sure `(venv)` shows in your terminal prompt — you may have forgotten to activate the virtual environment |
| Pylance shows red underlines on imports in VS Code | `Ctrl+Shift+P` → "Python: Select Interpreter" → choose the one inside `venv\Scripts\python.exe` |
| Groq model errors (`model_not_found`) | Groq occasionally deprecates model names — check [console.groq.com/docs/models](https://console.groq.com/docs/models) for current active models and update `LLM_MODEL` in `config.py` |
| `.env` not being read | Confirm the file is named exactly `.env` (not `.env.txt`) and is in the project root, not inside a subfolder |

---

## 🤝 Working as a team

- Pull the latest changes before starting work each session: `git pull`
- After making changes: `git add .` → `git status` (double check nothing unwanted is staged) → `git commit -m "describe your change"` → `git push`
- Each person uses their **own** `.env` with their own Groq key — never share API keys inside code or commits