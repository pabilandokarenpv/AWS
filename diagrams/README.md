# Diagram & Icon Conventions

## Architecture/flow diagrams → Mermaid

All architecture, sequence, and flow diagrams in this repo are written as **Mermaid** code
blocks directly in the Markdown. Why:
- Renders natively on GitHub (no external image hosting, never goes stale/broken-link)
- Version-controlled as text — diffs show exactly what changed
- Easy to update when AWS changes a service's flow

Common diagram types used:
- `flowchart` — request/data flow between services
- `sequenceDiagram` — step-by-step interaction over time (e.g., auth flows)
- `graph` — network/VPC topology
- `erDiagram` — database schema relationships

## Service logos/icons

All service icons in this repo are **committed locally** under [`diagrams/assets/icons/`](assets/icons)
— no external CDN dependency, so images never go stale or 404.

**Source:** [`awslabs/aws-icons-for-plantuml`](https://github.com/awslabs/aws-icons-for-plantuml)
(AWS's own open-source, MIT-licensed repo, rebuilt directly from AWS's official
[Architecture Icons](https://aws.amazon.com/architecture/icons/) asset package each release).
Icons are used under AWS's trademark guidelines to illustrate AWS architectures — unaltered,
no endorsement implied.

Convention used in every doc's header image:

```markdown
![Amazon S3](../../diagrams/assets/icons/amazons3.png)
```

(relative path depth adjusts based on how deep the doc lives — `services/<category>/x.md` is
two levels down from repo root, so `../../diagrams/assets/icons/...`).

Filenames are the service name lowercased with all non-alphanumeric characters stripped (e.g.
"Amazon DynamoDB" → `amazondynamodb.png`, "AWS Key Management Service" → `awskeymanagementservice.png`).

**Adding a new icon:** check `diagrams/assets/icons/` first (86+ already there). If missing,
find it in a fresh clone of `aws-icons-for-plantuml` under `dist/<Category>/<Service>.png`,
copy it in using the same normalized-filename convention, and reference it with a relative path.
Never link an external icon CDN directly — always vendor the file into this repo.

## Screenshots

Only used when a concept genuinely needs the real console UI (e.g., "where this setting lives").
Pulled from official AWS documentation pages, credited with a source link in the image caption.

## Rule

Every diagram gets a paragraph underneath explaining it step by step. A diagram with no
explanation is not finished — don't merge it.
