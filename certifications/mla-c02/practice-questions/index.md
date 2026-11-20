# MLA-C02 Practice Questions — Index

50 practice questions for **AWS Certified Machine Learning Engineer – Associate (MLA-C02)**,
weighted to match the official domain percentages so the question mix mirrors actual exam
emphasis. See the [certification README](../README.md) for exam overview, domain weights, and
study order.

## This isn't the only practice material — here's the full picture

This folder (50 domain-split questions) is for studying ONE domain at a time. Two more
resources exist for different stages of prep: **[`full-exams/`](full-exams/index.md)** — 2
full-length, **timed, blind** 65-question mock exams (separate question/answer-key files)
matching the real exam's exact item count and weighting — and **[`../exam-bank/`](../exam-bank/README.md)**
— 3 more 65-question **study-mode** banks (bank-1/2/3) with the answer and explanation
inline under each question. Use domain-split questions while learning a domain, exam-bank
for full-scope drilling after all domains are done, full-exams last under real time pressure.

## Question counts by domain

| File | Domain | Weight | Questions | Multi-select ("Choose TWO") |
|---|---|---|---|---|
| [`domain-1-questions.md`](domain-1-questions.md) | 1 — Data Preparation for ML and AI | 28% | 14 | 2 (Q4, Q9, Q14 touch 3 but Q14 counted once — see note below) |
| [`domain-2-questions.md`](domain-2-questions.md) | 2 — ML Model and Foundation Model Development | 24% | 12 | 2 (Q6, Q11) |
| [`domain-3-questions.md`](domain-3-questions.md) | 3 — Deployment and Orchestration of ML and AI Workflows | 24% | 12 | 2 (Q5, Q8) |
| [`domain-4-questions.md`](domain-4-questions.md) | 4 — Operating, Monitoring, and Securing ML and AI Solutions | 24% | 12 | 2 (Q10, Q12) |
| **Total** | | **100%** | **50** | **8 (16%)** |

Note on Domain 1: three questions use "(Choose TWO)" format — Q4, Q9, and Q14 — for 3 of 14
(21%); the bank-wide average across all 50 questions is 8/50 = 16%, in line with the ~15% target
for multi-select questions across the full set.

## Content coverage checks

- **Embeddings / RAG / Bedrock GenAI** — 8 questions reference this content (target: at least 4):
  Domain 1 Q6, Q7, Q8, Q14 (RAG decision, chunking, embedding-model consistency, vector store
  options); Domain 2 Q8 (fine-tuning vs. RAG); Domain 3 Q11, Q12 (Bedrock Knowledge Bases,
  Bedrock Agents); Domain 4 Q9 (Bedrock Guardrails). All link to
  [`embeddings-and-rag-data-prep.md`](../domain-1-data-preparation/embeddings-and-rag-data-prep.md)
  and/or [`services/machine-learning-ai/bedrock.md`](../../../services/machine-learning-ai/bedrock.md)
  where relevant.
- **Core ML fundamentals** (bias-variance, evaluation metrics, hyperparameter tuning) — 8
  questions in Domain 2 alone (target: at least 3): Q1, Q2 (overfitting/underfitting), Q3
  (bias-variance tradeoff), Q4, Q5 (precision/recall/accuracy traps), Q6 (hyperparameter search
  strategy), Q11 (regularization techniques), Q12 (AUC). All link to the
  [ML Fundamentals Glossary](../domain-2-model-development/ml-fundamentals-glossary.md).
- **Responsible AI / Guardrails** — Domain 4 Q9, Q10, Q11 directly cover
  [`responsible-ai-and-guardrails.md`](../domain-4-monitoring-security/responsible-ai-and-guardrails.md)
  (Guardrails vs. Clarify, pre- vs. post-training bias, explainability/SHAP).
- **Cost optimization** — Domain 4 Q3, Q4, Q5, Q12 cover
  [`ml-cost-optimization.md`](../domain-4-monitoring-security/ml-cost-optimization.md) (Spot,
  Savings Plans, Inference Recommender).

## Question format

Every question follows the same structure:
1. A realistic ML-engineer-focused AWS scenario (not a trivia/definition lookup).
2. Four answer options (A–D), or five options for "(Choose TWO)" multi-select questions.
3. The correct answer(s), stated explicitly.
4. A full explanation citing the specific SageMaker/Bedrock feature or ML concept involved, with
   a relative markdown link to the relevant domain doc or `services/` deep-dive doc.
5. A "Why the others are wrong" breakdown for every distractor — including common ML
   misconceptions (confusing precision/recall, overfitting/underfitting, data drift/concept
   drift, bias metrics vs. explainability, Clarify vs. Guardrails) where relevant, not just
   "this service doesn't do that."

## How to use this bank

- **Timed, closed-book pass first.** MLA-C02 is multiple choice/multiple response only (no
  ordering/matching/case studies) — treat each question as a real exam item: read the full
  scenario, pick an answer, don't peek at the explanation first.
- **Review every wrong-option rationale, even on questions you got right.** The "why X is wrong"
  text often contains the actual exam trap (e.g., why accuracy is misleading on imbalanced data,
  why RAG isn't the answer to every GenAI customization question) — these traps repeat across
  questions in different disguises.
- **Follow the links back to source docs** when an explanation doesn't fully click — each
  question links to the domain README or a specific `services/` doc with the full depth
  (diagrams, "How It Works" walkthroughs, pricing, exam tips) behind the one-paragraph
  explanation given here.
- **Weight your review time to match domain weights.** Spend proportionally more time on Domain
  1 (28%, the largest file) and treat Domains 2–4 as roughly equal (24% each) — don't let any one
  domain's question count make it feel more or less important than its actual exam weight.
- **Re-take missed questions after a few days**, not immediately — spaced repetition on the
  specific scenarios you got wrong is more effective than immediately re-reading the same
  explanation while it's still fresh.
- **Cross-reference with `labs.md`** in each domain folder once you've worked through its
  questions — the hands-on labs reinforce the same concepts (Feature Store, SageMaker Pipelines,
  RAG with local embeddings, Clarify/Guardrails stand-ins) with real, runnable practice instead
  of multiple-choice recall alone.

## Status

✅ Complete first pass — 50/50 questions written across all 4 domains, weighted to the official
MLA-C02 domain percentages (28/24/24/24). As the official C02 exam guide finalizes further ahead
of the January 2027 GA, revisit especially the GenAI-heavy questions (RAG, Guardrails, Agents) in
case task-statement wording shifts.
