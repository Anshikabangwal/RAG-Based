# 📚 Multi-PDF Student Preparation Assistant

A RAG (Retrieval-Augmented Generation) based AI study assistant with a chatbot-style interface. Upload your syllabus, lecture notes, textbooks, and previous-year question papers (PYQs) — the system answers your questions using your own study material, and (coming soon) analyzes PYQs to highlight high-priority topics.

---

## 🔄 What it does

1. **Upload documents** — syllabus, notes, textbooks, PYQs (sidebar)
2. **Chat with your material** — ask questions in a chatbot-style interface, get answers grounded in your uploaded content, with inline citations linked to source page references; recent conversation turns help resolve follow-up questions
3. **Optional web fallback** — enable “Use web for missing information” in the sidebar to search DuckDuckGo when your uploaded material cannot fully answer a question. For gap-research requests, the assistant searches each candidate topic separately and only reports gaps supported by exact quotes from retrieved PDF excerpts. It describes those as excerpt-level gaps, not proof that the whole syllabus omits a topic. Web references are labeled separately from PDF page citations; web search is off by default and needs no API key.
4. **Regenerate answers** — use the button below a previous assistant answer to request a fresh response to that question; its references are refreshed as well.
5. **PYQ analysis** *(in progress)* — will detect frequently repeated questions/topics across years and tell you what to prioritize

---

## 🧠 Tech Stack

| Piece | Tool |
|---|---|
| Language | Python |
| UI | Streamlit (chat interface via `st.chat_message` / `st.chat_input`) |
| PDF extraction | PyMuPDF |
| RAG orchestration | LangChain |
| Text splitting | `langchain-text-splitters` |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| Vector database | ChromaDB |
| LLM | Groq API (`openai/gpt-oss-20b`) |
| Optional web fallback | DuckDuckGo via `ddgs` |

---

## ⚙️ Setup Instructions

Follow these steps exactly, in order, the first time you set up the project on your machine.

### 1. Clone the repository

```bash
git clone https://github.com/Anshikabangwal/RAG-Based.git
cd RAG-Based
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (cmd):**
  ```cmd
  venv\Scripts\activate.bat
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

You'll know it worked when you see `(venv)` at the start of your terminal line. **Do this every time** you open a new terminal to work on this project.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

This may take several minutes — `torch` (used by sentence-transformers) is a large download. Let it run fully to completion without interrupting it.

Afterward, confirm everything installed correctly:
```bash
pip list
```
You should see `streamlit`, `langchain`, `langchain-community`, `langchain-groq`, `langchain-text-splitters`, `chromadb`, `sentence-transformers`, `python-dotenv`, `pymupdf`, `ddgs` in the list.

### 4. Set up your Groq API key

Each teammate needs their **own** free Groq API key.

1. Go to [console.groq.com](https://console.groq.com) and sign up (free, no credit card)
2. Left sidebar → **API Keys** → **Create API Key**
3. Copy the key immediately — Groq only shows it once

Create a file called `.env` in the project root (same folder as `app.py`) and add:

```
GROQ_API_KEY=your_actual_key_here
```

> ⚠️ **Never commit `.env` to GitHub.** It's already in `.gitignore` — double-check before pushing if you ever see it listed in `git status`.

### 5. Verify your Groq connection works

```bash
python test.py
```

If it prints back a short sentence from the model, your API key and connection are working.

### 6. Run the app

```bash
streamlit run app.py --server.headless true
```

Then open **http://localhost:8501** in your browser (Chrome or Edge recommended).

> **First run only:** the app will download the embedding model (`all-MiniLM-L6-v2`, ~90MB) from Hugging Face the first time you process a document. This is a one-time download — subsequent runs use the cached copy. Let it finish; the page may appear blank/idle in your browser until the download completes.

---

## 📁 Project Structure

```
RAG-Based/
├── app.py                     # Main Streamlit app — chat UI (entry point)
├── config.py                  # Settings — model names, chunk size, paths
├── requirements.txt           # Python dependencies
├── test.py                    # Quick script to verify Groq API connection
├── .env                       # Your API key (not committed — create this yourself)
│
├── core/
│   ├── pdf_processor.py       # Extract text from PDFs (PyMuPDF)
│   ├── chunker.py             # Split text into chunks (langchain-text-splitters)
│   ├── embeddings.py          # Generate embeddings (sentence-transformers)
│   ├── vector_store.py        # ChromaDB setup, add/query
│   ├── rag_chain.py           # Retrieval + LLM → final answer with sources
│   ├── web_search.py          # Optional DuckDuckGo lookup for missing information
│   │
│   └── pyq_analysis/          # PYQ analysis — the project's key differentiator (in progress)
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
```

**Note:** `data/uploads/` and `data/chroma_db/` are intentionally excluded from Git. They're generated locally when you use the app — every teammate will have their own local copies with their own test PDFs.

---

## 🔧 Common Issues

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` after install | Make sure `(venv)` shows in your terminal prompt — you may have forgotten to activate the virtual environment |
| Pylance shows red underlines on imports in VS Code | `Ctrl+Shift+P` → "Python: Select Interpreter" → choose the one inside `venv\Scripts\python.exe` |
| Groq model errors (`model_not_found`) | Groq occasionally deprecates model names — check [console.groq.com/docs/models](https://console.groq.com/docs/models) for current active models and update `LLM_MODEL` in `config.py` |
| `.env` not being read | Confirm the file is named exactly `.env` (not `.env.txt`) and is in the project root, not inside a subfolder |
| Web fallback returns an error or no references | Check your internet connection. Web lookup is optional and can be disabled in the sidebar; answers will then use only the uploaded PDFs |
| Blank white page in browser after `streamlit run` | Usually means the embedding model is still downloading in the background (first run only) — wait a minute, then refresh. If it persists, check the terminal for a real traceback and check the browser DevTools Console (F12) for errors |
| Terminal floods with `ModuleNotFoundError: No module named 'torchvision'` warnings | Harmless — this is Streamlit's file watcher scanning unrelated vision-model submodules inside `transformers`. We don't use `torchvision` in this project. Can be silenced (see `app.py` — `warnings.filterwarnings` / logging suppression near the top) |
| App unexpectedly prints "Stopping..." right after starting | Usually caused by another terminal/process already using port 8501, or an accidental `Ctrl+C`. Run `netstat -ano \| findstr :8501` to check, and use a single, untouched terminal tab per run |

---

## 🤝 Working as a team

- Pull the latest changes before starting work each session: `git pull`
- After making changes: `git add .` → `git status` (double check nothing unwanted is staged) → `git commit -m "describe your change"` → `git push`
- Each person uses their **own** `.env` with their own Groq key — never share API keys inside code or commits
- Run `python test.py` after pulling to quickly confirm your local setup still works before diving into feature work

---

## 🗺️ Roadmap

- [x] Multi-PDF upload and processing
- [x] Chat-based Q&A with source/page references
- [ ] PYQ question extraction
- [ ] Topic classification (map questions → syllabus units)
- [ ] Frequency analysis and priority-topic insights
- [ ] Unit-wise preparation dashboard