# MLA-C02 Full Mock Exams — Index

This folder contains **full-length mock exams** for **AWS Certified Machine Learning Engineer –
Associate (MLA-C02)**. These are different from the domain-split question banks one level up in
[`../domain-1-questions.md`](../domain-1-questions.md) through
[`../domain-4-questions.md`](../domain-4-questions.md) (50 questions total, organized and studied
one domain at a time). The mock exams here instead **mix all four domains together in a single
65-question sitting**, the same way the real exam presents questions, so you can practice pacing,
domain-switching, and endurance — not just topic recall.

## What's here

| File | Contents |
|---|---|
| [`exam-1-questions.md`](exam-1-questions.md) | Mock Exam 1 — 65 questions, Q1–Q65, options A–E, no answers shown |
| [`exam-1-answer-key.md`](exam-1-answer-key.md) | Mock Exam 1 — correct letter(s), full explanation, and a "why the others are wrong" breakdown for every question |
| [`exam-2-questions.md`](exam-2-questions.md) | Mock Exam 2 — 65 **different** questions, same format |
| [`exam-2-answer-key.md`](exam-2-answer-key.md) | Mock Exam 2 — answer key, same format |

## Why 65 questions

The real MLA-C02 exam (like SAA-C03 and DVA-C03 before it) presents **65 total questions**,
of which **15 are unscored** (used by AWS to evaluate future exam content) and the rest count
toward your score — you are **never told which 15 are unscored**, so every question must be
treated as if it counts. Each mock exam here is built to the same 65-question shape for realistic
timing and endurance practice.

## Format — matches the real exam exactly

- **Question types:** multiple choice (pick one) and multiple response (explicitly labeled
  **"(Choose TWO)"** in the question text) — **only**. MLA-C02 has no ordering, matching, or
  case-study-style items, so neither do these mocks.
- **Options:** 4 options (A–D) for single-answer questions, 5 options (A–E) for "Choose TWO"
  questions.
- **Domain mix:** each exam is weighted to the official MLA-C02 domain percentages:

  | Domain | Weight | Questions per exam |
  |---|---|---|
  | 1 — Data Preparation for ML and AI | 28% | 18 |
  | 2 — ML Model and Foundation Model Development | 24% | 16 |
  | 3 — Deployment and Orchestration of ML Workflows | 24% | 16 |
  | 4 — Operating, Monitoring, and Securing ML Solutions | 24% | 15 |
  | **Total** | **100%** | **65** |

  Questions are **interleaved across domains** throughout each exam (not grouped by domain), just
  like the real test — the answer key tells you which domain each question belongs to, but the
  question file deliberately does not, so you can't use question position to guess domain or
  anticipate what's coming next.
- **GenAI/Bedrock coverage:** both exams include real coverage of the content MLA-C02 added
  heaviest versus the old MLA-C01 — RAG architecture and chunking, embeddings and vector
  databases (OpenSearch Serverless, Aurora pgvector, Bedrock Knowledge Bases), Bedrock Agents and
  action groups, agent/session state management, Bedrock Guardrails (denied topics, PII
  redaction, contextual grounding), and GenAI evaluation metrics (BLEU, ROUGE, cosine similarity,
  hallucination/grounding).
- **ML fundamentals traps:** scenarios are written to test real engineering judgment, not
  trivia — including the classic exam traps of confusing precision vs. recall, overfitting vs.
  underfitting, data drift vs. concept drift, and accuracy's blind spot on imbalanced data.

## How to take these

1. **Time yourself.** The real exam gives 130 minutes for 65 questions (2 minutes/question).
   Set a timer for 130 minutes and sit the whole exam in one sitting, closed-book, before
   checking anything.
2. **Don't peek at the answer key until you're done.** Answer every question first — including
   ones you're unsure about — then grade the whole attempt at once. Looking at explanations
   mid-exam defeats the point of a timed mock.
3. **Mark and move on.** If a question stumps you, pick your best guess, flag it mentally (or on
   scratch paper), and keep moving — don't let one question eat your 2-minutes-per-question
   budget. There's no penalty for wrong answers, so never leave a question blank.
4. **Grade and compute your score out of 1000.** AWS reports MLA-C02 results on a scaled
   100–1000 score, not a raw percentage. Approximate it as:
   `score ≈ (correct ÷ 65) × 900 + 100`. The **passing bar is 720/1000**, which is **≈ 72%**
   (correct ÷ 65 ≈ 0.689 → roughly 45 of 65 correct, though AWS's actual scaling is not perfectly
   linear — use 72% as your practical target when self-grading).
5. **Review every explanation, even on questions you got right.** The "why the others are wrong"
   section usually contains the real exam trap in disguise (e.g., why RAG isn't the answer to
   every GenAI customization question, why a widening train/validation gap means overfitting and
   not underfitting) — these traps resurface in different scenarios on the real exam.
6. **Follow the links back to source docs** for anything that didn't fully click. Every
   explanation links to the relevant `services/` deep-dive doc or domain README with full depth
   (diagrams, "How It Works" walkthroughs, pricing, exam tips).
7. **Space out your retakes.** Don't re-take the same mock exam the next day — the specific
   question wording will still be fresh and you'll be testing memorization, not understanding.
   Wait several days, and prioritize working through
   [`../index.md`](../index.md)'s domain-split question banks and the domain READMEs/labs in
   between attempts to actually close knowledge gaps.
8. **Use both exams as a pair.** Take Exam 1 first as a baseline, study your weak areas using the
   domain-split banks and READMEs, then take Exam 2 later as a second, independent check — not as
   "practice for Exam 2," since reviewing Exam 1's answers in detail will otherwise make Exam 2's
   different-but-related questions too easy to be a fair re-test.

## Status

✅ Complete — both 65-question mock exams written, domain-weighted to 18/16/16/15 (28%/24%/24%/24%),
mixing multiple-choice and "Choose TWO" multiple-response questions, with real GenAI/Bedrock/RAG
coverage and full answer-key explanations for every question and every distractor.
