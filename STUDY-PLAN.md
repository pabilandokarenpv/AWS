# Study Plan — en's Path to SAA-C03 → DVA-C03 → MLA-C02

Target: **start SAA-C03 prep January 2027**, sit it first, then move to DVA-C03, then MLA-C02.

## Why this order

SAA-C03 builds the shared vocabulary (VPC/networking, IAM/security, storage, databases,
Well-Architected thinking) that both other certs assume you already know. Skipping straight to
DVA-C03 or MLA-C02 means re-learning fundamentals mid-domain, which is slower overall.

## Phase 0 — Before you open a single domain doc (do this once)

1. Read [`00-fundamentals/`](00-fundamentals) top to bottom (~5 files, ~1,200 lines). Don't skim —
   every cert assumes this cold.
2. Set up [Floci](labs-floci/README.md) locally (`docker run -d -p 4566:4566 floci/floci`), confirm
   `awslocal s3 ls` works. You'll use it in every domain's `labs.md`.
3. Skim [`glossary/README.md`](glossary/README.md) once just to know it exists — you'll come back
   to it constantly as a lookup, not read it linearly.

## Phase 1 — SAA-C03 (target: ~6-8 weeks of real study before exam date)

Work domain by domain, in order (weight-ranked, and each builds on the last):

| Week(s) | Domain | What "done" looks like |
|---|---|---|
| 1-2 | [Domain 1: Secure Architectures](certifications/saa-c03/domain-1-secure-architectures) (30%) | Every linked service doc read, both new domain docs (multi-account strategy, VPC security patterns) read, `labs.md` exercises run against Floci, `practice-questions/domain-1-questions.md` scored 80%+ |
| 3-4 | [Domain 2: Resilient Architectures](certifications/saa-c03/domain-2-resilient-architectures) (26%) | Same pattern — services read, labs run, 80%+ on domain 2 questions |
| 5 | [Domain 3: High-Performing Architectures](certifications/saa-c03/domain-3-high-performing-architectures) (24%) | Same pattern |
| 6 | [Domain 4: Cost-Optimized Architectures](certifications/saa-c03/domain-4-cost-optimized-architectures) (20%) | Same pattern |
| 7 | Full review | Re-run ALL 60 practice questions cold (no peeking), target 80%+ overall, weakest domain gets a re-read |
| 8 | Exam week | Light review only — skim "Common exam scenarios" sections in each domain README, don't cram new material |

**Rule of thumb:** if you score under 70% on a domain's practice questions, that domain isn't
done — go back to the specific service docs the wrong answers point to (every explanation links
one), not the whole domain again.

## Phase 2 — DVA-C03 (after SAA-C03 is passed/sat)

Same weekly rhythm, ~5-6 weeks (you already know the shared vocabulary from Phase 1, so this
moves faster):

1. [Domain 1: Development](certifications/dva-c03/domain-1-development) (30%) — includes the
   AI-assisted development pattern doc, read it once here, it's cross-linked everywhere else
2. [Domain 2: Security](certifications/dva-c03/domain-2-security) (26%) — includes the NEW
   Task 2.3 (AI service security) — don't skip this, it's new content with real question weight
3. [Domain 3: Testing and Deployment](certifications/dva-c03/domain-3-testing-deployment) (22%)
4. [Domain 4: Troubleshooting and Optimization](certifications/dva-c03/domain-4-troubleshooting-optimization) (22%)
5. Full review week, same 80%+ bar on all 50 practice questions

## Phase 3 — MLA-C02 (after DVA-C03)

~6-7 weeks — this one has real new conceptual load (ML fundamentals) even with the other two
certs behind you, so don't compress this phase:

1. [Domain 1: Data Preparation](certifications/mla-c02/domain-1-data-preparation) (28%) — includes
   embeddings/RAG data prep, new for C02
2. [Domain 2: Model Development](certifications/mla-c02/domain-2-model-development) (24%) — start
   with `ml-fundamentals-glossary.md` FIRST if ML concepts (epoch, overfitting, precision/recall)
   are new to you — don't read the SageMaker docs before this
3. [Domain 3: Deployment and Orchestration](certifications/mla-c02/domain-3-deployment-orchestration) (24%)
4. [Domain 4: Monitoring and Security](certifications/mla-c02/domain-4-monitoring-security) (24%) —
   includes responsible AI/Guardrails and ML cost optimization
5. Full review week, 80%+ bar on all 50 practice questions
6. **Important:** confirm the official MLA-C02 exam guide is fully published before booking (GA is
   Jan 14, 2027) — check [`certifications/mla-c02/README.md`](certifications/mla-c02/README.md) for
   the "what's provisional" note and re-verify against AWS's own guide once it's final.

## General rules across all 3 phases

- **Never passively read a domain doc once and move on.** Read it, do the lab, answer the
  practice questions, THEN mark it done.
- **Every wrong practice answer is a link, not a dead end** — the explanation points to the exact
  doc that covers what you missed. Go read that doc section again before re-attempting.
- **Mermaid diagrams are not decoration** — if you can't redraw a domain's core architecture
  diagram from memory (even roughly) by the end of that week, you don't know it yet.
- **Track progress** — tick off domains as "done" by editing this file or logging status to your
  own system (en: this maps to a Dev Work tracker entry — log "Study: SAA-C03 Domain X" as you go
  if you want visibility alongside your other projects).
- **Floci limitations are intentional honesty, not laziness** — where a lab says "Floci can't
  emulate this," that's exactly the signal that real AWS Free Tier or a documented alternative is
  worth the 20 minutes, because the exam tests real service behavior, not CLI syntax alone.
