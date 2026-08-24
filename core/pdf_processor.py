import fitz  # PyMuPDF

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF, page by page.
    Returns a list of dicts: [{"page": 1, "text": "..."}, ...]
    """
    doc = fitz.open(file_path)
    pages = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        if text.strip():  # skip blank pages
            pages.append({
                "page": page_num + 1,
                "text": text
            })

    doc.close()
    return pages