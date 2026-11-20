# SAA-C03 Full-Length Mock Exams

This folder contains **full-length practice exams** that simulate the real AWS Certified
Solutions Architect – Associate (SAA-C03) exam experience in one sitting. They are a
**different study tool** from the domain-split question banks one level up in
[`../`](../index.md) (`domain-1-questions.md` through `domain-4-questions.md`) — use both, but
for different purposes.

## How this differs from the domain-split banks

| | Domain-split banks (`../domain-N-questions.md`) | Full mock exams (this folder) |
|---|---|---|
| Purpose | Targeted practice and remediation, one domain at a time | Simulate the real exam end-to-end |
| Question order | Grouped by domain, in task-statement order | Domains mixed/interleaved, like the real exam |
| Length per sitting | 12–18 questions (one domain) | 65 questions (full exam) |
| When to use | While studying a domain, or re-drilling a weak domain | After finishing all 4 domains, as a readiness check |
| Timing | Untimed, work through at your own pace | Timed to match the real exam (130 minutes) |

Use the domain banks while you're learning and shoring up weak spots. Use these full mock
exams to rehearse the actual exam-day experience — time pressure, context-switching between
domains question to question, and the full 65-question mental endurance — before you book the
real thing.

## What's in this folder

| Exam | Questions file | Answer key |
|---|---|---|
| Mock Exam 1 | [`exam-1-questions.md`](exam-1-questions.md) | [`exam-1-answer-key.md`](exam-1-answer-key.md) |
| Mock Exam 2 | [`exam-2-questions.md`](exam-2-questions.md) | [`exam-2-answer-key.md`](exam-2-answer-key.md) |

Each exam has **65 total questions** — matching the real SAA-C03 format of 50 scored questions
plus 15 unscored (pretest) questions indistinguishable from each other on exam day, so for
practice purposes every question here counts and there's no way (or need) to tell which would
be "unscored." Each exam is a mostly-multiple-choice (one correct answer, 4 options), some-
multiple-response ("Choose TWO," explicitly labeled, 5 options) mix, scenario-based in the real
exam's style: a 2–4 sentence company/situation description, then a clear question.

Domain weighting matches the official exam blueprint on every mock exam:

| Domain | Weight | Questions per exam |
|---|---|---|
| [Domain 1 — Secure Architectures](../../domain-1-secure-architectures/README.md) | 30% | 20 |
| [Domain 2 — Resilient Architectures](../../domain-2-resilient-architectures/README.md) | 26% | 17 |
| [Domain 3 — High-Performing Architectures](../../domain-3-high-performing-architectures/README.md) | 24% | 15 |
| [Domain 4 — Cost-Optimized Architectures](../../domain-4-cost-optimized-architectures/README.md) | 20% | 13 |
| **Total** | **100%** | **65** |

Exam 2 is a fully independent set of 65 questions — different companies, different scenarios,
different specific angles on the domains — so you can take both without memorizing answers
from one to the other. Each answer key gives the correct letter(s), a full paragraph on *why*
the correct answer is right, an explicit explanation of *why every distractor is wrong*, and
links back to the relevant [`services/`](../../../../services) doc or domain README for deeper
review.

## How to take a mock exam

1. **Block out 130 minutes** (the real SAA-C03 time limit) and treat it as a real exam
   sitting: no phone, no notes, no looking anything up, one unbroken session if at all
   possible. Use a timer.
2. **Open only the questions file** (`exam-N-questions.md`). Do **not** open the answer key
   until you've answered all 65 questions — looking ahead defeats the entire point of a mock
   exam as a readiness signal.
3. Answer every question — there's no penalty for guessing on the real exam, so don't leave
   any blank. For "Choose TWO" questions, select exactly two letters.
4. Write down your answers as you go (letter per question number) in a scratch document, the
   same way you'd use the real exam's review/flag-and-revisit workflow.
5. When you finish (or time runs out at 130 minutes — stop there even if unfinished, since
   that's a realistic signal too), open the matching answer key and grade yourself.
6. **Score against the real passing bar.** AWS scores SAA-C03 on a scaled 100–1000 range with
   a **passing score of 720**. AWS doesn't publish the exact scaled-to-raw conversion (scoring
   isn't simple percent-correct, and unscored questions are mixed in indistinguishably), but
   **as a practical rule of thumb, treat ~72% correct (about 47 out of 65) as the bar you need
   to clear**, and aim meaningfully above it (80%+) in practice, since mock-exam questions and
   real exam questions are never perfectly equivalent in difficulty.
7. **Use the per-domain score tracker table at the top of the answer key** to see whether
   misses are spread evenly or concentrated in one domain — concentrated misses are your clear
   signal to go back to that domain's [README](../../README.md) and
   [domain-split question bank](../index.md) before your next mock exam or the real test.
8. **Review every missed question's full explanation**, including why each wrong option you
   *didn't* pick is wrong — the real exam rewards knowing why the tempting-but-wrong answer is
   wrong, not just knowing the right one.
9. Leave at least a few days between taking Exam 1 and Exam 2 (and between either exam and a
   second attempt) so you're testing retained knowledge, not short-term memorized answers.

## Status

✅ Both full mock exams written: 65 questions each (130 total), domain-weighted 20/17/15/13
matching the 30%/26%/24%/20% official blueprint, with full answer keys and explanations for
every question.
