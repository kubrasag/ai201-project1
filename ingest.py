"""Document ingestion + chunking pipeline.
Loads .txt files from documents/, cleans them, and splits into chunks.
"""
import os
import glob


def load_documents(folder="documents"):
    docs = []
    for path in sorted(glob.glob(os.path.join(folder, "*.txt"))):
        name = os.path.basename(path)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        if text.strip():
            docs.append({"source": name, "text": text})
    return docs


def clean_text(text):
    text = text.replace("&amp;", "&").replace("&#39;", "'").replace("&nbsp;", " ")
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def chunk_text(text, chunk_size=500, overlap=80):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if end < len(text):
            last_space = chunk.rfind(" ")
            if last_space > chunk_size * 0.5:
                chunk = chunk[:last_space]
                end = start + last_space
        chunk = chunk.strip()
        if len(chunk) > 0:
            chunks.append(chunk)
        start = end - overlap
    return chunks


def build_chunks(folder="documents"):
    docs = load_documents(folder)
    all_chunks = []
    for doc in docs:
        cleaned = clean_text(doc["text"])
        for i, c in enumerate(chunk_text(cleaned)):
            all_chunks.append({"text": c, "source": doc["source"], "position": i})
    return all_chunks


if __name__ == "__main__":
    chunks = build_chunks()
    print(f"Loaded {len(load_documents())} documents")
    print(f"Total chunks: {len(chunks)}\n")
    print("--- 5 sample chunks ---")
    for c in chunks[:5]:
        print(f"\n[{c['source']} #{c['position']}]")
        print(c["text"])
