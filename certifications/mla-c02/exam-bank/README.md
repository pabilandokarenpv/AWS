# MLA-C02 Exam Bank — Study-Mode Practice Exams

Three **complete, 65-question practice exams** (`bank-1.md`, `bank-2.md`, `bank-3.md`) for
**AWS Certified Machine Learning Engineer – Associate (MLA-C02)**, built in **study mode**:
the correct answer and a full explanation (including why every wrong option is wrong) appear
**immediately after each question**, so you can check your reasoning question-by-question
instead of waiting until the end.

This is a different folder from the other two MLA-C02 practice resources in this repo. All
three are meant to be used together, in order:

| Folder | Mode | Question count | When to use it |
|---|---|---|---|
| [`../practice-questions/`](../practice-questions/) (domain-1 through domain-4) | Study mode, one domain at a time | 50 (≈ 12–14 per domain) | **First pass.** Learn and drill one domain's concepts in isolation before mixing domains. |
| **`exam-bank/` (this folder)** | **Study mode, full mixed exam** | **195** (65 × 3, interleaved across all 4 domains) | **Second pass.** Reinforce recall with realistic domain-mixing and volume, but still get instant feedback after each question so you can patch gaps as you go. |
| [`../practice-questions/full-exams/`](../practice-questions/full-exams/) (exam-1, exam-2) | **Timed, blind** — questions and answer keys are in separate files | 130 (65 × 2) | **Final pass.** Simulate real exam conditions: no peeking at explanations until you've committed to every answer, then score yourself and review the separate answer key. |

## Suggested usage order

1. **Domain drills first** — work through `practice-questions/domain-1-questions.md` →
   `domain-4-questions.md` in order. Read every explanation, even for questions you got right;
   the "why the others are wrong" sections are where the real misconception-busting happens.
2. **Exam bank next (this folder)** — do `bank-1.md`, then `bank-2.md`, then `bank-3.md`, each
   as one sitting if possible (aim for ~90 minutes per 65-question bank, matching real exam
   pacing), but don't be afraid to stop and dig into the linked domain docs or service docs
   whenever an explanation references a concept you're shaky on. Study mode here is meant for
   **active review**, not passive timed practice — that comes next.
3. **Timed full exams last** — once `bank-1`–`bank-3` feel comfortable, switch to
   [`../practice-questions/full-exams/`](../practice-questions/full-exams/): answer all 65
   questions in `exam-1-questions.md` *without* looking at `exam-1-answer-key.md`, time
   yourself (130 minutes is the real exam's limit), score yourself against the 720/1000 passing
   bar explained in that folder's `index.md`, then repeat with `exam-2`. This is your dress
   rehearsal — no explanations until you've locked in every answer.

## What's in each bank

- **65 questions per bank, 195 total**, all mutually distinct from each other and from every
  question in `practice-questions/` and `practice-questions/full-exams/` — no repeated
  scenarios, numbers, or "flavor text" reused across any of the five question files in this repo.
- **Domain mix matches the official MLA-C02 exam weighting** in every bank:

  | Domain | Weight | Questions per bank |
  |---|---|---|
  | 1 — Data Preparation for ML and AI | 28% | 18 |
  | 2 — ML Model and Foundation Model Development | 24% | 16 |
  | 3 — Deployment and Orchestration of ML Workflows | 24% | 16 |
  | 4 — Operating, Monitoring, and Securing ML Solutions | 24% | 15 |
  | **Total** | **100%** | **65** |

  Domains are **interleaved question-by-question** (each bank uses a different interleaving
  offset), not grouped into four blocks — this matches how the real exam randomizes domain
  order and forces you to context-switch between topics the way the real test does.
- **Question types:** multiple choice (one correct option, A–D) and multiple response
  (explicitly marked **"(Choose TWO)"**, options A–E) only — MLA-C02 has no ordering,
  matching, or case-study items, so neither do these banks.
- **Heavy, deliberate GenAI/Bedrock coverage** per the real (post-2024) MLA-C02 content:
  vector databases, embeddings, RAG architecture and chunking strategy, Bedrock Knowledge
  Bases, Bedrock Agents, Bedrock Guardrails, and NLP evaluation metrics (BLEU, ROUGE,
  BERTScore, perplexity) — alongside classic ML fundamentals traps (precision/recall,
  overfitting/underfitting, bias-variance, regularization).
- **Diagrams:** roughly 15–20 of the 65 questions per bank include a **Mermaid diagram**,
  walked through step by step in the explanation, for scenarios where a visual materially
  clarifies the concept (RAG pipelines, training workflows, deployment/traffic-shifting
  architectures, agent orchestration loops, monitoring architectures).
- **A few questions per bank cite a real AWS documentation image** (curl-verified to return
  HTTP 200 at the time of writing), captioned with its source doc page, for extra grounding
  in the official reference architecture diagrams AWS itself publishes for Bedrock Knowledge
  Bases, Bedrock Agents, and SageMaker Model Monitor.
- **Every explanation cross-links** to the relevant [`services/machine-learning-ai/`](../../../services/machine-learning-ai/),
  [`services/analytics/`](../../../services/analytics/), or [`certifications/mla-c02/domain-*/`](../)
  doc in this repo, so a wrong answer is never a dead end — you can always jump to the deeper
  reference material.

## Format — matches the real exam exactly

- 4 options (A–D) for single-answer questions, 5 options (A–E) for "(Choose TWO)" questions.
- Each question is immediately followed by `**Correct Answer:**`, a full `**Explanation:**` of
  why that answer is right (what concept/service it tests and why it fits), and a
  `**Why the others are wrong:**` section giving a specific misconception for *every* wrong
  option — never just "incorrect."

## Files

| File | Contents |
|---|---|
| [`bank-1.md`](bank-1.md) | Practice Exam Bank 1 — 65 questions, study mode |
| [`bank-2.md`](bank-2.md) | Practice Exam Bank 2 — 65 different questions, study mode |
| [`bank-3.md`](bank-3.md) | Practice Exam Bank 3 — 65 more different questions, study mode |
