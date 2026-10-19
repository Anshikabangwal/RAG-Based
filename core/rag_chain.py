from langchain_groq import ChatGroq
from config import GROQ_API_KEY, LLM_MODEL
from core.vector_store import query_chunks

_llm = None

def get_llm():
    global _llm
    if _llm is None:
        _llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name=LLM_MODEL)
    return _llm

def answer_question(question, chat_id):
    """
    Retrieves relevant chunks (from this chat's PDFs only), builds a prompt,
    gets an answer from the LLM.
    Returns {"answer": "...", "sources": [{"source": ..., "page": ...}, ...]}
    """
    matches = query_chunks(question, chat_id)
    llm = get_llm()

    # No documents in this chat: just chat normally
    if not matches:
        prompt = f"""You are a friendly, helpful study assistant. The student has not
uploaded any documents in this chat yet. Reply to their message normally and helpfully.
If they ask about their own notes or PDFs, tell them to upload and process a PDF
in the sidebar first.

Student: {question}

Reply:"""
        response = llm.invoke(prompt)
        return {"answer": response.content, "sources": []}

    context = "\n\n".join(
        f"[Source: {m['source']}, Page {m['page']}]\n{m['text']}"
        for m in matches
    )

    prompt = f"""You are a friendly, helpful study assistant.

- For greetings or general conversation, reply normally and ignore the context.
- For questions about the student's study material, answer using ONLY the context
  below. If the answer isn't in the context, say so honestly.

Context:
{context}

Student: {question}

Reply:"""

    response = llm.invoke(prompt)

    # Don't show sources for plain small talk
    small_talk = question.strip().lower().rstrip("!?. ") in {
        "hi", "hello", "hey", "thanks", "thank you", "ok", "okay", "bye"
    }
    sources = [] if small_talk else [
        {"source": m["source"], "page": m["page"]} for m in matches
    ]

    return {
        "answer": response.content,
        "sources": sources
    }