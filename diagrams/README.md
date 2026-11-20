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

For service identity (not architecture flow), reference AWS's **official Architecture Icons**
package: https://aws.amazon.com/architecture/icons/ (free under AWS's trademark guidelines —
icons may be used to illustrate AWS architectures; don't alter the icon or imply endorsement).

Convention used in this repo for inline icons (lightweight CDN mirror of the official set, kept
in sync with AWS's category groupings):

```markdown
![Amazon S3](https://icon.icepanel.io/AWS/svg/Storage/Simple-Storage-Service.svg)
```

Category folders mirror AWS's own grouping: Compute, Storage, Database,
Networking-Content-Delivery, Security-Identity-Compliance, Machine-Learning, Analytics,
App-Integration, Management-Governance, Containers, Developer-Tools.

If a specific icon URL 404s, pull the current one from the official AWS Architecture Icons zip
(linked above), drop the SVG/PNG into `diagrams/assets/<category>/`, and reference it with a
relative path instead — this is the fallback for icons not available via CDN mirror.

## Screenshots

Only used when a concept genuinely needs the real console UI (e.g., "where this setting lives").
Pulled from official AWS documentation pages, credited with a source link in the image caption.

## Rule

Every diagram gets a paragraph underneath explaining it step by step. A diagram with no
explanation is not finished — don't merge it.
