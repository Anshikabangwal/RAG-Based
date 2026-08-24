from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_pages(pages, source_name):
    """
    Takes pages [{"page": 1, "text": "..."}] and splits them into chunks.
    Returns a list of dicts: [{"text": "...", "page": 1, "source": "file.pdf"}, ...]
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = []
    for page in pages:
        split_texts = splitter.split_text(page["text"])
        for text in split_texts:
            chunks.append({
                "text": text,
                "page": page["page"],
                "source": source_name
            })

    return chunks