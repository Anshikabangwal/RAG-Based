import chromadb
from config import CHROMA_DIR
from core.embeddings import embed_texts

_client = None
_collection = None

def get_collection():
    """Creates/loads a persistent ChromaDB collection."""
    global _client, _collection
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_DIR)
        _collection = _client.get_or_create_collection(name="study_docs")
    return _collection

def add_chunks(chunks):
    """
    Embeds and stores chunks in ChromaDB.
    chunks: [{"text": ..., "page": ..., "source": ...}, ...]
    """
    collection = get_collection()
    texts = [c["text"] for c in chunks]
    embeddings = embed_texts(texts)

    ids = [f"{c['source']}_p{c['page']}_{i}" for i, c in enumerate(chunks)]
    metadatas = [{"page": c["page"], "source": c["source"]} for c in chunks]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas
    )

def query_chunks(question, n_results=4):
    """
    Finds the most relevant chunks for a question.
    Returns list of {"text": ..., "page": ..., "source": ...}
    """
    collection = get_collection()
    question_embedding = embed_texts([question])[0]

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )

    matches = []
    docs = results["documents"][0]
    metas = results["metadatas"][0]

    for doc, meta in zip(docs, metas):
        matches.append({
            "text": doc,
            "page": meta["page"],
            "source": meta["source"]
        })

    return matches