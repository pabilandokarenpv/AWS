# Domain 1: Development with AWS Services (30%)

![Modern serverless mobile/web application architecture using Cognito, AppSync, Lambda, DynamoDB, and ECS/Fargate.](https://docs.aws.amazon.com/reference-architecture-diagrams/latest/modern-serverless-mobile-web/images/modern-serverless-mobile-web.png)
*Source: [AWS Reference Architecture Diagrams — Modern Serverless Mobile/Web Application](https://docs.aws.amazon.com/reference-architecture-diagrams/latest/modern-serverless-mobile-web/modern-serverless-mobile-web.html). This is close to the canonical shape Domain 1 tests end to end: an identity layer, an API layer, compute, and a data layer, wired together with events.*

This is the biggest single domain on DVA-C03 — nearly a third of the exam. It's the "can you
actually write the application code" domain: calling AWS services from your code, writing Lambda
functions correctly, and picking/using the right data store. Everything in Domains 2-4 (security,
testing/deployment, troubleshooting) assumes you can already do what's in this domain. If you take
nothing else from this folder, take this: Domain 1 is about **application code that calls AWS
APIs correctly** — not about clicking through console wizards. Every exam question in this domain
is really asking "does the candidate know what the SDK call does, what it returns, and what
happens when it fails?"

## Task statements (verbatim from the exam guide)

**Task 1.1 — Develop code for applications hosted on AWS**
- Use AWS SDKs/APIs to interact with AWS services from application code
- Work with streaming data
- Serialize and deserialize data
- Build event-driven applications (EventBridge, S3 event notifications)
- Use API Gateway stages correctly (dev/test/prod promotion, stage variables)

**Task 1.2 — Develop code for AWS Lambda**
- Configure Lambda to access resources inside a VPC (private RDS, ElastiCache, etc.)
- Use Lambda layers to share code/dependencies across functions
- Manage concurrency (reserved, provisioned, account/region limits)
- Configure triggers (synchronous, asynchronous, poll-based event sources)

**Task 1.3 — Use data stores in application development**
- Choose and use DynamoDB, S3, and RDS/Aurora correctly from application code
- Understand access patterns (how you query/write, not just "what the service does")
- Understand consistency models (DynamoDB eventual vs strong, RDS/Aurora ACID transactions)
- Use the AWS SDK correctly against each (client config, retries, pagination, batching)

## Every task, mapped to a doc

| Task | What to read | Where |
|---|---|---|
| 1.1 — SDK/API calls, retries, pagination | AWS Lambda doc covers SDK-from-handler patterns; also see IAM for the credentials the SDK uses | [`services/compute/lambda.md`](../../../services/compute/lambda.md), [`services/security-identity-compliance/iam.md`](../../../services/security-identity-compliance/iam.md) |
| 1.1 — Streaming data | Kinesis family for stream ingestion patterns | [`services/analytics/kinesis-family.md`](../../../services/analytics/kinesis-family.md) |
| 1.1 — Event-driven apps (EventBridge, S3 events) | EventBridge is the central event bus; S3 event notifications are covered in the S3 doc | [`services/application-integration/eventbridge.md`](../../../services/application-integration/eventbridge.md), [`services/storage/s3.md`](../../../services/storage/s3.md) |
| 1.1 — Messaging/decoupling patterns feeding event-driven code | SQS/SNS/Step Functions patterns | [`services/application-integration/messaging-patterns-overview.md`](../../../services/application-integration/messaging-patterns-overview.md), [`services/application-integration/sqs.md`](../../../services/application-integration/sqs.md), [`services/application-integration/sns.md`](../../../services/application-integration/sns.md), [`services/application-integration/step-functions.md`](../../../services/application-integration/step-functions.md) |
| 1.1 — API Gateway stages | Stage variables, deployment promotion, throttling per stage | [`services/networking-content-delivery/api-gateway.md`](../../../services/networking-content-delivery/api-gateway.md) |
| 1.1 — GraphQL APIs (alternative to REST/HTTP APIs) | AppSync for managed GraphQL | [`services/application-integration/appsync.md`](../../../services/application-integration/appsync.md) |
| 1.2 — Lambda + VPC | Covered inside the Lambda doc's "VPC access" section | [`services/compute/lambda.md`](../../../services/compute/lambda.md) (see also [`services/networking-content-delivery/vpc.md`](../../../services/networking-content-delivery/vpc.md)) |
| 1.2 — Lambda layers, concurrency, triggers | Same doc — Lambda is a single deep-dive covering all of Task 1.2 | [`services/compute/lambda.md`](../../../services/compute/lambda.md) |
| 1.2 — Container-image Lambda packaging (alternative to zip) | [`services/containers/ecr.md`](../../../services/containers/ecr.md) for the image registry side | [`services/containers/ecr.md`](../../../services/containers/ecr.md) |
| 1.3 — DynamoDB access patterns & consistency | Full deep-dive including partition key design and consistency model | [`services/database/dynamodb.md`](../../../services/database/dynamodb.md) |
| 1.3 — S3 from application code | Object operations, consistency, multipart upload | [`services/storage/s3.md`](../../../services/storage/s3.md) |
| 1.3 — RDS/Aurora access patterns & ACID | [`services/database/rds.md`](../../../services/database/rds.md), [`services/database/aurora.md`](../../../services/database/aurora.md) |
| 1.3 — In-memory caching layered in front of a data store | [`services/database/elasticache.md`](../../../services/database/elasticache.md) |
| 1.3 — Choosing between data stores | Decision framework when a question gives you requirements instead of a service name | [`services/database/database-selection-guide.md`](../../../services/database/database-selection-guide.md) |
| Supporting — IAM credentials the SDK uses under the hood | [`services/security-identity-compliance/iam.md`](../../../services/security-identity-compliance/iam.md), [`services/security-identity-compliance/sts-and-role-switching.md`](../../../services/security-identity-compliance/sts-and-role-switching.md) |
| Supporting — observability hooks you'll want once this code ships | [`../domain-4-troubleshooting-optimization/observability-instrumentation.md`](../domain-4-troubleshooting-optimization/observability-instrumentation.md) |

## New in DVA-C03: AI-assisted development

Task 1.1 (and parts of Domains 3 and 4) now expect you to recognize AI coding assistants
(Amazon Q Developer, Kiro, GitHub Copilot-style tools) as part of the normal dev workflow —
code generation, code review, and later test generation and error analysis. This pattern repeats
across all four domains, so it gets one canonical doc here, cross-linked everywhere else:

➡️ **[`ai-assisted-development.md`](ai-assisted-development.md)** — code generation/review here in
Domain 1; also referenced from [Domain 2](../domain-2-security/README.md#ai-assisted-development-cross-link),
[Domain 3](../domain-3-testing-deployment/README.md#ai-assisted-development-cross-link), and
[Domain 4](../domain-4-troubleshooting-optimization/README.md#ai-assisted-development-cross-link).

## How it fits together: a Lambda + API Gateway + DynamoDB request

This is the single most common request shape tested in Domain 1 — a REST API backed by a
serverless function backed by a NoSQL table. Nearly every Task 1.1/1.2/1.3 concept shows up
somewhere in this flow.

```mermaid
sequenceDiagram
    participant C as Client (browser/app)
    participant APIGW as API Gateway (stage: prod)
    participant IAM as IAM (execution role)
    participant L as Lambda Function
    participant DDB as DynamoDB Table

    C->>APIGW: HTTPS request (e.g. POST /orders)
    APIGW->>APIGW: Apply stage config (throttling, stage variables, auth)
    APIGW->>L: Invoke (synchronous), pass event (headers, body, path params)
    L->>IAM: Assume execution role (at cold start)
    IAM-->>L: Temporary credentials
    L->>L: Deserialize JSON body into app objects
    L->>DDB: PutItem / Query (SDK call, signed with role creds)
    DDB-->>L: Response (consistent or eventually consistent read)
    L->>L: Serialize result back to JSON
    L-->>APIGW: Return response object (statusCode, body, headers)
    APIGW-->>C: HTTPS response
```

Step by step:
1. **Client calls API Gateway**, not Lambda directly — API Gateway is the front door, handling
   TLS termination, request validation, throttling, and routing.
2. **The stage matters** — the same API definition can have a `dev` stage and a `prod` stage with
   different throttle limits, different stage variables (e.g. which Lambda alias to call), and
   different deployment history. This is exactly Task 1.1's "use API Gateway stages correctly."
3. **API Gateway invokes Lambda synchronously** for a REST/HTTP API integration — the caller is
   waiting, so Lambda must respond within the configured timeout or API Gateway returns a 504.
4. **Lambda assumes its execution role via IAM** to get temporary credentials — this role, not the
   caller's identity, is what authorizes the DynamoDB call. Get the IAM policy wrong (missing
   `dynamodb:PutItem`) and the function fails with an `AccessDeniedException`, not a Lambda error.
5. **The handler deserializes the incoming JSON** into whatever objects the application code
   uses — Task 1.1's "serialize/deserialize data" skill.
6. **The SDK call to DynamoDB** uses the credentials from step 4. Whether the read is strongly or
   eventually consistent is a parameter you choose per-call — exam questions test whether you know
   which one a given scenario needs (e.g. "must read your own write immediately" → strong).
7. **The result is serialized back to JSON** and returned in the specific shape API Gateway's Lambda
   proxy integration expects (`statusCode`, `headers`, `body` as a string) — a very common exam trap
   is forgetting that `body` must be a JSON *string*, not a raw object.
8. **API Gateway relays the response** to the client, applying any configured response mapping.

## Event-driven alternative: S3 upload fan-out

Not every Domain 1 question is a synchronous API. The other half of Task 1.1 is event-driven,
asynchronous processing — and the exam loves mixing the two shapes in the same scenario to see if
you can tell a synchronous call apart from an asynchronous trigger.

```mermaid
flowchart LR
    U[User uploads file] -->|s3:ObjectCreated event| S3[S3 Bucket]
    S3 -->|event notification| EB[EventBridge]
    EB -->|rule: key prefix = uploads/| L1[Lambda: validate file]
    EB -->|rule: key prefix = exports/| L2[Lambda: notify downstream]
    L1 -->|on failure, after retries| DLQ[(SQS Dead-Letter Queue)]
    L1 -->|success| SNS[SNS Topic: fan-out]
    SNS --> SUB1[Email subscriber]
    SNS --> SUB2[SQS queue: audit log]
```

Step by step: an S3 object creation fires an event notification. Routing it straight to a single
Lambda function works for simple cases, but routing through **EventBridge** first lets you apply
multiple rules (different prefixes, different event types) to fan the same underlying event out to
several independent consumers without any of them needing to know about each other — this is the
decoupling Task 1.1 is testing when a scenario says "add a new consumer without changing existing
code." Lambda's **asynchronous invocation model** here means S3/EventBridge don't wait for a
response; if the function fails, Lambda retries automatically (default: twice) before routing the
event to a configured **dead-letter queue (DLQ)** or **on-failure destination** so the event isn't
silently lost. Know this distinction: synchronous invocations (API Gateway, direct SDK `Invoke`)
return the error to the *caller*; asynchronous invocations (S3, EventBridge, SNS) retry internally
and need an explicit DLQ/destination or failures disappear.

## Lambda triggers: three invocation models, one function

Task 1.2's "configure triggers" bullet is really asking you to recognize which of three invocation
models a given event source uses, because that changes how you must handle errors and concurrency.

```mermaid
flowchart TD
    subgraph SYNC["Synchronous"]
        APIGW[API Gateway] --> L1[Lambda]
        ALB[Application Load Balancer] --> L1
        DIRECT[SDK Invoke RequestResponse] --> L1
    end
    subgraph ASYNC["Asynchronous"]
        S3EV[S3 events] --> L2[Lambda]
        SNSEV[SNS] --> L2
        EBEV[EventBridge] --> L2
        L2 -->|retries exhausted| DLQ2[(DLQ / failure destination)]
    end
    subgraph POLL["Poll-based (event source mapping)"]
        SQSEV[SQS] --> ESM[Lambda polls on your behalf]
        KINESISEV[Kinesis Data Streams] --> ESM
        DDBSTREAM[DynamoDB Streams] --> ESM
        ESM --> L3[Lambda — batch of records]
        L3 -->|failed batch| REDRIVE[Retry whole batch / partial batch response]
    end
```

- **Synchronous**: the caller blocks for a response. Errors return directly to the caller; there's
  no Lambda-managed retry — if you want retry behavior, the *caller* must implement it (API Gateway
  doesn't retry a 5xx from Lambda automatically).
- **Asynchronous**: the event source hands the event to the Lambda service and moves on. Lambda
  itself retries (twice, by default) with a delay, then gives up and routes to a DLQ or configured
  failure destination if one exists — if neither exists, the event is dropped.
- **Poll-based (event source mapping)**: Lambda's own poller reads a batch of records from SQS,
  Kinesis, or DynamoDB Streams and invokes your function with the batch. A single bad record can
  block a whole batch unless you enable **partial batch response** (`ReportBatchItemFailures`) so
  only the failed items are retried/redriven instead of the entire batch repeating.

## Choosing a data store: the Task 1.3 decision tree

```mermaid
flowchart TD
    Q1{Need ACID transactions /\nmulti-table SQL joins?} -->|Yes| RDS[RDS / Aurora]
    Q1 -->|No| Q2{Storing files/blobs,\nnot structured records?}
    Q2 -->|Yes| S3DS[Amazon S3]
    Q2 -->|No| Q3{Access pattern is simple\nkey lookups at massive scale,\nlow predictable latency?}
    Q3 -->|Yes| Q4{Need microsecond reads\non top of an existing DB?}
    Q4 -->|Yes| DAX[DynamoDB + DAX cache]
    Q4 -->|No| DDBDS[DynamoDB]
    Q3 -->|No, relational + occasional\nheavy analytical queries| AuroraDS[Aurora — read replicas /\nAurora Serverless v2]
```

This is the single most commonly tested "pick the right service" decision in Domain 1. A scenario
that says "need joins across normalized tables, strict referential integrity" is RDS/Aurora every
time, no matter how fast the questioner claims the NoSQL alternative "could" be made to work.
Conversely, "single-digit-millisecond reads at effectively unbounded scale, access pattern is
always by a known key" is DynamoDB — trying to force that into RDS means either a sharding project
or a connection-pool bottleneck under load.

## Full worked case study: a flash-sale order API

**Requirement.** A retail client is launching a flash sale. They need an order-placement API that
can absorb a sudden 50x traffic spike for about 10 minutes, must never lose an accepted order even
if a downstream payment step is briefly unavailable, must return inventory-availability checks
with reads that are allowed to be a few hundred milliseconds stale (they explicitly do **not** need
a strongly consistent read on inventory count, just "close enough"), and must guarantee that a
confirmed order is never double-charged even if the client retries the request.

**Architecture.**

```mermaid
flowchart TD
    CLIENT[Shopper's browser] -->|POST /orders, idempotency key header| APIGW[API Gateway — prod stage]
    APIGW --> L1[Lambda: CreateOrder]
    L1 -->|check idempotency key| DDB1[(DynamoDB: IdempotencyKeys table)]
    L1 -->|eventually consistent read, OK per requirements| DDB2[(DynamoDB: Inventory table)]
    L1 -->|conditional PutItem, ConditionExpression=attribute_not_exists| DDB3[(DynamoDB: Orders table)]
    L1 -->|publish, do not wait for payment| EB[EventBridge: OrderPlaced event]
    EB --> L2[Lambda: ChargePayment]
    L2 -->|on failure, after retries| DLQ[(SQS DLQ: failed-payments)]
    L2 -->|success| EB2[EventBridge: PaymentSucceeded]
    L1 -.reserved concurrency cap.-> L1
    L2 -.provisioned concurrency, pre-warmed for the sale window.-> L2
```

**Why each choice:**
- **DynamoDB, not RDS, for Orders/Inventory/IdempotencyKeys.** The access pattern is simple key
  lookups at extreme, bursty scale — exactly Task 1.3's DynamoDB case. On-demand capacity mode
  (or provisioned with auto scaling pre-warmed before the sale) absorbs the 50x spike without a
  capacity-planning exercise, and DynamoDB has no connection-pool ceiling the way RDS does under a
  sudden burst of concurrent Lambda executions.
- **Eventually consistent reads for the inventory check, explicitly.** The requirement states
  "close enough" is fine — using `ConsistentRead=true` here would needlessly double the
  read-capacity cost for a guarantee the business doesn't need. This is a direct Task 1.3 consistency
  trade-off decision, not a default to blindly apply everywhere.
- **A conditional write (`ConditionExpression=attribute_not_exists(orderId)`) on the Orders table**
  combined with a client-supplied **idempotency key** stored in its own table is how "never
  double-charge on retry" is actually implemented — not a queue setting, not a Lambda setting, an
  application-level pattern using DynamoDB's conditional-write feature.
- **EventBridge decouples order placement from payment**, so a payment-service outage doesn't fail
  the customer-facing order request — the order is durably recorded first, and payment is charged
  asynchronously. If payment ultimately fails, the event lands in a DLQ for manual/automated
  reconciliation instead of silently vanishing — the "never lose an accepted order" requirement.
- **Reserved concurrency on `CreateOrder`** caps how many concurrent executions it can consume,
  protecting the rest of the account's Lambda concurrency pool from being starved during the spike.
  **Provisioned concurrency on `ChargePayment`**, pre-warmed ahead of the sale's known start time,
  eliminates cold-start latency on the function handling money — a case where paying for
  pre-warmed capacity is worth it precisely *because* the traffic spike is predictable in advance.
- **API Gateway's `prod` stage** fronts the whole thing with its own throttle limits, so a runaway
  client can't consume the account's entire Lambda concurrency budget on its own.

This single scenario, reworded, is one of the most common "design the right architecture" essay-style
questions on the real exam — know this pattern and you can answer a large fraction of Domain 1's
harder scenario questions by recognizing which piece of it is being tested.

## SDK patterns Task 1.1 actually tests: retries, pagination, batching

The exam guide's "use AWS SDKs/APIs" bullet sounds generic, but in practice it's testing three
specific code-level behaviors that show up constantly in both multiple-choice distractors and
"what's wrong with this code snippet" questions.

**Retries with exponential backoff.** Every AWS SDK retries throttling/5xx errors automatically,
but the *default* retry count and backoff strategy aren't always enough for a bursty workload:

```python
import boto3
from botocore.config import Config

config = Config(
    retries={"max_attempts": 10, "mode": "adaptive"}  # adaptive backs off faster under sustained throttling
)
ddb = boto3.client("dynamodb", config=config)
```

Exam angle: a scenario describing "intermittent `ProvisionedThroughputExceededException` under
load, and the application should retry with increasing delay instead of failing immediately" wants
you to recognize this is a *client configuration* fix (retry mode/count), not a request to raise
table capacity blindly — capacity and retry tuning are two separate levers.

**Pagination.** Nearly every AWS "list"/"scan"/"query" API caps how many items it returns per call
and gives back a continuation token — missing this is one of the most common real bugs in
candidate-written sample code:

```python
paginator = ddb.get_paginator("scan")
items = []
for page in paginator.paginate(TableName="Orders"):
    items.extend(page["Items"])  # without a paginator, you'd only ever see the first page
```

Exam angle: "a Scan only returns a subset of the table's items even though more match the filter" →
the code isn't following `LastEvaluatedKey`/using a paginator, not a service bug.

**Batching.** `PutItem`/`GetItem` one record at a time at scale wastes round trips; `BatchWriteItem`/
`BatchGetItem` (DynamoDB) or `PutRecords` (Kinesis) batch up to a per-call limit (DynamoDB: 25 items
per batch write, 100 per batch get) — and a batch call can **partially fail**, returning
`UnprocessedItems`/`UnprocessedRecords` that your code must retry, it won't raise an exception for
a partial failure the way a single-item call would.

## Serialization and streaming data, concretely

**Serialize/deserialize** (Task 1.1) in an AWS context almost always means: JSON in/out of a Lambda
handler (API Gateway proxy integration), and DynamoDB's own attribute-value wire format (every
value is wrapped, e.g. `{"S": "hello"}` for a string, `{"N": "42"}` for a number) when you use the
low-level `dynamodb` client instead of the higher-level `dynamodb.resource`/`DynamoDbEnhancedClient`
abstraction that hides the wrapping. A classic exam trap: code that works against the DynamoDB
*resource* API (plain Python/JS types) is pasted into a context expecting the low-level *client*
API (wrapped types) and fails — know that both exist and are not interchangeable without conversion.

**Streaming data** (Task 1.1) means Kinesis Data Streams in application code: a producer calls
`PutRecord`/`PutRecords` with a **partition key** that determines which shard a record lands on
(records with the same partition key always land on the same shard, preserving per-key order), and
a consumer either polls with the SDK directly (`GetRecords`, tracking a shard iterator manually) or
— far more commonly tested — lets a Lambda **event source mapping** poll on its behalf, delivering
batches of records per shard. The exam-relevant subtlety: a hot partition key (one key receiving a
disproportionate share of traffic) creates a hot shard, which throttles that one shard, which is
exactly the kind of DynamoDB-partition-key lesson from Task 1.3 showing up again in a different
service — AWS repeats this "even distribution of keys matters" idea across Kinesis, DynamoDB, and
(less directly) S3 key-prefix design, and the exam expects you to recognize it as one concept.

## Lambda concurrency, precisely

Task 1.2's "manage concurrency" bullet has three distinct knobs that get mixed up constantly:

| Knob | What it actually does | When to use it |
|---|---|---|
| **Unreserved account concurrency** | The shared pool every function draws from by default (account/region soft limit, default 1,000, raisable via support ticket) | The default — fine until one noisy function can starve the rest |
| **Reserved concurrency** | Caps (and guarantees) a specific number of concurrent executions *for one function*, carved out of the shared pool | Protect other functions from being starved by one noisy one; or deliberately throttle a function's downstream impact (e.g. never hit a legacy DB with more than N concurrent connections) |
| **Provisioned concurrency** | Pre-initializes a set number of execution environments so they're warm and ready — eliminates cold starts for that count | Latency-sensitive, predictable-traffic workloads (e.g. a payment function right before a known traffic spike) — costs money even when idle, unlike reserved concurrency which costs nothing extra by itself |

A classic wrong-answer pattern: a question describes a cold-start latency problem and the
distractor answer is "increase reserved concurrency." Reserved concurrency guarantees *capacity
exists*, it does not pre-warm anything — only provisioned concurrency fixes cold starts.

## Common exam scenarios

- *"A Lambda function needs to read from an RDS instance in a private subnet"* → Lambda must be
  attached to that VPC (ENI in the private subnet) with a security group allowing the DB port; add
  NAT if the function also needs internet access.
- *"Multiple Lambda functions share the same third-party SDK/dependency and you want to avoid
  duplicating it in every deployment package"* → Lambda layers.
- *"A burst of traffic is causing cold starts to hurt p99 latency on a latency-sensitive API"* →
  provisioned concurrency, not just reserved concurrency (reserved only caps/guarantees capacity,
  it doesn't pre-warm).
- *"An application must process an object immediately after it's uploaded to S3"* → S3 event
  notification → Lambda (or to SQS/SNS/EventBridge first if you need fan-out, retry buffering, or
  filtering before Lambda).
- *"You need an item read immediately after writing it to reflect the latest value, every time"* →
  DynamoDB strongly consistent read (`ConsistentRead=true`), at roughly double the read-capacity cost.
- *"An application needs multi-table joins and guaranteed ACID transactions across them"* → that's
  a relational workload → RDS/Aurora, not DynamoDB (DynamoDB transactions exist but are limited to
  25 items and don't do SQL joins).
- *"Decouple a producer and consumer so a traffic spike on one side doesn't overwhelm the other"* →
  SQS queue in between (buffer + backpressure), not a direct synchronous call.
- *"The exam scenario mentions Amazon Q suggesting code changes in the IDE, or reviewing a pull
  request"* → that's the AI-assisted development pattern — see
  [`ai-assisted-development.md`](ai-assisted-development.md).
- *"An asynchronously invoked Lambda function keeps failing and the events seem to disappear"* →
  no DLQ or on-failure destination was configured; async invocations retry twice, then drop the
  event unless one is set.
- *"One malformed record in an SQS batch is causing the entire batch to be retried forever"* → the
  function isn't using `ReportBatchItemFailures` (partial batch response) on the event source
  mapping — without it, one bad record fails the whole batch every time.
- *"The client may send the same `POST /orders` request twice due to a network retry, and it must
  not create two orders"* → idempotency key + a DynamoDB conditional write
  (`ConditionExpression=attribute_not_exists`), see the case study above.
- *"A mobile app needs a managed GraphQL API with real-time subscriptions instead of REST"* →
  AppSync, not API Gateway + Lambda for every field (AppSync resolvers call Lambda/DynamoDB/etc.
  per field/operation, but the API shape itself is GraphQL).
- *"A function needs microsecond-level read latency on a DynamoDB table that gets repeated reads of
  the same hot items"* → DynamoDB Accelerator (DAX) as a caching layer in front of DynamoDB, not a
  general-purpose cache like ElastiCache for this specific DynamoDB-shaped need.
- *"A high-throughput clickstream must be ingested and processed in near-real-time by multiple
  consumers independently"* → Kinesis Data Streams (multiple independent consumers read the same
  stream at their own pace) rather than SQS (a message is typically consumed once).
- *"A Lambda function's response to API Gateway is a 502 even though the function logs show it ran
  successfully"* → the returned object doesn't match the Lambda proxy integration's required shape
  (commonly: `body` wasn't serialized to a JSON string, or `statusCode` is missing/wrong type).

## Domain 1 study checklist

Before moving to Domain 2, make sure you can do all of the following without looking anything up:

- [ ] Write a Lambda handler that reads a JSON body from an API Gateway proxy event and returns a
      correctly shaped response (`statusCode`, `headers`, `body` as a string).
- [ ] Explain the difference between a synchronous, asynchronous, and poll-based Lambda trigger,
      and what happens to a failed invocation under each.
- [ ] Explain when to use `ConsistentRead=true` on DynamoDB and what it costs.
- [ ] Explain why RDS/Aurora wins over DynamoDB for a given scenario, and vice versa.
- [ ] Configure Lambda VPC access and know what breaks if the security group or route table is wrong.
- [ ] Describe reserved vs. provisioned concurrency and pick the right one for a cold-start question.
- [ ] Recognize an idempotent-write pattern (conditional expression + client-supplied idempotency key).
- [ ] Recognize when AI-assisted code generation/review is the pattern being tested (see
      [`ai-assisted-development.md`](ai-assisted-development.md)) vs. when it's a distractor.

## Labs

See [`labs.md`](labs.md) for hands-on Floci exercises covering this domain — now including the
idempotent-write and event-source-mapping patterns from the case study above.
