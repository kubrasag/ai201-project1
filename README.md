# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

Student reviews of Computer Science professors at Georgia State University. I collected
the ratings and written reviews of 10 professors from the GSU Computer Science department
on Rate My Professors.

This knowledge is hard to find through official channels because the course catalog only
lists titles, times, and credit hours, not the things students actually care about:
whether a professor's exams match their lectures, whether attendance matters, or whether
grading is lenient or harsh. That information is spread across many separate reviews
written for different courses at different times, so a student has to read through all of
them to get the full picture. This system makes that scattered, opinion-based knowledge
searchable with plain-language questions.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

One review per chunk. Each file is split on its "--- Review (...) ---" markers so that every chunk is exactly one complete review. Reviews are short, so in practice each chunk is roughly 40–120 words (about 200–700 characters). The professor's name and course code are prepended to each chunk before embedding.

**Overlap:**

None. Each review is independent and about a specific course and semester, so overlapping them would merge unrelated opinions (different courses, different years) into
one chunk and hurt retrieval. Overlap helps when one idea is split across a boundary; here each idea is one review and already fits in a single chunk.

**Why these choices fit your documents:**

My documents are short reviews, not long guides.
A fixed character count would cut some reviews in half or merge several into one, so I split by review instead. This keeps each chunk as one complete opinion, which is what
semantic search needs. Prepending the professor's name fixes the case where a review's text alone wouldn't be retrievable — a query like "is Pruitt easy?" can match a review that only says "He's easy" and never names him. Too small a chunk carries too little meaning to match; too large a chunk matches everything and tells you nothing. One review per chunk avoids both.

**Final chunk count:**

83 chunks across 10 documents.
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2 via sentence-transformers. It runs locally, needs no API key, and has no rate limits, which fits a free, offline project. It is small and fast, and my chunks are short reviews, so I don't need a large context window. Chunks are stored in ChromaDB using cosine distance.

**Production tradeoff reflection:**

If cost weren't a constraint, I would weigh a larger
embedding model (e.g. an OpenAI or Cohere embedding API) for better accuracy on domain-specific text, since student slang and course codes can confuse a small model. I would also consider multilingual support if reviews appeared in other languages, and context length if I later switched to long-form documents. The main tradeoffs are accuracy and features versus higher cost, added latency, and dependence on an external API instead of a local model.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

The LLM (Groq llama-3.3-70b-versatile) is instructed to answer ONLY using the retrieved review excerpts and to use no outside or general knowledge. If the excerpts do not contain enough information, it must reply exactly "I don't have enough information on that." The model also runs at a near-zero temperature to reduce invented content. This grounding was verified with an out-of-scope question ("What is the capital of France?"), which the system correctly declined to answer instead of replying "Paris."

**How source attribution is surfaced in the response:**

he retrieved chunks each carry a "source" metadata field (the filename). After generation, the unique source filenames of the retrieved chunks are collected and returned alongside the answer, and displayed in a
"Retrieved from (sources)" panel in the Gradio interface. Attribution is therefore added programmatically by the pipeline, not left to the LLM to invent.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 |  How much of the grade in Towhidul's classes comes from exams?  |  50%+ of the grade comes from 2 exams, no curve  |  Said 50% from 2 exams in CSC3320; in CSC2720, 2 tests (20% + 30% final)  |  Relevant  | Accurate |
| 2 |  Which professor gives the most useful feedback?  |  Dr. Raj Sunderraman (repeatedly "gives good feedback")  |  Named Abdullah Bal as the one with an explicit "Gives good feedback" tag, with Sunderraman second  |  Partially relevant  |  Partially accurate |
| 3 |  What do students say about Hongyu Ke's exams? |  Very hard tests, saved by a generous curve; language barrier |  Tests "very, very hard," "insane" curve helped a student get a B, test reviews "very vague" | Relevant | Accurate |
| 4 |  How are Yanqing Zhang's lectures described?  |  Disorganized, off-topic tangents, self-teaching |  "Horribly disorganized," "could have been done in half the time," goes off on tangents | Relevant | Accurate |
| 5 |  Does attendance matter in Abdullah Bal's classes? |  Yes — must attend; skipping 50%+ makes it hard |  Yes, rewards participation, attendance mandatory, skipping 50%+ makes the class hard  | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
"Which professor gives the most useful feedback?"

**What the system returned:**
It named Abdullah Bal as the professor who gives the most
useful feedback, because one of his retrieved reviews carried an explicit "Gives good feedback" tag. Dr. Raj Sunderraman — whose file actually contains the most "gives good feedback" reviews across many entries — was mentioned only secondarily.

**Root cause (tied to a specific pipeline stage):**
This is a retrieval limitation, not a generation error. The system retrieves only the top k=5 chunks and the LLM answers from those alone. The question asks for a "most" comparison, which requires counting evidence across the entire corpus. Sunderraman's many "gives good feedback" reviews are spread over his file, and only a couple of them landed in the top 5, while a single strongly-tagged Bal
review ranked high. Because the model never sees the full set of reviews, it cannot tally who has the most positive feedback overall — it can only reason over the 5 chunks it was given. Superlative/aggregation questions are a known weak spot for top-k RAG.

**What you would change to fix it:**
Increase k for aggregation-style questions, or add a
counting step that groups retrieved chunks by professor before answering. A more robust fix would be metadata filtering or a pre-aggregation pass that summarizes each professor's reviews, so superlative questions reason over summaries rather than a small sample of raw
chunks.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
Deciding the chunking strategy in planning.md before writing code saved a lot of rework. Because I had already reasoned that each review should be one chunk and that the professor's name should be prepended, the ingestion code had a clear target. When I later saw that short reviews like "He's easy" would otherwise be unretrievable, the spec had already anticipated it, so I didn't have to redesign the pipeline mid-build.

**One way your implementation diverged from the spec, and why:**
The spec planned for top-k= 5 with the assumption that 5 chunks would be enough context. During testing I first used
k=6 and saw loosely related chunks from other professors appearing in the source list, so I moved to k=5 to match the spec and reduce noise. I also added cosine distance to ChromaDB, which wasn't in the original spec — the default squared-L2 distance produced scores above 1.0 that were hard to interpret, and cosine brought the relevant results below 0.5 as the spec's checkpoint expected.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* My Chunking Strategy section from planning.md plus a sample of one review file, and asked it to implement the document loading and chunking in ingest.py.

- *What it produced:*
A loader using pathlib and a parser that split each file on the "--- Review ---" markers with a regex, prepending the professor name to each chunk.

- *What I changed or overrode:*
The first version left a stray double parenthesis around
the course info, so I added a .strip("()") to clean it. I also restructured the chunks from plain (filename, text) tuples into dicts with text/source/position so the vector
store could store proper metadata.

**Instance 2**

- *What I gave the AI:*

My grounding requirement and the Retrieval Approach section, and asked it to write the generation step in query.py and a Gradio interface.

- *What it produced:*
A Groq call with a grounding system prompt, a function returning the answer plus unique sources, and a Gradio Blocks UI.

- *What I changed or overrode:*
I verified that the system prompt actually enforced
grounding by testing an out-of-scope question, and confirmed the model declined instead of using general knowledge. I lowered the temperature to keep answers grounded, and reduced k from 6 to 5 after seeing unrelated sources appear in the attribution list.