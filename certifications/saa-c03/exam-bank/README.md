# SAA-C03 Exam Bank — Study-Mode Practice Exams

This folder contains **three full-length, study-mode practice exams** (195 questions total)
for the [AWS Certified Solutions Architect – Associate (SAA-C03)](../README.md) exam. It is a
**different study tool** from the other two question resources one level up in this repo —
use all three, but for different purposes, at different points in your prep.

## How this differs from the other two question resources

| | [`practice-questions/`](../practice-questions/index.md) (domain banks) | **`exam-bank/`** (this folder) | [`practice-questions/full-exams/`](../practice-questions/full-exams/index.md) |
|---|---|---|---|
| Format | Answer immediately follows each question | **Answer immediately follows each question** | Answer is in a **separate** answer-key file |
| Question order | Grouped by domain | **Mixed/interleaved**, like the real exam | Mixed/interleaved, like the real exam |
| Length per sitting | 12–18 questions (one domain) | **65 questions** (full exam) | 65 questions (full exam) |
| Timing | Untimed | **Untimed — study mode** | Timed (130 minutes) — simulates exam day |
| Purpose | Targeted practice while learning one domain | **Deep review/drilling with instant feedback** | Readiness check / dress rehearsal |
| Diagrams | Some | **15–20+ Mermaid diagrams per bank**, plus a few real AWS doc images | Text-only |

The key distinction from `full-exams/`: those two mock exams are **blind** — you answer all 65
questions before ever seeing the answer key, simulating real exam pressure and pacing. The
three banks in **this folder** show you the answer and full explanation **immediately after
each question**, so you can learn and correct course question-by-question. That makes this
folder better for *active drilling and review*, and `full-exams/` better for a *final,
realistic readiness check* right before you book the real test.

## What's in this folder

| Bank | Questions | Best used |
|---|---|---|
| [`bank-1.md`](bank-1.md) | 65 | After finishing Domain 1 and Domain 2 study |
| [`bank-2.md`](bank-2.md) | 65 | After finishing Domain 3 and Domain 4 study |
| [`bank-3.md`](bank-3.md) | 65 | As a final full review, right before `full-exams/` |

All **195 questions across the three banks are mutually distinct scenarios** — no company,
situation, or specific technical angle repeats between Bank 1, Bank 2, and Bank 3 — and all are
distinct from the scenarios in [`practice-questions/`](../practice-questions/index.md) and
[`practice-questions/full-exams/`](../practice-questions/full-exams/index.md). You can safely
work through all three banks (and the other two resources) without ever drilling the same
scenario twice.

Each bank matches the real exam's format exactly:

| Domain | Weight | Questions per bank |
|---|---|---|
| [Domain 1 — Secure Architectures](../domain-1-secure-architectures/README.md) | 30% | 20 |
| [Domain 2 — Resilient Architectures](../domain-2-resilient-architectures/README.md) | 26% | 17 |
| [Domain 3 — High-Performing Architectures](../domain-3-high-performing-architectures/README.md) | 24% | 15 |
| [Domain 4 — Cost-Optimized Architectures](../domain-4-cost-optimized-architectures/README.md) | 20% | 13 |
| **Total** | **100%** | **65 per bank, 195 total** |

Domains are **interleaved/mixed** within each bank (not grouped), matching the real exam's
question order. A handful of questions in every bank are labeled **"(Choose TWO)"**,
matching the real exam's mix of single-answer and multiple-response question formats.

## What every question includes

Immediately after each question's scenario and its 4–5 answer options, you'll find:

1. **The correct answer letter(s)** — bolded, impossible to miss.
2. **A full paragraph explaining *why* the correct answer is right** — not just naming the
   service, but walking through the specific reasoning that makes it the correct fit for
   *this* scenario's specific constraints.
3. **A full explanation for *every* wrong option** — not "incorrect," but the specific
   misconception, mismatched capability, or overlooked constraint each distractor represents.
   The real exam rewards knowing *why* a tempting-but-wrong answer is wrong, not just picking
   the right one — these explanations are where that nuance lives.
4. **A cross-link** to the relevant [`services/`](../../../services) doc or
   [domain doc](../README.md#domains--weights) in this repo, so a shaky answer is one click
   away from the deeper material.
5. **For architecture/scenario-based questions where a visual clarifies the explanation** (at
   least 15–20 questions per bank): a **Mermaid diagram** showing the recommended architecture,
   walked through step by step underneath it. A few questions also reference a real AWS
   documentation image (with a caption and source link) instead of or alongside a diagram.

## Suggested usage order

This folder's three banks are numbered for a reason — they're designed to be taken **in order,
at specific points in your study timeline**, not all at once or in isolation:

1. **Study [Domain 1](../domain-1-secure-architectures/README.md) and
   [Domain 2](../domain-2-resilient-architectures/README.md)** using their README, deep-dive
   docs, and labs.
2. **Take `bank-1.md`.** With both domains fresh, this 65-question bank gives you immediate
   feedback on what actually stuck — read every explanation, even for questions you got right,
   since the "why the others are wrong" sections often reveal gaps in nearby concepts.
3. **Study [Domain 3](../domain-3-high-performing-architectures/README.md) and
   [Domain 4](../domain-4-cost-optimized-architectures/README.md)**.
4. **Take `bank-2.md`.** Same approach — read every explanation, follow links for anything
   shaky, and note which domain(s) your misses cluster in.
5. **Review your weak spots** from Banks 1 and 2 — revisit the specific `services/` or domain
   docs linked from questions you missed, and re-skim the domain READMEs for task statements
   you're still unsure about.
6. **Take `bank-3.md`** as your final full review — a comprehensive, all-domains-mixed pass
   covering everything, immediately before moving to the timed simulation.
7. **Move to [`practice-questions/full-exams/`](../practice-questions/full-exams/index.md)**
   for the timed, blind mock-exam experience — book 130 minutes, no notes, no looking anything
   up, and treat it as a dress rehearsal for the real test.
8. If you need more practice after that, the domain-split
   [`practice-questions/`](../practice-questions/index.md) bank is there for targeted
   re-drilling of whichever domain(s) keep tripping you up.

A sensible overall sequence through *all* of this repo's SAA-C03 question material looks like:

```
Domain 1-2 study → bank-1.md → Domain 3-4 study → bank-2.md → weak-spot review
→ bank-3.md → full-exams/exam-1 (timed) → review misses → full-exams/exam-2 (timed)
→ (optional) practice-questions/ domain banks for any domain still shaky
```

## Status

✅ All 3 banks written: 65 questions each (195 total), domain-weighted 20/17/15/13 per bank
matching the 30%/26%/24%/20% official blueprint, mixed/interleaved domain order, study-mode
format (answer + full explanation immediately after every question), 14–17 Mermaid diagrams
per bank plus a verified real AWS documentation image in each, and 2–3 "Choose TWO" questions
per bank. All 195 scenarios confirmed mutually distinct across the three banks and distinct
from [`practice-questions/`](../practice-questions/index.md) and
[`practice-questions/full-exams/`](../practice-questions/full-exams/index.md).
