# AWS — Complete Certification Documentation & Learning Compilation

A single, organized, from-scratch-to-professional reference for Amazon Web Services —
built to **understand AWS deeply** and **pass the certifications**, not just memorize answers.

Written for both technical and non-technical readers: every topic starts with a plain-English
definition before going deep into architecture, diagrams, and exam-level detail.

## 🎯 Goals

1. Document every AWS domain, service, and term used across the three target certifications, in full.
2. Make it understandable to someone with zero cloud background, while still being deep enough
   for a working engineer.
3. Map every topic to **why it exists, when to use it, when NOT to use it, and why it matters**
   — not just "what it is."
4. Give everything a visual: architecture diagrams (Mermaid, rendered natively on GitHub) and
   official AWS service icons, so concepts are seen, not just read.
5. Pair every domain with free, no-cost hands-on labs using **[Floci](https://github.com/floci-io/floci)**
   (open-source local AWS emulator) — no AWS bill required to practice.

## 🏆 Target Certifications

| Certification | Code | Level | Status (as of Nov 2026) | Folder |
|---|---|---|---|---|
| Solutions Architect – Associate | **SAA-C03** | Associate | Current, stable | [`certifications/saa-c03`](certifications/saa-c03) |
| Developer – Associate | **DVA-C03** | Associate | New version, live **Dec 1, 2026** (replaces DVA-C02) | [`certifications/dva-c03`](certifications/dva-c03) |
| Machine Learning Engineer – Associate | **MLA-C02** | Associate | New version, GA **Jan 14, 2027** (replaces MLA-C01, adds GenAI/Bedrock) | [`certifications/mla-c02`](certifications/mla-c02) |

> We deliberately target the **newest exam version** of each cert (not the one retiring) so this
> doc stays useful through en's actual exam dates. Each cert folder's README has the live exam
> guide link, domain weights, task statements, format, cost, and scoring — pulled from AWS's
> official exam guide, not third-party guesses.

## 📁 Repository Structure

```
AWS/
├── 00-fundamentals/        ← Start here if you're new to AWS. Core concepts every cert assumes
│                             you already know: global infrastructure, shared responsibility,
│                             IAM basics, pricing models, the Well-Architected Framework.
├── certifications/         ← One folder per cert, organized exactly like AWS's own exam guide
│   ├── saa-c03/
│   │   ├── README.md               ← exam overview, format, scoring, domain weight table
│   │   ├── domain-1-secure-architectures/
│   │   ├── domain-2-resilient-architectures/
│   │   ├── domain-3-high-performing-architectures/
│   │   ├── domain-4-cost-optimized-architectures/
│   │   └── practice-questions/
│   ├── dva-c03/             ← same pattern, DVA-C03's 4 domains
│   └── mla-c02/             ← same pattern, MLA-C02's 4 domains
├── services/                ← Service-by-service deep reference, grouped by AWS category
│   │                           (a service like S3 or IAM shows up in multiple certs — this is
│   │                           the canonical, single source of truth per service; domain docs
│   │                           link here instead of repeating themselves)
│   ├── compute/
│   ├── storage/
│   ├── database/
│   ├── networking-content-delivery/
│   ├── security-identity-compliance/
│   ├── machine-learning-ai/
│   ├── analytics/
│   ├── application-integration/
│   ├── management-governance/
│   ├── containers/
│   └── developer-tools/
├── glossary/                ← A–Z index of every term used anywhere in this repo, one-liner +
│                               link to the full explanation
├── labs-floci/              ← Hands-on labs using Floci (free local AWS emulator), mapped to
│                               each domain so you can actually DO the thing, not just read it
├── diagrams/                ← Shared diagram conventions + official AWS icon asset references
├── CONTENT_TEMPLATE.md      ← the exact structure every topic doc follows (read this once)
└── RESOURCES.md             ← official exam guides, whitepapers, Skill Builder, Floci docs
```

## 🧩 How every topic is documented

Every service/term/topic doc follows the same template (see [`CONTENT_TEMPLATE.md`](CONTENT_TEMPLATE.md)):

**Definition → Purpose → How it works (with diagram) → Use cases / when to use → When NOT to
use / alternatives → Why it's important → Pricing model → Hands-on lab (Floci) → Exam tips →
Related terms**

This keeps every page useful whether you're skimming for the exam or trying to actually
understand the service for the first time.

## 🖼️ Diagrams & Images

- **Architecture/flow diagrams** are written as [Mermaid](https://mermaid.js.org/) code blocks —
  they render directly on GitHub, need no external hosting, and stay version-controlled as text.
- **Service logos/icons** reference AWS's official [Architecture Icons](https://aws.amazon.com/architecture/icons/)
  asset package (free to use, AWS's own branding guidelines apply) — see `diagrams/README.md`
  for the exact icon-linking convention used across docs.
- Where a concept benefits from a real screenshot (console UI, CLI output), it's pulled from the
  official AWS documentation and credited.

## 🧪 Hands-on: Floci

[Floci](https://github.com/floci-io/floci) is a free, open-source, MIT-licensed local AWS
emulator (an actively maintained alternative to LocalStack, no auth token, no feature gates).
Point the AWS CLI/SDK/Terraform/CDK at `http://localhost:4566` and most AWS APIs behave like
the real thing — S3, DynamoDB, Lambda, SQS, SNS, IAM, STS, API Gateway, Cognito, Step Functions,
CloudFormation, and more, with real Docker containers backing RDS/ECS/EKS/EC2 where it matters.

We use it so every domain's labs are **free and offline** — no AWS account, no risk of a
surprise bill, same CLI commands you'd run against real AWS. See [`labs-floci/README.md`](labs-floci/README.md).

## 📊 Build status

This is a living repository. Scaffolding and fundamentals are in place; domain content is being
filled in per-cert, per-domain, per-service. Track progress in each cert's README (checklist at
the top of every domain folder).

## 📚 Start here

1. New to AWS entirely → [`00-fundamentals/`](00-fundamentals)
2. Studying for a specific cert → jump into that cert's folder, read its `README.md` first
   (exam format + domain weights), then work domain by domain
3. Looking up one service/term → [`services/`](services) or the [`glossary/`](glossary)
4. Want to practice hands-on for free → [`labs-floci/`](labs-floci)
