# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
Student reviews of Computer Science professors at Georgia State University. I collected the ratings and written reviews of 10 professors from the GSU Computer Science department on Rate My Professors.

This knowledge is hard to find through official channels because the course catalog only lists titles, times, and credit hours, not the things students actually care about: whether a professor's exams match their lectures, whether attendance matters, or whether grading is lenient or harsh. That information is spread across many separate reviews written for different courses at different times, so a student has to read through all of them to get the full picture. This system makes that scattered, opinion-based knowledge searchable with plain-language questions.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Rate My Professors – Abdullah Bal | 3.8/5, 20 reviews (CSC4520 Algorithms, CSC3210, CSC6260). | https://www.ratemyprofessors.com/professor/2942443 |
| 2 | Rate My Professors – Hongyu Ke |  3.7/5, 7 reviews (CSC3320 Systems / C).  | https://www.ratemyprofessors.com/professor/2926638 |
| 3 | Rate My Professors – Ian Pruitt  | 5.0/5, 3 short reviews (CSC2510). | https://www.ratemyprofessors.com/professor/3071554 |
| 4 |  Rate My Professors – Bhaskar Ray | First-year professor (CSC1301K), only 1 review (4.0/5). | https://www.ratemyprofessors.com/professor/3113022 |
| 5 |  Rate My Professors – Rajshekhar Sunderraman (Dr. Raj) | 4.8/5, 15 reviews. | https://www.ratemyprofessors.com/professor/2614203 |
| 6 | Rate My Professors – Farhan Tanvir | 3.0/5, 11 reviews (CSC4760 Data Mining).  | https://www.ratemyprofessors.com/professor/2962612 |
| 7 |  Rate My Professors – Preetham Thelluri  | 5.0/5, 3 short reviews (CSC2720 Data Structures). | https://www.ratemyprofessors.com/professor/2862699 |
| 8 |  Rate My Professors – Islam S M Towhidul | Polarizing, 30 reviews (2.8/5). | https://www.ratemyprofessors.com/professor/2920434 |
| 9 |  Rate My Professors – Ping Xu  | Graduate seminar (CSC8980), 1.0/5, 2 reviews. | https://www.ratemyprofessors.com/professor/3161718 |
| 10 |  Rate My Professors – Yanqing Zhang | 2.0/5, 11 reviews (CSC4810 AI, CSC4320 OS). | https://www.ratemyprofessors.com/professor/1806387 |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
One review per chunk. I split each file on its
"--- Review (...) ---" markers so that every chunk is exactly one complete review. Reviews are short, so in practice each chunk is roughly 40–120 words (about 200–700 characters). I don't enforce a fixed character count because a single review is already the natural unit of meaning. I also prepend the professor's name and course code to each chunk before embedding, since many reviews never name the professor themselves.

**Overlap:**
None between reviews. Each review is independent and about a
specific course and semester, so overlapping them would merge unrelated opinions (different courses, different years) into one chunk and hurt retrieval.

**Reasoning:**

My documents are short reviews, not long guides. A fixed character count would cut some reviews in half or merge several into one, so I split by review instead. This keeps each chunk as one complete opinion, which is what semantic
search needs. I also add the professor's name to each chunk, so a query like "is Pruitt easy?" can match a review that only says "He's easy" and never names him. Too small a chunk carries too little meaning to match; too large a chunk
matches everything and tells you nothing. One review per chunk avoids both.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

all-MiniLM-L6-v2 via sentence-transformers. It runs locally, needs no API key, and has no rate limits, which fits a free, offline project. It is small and fast, and my chunks are short reviews, so I don't need a large context window.

**Top-k:**

I retrieve the top 5 chunks per query (k=5). With short reviews, one chunk is often not enough to answer a question, so I pull a few so the LLM sees several
opinions. Too few (k=1) risks missing the relevant review; too many (k=15) adds unrelated reviews that pull the answer off-topic. I will tune k after seeing real results.

**Production tradeoff reflection:**

If cost weren't a constraint, I would weigh a larger embedding model (e.g. an OpenAI or Cohere embedding API) for better accuracy on domain-specific text, since student slang and course codes can confuse a small model. I would also consider multilingual support if reviews appeared in other languages, and context length if I later switched to long-form documents. The main tradeoffs are accuracy and features versus higher cost, added latency, and dependence on an external API instead of a local model.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Which GSU CS professor do students say gives the most useful feedback? | Dr. Raj Sunderraman — reviews repeatedly call him passionate, "gives good feedback," and accessible outside class. (sunderraman_gsu.txt) |
| 2 | How much of the grade in Towhidul's classes comes from exams?  | More than 50% of the grade comes from just 2 exams, and he gives no curve. (towhidul_gsu.txt) |
| 3 | What do students say about Hongyu Ke's exams? | The tests are very hard, but a generous curve saves students; reviewers also mention a language barrier. (ke_gsu.txt) |
| 4 | How are Yanqing Zhang's lectures described? | Disorganized and full of off-topic tangents (e.g. Chinese chess, a Waymo photo for 50 minutes); largely self-teaching. (zhang_gsu.txt) |
| 5 | Does attendance matter in Abdullah Bal's classes? | Yes — multiple reviews say you must attend; if you skip 50%+ of classes the course becomes much harder. (bal_gsu.txt) |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Polarizing professors give conflicting reviews. Some professors (Towhidul, Bal, Tanvir) have both very positive and very negative reviews. For a query like "is Bal a good professor?", the top-k chunks may pull a mix of 5-star and 1-star opinions, so the system could give a one-sided answer depending on which reviews happen to rank highest. The honest answer is "it's mixed," and the system may not capture that.

2. Low-coverage professors have too little data. Ray has only one review and Pruitt's reviews are very short and vague ("He's easy"). A specific question about these professors may retrieve a chunk that doesn't actually contain the answer, and the system might either say "not enough information" or, worse, fill the gap with general knowledge instead of the documents (a grounding failure / hallucination).

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

________________________________________________________________________
|                                                                      |
| 1. DOCUMENT INGESTION │  10 .txt files (GSU CS professor reviews)    |
|                                                                      |
|    Python file I/O   │   load each file, clean boilerplate           |
|                                                                      |
|______________________________________________________________________|

                                   │

                                   ▼

________________________________________________________________________
|                                                                      |
|     2. CHUNKING │   split on "--- Review ---" markers                |
|                                                                      |
| Python (custom) │ one review per chunk + prepend prof name/course    |
|                                                                      |
|______________________________________________________________________|

                                   │

                                   ▼

________________________________________________________________________
|                                                                      |
| 3. EMBEDDING + STORE │ embed chunks -> vectors, store with metadata  |
|                                                                      |
|       all-MiniLM-L6-v2  │  (sentence-transformers)                   |
|        + ChromaDB │   metadata: source filename, positio             |
|______________________________________________________________________|

                                   │

                                   ▼

─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─---------------------------

user question ──►
________________________________________________________________________
|                                                                      |
|       4. RETRIEVAL │   embed query, find top-k=5 nearest chunks      |
|                                                                      |
|            ChromaDB  │  return chunks + source metadata              |
|                                                                      |
|______________________________________________________________________|

                                   │

                                   ▼

________________________________________________________________________
|                                                                      |
|            5. GENERATION |  answer using ONLY retrieved chunks       |
|                                                                      |
|            Groq llama-3.3-70b   │  + cite source document(s)         |
|                                                                      |
|______________________________________________________________________|

                                   │

                                   ▼

                    grounded answer + sources

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

Retrieval. Tool: Claude. Input: Retrieval Approach (top-k=5). Ask it for a retrieve(query) function returning the top 5 chunks with scores and sources.
Verify: run 3 eval questions and check chunks are on-topic, distances below ~0.5.


**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
