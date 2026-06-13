"""Embedding + vector store + retrieval.
Embeds chunks with all-MiniLM-L6-v2 and stores them in ChromaDB.
"""
import chromadb
from sentence_transformers import SentenceTransformer
from ingest import build_chunks

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.Client()  # in-memory; rebuilt each run


def setup_collection():
    chunks = build_chunks()
    try:
        client.delete_collection("guide")
    except Exception:
        pass
    
    collection = client.create_collection(
        "guide",
        metadata={"hnsw:space": "cosine"},
    )

    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True).tolist()
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"source": c["source"], "position": c["position"]} for c in chunks]

    collection.add(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)
    print(f"Embedded and stored {len(chunks)} chunks.")
    return collection


def retrieve(collection, query, k=4):
    q_emb = model.encode([query]).tolist()
    results = collection.query(query_embeddings=q_emb, n_results=k)
    out = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        out.append({"text": doc, "source": meta["source"], "distance": dist})
    return out


if __name__ == "__main__":
    collection = setup_collection()
    test_queries = [
        "Which professor has the highest rating and best student reviews?",
        "Professor Towhidul exams tests don't match what is taught",
        "Hongyu Ke accent language barrier hard to understand lectures",
    ]
    for q in test_queries:
        print(f"\n=== {q} ===")
        for r in retrieve(collection, q, k=6):
            print(f"[{r['source']}] distance={r['distance']:.3f}")
            print("   " + r["text"][:120].replace("\n", " "))