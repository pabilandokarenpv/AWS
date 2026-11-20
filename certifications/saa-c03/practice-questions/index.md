# SAA-C03 Practice Questions

Scenario-based practice questions for the [AWS Certified Solutions Architect – Associate
(SAA-C03)](../README.md) exam — en's first cert, starting Jan 2027, and the highest-priority
material in this repo.

## Question count per domain

| Domain | Weight | Questions | Multi-select ("Choose TWO") |
|---|---|---|---|
| [Domain 1 — Secure Architectures](domain-1-questions.md) | 30% | 18 | 3 |
| [Domain 2 — Resilient Architectures](domain-2-questions.md) | 26% | 16 | 2 |
| [Domain 3 — High-Performing Architectures](domain-3-questions.md) | 24% | 14 | 2 |
| [Domain 4 — Cost-Optimized Architectures](domain-4-questions.md) | 20% | 12 | 2 |
| **Total** | **100%** | **60** | **9 (~15%)** |

The question count per domain is weighted to match the official exam's domain weighting
(see [`../README.md`](../README.md#domains--weights)) — Domain 1 gets the most questions
because it's 30% of the real exam and its concepts (IAM, VPC security, encryption) are
assumed knowledge everywhere else. The ~15% multi-select ratio matches the real exam's mix
of "multiple choice" and "multiple response" question formats.

Every question is scenario-based (a company/constraint/ask, not trivia recall), includes
exactly one correct answer (or two for "Choose TWO" questions), a full explanation of *why*
the correct answer is right citing the specific AWS service or concept, and an explicit
explanation of *why each wrong option is wrong* — not just "incorrect," but the specific
misconception or mismatch it represents. Every explanation links back to the relevant
[`services/`](../../../services) doc or domain doc in this repo for deeper review.

## This isn't the only practice material — here's the full picture

This folder (60 domain-split questions) is for studying ONE domain at a time. Two more
resources exist for different stages of prep:

- **[`full-exams/`](full-exams/index.md)** — 2 full-length, **timed, blind** 65-question mock
  exams (questions and answer keys in separate files) matching the real exam's exact item
  count and domain weighting. Use these last, under real time pressure, once you've finished
  all domains.
- **[`../exam-bank/`](../exam-bank/README.md)** — 3 more 65-question banks (bank-1/2/3), but
  **study-mode**: the answer and full explanation sit right under each question, for drilling
  after a full first pass through all 4 domains, before you attempt the timed `full-exams/`.

## How to use these

1. **Attempt every question cold, without looking at the answer first.** Write down your
   choice (and your reasoning in one sentence) before revealing the explanation — the
   point is to catch what you don't know, not to confirm what you do.
2. **Read the explanation even when you got it right.** The real exam often rewards knowing
   *why* a close second-best option is wrong, not just picking the right one — these
   explanations are where that nuance lives.
3. **Follow the linked `services/` or domain doc for anything shaky.** A wrong answer (or a
   right answer you weren't confident about) is a signal to go read the full topic doc, not
   just move on.
4. **Re-attempt the full domain file after about a week**, cold again, without rereading
   your notes first. Compare against your first pass — questions you miss a second time are
   your real weak spots and deserve focused review before moving to the next domain.
5. **Work in domain order (1 → 2 → 3 → 4)**, matching the [study order](../README.md#study-order)
   in the SAA-C03 README — Domain 1's security concepts recur as assumed knowledge in
   Domains 2–4, so shoring it up first pays off everywhere else.
6. Track score per domain over attempts (even a simple tally) — consistent misses
   concentrated in one domain/task statement is the clearest signal of where to focus before
   scheduling the real exam.

## Status

✅ All 60 questions written (as of this authoring pass). Covers every task statement listed
in [Domain 1](../domain-1-secure-architectures/README.md), [Domain 2](../domain-2-resilient-architectures/README.md),
[Domain 3](../domain-3-high-performing-architectures/README.md), and
[Domain 4](../domain-4-cost-optimized-architectures/README.md) READMEs.
