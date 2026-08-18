import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Model settings
LLM_MODEL = "openai/gpt-oss-20b"     # updated — llama-3.1-8b-instant was deprecated by Groq
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Chunking settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

# Paths
UPLOAD_DIR = "data/uploads"
CHROMA_DIR = "data/chroma_db"