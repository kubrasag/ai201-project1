"""Document ingestion + chunking pipeline.
Loads .txt files from documents/, cleans them, and splits into chunks.
"""
from pathlib import Path
import re

DOCUMENTS_DIR = Path("documents")

def load_documents():
    """Read every .txt file in documents/ and return a list of (filename, txt) pairs"""
    documents = []
    for file_path in sorted(DOCUMENTS_DIR.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8")
        documents.append((file_path.name, text))
    return documents

def parse_document(filename, text):
    """ Take one file's text and return a list of chinks.
    Each chunk is one review with the professor name + course attached"""

    #1. Pull the professor's name out of the header (the "Professor:" line)
    prof_match = re.search(r"Professor:\s*(.+)", text)
    professor = prof_match.group(1).strip() if prof_match else "Unknown professor"

    #2. Split the text on the "--- Review (...) ---" markers.
    # re.split keeps everything between markers as separate pieces.
    parts = re.split(r"--- Review (.+?) ---", text)
    # parts[0] is the header block (before the first review), we skip it.
    #After that, parts come in pairs: (review_info, review_text), (review_info, review_text)...

    chunks = []
    # step through the parts two at a time: info, then body
    for i in range(1, len(parts), 2):
        review_info = parts[i].strip("()") #e.g. "CSC2510, DEc 2025, Grade A+"
        review_body = parts[i+1].strip() # the actuial review text

        # 3. Buil dthe chunk: prepend professor + course info to the review
        chunk_text = f"Professor {professor} ({review_info}): {review_body}"
        chunks.append(chunk_text)
    return chunks

def build_all_chunks():
    """Load every document and return a list of (filename, chunk_text) pairs."""
    docs = load_documents()
    all_chunks = []
    for filename, text in docs:
        for chunk in parse_document(filename, text):
            all_chunks.append((filename, chunk))
    return all_chunks