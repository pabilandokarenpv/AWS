# Content Template

Every service/topic/term doc in this repo (under `services/`, `00-fundamentals/`, and each
cert's `domain-*/` folders) follows this exact structure. Copy this file's skeleton when adding
a new topic. The goal: a non-technical reader gets the idea, a technical reader gets the depth,
and an exam-taker gets what's actually tested.

```markdown
# <Service / Topic Name>

![<Service> icon](https://icon.icepanel.io/AWS/svg/<Category>/<Service-Icon-Name>.svg)
<!-- or official AWS Architecture Icons asset; see diagrams/README.md for the convention -->

## Definition
One or two plain-English sentences. No jargon. What IS this, in the simplest possible terms.

## Purpose
Why does this service/concept exist? What problem was AWS solving when they built it?

## How It Works
Plain explanation, then a Mermaid diagram showing the flow/architecture.

\`\`\`mermaid
flowchart LR
    A[Client] --> B[Service]
    B --> C[(Data Store)]
\`\`\`

Walk through the diagram step by step underneath it — never leave a diagram unexplained.

## Key Features / Components
Bullet list of the sub-parts or capabilities, each with a one-line explanation.

## Use Cases — When to Use It
Concrete, real scenarios. "Use this when X." Not abstract — name the situation.

## When NOT to Use It / Alternatives
Equally important: what this is a bad fit for, and what to use instead, with the tradeoff.

## Why It's Important
Real-world weight (cost, reliability, security implications) AND exam weight (why AWS tests
this, which domain/task statement it maps to).

## Pricing Model (summary)
How you get billed for this — free tier, per-request, per-GB, per-hour, reserved vs on-demand,
whatever applies. Link the official pricing page for exact current numbers (they change).

## Hands-on Lab (Floci)
A runnable example against the free local Floci emulator — actual CLI commands, not pseudocode.
Link to the matching file under `labs-floci/`.

## Exam Tips
- Common exam traps / confusions with similar services
- Keywords in a question that point to this service
- Which domain(s) and cert(s) this shows up in

## Related Terms
Links to glossary entries and other service docs this connects to.
```

## Rules for every doc

- **Define before you use.** Never use a term without it being defined somewhere linked.
- **One concept, one file.** Don't cram multiple services into a single doc — cross-link instead.
- **Diagrams must be explained**, not decorative. If a diagram adds nothing beyond the text, cut it.
- **Cite the official source** for anything that changes often (pricing, quotas, exam domains).
- **Exam relevance is mandatory** — every doc states which cert/domain it maps to, even fundamentals.
