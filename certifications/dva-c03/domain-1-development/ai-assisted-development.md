# AI-Assisted Development (cross-domain pattern)

![The Amazon Q Developer inline chat input screen in an IDE.](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/images/inline-chat-input-screen.png)
*Source: [AWS Documentation — Chatting inline with Amazon Q Developer](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-in-IDE-inline-chat.html). A developer highlights code, types an instruction, and the assistant proposes a change — the human stays the one who accepts or rejects it.*

> This doc lives in Domain 1 because code generation/review is where the pattern starts, but the
> same underlying idea — an AI assistant doing part of a workflow a human used to do entirely by
> hand — repeats in [Domain 2](../domain-2-security/README.md#ai-assisted-development-cross-link)
> (reviewing AI-service security risks), [Domain 3](../domain-3-testing-deployment/README.md#ai-assisted-development-cross-link)
> (test generation, deployment approvals), and [Domain 4](../domain-4-troubleshooting-optimization/README.md#ai-assisted-development-cross-link)
> (error analysis, optimization suggestions). Read this once; recognize it everywhere.

## Definition

AI-assisted development means using an AI coding tool — **Amazon Q Developer**, **Kiro**, or a
similar assistant — inline in your IDE or CLI to generate code, review it, write tests for it,
help decide whether a deployment is safe, or explain why something broke. DVA-C03 is new in
testing this explicitly: you're expected to recognize *which part of the SDLC* a given AI
interaction fits into, and what its real limits are, not to know how to operate any specific tool.

## Purpose

Writing, testing, deploying, and debugging code are all time-consuming and error-prone when done
entirely by hand. AWS added these assistants (and the exam added this topic) because developer
workflows increasingly include an AI step at each stage — and because using one safely/well is now
a distinct, testable skill: knowing what to trust, what to double-check, and what never to hand
an assistant (secrets, production credentials, unreviewed auto-merges).

## How It Works — the pattern across the SDLC

```mermaid
flowchart TD
    subgraph D1["Domain 1: Development"]
        A1[Developer writes prompt / partial code] --> A2[AI suggests code completion or full function]
        A2 --> A3[Developer reviews & accepts/edits]
    end
    subgraph D3["Domain 3: Testing & Deployment"]
        B1[AI generates unit/integration tests from code] --> B2[AI flags a risky deployment diff]
        B2 --> B3[Human approves/rejects before pipeline promotes]
    end
    subgraph D4["Domain 4: Troubleshooting & Optimization"]
        C1[AI reads CloudWatch Logs/X-Ray traces] --> C2[AI summarizes likely root cause]
        C2 --> C3[AI suggests optimization: e.g. right-size Lambda memory]
    end
    A3 --> B1
    B3 --> C1
    C3 -.feeds back into.-> A1
```

Step by step:
1. **Domain 1 — generation & review**: you describe intent (a comment, a prompt, a partial
   function signature); the assistant proposes code. You, the developer, remain responsible for
   correctness — the assistant is a fast first draft, not a final reviewer. Exam angle: a question
   describing "a developer uses an AI tool suggestion in their IDE to speed up writing a Lambda
   handler" is Task 1.1 territory, not magic — same IAM, same error handling rules apply to the
   generated code.
2. **Domain 3 — test generation & deployment approvals**: the same kind of assistant can read your
   function and propose unit tests or regression tests (Task 3.2), or evaluate a pipeline's planned
   change and flag something that looks risky for a human to approve before CodePipeline/CodeDeploy
   promotes it (Task 3.3). The AI never *replaces* the approval gate — it informs it.
3. **Domain 4 — root cause & optimization**: an assistant can ingest CloudWatch Logs/Metrics, X-Ray
   trace data, and CloudTrail events and propose a likely root cause or a specific tuning change
   (e.g. "this Lambda is memory-constrained, not CPU-constrained — increase memory") (Task 4.1, 4.3).
   You still verify against the actual metrics before acting.

## The two assistants the exam cares about: Amazon Q Developer vs. Kiro

The exam guide names both explicitly, and it's worth knowing roughly how they differ in emphasis
even though the exam tests the *pattern*, not product trivia:

| | Amazon Q Developer | Kiro |
|---|---|---|
| Primary surface | Chat/inline suggestions inside an existing IDE (VS Code, JetBrains, etc.) | A full agentic IDE built around a spec-first workflow |
| Typical use | Ask questions, generate/complete code, explain an existing codebase, scan for vulnerabilities | Turn a natural-language requirement into a structured spec, then generate and iterate on an implementation against that spec |
| Where it shows up on DVA-C03 | Task 1.1 (generation/review), cross-linked into 3.2/3.3/4.1/4.3 | Same task statements — treated as an equivalent example of "AI coding assistant," not a separately tested product |
| End-of-support note | AWS has signaled it is winding down the standalone Q Developer IDE plugins in favor of Kiro-style tooling — for the exam, know both names and that they fill the same *role* | — |

Exam angle: don't memorize a feature comparison matrix. If a question names either tool, map it to
the *generic capability* (code gen, review, test gen, deployment-risk flagging, error analysis,
optimization suggestion) and answer based on that capability's rules, not the product name.

## Code generation and review, in practice

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant IDE as IDE (with AI assistant)
    participant AI as AI assistant backend
    participant Repo as Git repo / PR

    Dev->>IDE: Highlight code, type instruction ("add input validation")
    IDE->>AI: Send code context + instruction
    AI-->>IDE: Proposed diff
    IDE-->>Dev: Show diff inline
    Dev->>Dev: Review diff against requirements, security rules
    Dev->>IDE: Accept (or reject/edit)
    IDE->>Repo: Commit change (attributed to the developer, not the AI)
    Repo->>AI: (separately) AI reviews the open PR
    AI-->>Repo: Comment: flags a hardcoded secret / overly broad IAM statement
    Dev->>Repo: Addresses comment before merge
```

Two distinct moments matter here, and the exam likes to test whether you can tell them apart:
1. **Generation-time review** — the developer reviews a suggestion *before* accepting it into the
   codebase. This is the fastest feedback loop and catches the most obviously wrong suggestions.
2. **Post-hoc AI code review** — a second AI pass over an already-committed diff/PR, looking for
   patterns a human reviewer might also look for (hardcoded secrets, SQL injection shapes,
   overly permissive IAM). This doesn't replace a human reviewer, it's a faster first pass that
   surfaces things for the human to actually decide on.

## Key capabilities tested

- **Code generation/completion** — inline suggestions, full function scaffolds, boilerplate (IAM
  policy JSON, CloudFormation/CDK snippets, SDK calls).
- **Code review** — flagging obvious bugs, insecure patterns (hardcoded secrets, overly broad IAM),
  or style inconsistencies before a human merges.
- **Test generation / regression automation** — proposing unit tests, edge cases, or mock event
  payloads for Lambda test events.
- **Deployment approvals** — surfacing risk in a change (e.g. "this CDK diff deletes a DynamoDB
  table") so a human approver has more context before clicking approve in CodePipeline.
- **Error analysis** — summarizing logs/traces into a plain-English likely cause.
- **Optimization recommendations** — Lambda memory/timeout tuning, identifying overprovisioned
  resources, suggesting caching opportunities.
- **Codebase Q&A** — answering "where is X implemented" or "how does this module call that
  service" against your actual repository, which is a different capability from pure generation
  and shows up in scenarios about onboarding/understanding unfamiliar code.

## Use Cases — When to Use It

- Scaffolding repetitive boilerplate (SDK client setup, CRUD handlers, IaC resource blocks) so a
  developer's time goes to the logic that's actually novel.
- Generating a first pass at unit tests immediately after writing a function, before a human adds
  the edge cases the AI missed.
- Summarizing a wall of CloudWatch Logs into "here are the three requests that errored and why"
  during an incident, to shortcut triage.
- Getting a second opinion on an IAM policy or security group rule before it ships.
- Explaining an unfamiliar legacy module to a new team member faster than reading the whole thing
  line by line.
- Drafting a first version of documentation (README, runbook) from existing code/comments, which a
  human then edits for accuracy.

## When NOT to Use It / Limits

- **Never feed secrets, credentials, customer PII, or proprietary source you don't have rights to
  share into a third-party-hosted assistant** unless you've confirmed the specific tool's data
  handling (see [Task 2.3 security doc](../domain-2-security/ai-service-security-risks.md) for how
  this is modeled for Bedrock-style AI services specifically).
- **Never let an AI-proposed change auto-deploy to production without a human approval gate** —
  Task 3.3 still expects CodeDeploy/CodePipeline manual approval actions or equivalent guardrails.
- **Don't trust AI-generated root-cause explanations as ground truth** — always cross-check against
  the actual CloudWatch/X-Ray data; the assistant can hallucinate a plausible-sounding but wrong
  explanation.
- Generated code still needs the same code review rigor as human-written code — faster to produce
  is not the same as more correct.
- **Don't treat AI-generated IAM policies as safe-by-default** — a common real failure mode is an
  assistant proposing `Resource: "*"` "to make it work" because that's the shortest path to a
  passing test; the developer still owns scoping it down.
- **Don't rely on AI-generated tests as your only test coverage** — they're a strong starting point
  but tend to miss the edge cases the original developer didn't think to mention either.

## Why It's Important

Real-world: these tools are now a default part of how teams at AWS-using companies build software;
not knowing their failure modes (over-trusting output, leaking data into prompts) is a genuine
operational risk. Exam weight: this is explicitly called out as new in DVA-C03 across Tasks 1.1,
3.2, 3.3, and 4.1/4.3 — expect at least one question per domain that's really testing "do you know
where the human judgment still has to sit."

## Worked scenario: using AI assistance correctly through one feature's lifecycle

A team is adding a "reorder previous purchase" button to an e-commerce app's Lambda-backed API.
Walk through how AI assistance shows up correctly at each stage, and where a human must step in:

1. **Generation (Domain 1).** The developer prompts the IDE assistant: "write a handler that looks
   up the user's last order from DynamoDB and re-creates it as a new order." The assistant
   generates a first draft. The developer reviews it and notices it doesn't handle the case where
   the user has no previous orders — adds that check manually. *Correct use*: fast first draft,
   human catches the gap.
2. **Test generation (Domain 3).** Before opening a PR, the developer asks the assistant to
   generate unit tests for the handler. It proposes tests for the happy path and the no-previous-
   order case, but misses a test for a previous order that references a now-discontinued product.
   The developer adds that test by hand after thinking about what could realistically go wrong.
   *Correct use*: AI covers the obvious cases fast, human adds the business-specific edge case.
3. **Deployment approval (Domain 3).** The PR merges and CodePipeline builds a deployment. An AI
   step summarizes the diff for the approver: "adds a new Lambda function and a new IAM permission
   to read the Orders table — no destructive changes." A human approver reads the summary, confirms
   it against the actual diff, and clicks approve. *Correct use*: the AI saves the approver time
   reading a full diff, but the approver still makes the actual decision.
4. **Incident response (Domain 4).** A week later, the function starts erroring. An AI tool reads
   the CloudWatch Logs and X-Ray trace and proposes: "likely cause: the discontinued-product edge
   case is throwing an unhandled exception." An engineer checks the actual logs, confirms the
   AI's hypothesis is correct this time, and ships a fix. *Correct use*: faster triage, verified
   before acting — not blind trust.

Every step followed the same shape: **AI proposes, human verifies, human remains accountable.**
That shape, not any specific tool feature, is what DVA-C03 is actually testing.

## Pricing Model (summary)

Not a billed AWS service line item in the same sense as compute/storage — Amazon Q Developer has
free and paid (Pro) tiers tied to usage limits and organizational features; Kiro's pricing is
usage/seat based. Exam-relevant point: cost isn't the testable angle here, *usage pattern* is.

## Hands-on Lab (Floci)

Floci doesn't emulate AI coding assistants themselves (there's no API surface to call locally for
code generation). See [`labs.md`](labs.md) Lab 4 for an exercise that simulates the *pattern* —
writing a script that mimics "AI proposes, pipeline gate requires human approval" using
EventBridge + a manual Step Functions approval task, which is the testable mechanism underneath
the AI-assisted-deployment-approval idea.

## Feature-by-feature: what each AI capability maps to on the exam

| Capability | What it looks like in practice | Exam task it maps to | What a human must still verify |
|---|---|---|---|
| Inline code completion | Ghost-text suggestion as you type, accepted with Tab | 1.1 | Logic correctness, IAM scope of any API calls it introduces |
| Chat-based generation | "write a function that does X" in a chat panel | 1.1 | Same as above, plus that the generated code matches the *actual* event shape (e.g. S3 vs. SQS event structure) |
| Inline diff / refactor | Highlight code, ask for a change, review a diff before accepting | 1.1 | The diff doesn't silently change behavior outside what was asked |
| Security/vulnerability scanning | Static-analysis-style scan flags a hardcoded secret, SQL injection shape, or overly broad IAM statement | 1.1 / 2.1 / 2.2 (overlaps into security) | A flagged finding is still a human decision to fix/ignore — false positives happen |
| Unit/integration test generation | Given a function, propose test cases including a few edge cases | 3.2 | Business-specific edge cases the AI has no way to know about |
| Documentation/explanation | Summarize what an unfamiliar module does | — (productivity, not directly task-mapped) | Accuracy against the actual code, not just plausible-sounding prose |
| Deployment-risk summarization | Summarize a pending IaC diff's blast radius for an approver | 3.3 | The approver reads the actual diff too for anything destructive |
| Log/trace summarization | Condense a wall of CloudWatch/X-Ray data into a likely root cause | 4.1 | Cross-check against the raw metrics/trace before acting |
| Optimization suggestion | "this function is memory-constrained, raise memory" | 4.3 | Confirm with actual CloudWatch Duration/Memory-utilization metrics before changing production config |

## Concrete before/after: a Lambda handler reviewed by an AI assistant

What a *correct* AI-assisted review catches, concretely — this is the shape of a Domain 1/2
overlap question:

```python
# Before: developer's first draft (hands this to the assistant for review)
import boto3
ddb = boto3.client("dynamodb")

def handler(event, context):
    table = "Orders"
    user_id = event["queryStringParameters"]["userId"]
    resp = ddb.query(
        TableName=table,
        KeyConditionExpression="userId = :u",
        ExpressionAttributeValues={":u": {"S": user_id}}
    )
    return {"statusCode": 200, "body": resp["Items"]}  # BUG: body must be a JSON string
```

```python
# After: AI-flagged issues addressed by the developer, not blindly auto-applied
import boto3, json
ddb = boto3.client("dynamodb")

def handler(event, context):
    qsp = event.get("queryStringParameters") or {}
    user_id = qsp.get("userId")
    if not user_id:
        return {"statusCode": 400, "body": json.dumps({"error": "userId is required"})}

    resp = ddb.query(
        TableName="Orders",
        KeyConditionExpression="userId = :u",
        ExpressionAttributeValues={":u": {"S": user_id}}
    )
    return {"statusCode": 200, "body": json.dumps(resp["Items"])}
```

Three things an assistant plausibly flags here, mapped to what's actually being tested: (1) the
missing JSON serialization of `body` (Task 1.1's serialize/deserialize skill), (2) no defensive
check for a missing query string parameter (basic input validation, not AWS-specific but a common
"what's wrong with this code" exam snippet pattern), (3) implicitly, that `event["queryStringParameters"]`
can be `None` entirely (not just missing a key) if the request had no query string at all — a very
common real Lambda bug that an assistant's suggestion correctly guards against with `.get(...) or {}`.

## Real-world failure modes worth knowing by name

- **Prompt-to-production with no review.** A team configures a pipeline step that takes an AI
  tool's suggested fix for a failing test and auto-commits it directly to the deploy branch with no
  human review. The fix happens to "pass" by deleting the failing assertion rather than fixing the
  underlying bug. This is the textbook wrong-answer shape on the exam: any workflow where AI output
  reaches production without a human checkpoint is the incorrect option.
- **Context leakage.** A developer pastes a full stack trace into a chat assistant to get help
  debugging, not noticing the stack trace includes a database connection string with embedded
  credentials. Mitigation is procedural (scrub secrets before pasting, or use a tool/config that
  guarantees inputs aren't retained/used for training) — see
  [`../domain-2-security/ai-service-security-risks.md#keeping-inputsoutputs-out-of-model-training`](../domain-2-security/ai-service-security-risks.md#keeping-inputsoutputs-out-of-model-training).
- **Over-broad generated IAM.** An assistant generates a Lambda execution role with
  `"Action": "dynamodb:*"` because the prompt didn't specify which actions were actually needed and
  the broadest policy is the fastest way to make a demo "just work." Ships without being scoped
  down. This is Task 2.1/2.2 territory wearing a Domain-1 hat — least privilege is still the
  developer's job regardless of who/what wrote the first draft of the policy.
- **Confident wrong root cause.** During an incident, an AI summarizes CloudWatch Logs and
  confidently states the cause is a downstream timeout, when the actual cause (visible in X-Ray but
  not surfaced in the summary) is a cold-start-induced delay exceeding an API Gateway timeout. An
  engineer who ships a fix for the wrong cause (increasing a downstream timeout) wastes an incident
  cycle. This is exactly why Task 4.1 still expects a human to verify against the raw data.

## Kiro's spec-driven workflow, in a bit more depth

Where Amazon Q Developer's primary mode is conversational/inline assistance inside an existing
project, Kiro leans into a **spec-first** workflow that's worth understanding conceptually (not
operationally) because it's a cleaner illustration of "AI proposes, human verifies" than a single
inline suggestion is:

```mermaid
flowchart LR
    REQ[Developer writes a natural-language requirement] --> SPEC[Kiro generates a structured spec:\nrequirements + design + task list]
    SPEC --> REVIEW{Developer reviews/edits the spec}
    REVIEW -->|approved| IMPL[Kiro generates implementation against the approved spec]
    REVIEW -->|needs changes| SPEC
    IMPL --> TEST[Generated/human tests run]
    TEST -->|pass| PR[Opened as a PR for human review]
    TEST -->|fail| IMPL
```

The exam-relevant takeaway isn't the tool's UI, it's that this workflow makes the "human
checkpoint" explicit and structural (you review the *spec* before any code is generated against
it) rather than ad hoc (reviewing a diff after the fact). Both are valid instances of the same
underlying pattern this doc keeps repeating: **generation, then human judgment, before anything
becomes permanent.** A scenario question contrasting "a team wants requirements reviewed and
locked before any code is generated" against "a team wants fast inline suggestions while typing"
is really just asking you to recognize these as two flavors of the same safe pattern, not to pick
a specific product by name.

## Exam Tips

- If a question describes an AI tool *doing* something irreversible (deploying, deleting, merging)
  with zero human check — that's the wrong answer. The correct pattern always keeps a human gate.
- If a question is about *generating* code/tests/explanations to *assist* a human — that's the
  right usage pattern.
- Don't memorize specific tool names' feature lists — the exam tests the *pattern* (generation,
  review, test-gen, approval-assist, error-analysis, optimization-assist), not product trivia.
- If a question asks "what should NOT be sent to an AI coding assistant," the answer is always
  secrets/credentials/PII — regardless of which specific tool is named.
- Expect at most one or two direct questions per domain on this topic; it's broad but shallow on
  this exam version — know the pattern, don't over-invest in tool-specific trivia.

## Related Terms

- [`../domain-2-security/ai-service-security-risks.md`](../domain-2-security/ai-service-security-risks.md) — the security-specific risks of AI *services* (Bedrock/Q), distinct from this dev-workflow pattern.
- [`../domain-3-testing-deployment/README.md#ai-assisted-development-cross-link`](../domain-3-testing-deployment/README.md#ai-assisted-development-cross-link) — test generation and deployment approvals in practice.
- [`../domain-4-troubleshooting-optimization/README.md#ai-assisted-development-cross-link`](../domain-4-troubleshooting-optimization/README.md#ai-assisted-development-cross-link) — error analysis and optimization recommendations in practice.
- [`services/machine-learning-ai/bedrock.md`](../../../services/machine-learning-ai/bedrock.md)
- [`services/machine-learning-ai/amazon-q.md`](../../../services/machine-learning-ai/amazon-q.md)
- [`services/developer-tools/codepipeline.md`](../../../services/developer-tools/codepipeline.md) — where deployment approval gates live.
- [`services/developer-tools/codedeploy.md`](../../../services/developer-tools/codedeploy.md) — where an AI-flagged risky deployment would actually be held for approval.
- [`services/management-governance/cloudwatch.md`](../../../services/management-governance/cloudwatch.md) — the data AI-assisted error analysis reads.
- [`services/compute/lambda.md`](../../../services/compute/lambda.md) — the most common target of AI-generated code on this exam's scenarios.
