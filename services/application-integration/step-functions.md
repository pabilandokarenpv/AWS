# AWS Step Functions

![AWS Step Functions](https://icon.icepanel.io/AWS/svg/App-Integration/Step-Functions.svg)
<!-- If this icon 404s, pull "Step-Functions.svg" from the official AWS Architecture Icons zip
(App-Integration category) — see diagrams/README.md -->

## Definition

AWS Step Functions is a **serverless workflow orchestrator**. You describe a multi-step process
— call this Lambda, then check a condition, then call that Lambda, retry on failure, wait for a
human approval — as a **state machine** (a diagram of steps and transitions), and Step
Functions runs it, tracks exactly where it is, handles retries/errors, and shows you the
execution history visually. Instead of writing your own "what happens after this succeeds / what
happens if this fails" glue code, you declare it.

## Purpose

Coordinating multiple services into one business process (e.g., "process an order: charge the
card, reserve inventory, schedule shipping, send confirmation — and roll back cleanly if any
step fails") traditionally meant either a giant Lambda function full of try/except chains, or a
hand-rolled queue-based saga with no central visibility into where a given order currently is.
AWS built Step Functions to make that orchestration explicit, visual, and resilient by default:
the state machine itself owns retries, timeouts, parallel branches, and error handling, and
every execution's history is inspectable step by step after the fact — essential for debugging
"why did order #4471 get stuck."

## How It Works

You define a **state machine** using **Amazon States Language (ASL)**, a JSON structure
describing **states** (steps) and the transitions between them. Step Functions executes it:
each state does something (invoke a Lambda, call another AWS service directly, wait, branch on
a condition, run branches in parallel, or stop), and the service tracks the current state,
input/output passed between states, and retry/catch behavior per state, for every execution.

```mermaid
flowchart TD
    START([Start: OrderPlaced]) --> V[Task: ValidatePayment]
    V -->|success| C{Choice: Inventory Available?}
    V -->|failure, after retries| F1[Fail: PaymentDeclined]
    C -->|yes| P[Parallel]
    C -->|no| F2[Fail: OutOfStock]
    P --> R[Task: ReserveInventory]
    P --> N[Task: NotifyWarehouse]
    R --> W[Task: ScheduleShipping]
    N --> W
    W --> END([Succeed: OrderComplete])
```

Step by step:
1. **Start**: an execution begins with an input payload (e.g., the order details), usually
   triggered by EventBridge, API Gateway, or a direct SDK call.
2. **Task state — ValidatePayment**: invokes a Lambda (or calls a service API directly via
   Step Functions' native integrations); if it fails, Step Functions can automatically **retry**
   with backoff per a configured policy before giving up.
3. **Choice state**: branches the workflow based on the task's output — no custom code needed,
   it's a declarative condition in the state machine definition.
4. **Catch/Fail states**: if validation ultimately fails or inventory is unavailable, the
   execution moves to an explicit **Fail** state — recorded clearly in the execution history,
   not buried in a log line.
5. **Parallel state**: runs `ReserveInventory` and `NotifyWarehouse` at the same time, each as
   its own branch; the state machine waits for both to finish before moving on.
6. **Succeed**: once shipping is scheduled, the execution ends successfully — the entire
   history (every state entered, every input/output, every retry) is visible afterward in the
   console or via API, which is the core debugging value proposition.

## Key Features / Components

- **State machine** — the ASL JSON definition of states and transitions; the unit you deploy
  and version.
- **States** — `Task` (do work, usually invoking another AWS service), `Choice` (branch),
  `Parallel` (run branches concurrently), `Map` (run a step over each item in an array,
  optionally concurrently), `Wait` (pause for a duration or until a timestamp), `Pass` (no-op,
  reshape data), `Succeed`/`Fail` (terminal states).
- **Standard Workflows** — long-running (up to 1 year), exactly-once execution, full execution
  history retained, priced per state transition.
- **Express Workflows** — short-duration (up to 5 minutes), at-least-once execution, built for
  high-volume/high-throughput event processing, priced per invocation + duration + memory
  (like Lambda), history goes to CloudWatch Logs instead of being retained natively.
- **Native service integrations** — many AWS services (DynamoDB, SNS, SQS, ECS, Glue, SageMaker,
  and more) can be called directly from a Task state without a Lambda in between.
- **Error handling** — `Retry` (with interval, backoff rate, max attempts) and `Catch` (route
  to a fallback state) can be attached per state, declaratively.
- **Map state "distributed mode"** — process large datasets (millions of items) with massive
  concurrency, each item run as its own sub-execution.

## Use Cases — When to Use It

- **Multi-step business processes with branching and compensation logic**: order processing,
  loan approval pipelines, employee onboarding workflows.
- **Orchestrating a sequence of Lambda functions** where you'd otherwise write custom
  state-tracking and retry code inside the functions themselves.
- **ETL/data processing pipelines**: coordinate Glue jobs, batch processing, and conditional
  branches based on data validation results.
- **High-volume, short-lived event processing at scale** (Express Workflows): e.g.,
  transforming and routing millions of IoT telemetry events per day.
- **Human-in-the-loop approval steps**: pause a workflow (via the "wait for callback" task
  token pattern) until a person approves a request through a separate system.

## When NOT to Use It / Alternatives

- **A single, simple function call with no branching, retries, or multi-step coordination** →
  just invoke the Lambda directly (via API Gateway, EventBridge target, or SDK) — Step
  Functions adds cost and complexity for no benefit if there's nothing to orchestrate.
- **Need one event delivered to many independent, unrelated consumers** → **SNS**/
  **EventBridge**; Step Functions represents *one* coordinated process, not a fan-out broadcast.
- **Need a durable work queue many interchangeable workers pull from** → **SQS**; Step
  Functions is about sequencing/branching a specific process, not generic queuing.
- **Extremely high-throughput (sub-100ms, massive scale) stateless transformations with no
  need for execution history** → plain Lambda or Kinesis-based stream processing may be
  cheaper and simpler than Express Workflows.
- **Cost-sensitive, very frequent, trivial workflows** on Standard Workflows — per-state-transition
  pricing adds up fast for chatty, high-frequency simple workflows; Express Workflows or a
  different design may be cheaper.

### Standard vs Express Workflows

| | Standard | Express |
|---|---|---|
| Max duration | Up to 1 year | Up to 5 minutes |
| Execution semantics | Exactly-once | At-least-once |
| Execution history | Full history retained & viewable in console | Sent to CloudWatch Logs (optional), not retained in the same way |
| Pricing | Per state transition | Per invocation + duration + memory (Lambda-like) |
| Throughput | Lower (built for durability, not raw speed) | Very high (built for event-heavy, high-volume workloads) |
| Best for | Long-running, auditable business processes | High-volume, short, frequent event processing |

## Why It's Important

**Real-world**: Step Functions turns "a bunch of Lambdas calling each other with custom retry
logic scattered across the codebase" into one visual, versioned, auditable definition —
dramatically cutting both bugs (declarative retry/catch beats hand-rolled try/except sprawl)
and mean-time-to-diagnose (you can see exactly which execution got stuck at which state, with
what input).

**Exam mapping**:
- **SAA-C03 Domain 2 (Design Resilient Architectures), Task 2.1** — orchestrating multi-step,
  loosely coupled serverless architectures resiliently; Step Functions is the named answer
  whenever a scenario needs coordinated retries/rollback across multiple services rather than
  one Lambda doing everything.
- **DVA-C03 Domain 1 (Development with AWS Services), Task 1.1** — building event-driven
  applications with proper orchestration; expect direct questions on choosing Standard vs
  Express based on duration/volume/exactly-once requirements, and on Task/Choice/Parallel/Map
  state semantics.

## Pricing Model (summary)

**Standard Workflows**: priced per state transition (each step executed in an execution counts
as one transition); no charge for idle/waiting states beyond the transition into/out of them.
**Express Workflows**: priced per number of requests (invocations) plus duration × memory
consumed, similar to Lambda billing. Both have a monthly free tier allotment. See the
[official Step Functions pricing page](https://aws.amazon.com/step-functions/pricing/) for
current numbers.

## Hands-on Lab (Floci)

```bash
# A minimal state machine definition (save as state-machine.json)
cat <<'EOF' > /tmp/state-machine.json
{
  "Comment": "Simple order validation workflow",
  "StartAt": "ValidateOrder",
  "States": {
    "ValidateOrder": {
      "Type": "Pass",
      "Result": {"status": "validated"},
      "Next": "IsValid"
    },
    "IsValid": {
      "Type": "Choice",
      "Choices": [
        {"Variable": "$.status", "StringEquals": "validated", "Next": "OrderComplete"}
      ],
      "Default": "OrderFailed"
    },
    "OrderComplete": {"Type": "Succeed"},
    "OrderFailed": {"Type": "Fail", "Error": "ValidationFailed"}
  }
}
EOF

# Create an IAM role Step Functions can assume (Floci accepts any ARN-shaped value locally)
# Create the state machine
awslocal stepfunctions create-state-machine \
  --name order-validation \
  --definition file:///tmp/state-machine.json \
  --role-arn arn:aws:iam::000000000000:role/floci-stepfunctions-role \
  --type STANDARD

# Start an execution
awslocal stepfunctions start-execution \
  --state-machine-arn arn:aws:states:us-east-1:000000000000:stateMachine:order-validation \
  --input '{"orderId": "3001"}'

# List executions and check status
awslocal stepfunctions list-executions \
  --state-machine-arn arn:aws:states:us-east-1:000000000000:stateMachine:order-validation

# Describe one execution to see its final output/history
awslocal stepfunctions describe-execution --execution-arn "<execution-arn-from-above>"
```
Full walkthrough (Task states invoking Lambda, Parallel/Map, Express vs Standard side by side):
`labs-floci/README.md` lab index → application-integration section.

## Exam Tips

- **Standard vs Express is a guaranteed exam topic**: duration > 5 minutes, need exactly-once,
  need full execution history in-console → Standard. High volume, short-lived, cost-sensitive
  at scale, at-least-once is acceptable → Express.
- **"Orchestration" is the keyword** that points to Step Functions in a scenario — if the
  question describes several Lambdas that must run in a specific order with conditional
  branching/retries/rollback, that's Step Functions, not a single Lambda with internal if/else.
- **Native service integrations** mean Step Functions can call DynamoDB, SNS, SQS, ECS, and
  others *directly* from a Task state — a question asking "how do I avoid writing a Lambda just
  to make one API call" often wants a native integration, not an unnecessary Lambda wrapper.
- **Map state (distributed mode)** is the answer for "process millions of files/records with
  high concurrency without managing your own fleet of workers."
- Exam domains: **SAA-C03 Domain 2 Task 2.1**, **DVA-C03 Domain 1 Task 1.1**.

## Related Terms

- [`eventbridge.md`](./eventbridge.md) — commonly the trigger that starts a Step Functions
  execution.
- [`sqs.md`](./sqs.md) / [`sns.md`](./sns.md) — often called as native integration targets
  from within a Task state.
- [`messaging-patterns-overview.md`](./messaging-patterns-overview.md) — where orchestration
  fits relative to pure messaging/eventing.
- `glossary/README.md` — State Machine, Amazon States Language (ASL), Task Token, Saga Pattern.
