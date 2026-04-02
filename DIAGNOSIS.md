# RAG Failure Diagnosis

This document records three structural failure modes observed in the Logos RAG system, diagnosed by querying the system deliberately and examining the full prompt, retrieved chunks, and generated answers.

**Initial System Configuration (2026-03-31):**

- Chunking: character-based, 512 chars, 100 char overlap
- Retrieval: cosine similarity via pgvector HNSW index, top 5 chunks
- Embedding model: OpenAI text-embedding-3-small (1536 dimensions)
- Generation model: gpt-4o, temperature 0.3, max tokens 1024
- Corpus: 21 papers on epistemic opacity in AI/ML (2023–2026)

---

## Failure 1: Chunking Boundary Splits an Argument

Character-based chunking at 512 characters splits philosophical arguments mid-sentence
and mid-word. Retrieval returns fragments that contain premises without conclusions or
conclusions without premises, and the LLM produces plausible-sounding but incomplete
answers that mask the information gap.

### Query 1A: "What is Duede's argument that deep learning is epistemically opaque?"

#### Generated Answer

Eamon Duede argues that deep learning models are epistemically opaque because it is not possible to evaluate all of the epistemically relevant factors that lead to the outputs of these models. This opacity presents significant challenges, particularly in high-stakes settings, because the factors governing the model's behavior are fundamentally unsurveyable and unintelligible. As a result, doing good science with such opaque models is exceptionally challenging, if not impossible, due to the difficulty in justifying belief or trust in their outputs ("Deep Learning Opacity in Scientific Discovery").

#### Full Prompt

```text
[SYSTEM]
You are a research assistant for philosophy of science.Answers the user's questions based only on the
provided context.Cite your sources by referencing the paper titles and the author.If the context does not
contain enough information to answer the user's question, then say so. Don't hallucinate.

[USER]

CONTEXT:

[Source: Apriori Knowledge in an Era of Computational Opacity: The Role of AI in Mathematical Discovery]
ed DNNs are said to be epistemically opaque [Hum04, Bog22], meaning
that all of the epistemically relevant factors governing the model's behavior are fundamentally
unsurveyable. In general, it is not possible to determine or 'fathom' [Zer22] in any intelligible
or meaningful sense the algorithmic rules or principles governing the transformation of inputs
to outputs of the model. As such, DNNs are opaque at the algorithmic level and, thus, at
the structural level, as well. This lack of transparency is due, i

***

[Source: Deep Learning Opacity in Scientific Discovery]
Deep Learning Opacity in Scientific Discovery
Eamon Duede
Department of Philosophy
Committee on Conceptual & Historical Studies of Science
Pritzker School of Molecular Engineering
Knowledge Lab
University of Chicago
eduede@uchicago.edu
August 23, 2022
Abstract
Philosophers have recently focused on critical, epistemological challenges that arise
from the opacity of deep neural networks. One might conclude from this literature
that doing good science with opaque models is exceptionally challenging, if not
imp

---

[Source: Deep Learning Opacity in Scientific Discovery]
se falling under Creel's algorithmic and structural levels and Zerilli's intelligibility and
fathomability criteria. As such, DLMs are "epistemically opaque".
3
Discovery and Justification with Deep Learning
When it comes to justifying belief or trust in the outputs of deep learning models, their
epistemic opacity is straightforwardly problematic.
This is due to the fact that it is
not possible to evaluate all of the epistemically relevant factors that led to the output.
In high-stakes settings such as medi

---

[Source: Deep Learning Opacity in Scientific Discovery]
y of science [Cre20, Zer22], I explain the relevant sense in which
deep learning models are opaque. In Section 3, I sketch the epistemologically relevant
distinction between treating neural network outputs as standing in need of justification
(e.g., positioning outputs in the context of justification) and treating such outputs as part
of a wider process of conceiving new knowledge (e.g., positioning outputs in the context
of discovery). In Section 4, I present two cases which demonstrate the way in which
re

---

[Source: Of Opaque Oracles: Epistemic Dependence on AI in Science Poses No Novel Problems for Social
Epistemology]
atter (e.g. ethnicity). If a DNN is epistemically opaque,
however, it is hard to know which aspects of the data are, in fact, being used for
predictions. While it is sometimes possible to empirically test for aspects that might
have been picked up on during training, the fact that the DNN is essentially opaque
inhibits an exhaustive understanding of what is going on. As a result, it emerges what
one might call a trust vacuum– neither can the DNN itself assume responsibility for
these unknowable decisi

QUESTION: What is Duede's argument that deep learning is epistemically opaque?

```

#### What went wrong:

1. Mid-word truncation is pervasive. All five chunks are cut mid-sentence: "due, i",
   "if not imp", "such as medi", "in which re", "decisi". The 512-character window
   has no awareness of sentence, word, or semantic boundaries.
2. The argument's key distinction is severed. Duede's core contribution is distinguishing
   the _context of justification_ (where opacity is problematic) from the _context of discovery_
   (where it may not be). Chunk 4 begins to reference this distinction but is cut at
   "the way in which re" — right before the payoff.
3. The answer captures only half the argument. The LLM reports the "opacity is
   problematic" side but entirely misses the discovery-side nuance, because no retrieved
   chunk contains the complete argument.
4. The highest-scoring chunk (0.746) is from a different paper — Duede & Davey (2024),
   not Duede (2023). The system retrieved a secondhand summary over the primary source.

---

### Query 1B: "How does Koskinen argue that we lack a social epistemology of AI-based science?"

#### Generated Answer

Koskinen argues that we lack a satisfactory social epistemology of AI-based science because current AI-based science cannot meet the conditions formulated by philosophers involved in this discussion. She highlights that the relationships of trust, which are necessary in contemporary collaborative science characterized by opaque epistemic dependence, are not adequately addressed in the context of AI-based science. This suggests that existing frameworks for understanding social epistemology in science are insufficient when applied to AI-based scientific practices (Koskinen, "We Have No Satisfactory Social Epistemology of AI-Based Science").

#### Full Prompt

```
[SYSTEM]
You are a research assistant for philosophy of
science.Answers the user's questions based only on the
provided context.Cite your sources by referencing the
paper titles and the author.If the context does not
contain enough information to answer the user's question,
then say so. Don't hallucinate.

[USER]

CONTEXT:

[Source: Of Opaque Oracles: Epistemic Dependence on AI in
Science Poses No Novel Problems for Social Epistemology]
roscience. In J. Duran & G. Pozzi (Eds.), Philosophy of
science for machine learning: Core issues and new
perspectives. Synthese Library.
Koskinen, I. (2023). We have no satisfactory social
epistemology of AI-based science. Social Epistemol
ogy. https://doi.org/10.1080/02691728.2023.2286253
Koskinen, I. (2024). We still have no satisfactory social
epistemology of AI-based science: A response to
peters. Social Epistemology Review and Reply Collective,
13(5), 9–

***

[Source: Science Based on Artificial Intelligence Need Not
  Pose a Social Epistemological Problem]
rrently our best social epistemology of science and this
view can't account for
AI-based science, "we currently have no satisfactory
social epistemology of AI-based
science", Koskinen concludes (15).

There's much to agree with in her paper. But I'm less
pessimistic and think that there are
some problematic internalist assumptions underlying
Koskinen's argument. If we remove
these assumptions then the version of the NT view that is
left needn't have a problem
accounting for AI-based science.

***

[Source: We Still Have No Satisfactory Social Epistemology
  of AI-Based Science: A Response to Peters]
45–666.
Koskinen, Inkeri. 2023. "We Have No Satisfactory Social
Epistemology of AI-Based
Science." Social Epistemology 1–18. doi:
10.1080/02691728.2023.2286253.
Longino, Helen E. 1990. Science as Social Knowledge:
Values and Objectivity in Scientific Inquiry.
Princeton: Princeton University Press.




I. Koskinen

14
Peters, Uwe. 2024. "Science Based on Artificial
Intelligence Need not Pose a Social
Epistemological Problem." Social Epistemology Review and
Reply Collective 13 (1): 58–
66. htt

***

[Source: We Still Have No Satisfactory Social Epistemology
  of AI-Based Science: A Response to Peters]
  The goal, then, is not to dictate how scientific research
  should be conducted, but to
argue for the acceptability of collective scientific
knowledge production, as long as it is
responsibly organised.

When I say that we do not have a satisfactory social
epistemology of AI-based science, I
claim that current AI-based science cannot meet the
conditions that philosophers taking part
in this discussion have formulated. When the AI
applications used in science are




I. Koskinen

10
epistemica

***

[Source: We Have No Satisfactory Social Epistemology of
AI-Based Science]
1
Forthcoming in Social Epistemology
Final submitted version, November 2023


We have no satisfactory social epistemology of AI-based
science
Inkeri Koskinen
University of Helsinki
inkeri.koskinen@helsinki.fi


Abstract: In the social epistemology of scientific
knowledge, it is largely accepted that
relationships of trust, not just reliance, are necessary
in contemporary collaborative science
characterised by relationships of opaque epistemic
dependence. Such relationships of trust
are taken t

QUESTION: How does Koskinen argue that we lack a social
epistemology of AI-based science?
```

#### What went wrong:

1. Two of five retrieval slots are wasted on bibliography
   entries. Chunks 1 and 3
   contain DOIs, page numbers, and publisher info — zero
   argumentative content. Only 3 of
   5 chunks carry substance.
2. The core argument is cut at the critical moment. Chunk
   4 reaches Koskinen's own
   statement — "current AI-based science cannot meet the
   conditions" — then cuts to
   "epistemica" (mid-word) right where she is about to state
   what those conditions are.
3. The abstract is truncated before the argument begins.
   Chunk 5 sets up "relationships
   of trust" and "opaque epistemic dependence" but cuts at
   "are taken t" — we never see
   what they are taken to require.
4. The answer is vague as a result. It says "cannot meet
   the conditions" without saying
   what those conditions are, because no chunk contains them
   in full.
5. The best chunk for this query (Koskinen's own paper)
   scored lowest (0.749), while
   a bibliography entry from a different paper scored highest
   (0.807). The embedding model
   matches on keyword density rather than argumentative
   content.

---

### Failure 1 Summary

- 512-character chunking reliably splits philosophical
  arguments mid-word and mid-sentence.
- Arguments are consistently cut right before the payoff —
  premises without conclusions.
- Bibliography and reference-list chunks pollute retrieval
  slots.
- The LLM produces plausible-sounding but incomplete
  answers, masking the information gap.
- Embedding similarity favours keyword-dense fragments
  (titles, abstracts, bibliographies)
  over substantive argument passages.

---

## Failure 2: Contradictory Chunks Blended or Ignored

The corpus contains a multi-paper debate between Koskinen
and Peters with directly opposing
claims. Cosine similarity retrieves chunks by relevance to
the query, not by coherence with
each other. When both sides appear, the LLM may blend
them; when only one side appears,
the LLM presents a contested claim as settled.

### Query 2A: "Does AI-based science pose a social epistemological problem?"

#### Generated Answer

The question of whether AI-based science poses a social epistemological problem is debated. One perspective, as discussed in "We Still Have No Satisfactory Social Epistemology of AI-Based Science: A Response to Peters," suggests that there is indeed a problem. [...]

On the other hand, Uwe Peters, in "Science Based on Artificial Intelligence Need Not Pose a Social Epistemological Problem," argues that AI-based science does not necessarily pose such a problem. [...]

Overall, the context indicates that there is no consensus, and the question remains open for further exploration and debate within the field.

#### Full Prompt

```
[SYSTEM]
You are a research assistant for philosophy of science.Answers the user's
  questions based only on the provided context.Cite your sources by
referencing the paper titles and the author.If the context does not
contain enough information to answer the user's question, then say so.
Don't hallucinate.

[USER]

CONTEXT:

[Source: We Still Have No Satisfactory Social Epistemology of AI-Based
Science: A Response to Peters]
estion of course arises whether this is a problem for AI-based science or
for the social epistemology of science. I, however, take it to be obvious
  that the problem
should at least initially be treated as one for social epistemology: we
should suspect that the
necessary trust view is in some way flawed or incomplete. As long as
questions about AI-
based science have not been thoroughly addressed in the social
epistemology of science, we
have no grounds for claiming that the problem lies within AI-based

***

[Source: We Still Have No Satisfactory Social Epistemology of AI-Based
Science: A Response to Peters]
AI applications are used in science are
unproblematic from the perspective of the necessary trust view. However,
if the scientific
community also accepts uses that are incompatible with the necessary
trust view, then the
social epistemology of science has a problem. And in my view, the
scientific community
nowadays does accept such uses of AI applications in knowledge
production.

If I am right, the question of course arises whether this is a problem
for AI-based science or
for the social epistemolo

***

[Source: We Have No Satisfactory Social Epistemology of AI-Based Science]
e that the use of epistemically opaque AI applications in science creates
  for the social
epistemology of scientific knowledge, a problem I believe has not yet
been discussed in the
field. I argue that we currently have no satisfactory way to reconcile
the practices of AI-based
science with the idea – supported by many in the field – that
relationships of trust, not of
mere reliance, are unavoidable and indispensable in contemporary science,
  where knowledge
is largely produced collectively and scientist

***

[Source: Science Based on Artificial Intelligence Need Not Pose a Social
Epistemological Problem]
http://social-epistemology.com
ISSN: 2471-9560


Science Based on Artificial Intelligence Need not Pose a Social
Epistemological Problem

Uwe Peters, Utrecht University, u.peters@uu.nl

––––––––––––––––––

Peters, Uwe. 2024. "Science Based on Artificial Intelligence Need not
Pose a Social
Epistemological Problem." Social Epistemology Review and Reply Collective
  13 (1): 58–66.
https://wp.me/p1Bfg0-8vp.




58
13 (1): 58–66. 2024.
https://wp.me/p1Bfg0-8vp
Abstract

It has been argued

***

[Source: We Have No Satisfactory Social Epistemology of AI-Based Science]
cience. Without much further work this does not seem a firm basis for a
social
epistemology of AI-based science. And finally, it is not clear that in
all cases where scientists
use epistemically opaque AI applications we can really observe the kind
of "fluid
incorporation of those tools and technologies deep into our cognitive
repertoires" that Clark
(2015, 3774) highlights when arguing for extended knowledge and extended
agency, as the
"trust and glue" conditions are not met.
The other option is to a

QUESTION: Does AI-based science pose a social epistemological problem?

```

#### What went wrong:

1. Asymmetric representation. Retrieval returned 4 Koskinen chunks to 1
   Peters chunk.
   The LLM acknowledged both sides but could only present Koskinen's
   reasoning in detail.
2. Peters' chunk is metadata, not argument. The one Peters chunk (0.739)
   is a title page
   with header, ISSN, and citation info. His actual counterargument is
   absent from the context.
3. The LLM hedged Peters' position. It says Peters argues AI "does not
   necessarily
   pose such a problem" — a weaker claim than Peters actually makes. The
   hedge was
   invented because the context contained no substance from Peters to work
   with.
4. A reader would conclude Koskinen's case is stronger — not because it
   is, but because
   retrieval happened to favour it. The asymmetry is invisible to the user.

---

### Query 2B: "Can we have a satisfactory social epistemology of AI-based science?"

#### Generated Answer

Based on the provided context, it appears that we currently do not have a satisfactory social epistemology of AI-based science. The use of epistemically opaque AI applications in science poses challenges that have not yet been adequately addressed within the field of social epistemology. The necessary trust view, which is widely accepted in the social epistemology of science, seems incompatible with current AI-based science practices. [...]

#### Full Prompt

```
[SYSTEM]
You are a research assistant for philosophy of science.Answers the user's questions based only on the provided context.Cite your sources by
referencing the paper titles and the author.If the context does not
contain enough information to answer the user's question, then say so.
Don't hallucinate.

[USER]

CONTEXT:

[Source: We Have No Satisfactory Social Epistemology of AI-Based Science]
  in science. This leaves us without a satisfactory social epistemology of
  AI-based
science.

2. The necessary trust view
It is largely accepted in the social epistemology of scientific knowledge
  that trust plays an
indispensable role in scientific knowledge production today. Given the
collaborative nature
of science, scientists cannot help but trust other scientists. This view
takes several slightly
different forms, as different philosophers focus on different aspects of
the relationships of
trust

***

[Source: We Still Have No Satisfactory Social Epistemology of AI-Based
Science: A Response to Peters]
nformed epistemic
responsibility.

At the End of the Day

I still agree with my original argument: we do not have a satisfactory
social epistemology of
AI-based science. I find it obvious and exciting that the use of
epistemically opaque AI
applications in science will only increase, as they can be extremely
useful. I assume that the
incompatibility I have articulated between current AI-based science and
the necessary trust
view that is widely accepted in the social epistemology of science gives
re

***

[Source: We Have No Satisfactory Social Epistemology of AI-Based Science]
cience. Without much further work this does not seem a firm basis for a
social
epistemology of AI-based science. And finally, it is not clear that in
all cases where scientists
use epistemically opaque AI applications we can really observe the kind
of "fluid
incorporation of those tools and technologies deep into our cognitive
repertoires" that Clark
(2015, 3774) highlights when arguing for extended knowledge and extended
agency, as the
"trust and glue" conditions are not met.
The other option is to a

***

[Source: We Have No Satisfactory Social Epistemology of AI-Based Science]
e that the use of epistemically opaque AI applications in science creates
  for the social
epistemology of scientific knowledge, a problem I believe has not yet
been discussed in the
field. I argue that we currently have no satisfactory way to reconcile
the practices of AI-based
science with the idea – supported by many in the field – that
relationships of trust, not of
mere reliance, are unavoidable and indispensable in contemporary science,
  where knowledge
is largely produced collectively and scientist

***

[Source: We Still Have No Satisfactory Social Epistemology of AI-Based
Science: A Response to Peters]
estion of course arises whether this is a problem for AI-based science or
for the social epistemology of science. I, however, take it to be obvious
  that the problem
should at least initially be treated as one for social epistemology: we
should suspect that the
necessary trust view is in some way flawed or incomplete. As long as
questions about AI-
based science have not been thoroughly addressed in the social
epistemology of science, we
have no grounds for claiming that the problem lies within AI-based

QUESTION: Can we have a satisfactory social epistemology of AI-based
science?
```

#### What went wrong:

1. The contradiction was erased entirely. All 5 retrieved chunks are from Koskinen — 3 from her 2024a paper and 2 from her 2024b response. Zero chunks from Peters, Ortmann, or anyone who disagrees.
2. Peters argues directly that we can. His paper is literally titled
   "Science Based on Artificial Intelligence Need Not Pose a Social Epistemological Problem." But it didn't make the top 5. Neither did Ortmann (2025), who uses AlphaFold as a counterexample.
3. The LLM presented one side of a debate as settled fact. "We currently
   do not have a satisfactory social epistemology" appears as the answer, with no hedge, no mention that this is contested. A user would have no idea there's a debate.
4. This is the worst outcome for a research assistant. A philosophy
   student relying on this answer would walk away with a distorted picture of the literature.
5. Root cause: Koskinen's keyword density for this exact phrasing is
   higher — it's her title, repeated in her abstract, introduction, and conclusion. Peters and Ortmann use different framings to make their counterarguments. Cosine similarity matched Koskinen's vocabulary, not the conceptual opposition.

### Failure 2 Summary

- Query 2A: contradiction was asymmetrically represented (4:1 Koskinen).
  The LLM acknowledged both sides but could only substantiate one.
- Query 2B: contradiction was erased entirely. All 5 chunks from one
  side. The LLM presented a contested claim as settled.
- Root cause: cosine similarity matches vocabulary, not conceptual
  relationships. An author who opposes a claim using different vocabulary won't be retrieved alongside the claim.

---

## Failure 3: Temporal Ordering — Outdated Claims Without Supersession Signals

The corpus contains a chronological debate chain: Koskinen (2024a) →
Peters (2024a) → Koskinen (2024b) → Peters (2024b) → Ortmann (2025). The system stores no publication date metadata in chunks and has no mechanism to prioritize newer sources or signal which claims have been superseded.

### Query 3A: "What is Koskinen's current position on social epistemology of AI?"

#### Generated Answer

Koskinen's current position is that we do not have a satisfactory social epistemology of AI-based science. She argues that the existing frameworks for social epistemology, which emphasize relationships of trust in collaborative science, are inadequate when applied to AI-based science due to the opaque nature of AI systems. [...] ("We Have No Satisfactory Social Epistemology of AI-Based Science," Koskinen, 2024a).

#### Full Prompt

```
[SYSTEM]
You are a research assistant for philosophy of science.Answers the user's questions based only on the provided context.Cite your sources by
referencing the paper titles and the author.If the context does not
contain enough information to answer the user's question, then say so.
Don't hallucinate.

[USER]

CONTEXT:

[Source: We Still Have No Satisfactory Social Epistemology of AI-Based
Science: A Response to Peters]
45–666.
Koskinen, Inkeri. 2023. "We Have No Satisfactory Social Epistemology of
AI-Based
Science." Social Epistemology 1–18. doi: 10.1080/02691728.2023.2286253.
Longino, Helen E. 1990. Science as Social Knowledge: Values and
Objectivity in Scientific Inquiry.
Princeton: Princeton University Press.




I. Koskinen

14
Peters, Uwe. 2024. "Science Based on Artificial Intelligence Need not
Pose a Social
Epistemological Problem." Social Epistemology Review and Reply Collective
  13 (1): 58–
66. htt

***

[Source: Science Based on Artificial Intelligence Need Not Pose a Social
Epistemological Problem]
rrently our best social epistemology of science and this view can't
account for
AI-based science, "we currently have no satisfactory social epistemology
of AI-based
science", Koskinen concludes (15).

There's much to agree with in her paper. But I'm less pessimistic and
think that there are
some problematic internalist assumptions underlying Koskinen's argument.
If we remove
these assumptions then the version of the NT view that is left needn't
have a problem
accounting for AI-based science.

***

[Source: Of Opaque Oracles: Epistemic Dependence on AI in Science Poses
No Novel Problems for Social Epistemology]
roscience. In J. Duran & G. Pozzi (Eds.), Philosophy of
science for machine learning: Core issues and new perspectives. Synthese
Library.
Koskinen, I. (2023). We have no satisfactory social epistemology of
AI-based science. Social Epistemol
ogy. https://doi.org/10.1080/02691728.2023.2286253
Koskinen, I. (2024). We still have no satisfactory social epistemology of
  AI-based science: A response to
peters. Social Epistemology Review and Reply Collective, 13(5), 9–

***

[Source: We Have No Satisfactory Social Epistemology of AI-Based Science]
1
Forthcoming in Social Epistemology
Final submitted version, November 2023


We have no satisfactory social epistemology of AI-based science
Inkeri Koskinen
University of Helsinki
inkeri.koskinen@helsinki.fi


Abstract: In the social epistemology of scientific knowledge, it is
largely accepted that
relationships of trust, not just reliance, are necessary in contemporary
collaborative science
characterised by relationships of opaque epistemic dependence. Such
relationships of trust
are taken t

***

[Source: Living with Uncertainty: Full Transparency of AI isn't Needed
for Epistemic Trust in AI-based Science]
disagree with Koskinen that when AI systems are epistemically opaque,
human agents cannot take
appropriate responsibility (to be epistemically trusted) for the
processing of these systems. In a recent
commentary (Peters, 2024), I offered several arguments against Koskinen's
  view. She has now replied. I
think her replies don't succeed against my initial points.

2. Overlooking similarities between human and AI opacity

In her reply, Koskinen insists that her favored

argument for the necessary trus

QUESTION: What is Koskinen's current position on social epistemology of
AI?
```

#### What went wrong:

1. The LLM cited Koskinen (2024a) as her "current position." But Koskinen
   published a second paper (2024b) — "We Still Have No Satisfactory Social
   Epistemology" — where she refined and defended her position against Peters' objections. The answer ignores the evolution entirely.
2. The retrieval contains the debate timeline but can't order it. The
   context includes fragments from across the debate chain — Koskinen (2024a), Peters (2024a), Koskinen (2024b) bibliography, Ortmann (2025) bibliography, and Peters (2024b). But there is no temporal signal connecting them.
3. The most temporally relevant chunk scored lowest (0.695). Peters
   (2024b) explicitly says "She has now replied. I think her replies don't succeed" — this is the latest exchange in the debate. But the LLM ignored it in favour of the older 2024a paper.
4. The answer a researcher would want: "Koskinen originally argued X
   (2024a). Peters objected (2024a). Koskinen maintained and refined her position in response (2024b), arguing that we still have no satisfactory social epistemology because..." — a narrative that requires temporal ordering the system cannot provide.

---

### Query 3B: "Has Peters responded to Koskinen's critique? Who else has responded to Koskinen's critique over the last year? Does anyone use the example of AlphaFold to argue against her critique?"

#### Generated Answer

Yes, Peters has responded to Koskinen's critique. In the source titled "Living with Uncertainty: Full Transparency of AI isn't Needed for Epistemic Trust in AI-based Science," Peters mentions that he offered several arguments against Koskinen's view and that she has replied to them, but he believes her replies do not succeed against his initial points.

Additionally, the example of AlphaFold is used to argue against Koskinen's critique. In the source "Of Opaque Oracles," it is argued that AlphaFold serves as a direct counterexample to Koskinen's argument, despite meeting her criteria of essential opacity and epistemic dependence.

There is no information provided about other individuals who have responded to Koskinen's critique over the last year.

#### Full Prompt

```
[SYSTEM]
You are a research assistant for philosophy of science.Answers the user's questions based only on the provided context.Cite your sources by
referencing the paper titles and the author.If the context does not
contain enough information to answer the user's question, then say so.
Don't hallucinate.

[USER]

CONTEXT:

[Source: Of Opaque Oracles: Epistemic Dependence on AI in Science Poses
No Novel Problems for Social Epistemology]
cal
response to Koskinen's argument. Section 2 presents and refines
Koskinen's argu
ment, but ultimately finds that her account leaves open certain questions
  that are best
addressed by close examination of scientific practice. Thus, in Sect. 3,
I introduce the
case of AlphaFold2, a breakthrough AI application in structural biology.
Given its use
of opaque DNNS and its widespread use by scientists today, I take it to
fit the crite
ria that gave rise to Koskinen's concerns. However, I will find that the

***

[Source: Living with Uncertainty: Full Transparency of AI isn't Needed
for Epistemic Trust in AI-based Science]
disagree with Koskinen that when AI systems are epistemically opaque,
human agents cannot take
appropriate responsibility (to be epistemically trusted) for the
processing of these systems. In a recent
commentary (Peters, 2024), I offered several arguments against Koskinen's
  view. She has now replied. I
think her replies don't succeed against my initial points.

2. Overlooking similarities between human and AI opacity

In her reply, Koskinen insists that her favored

argument for the necessary trus

***

[Source: Of Opaque Oracles: Epistemic Dependence on AI in Science Poses
No Novel Problems for Social Epistemology]
r's, analysis of crop resilience, and many more.
This success story arguably makes AlphaFold a paradigm case of AI use in
sci
ence. Therefore, one might expect that it is also a paradigm case in
support of Koski
nen's argument. Contrary to such expectations, however, I will argue in
the following
that AlphaFold serves as a direct counterexample to Koskinen's argument.
While
AlphaFold does meet Koskinen's criteria of essential opacity and
epistemic depen
dence, as I will defend later, it nonetheless doe

***

[Source: We Still Have No Satisfactory Social Epistemology of AI-Based
Science: A Response to Peters]
http://social-epistemology.com
ISSN: 2471-9560


We Still Have No Satisfactory Social Epistemology of AI-Based Science: A
Response to
Peters

Inkeri Koskinen, University of Helsinki, inkeri.koskinen@tuni.fi

––––––––––––––––––

Koskinen, Inkeri. 2024. "We Still Have No Satisfactory Social
Epistemology of AI-Based
Science: A Response to Peters." Social Epistemology Review and Reply
Collective 13 (5): 9–14.
https://wp.me/p1Bfg0-8LL.

***

[Source: Of Opaque Oracles: Epistemic Dependence on AI in Science Poses
No Novel Problems for Social Epistemology]
  AI-based science: A response to
peters. Social Epistemology Review and Reply Collective, 13(5), 9–14.
Laurents, D. V. (2022). AlphaFold 2 and NMR spectroscopy: Partners to
understand protein structure,
dynamics and function. Frontiers in Molecular Biosciences, 9, 906437.
https://doi.org/10.3389/fmo
lb.2022.906437
Miller, B., & Freiman, O. (2020). Trust and distributed epistemic labor.
In J. Simon (Ed.), The routledge hand
book of trust and philosophy (pp. 341–35

QUESTION: Has Peters responded to Koskinen's critique? Who else has
responded to Koskinen's critique over the last year? Does anyone use the
example of AlphaFold to argue against her critique?
```

#### What went wrong:

1. The system cannot reconstruct the debate timeline. The actual
   chronology is: Koskinen (2024a) → Peters (2024a) → Koskinen (2024b) → Peters (2024b) → Ortmann (2025).
   Fragments from all of these appear in the context, but there is no signal about ordering.
2. "Over the last year" is unanswerable. The query requires knowing
   publication dates. The system has no date metadata in the retrieval context. Dates are buried in citation strings but not structured for temporal reasoning. The LLM punts: "There is no information provided about other individuals."
3. Ortmann is invisible as a respondent. Three of five chunks are from
   Ortmann's paper. The LLM correctly identifies the AlphaFold argument but never identifies Ortmann as someone who responded to Koskinen — because the chunks don't explicitly say "Ortmann responds to Koskinen." Inferring that a paper engaging with someone's argument is a response requires citation-graph reasoning the system cannot perform.
4. Peters responded twice but only one response is reported. Peters
   (2024a) and Peters (2024b) are separate papers. The LLM only reports one. Koskinen's counter-response (2024b) is also missing from the narrative.

### Failure 3 Summary

- The system has no concept of "current" or "latest." Queries asking for
  temporal information get answers anchored to whichever paper's chunks happened to score highest.
- Publication dates exist only as incidental text in citation strings —
  not as structured metadata the system can reason about.
- The system cannot reconstruct a debate timeline even when all participants' chunks are retrieved, because there is no ordering signal.
- Multi-step exchanges (claim → response → counter-response) are
  flattened into an unordered set of fragments.

  ***

## Conclusion

The three failure modes documented here are not independent — they  
compound each other. _Chunking boundaries_ (Failure 1) produce fragments that lack argumentative structure. _Cosine similarity retrieval_ (Failure 2) selects from those fragments based on vocabulary overlap, not conceptual relevance, which means opposing views framed in
different language are systematically excluded. And the _absence of temporal metadata_ (Failure 3) means that even when the system retrieves fragments from across a multi-year debate, it cannot  
distinguish an original claim from its refutation or a superseded  
position from its update.

The result is a system that is most dangerous when it appears most  
confident: it returns plausible, well-cited answers that a user has no reason to doubt, but that _silently omit half a debate, truncate the core of an argument, or present a superseded claim as current_.

For a research assistant aimed at philosophers — users who care precisely about the structure of arguments, the evolution of positions, and the relationship between competing views — these are not edge cases. They are the central use case, failing.

---
