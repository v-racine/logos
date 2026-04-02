# Logos RAG — Diagnosis Summary

## Methodology

To evaluate the structural limitations of the Logos RAG system, I designed and ran targeted queries against the full 21-paper corpus using the Gradio UI with full observability enabled (retrieved chunks with similarity scores, and the complete prompt sent to the LLM). Three failure modes were observed: chunking boundary splits, contradictory retrieval, and temporal ordering failure. Two queries were run per failure mode. Full query outputs, prompts, retrieved chunks, and analysis are documented in `DIAGNOSIS.md`.

**System configuration at time of diagnosis (2026-03-31):**

- Chunking: character-based, 512 chars, 100 char overlap
- Retrieval: cosine similarity via pgvector HNSW index, top 5 chunks
- Embedding model: text-embedding-3-small (1536 dimensions)
- Generation model: gpt-4o, temperature 0.3, max 1024 tokens
- Corpus: 21 papers on epistemic opacity in AI/ML (2023–2026)

---

## Failure 1: Chunking Boundary Splits an Argument

512-character chunking splits philosophical arguments mid-sentence and mid-word.
Retrieval returns fragments — premises without conclusions, or conclusions without
premises — and the LLM produces plausible-sounding but incomplete answers that
mask the information gap.

The most striking finding: bibliography chunks score _higher_ than substantive argument
passages because of keyword density. In one query, a chunk containing only DOIs and
page numbers scored 0.807, the highest of the five retrieved chunks, while the actual
argument was cut mid-word at "epistemica" right before its payoff. The LLM answered
confidently despite receiving almost no usable content.

_See DIAGNOSIS.md, Failure 1 (Queries 1A and 1B) for full prompts and analysis._

---

## Failure 2: Contradictory Chunks Blended or Ignored

The corpus contains a multi-paper debate with directly opposing claims. Cosine
similarity retrieves by relevance to the query, not coherence with other retrieved
chunks. The result is either asymmetric representation (one side dominates) or
complete erasure of the opposition.

The most striking finding: when asked "Can we have a satisfactory social epistemology
of AI-based science?", all five retrieved chunks came from Koskinen. Zero chunks from
Peters, Ortmann, or anyone who disagrees. The LLM presented a contested claim as
settled fact; no hedge, and no mention of a debate. This is the most dangerous failure
mode: the user receives a confident, well-written answer that is structurally one-sided
with no visible signal that a counter-position exists.

Root cause: cosine similarity matches vocabulary, not conceptual relationships. Peters
and Ortmann argue against Koskinen using different vocabulary, so they don't surface
when Koskinen's phrasing drives the query.

_See DIAGNOSIS.md, Failure 2 (Queries 2A and 2B) for full prompts and analysis._

---

## Failure 3: Temporal Ordering — Outdated Claims Without Supersession Signals

The corpus contains a five-paper debate chain (Koskinen 2024a → Peters 2024a →
Koskinen 2024b → Peters 2024b → Ortmann 2025), but the system stores no publication
date metadata and treats all chunks as equally current.

The most striking finding: when asked for Koskinen's _current_ position, the LLM cited
her 2024a paper, missing her 2024b refinement entirely. The most temporally relevant
chunk (Peters 2024b, which explicitly states "She has now replied") scored lowest
(0.695). Queries using temporal language ("current", "latest", "over the last year")
produce answers anchored to whichever paper's vocabulary happened to score highest rather than the most recent paper.

_See DIAGNOSIS.md, Failure 3 (Queries 3A and 3B) for full prompts and analysis._

---

## Structural vs. Fixable: A Distinction

Not all failures are equally addressable:

**Potentially improvable with architectural changes:**

- Mid-word/mid-sentence truncation → sentence-aware or paragraph-aware chunking
- Bibliography chunk pollution → filtering chunks below a minimum content threshold
- Temporal ordering → storing publication year as structured metadata and surfacing
  it in the retrieval context or prompt

**Fundamental to flat cosine retrieval (not fixable without architectural redesign):**

- Vocabulary-driven retrieval bias (Failure 2) → requires concept-aware retrieval,
  hypothetical document embeddings, or query expansion strategies
- Inability to reason about conceptual opposition → requires graph-based or
  citation-aware retrieval, not vector similarity alone

---

## Actionable Insights

### Short-term improvements (low implementation cost)

**1. Surface publication year in the retrieval context**

The simplest mitigation for Failure 3. Add a `year` field to the `papers` table and
include it when building the context string in `llm.py`:

```python
f"[Source: {chunk.paper_title} ({chunk.publication_year})]\n{chunk.content}"
```

This doesn't give the LLM the ability to reason about ordering, but it gives the user
and the LLM a visible signal about relative recency. A prompt instruction can reinforce
this: _"When sources conflict, prefer more recent publications."_

**2. Filter bibliography chunks at index time**

Add a minimum content-length threshold in `IndexingService` before embedding:

```python
if len(text) < 100:  # skip very short chunks
    continue
```

A more robust version would use a heuristic to detect reference-list chunks (e.g., high
density of DOI strings or author-year citation patterns) and exclude them from the index.

**3. Increase chunk size**

Increasing `chunk_size` from 512 to 1500–2000 characters (approximately 400–500 tokens)
would reduce mid-sentence truncation and keep more argumentative context together. The
tradeoff is reduced retrieval precision, but larger chunks are more likely to contain
irrelevant content alongside relevant content. Worth testing with the same diagnostic
queries to compare before/after.

### Medium-term improvements (moderate implementation cost)

**4. Sentence-aware chunking**

Replace character-based splitting with sentence-aware splitting using a library like
`spacy` or `nltk`. Chunks would always start and end at sentence boundaries, eliminating
mid-word truncation entirely. The chunk size would vary but would preserve semantic units.

**5. Conversation history**

Add session-scoped conversation history to the Gradio UI, passing prior Q&A pairs as
additional context in the LLM prompt. This directly addresses a UX consequence of
Failure 1. Users can ask follow-up questions to recover missing context rather than
being stranded by a truncated first answer. Implementation requires updating
`LLMClient.generate()` to accept an optional `history` parameter and modifying the
Gradio handler to maintain and pass the session history.

### Long-term improvements (high implementation cost)

**6. Metadata-filtered retrieval**

Store structured metadata (publication year, authors, source URL) as separate columns
in the `chunks` table and expose them as retrieval filters. A user asking "what did
Koskinen argue in 2024?" could filter by author and year rather than relying on
similarity alone.

**7. Hypothetical document embeddings (HyDE)**

Rather than embedding the user's query directly, use an LLM to generate a hypothetical
answer to the query, embed that instead, and use it to retrieve similar chunks. This
partially addresses Failure 2. The hypothetical answer would use the vocabulary of
the expected response, not just the query, improving retrieval of conceptually relevant
but lexically different passages.

**8. Citation-graph-aware retrieval**

Build a citation graph from the corpus and use it to surface related papers alongside
similarity-retrieved chunks. A paper that cites Koskinen (2024a) is likely to be
relevant to queries about Koskinen's argument, regardless of cosine similarity. This
directly addresses the invisibility of Ortmann and Peters in Failure 2 and 3 queries.

> Co-Authored-By: Claude Opus 4.6
