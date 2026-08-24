from langchain_groq import ChatGroq
from config import GROQ_API_KEY, LLM_MODEL
from core.vector_store import query_chunks

_llm = None

def get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name=LLM_MODEL)
    return _llm

def answer_question(question):
    """
    Retrieves relevant chunks, builds a prompt, gets an answer from the LLM.
    Returns {"answer": "...", "sources": [{"source": ..., "page": ...}, ...]}
    """
    matches = query_chunks(question)

    if not matches:
        return {
            "answer": "I couldn't find anything relevant in your uploaded documents.",
            "sources": []
        }

    context = "\n\n".join(
        f"[Source: {m['source']}, Page {m['page']}]\n{m['text']}"
        for m in matches
    )

    prompt = f"""You are a helpful study assistant. Answer the student's question
using ONLY the context below. If the answer isn't in the context, say so honestly.

Context:
{context}

Question: {question}

Answer:"""

    llm = get_llm()
    response = llm.invoke(prompt)

    sources = [{"source": m["source"], "page": m["page"]} for m in matches]

    return {
        "answer": response.content,
        "sources": sources
    }