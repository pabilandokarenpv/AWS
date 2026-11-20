# 00 — Fundamentals

Read this folder before any certification-specific content. Every cert assumes you already
understand these concepts; none of the three exam guides re-explain them from scratch.

## Contents

| File | What it covers |
|---|---|
| [`aws-global-infrastructure.md`](aws-global-infrastructure.md) | Regions, Availability Zones, Edge Locations — how AWS's physical footprint works and why it matters for every architecture decision |
| [`shared-responsibility-model.md`](shared-responsibility-model.md) | What AWS secures vs. what you secure — the single most-tested concept across all 3 certs |
| [`well-architected-framework.md`](well-architected-framework.md) | The 6 pillars AWS judges every architecture against |
| [`iam-fundamentals.md`](iam-fundamentals.md) | Identity, authentication, authorization — the backbone of every security question on every exam |
| [`pricing-and-billing.md`](pricing-and-billing.md) | How AWS bills you, the core pricing models, and the tools to track/control spend |
| [`compute-storage-network-database-primer.md`](compute-storage-network-database-primer.md) | The 4 resource categories every AWS service falls into, explained with zero jargon, before we name a single service |

## Why fundamentals come first

All three certifications (SAA-C03, DVA-C03, MLA-C02) silently assume this knowledge. Exam
questions won't ask "what is a Region" directly — they'll ask you to choose between two
architectures, and the correct answer depends on understanding Regions/AZs cold. Skipping this
section is the #1 reason people re-read domain docs 3 times without it sticking.
