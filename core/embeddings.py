from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

_model = None

def get_embedding_model():
    """Loads the embedding model once and reuses it (avoids reloading on every call)."""
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model

def embed_texts(texts):
    """Takes a list of strings, returns a list of embedding vectors."""
    model = get_embedding_model()
    return model.encode(texts).tolist()