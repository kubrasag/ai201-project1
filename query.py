"""Grounded answer generation with Groq.
Retrieves relevant chunks and asks the LLM to answer ONLY from them.
"""
import os
from dotenv import load_dotenv
from groq import Groq
from vectorstore import setup_collection, retrieve

load_dotenv()
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

# Build the vector store once when this module is imported.
_collection = setup_collection()

SYSTEM_PROMPT = """You are an assistant that answers questions about Georgia State \
University CS professors using student reviews.
Answer ONLY using the information in the provided review excerpts below.
Do NOT use any outside or general knowledge.
If the excerpts do not contain enough information to answer, reply exactly: \
"I don't have enough information on that."
Keep your answer concise and specific."""


def ask(question, k=6):
    chunks = retrieve(_collection, question, k=k)
    context = "\n\n".join(
        f"[Source: {c['source']}]\n{c['text']}" for c in chunks
    )
    user_prompt = f"""Review excerpts:
{context}

Question: {question}

Answer using only the excerpts above."""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.1,
    )
    answer = response.choices[0].message.content

    sources = list(dict.fromkeys(c["source"] for c in chunks))
    return {"answer": answer, "sources": sources}


if __name__ == "__main__":
    for q in [
        "Which professor has the best reviews and highest rating?",
        "What do students say about Professor Towhidul's exams?",
        "What is the capital of France?",  # out-of-scope test
    ]:
        print(f"\n=== {q} ===")
        result = ask(q)
        print(result["answer"])
        print("Sources:", result["sources"])