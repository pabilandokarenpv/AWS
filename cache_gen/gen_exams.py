#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator for DVA-C03 full mock exams 1 & 2."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "certifications/dva-c03/practice-questions/full-exams")

def L(suffix):
    return f"[`services/{suffix}`](../../../../services/{suffix})"

def D(suffix):
    return f"[`{suffix}`](../../{suffix})"

DOMAIN_NAMES = {
    1: "Domain 1 — Development with AWS Services",
    2: "Domain 2 — Security",
    3: "Domain 3 — Testing and Deployment",
    4: "Domain 4 — Troubleshooting and Optimization",
}

# =====================================================================
# EXAM 1
# =====================================================================
E1_D1 = [
dict(stem="""A payments service writes an order item to DynamoDB and later needs to update its `status`
field from `PENDING` to `SHIPPED`, but only if another process hasn't already moved it to
`CANCELLED` in the meantime. The current code does a plain `UpdateItem` call with no extra
parameters, and the team has seen orders incorrectly flip from `CANCELLED` back to `SHIPPED` under
race conditions. What should the developer add to the `UpdateItem` call to fix this?""",
multi=False,
options=[
"A `ProjectionExpression` limiting the call to only the `status` attribute.",
"A `ConditionExpression` such as `status <> :cancelled` so the update is rejected if the item has already moved to CANCELLED.",
"A second `GetItem` call immediately before `UpdateItem`, performed in the same application thread.",
"Strongly consistent reads (`ConsistentRead: true`) on the `UpdateItem` call.",
],
correct=[1],
explain="""A `ConditionExpression` makes the write conditional server-side — DynamoDB evaluates it
atomically against the item's current state and rejects the update (`ConditionalCheckFailedException`)
if the condition isn't met, which is exactly how to implement optimistic locking / safe state
transitions without a separate read-then-write race window.""",
wrong={
0: "`ProjectionExpression` only controls which attributes are returned by a read; it has no effect on write conditions.",
2: "A `GetItem` followed by a separate `UpdateItem` is a classic check-then-act race — another process can change the item between the two calls, which is the exact bug described.",
3: "`ConsistentRead` applies to read operations (`GetItem`/`Query`/`Scan`); `UpdateItem` is always strongly consistent on the item it writes, and this option doesn't exist as a parameter on `UpdateItem`.",
},
links=[L("database/dynamodb.md")]),

dict(stem="""A clickstream ingestion pipeline uses a Kinesis Data Stream with 20 shards. Three
separate applications need to independently read every record from the stream at their own pace:
a real-time fraud-detection Lambda, a batch analytics job, and a new dashboard that was just added
and is causing the fraud-detection Lambda's `GetRecords` calls to occasionally hit
`ReadProvisionedThroughputExceeded`. What is the best fix that lets all three consumers read
independently without throttling each other?""",
multi=False,
options=[
"Increase the number of shards until the throttling stops.",
"Switch all three consumers to enhanced fan-out, giving each consumer its own dedicated 2 MB/sec read throughput per shard instead of sharing the classic 2 MB/sec/shard pool.",
"Have the dashboard read from an SQS queue instead, fed by polling the stream on a cron schedule.",
"Combine all three consumers into a single Lambda function so there is only one reader.",
],
correct=[1],
explain="""Classic (shared-throughput) consumers all compete for the same 2 MB/sec-per-shard /
5 transactions-per-second read budget, so adding consumers increases contention. Enhanced fan-out
gives each registered consumer a dedicated 2 MB/sec pipe per shard pushed over HTTP/2, which is
precisely the feature for "multiple independent consumers reading the same stream without
throttling each other.\"""",
wrong={
0: "More shards raises overall throughput but doesn't fix shared-throughput contention between consumers on the shards that already exist; it also costs more and doesn't address the root cause.",
2: "Polling a stream on a schedule to feed a queue adds latency and defeats near-real-time consumption; it doesn't solve the throttling problem for the other two readers either.",
3: "Merging unrelated workloads (fraud detection vs. batch analytics) into one function violates separation of concerns and doesn't change the number of GetRecords calls needed overall.",
},
links=[L("analytics/kinesis-family.md")]),

dict(stem="""An API Gateway REST API uses Lambda proxy integration. A developer's Python handler
returns:
```python
return {
    "statusCode": 200,
    "headers": {"Content-Type": "application/json"},
    "body": {"orderId": "abc123", "total": 42.50}
}
```
Every client call fails with a generic `Internal Server Error`, even though CloudWatch Logs show
the handler ran to completion with no exceptions. What is wrong?""",
multi=False,
options=[
"The Lambda execution role is missing `execute-api:Invoke` permission.",
"`body` must be a JSON-encoded string (e.g. `json.dumps({...})`), not a raw Python dict — proxy integration passes `body` through to the client byte-for-byte.",
"`statusCode` must be passed as the string `\"200\"` rather than the integer `200`.",
"The `headers` dict must include `Access-Control-Allow-Origin` even for non-browser clients, or API Gateway rejects the response.",
],
correct=[1],
explain="""In Lambda proxy integration, the response contract requires `body` to already be a
serialized JSON string — API Gateway does not re-serialize it, it forwards the string as-is. A raw
dict there breaks the integration response contract and API Gateway surfaces that as a 500, even
though the Lambda invocation itself succeeded.""",
wrong={
0: "`execute-api:Invoke` governs who can call the API Gateway endpoint (resource-policy / IAM auth), not the Lambda function's own execution role, and a permissions problem would surface as 403, not a 500 after a successful Lambda run.",
2: "`statusCode` is expected as an integer in the proxy response shape; sending it as a string is not the documented contract and is not the bug here.",
3: "CORS headers are optional and only matter for browser-origin requests; their absence does not cause a 500.",
},
links=[L("networking-content-delivery/api-gateway.md"), D("domain-1-development/README.md")]),

dict(stem="""A Lambda function needs to query a private RDS instance that lives in a VPC with no
internet gateway. After deploying the function with VPC configuration attached, invocations now
time out when the function also tries to call `s3.get_object()` to fetch a config file from an S3
bucket, something that worked before the function was attached to the VPC. What is the most likely
cause and fix?""",
multi=False,
options=[
"Lambda functions cannot access S3 at all once placed in a VPC; move the config into environment variables instead.",
"The subnets have no route to the internet or an S3 gateway endpoint, so outbound HTTPS calls to the public S3 service endpoint have nowhere to go; add an S3 gateway VPC endpoint (or a NAT gateway) to the route table used by the Lambda's subnets.",
"The Lambda execution role is missing `s3:GetObject`; re-attach VPC config has nothing to do with it.",
"Increase the Lambda function's timeout setting so the S3 call has more time to complete.",
],
correct=[1],
explain="""Once a Lambda function is attached to a VPC, its network traffic — including calls to
AWS public-endpoint services like S3 — goes through that VPC's networking, not Lambda's own managed
network. If the private subnets have no NAT gateway and no S3 gateway VPC endpoint, outbound calls
to S3's public endpoint simply have no route and hang until timeout. Adding an S3 gateway endpoint
(free, and the standard pattern for this) or a NAT gateway restores connectivity.""",
wrong={
0: "Lambda in a VPC can reach S3 fine — it just needs a route, via a gateway endpoint or NAT — this isn't a hard limitation.",
2: "A missing IAM permission produces an `AccessDenied` exception immediately, not a network-level timeout; the symptom described is networking, not authorization.",
3: "Raising the timeout doesn't create a network path; the call will still never succeed because there is nowhere for the request to route.",
},
links=[L("compute/lambda.md"), L("networking-content-delivery/vpc.md")]),

dict(stem="""Five Lambda functions across a serverless application all need the same third-party
HTTP client library and a shared internal logging utility. The developer wants to avoid packaging
the same ~15 MB of dependencies into all five deployment packages and wants a single place to patch
the library version. What AWS feature solves this?""",
multi=False,
options=[
"AWS Lambda layers — publish the shared dependencies as a layer version and attach it to all five functions; each function's own package stays small.",
"Lambda function aliases pointing at a shared version.",
"A single Lambda function with five different handler entry points configured via environment variables.",
"Amazon EFS mounted read-write by each function, with the dependencies copied in at every cold start.",
],
correct=[0],
explain="""Lambda layers are built exactly for this: a .zip of shared code/dependencies, versioned
independently, extracted to `/opt` in every attached function's execution environment. Updating the
shared library means publishing a new layer version and pointing functions at it — no need to touch
or re-upload each function's own deployment package.""",
wrong={
1: "Aliases point at specific **versions of a single function**, they don't share code between different functions.",
2: "Collapsing five functions into one trades a packaging problem for a different design smell (loses independent scaling/permissions/memory tuning per responsibility) and isn't what the services offer natively for shared dependencies.",
3: "EFS can be used to share large assets, but copying dependencies in at every cold start adds latency and is not the purpose-built mechanism — layers solve this more directly and without a filesystem round-trip.",
},
links=[L("compute/lambda.md"), D("domain-1-development/README.md")]),

dict(stem="""A Lambda function processes orders and is invoked by API Gateway (synchronous). During
a flash sale, the account's overall concurrency limit is being exhausted by a completely unrelated,
lower-priority batch-processing function, causing the order function to be throttled with
`TooManyRequestsException`. What is the correct fix to protect the order function specifically?""",
multi=False,
options=[
"Set **reserved concurrency** on the order function so it always has a guaranteed, ring-fenced pool of concurrency that other functions in the account cannot consume.",
"Increase the batch function's memory allocation so it finishes faster and frees concurrency sooner.",
"Set the order function's timeout to the maximum (15 minutes) so it never gets throttled.",
"Delete the batch function's event source mapping and recreate it after the sale.",
],
correct=[0],
explain="""Reserved concurrency carves out (and caps) a specific slice of the account's total
concurrency pool exclusively for one function — both guaranteeing it a minimum available concurrency
and capping its maximum, so a burst elsewhere in the account can no longer starve it. This is the
standard Task 1.2 control for isolating one function's concurrency from the rest of the account.""",
wrong={
1: "Faster execution reduces concurrent invocations somewhat but doesn't guarantee capacity is available at the moment of the flash-sale spike — it's a mitigation, not a reservation.",
2: "Timeout controls how long a single invocation is allowed to run; it has no relationship to whether a request is throttled due to concurrency limits.",
3: "Removing the batch function's trigger is an operational sledgehammer that stops unrelated legitimate work rather than correctly partitioning concurrency.",
},
links=[L("compute/lambda.md")]),

dict(stem="""An image-processing Lambda is triggered by an SQS standard queue (event source
mapping, batch size 10). The team notices the same image is sometimes processed twice. The function
itself is idempotent-unsafe (processing twice corrupts output), and investigation shows the
function occasionally takes longer than the queue's visibility timeout to finish a batch. What
should be changed?""",
multi=False,
options=[
"Increase the queue's visibility timeout to comfortably exceed the function's maximum expected processing time for a batch (at least 6x the function timeout, per AWS guidance).",
"Switch the queue to SNS so messages are pushed instead of polled.",
"Reduce the Lambda batch size to 1 so visibility timeout no longer matters.",
"Delete messages from the queue manually inside the handler before processing them.",
],
correct=[0],
explain="""SQS standard queues are at-least-once delivery: if the consumer doesn't delete a message
before its visibility timeout expires, the message becomes visible again and can be redelivered —
including to a second concurrent Lambda invocation. AWS's documented guidance is to set the queue's
visibility timeout to at least 6x the function's timeout for event-source-mapped Lambda consumers,
so an in-flight batch isn't prematurely considered abandoned.""",
wrong={
1: "SNS doesn't buffer/queue messages for pull-based polling the way SQS does, and doesn't resolve a visibility-timeout/duplicate-processing problem — it's not a drop-in substitute here.",
2: "A batch size of 1 reduces blast radius per message but does not fix an undersized visibility timeout; the same message can still be redelivered if processing exceeds the timeout.",
3: "Lambda's SQS event source mapping manages deletion automatically on successful return; manually deleting mid-handler bypasses the error-handling/retry contract and isn't the documented fix for this symptom.",
},
links=[L("application-integration/sqs.md"), L("compute/lambda.md")]),

dict(stem="""A media application lets users upload video files that range from a few MB to over
10 GB directly to S3 from a browser using presigned URLs. Uploads larger than ~100 MB fail or are
unreliable on flaky mobile connections. What change improves reliability for large uploads?""",
multi=False,
options=[
"Use the S3 Multipart Upload API to split large files into parts uploaded independently (and resumably) in parallel, rather than a single `PutObject` call.",
"Switch the bucket's storage class to S3 Glacier Instant Retrieval before upload.",
"Increase the presigned URL's expiration time to 7 days.",
"Enable S3 Transfer Acceleration only, with no change to the upload API calls.",
],
correct=[0],
explain="""Multipart upload is the documented mechanism for large objects: it splits the object
into independently-uploaded parts (AWS recommends considering it above 100 MB), lets failed parts
be retried individually instead of restarting the whole transfer, and can upload parts in parallel
for throughput — directly fixing reliability on unstable connections for large files.""",
wrong={
1: "Storage class governs retrieval cost/latency after the object exists; it has no bearing on upload reliability or size handling.",
2: "A longer URL expiration affects how long the link is valid, not how resiliently the bytes are transferred — it doesn't fix partial-failure retries.",
3: "Transfer Acceleration speeds up transfer over Amazon's edge network but doesn't by itself add the resumable, per-part retry behavior that fixes reliability for very large single-stream uploads; it pairs with multipart upload rather than replacing it.",
},
links=[L("storage/s3.md")]),

dict(stem="""A table `Orders` has partition key `orderId`. A new requirement appears: look up all
orders for a given `customerId`, sorted by order date, without scanning the whole table. The table
is already live in production with existing items and access patterns that must keep working.
What's the correct way to add this access pattern?""",
multi=False,
options=[
"Add a Global Secondary Index (GSI) with partition key `customerId` and sort key `orderDate` — it can be created on an existing table without disrupting the existing key schema or current access patterns.",
"Change the table's partition key from `orderId` to `customerId`.",
"Add a Local Secondary Index (LSI) with partition key `customerId`.",
"Run a `Scan` with a `FilterExpression` on `customerId` for this access pattern.",
],
correct=[0],
explain="""A GSI has its own partition/sort key independent of the base table's key schema, can be
added at any time to an existing table, and is queried like a separate table-shaped index — exactly
the tool for adding a new query pattern after the table is already live.""",
wrong={
1: "A table's primary key schema is fixed at creation time and can't be changed afterward without recreating the table, which would break every existing access pattern.",
2: "An LSI must share the base table's partition key and can only be defined **at table creation time** — it cannot use a different partition key (`customerId` here) and cannot be added to an existing table.",
3: "A `Scan` with a filter reads the entire table and discards non-matching items, which is exactly the inefficient full-table-scan behavior the question is trying to avoid.",
},
links=[L("database/dynamodb.md")]),

dict(stem="""Choose **TWO** correct statements about building a highly available, read-scaled
relational database for an application with a global user base that also needs disaster recovery
across AWS Regions, using Amazon Aurora.""",
multi=True,
options=[
"Aurora Replicas within the same Region can serve read traffic and provide fast failover for the writer in case of failure.",
"Aurora Global Database replicates a primary cluster's data to secondary clusters in other Regions with typically sub-second replication lag, enabling fast regional disaster recovery.",
"Aurora requires manually configured binlog-based replication to create cross-Region read replicas.",
"Aurora Replicas can accept both read and write traffic simultaneously for true multi-master writes by default.",
"Cross-Region read replicas are only possible for Aurora PostgreSQL, never Aurora MySQL.",
],
correct=[0,1],
explain="""Aurora Replicas (up to 15) share the same underlying storage volume as the writer within
a Region, so they serve reads with minimal lag and can be promoted quickly if the writer fails.
Aurora Global Database extends this across Regions by replicating storage-layer changes to
secondary Region clusters with typically sub-second lag, specifically built for low-RPO/RTO
disaster recovery — the correct combination for \"read scaling in-Region + DR across Regions.\"""",
wrong={
2: "Aurora's native cross-Region replication (Global Database) is a managed feature, not something that requires the developer to hand-build binlog replication.",
3: "A regular Aurora cluster has exactly one writer at a time (plus up to 15 read replicas); true multi-writer is a separate, opt-in Aurora capability, not the default replica behavior.",
4: "Aurora Global Database is supported for both Aurora MySQL-compatible and Aurora PostgreSQL-compatible editions, not PostgreSQL only.",
},
links=[L("database/aurora.md"), L("database/database-selection-guide.md")]),

dict(stem="""An API Gateway REST API has three stages: `dev`, `test`, and `prod`. Each stage must
invoke a different Lambda function alias (`dev-alias`, `test-alias`, `prod-alias`) without
maintaining three separate API definitions or three separate integration configurations. What
feature accomplishes this cleanly?""",
multi=False,
options=[
"Stage variables — reference `${stageVariables.lambdaAlias}` in the integration's Lambda function ARN so each stage's own stage variable value resolves to the right alias at invoke time.",
"Create three entirely separate REST APIs, one per environment.",
"Hardcode three different Lambda ARNs in the integration and use a resource policy to pick one based on the caller's IP.",
"Use three different custom domain names that all point at the same single stage.",
],
correct=[0],
explain="""Stage variables are precisely this feature in API Gateway: a key/value pair scoped to a
stage that can be referenced inside the integration configuration (e.g. in the Lambda ARN used for
the integration), letting one API definition route each stage to a different backend — the
documented Task 1.1 pattern for dev/test/prod promotion without duplicating the API.""",
wrong={
1: "Separate APIs per environment duplicates the whole definition and configuration, exactly what the question says to avoid, and loses the single-source-of-truth benefit of stages.",
2: "Hardcoding ARNs defeats the purpose of having multiple stages share one integration, and resource policies filter by caller identity/IP, not by which stage was invoked.",
3: "A custom domain maps to a single stage (via a base path mapping); it doesn't change which Lambda alias a given stage's integration invokes.",
},
links=[L("networking-content-delivery/api-gateway.md"), D("domain-1-development/README.md")]),

dict(stem="""An order-processing system publishes an `OrderPlaced` event to an EventBridge custom
event bus. Three independent consumers exist: a shipping service that only cares about orders with
`region: \"US\"`, an email service that cares about all orders, and a fraud-review service that
only cares about orders over `$1000`. How should this be implemented so each consumer only receives
the events relevant to it, with no custom filtering logic inside the consumers themselves?""",
multi=False,
options=[
"Create one EventBridge rule per consumer, each with an event pattern matching the attributes that consumer cares about (e.g. `{\"detail\": {\"region\": [\"US\"]}}`), targeting only that consumer.",
"Publish three separate events (one tailored per consumer) from the order service every time an order is placed.",
"Use a single rule with no event pattern that targets all three consumers, and have each consumer filter in its own code.",
"Use SQS message attributes for filtering instead of EventBridge, since EventBridge does not support content-based filtering.",
],
correct=[0],
explain="""EventBridge rules support event patterns that match on the structure/values inside an
event's `detail` (and other fields), and each rule can target a different consumer — this is
exactly content-based routing/filtering done by the bus itself, so consumers never need to inspect
fields they don't care about or receive events irrelevant to them.""",
wrong={
1: "Making the producer aware of every consumer's filtering needs tightly couples the order service to downstream consumers, which event-driven architecture is meant to avoid.",
2: "A single unfiltered rule pushes every event to every target, contradicting \"only relevant events\" and pushing filtering logic back into consumer code — the opposite of what's asked.",
3: "EventBridge explicitly supports rich content-based event pattern matching on event `detail` fields; this option is factually wrong about EventBridge's capability.",
},
links=[L("application-integration/eventbridge.md"), L("application-integration/messaging-patterns-overview.md")]),

dict(stem="""A mobile app needs a GraphQL API backed directly by DynamoDB for simple CRUD
operations (get a user profile, list a user's posts) with minimal backend code to maintain. Which
approach avoids writing and deploying a separate Lambda function for every single resolver?""",
multi=False,
options=[
"AWS AppSync with a DynamoDB data source and a VTL (or JavaScript) resolver mapping template that talks to DynamoDB directly, with no Lambda in the middle for simple operations.",
"API Gateway with a Lambda proxy integration per GraphQL field.",
"AppSync configured to invoke one giant Lambda function per query, which then calls DynamoDB.",
"Amazon Cognito with a custom authentication Lambda trigger that also queries DynamoDB.",
],
correct=[0],
explain="""AppSync can attach a DynamoDB table as a direct data source and use a resolver mapping
template (VTL or APPSYNC_JS) to translate a GraphQL query straight into DynamoDB API calls
(`GetItem`, `Query`, `PutItem`, etc.) with zero custom compute to deploy or maintain for
straightforward CRUD resolvers — the documented "direct Lambda-less integration" pattern.""",
wrong={
1: "API Gateway doesn't natively speak GraphQL field resolution; this would require significant custom routing and still needs a Lambda per field, which is what the question wants to avoid.",
2: "Routing everything through one Lambda still requires writing and deploying that function and loses the no-code-resolver benefit AppSync's direct DynamoDB integration offers for simple operations.",
3: "Cognito handles authentication, not GraphQL query resolution — unrelated to this requirement.",
},
links=[L("application-integration/appsync.md")]),

dict(stem="""A Step Functions state machine orchestrates an order workflow: validate payment, reserve
inventory, ship order. The `ReserveInventory` Lambda task occasionally fails due to a transient
downstream throttle, and when it fails permanently the workflow must transition to a
`NotifyCustomerOfFailure` state instead of simply erroring out the whole execution. Which two state
machine fields implement "retry a few times, then gracefully handle the failure"?""",
multi=False,
options=[
"`Retry` (to retry the task a bounded number of times with backoff) and `Catch` (to route to a fallback state after retries are exhausted).",
"`Parallel` and `Map`.",
"`Choice` and `Wait`.",
"`TimeoutSeconds` alone, with no other fields.",
],
correct=[0],
explain="""`Retry` lets a state (or a specific error type) retry automatically with configurable
`IntervalSeconds`/`BackoffRate`/`MaxAttempts` before giving up, and `Catch` lets the state machine
route execution to a different state (e.g. a failure-notification branch) once retries are
exhausted or for errors `Retry` doesn't cover — together they implement exactly the "retry
transient errors, then gracefully handle a permanent one" pattern.""",
wrong={
1: "`Parallel` runs branches concurrently and `Map` iterates over a collection — neither relates to error handling/retry semantics.",
2: "`Choice` branches on data values and `Wait` pauses execution; neither implements retry-then-fallback error handling.",
3: "`TimeoutSeconds` only bounds how long a task is allowed to run before being treated as failed — it doesn't retry or route to a fallback state on its own.",
},
links=[L("application-integration/step-functions.md")]),

dict(stem="""Choose **TWO** correct statements about using Amazon ElastiCache to hold web session
data for a fleet of stateless EC2 instances behind a load balancer (sessions must survive across
requests landing on different instances, and some session keys need atomic increment operations).""",
multi=True,
options=[
"ElastiCache for Redis supports atomic operations like `INCR` and richer data structures (lists, hashes, sorted sets), making it a good fit when the app needs more than simple key/value get/set.",
"Because ElastiCache sits outside any individual EC2 instance, any instance can read a session written by another instance — this is what makes it suitable for sharing session state across a stateless fleet.",
"ElastiCache for Memcached supports built-in multi-AZ automatic failover with data replication, identical to Redis.",
"Sessions stored only in each EC2 instance's local memory would work equally well for a stateless, load-balanced fleet.",
"ElastiCache cannot be used for session storage; only DynamoDB supports this pattern.",
],
correct=[0,1],
explain="""Redis's richer data model (and atomic ops like `INCR`) handles counters and structured
session data cleanly, and because the cache is a separate, shared service reachable from every
instance, any instance behind the load balancer can read a session another instance wrote — which
is the core requirement for a stateless fleet (no sticky-session dependency on which instance
served a prior request).""",
wrong={
2: "Memcached does not provide built-in replication or automatic failover the way Redis does (via ElastiCache for Redis replication groups/Multi-AZ); this is a real, exam-relevant differentiator and this statement is false.",
3: "Local in-instance memory is private to that instance — a request landing on a different instance behind the load balancer wouldn't see it, which breaks the stateless-fleet requirement entirely.",
4: "DynamoDB can also store sessions, but ElastiCache is a fully valid (and lower-latency) option for this pattern too — this statement is simply false.",
},
links=[L("database/elasticache.md")]),

dict(stem="""A company ingests IoT sensor data and wants every record permanently and durably
delivered into S3 as compressed Parquet files for later Athena queries, with automatic batching
and no custom consumer code to write, poll, or operate. Which service is the best fit for the
delivery layer, as opposed to raw Kinesis Data Streams?""",
multi=False,
options=[
"Amazon Kinesis Data Firehose — a fully managed delivery service that batches, optionally transforms/converts format, and writes records to a destination like S3 automatically, with no consumer application to run.",
"Amazon Kinesis Data Streams alone, with a custom Lambda consumer that buffers records in memory and writes to S3 every 5 minutes.",
"Amazon SQS, polled by an EC2 fleet that batches messages into Parquet files.",
"AWS Step Functions, with a state machine invoked per record to write it to S3.",
],
correct=[0],
explain="""Firehose is purpose-built as a managed delivery pipe: point it at a destination (S3,
Redshift, OpenSearch, etc.), optionally enable format conversion to Parquet/ORC and compression,
and it handles batching, buffering, and retries with zero consumer code to operate — exactly "no
custom consumer, just deliver it" versus Kinesis Data Streams, which requires you to write and run
a consumer yourself.""",
wrong={
1: "This recreates Firehose's job by hand (custom buffering/consumer code to operate and keep highly available) — more operational burden for no benefit over using Firehose directly.",
2: "SQS has no native batching-to-S3-with-format-conversion capability; this would require significant custom code and infrastructure to operate.",
3: "Per-record Step Functions executions for high-volume IoT ingestion is both costly and the wrong tool — Step Functions orchestrates workflows, it isn't a streaming delivery pipe.",
},
links=[L("analytics/kinesis-family.md")]),

dict(stem="""A `Sessions` DynamoDB table stores user session items that should automatically
disappear 24 hours after creation, without any application code running a cleanup job. Which
DynamoDB feature should the developer use, and how?""",
multi=False,
options=[
"DynamoDB Time to Live (TTL) — set a Unix-epoch-seconds attribute (e.g. `expiresAt`) on each item and enable TTL on that attribute; DynamoDB automatically deletes expired items in the background at no extra write-capacity cost for the deletion.",
"A DynamoDB Stream that triggers a Lambda function to call `DeleteItem` on any item older than 24 hours, polling every minute.",
"A scheduled EventBridge rule that runs a full table `Scan` every hour, deleting items with an old timestamp.",
"Set the table's billing mode to on-demand, which automatically expires old items.",
],
correct=[0],
explain="""TTL is DynamoDB's native, no-code expiration mechanism: once an item's designated
TTL attribute (an epoch timestamp) is in the past, DynamoDB marks it for deletion and removes it in
the background, typically within 48 hours of expiration, without consuming write capacity for the
delete and without any application/cron logic required.""",
wrong={
1: "This reinvents TTL with custom polling code, added cost (RCU/WCU for scanning and explicit deletes), and operational burden, when a native zero-code feature already does exactly this.",
2: "A full-table `Scan` every hour is expensive (consumes read capacity proportional to table size) and exactly the pattern TTL exists to avoid.",
3: "Billing mode (provisioned vs. on-demand) controls capacity management, not item expiration — this option is factually incorrect.",
},
links=[L("database/dynamodb.md")]),

dict(stem="""An order-processing pipeline uses an SQS **FIFO** queue so that updates for the same
order are always processed in the order they were sent, and so that an accidental duplicate
`SendMessage` call (e.g. due to a client-side retry) doesn't create a second entry. Which two
message attributes/settings make this work?""",
multi=False,
options=[
"`MessageGroupId` set to the order ID (messages sharing a group are delivered in strict FIFO order) and either content-based deduplication or an explicit `MessageDeduplicationId` (to suppress duplicate sends within the 5-minute dedup interval).",
"`DelaySeconds` and `VisibilityTimeout` alone — these are sufficient for both ordering and deduplication on a FIFO queue.",
"Standard queue long polling with `ReceiveMessageWaitTimeSeconds` set to 20.",
"A Lambda function downstream that manually sorts messages by timestamp after receiving them out of order.",
],
correct=[0],
explain="""On a FIFO queue, `MessageGroupId` scopes strict ordering to messages sharing the same
group (e.g. all messages for one `orderId`), while deduplication — either automatic
content-based deduplication or a caller-supplied `MessageDeduplicationId` — causes SQS to silently
discard a second identical send within its 5-minute deduplication interval, satisfying both
"in order" and "no duplicates" requirements natively.""",
wrong={
1: "`DelaySeconds` postpones initial visibility and `VisibilityTimeout` governs in-flight redelivery; neither provides ordering guarantees or deduplication — those are FIFO-specific features, not these settings.",
2: "Long polling reduces empty-receive API calls/cost; it has no effect on message ordering or duplicate suppression, and standard queues don't guarantee strict order regardless.",
3: "Manually re-sorting after the fact works around a standard queue's lack of ordering rather than using the queue type built to guarantee it, and does nothing about duplicate messages.",
},
links=[L("application-integration/sqs.md")]),

dict(stem="""A public API Gateway endpoint accepts JSON order submissions. The team wants malformed
requests (missing required fields, wrong data types) rejected with a `400` **before** the request
ever reaches the backend Lambda function, to reduce unnecessary invocations and keep validation
logic out of application code. What should they configure?""",
multi=False,
options=[
"API Gateway request validation with a JSON Schema model attached to the method, so API Gateway itself checks the payload shape and required fields and rejects non-conforming requests at the gateway.",
"A Lambda authorizer that parses and validates the full request body.",
"VTL mapping templates that silently drop invalid fields and forward the rest to Lambda.",
"Increase the Lambda function's memory so it can validate requests faster.",
],
correct=[0],
explain="""API Gateway supports attaching a JSON Schema request model to a method and enabling
request validation (`validateRequestBody` / `validateRequestParameters`), which checks the incoming
payload against the schema and returns a `400 Bad Request` automatically — without invoking the
backend integration at all — exactly "reject bad input before the Lambda runs.\"""",
wrong={
1: "A Lambda authorizer's job is authentication/authorization (identity), not payload schema validation, and still involves invoking a Lambda function for every request.",
2: "Silently stripping fields changes the payload rather than rejecting it, and doesn't satisfy \"reject malformed requests with a 400.\"",
3: "Memory affects compute speed, not whether invalid requests are filtered before reaching the function at all.",
},
links=[L("networking-content-delivery/api-gateway.md")]),

dict(stem="""Choose **TWO** correct statements about using Amazon SNS to fan out a single
`PaymentReceived` notification to multiple SQS queues (one per downstream team), where each team's
queue should only receive messages for payments over $500 in their own region.""",
multi=True,
options=[
"SNS subscription filter policies can be attached per-subscription so each SQS queue only receives messages matching that subscription's filter policy (e.g. matching on message attributes like `amount` and `region`), even though all subscriptions point at the same topic.",
"Filtering happens on message **attributes**, not the message body, so the publisher should set relevant fields (like `amount`, `region`) as SNS message attributes, not bury them only in the JSON body.",
"SNS topics can only fan out to Lambda functions, never to SQS queues.",
"Filter policies are applied by the publisher before `Publish` is even called, not by SNS at delivery time.",
"Every subscriber to an SNS topic always receives every message published to that topic, with no way to narrow delivery per subscriber.",
],
correct=[0,1],
explain="""SNS subscription filter policies let each subscription declare which messages it wants
based on message attributes, and SNS evaluates that at delivery time per subscription — so the
same topic can fan out to many SQS queues (or other protocols) while each only gets the subset it
asked for, as long as the relevant data is published as **message attributes** (not just inside the
opaque message body) so SNS can evaluate it.""",
wrong={
2: "SNS fans out to many protocols including SQS, Lambda, HTTP(S), email, and mobile push — this statement is factually wrong.",
3: "Filter policies are evaluated by SNS at delivery time against each subscription, not something the publisher applies before calling `Publish`.",
4: "This describes default behavior with **no filter policy** attached; once a subscription has a filter policy, SNS narrows delivery to only matching messages for that subscription — so \"always every message, no way to narrow\" is false once filtering is used.",
},
links=[L("application-integration/sns.md"), L("application-integration/messaging-patterns-overview.md")]),
]

E1_D2 = [
dict(stem="""An IAM user has a policy attached that grants `s3:*` on `arn:aws:s3:::reports-bucket/*`.
A separate policy, attached to the same user by a different team for a compliance requirement,
explicitly denies `s3:DeleteObject` on all resources. The user calls `DeleteObject` on an object in
`reports-bucket`. What happens, and why?""",
multi=False,
options=[
"The call succeeds, because the Allow statement is more specific (bucket-scoped) than the Deny statement (account-wide).",
"The call is denied — an explicit Deny in any applicable policy always overrides any Allow, regardless of specificity or how many other policies grant access.",
"The call succeeds only if the Deny policy was attached after the Allow policy.",
"IAM evaluates policies in attachment order and only applies the last one attached.",
],
correct=[1],
explain="""IAM's policy evaluation logic is: explicit Deny always wins. Across every policy type
that applies to a request (identity-based, resource-based, permissions boundaries, SCPs), if any
statement explicitly denies the action, the request is denied — full stop — no matter how many
other statements allow it or how "specific" the Allow looks.""",
wrong={
0: "Specificity of the resource ARN does not create precedence over an explicit Deny; IAM has no such tie-breaking rule — Deny always wins regardless.",
2: "IAM evaluation doesn't depend on attachment order/recency; all applicable policies are evaluated together and any explicit Deny wins.",
3: "There is no \"last attached wins\" rule in IAM policy evaluation — this misunderstands the deny-by-default, explicit-deny-always-wins model entirely.",
},
links=[L("security-identity-compliance/iam.md")]),

dict(stem="""A SaaS vendor needs to let each of its customers' own AWS accounts assume a role in the
vendor's account to push data, without creating per-customer IAM users and without risking that one
customer could trick another customer's intermediary into assuming the vendor's role on their
behalf (the "confused deputy" problem). What should the trust policy include?""",
multi=False,
options=[
"A condition requiring a unique `sts:ExternalId` value (assigned per customer) in the `AssumeRole` call, checked against the value the vendor recorded for that specific customer.",
"A condition that only checks the calling principal's AWS account ID, with no external ID.",
"Granting `sts:AssumeRole` with `Resource: *` so any account can assume the role.",
"Requiring MFA on the customer's IAM user calling `AssumeRole`, with no external ID.",
],
correct=[0],
explain="""The `sts:ExternalId` condition is AWS's documented mitigation for the confused-deputy
problem in third-party cross-account role assumption: the vendor hands each customer a unique,
pre-agreed external ID, and the trust policy requires it to match on every `AssumeRole` call —
so even if a malicious third party convinces the vendor to call `AssumeRole` against a victim's
resource, it can't produce the victim's private external ID.""",
wrong={
1: "Account-ID-only trust narrows who can attempt the assumption but doesn't address the confused-deputy scenario where the *vendor itself* is tricked into acting on behalf of the wrong customer context — external ID is the documented fix for that specific pattern.",
2: "A wildcard resource/account trust defeats the purpose of restricting role assumption at all and is the opposite of a secure cross-account pattern.",
3: "MFA strengthens the customer's own authentication but does not solve the confused-deputy problem the external ID condition specifically addresses.",
},
links=[L("security-identity-compliance/sts-and-role-switching.md")]),

dict(stem="""A mobile app authenticates end users with email/password, then needs those authenticated
users to upload photos directly to S3 using temporary AWS credentials scoped to only their own
"folder" in the bucket, without routing the upload through a backend server. Which Cognito
construct issues these temporary AWS credentials after sign-in?""",
multi=False,
options=[
"A Cognito user pool alone — user pools can directly issue IAM credentials for AWS API calls.",
"A Cognito identity pool, federated with the Cognito user pool as an identity provider — the identity pool exchanges the user pool's ID token for temporary IAM credentials via STS, scoped by an IAM role mapped to the authenticated identity.",
"An IAM user created on the fly for each app user at sign-up.",
"API Gateway Lambda authorizer, which issues AWS credentials directly to the client.",
],
correct=[1],
explain="""User pools handle authentication (who the user is) and issue JWTs (ID/access/refresh
tokens) — they do not themselves grant AWS credentials. Identity pools are the piece that takes a
trusted identity (e.g. a user pool token) and calls STS to vend temporary, role-scoped IAM
credentials the client can use directly against AWS APIs like S3, which is exactly the
"authenticate, then get scoped temp AWS creds for direct S3 access" pattern.""",
wrong={
0: "User pools issue identity/authentication tokens (JWTs), not IAM credentials — they are not interchangeable with identity pools for this purpose.",
2: "Creating per-user IAM users is both an anti-pattern (IAM users aren't meant for this) and operationally unworkable at mobile-app scale with no automatic token exchange.",
3: "A Lambda authorizer evaluates whether to allow an API Gateway request; it does not vend AWS credentials to a mobile client for direct S3 access.",
},
links=[L("security-identity-compliance/cognito.md")]),

dict(stem="""A company with 40 AWS accounts organized under AWS Organizations wants developers to be
able to sign in once and switch between accounts they're authorized for, using a consistent set of
permissions (e.g. "Developer", "ReadOnly") defined centrally rather than recreating IAM roles by
hand in every account. What AWS feature is designed for this?""",
multi=False,
options=[
"AWS IAM Identity Center (successor to AWS SSO) with permission sets assigned to users/groups across accounts — permission sets define the permissions once and are provisioned as IAM roles into each assigned account automatically.",
"Create an identical IAM user in all 40 accounts with the same password.",
"A single IAM role in the Organizations management account that every developer assumes directly, regardless of which member account they need to work in.",
"Amazon Cognito user pools, one per AWS account.",
],
correct=[0],
explain="""IAM Identity Center is purpose-built for exactly this: centralized workforce identity,
single sign-on across the AWS Organization, and **permission sets** — a template of permissions
defined once and automatically provisioned as an IAM role in every account a user/group is assigned
to — avoiding hand-maintained, duplicated IAM roles per account.""",
wrong={
1: "Duplicating IAM users per account is exactly the manual, unscalable, insecure pattern IAM Identity Center exists to replace.",
2: "A single centrally-assumed role doesn't provide differentiated, per-account permission sets (Developer vs. ReadOnly) the way Identity Center's permission sets do, and doesn't match \"consistent but centrally defined\" per-account access.",
3: "Cognito user pools are for application end-user authentication, not workforce access to the AWS Management Console/CLI across an Organization.",
},
links=[L("security-identity-compliance/iam-identity-center-sso.md")]),

dict(stem="""A company must ensure that **no account** in its AWS Organization can ever launch
resources outside two approved Regions, even if an account administrator with full IAM
"AdministratorAccess" tries to do so. What is the correct control, and where is it enforced?""",
multi=False,
options=[
"A Service Control Policy (SCP) attached at the Organization or OU level, denying actions when `aws:RequestedRegion` is not one of the approved Regions — SCPs set the maximum permissions boundary for every principal in the account, which even a full-admin IAM policy cannot override.",
"An IAM policy with the same region condition, attached only in the accounts that need it.",
"A CloudWatch alarm that notifies security if a non-approved-Region resource is launched.",
"Removing the `AdministratorAccess` managed policy from all IAM roles.",
],
correct=[0],
explain="""SCPs are an Organizations-level guardrail that define the *maximum available*
permissions for every principal in affected accounts — they don't grant permissions, they cap them,
and they apply account-wide regardless of what IAM policies (including AdministratorAccess) say
inside the account. This is the only one of these options that actually constrains an
account admin, since IAM policies within an account can be bypassed/changed by that same admin.""",
wrong={
1: "An IAM policy can be edited, deleted, or bypassed by an account administrator with sufficient permissions — it cannot act as a guardrail that binds the administrator themselves.",
2: "A CloudWatch alarm is detective (notifies after the fact), not preventive — it doesn't stop the action from happening.",
3: "Removing a managed policy doesn't prevent an administrator from attaching permissions again, and doesn't scale as a durable, org-wide control the way an SCP does.",
},
links=[L("security-identity-compliance/organizations-and-scps.md")]),

dict(stem="""An Application Load Balancer needs a TLS certificate for `api.example.com` so the
application can terminate HTTPS at the load balancer. The certificate must auto-renew without the
team manually re-uploading a new certificate every year. What is the correct approach?""",
multi=False,
options=[
"Request a public certificate through AWS Certificate Manager (ACM), validate domain ownership via DNS validation (a CNAME record), and attach the ACM certificate ARN to the ALB's HTTPS listener — ACM manages renewal automatically as long as the validation record remains in place.",
"Generate a self-signed certificate and upload it to IAM's server certificate store, renewing it manually each year.",
"Use AWS KMS to issue a TLS certificate directly for the ALB listener.",
"Store the certificate's private key in Secrets Manager and have the ALB fetch it on every request.",
],
correct=[0],
explain="""ACM-issued public certificates used with integrated services (ALB, CloudFront, API
Gateway) are automatically renewed by ACM before expiry as long as the domain validation (DNS
CNAME, typically) stays valid — this is the whole point of using ACM instead of manually managed
certificates, and it directly fixes the "don't want to manually re-upload yearly" requirement.""",
wrong={
1: "Self-signed certs trigger browser trust warnings for a public API and still require fully manual renewal — the opposite of the automated goal.",
2: "KMS manages encryption keys, not TLS/X.509 certificate issuance for load balancer listeners — this is the wrong service.",
3: "ALB HTTPS listeners attach to a certificate (via ACM or IAM), they don't fetch raw private key material from Secrets Manager per request — this isn't how ALB TLS termination works.",
},
links=[L("security-identity-compliance/acm-and-private-ca.md")]),

dict(stem="""An application in Account A needs to read objects from an S3 bucket in Account B that
are encrypted with a KMS key owned by Account B. Account A's Lambda execution role already has
`s3:GetObject` granted via the bucket policy. The `GetObject` calls still fail with `AccessDenied`
related to KMS. What else is required?""",
multi=False,
options=[
"The KMS key policy in Account B must also grant Account A's Lambda execution role (or role ARN) `kms:Decrypt` permission — S3 bucket permissions and the KMS key's own resource policy/grants are evaluated separately, and both must allow the action.",
"Nothing else — S3 bucket policies automatically imply permission to use whatever KMS key encrypted the objects.",
"Account A must create its own copy of the same KMS key.",
"The objects must be re-uploaded unencrypted before Account A can read them.",
],
correct=[0],
explain="""Accessing an SSE-KMS encrypted object requires permission on *two* independent resources:
the S3 object/bucket (via bucket policy or IAM) **and** the KMS key used to encrypt it (via the
key's resource-based key policy, or a grant) — cross-account access needs the external principal
explicitly allowed in the key policy too, since IAM permissions in Account A alone cannot reach
into Account B's KMS key policy.""",
wrong={
1: "S3 permissions and KMS key permissions are enforced independently; having one does not imply the other, which is exactly why this `AccessDenied` is happening despite the bucket policy already allowing `GetObject`.",
2: "Creating a separate key in Account A would encrypt different data under a different key — it does nothing to grant decrypt rights to the *existing* objects encrypted under Account B's key.",
3: "Re-uploading unencrypted defeats the encryption-at-rest requirement and isn't a reasonable or correct fix for a permissions problem.",
},
links=[L("security-identity-compliance/kms.md"), L("storage/s3.md")]),

dict(stem="""An RDS database's master password needs to rotate automatically every 30 days without
any application downtime or manual password updates, and the connecting Lambda function should
always fetch the current password at runtime. Separately, a feature-flag config value (not
sensitive) needs to be read by the same function. Which combination is correct?""",
multi=False,
options=[
"AWS Secrets Manager for the RDS credential, using its built-in automatic rotation (with an AWS-provided or custom rotation Lambda) so the function always calls `GetSecretValue` for the current password; AWS Systems Manager Parameter Store (Standard, plaintext) for the non-sensitive feature flag.",
"Systems Manager Parameter Store `SecureString` for the RDS password, since it is cheaper, and Secrets Manager for the feature flag, since it is more fully featured.",
"Hardcode the RDS password as a Lambda environment variable and update it manually every 30 days.",
"Store both values in the same DynamoDB item with no encryption, since Lambda already has an execution role.",
],
correct=[0],
explain="""Secrets Manager's native strength over Parameter Store is built-in automatic *rotation*
with direct database integrations (RDS, Aurora, Redshift, DocumentDB) — exactly what's needed for a
rotating database password with zero app changes. Parameter Store is the right (and cheaper) choice
for ordinary, non-rotating configuration like a feature flag, which doesn't need rotation at all.""",
wrong={
1: "Parameter Store does not provide the managed automatic-rotation workflow Secrets Manager has for databases; using it for a rotating RDS credential loses that capability, and using Secrets Manager for a simple flag adds unnecessary cost/complexity.",
2: "Hardcoded environment variables require a function re-deploy on every rotation (causing exactly the \"manual update\" and downtime risk the requirement rules out) and leaks the secret into deployment artifacts/console views.",
3: "Storing unencrypted secrets in a general-purpose data store with no secret-specific access logging or rotation is not an acceptable secrets-management pattern.",
},
links=[L("security-identity-compliance/secrets-manager-vs-parameter-store.md")]),

dict(stem="""A company suspects an S3 bucket used for customer document uploads may contain
Social Security Numbers and credit card numbers that were never supposed to land there. They want
an automated, recurring scan across all buckets in the account to detect this kind of sensitive
data without writing custom detection logic. What should they use?""",
multi=False,
options=[
"Amazon Macie — it uses machine learning and pattern matching to automatically discover and classify sensitive data (PII, financial data, credentials) in S3 and can run scheduled, recurring discovery jobs.",
"Amazon GuardDuty, which scans S3 object contents for PII by default.",
"AWS Config, configured with a rule that reads the content of every S3 object.",
"AWS Trusted Advisor's security category.",
],
correct=[0],
explain="""Macie is purpose-built for exactly this: automated discovery and classification of
sensitive data in S3 (PII, credentials, financial data) using managed data identifiers, with the
ability to run one-off or recurring scheduled discovery jobs across one or many buckets — no custom
detection logic required.""",
wrong={
1: "GuardDuty is a threat-detection service analyzing account/network/API activity (e.g. CloudTrail, VPC Flow Logs, DNS logs) for malicious behavior — it does not scan S3 object content for PII; that's Macie's job.",
2: "AWS Config evaluates resource *configuration* against rules (e.g. \"is encryption enabled\"); it does not inspect the content of objects stored inside them.",
3: "Trusted Advisor gives best-practice checks (cost, security config, fault tolerance) — it does not perform content-level PII discovery inside objects.",
},
links=[L("security-identity-compliance/macie.md")]),

dict(stem="""Under the AWS Shared Responsibility Model, which of the following is the **customer's**
responsibility when running a web application on AWS Lambda?""",
multi=False,
options=[
"Patching the underlying operating system and the Lambda execution runtime environment's host infrastructure.",
"Writing IAM policies that follow least privilege for the function's execution role, and configuring encryption for any data the function reads or writes.",
"Physical security of the data center housing the Lambda compute fleet.",
"Patching the hypervisor layer that AWS uses to isolate Lambda execution environments.",
],
correct=[1],
explain="""With Lambda, AWS manages "security OF the cloud" — the underlying OS, host patching,
hypervisor, physical facilities, and the managed runtime environment itself. The customer is
responsible for "security IN the cloud": what their code does, how it's permissioned (IAM), what
data it handles and how that data is protected (encryption, secrets handling) — exactly Task 2.2's
scope for a serverless workload.""",
wrong={
0: "This is explicitly AWS's responsibility for managed/serverless compute like Lambda — the customer never patches the underlying host OS or runtime infrastructure.",
2: "Physical data center security is always AWS's responsibility across every service, never the customer's.",
3: "Hypervisor-layer isolation and patching is part of AWS's 'security OF the cloud' infrastructure management, not something a Lambda customer can or needs to touch.",
},
links=[L("security-identity-compliance/shared-responsibility-model-deep-dive.md")]),

dict(stem="""A public-facing API Gateway endpoint is being hit by a scripted client sending an
abnormally high volume of requests from a small set of IP addresses, degrading service for
legitimate users, but it isn't large enough to be a volumetric DDoS attack. What should be
configured to automatically block this pattern at the edge, before it reaches the API?""",
multi=False,
options=[
"An AWS WAF web ACL with a rate-based rule, associated with the API Gateway stage, that automatically blocks IP addresses exceeding a configured request-rate threshold within a rolling time window.",
"AWS Shield Advanced alone, with no WAF rule.",
"Increase the API Gateway account-level throttling limit so more requests can be processed.",
"Switch the API from REST to HTTP API type.",
],
correct=[0],
explain="""A WAF rate-based rule is exactly the documented mechanism for this: it tracks request
rate per originating IP over a rolling window and automatically blocks (or challenges) IPs that
exceed the configured threshold — ideal for application-layer abuse/scripted-client floods that
don't rise to the scale of a true volumetric DDoS.""",
wrong={
1: "Shield Advanced focuses on larger-scale network/transport-layer DDoS protection and cost protection; the specific 'block abusive IPs by request rate' control at the application layer is WAF's rate-based rule, which Shield Advanced is typically paired with rather than substituted for.",
2: "Raising the throttle limit lets more of the abusive traffic through to the backend rather than blocking it — the opposite of the desired outcome.",
3: "The REST vs. HTTP API Gateway type choice is about feature set/cost/latency, not a defense against abusive traffic volume.",
},
links=[L("security-identity-compliance/waf.md")]),

dict(stem="""Choose **TWO** correct statements about layering AWS Shield Advanced with AWS WAF to
protect a public API Gateway + Lambda application against DDoS attacks, where the team also wants
cost protection against charges incurred from a DDoS-driven usage spike.""",
multi=True,
options=[
"Shield Advanced provides enhanced protection against larger-scale network and transport layer (Layer 3/4) DDoS events and includes DDoS cost protection credits for scaling charges incurred during a declared attack.",
"WAF web ACLs provide application-layer (Layer 7) protections — rate-based rules, managed rule groups (e.g. SQL injection, known bad inputs) — that Shield Advanced does not provide on its own.",
"Shield Standard and Shield Advanced provide identical protections and pricing; there's no reason to pay for Advanced.",
"Enabling Shield Advanced automatically disables the need for any WAF rules, since Shield covers every OSI layer.",
"Shield Advanced can only be used with EC2, never with API Gateway or CloudFront.",
],
correct=[0,1],
explain="""Shield Advanced and WAF are complementary, not redundant: Shield Advanced strengthens
network/transport-layer DDoS resilience and adds cost protection for scaling charges during an
attack, while WAF handles application-layer (L7) rules like rate limiting and malicious-pattern
blocking that Shield doesn't itself implement — using both together is the standard DVA-C03
"defense in depth against DDoS" pattern.""",
wrong={
2: "Shield Standard (free, automatic) covers common, most-frequent network/transport DDoS patterns; Shield Advanced is a paid tier with additional detection, response team access (DRT), and cost protection — they are not identical.",
3: "Shield protects against volumetric/protocol attacks; it does not replace WAF's application-layer rule evaluation (e.g. SQL injection patterns, rate-based IP blocking) — both are typically used together.",
4: "Shield Advanced explicitly supports API Gateway, CloudFront, Global Accelerator, and ALB/NLB/EC2 with Elastic IPs — not EC2 only.",
},
links=[L("security-identity-compliance/shield.md"), L("security-identity-compliance/waf.md")]),

dict(stem="""Amazon GuardDuty raises a finding: `UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration`,
indicating an EC2 instance's credentials were used to make API calls from an unusual geographic
location shortly after also being used normally from inside the VPC. What is the most appropriate
immediate response, consistent with Task 4.1's root-cause workflow?""",
multi=False,
options=[
"Ignore it — GuardDuty findings are frequently false positives and don't require investigation.",
"Immediately rotate/invalidate the instance's credentials (e.g. by replacing the instance profile role's trust or terminating/replacing the instance), then use CloudTrail to review exactly which API calls that role made, from where, and over what time window, to scope the impact.",
"Delete the GuardDuty detector so the finding stops appearing in the console.",
"Wait for a scheduled quarterly security review to look into it.",
],
correct=[1],
explain="""This finding specifically indicates likely-stolen instance credentials being used outside
the expected context — the correct immediate action is containment (rotate/invalidate the exposed
credentials) paired with CloudTrail-driven root cause analysis (Task 4.1: "use CloudTrail to find
who/what made an API call") to determine exactly what the compromised credentials were used to do,
so the blast radius can be assessed and remediated.""",
wrong={
0: "This is a specific, named GuardDuty finding type for a serious credential-exfiltration pattern, not generic noise — treating it as a false positive by default risks missing an active compromise.",
2: "Deleting the detector hides the symptom rather than addressing the underlying compromised-credential incident, and loses future detection capability entirely.",
3: "Credential exfiltration is an active, time-sensitive security event — waiting for a scheduled review lets a live compromise continue unaddressed.",
},
links=[L("security-identity-compliance/guardduty.md"), L("management-governance/cloudtrail.md")]),

dict(stem="""An organization needs an immutable, tamper-evident audit trail of every management API
call made across all 15 of its AWS accounts and all Regions, retained centrally for compliance,
with log file integrity validation to prove logs haven't been altered after the fact. What should
be configured?""",
multi=False,
options=[
"A single multi-Region CloudTrail organization trail (created from the Organizations management account) delivering to a centralized, access-restricted S3 bucket, with log file validation enabled to generate digitally signed digest files.",
"A separate, independently configured CloudTrail trail in each of the 15 accounts, each writing to its own local bucket with no centralization.",
"CloudWatch Logs alone, with no CloudTrail, since CloudWatch already retains all API call history by default.",
"VPC Flow Logs, since they capture all account activity including console and API actions.",
],
correct=[0],
explain="""An AWS Organizations trail, enabled once from the management account and applied
org-wide, automatically covers every member account and (when configured multi-Region) every
Region, delivering to one centralized S3 destination — exactly the "single pane" compliance
requirement. Enabling log file validation adds SHA-256/RSA digest files AWS signs, so any
tampering with delivered log files becomes provably detectable, satisfying "tamper-evident.\"""",
wrong={
1: "15 independently managed trails create 15 places to audit, configure retention/permissions on, and reconcile — the opposite of a centralized compliance trail, and still needs validation enabled on each separately.",
2: "CloudWatch Logs do not capture AWS management/API-call history by default — that is specifically what CloudTrail records; CloudWatch is a destination CloudTrail can optionally stream *into*, not a replacement for it.",
3: "VPC Flow Logs capture IP traffic metadata at the network interface level — they do not record AWS API calls at all.",
},
links=[L("management-governance/cloudtrail.md")]),

dict(stem="""A chatbot application calls Amazon Bedrock's `InvokeModel` API using a Lambda function's
execution role. The role currently has the managed policy granting `"Action": "bedrock:*",
"Resource": "*"` attached, left over from initial development. A security review flags this under
Task 2.3. What should the policy be changed to?""",
multi=False,
options=[
"Scope the policy to only `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream` on the specific foundation model ARN(s) the chatbot is approved to use (e.g. one Claude model family ARN), removing management-plane Bedrock actions entirely from the runtime role.",
"Leave it as-is, since Bedrock has no sensitive management-plane actions worth restricting.",
"Replace `bedrock:*` with `s3:*` since the model's underlying weights are stored in S3.",
"Grant the same wildcard policy to every other Lambda function in the account as well, for consistency.",
],
correct=[0],
explain="""Task 2.3's access-control guidance for AI services is least-privilege exactly like any
other AWS API: a runtime application role should only get the specific invoke actions on the
specific model ARNs it's approved to call, never a `bedrock:*`/`Resource: *` wildcard — which
would also allow management-plane actions (creating custom models, modifying guardrails, deleting
resources) that a chatbot's runtime role has no legitimate need for.""",
wrong={
1: "Bedrock absolutely has sensitive management-plane actions (e.g. managing custom models, guardrails, provisioned throughput); a wildcard grants all of them to a role that should only ever invoke a model.",
2: "The model weights' own storage is managed internally by the Bedrock service, not something the caller's IAM policy needs S3 permissions for — this conflates two unrelated things.",
3: "Spreading an overly broad policy to more roles multiplies the security exposure rather than fixing it.",
},
links=[D("domain-2-security/ai-service-security-risks.md"), L("machine-learning-ai/bedrock.md")]),

dict(stem="""A healthcare company's application calls Amazon Bedrock from Lambda functions running
inside a VPC with no internet gateway or NAT, for compliance reasons requiring no public-internet
egress for any workload handling patient data. The calls currently fail because the subnets have no
route to Bedrock's public endpoint. What is the correct Task 2.3 fix?""",
multi=False,
options=[
"Create an interface VPC endpoint (AWS PrivateLink) for `bedrock-runtime` (and `bedrock-agent-runtime` if using agents) in the Lambda's VPC, with an endpoint policy restricting which principals/resources can use it, so traffic to Bedrock stays on the AWS private network.",
"Add a NAT gateway and an internet gateway so the subnet can reach Bedrock's public endpoint over the internet.",
"Disable the compliance requirement for this one workload since Bedrock cannot be reached privately.",
"Move the Lambda function out of the VPC entirely, since that is the only way to reach any AWS service.",
],
correct=[0],
explain="""This is precisely Task 2.3's "data privacy via VPC endpoints" bullet: a `bedrock-runtime`
interface VPC endpoint keeps Bedrock API traffic on AWS's private network path instead of transiting
the public internet, satisfying a no-public-egress compliance requirement while still allowing the
workload to call Bedrock — paired with an endpoint policy to further scope which roles/resources can
use that private path.""",
wrong={
1: "Adding internet access is the opposite of the no-public-egress compliance requirement; it reintroduces the exact exposure the control is meant to prevent.",
2: "Bedrock explicitly supports private connectivity via VPC endpoints — the compliance requirement does not need to be waived; this is a solvable, documented configuration.",
3: "Lambda functions can run outside a VPC and still reach public AWS endpoints by default, but that reintroduces public-internet egress, which fails the stated compliance requirement — the VPC endpoint is the fix that keeps the function private *and* compliant.",
},
links=[D("domain-2-security/ai-service-security-risks.md"), L("networking-content-delivery/vpc-endpoints-privatelink.md")]),

dict(stem="""Choose **TWO** correct Task 2.3 mitigations for a customer-facing Bedrock-powered
support chatbot that must (a) refuse to output harmful/toxic content and resist prompt-injection
attempts hidden in user messages, and (b) never let an attached Bedrock Agent take actions beyond
what the support use case requires, even if a malicious user tries to manipulate the agent into
calling an unintended tool.""",
multi=True,
options=[
"Configure Amazon Bedrock Guardrails with content filters and denied-topic/word policies, and apply them to both user input and model output, which also helps detect and block prompt-injection-style attempts to override the system instructions.",
"Scope the Bedrock Agent's own execution role to only the specific action groups/Lambda functions the support use case legitimately needs, following least privilege, rather than granting it a broad set of tools 'just in case.'",
"Trust the foundation model's own built-in judgment entirely and skip Guardrails, since modern models never fall for prompt injection.",
"Grant the Bedrock Agent `AdministratorAccess` so it never fails due to missing permissions during a demo.",
"Rely solely on client-side (browser) input filtering, since server-side filtering is redundant for a chatbot.",
],
correct=[0,1],
explain="""Guardrails are Bedrock's managed control for content filtering and prompt-injection
mitigation, applied at the service layer to both input and output; and scoping the Agent's own IAM
execution role to least privilege ensures that even a successfully manipulated agent still can't
exceed its intended toolset — these two controls together address both halves of Task 2.3's
"content filtering/prompt injection" and "AI agent security" bullets.""",
wrong={
2: "Foundation models remain susceptible to crafted prompt-injection inputs; skipping a dedicated guardrail layer is explicitly against documented best practice.",
3: "Granting a chatbot's agent `AdministratorAccess` is the textbook violation of least privilege for agent tool use and massively increases blast radius if the agent is manipulated.",
4: "Client-side filtering is trivially bypassed by any user calling the API directly; server-side enforcement (Guardrails) is required, not optional or redundant.",
},
links=[D("domain-2-security/ai-service-security-risks.md"), L("machine-learning-ai/bedrock.md")]),
]

E1_D3 = [
dict(stem="""A team manages a serverless application with a `template.yaml` written in AWS SAM.
Before every deployment, they want to catch structural errors (e.g. a Lambda function referencing
an IAM role that doesn't exist in the template, invalid resource properties) without actually
deploying anything to AWS. What command accomplishes this as an automated pre-deploy check in
CI/CD?""",
multi=False,
options=[
"`sam validate` (or `sam validate --lint` for deeper linting), run as a CI step before `sam deploy`, which parses and validates the template's structure and references without creating or changing any AWS resources.",
"`sam deploy --dry-run-only`, which does not exist as a flag but is assumed to work.",
"Manually read through the YAML file for syntax errors before every deployment.",
"`aws cloudformation delete-stack`, run first to confirm the stack doesn't already exist.",
],
correct=[0],
explain="""`sam validate` is exactly Task 3.2's "validate infrastructure templates before deploying
them" capability — it statically checks the SAM/CloudFormation template for syntax and structural
correctness, catching broken references and invalid properties in a CI pipeline stage with zero AWS
side effects, before any real deployment attempt.""",
wrong={
1: "This flag doesn't exist on the SAM CLI; `sam validate` is the actual documented command for this.",
2: "Manual review doesn't scale, isn't automatable in CI/CD, and misses the exact kind of structural/reference errors a validator catches reliably.",
3: "Deleting a stack has nothing to do with validating a template's correctness before deployment — this is an unrelated and destructive operation.",
},
links=[L("developer-tools/sam.md"), D("domain-3-testing-deployment/README.md")]),

dict(stem="""A Lambda function's dependencies (including a large machine-learning library) make
its deployment package exceed the 250 MB unzipped limit for .zip-based Lambda functions. The team
still wants to deploy on Lambda rather than move to a different compute service. What is the
correct fix?""",
multi=False,
options=[
"Package and deploy the function as a container image (up to 10 GB) stored in Amazon ECR instead of a .zip archive — Lambda supports container image packaging specifically for cases exceeding the zip size limits.",
"Split the single function into 10 smaller functions that each import a tenth of the library.",
"Ask AWS Support to manually raise the 250 MB limit for this one function.",
"Store the library in S3 and have the function download it on every invocation before running.",
],
correct=[0],
explain="""Lambda supports two packaging formats: .zip (capped at 250 MB unzipped) and container
images (up to 10 GB, built with the Lambda runtime interface client, stored in ECR) — exactly the
documented Task 3.1 escape hatch for large dependencies like ML libraries that blow past the zip
size limit, with no change needed to the invocation model or trigger configuration.""",
wrong={
1: "Arbitrarily splitting a function by which part of a library it imports usually isn't feasible (the library is typically used as a whole) and doesn't address the actual constraint cleanly.",
2: "The 250 MB unzipped limit for .zip deployment packages is a hard platform limit, not a per-function quota that can be raised via a support ticket.",
3: "Downloading a large library on every cold start adds significant latency and reliability risk compared to simply using the container image packaging format built for this case.",
},
links=[L("compute/lambda.md"), L("containers/ecr.md")]),

dict(stem="""A team deploys a new Lambda function version behind an alias used by API Gateway. They
want traffic to shift gradually — 10% to the new version, then the rest after 5 minutes if no
CloudWatch alarms fire — and to automatically roll back to the previous version if an alarm does
fire during the shift. What AWS feature implements this?""",
multi=False,
options=[
"AWS CodeDeploy for Lambda, using a canary deployment configuration (e.g. `Canary10Percent5Minutes`) with a CloudWatch alarm configured on the deployment group to trigger automatic rollback.",
"Manually updating the Lambda alias's weighted routing configuration every few minutes by hand and watching CloudWatch dashboards in a separate browser tab.",
"API Gateway stage variables alone, with no CodeDeploy involvement.",
"Lambda reserved concurrency, set to 10% of the function's normal value during deployment.",
],
correct=[0],
explain="""CodeDeploy natively supports Lambda deployments with built-in canary (and linear)
deployment configurations that automatically shift alias traffic in defined percentage/time
increments, and — critically — can be wired to CloudWatch alarms so that if an alarm goes into
ALARM state during the shift, CodeDeploy automatically rolls the alias back to the prior version
with no manual intervention.""",
wrong={
1: "Manual weight adjustment is exactly the error-prone, non-automated process CodeDeploy exists to replace, and provides no automatic rollback on alarm.",
2: "Stage variables route to an alias but have no concept of gradual percentage-based traffic shifting over time or alarm-triggered rollback — that orchestration is CodeDeploy's job.",
3: "Reserved concurrency caps how many concurrent executions a function can have; it does not implement weighted alias traffic shifting between two versions.",
},
links=[L("developer-tools/codedeploy.md"), L("compute/lambda.md")]),

dict(stem="""A CI/CD pipeline automatically deploys every merge to `main` straight to production with
no human review, and a recent bad deploy caused a customer-facing outage. The team wants to keep
full automation for build/test but require a human to explicitly approve the specific release
before it reaches the production stage, without reverting to manual deployments entirely. What
should be added to the pipeline?""",
multi=False,
options=[
"A manual approval action in AWS CodePipeline, placed as its own stage immediately before the production deployment stage, which pauses the pipeline until an authorized reviewer approves (or rejects) via the console, CLI, or SNS-notified link.",
"Remove the production stage from the pipeline entirely and deploy production manually outside of CodePipeline forever.",
"Add a `sleep 3600` step to the buildspec so there is a delay before deployment.",
"Require every commit to main to be signed with GPG.",
],
correct=[0],
explain="""CodePipeline's manual approval action is designed for precisely this: it pauses pipeline
execution at a defined point and waits for an explicit approve/reject decision from an authorized
principal before continuing — keeping build/test automated end-to-end while inserting exactly one
deliberate human gate before production, directly addressing Task 3.3's "AI-assisted deployment
approvals / human-in-the-loop gating" pattern in its general (human-gated) form.""",
wrong={
1: "Removing pipeline automation for production entirely throws away CI/CD's reliability and auditability benefits — overcorrecting far past what's needed.",
2: "A fixed sleep delay doesn't require or capture any human decision — it only adds latency, not a gate.",
3: "Commit signing verifies author identity, not that a human reviewed and approved this specific release going to production.",
},
links=[L("developer-tools/codepipeline.md"), D("domain-3-testing-deployment/README.md")]),

dict(stem="""An ECR repository accumulates thousands of old, untagged container images from CI
builds, most of which are never deployed and are only superseded by newer ones in the same
repository. The team wants these cleaned up automatically rather than manually deleting images,
while keeping the last 10 tagged `release-*` images indefinitely. What should they configure?""",
multi=False,
options=[
"An ECR lifecycle policy with rules that expire untagged images after a set number of days, and a separate rule that keeps only the most recent N images matching the `release-*` tag prefix.",
"Set the repository to private, which automatically purges old images after 30 days.",
"Manually run `aws ecr batch-delete-image` once a week via a person logging in to check.",
"Disable image tagging entirely so there's nothing to clean up.",
],
correct=[0],
explain="""ECR lifecycle policies are exactly the automated-cleanup mechanism for this: JSON rule
sets that match images by tag status/prefix/age/count and automatically expire ones that match,
letting the team both prune untagged build noise and preserve a bounded, named set of tagged
release images with zero manual intervention.""",
wrong={
1: "Repository visibility (private vs. public) is unrelated to image retention/expiration; there is no such automatic 30-day purge tied to privacy setting.",
2: "A weekly manual process is exactly the toil the question says to avoid and doesn't scale or stay consistent.",
3: "Disabling tagging would break the ability to reference specific release versions in deployments, which is the opposite of what's needed.",
},
links=[L("containers/ecr.md")]),

dict(stem="""A containerized service runs on Amazon ECS with the Fargate launch type behind an
Application Load Balancer. The team wants a blue/green deployment where a new task set is fully
provisioned and validated before any production traffic shifts to it, with the ability to roll back
instantly to the old task set if post-deployment validation fails. What should orchestrate this?""",
multi=False,
options=[
"AWS CodeDeploy configured for an ECS blue/green deployment, using two ALB target groups (one for the current/blue task set, one for the new/green task set) — CodeDeploy provisions the green set, reroutes the listener once healthy, and can roll back by rerouting back to blue.",
"A manual `aws ecs update-service --force-new-deployment`, which performs an in-place rolling update with no separate green environment.",
"Deleting the ECS service and recreating it from scratch for every release.",
"Switching the launch type from Fargate to EC2 to enable blue/green support, since Fargate doesn't support it.",
],
correct=[0],
explain="""CodeDeploy's ECS blue/green deployment type is built exactly for this: it stands up a
parallel "green" task set, validates it (optionally with lifecycle hooks running smoke tests),
then shifts the ALB listener's traffic from blue to green — with the old blue task set kept running
briefly so an instant rollback (rerouting the listener back) is possible if something's wrong.""",
wrong={
1: "A forced new rolling deployment replaces tasks in place without a separate parallel environment to validate first or instantly roll back to — it's a different (rolling) strategy, not blue/green.",
2: "Recreating the whole service from scratch causes downtime and discards the ability to keep the old version running for comparison/rollback — far more disruptive than necessary.",
3: "Fargate fully supports ECS blue/green deployments via CodeDeploy; this statement is factually incorrect.",
},
links=[L("containers/ecs.md"), L("developer-tools/codedeploy.md"), D("domain-3-testing-deployment/README.md")]),

dict(stem="""Before applying a CloudFormation stack update that modifies a production RDS instance's
engine version, the team wants to see exactly which resources will be added, modified (and whether
modification is in-place or requires replacement), or deleted — without actually applying the
update yet. What should they use?""",
multi=False,
options=[
"A CloudFormation change set — create one from the updated template, review the proposed resource-level changes (including replacement vs. in-place indicators), then execute it only if the preview looks correct.",
"`aws cloudformation delete-stack` followed immediately by `create-stack` with the new template.",
"Directly edit the resource in the RDS console, bypassing CloudFormation, then run `update-stack` afterward to \"sync\" the template.",
"Deploy the change directly to production first, then check the stack's event history afterward to see what happened.",
],
correct=[0],
explain="""Change sets are exactly CloudFormation's preview mechanism: they compute and display the
full diff of what an update would do — including whether each change is an in-place update or a
disruptive replacement (critical to know before touching a stateful resource like an RDS instance)
— without making any actual changes until the change set is explicitly executed.""",
wrong={
1: "Deleting and recreating a stack destroys the existing RDS instance and its data unless explicitly protected — a destructive, unacceptable approach to a routine engine version update.",
2: "Manually drifting a resource outside CloudFormation breaks the stack's state tracking (\"drift\") and isn't a preview mechanism at all — it actively creates an inconsistency to later resolve.",
3: "Checking after the fact is not a preview — the question asks to see the impact *before* applying the change, which only a change set provides.",
},
links=[L("management-governance/cloudformation.md")]),

dict(stem="""An application currently has a feature flag (`enableNewCheckout: true/false`) baked
into its deployment package as a config file, requiring a full redeploy to flip it. The team wants
to toggle the flag instantly in production, target it to a percentage of users for gradual rollout,
and automatically roll back the flag change if an associated CloudWatch alarm fires — all without
redeploying code. What service fits this?""",
multi=False,
options=[
"AWS AppConfig — define the flag as an externalized configuration profile, deploy configuration changes independently of code deployments, with built-in deployment strategies (gradual percentage rollout) and automatic rollback tied to a CloudWatch alarm.",
"Bake a new config file into the deployment package and redeploy every time the flag needs to change.",
"Store the flag in the Lambda function's code as a hardcoded boolean and redeploy to change it.",
"Use S3 Versioning alone, with the application polling a bucket object every request with no caching.",
],
correct=[0],
explain="""AppConfig is purpose-built for exactly this Task 3.1 "externalize configuration" pattern
taken further: it separates configuration deployment from code deployment entirely, supports
gradual percentage-based rollout strategies, and integrates with CloudWatch alarms to automatically
roll back a configuration deployment if the monitored alarm trips — all without touching the
application's deployment package.""",
wrong={
1: "Baking the flag into the deployable artifact is exactly the anti-pattern the requirement says to avoid (full redeploy needed just to flip a flag).",
2: "A hardcoded boolean in code is the least flexible option and still requires a full code redeploy to change — the opposite of \"instant toggle.\"",
3: "Raw S3 polling with no caching or deployment-strategy tooling reinvents (poorly) what AppConfig already provides managed, including rollout percentage and alarm-based rollback.",
},
links=[L("management-governance/systems-manager.md"), D("domain-3-testing-deployment/README.md")]),

dict(stem="""A developer wants to test a Lambda function's event-handling logic against a sample
S3 `ObjectCreated` event, entirely on their local machine, without deploying anything to AWS or
paying for any Lambda invocations, and also wants to simulate invoking it behind API Gateway
locally before pushing code. Which SAM CLI commands enable this?""",
multi=False,
options=[
"`sam local invoke` with a local JSON test event file to directly invoke the function handler locally in a Docker-simulated Lambda runtime, and `sam local start-api` to emulate API Gateway + Lambda proxy integration locally for interactive HTTP testing.",
"`sam deploy --stage local`, which creates a special \"local\" stage inside the real AWS account.",
"`aws lambda invoke` against a function that doesn't exist yet, since invoking a nonexistent ARN automatically creates it in a sandbox.",
"Manually copy the handler code into a Jupyter notebook and call the function directly, bypassing the Lambda runtime entirely.",
],
correct=[0],
explain="""`sam local invoke` and `sam local start-api` are exactly SAM's offline/local-testing
commands under Task 3.2's "use mock APIs and test events to exercise Lambda functions without live
dependencies": they run the function in a Docker container modeling the real Lambda execution
environment, accept local JSON test events, and can emulate the full API Gateway proxy-integration
HTTP surface for interactive testing — with zero real AWS resources touched or billed.""",
wrong={
1: "There's no \"local\" deployment stage that runs inside a real AWS account without creating real resources — `sam deploy` always provisions actual cloud resources.",
2: "Invoking a nonexistent Lambda ARN returns a `ResourceNotFoundException`; AWS does not auto-create functions on invoke.",
3: "Running handler code directly in a notebook skips the actual Lambda runtime environment/event contract entirely, so it doesn't validate the real integration behavior the way SAM's local emulation does.",
},
links=[L("developer-tools/sam.md"), D("domain-3-testing-deployment/README.md")]),

dict(stem="""A `buildspec.yml` for AWS CodeBuild needs to: install exact dependency versions from a
lockfile, run unit tests and fail the build if they don't pass, then zip the Lambda handler code
and dependencies into a deployable artifact for the next pipeline stage. Which `buildspec.yml`
phases map to these three responsibilities, in order?""",
multi=False,
options=[
"`install` (install dependencies from the lockfile), `build` (run unit tests — a non-zero exit fails the build automatically), `post_build` (package the artifact, e.g. `zip`), with the resulting file listed under `artifacts`.",
"`pre_build`, `pre_build`, `pre_build` — everything happens in a single phase for simplicity.",
"`artifacts`, `install`, `build` — artifacts must be declared first before any other phase runs.",
"There is no concept of ordered phases in CodeBuild; all commands in the file run in parallel.",
],
correct=[0],
explain="""CodeBuild's buildspec defines an ordered sequence of phases (`install`, `pre_build`,
`build`, `post_build`), each with a `commands` list run in sequence, and CodeBuild fails the overall
build if any command in a phase returns a non-zero exit code (which is exactly how a failing test
suite in the `build` phase stops the pipeline); the `artifacts` section then declares which output
files/paths get zipped up and handed to the next pipeline stage.""",
wrong={
1: "Collapsing everything into `pre_build` loses the documented separation of concerns and the implicit 'stop the build if build-phase commands fail' semantics associated with the `build` phase specifically for test runs.",
2: "`artifacts` is a top-level section describing output files, not a phase that executes commands, and it doesn't need to be declared before other phases run — order doesn't work that way.",
3: "Phases execute in a defined sequential order (`install` → `pre_build` → `build` → `post_build`), not in parallel — this option misstates how buildspec phases work.",
},
links=[L("developer-tools/codebuild.md")]),

dict(stem="""A team wants every pull request opened against their main branch to automatically
trigger a build-and-test run in CodeBuild, with the result (pass/fail) reported back as a status
check on the PR, before code review is considered complete — without merging the code first. Which
setup achieves this?""",
multi=False,
options=[
"Configure the source repository's pull-request webhook/events to trigger CodeBuild (directly, or via a CodePipeline source stage with webhook-based triggers) to run on PR creation/update, reporting build status back to the PR.",
"Only run CodeBuild after merge, on the main branch, and retroactively revert the merge if the build fails.",
"Have developers manually run the test suite locally and paste the output into the PR description.",
"Configure CodeBuild to run once per day on a fixed schedule, regardless of PR activity.",
],
correct=[0],
explain="""Both CodeBuild (via its own webhook-based triggers) and CodePipeline (via a source stage
with webhook filters for PR events) support triggering automatically on pull-request creation/update
and reporting the pass/fail result back to the PR as a status check — enforcing "tested before
merge" rather than "tested, and reverted if broken, after merge." """,
wrong={
1: "Testing only after merge means broken code was already merged to main before anyone found out — the opposite of a pre-merge quality gate.",
2: "Manual local runs pasted into a PR description are unverifiable, inconsistent, and not an automated CI gate.",
3: "A fixed daily schedule is decoupled from actual PR activity — a PR opened right after the daily run wouldn't get tested until the next day, failing the 'every PR' requirement.",
},
links=[L("developer-tools/codecommit.md"), L("developer-tools/codebuild.md")]),

dict(stem="""A CloudFormation stack update partially fails midway through (e.g. one resource's
update throws an error after three other resources were already successfully updated). By default,
what does CloudFormation do, and why does this matter for Task 3.3's "configure rollback"
requirement?""",
multi=False,
options=[
"CloudFormation automatically rolls the entire stack back to its last known-good state, undoing the already-applied changes, so the stack never sits in a half-updated, inconsistent state — this default behavior is why rollback doesn't need to be separately 'configured' for basic stack update failures.",
"CloudFormation leaves the three successfully updated resources in their new state and simply stops, leaving the stack permanently inconsistent until manually fixed.",
"CloudFormation deletes the entire stack and all its resources immediately on any update failure.",
"CloudFormation retries the failed resource indefinitely until it succeeds, blocking forever.",
],
correct=[0],
explain="""Automatic rollback on failure is CloudFormation's default stack update behavior
(`ROLLBACK_COMPLETE`/`UPDATE_ROLLBACK_COMPLETE`): if any resource fails to update, CloudFormation
reverts every resource it already changed back to the prior state, keeping the stack internally
consistent — which is why "rollback" for ordinary stack updates is a built-in safety net rather
than something the developer must explicitly wire up (unlike CodeDeploy's alarm-based rollback,
which is explicit configuration).""",
wrong={
1: "This describes the opposite of CloudFormation's actual default behavior — it does *not* leave partial changes in place; it rolls them back automatically.",
2: "A failed update does not delete the whole stack; rollback reverts to the previous good state, it doesn't tear down the stack itself.",
3: "CloudFormation does not retry indefinitely by default; it fails the update and initiates rollback rather than hanging forever.",
},
links=[L("management-governance/cloudformation.md")]),

dict(stem="""A team is choosing between Amazon EKS and Amazon ECS for a new containerized workload.
The deciding requirement is that the team already has significant in-house Kubernetes tooling,
Helm charts, and `kubectl`-based operational runbooks from workloads running elsewhere (e.g.
on-prem), and wants to reuse that tooling as-is, while still using Fargate so they don't manage EC2
instances. What should they choose?""",
multi=False,
options=[
"Amazon EKS with Fargate profiles — EKS exposes a standard, compliant Kubernetes API (so existing `kubectl`/Helm/K8s-native tooling works unmodified), and Fargate profiles let specific pods run on Fargate with no EC2 node management.",
"Amazon ECS with the Fargate launch type, since ECS also fully supports Helm charts and raw `kubectl` natively.",
"Amazon ECS with the EC2 launch type, since Fargate cannot be combined with Kubernetes-style tooling under any circumstances.",
"AWS Lambda, since both ECS and EKS are being deprecated in favor of pure serverless functions for containerized workloads.",
],
correct=[0],
explain="""EKS is the right choice specifically when existing investment is in the Kubernetes API
and its ecosystem (kubectl, Helm, K8s-native CI/CD and observability tooling) — that tooling only
works against a real Kubernetes control plane, which EKS provides, whereas ECS has its own
proprietary API/task definition model. Fargate profiles then let the team avoid managing EC2 nodes
for the specified pods/namespaces while staying on native Kubernetes.""",
wrong={
1: "ECS does not expose a Kubernetes API — Helm charts and `kubectl` do not work against ECS; it has an entirely separate task-definition/service model, so this statement is factually wrong.",
2: "This conflates two independent choices (launch type vs. orchestrator) and is also factually wrong — Fargate is fully compatible with EKS via Fargate profiles.",
3: "Neither ECS nor EKS is being deprecated, and Lambda is not a drop-in replacement for long-running, Kubernetes-API-dependent containerized workloads.",
},
links=[L("containers/eks.md"), L("containers/containers-vs-vms-vs-serverless.md")]),

dict(stem="""Before merging a new Lambda handler that processes refund requests, the team wants to
quickly generate a baseline set of unit tests covering typical inputs, edge cases (empty refund
amount, negative amount), and error paths, to accelerate Task 3.2 test coverage, then have a human
review and refine the generated tests before they're trusted as the real regression suite. Which
practice does this describe?""",
multi=False,
options=[
"AI-assisted test generation — using an AI coding assistant to draft an initial unit test suite from the handler's code/signature, which a developer then reviews, edits, and validates before it's relied upon as the authoritative regression suite.",
"Skipping unit tests entirely and relying only on manual QA in the `test` stage before promoting to `prod`.",
"Letting the AI-generated tests run in production directly with no review, since AI-generated code is assumed correct.",
"Writing the tests by hand with no tooling assistance, since AI should never be involved in testing.",
],
correct=[0],
explain="""This is explicitly Task 3.2's "AI-assisted test generation" item: an AI assistant
accelerates writing the first draft of a test suite (including edge cases a developer might not
think of immediately), but the documented pattern still requires human review before the generated
tests are trusted as the real regression baseline — AI drafts, a person verifies.""",
wrong={
1: "Skipping automated unit tests in favor of only manual QA is a regression in test coverage and automation, not what's being described or recommended.",
2: "Trusting AI-generated tests with zero human review risks subtly wrong assertions (tests that pass but don't actually validate correct behavior) — the documented practice always includes a review step.",
3: "The scenario is specifically about using AI assistance for a first draft, which this option incorrectly rules out entirely.",
},
links=[D("domain-1-development/ai-assisted-development.md"), D("domain-3-testing-deployment/README.md")]),
]

E1_D4 = [
dict(stem="""A production Lambda function started throwing intermittent `ProvisionedThroughputExceededException`
errors from DynamoDB about an hour ago, across thousands of log lines spread over dozens of log
streams. The developer needs to find the exact table name and the time window the errors started,
without manually opening each log stream. What is the fastest way to do this?""",
multi=False,
options=[
"Run a CloudWatch Logs Insights query against the function's log group filtering for `ProvisionedThroughputExceededException`, extracting the table name field and aggregating error counts by time bucket (e.g. `stats count() by bin(5m)`).",
"Download every log stream's raw text file and `grep` through them one at a time locally.",
"Increase the Lambda function's memory, which will make the error messages easier to read.",
"Disable logging temporarily so the error stops appearing.",
],
correct=[0],
explain="""CloudWatch Logs Insights is exactly the Task 4.1 tool for this: a purpose-built query
language that searches across every log stream in a log group at once, lets you filter on the
exact exception string, extract structured fields, and aggregate by time — turning "search
thousands of scattered log lines by hand" into a single query that returns the table name and the
exact time the error pattern started.""",
wrong={
1: "Manually downloading and grepping every stream doesn't scale across dozens of streams and is far slower than a single Logs Insights query over the whole log group.",
2: "Memory affects compute speed, not log readability, and has nothing to do with locating the error's source or timing.",
3: "Disabling logging removes visibility into the very problem being investigated — the opposite of useful troubleshooting.",
},
links=[L("management-governance/cloudwatch.md"), D("domain-4-troubleshooting-optimization/README.md")]),

dict(stem="""An API request traverses API Gateway → Lambda → RDS and takes 3.2 seconds end-to-end,
well above the SLA. AWS X-Ray is enabled with active tracing on the Lambda function. Looking at the
trace's service map and segment timeline, what is the correct way to identify exactly which part of
the call chain caused the slowdown?""",
multi=False,
options=[
"Open the trace timeline and compare the duration of each segment/subsegment (Lambda initialization, handler execution, and the RDS call captured via the X-Ray SDK's database client instrumentation) — the subsegment with the largest duration is where the time is actually being spent.",
"Assume the slowdown is always in API Gateway, since it's the entry point.",
"Only check CloudWatch Logs timestamps, since X-Ray cannot show per-call timing within a single invocation.",
"Re-run the request from a different Region and see if it's faster there.",
],
correct=[0],
explain="""X-Ray's value is exactly per-segment timing breakdown within a single request's trace:
with the SDK instrumenting outbound calls (e.g. wrapping the database client), the trace shows a
subsegment for the RDS call with its own duration, separate from Lambda init/handler overhead — so
comparing subsegment durations directly localizes the slow part of the chain (Task 4.1: "use X-Ray
to find *where* in a distributed call chain it happened").""",
wrong={
1: "Guessing based on position in the chain isn't root-cause analysis and is frequently wrong — the entry point is rarely the actual source of backend latency.",
2: "This is factually wrong — X-Ray's entire purpose is per-call, per-segment timing within a distributed request, which plain log timestamps don't cleanly reconstruct across services.",
3: "Testing from a different Region doesn't diagnose which component in *this* specific request's call chain is slow; it's an unrelated variable.",
},
links=[D("domain-4-troubleshooting-optimization/observability-instrumentation.md"), L("compute/lambda.md")]),

dict(stem="""A critical S3 bucket policy was unexpectedly modified overnight, removing a restriction
that previously blocked public access, and the security team needs to know exactly which IAM
principal made the change, from what source IP, and at what time, to investigate whether it was
authorized. Which service provides this information?""",
multi=False,
options=[
"AWS CloudTrail — search the event history (or a configured trail's delivered logs) for the `PutBucketPolicy` management event on that bucket, which records the calling principal's ARN, source IP, user agent, and exact timestamp.",
"Amazon CloudWatch Logs alone, since every AWS API call is written there automatically with no CloudTrail involved.",
"AWS Config, since it can tell you who made a change, not just what changed.",
"S3 Server Access Logs, which record every IAM principal's console actions by default.",
],
correct=[0],
explain="""CloudTrail is specifically the record of "who/what called which AWS API, from where, and
when" — exactly Task 4.1's "use CloudTrail to find who/what made an API call that caused it." A
`PutBucketPolicy` event in CloudTrail's event history includes the caller identity (user/role ARN),
source IP address, and timestamp needed to attribute and investigate the change.""",
wrong={
1: "CloudWatch Logs doesn't automatically capture AWS management API calls on its own; CloudTrail is the service that records API activity, and can optionally also stream into CloudWatch Logs.",
2: "AWS Config tracks *configuration state changes* and can show a resource's configuration timeline/drift, but the authoritative record of *who* made the API call (identity, source IP) is CloudTrail's job, and Config itself relies on CloudTrail-recorded events for some of this context.",
3: "S3 server access logs record *requests made to the bucket's objects* (data-plane access like GetObject), not management-plane IAM calls like changing the bucket policy — that's a CloudTrail management event.",
},
links=[L("management-governance/cloudtrail.md"), D("domain-4-troubleshooting-optimization/README.md")]),

dict(stem="""A Lambda function behind API Gateway has high p99 latency specifically on the first
request after a period of inactivity (cold start), while warm invocations are consistently fast.
The function is memory-constrained at 128 MB and does meaningful CPU-bound initialization work
(parsing a large configuration object) during the INIT phase. The team needs to both reduce cold
start impact for latency-sensitive traffic and speed up the init phase itself. What two changes
address this?""",
multi=False,
options=[
"Enable Provisioned Concurrency to keep a pool of initialized execution environments ready (eliminating cold starts for that pool), and separately increase the function's memory allocation, which proportionally increases allocated CPU and speeds up the CPU-bound initialization work itself.",
"Decrease the function's timeout setting, which directly reduces cold start duration.",
"Switch the function's trigger from API Gateway to an SQS queue, since SQS-triggered functions never experience cold starts.",
"Add more reserved concurrency, which makes individual cold starts faster.",
],
correct=[0],
explain="""These are two distinct, well-documented Task 4.3 levers: Provisioned Concurrency
pre-initializes a pool of execution environments so requests routed to that pool skip the cold
init phase entirely, while raising memory (which scales CPU/network proportionally in Lambda) 
directly speeds up CPU-bound work like parsing — including the init-phase work itself, independent
of whether an invocation is cold or warm.""",
wrong={
1: "Timeout only bounds how long an invocation is allowed to run before being killed; it has no effect on how fast initialization or execution actually happens.",
2: "Cold starts happen with any trigger type when a new execution environment must be created; switching triggers doesn't eliminate the underlying initialization cost.",
3: "Reserved concurrency guarantees/caps available concurrency; it does not change the speed of any individual invocation's cold start.",
},
links=[L("compute/lambda.md"), D("domain-4-troubleshooting-optimization/README.md")]),

dict(stem="""A payments service's error rate alarm fires frequently during normal, expected daily
traffic spikes (e.g. lunchtime), creating alert fatigue, because its static threshold doesn't
account for the workload's predictable daily/weekly seasonality. The team wants an alarm that
adapts its expected range to historical patterns rather than using one fixed number. What CloudWatch
feature should they use?""",
multi=False,
options=[
"CloudWatch anomaly detection — it models a metric's expected value as a band that adapts to historical trends and seasonality (e.g. daily/weekly cycles), and an anomaly detection alarm fires only when the metric falls **outside** that dynamically computed band, rather than crossing one static number.",
"A static threshold alarm set to the highest value ever observed, so it never fires.",
"Deleting the alarm entirely, since false positives are unavoidable.",
"A CloudWatch dashboard widget, which can itself trigger a page to on-call engineers.",
],
correct=[0],
explain="""Anomaly detection is exactly built for this: CloudWatch learns a metric's normal
seasonal/trend pattern over time and computes an expected range band, and an anomaly-detection
alarm triggers only on deviation from that adaptive band — directly solving "normal daily spikes
shouldn't alert, but a genuinely abnormal spike should.\"""",
wrong={
1: "Setting the threshold to the historical max defeats the point of alerting at all — it would also fail to catch real problems below that ceiling.",
2: "Removing the alarm loses all detection capability rather than fixing the false-positive rate — not a real fix.",
3: "Dashboards are visualization only; they don't evaluate conditions or trigger notifications on their own without an underlying alarm.",
},
links=[L("management-governance/cloudwatch.md")]),

dict(stem="""A team wants to emit a custom business metric (`OrdersProcessed`, dimensioned by
`region`) from inside a Lambda function's structured JSON logs, without making an extra
`cloudwatch:PutMetricData` API call on every invocation (to avoid added latency and API cost), while
still having the metric show up in CloudWatch Metrics for dashboards and alarms. What should they
use?""",
multi=False,
options=[
"Embedded Metric Format (EMF) — write a specially structured JSON log line (including a `_aws` metadata block defining metric names/namespaces/dimensions) using the CloudWatch Logs/Lambda Powertools EMF helper; CloudWatch Logs automatically extracts and publishes it as a real CloudWatch metric with no extra API call from the function.",
"Call `cloudwatch:PutMetricData` synchronously inside the handler for every invocation, awaiting the response before returning.",
"Write the metric value to a DynamoDB table and build a separate ETL job to copy it into CloudWatch nightly.",
"Store the metric in an environment variable that updates on every invocation.",
],
correct=[0],
explain="""EMF is specifically designed to solve this Task 4.2 "instrument code for observability"
problem: the application just logs a structured JSON line (which it was likely already doing
anyway), and CloudWatch Logs' EMF processing pipeline extracts the described metric straight into
CloudWatch Metrics — avoiding a dedicated synchronous `PutMetricData` call (and its added latency)
on the hot path entirely.""",
wrong={
1: "A synchronous `PutMetricData` call on every invocation adds latency and an extra billed API call per invocation — exactly what the requirement says to avoid.",
2: "Building a custom nightly ETL pipeline to backfill CloudWatch Metrics is far more complex and far less real-time than EMF's built-in log-to-metric extraction.",
3: "Environment variables are static per deployment and are not a mechanism for emitting a time-series metric value at all.",
},
links=[L("management-governance/cloudwatch.md"), D("domain-4-troubleshooting-optimization/observability-instrumentation.md")]),

dict(stem="""A compliance requirement states that every EBS volume in the account must be encrypted
at rest, but the team has discovered (after the fact) several unencrypted volumes that were created
by mistake weeks ago. They want continuous, automatic detection going forward — flagging any new
non-compliant volume the moment it's created — rather than periodic manual audits. What should they
configure?""",
multi=False,
options=[
"An AWS Config managed rule (e.g. `encrypted-volumes`) with the recorder enabled for EBS volumes — Config continuously evaluates resource configuration against the rule and flags any volume (new or existing) that drifts into non-compliance, close to real-time.",
"A CloudFormation stack policy that merely documents the encryption requirement in a README.",
"A one-time AWS CLI script run manually once a quarter to list unencrypted volumes.",
"S3 Object Lambda, since it can intercept and modify EBS volume configurations.",
],
correct=[0],
explain="""AWS Config is purpose-built for exactly this Task 4.2 "audit config drift" need:
managed or custom Config rules continuously evaluate live resource configuration (not periodic
exports) against a defined compliance rule and surface non-compliant resources essentially as soon
as they drift, which is the documented mechanism for ongoing automated compliance detection (and
can be paired with Systems Manager Automation to auto-remediate).""",
wrong={
1: "A stack policy documented in a README is not an enforced, automated detection mechanism — it's just documentation that's easy to ignore.",
2: "A quarterly manual script is periodic, not continuous, and reintroduces the exact 'weeks before anyone noticed' lag the requirement says to eliminate.",
3: "S3 Object Lambda intercepts S3 GET requests to transform object data; it has no relationship to EBS volume configuration at all.",
},
links=[L("management-governance/aws-config.md")]),

dict(stem="""A recurring incident requires restarting a stuck application service on a fleet of EC2
instances via SSH, which an on-call engineer currently does manually by logging into each instance.
The team wants this turned into a safe, auditable, one-click (or fully automatic, triggered by a
CloudWatch alarm) remediation that doesn't require SSH key distribution or opening inbound SSH
access. What should they use?""",
multi=False,
options=[
"AWS Systems Manager Automation, running a runbook (Automation document) that uses SSM Run Command / Agent (already on the instances, reachable without inbound SSH) to restart the service, triggerable manually or automatically from a CloudWatch alarm action.",
"Distribute the same SSH private key to every engineer and document the restart steps in a wiki page.",
"Open inbound SSH (port 22) from 0.0.0.0/0 to make it faster for any engineer to log in during an incident.",
"Have CloudWatch directly SSH into the instance and run the restart command itself.",
],
correct=[0],
explain="""Systems Manager Automation runbooks are exactly the documented Task 4.2 "automating
remediation/runbooks" mechanism: using the SSM Agent (no SSH, no key management, no inbound ports
needed) to execute a defined, auditable, repeatable set of actions — and Automation documents can
be invoked directly from a CloudWatch alarm action for fully automatic remediation, removing the
manual SSH step entirely.""",
wrong={
1: "Shared SSH keys are a major credential-management and audit-trail anti-pattern — no per-engineer attribution and a huge blast radius if the key leaks.",
2: "Opening SSH to the entire internet is a serious security regression that trades a minor convenience for a large new attack surface.",
3: "CloudWatch does not itself have an SSH client/remote-execution capability — alarm actions can invoke SSM Automation, Lambda, or SNS, not raw SSH.",
},
links=[L("management-governance/systems-manager.md")]),

dict(stem="""A DynamoDB table provisioned with fixed read/write capacity is throttling
(`ProvisionedThroughputExceededException`) during unpredictable traffic spikes that vary widely day
to day, and the team doesn't want to constantly hand-tune capacity numbers. What is the most
appropriate fix?""",
multi=False,
options=[
"Switch the table's billing mode to On-Demand (pay-per-request), which automatically scales to accommodate traffic without any capacity planning, or alternatively configure DynamoDB Auto Scaling on the provisioned table to adjust capacity within defined bounds based on utilization.",
"Add a Global Secondary Index, since GSIs automatically absorb all throttling from the base table.",
"Enable DynamoDB Streams, which increases the base table's throughput ceiling automatically.",
"Switch the table to use Strongly Consistent reads, which consume less capacity than eventually consistent reads.",
],
correct=[0],
explain="""On-Demand capacity mode (or Auto Scaling on a provisioned table) is exactly the
documented Task 4.3 cost/performance tradeoff answer for unpredictable, spiky traffic: On-Demand
removes capacity planning entirely at a higher per-request cost, while Auto Scaling adjusts
provisioned capacity automatically within configured min/max bounds — either removes the need for
manual capacity tuning that's currently causing throttling.""",
wrong={
1: "A GSI is a separate index with its own capacity and can itself throttle; it doesn't absorb or fix base-table throttling, and this option misstates how GSIs work.",
2: "DynamoDB Streams captures a change log of table activity; enabling it does not increase the table's provisioned throughput ceiling.",
3: "This is backwards — strongly consistent reads consume *more* read capacity than eventually consistent reads, not less, so this would make throttling worse, not better.",
},
links=[L("database/dynamodb.md"), D("domain-4-troubleshooting-optimization/README.md")]),

dict(stem="""A Lambda function's average duration is 2800 ms at 128 MB memory, costing a certain
amount per invocation. The team suspects that increasing memory (and therefore proportionally
allocated CPU) could make the function finish so much faster that total cost per invocation
actually goes **down**, despite the higher per-GB-second price, because duration drops more than
proportionally. What is the correct way to find the actual optimal memory setting rather than
guessing?""",
multi=False,
options=[
"Benchmark the function at multiple memory settings (e.g. using a tool like AWS Lambda Power Tuning, which runs the function at several memory values and plots duration vs. cost) and pick the memory value that minimizes actual billed cost (or best balances cost and latency) for this specific workload.",
"Always set every Lambda function to the maximum available memory (10,240 MB), since more memory is always cheaper.",
"Reduce the memory setting as low as possible, since memory is the dominant cost driver regardless of duration.",
"Assume CPU-bound functions and I/O-bound functions behave identically with respect to memory/duration tradeoffs.",
],
correct=[0],
explain="""Because Lambda cost is a function of both memory *and* duration, and duration doesn't
scale linearly with memory for every workload, the only reliable way to find the true
cost-optimal setting is to actually benchmark multiple memory values for the specific function
(exactly what the Power Tuning approach does) rather than assuming a universal rule — a CPU-bound
function may see large duration drops from more memory/CPU, while an I/O-bound function may not.""",
wrong={
1: "Maximum memory is not universally cheapest — for many functions duration improvements plateau well before 10,240 MB, so cost per invocation can rise again past the actual optimal point.",
2: "This ignores that duration is the other half of the cost equation; a workload whose duration drops sharply with more memory can end up cheaper overall at a higher memory setting, not lower.",
3: "CPU-bound and I/O-bound workloads respond very differently to added memory/CPU (I/O-bound code often sees little duration improvement) — this is precisely why benchmarking per-function matters instead of assuming one universal behavior.",
},
links=[L("compute/lambda.md"), D("domain-4-troubleshooting-optimization/README.md")]),

dict(stem="""API Gateway starts returning `503 Service Unavailable` to a subset of clients during a
traffic spike, while CloudWatch shows the Lambda function's `Throttles` metric spiking at the same
time and the function's concurrent executions metric flat-lining at its reserved concurrency limit.
What is the correct interpretation and fix?""",
multi=False,
options=[
"The Lambda function's reserved/account concurrency is being exhausted by the spike, so new invocation attempts are throttled (`TooManyRequestsException`), which API Gateway surfaces to clients as a 503 — raise the function's reserved concurrency (or account-level limit) or add a buffering layer (e.g. SQS) in front of it to smooth the burst.",
"The issue is unrelated to Lambda; API Gateway custom domain names cause 503s under any load regardless of backend health.",
"The fix is to disable X-Ray tracing, which is known to cause 503 errors under load.",
"The fix is to reduce the Lambda function's timeout to 1 second so it fails faster and frees capacity sooner.",
],
correct=[0],
explain="""The CloudWatch evidence directly ties the symptom to Lambda concurrency exhaustion:
flat-lined concurrent executions at the reserved limit plus a `Throttles` spike means new
invocations are being rejected, and API Gateway's Lambda proxy integration surfaces that backend
throttling as a 503 to the caller — the fix is raising the concurrency ceiling (reserved or account
limit) or decoupling the burst with a buffer (SQS) so Lambda scales consumption at its own pace.""",
wrong={
1: "Custom domain configuration is unrelated to backend throttling and doesn't explain the correlated Lambda `Throttles` metric spike shown in the evidence.",
2: "X-Ray tracing overhead is minor and not a documented cause of 503s; this doesn't match the concurrency-exhaustion evidence presented.",
3: "A shorter timeout makes each invocation fail faster but does not increase the number of concurrent invocations allowed — it doesn't address the actual concurrency ceiling being hit.",
},
links=[L("networking-content-delivery/api-gateway.md"), L("compute/lambda.md"), D("domain-4-troubleshooting-optimization/README.md")]),

dict(stem="""A monthly AWS bill review shows a large, steadily growing RDS instance that Cost
Explorer shows running at under 5% average CPU utilization for the last 90 days, alongside several
unattached EBS volumes left over from terminated instances. The team wants an automated, ongoing
set of recommendations flagging this kind of waste across the whole account, rather than manually
reviewing Cost Explorer every month. What should they use?""",
multi=False,
options=[
"AWS Trusted Advisor's cost optimization checks (e.g. low-utilization EC2/RDS instances, idle load balancers, unattached EBS volumes) — these run continuously and surface actionable, recurring recommendations without a manual monthly review.",
"AWS Budgets alerts alone, which only notify when a spending threshold is crossed, not which specific resources are underutilized.",
"Manually re-running the same Cost Explorer report every month and eyeballing the same trends by hand.",
"Deleting the RDS instance immediately with no further investigation, since any utilization under 100% is automatically waste.",
],
correct=[0],
explain="""Trusted Advisor's cost optimization category is exactly built for this recurring,
automated waste-detection need — flagging specific underutilized or idle resources (low-CPU RDS/EC2
instances, unattached EBS volumes, idle load balancers) on an ongoing basis, which is more targeted
and continuous than a manual monthly spend-trend review.""",
wrong={
1: "Budgets tells you *that* spend crossed a threshold, not *which specific resources* are the source of the waste — it's a complementary but different tool.",
2: "Manual monthly review is exactly the non-automated, easy-to-skip process the requirement wants replaced with a standing, automatic check.",
3: "Deleting a production database with no investigation into whether that CPU level is actually sufficient for its workload (or whether it's a read-replica serving a lighter but real purpose) is reckless; the right first step is review/right-sizing, not blind deletion.",
},
links=[L("management-governance/trusted-advisor.md"), L("management-governance/cost-management-tools.md")]),

dict(stem="""A read-heavy product-catalog API hits RDS directly for every request, and RDS CPU and
connection count are both consistently near their limits during peak hours even though most
catalog data changes only a few times a day. The team wants to reduce load on RDS for this
read-heavy, infrequently-changing data without rearchitecting the whole data model. What pattern
should they apply?""",
multi=False,
options=[
"A cache-aside pattern with Amazon ElastiCache in front of RDS: on a read, check the cache first; on a cache miss, read from RDS and populate the cache with a reasonable TTL; invalidate or update the cache entry when the underlying data changes.",
"Increase the RDS instance's storage size, since storage capacity is what's limiting read throughput.",
"Remove all indexes from the RDS tables to speed up writes, since writes are the real bottleneck.",
"Switch the API to use eventually-consistent DNS resolution, which reduces database load.",
],
correct=[0],
explain="""Cache-aside with ElastiCache is the textbook Task 4.3 optimization for exactly this
profile — read-heavy, infrequently-changing data causing a hot, saturated database: most reads get
served from cache (sub-millisecond, no DB round trip) and only cache misses or changed data touch
RDS, directly reducing CPU/connection pressure on the database for the majority of traffic.""",
wrong={
1: "Storage size affects capacity for data volume, not CPU/connection saturation from read query volume — it doesn't address the described bottleneck.",
2: "Removing indexes would typically make reads (and often even writes with complex queries) slower, not faster, and doesn't relate to the stated read-heavy bottleneck at all.",
3: "DNS resolution has no relationship to database read load; this option is a non-sequitur relative to the problem described.",
},
links=[L("database/elasticache.md"), D("domain-4-troubleshooting-optimization/README.md")]),

dict(stem="""After a production incident, an engineer pastes 40,000 lines of CloudWatch Logs and an
X-Ray trace export into an AI assistant and asks it to summarize the likely root cause before the
team's post-incident review. What is the correct way to treat the AI's output, consistent with
Task 4.1's "AI-assisted error analysis" guidance?""",
multi=False,
options=[
"Treat it as a fast first-pass hypothesis that accelerates triage, then have an engineer verify the suggested root cause against the actual logs/trace/metrics before it's written into the official incident report as the confirmed cause.",
"Copy the AI's summary verbatim into the official incident report as the final, confirmed root cause with no verification.",
"Ignore AI assistance entirely for incident analysis, since it is explicitly out of scope for DVA-C03.",
"Use the AI's summary to automatically close the incident ticket without any human reviewing it.",
],
correct=[0],
explain="""Exactly like AI-assisted test generation, Task 4.1's AI-assisted error analysis pattern
is "AI accelerates the first pass, a human verifies before it's trusted" — summarizing a large
volume of logs/traces into a likely cause narrows where to look fast, but the documented practice
still requires an engineer to confirm that hypothesis against the real evidence before it becomes
the record of what actually happened.""",
wrong={
1: "Treating unverified AI output as the final confirmed cause risks enshrining a plausible-sounding but wrong conclusion in the official record — verification is the documented step this skips.",
2: "AI-assisted error analysis is explicitly called out as in-scope content for DVA-C03's Task 4.1 — this option is factually wrong about exam scope.",
3: "Auto-closing an incident based on unverified AI output skips human confirmation entirely, which is the opposite of the documented safe pattern.",
},
links=[D("domain-4-troubleshooting-optimization/README.md"), D("domain-1-development/ai-assisted-development.md")]),
]

# =====================================================================
# EXAM 2
# =====================================================================
E2_D1 = [
dict(stem="""A DynamoDB table `Inventory` uses partition key `sku` and stores a `stockCount`
attribute. Multiple warehouse scanners increment `stockCount` concurrently as items arrive. Using a
plain `GetItem` followed by an application-side `stockCount + 1` and then `PutItem` occasionally
loses updates when two scanners process items at nearly the same moment. What single-call change
fixes this race condition cleanly?""",
multi=False,
options=[
"Use `UpdateItem` with an `ADD` (or `SET stockCount = stockCount + :incr`) update expression, which performs the increment atomically inside DynamoDB itself rather than reading, computing, and writing back in application code.",
"Read with `ConsistentRead: true` before writing, which alone prevents the race.",
"Have scanners write to a separate table per scanner and sum the tables nightly.",
"Add a `ProjectionExpression` restricting the write to only the `stockCount` attribute.",
],
correct=[0],
explain="""DynamoDB's `UpdateItem` with an atomic counter update (`ADD` or an arithmetic `SET`
expression) performs the read-modify-write entirely server-side as a single atomic operation, so
two concurrent increments from different scanners both land correctly instead of one overwriting
the other — this removes the check-then-act window inherent in a separate GetItem/PutItem pair.""",
wrong={
1: "Consistent reads guarantee you see the latest written value at read time, but the race is in the *gap* between read and write in application code — a consistent read doesn't close that gap by itself.",
2: "Splitting state across per-scanner tables adds significant complexity and a batch-reconciliation delay, when a single atomic update expression solves it immediately and simply.",
3: "`ProjectionExpression` only applies to reads, limiting which attributes are returned; it has no effect on write semantics or atomicity.",
},
links=[L("database/dynamodb.md")]),

dict(stem="""A video-processing pipeline ingests a Kinesis Data Stream with 8 shards. Traffic has
grown and the stream now regularly hits `WriteProvisionedThroughputExceededException` during peak
hours, while off-peak traffic fits comfortably within 8 shards. The team wants to increase write
throughput for peak periods without over-provisioning (and over-paying for) capacity during quiet
hours. What should they do?""",
multi=False,
options=[
"Enable Kinesis Data Streams On-Demand capacity mode, which automatically scales shard capacity up and down based on observed traffic, removing the need to manually reshard for predictable peak/off-peak cycles.",
"Permanently split every shard into two, doubling the shard count forever regardless of time of day.",
"Switch to a Standard SQS queue, which has unlimited throughput with no configuration needed.",
"Disable the stream's retention period to increase write throughput.",
],
correct=[0],
explain="""On-Demand mode for Kinesis Data Streams automatically scales the stream's capacity based
on observed throughput over the preceding 30 days, without the developer having to manually reshard
(split/merge shards) for predictable but varying peak/off-peak patterns — directly addressing
"handle peak throughput without permanently over-provisioning for off-peak" more simply than manual
provisioned-mode resharding.""",
wrong={
1: "Permanently doubling shard count fixes peak throughput but keeps paying for that doubled capacity during off-peak hours too — exactly the over-provisioning the team wants to avoid.",
2: "SQS is a different service with a different delivery model (queue, not an ordered replayable stream) and migrating to it is a far larger change than adjusting Kinesis capacity mode, and SQS Standard queues are also not literally unlimited in a way that requires zero configuration.",
3: "Retention period controls how long records remain available to replay; it has no relationship to write throughput capacity.",
},
links=[L("analytics/kinesis-family.md")]),

dict(stem="""An API Gateway REST API uses a **non-proxy (custom)** Lambda integration. The backend
Lambda returns `{"order": {"id": "123", "total": 42.5}}`, but the client needs the response shaped
as `{"orderId": "123", "amount": 42.5}` without modifying the Lambda function's code (it's shared
by other consumers that expect the original shape). What should the developer configure?""",
multi=False,
options=[
"An integration response mapping template (VTL) on the method, which transforms the Lambda's raw output into the client-facing shape before API Gateway returns it — exactly the use case for non-proxy integration's response mapping.",
"Switch to Lambda proxy integration, which automatically reshapes JSON for every client without any mapping template.",
"Ask every consuming client to parse the original shape themselves and ignore the requirement.",
"Add a second Lambda function that does nothing but rename two JSON fields, and chain it after the first via a Step Functions workflow for every single request.",
],
correct=[0],
explain="""This is precisely what non-proxy (custom) integration is for: a mapping template
(written in VTL) sits between the Lambda's raw return value and the client response, transforming
the shape as needed per-method — without touching the shared Lambda function's code or its other
consumers' expected contract.""",
wrong={
1: "Proxy integration passes the Lambda's response straight through unmodified (aside from the proxy response contract) — it does not reshape JSON; that transformation capability belongs to non-proxy mapping templates, which this scenario is already using.",
2: "Pushing the transformation requirement onto every client contradicts the stated goal of a single clean reshaping done once, and increases client-side complexity unnecessarily.",
3: "Adding a second Lambda and a Step Functions execution for a simple field rename is far more operational overhead and latency than a mapping template evaluated inline by API Gateway.",
},
links=[L("networking-content-delivery/api-gateway.md")]),

dict(stem="""A Lambda function needs to call a private RDS instance inside a VPC. After attaching
the function to the VPC's private subnets with no NAT gateway, the function can reach RDS fine, but
now fails when it also needs to call the Bedrock API, which has no VPC gateway endpoint equivalent
(interface endpoints only). What fixes the Bedrock connectivity without exposing the RDS-facing
subnet to the broader internet unnecessarily?""",
multi=False,
options=[
"Create an interface VPC endpoint for `bedrock-runtime` in the same subnets/route tables the Lambda function uses, so Bedrock traffic routes privately through the endpoint's ENI rather than needing internet access at all.",
"Add a NAT gateway and route 0.0.0.0/0 through it, granting the subnet full internet access just to reach Bedrock.",
"Give up on using Bedrock from this function and only call it from a different, public-subnet function instead.",
"Increase the Lambda function's timeout so the call to Bedrock eventually succeeds despite having no route.",
],
correct=[0],
explain="""Bedrock (like many AWS services) is reachable via an interface VPC endpoint
(PrivateLink), which creates ENIs inside the specified subnets that resolve the service's private
DNS name — this gives the Lambda function a private path to Bedrock without needing any internet
gateway/NAT at all, keeping the subnet fully private while still being functional, which is more
scoped than opening general internet egress just for one service call.""",
wrong={
1: "A NAT gateway solves connectivity but grants broad internet egress to resources that otherwise only needed to talk to RDS and one specific AWS API — more exposure than necessary when an interface endpoint solves it precisely.",
2: "Splitting the workload across a private function and a separate public-subnet function adds architectural complexity to work around a solvable connectivity gap.",
3: "There is no route to the destination at all without an endpoint or NAT; raising the timeout doesn't create a network path, so the call will still never succeed.",
},
links=[L("networking-content-delivery/vpc-endpoints-privatelink.md"), L("machine-learning-ai/bedrock.md")]),

dict(stem="""A Lambda layer published in Account A (`arn:aws:lambda:us-east-1:111122223333:layer:shared-utils:3`)
needs to be used by Lambda functions in Account B. The functions in Account B currently fail to
attach the layer with a permissions error. What must be configured in Account A to allow this?""",
multi=False,
options=[
"Add a layer-version resource-based permission (via `lambda:AddLayerVersionPermission`) granting Account B (or a specific principal in it) `lambda:GetLayerVersion` on that exact layer version ARN.",
"Nothing — Lambda layers are public by default across all AWS accounts once published.",
"Copy the entire layer's .zip contents manually into Account B's own S3 bucket and re-publish it as an identical layer there, since cross-account layer sharing isn't supported at all.",
"Grant Account B's functions `lambda:*` in Account A's IAM policies.",
],
correct=[0],
explain="""Cross-account layer sharing uses the layer version's own resource-based policy
(distinct from the function's execution role's identity-based IAM policy): the layer owner grants
a specific account (or principal) `lambda:GetLayerVersion` permission on a specific layer version
ARN, after which a function in the granted account can reference that exact ARN when attaching
layers — each layer version's permission must be granted individually.""",
wrong={
1: "Layers are private to the owning account by default; cross-account use requires an explicit resource-based permission grant, not an automatic public default.",
2: "Cross-account layer sharing is explicitly supported via resource-based permissions on the layer version; re-publishing a duplicate copy is unnecessary extra work and loses version parity with the source.",
3: "`lambda:*` IAM permissions in Account A don't grant Account B's principals anything — IAM policies in Account A only govern principals that can be evaluated against Account A's own policies, not resource-based cross-account layer access, which needs the layer's own resource policy.",
},
links=[L("compute/lambda.md")]),

dict(stem="""A Lambda function configured with provisioned concurrency of 20 is deployed with a new
version during a release. Traffic is currently routed to the alias pointing at the previous
version. What happens to provisioned concurrency during this deployment, and what should the team
configure to avoid a gap in pre-warmed capacity?""",
multi=False,
options=[
"Provisioned concurrency is tied to a specific published version (or an alias pointing at one); the team should configure provisioned concurrency on the alias itself (or use CodeDeploy's traffic-shifting with pre-provisioning) so the new version has its own warmed pool ready before traffic shifts, avoiding a gap where the new version briefly serves only cold-started invocations.",
"Provisioned concurrency automatically transfers itself to whatever the newest published version is, with no configuration needed.",
"Provisioned concurrency only applies to the `$LATEST` version and is irrelevant to aliases entirely.",
"Nothing needs to change — reserved concurrency and provisioned concurrency are the same setting and move together automatically.",
],
correct=[0],
explain="""Provisioned concurrency is explicitly configured per function version (directly, or via
an alias pointing to that version) — it does not automatically "follow" a new version. The
documented pattern for safe deploys is to provision concurrency on the new version ahead of the
traffic shift (e.g. CodeDeploy supports pre-provisioning during a canary/linear deployment) so
warmed capacity exists before real traffic arrives at the new version.""",
wrong={
1: "This is false — provisioned concurrency must be explicitly configured on a version or alias; it does not automatically migrate to new versions on publish.",
2: "Provisioned concurrency can be configured on `$LATEST` (unqualified ARN) or on a published version/alias; aliases are a standard, commonly used target for it, especially for blue/green-style promotions.",
3: "Reserved concurrency (an account-level allocation cap/floor) and provisioned concurrency (pre-initialized, warmed execution environments) are distinct settings that serve different purposes, despite the similar names.",
},
links=[L("compute/lambda.md")]),

dict(stem="""A document-processing Lambda is triggered by an SQS queue with event source mapping. A
specific malformed message consistently causes the handler to throw an exception on every delivery
attempt, and because the queue's redrive policy has no dead-letter queue configured, the same
message keeps cycling back after each visibility timeout, consuming Lambda invocations indefinitely
and blocking the processing of other, valid messages in the same batch. What should be configured?""",
multi=False,
options=[
"Configure a redrive policy on the source queue pointing at a dead-letter queue (DLQ), with `maxReceiveCount` set so that after N failed delivery attempts, SQS automatically moves the poison message to the DLQ instead of redelivering it forever — freeing the main queue (and batches) from being blocked by it.",
"Increase the Lambda function's memory, which will make the malformed message parse correctly.",
"Delete the entire queue and recreate it, which will discard the poison message along with every other valid message currently queued.",
"Set the queue's visibility timeout to 0 so the message is never considered in-flight.",
],
correct=[0],
explain="""A DLQ with `maxReceiveCount` is the documented poison-message handling pattern for
SQS-triggered Lambda: once a message has failed processing the configured number of times, SQS
redirects it to the DLQ automatically instead of endlessly recycling it back onto the main queue —
unblocking batches (since, depending on batch item failure reporting, a persistently failing
message no longer keeps forcing retries of the whole batch) and giving the team a place to inspect
the bad message later.""",
wrong={
1: "Memory affects compute resources, not whether a specific message's content is malformed and causes a parsing exception — it won't fix a genuinely bad payload.",
2: "Deleting the whole queue destroys every currently-queued valid message along with the one bad one — a wildly disproportionate and destructive fix.",
3: "A visibility timeout of 0 would make messages immediately visible again to other consumers while still being processed, causing even more duplicate concurrent processing — the opposite of the desired effect.",
},
links=[L("application-integration/sqs.md"), L("compute/lambda.md")]),

dict(stem="""A media company serves large video files from S3 to a globally distributed user base
uploading from mobile devices on inconsistent networks, and wants to minimize the time it takes for
uploads to actually start being received and reduce the impact of long-distance network latency to
the bucket's Region. Which S3 feature is designed specifically for this upload-side latency
problem?""",
multi=False,
options=[
"S3 Transfer Acceleration — it routes uploads through the nearest Amazon CloudFront edge location onto Amazon's optimized backbone network to the bucket's Region, reducing the effect of long-distance public internet latency on upload speed.",
"S3 Intelligent-Tiering, which automatically moves objects between storage classes based on access patterns.",
"S3 Object Lock, which enforces WORM (write-once-read-many) retention.",
"Cross-Region Replication (CRR), configured to replicate objects after they're already fully uploaded.",
],
correct=[0],
explain="""Transfer Acceleration is specifically built to speed up transfers (including uploads)
over long geographic distances by using CloudFront's global edge network as an on-ramp onto AWS's
backbone, rather than having the client's bytes traverse the public internet all the way to the
bucket's Region — exactly the documented fix for "far-away uploaders, slow long-haul network path." """,
wrong={
1: "Intelligent-Tiering optimizes storage cost based on access frequency after objects exist; it has no effect on upload transfer speed.",
2: "Object Lock enforces retention/immutability policies; it is unrelated to transfer performance.",
3: "CRR only begins after an object is already fully uploaded to the source bucket — it doesn't address the upload leg's latency at all, just post-upload replication to another Region.",
},
links=[L("storage/s3.md")]),

dict(stem="""A `Flights` table stores items keyed by `flightId` (partition key). A new requirement
needs a strict guarantee: when booking the last available seat, deduct from `seatsAvailable` on the
`Flights` item **and** insert a new item into a `Bookings` table **atomically** — either both
succeed or neither does, with no possibility of a booking existing without a matching seat
deduction (or vice versa). Which DynamoDB capability provides this cross-item, cross-table
guarantee?""",
multi=False,
options=[
"`TransactWriteItems` — it groups multiple `Put`/`Update`/`Delete`/`ConditionCheck` operations across one or more tables into a single all-or-nothing atomic transaction.",
"Two separate `UpdateItem`/`PutItem` calls made back-to-back in application code, since DynamoDB automatically treats sequential calls from the same Lambda invocation as one transaction.",
"DynamoDB Streams, configured to automatically roll back the first write if the second write fails.",
"Strongly consistent reads on both tables before writing.",
],
correct=[0],
explain="""`TransactWriteItems` is exactly DynamoDB's native ACID-transaction API for this: up to
100 actions across one or more tables are committed as a single atomic unit — all succeed or all
are rolled back — which is the documented mechanism for "these two writes must happen together or
not at all," satisfying the cross-item/cross-table consistency guarantee this scenario requires.""",
wrong={
1: "DynamoDB does not automatically group unrelated sequential API calls into a transaction just because they're in the same Lambda invocation — without `TransactWriteItems`, the two writes are fully independent and either could succeed while the other fails.",
2: "DynamoDB Streams is a change-capture mechanism for reacting to writes after they happen; it has no transactional rollback capability for a separate, already-committed write.",
3: "Consistent reads affect read freshness, not whether two separate writes commit together atomically — they don't provide any transactional guarantee.",
},
links=[L("database/dynamodb.md")]),

dict(stem="""Choose **TWO** correct statements about using API Gateway usage plans and API keys to
manage a public API offered to external third-party developers, where different subscription tiers
(Free, Pro) should get different request-rate limits and usage quotas, and the team needs to
measure/limit usage per customer.""",
multi=True,
options=[
"A usage plan can define throttling (steady-state rate and burst) and a quota (e.g. 10,000 requests/month) that applies to every API key associated with that plan — different plans (Free vs. Pro) can have different throttle/quota values.",
"An API key uniquely identifies a calling customer for metering purposes and is associated with one or more usage plans, letting API Gateway track and enforce that specific customer's consumption against the plan's limits.",
"API keys alone, with no usage plan attached, enforce rate limiting and quotas automatically.",
"Usage plans can only be applied to private (VPC-only) APIs, never to public APIs.",
"Changing a customer's usage plan always requires generating them a brand-new API key.",
],
correct=[0,1],
explain="""Usage plans define the actual throttle/quota numbers (and can differ per tier), while
API keys are the per-customer identity that's associated with a usage plan so API Gateway can meter
and enforce that specific customer's consumption against their assigned plan's limits — this
two-part model (plan = limits, key = identity/association) is exactly how tiered public API access
control works on API Gateway.""",
wrong={
2: "An API key with no usage plan attached does not enforce any throttling/quota by itself — the usage plan is what actually carries the limits; the key is just the identifier associated with a plan.",
3: "Usage plans work with any API Gateway-published API (public or private); this statement about a VPC-only restriction is incorrect.",
4: "A customer can be moved to a different usage plan by re-associating their *existing* API key with the new plan — a new key is not required just to change tiers.",
},
links=[L("networking-content-delivery/api-gateway.md")]),

dict(stem="""Choose **TWO** correct statements about choosing between AWS Step Functions Standard
and Express workflows for a new order-processing state machine that calls several Lambda functions
and needs to run for up to 2 hours end-to-end with exactly-once execution semantics and a full
execution history visible in the console for auditing.""",
multi=True,
options=[
"Standard Workflows support executions lasting up to one year, provide exactly-once workflow execution semantics, and retain a full, visualized execution history for every run in the console.",
"Express Workflows are optimized for high-volume, short-duration workloads (up to 5 minutes), using at-least-once execution semantics, making them a poor fit for a 2-hour exactly-once requirement.",
"Express Workflows can run for up to one year, identical to Standard Workflows.",
"Standard Workflows provide only at-least-once execution semantics, identical to Express.",
"Pricing for Standard Workflows is based on the number of state transitions, which matters for a long-running workflow with many steps.",
],
correct=[0,1],
explain="""Standard Workflows are the correct fit here specifically because of the stated
requirements — up to a year of duration, exactly-once semantics, and full execution history in the
console — none of which Express Workflows provide, since Express targets high-throughput,
short-duration (≤5 minute), at-least-once workloads instead. (Note: the fifth statement about
per-transition pricing is also factually true of Standard Workflows, but only two options are
required for this question — the two listed above are the ones that directly justify the choice.)""",
wrong={
2: "Express Workflows are capped at 5 minutes of execution duration, not one year — this statement is factually wrong and is the opposite of Standard's duration limit.",
3: "Standard Workflows provide exactly-once execution semantics, not at-least-once — this statement incorrectly swaps the two workflow types' characteristics.",
4: "This statement is actually true of Standard Workflows (state-transition-based pricing) but is not one of the two required answers for this specific question about duration/semantics/history — it's included as a plausible-sounding but non-selected true fact to test careful reading of \'choose TWO\'.",
},
links=[L("application-integration/step-functions.md")]),

dict(stem="""A ride-sharing app's AppSync GraphQL API needs to push live driver-location updates to
a rider's app the instant the driver's position changes, without the rider's client polling on an
interval. Which AppSync capability implements this push-based, real-time delivery over a
persistent connection?""",
multi=False,
options=[
"AppSync Subscriptions — clients subscribe to a GraphQL subscription operation, and AppSync pushes matching data to connected clients in real time over a managed WebSocket connection whenever a corresponding mutation occurs.",
"Clients polling a `getDriverLocation` query every 500 milliseconds.",
"A scheduled EventBridge rule that emails the rider a PDF of the driver's location every 5 minutes.",
"API Gateway WebSocket APIs are the only AWS mechanism that can do this; AppSync has no equivalent.",
],
correct=[0],
explain="""Subscriptions are AppSync's dedicated real-time feature: a client issues a GraphQL
subscription, AppSync maintains a managed WebSocket connection, and whenever a mutation that
matches the subscription fires, AppSync pushes the updated data to every subscribed client
immediately — exactly the "instant push, no client polling" requirement.""",
wrong={
1: "Sub-second client polling wastes bandwidth/battery and still introduces polling-interval latency; it's the pattern subscriptions exist to replace.",
2: "A 5-minute scheduled email is nowhere near 'the instant it changes' and is a batch, not real-time, notification mechanism.",
3: "API Gateway WebSocket APIs are a valid way to build custom real-time features, but this statement is factually wrong that AppSync has no native equivalent — Subscriptions is exactly that equivalent, and is the documented Task 1.1 AppSync real-time pattern.",
},
links=[L("application-integration/appsync.md")]),

dict(stem="""Choose **TWO** correct statements about choosing Amazon Aurora over standard Amazon
RDS (e.g. RDS for MySQL) for a new relational workload expected to scale significantly and require
fast failover.""",
multi=True,
options=[
"Aurora separates compute from a distributed, auto-scaling storage layer (replicated across 3 Availability Zones by design), which lets it scale storage automatically without the manual storage-resizing operations needed on standard RDS.",
"Aurora Replicas typically fail over faster than RDS Multi-AZ standby promotion, because replicas share the writer's storage volume and don't need to replay a separate replication stream from scratch to catch up.",
"Aurora and RDS for MySQL have identical maximum storage limits and failover times, with no meaningful difference between them.",
"Aurora only supports a single Availability Zone per cluster, making it less resilient than RDS Multi-AZ.",
"Standard RDS automatically converts to Aurora at midnight UTC if usage exceeds a certain threshold.",
],
correct=[0,1],
explain="""Aurora's storage architecture (distributed, auto-scaling, replicated across 3 AZs by
default) and its replica-failover design (replicas share the same underlying storage, so promotion
doesn't require replaying a replication stream) are the two headline differentiators that make it
both easier to scale and typically faster to fail over than standard RDS Multi-AZ — directly
matching the stated "scale significantly" and "fast failover" requirements.""",
wrong={
2: "This is factually false — Aurora's storage auto-scales up to very large sizes with no manual resizing, and failover is generally faster due to the shared-storage replica design; they are not identical.",
3: "Aurora clusters are inherently multi-AZ by design (storage replicated across 3 AZs); this statement inverts the actual resilience characteristics.",
4: "There is no such automatic conversion feature between RDS and Aurora based on usage thresholds — migrating requires an explicit, deliberate action (e.g. snapshot migration).",
},
links=[L("database/aurora.md"), L("database/rds.md"), L("database/database-selection-guide.md")]),

dict(stem="""A logistics company needs to track a package's state through a strict sequence:
`Created` → `PickedUp` → `InTransit` → `Delivered`, where each transition must call a different
Lambda function, some steps must wait for an external callback (e.g. a customs clearance system
taking up to 48 hours to respond) before continuing, and the whole workflow must be visually
auditable per package. What should orchestrate this instead of hand-rolled state-tracking logic
inside one monolithic Lambda function?""",
multi=False,
options=[
"AWS Step Functions, using a state machine with a `Task` state per transition and the `waitForTaskToken` service integration pattern for the long-running customs callback step, pausing the execution (without consuming compute or holding a Lambda invocation open) until the external system calls back with the token.",
"A single long-running Lambda function that sleeps in a loop for up to 48 hours waiting for the customs system's callback.",
"Amazon SQS alone, with the package state stored as the queue's position in line.",
"CloudWatch Events scheduled to poll the customs system every second for 48 hours.",
],
correct=[0],
explain="""Step Functions' `waitForTaskToken` pattern is exactly built for this: it pauses the
state machine at that step (consuming no compute while waiting, unlike a sleeping Lambda) until an
external process calls `SendTaskSuccess`/`SendTaskFailure` with the matching token, and the whole
sequence — including long external waits — is visually represented and auditable per execution in
the Step Functions console, directly satisfying both the long-wait and auditability requirements.""",
wrong={
1: "Lambda has a hard 15-minute maximum execution duration — it physically cannot sleep for 48 hours in a single invocation, and even if it could, it would be needlessly billed for idle wait time.",
2: "SQS has no concept of a visual, auditable multi-step state machine with long external waits; it's a message queue, not a workflow orchestrator.",
3: "Polling every second for 48 hours (over 172,000 calls) is extremely wasteful and unnecessary compared to an event-driven callback via task tokens.",
},
links=[L("application-integration/step-functions.md")]),

dict(stem="""A gaming leaderboard application uses ElastiCache for Redis to store real-time
player scores, sorted sets, and session data. As the player base grows past what a single Redis
node's memory can hold, the team needs to scale the dataset horizontally across multiple nodes
while keeping sub-millisecond read/write latency. What ElastiCache for Redis feature enables this?""",
multi=False,
options=[
"Redis Cluster Mode Enabled — it shards data across multiple node groups (each with a primary and optional replicas), automatically distributing keys by hash slot so the total dataset can exceed a single node's memory capacity while each shard independently serves its portion of the keyspace.",
"Switching to ElastiCache for Memcached, since Memcached automatically shards data across nodes with zero configuration and Redis cannot do this at all.",
"Increasing the single node's instance type indefinitely, since Redis has no concept of sharding across multiple nodes.",
"Enabling Multi-AZ alone, with Cluster Mode left disabled, since Multi-AZ itself distributes the dataset across nodes for horizontal scale.",
],
correct=[0],
explain="""Cluster Mode Enabled is specifically Redis's horizontal-scaling mechanism in
ElastiCache: the keyspace is partitioned into hash slots distributed across multiple shards (node
groups), letting total cluster capacity scale well beyond any single node's memory while
maintaining Redis's characteristic low-latency operations — directly solving "dataset bigger than
one node can hold.\"""",
wrong={
1: "This both overstates Memcached (which does support client-side/consistent-hash-based sharding, not something fundamentally beyond Redis) and understates Redis, which explicitly supports cluster-mode sharding — the comparison as stated is incorrect.",
2: "Vertically scaling a single node has a hard ceiling (the largest available instance type) and doesn't provide horizontal scale-out; Redis absolutely does support multi-node sharding via Cluster Mode.",
3: "Multi-AZ (replication group failover) provides high availability for a given shard's data, not horizontal partitioning of the dataset across more capacity — Cluster Mode is the distinct feature needed for that.",
},
links=[L("database/elasticache.md")]),

dict(stem="""A nightly batch job needs to invoke a Lambda function at exactly 2:00 AM UTC every
day to generate a sales report, with no manual trigger and no EC2 instance to keep running just to
fire the job. What is the correct, fully managed way to schedule this?""",
multi=False,
options=[
"An Amazon EventBridge scheduled rule using a cron expression (e.g. `cron(0 2 * * ? *)`) targeting the Lambda function directly — EventBridge invokes the function on the defined schedule with no infrastructure to manage.",
"A `while True: time.sleep(86400)` loop inside the Lambda function itself, checking the current time on every wakeup.",
"An EC2 instance left running 24/7 with a local cron job that calls the Lambda function's URL once a day.",
"API Gateway configured with a `rate()` limit of one request per day, since usage plans substitute for schedules.",
],
correct=[0],
explain="""EventBridge scheduled rules (cron or rate expressions) are the documented, fully
managed way to invoke a target like Lambda on a recurring schedule, with zero servers to run or
maintain — exactly matching "no EC2 instance just to fire a nightly job," which is a Task 1.1
event-driven-application pattern applied to scheduling.""",
wrong={
1: "Lambda has a 15-minute maximum execution duration — it cannot sleep in a loop waiting for the next day; this also wastes billed compute time sitting idle.",
2: "Keeping an EC2 instance running 24/7 just to fire one daily job defeats the serverless, no-idle-infrastructure goal entirely.",
3: "API Gateway usage plan quotas limit *how many* requests a client can make; they don't actively trigger an invocation on a schedule — this conflates two unrelated concepts.",
},
links=[L("application-integration/eventbridge.md")]),

dict(stem="""A `Products` table has partition key `productId`. A new GSI is added with partition
key `category` to support "list products in a category" queries. The application only ever needs
`productId`, `name`, and `price` from that query — never the other 15 attributes on each product
item. Which GSI projection type minimizes the GSI's storage cost and write amplification while
still satisfying the query?""",
multi=False,
options=[
"`INCLUDE`, projecting only `productId`, `name`, and `price` (plus the table's keys, which are always projected) into the index — storing exactly the attributes the query needs and nothing more.",
"`ALL`, projecting every attribute from the base table into the index, since more projected data always performs better regardless of what's actually queried.",
"`KEYS_ONLY`, since the application can always make a second `GetItem` call per result if needed.",
"GSIs cannot have a restricted projection; they always copy every attribute from the base table.",
],
correct=[0],
explain="""`INCLUDE` lets a GSI project only the specific non-key attributes actually needed by
queries against it, minimizing both the extra storage consumed by the index and the write-capacity
cost of keeping it in sync on every base-table write — the right choice here since exactly three
non-key attributes are needed and nothing more, which is cheaper than `ALL` and avoids `KEYS_ONLY`'s
need for a second round-trip per result.""",
wrong={
1: "`ALL` costs more in storage and per-write overhead for attributes the query never uses; it's not universally 'better' when a narrower set of attributes is known to be sufficient.",
2: "`KEYS_ONLY` would require a follow-up `GetItem` per item to fetch `name` and `price`, adding latency and extra read capacity consumption that `INCLUDE` avoids entirely by projecting those specific attributes directly into the index.",
3: "This is factually incorrect — GSIs explicitly support `KEYS_ONLY`, `INCLUDE`, and `ALL` projection types specifically to let developers control exactly this tradeoff.",
},
links=[L("database/dynamodb.md")]),

dict(stem="""A document archive stores millions of files in S3. Compliance requires keeping files
accessible for 90 days at standard retrieval speed, then moving them to much cheaper archival
storage for 9 more months (still occasionally retrievable within hours if needed), and permanently
deleting them after one year total — all without any application code managing the transitions.
What should be configured?""",
multi=False,
options=[
"An S3 Lifecycle configuration with a transition rule moving objects to S3 Glacier Flexible Retrieval (or Glacier Instant Retrieval) at 90 days, and an expiration rule deleting objects at 365 days — S3 applies both actions automatically with no application involvement.",
"A Lambda function scheduled via EventBridge to run daily, listing every object in the bucket and manually calling `CopyObject`/`DeleteObject` based on each object's age.",
"S3 Versioning alone, since old versions are automatically deleted after 90 days by default.",
"Store the retention rules in a DynamoDB table and have every application read request check the table before deciding whether to serve the file.",
],
correct=[0],
explain="""S3 Lifecycle rules are exactly the native, no-code mechanism for this: transition
actions move objects between storage classes at defined ages, and expiration actions delete
objects at a defined age — both evaluated and executed by S3 itself in the background, directly
matching "90 days standard → archival for 9 months → delete at 1 year" with zero custom code.""",
wrong={
1: "Hand-rolling a daily scan-and-migrate Lambda duplicates Lifecycle's built-in functionality with far more code, cost (listing/copying millions of objects), and operational risk.",
2: "S3 Versioning has no automatic 90-day deletion behavior by default; versions persist until an explicit lifecycle rule or deletion removes them — this option misstates Versioning's behavior.",
3: "Building a custom retention-tracking table and gating every read on it reinvents what Lifecycle already does natively, with added latency and a new system to maintain.",
},
links=[L("storage/s3.md")]),

dict(stem="""A real-time chat application needs clients to maintain a persistent, bidirectional
connection to the backend so either side can push messages at any time, with each connected
client's unique connection identifier stored so the backend can target a message to a specific
user later. Which API Gateway capability, combined with what storage, implements this?""",
multi=False,
options=[
"An API Gateway WebSocket API with `$connect`/`$disconnect`/custom routes, storing each client's `connectionId` (available in the `$connect` route's Lambda event) in a DynamoDB table, then using the API Gateway Management API's `PostToConnection` call to push a message to a specific stored `connectionId` later.",
"An API Gateway REST API, since REST APIs natively support persistent bidirectional connections with no additional configuration.",
"Amazon SNS alone, since every SNS subscriber maintains a reusable open HTTP connection to the publisher.",
"Polling a REST endpoint every 200 milliseconds from each client to check for new messages.",
],
correct=[0],
explain="""WebSocket APIs are API Gateway's purpose-built feature for persistent, bidirectional
client connections: the `$connect` route event includes the new `connectionId`, which the app
typically persists in DynamoDB; later, the backend can push a message to any specific stored
`connectionId` via the API Gateway Management API's `PostToConnection` action — exactly the
documented "push to a specific connected client" chat pattern.""",
wrong={
1: "REST APIs are request/response over HTTP; they have no concept of a persistent, server-push-capable connection — that's specifically what the WebSocket API type adds.",
2: "SNS delivers to subscribed endpoints (SQS, Lambda, HTTP(S), etc.) per publish; it does not maintain a persistent connection per end-user client the way a WebSocket API does, and isn't designed for per-connection targeted pushes like this.",
3: "Sub-second polling from every client is far less efficient and far higher latency than a true push-based WebSocket connection, and is exactly the pattern WebSocket APIs exist to replace.",
},
links=[L("networking-content-delivery/api-gateway.md")]),

dict(stem="""Choose **TWO** correct statements about fanning out a single `UserSignedUp` event from
an SNS topic to three independent SQS queues (one per downstream microservice: welcome-email,
analytics, and fraud-check), where each microservice should process the event at its own pace
without affecting the others.""",
multi=True,
options=[
"The SNS-to-multiple-SQS fan-out pattern decouples the publisher from the number and identity of consumers — the publishing service only needs to know about the topic, not about any specific downstream queue or service.",
"Because each microservice has its own SQS queue, one microservice falling behind or failing to process messages does not block or slow down the other two microservices' independent processing of their own queue.",
"SNS guarantees that a message delivered to one subscribed SQS queue is automatically removed from the other two queues once any one of them processes it.",
"This pattern requires the publisher to send three separate, individually addressed messages — one per downstream queue — since SNS cannot deliver one message to multiple queues.",
"Each SQS queue in this fan-out pattern can independently configure its own visibility timeout and DLQ redrive policy, appropriate to that specific microservice's processing characteristics.",
],
correct=[0,1],
explain="""This is the canonical SNS fan-out pattern precisely because it (a) decouples the
publisher entirely from how many or which services ultimately consume the event, and (b) gives each
consumer its own independent queue, so one slow or failing consumer's backlog has zero effect on
the others' throughput — exactly the stated requirement of independent per-microservice pacing.
(Statement 5 is also factually true of this architecture but isn't one of the two required answers
for what makes it the right choice here.)""",
wrong={
2: "Each subscribed queue receives its own independent copy of the message; processing in one queue has no effect on the copies in the other two queues — there is no cross-queue \"consumed once\" behavior in a fan-out topology.",
3: "SNS natively fans a single published message out to every subscribed endpoint (including multiple SQS queues) — the publisher sends exactly one message to the topic, not one per destination; this statement misstates how SNS fan-out works.",
4: "True but not one of the two selected answers — it's a correct supporting detail about independent queue configuration, included to test careful 'choose exactly TWO' selection rather than picking every true-sounding option.",
},
links=[L("application-integration/sns.md"), L("application-integration/messaging-patterns-overview.md")]),
]

E2_D2 = [
dict(stem="""An IAM policy attached to a developer role includes:
```json
{
  "Effect": "Allow",
  "NotAction": "iam:*",
  "Resource": "*"
}
```
with no other statements in the policy. What does this statement actually grant, and why is
`NotAction` combined with `Resource: *` and no other conditions a common Task 2.1 misconfiguration
to watch for?""",
multi=False,
options=[
"It allows every AWS action **except** the listed `iam:*` actions, on every resource — meaning the role gets broad access across virtually every other service (EC2, S3, DynamoDB, etc.), which is almost certainly far more permissive than intended, even though it looks restrictive at a glance because of the word 'Not'.",
"It denies every action except `iam:*`, which is the opposite of an overly broad grant.",
"`NotAction` has no effect when combined with `Allow`; this statement grants nothing at all.",
"It only allows IAM actions, since `NotAction` is a typo for `Action` and AWS silently corrects it.",
],
correct=[0],
explain="""`NotAction` inverts the action list — an `Allow` with `NotAction: iam:*` and `Resource:
*` grants every action in every other service, which is a dramatically broader grant than it
appears at first glance. This is a real, documented exam trap: `NotAction` is easy to misread as
restrictive when paired with `Allow`, when it actually produces a near-administrator-level grant
unless scoped down with additional conditions or resource restrictions.""",
wrong={
1: "This misreads the semantics entirely — with `Effect: Allow`, `NotAction` grants everything *except* the listed actions, not the reverse.",
2: "`NotAction` is a valid, documented IAM policy element with well-defined (if often misunderstood) semantics; it is not a no-op.",
3: "`NotAction` and `Action` are two distinct, valid policy elements, not a typo of one another — there is no silent auto-correction in IAM.",
},
links=[L("security-identity-compliance/iam.md")]),

dict(stem="""A GitHub Actions CI/CD pipeline needs to deploy to AWS without storing any long-lived
AWS access keys as GitHub repository secrets, since the team wants to eliminate the risk of a
leaked long-lived credential entirely. What AWS mechanism supports this keyless pattern?""",
multi=False,
options=[
"`AssumeRoleWithWebIdentity` using OIDC federation — configure an IAM OIDC identity provider trusting GitHub's OIDC token issuer, and a role trust policy scoped to the specific repository/branch, so GitHub Actions exchanges its short-lived OIDC token for short-lived AWS credentials on every run with no stored AWS keys at all.",
"Store a long-lived IAM user's access key and secret key as encrypted GitHub secrets, and accept the leak risk as unavoidable.",
"Use the AWS root account's access keys in the pipeline, since root keys never expire and are therefore more reliable for automation.",
"Hardcode the credentials directly in the workflow YAML file for simplicity, since GitHub's repository is private.",
],
correct=[0],
explain="""`AssumeRoleWithWebIdentity` with an OIDC identity provider is exactly AWS's
documented keyless CI/CD pattern: GitHub Actions presents a short-lived, workflow-scoped OIDC
token, IAM verifies it against a configured trust relationship (which can be scoped to specific
repos/branches/environments), and STS returns short-lived AWS credentials for that run only — no
long-lived access key ever needs to be created, stored, or rotated.""",
wrong={
1: "Storing a long-lived access key, even encrypted as a GitHub secret, is exactly the risk the OIDC pattern is designed to eliminate — it remains a standing credential that could leak or be misused.",
2: "Root account keys are a severe security anti-pattern under any circumstance — root credentials should never be used for routine automation, and never expiring is a liability here, not a benefit.",
3: "Hardcoding credentials in a workflow file, private repo or not, is a well-known credential-exposure risk (history, forks, logs, misconfigured visibility) and should never be done regardless of repo privacy settings.",
},
links=[L("security-identity-compliance/sts-and-role-switching.md")]),

dict(stem="""A company's mobile app allows anyone to sign up with an email address, but the team
only wants to allow sign-ups from company-approved partner domains (e.g. `@partnerco.com`), rejecting
all others at sign-up time, before an account is ever created. Which Cognito feature implements
this custom business rule?""",
multi=False,
options=[
"A Cognito user pool **Pre Sign-up** Lambda trigger — it runs synchronously during the sign-up flow and can inspect the submitted email domain, returning an error to reject the sign-up (or auto-confirm it) before the user record is created.",
"An IAM policy attached to the user pool restricting which email domains can call `SignUp`.",
"A Cognito identity pool role mapping rule, since identity pools handle sign-up validation.",
"Manually reviewing every new sign-up in the console and deleting unapproved ones after the fact.",
],
correct=[0],
explain="""The Pre Sign-up Lambda trigger is exactly the documented Cognito extension point for
custom sign-up business logic: it fires synchronously as part of the `SignUp` flow, before the
user is created, letting custom code (like a domain allow-list check) reject or auto-confirm the
sign-up — directly implementing "only approved domains may sign up" without any after-the-fact
cleanup.""",
wrong={
1: "IAM policies control which AWS principals can call AWS APIs; they have no visibility into or control over end-user-submitted sign-up form fields like an email domain.",
2: "Identity pools issue temporary AWS credentials after authentication; they have no role in the user pool's sign-up validation flow at all.",
3: "Manual post-hoc review and deletion lets unapproved accounts exist (even briefly) and doesn't scale, unlike a synchronous pre-sign-up check that rejects them immediately.",
},
links=[L("security-identity-compliance/cognito.md")]),

dict(stem="""A company uses AWS IAM Identity Center with permission sets assigned per-account.
A contractor needs `ReadOnlyAccess`-level permissions in exactly one of 30 member accounts for a
3-month engagement, and the team wants this scoped as tightly and auditable as possible, with easy
revocation at the end of the engagement. What is the correct approach, as opposed to creating a
standalone IAM user directly in that one account?""",
multi=False,
options=[
"Create (or reuse) a `ReadOnly` permission set in IAM Identity Center and assign it to the contractor's Identity Center user for only that one specific account — granting access through the centrally managed assignment, which can be revoked instantly by removing the assignment, with Identity Center's own audit trail of who has what.",
"Create a standalone IAM user in that one account with `ReadOnlyAccess` attached directly, and share its password with the contractor over email.",
"Grant the contractor `AdministratorAccess` in all 30 accounts temporarily, since permission sets cannot be scoped to a single account.",
"Add the contractor to the AWS Organizations management account's root user credentials.",
],
correct=[0],
explain="""Permission sets in IAM Identity Center are explicitly designed to be assigned per
user/group and per account — a `ReadOnly` permission set assigned to exactly one account gives
exactly the scoped, time-boxed access needed, with centralized visibility into every assignment and
one-click revocation by removing the account assignment when the engagement ends, which is both
more auditable and more easily revocable than a standalone IAM user.""",
wrong={
1: "A standalone IAM user with an emailed password is a far weaker, harder-to-audit, harder-to-revoke-cleanly pattern than a centrally managed Identity Center assignment, and email is not a secure credential-sharing channel.",
2: "Permission sets are explicitly scoped per-account during assignment; granting broad admin access across all 30 accounts when only one account and read-only access is needed is a severe over-grant.",
3: "Root user credentials should never be shared with anyone, let alone a short-term contractor — this is one of the most severe possible security anti-patterns.",
},
links=[L("security-identity-compliance/iam-identity-center-sso.md")]),

dict(stem="""A company wants every account in a specific Organizational Unit (OU) to be prevented
from ever disabling AWS CloudTrail or deleting its S3 log bucket, even by an account's own
administrator, to guarantee an unbroken audit trail for compliance. What is the correct control?""",
multi=False,
options=[
"An SCP attached to that OU that explicitly denies `cloudtrail:StopLogging`, `cloudtrail:DeleteTrail`, and the relevant `s3:DeleteBucket`/`s3:DeleteObject` actions on the logging bucket, for every principal in accounts under that OU — including the account's own root/admin user.",
"A CloudTrail configuration setting called 'TamperProof Mode' that any account admin can toggle on.",
"An IAM policy attached only to the specific CloudTrail service role, with no SCP involved.",
"Trusting that account administrators will simply not do this, with no technical control.",
],
correct=[0],
explain="""Because SCPs bound the maximum permissions available to every principal in an account
— including that account's own administrators — an SCP explicitly denying the trail-stopping and
log-bucket-deletion actions is the only one of these options that actually prevents even a
full-admin account owner from tampering with the audit trail, which is exactly the guarantee a
compliance requirement like this needs.""",
wrong={
1: "No such named feature exists, and even if a toggle like this existed, something an admin can simply toggle would not meet a hard compliance guarantee against that same admin.",
2: "An IAM policy scoped to a service role doesn't constrain what an account's own administrators (who can edit IAM policies) are able to do — only an SCP, enforced outside the account's own IAM control, can bind the admin themselves.",
3: "Relying on trust with no enforced technical control doesn't satisfy a compliance requirement for a guaranteed, unbroken audit trail.",
},
links=[L("security-identity-compliance/organizations-and-scps.md"), L("management-governance/cloudtrail.md")]),

dict(stem="""Two internal microservices communicate over mutual TLS (mTLS) within a private VPC,
and the team wants certificates issued by an internal certificate authority that's trusted only
within the organization (not a publicly trusted CA, since these services are never exposed to the
public internet). What AWS service should issue these certificates?""",
multi=False,
options=[
"AWS Private Certificate Authority (Private CA) — it operates a managed internal CA hierarchy that issues certificates trusted by anything configured to trust that private root/subordinate CA, appropriate for internal mTLS between services that should never need a publicly trusted certificate.",
"AWS Certificate Manager's standard public certificate issuance flow, since all ACM certificates are automatically trusted by every client worldwide, public or internal.",
"Amazon Cognito, since it can issue arbitrary X.509 certificates for any use case.",
"AWS KMS, since KMS keys can be directly used as TLS certificates with no conversion needed.",
],
correct=[0],
explain="""Private CA is exactly the service for internal-only PKI: it issues certificates from a
CA hierarchy that's trusted only by systems explicitly configured to trust it (e.g. internal
service meshes doing mTLS), which is the right tool when certificates are for internal,
never-public-facing use — unlike public ACM certificates, which are meant for publicly trusted
TLS endpoints.""",
wrong={
1: "Public ACM certificates are issued from a publicly trusted CA chain and are meant for internet-facing endpoints; using that mechanism doesn't make sense (and isn't the documented approach) for purely internal, never-public service-to-service mTLS.",
2: "Cognito is an identity/authentication service for end users and applications; it does not issue X.509 certificates for mTLS between backend services.",
3: "KMS manages symmetric/asymmetric encryption keys; a raw KMS key is not itself a TLS certificate and cannot be used as one without an entirely different issuance process (which is what Private CA provides).",
},
links=[L("security-identity-compliance/acm-and-private-ca.md")]),

dict(stem="""An application needs to encrypt a large (50 MB) file client-side before uploading it
to S3, using envelope encryption with a KMS customer-managed key, without sending the entire 50 MB
payload to KMS itself (which has request size and throughput limits unsuited to bulk data
encryption). What is the correct envelope encryption flow?""",
multi=False,
options=[
"Call `kms:GenerateDataKey` to get a plaintext data key and its KMS-encrypted counterpart; use the plaintext data key locally (client-side) to encrypt the 50 MB file with a fast symmetric cipher (e.g. AES-256-GCM); discard the plaintext data key from memory; store the encrypted data key alongside the encrypted file (e.g. as S3 object metadata), so decryption later calls `kms:Decrypt` on just the small data key, not the large file.",
"Send the full 50 MB file directly to `kms:Encrypt`, since KMS has no practical size limit on the data it can encrypt directly.",
"Use the KMS key's key material to manually derive an AES key using custom application code instead of calling KMS APIs at all.",
"Store the file unencrypted and instead encrypt only its filename using KMS, which is sufficient for compliance.",
],
correct=[0],
explain="""This is the textbook envelope encryption pattern and exactly why `GenerateDataKey`
exists: KMS generates and returns both a plaintext and an encrypted copy of a data key, the
plaintext copy is used locally for fast bulk symmetric encryption of the large payload (never
sent to KMS), and only the small encrypted data key (not the large file) needs a KMS `Decrypt`
call later — this is precisely Task 2.2's "envelope encryption" pattern for large data.""",
wrong={
1: "`kms:Encrypt` is explicitly documented with a small payload size limit (4 KB for symmetric keys) — it is not designed or usable for directly encrypting a 50 MB file; this option is factually incorrect.",
2: "KMS key material is deliberately never exposed outside KMS for customer-managed keys backed by KMS's own HSMs — there is no supported way to extract raw key material to derive keys manually, and doing so would undermine the whole security model.",
3: "Encrypting only the filename leaves the actual file content (the sensitive 50 MB payload) completely unencrypted, failing any real encryption-at-rest requirement.",
},
links=[L("security-identity-compliance/kms.md")]),

dict(stem="""An application reads a non-sensitive application configuration value (`maxRetries: 3`)
from AWS Systems Manager Parameter Store on every Lambda cold start. The team notices this adds
noticeable latency to every cold start and wants to reduce the number of `GetParameter` API calls
without hardcoding the value or losing the ability to update it without a redeploy. What should
they add?""",
multi=False,
options=[
"The AWS Parameters and Secrets Lambda Extension (or an in-memory cache with a TTL inside the handler) to cache the parameter value for a configurable duration within the execution environment, avoiding a fresh `GetParameter` call on every single invocation while still allowing updates to propagate after the cache TTL expires.",
"Call `GetParameter` once at build time and bake the resulting value permanently into the deployment package.",
"Increase the Lambda function's memory, which caches Parameter Store values automatically.",
"Switch from Parameter Store to Secrets Manager, which has zero API latency by design.",
],
correct=[0],
explain="""Caching with a bounded TTL (via the purpose-built Parameters and Secrets Lambda
Extension, or a simple in-handler cache keyed by execution environment reuse) is the documented
way to reduce repeated Parameter Store calls while still allowing config changes to take effect
after the cache expires — directly balancing "fewer calls/less latency" against "still updatable
without redeploying code," which permanently baking the value in would sacrifice.""",
wrong={
1: "Baking the value in at build time means any future change again requires a full redeploy, which is exactly the flexibility the team wants to keep.",
2: "Memory configuration has no relationship to Parameter Store client-side caching; this is not a real feature of Lambda memory settings.",
3: "Secrets Manager is also a remote API call with its own latency characteristics; switching services doesn't eliminate network/API call latency, and this statement about zero latency is not accurate.",
},
links=[L("security-identity-compliance/secrets-manager-vs-parameter-store.md"), L("compute/lambda.md")]),

dict(stem="""A company runs automated, recurring Amazon Macie sensitive-data discovery jobs across
all its S3 buckets, and separately wants ongoing vulnerability scanning of its EC2 instances and
container images for known CVEs. Which two services, together, cover these two distinct needs?""",
multi=False,
options=[
"Amazon Macie for sensitive-data discovery in S3 (already in place) and Amazon Inspector for automated vulnerability scanning of EC2 instances and container images against known CVE databases.",
"Amazon GuardDuty alone covers both sensitive-data discovery and vulnerability scanning, making a second service unnecessary.",
"AWS Config alone covers both needs, since it can scan both object content and CVE databases.",
"AWS Trusted Advisor is the correct tool for CVE-level vulnerability scanning of running workloads.",
],
correct=[0],
explain="""Macie and Inspector are complementary, purpose-specific services: Macie classifies and
discovers sensitive data at rest in S3, while Inspector automatically and continuously scans EC2
instances, running container images in ECR, and Lambda functions for known software
vulnerabilities (CVEs) and network reachability issues — together covering both of the distinct
needs described, neither of which the other fully replaces.""",
wrong={
1: "GuardDuty is a threat-detection service analyzing activity logs for malicious behavior; it does not perform content-level sensitive-data discovery (Macie's job) or systematic CVE vulnerability scanning (Inspector's job).",
2: "AWS Config evaluates resource *configuration* against rules; it has no sensitive-data content scanning capability and no CVE vulnerability database scanning capability.",
3: "Trusted Advisor provides general best-practice checks (cost, fault tolerance, some security configuration checks); it is not a CVE/vulnerability scanning engine for running workloads — that is specifically Inspector's purpose.",
},
links=[L("security-identity-compliance/macie.md"), L("security-identity-compliance/security-hub-and-inspector.md")]),

dict(stem="""Under the AWS Shared Responsibility Model, for an application using Amazon RDS
(a managed database service, as opposed to self-managed EC2-hosted MySQL), which of the following
is AWS's responsibility rather than the customer's?""",
multi=False,
options=[
"Patching the underlying database engine's software, OS, and host infrastructure for a standard RDS-managed deployment.",
"Configuring the database's security group rules to restrict network access appropriately.",
"Designing a least-privilege IAM policy for the application's role that connects to the database.",
"Choosing strong master credentials and rotating them on an appropriate schedule.",
],
correct=[0],
explain="""RDS is explicitly a managed database service — AWS takes on patching the underlying
engine software and host OS as part of "security OF the cloud," which is the key differentiator
from self-managed EC2-hosted databases where the customer would be responsible for all of that
patching themselves. The customer remains responsible for everything else listed (network access
config, IAM, credential hygiene) as "security IN the cloud.\"""",
wrong={
1: "Security group configuration is explicitly the customer's responsibility under the shared responsibility model for any VPC-attached resource, including RDS.",
2: "IAM policy design for application roles is always the customer's responsibility — AWS never decides an application's own permission scoping for them.",
3: "Credential strength/rotation practices for the database's own master user are the customer's operational responsibility, even though RDS can assist (e.g. integration with Secrets Manager rotation).",
},
links=[L("security-identity-compliance/shared-responsibility-model-deep-dive.md")]),

dict(stem="""A web application behind CloudFront and API Gateway is being probed with crafted
requests attempting SQL injection in query string parameters. The team wants these blocked
automatically at the edge using AWS-maintained, continuously updated rule sets, without writing and
maintaining custom regex rules themselves. What should they use?""",
multi=False,
options=[
"An AWS WAF web ACL with the AWS Managed Rules groups (e.g. the SQL database rule group and the Core Rule Set), associated with the CloudFront distribution/API Gateway stage, so known SQL injection patterns are blocked using rules AWS maintains and updates on an ongoing basis.",
"A custom Lambda@Edge function that the team writes and maintains itself to pattern-match every known SQL injection signature manually.",
"AWS Shield Standard, which includes SQL injection-specific managed rule groups.",
"Amazon GuardDuty, configured to block requests matching SQL injection signatures in real time.",
],
correct=[0],
explain="""WAF's AWS Managed Rules are exactly built for this: pre-built, continuously updated
rule groups (including a SQL-injection-focused rule group) maintained by AWS, attached to a web ACL
on CloudFront/API Gateway/ALB — giving "blocked automatically with no custom regex to maintain,"
which is the documented alternative to hand-rolling detection logic.""",
wrong={
1: "Writing and maintaining custom SQL injection detection logic by hand duplicates exactly what AWS Managed Rules already provides, with ongoing maintenance burden the question explicitly wants to avoid.",
2: "Shield Standard protects against common network/transport-layer DDoS patterns automatically; it has no application-layer rule groups for SQL injection — that's WAF's domain.",
3: "GuardDuty is a detection service analyzing logs/activity for threats; it does not sit inline blocking HTTP requests at the edge the way a WAF web ACL does.",
},
links=[L("security-identity-compliance/waf.md")]),

dict(stem="""Choose **TWO** correct actions for integrating Amazon GuardDuty and AWS Security Hub
so that a GuardDuty finding indicating a likely-compromised EC2 instance automatically triggers an
isolation workflow (e.g. quarantining the instance's security group) without a human needing to
manually notice and act on the finding in the console.""",
multi=True,
options=[
"Enable GuardDuty findings to flow into Security Hub for centralized, aggregated visibility across multiple detection sources, and separately create an EventBridge rule matching the specific GuardDuty finding type/severity that targets a Lambda function (or Systems Manager Automation document) to perform the isolation action automatically.",
"Configure the EventBridge rule to match on the GuardDuty finding event pattern (e.g. detail-type 'GuardDuty Finding' with a severity threshold), since EventBridge is the mechanism that actually triggers the automated remediation target, not Security Hub aggregation alone.",
"Security Hub aggregation alone automatically performs remediation actions with no EventBridge rule or target needed.",
"GuardDuty findings cannot be consumed by EventBridge under any circumstances; only manual console review is supported.",
"Disable GuardDuty once Security Hub is enabled, since Security Hub replaces GuardDuty's detection capability entirely.",
],
correct=[0,1],
explain="""Automated remediation requires both pieces working together: Security Hub gives
centralized visibility/aggregation (useful for reporting and prioritization) but does not itself
execute remediation actions, while an EventBridge rule matching on the GuardDuty finding event is
the actual trigger that invokes a remediation target (Lambda, SSM Automation, etc.) — Security Hub
aggregation and the EventBridge-driven trigger are the two distinct, necessary pieces for this
no-human-in-the-loop workflow.""",
wrong={
2: "Security Hub centralizes and prioritizes findings for human/dashboard consumption; it does not independently execute remediation actions without an EventBridge rule (or similar) wired to an actual target.",
3: "GuardDuty findings are explicitly designed to be consumed as EventBridge events — this is the standard, documented integration path for automated response, so this statement is factually wrong.",
4: "Security Hub is a findings-aggregation and posture-management service; it does not generate GuardDuty's own threat-detection analytics and does not replace GuardDuty — disabling GuardDuty would remove the actual detection capability entirely.",
},
links=[L("security-identity-compliance/guardduty.md"), L("security-identity-compliance/security-hub-and-inspector.md")]),

dict(stem="""A security team wants to know, for compliance audit purposes, exactly which S3
objects in a sensitive bucket were read (not just which API calls were made to the bucket overall)
over the last 90 days, including by which IAM principal and at what time, down to the individual
`GetObject` call. What CloudTrail feature is required, since it is not enabled by default?""",
multi=False,
options=[
"CloudTrail data events for S3 — unlike default management events, data events (which log object-level operations like `GetObject`/`PutObject`) must be explicitly enabled on a trail (often selectively, by bucket/prefix, since they can be high-volume) and record exactly this kind of per-object access detail.",
"CloudTrail management events alone, since they already log every individual `GetObject` call by default.",
"VPC Flow Logs, since they capture a log line for every S3 `GetObject` API call automatically.",
"S3 Versioning, which tracks who read each object version by default.",
],
correct=[0],
explain="""Management events (enabled by default on a trail) capture control-plane operations
like creating/deleting a bucket or changing its policy — they do **not** capture per-object
data-plane calls like `GetObject`. Data events are the specific, opt-in CloudTrail feature for
object-level S3 (and Lambda invoke, DynamoDB item-level, etc.) logging, which is exactly what's
needed to audit individual object reads by principal and time.""",
wrong={
1: "This is factually incorrect — management events do not include individual object-level `GetObject`/`PutObject` calls; that is specifically what data events add.",
2: "VPC Flow Logs capture IP-layer traffic metadata (source/destination IP, port, bytes) at the network interface level, not which S3 API action was called or by which IAM principal.",
3: "S3 Versioning tracks object version history for overwrites/deletes; it has no concept of logging *read* access by principal — that is a CloudTrail data events / S3 server access logging concern, not Versioning.",
},
links=[L("management-governance/cloudtrail.md"), L("storage/s3.md")]),

dict(stem="""A mobile app uses a Cognito identity pool to let unauthenticated ("guest") users browse
a public product catalog stored in DynamoDB, without requiring sign-in, while authenticated
(signed-in) users should additionally be able to write to their own cart data. What is the correct,
least-privilege way to configure the two Cognito identity pool roles for this?""",
multi=False,
options=[
"Configure the unauthenticated role with read-only IAM permissions scoped to just the public catalog table/items, and configure the authenticated role with the catalog read permissions **plus** write permissions scoped (e.g. via `dynamodb:LeadingKeys` conditions) to only that specific signed-in user's own cart items.",
"Grant both the unauthenticated and authenticated roles full `dynamodb:*` access on every table, since simplicity outweighs scoping for a mobile app.",
"Use a single shared role for both unauthenticated and authenticated users, since Cognito identity pools only support one role total.",
"Give the unauthenticated role write access to the cart table as well, since guests might want to add items before signing in later.",
],
correct=[0],
explain="""Cognito identity pools support two distinct IAM roles — one for unauthenticated,
one for authenticated identities — and the least-privilege design here scopes the unauthenticated
role to only read-only catalog access (guests have no identity-specific data to protect/write),
while the authenticated role adds narrowly scoped write access to only the signed-in user's own
cart data (e.g. via a `dynamodb:LeadingKeys` condition tying access to their Cognito identity ID),
directly matching the stated requirements for each user class.""",
wrong={
1: "Blanket `dynamodb:*` access for both roles is a severe least-privilege violation, letting a guest read or write arbitrary data far beyond the public catalog.",
2: "Identity pools explicitly support two separate roles (unauthenticated and authenticated) specifically so each class of user can have different permissions — this statement is factually wrong.",
3: "Allowing unauthenticated guests to write to a cart table they have no durable identity tied to creates orphaned, unattributable data and exceeds what an anonymous guest role should be trusted with.",
},
links=[L("security-identity-compliance/cognito.md")]),

dict(stem="""A team's Bedrock-based document-summarization feature processes internal company
documents, some containing confidential business data. The compliance team requires written
assurance that none of this data will be used by the underlying foundation model provider to
improve or train their models. What Task 2.3 control addresses this specific concern?""",
multi=False,
options=[
"Confirm Bedrock's documented data handling posture: Amazon Bedrock does not use customer input/output data sent through the Bedrock API to train the underlying foundation models, and does not share that data with the model providers for their own model improvement — this is a standing data-handling guarantee of the Bedrock service itself, not a per-request opt-out the application needs to configure.",
"Manually strip every document of sensitive content before calling Bedrock, since Bedrock always uses all submitted data to retrain all available models by default.",
"Switch to a self-managed, on-premises ML model, since no AWS AI service can ever guarantee data isn't used for training.",
"Encrypt the documents with an S3 bucket key before sending them to Bedrock's `InvokeModel` API, which prevents the model from using the plaintext content for training.",
],
correct=[0],
explain="""Task 2.3's "keeping your inputs/outputs out of a provider's model training data" bullet
maps directly to Bedrock's actual documented data-handling model: AWS states that Amazon Bedrock
does not use customer content submitted through the API to train the underlying foundation models
or share it with model providers for their own improvement — this is the core fact to know for
this exam topic, not a feature flag that needs separate opt-out configuration per request.""",
wrong={
1: "This option states the opposite of Bedrock's actual documented data-handling behavior and recommends an unnecessary (and impractical) workaround to a non-existent default-training-use problem.",
2: "Bedrock's data-handling commitments specifically address this training-data concern for AWS-hosted use of the service; a self-managed model isn't required to get this assurance.",
3: "`InvokeModel` requires the model to receive processable plaintext input to generate a summary — encrypting the document before sending it would make it unusable to the model, and this isn't actually how the training-data protection works (it's a service-level data-handling commitment, not something achieved by client-side encryption of the payload).",
},
links=[D("domain-2-security/ai-service-security-risks.md"), L("machine-learning-ai/bedrock.md")]),

dict(stem="""A Bedrock-powered customer support chatbot logs each conversation turn (including the
full user message and the model's full response) to CloudWatch Logs for debugging purposes. A
security review flags this under Task 2.3's "sensitive data in logs from AI service calls" item,
since users sometimes paste account numbers or other PII into their chat messages. What is the
correct remediation?""",
multi=False,
options=[
"Apply redaction/masking to the logged conversation content before it's written (e.g. using a log-processing step or Macie-style pattern detection to strip/mask PII patterns like account numbers), and restrict access to any logs that might still retain sensitive context via IAM and log group access controls — treating AI service call logs with the same sensitive-data handling rigor as any other application log that might contain PII.",
"Stop logging entirely, since any logging of AI interactions is inherently non-compliant and cannot be fixed.",
"Log the conversations in full, unredacted, since CloudWatch Logs is itself a PII-safe, specially exempted storage location.",
"Only redact the model's responses, since user input can never contain sensitive data.",
],
correct=[0],
explain="""Task 2.3's logging concern is addressed the same way any other sensitive-data-in-logs
problem is: redact/mask known sensitive patterns before they're persisted, and apply standard
least-privilege access controls to whatever log data remains — AI service call logs aren't exempt
from the general Task 2.2/2.3 principle of not persisting PII in plaintext where it isn't needed and
isn't tightly access-controlled.""",
wrong={
1: "Logging is valuable for debugging and support quality; the documented fix is redaction/access control, not eliminating all observability for the feature.",
2: "CloudWatch Logs is a general-purpose log store with no built-in PII exemption or automatic redaction — storing PII there in plaintext carries the same compliance exposure as storing it in any other unprotected store.",
3: "User input is exactly where users are described as pasting PII (account numbers) in this scenario — restricting redaction to only the model's output would miss the actual source of the sensitive data described.",
},
links=[D("domain-2-security/ai-service-security-risks.md"), L("management-governance/cloudwatch.md")]),

dict(stem="""A company deploys a Bedrock Agent that can call two action groups: one that looks up
order status (read-only) and one that issues refunds (a real financial action). A penetration test
successfully tricks the agent, via a crafted user message, into attempting to call the refund
action group when the user only asked a status question. The refund call fails only because the
agent's own execution role happens to lack `lambda:InvokeFunction` on that specific action group's
function. What does this near-miss indicate about the deployment, and what is the correct fix,
per Task 2.3's "AI agent security" guidance?""",
multi=False,
options=[
"The agent's IAM execution role is currently under-scoped in a way that accidentally saved the day, but the deployment should not rely on accidental permission gaps — explicitly and deliberately scope the agent's role to only the action groups a given use case legitimately needs (here, likely read-only order status only, with refunds handled through a separate, more tightly gated flow), and add Guardrails/input validation so manipulated prompts are also rejected before ever reaching the point of attempting an unauthorized tool call.",
"Nothing needs to change, since the call ultimately failed and no refund was issued.",
"Grant the agent's role full permissions on both action groups, since restricting permissions caused this near-miss and more permissions would have avoided the confusing error.",
"Disable IAM entirely for Bedrock Agents, since IAM evidently interfered with the agent's ability to do its job.",
],
correct=[0],
explain="""This is exactly Task 2.3's "AI agent security" principle in action: an agent should
never be *able* to attempt actions beyond its intended scope, and relying on an incidental,
undocumented permission gap to prevent real damage is not a security control — it's luck. The
correct fix is deliberate least-privilege scoping of the agent's execution role (so sensitive
actions like refunds simply aren't reachable from a status-inquiry use case) combined with
guardrails/input handling so manipulated prompts are also caught before an unauthorized tool call
is even attempted.""",
wrong={
1: "Treating an accidental permission gap as 'working as intended' ignores that the agent was successfully manipulated into attempting an unauthorized action — the control that happened to stop it wasn't deliberate, and a differently configured role (or a different exploited action group) could easily have succeeded.",
2: "Granting full permissions on both action groups removes the only thing that currently prevents the successful exploit from actually completing — this is the opposite of the correct fix.",
3: "IAM scoping is precisely the control that limited the blast radius here; removing it entirely would make a successful prompt-injection exploit fully effective rather than blocked.",
},
links=[D("domain-2-security/ai-service-security-risks.md"), L("machine-learning-ai/bedrock.md")]),
]

E2_D3 = [
dict(stem="""A team defines infrastructure as AWS CDK (TypeScript) constructs. Before every deploy,
they want to catch issues like a security group allowing unrestricted inbound SSH, or an S3 bucket
missing encryption, as part of CI — ideally before `cdk deploy` ever runs, using rules that can be
customized for the organization's own security standards (not just generic CloudFormation syntax
validity). What should they add to the pipeline?""",
multi=False,
options=[
"A CDK-aware static analysis/linting step (e.g. `cdk-nag`, run against the synthesized CloudFormation template or directly against CDK constructs) as a CI stage after `cdk synth` and before `cdk deploy`, failing the build if a defined security rule (like 'no 0.0.0.0/0 on port 22') is violated.",
"Rely solely on `cdk synth` succeeding, since successful synthesis guarantees the infrastructure is secure.",
"Manually review every CDK diff by eye before every deployment, with no tooling.",
"Wait for AWS Config to flag the problem after the resources are already deployed to production.",
],
correct=[0],
explain="""This is Task 3.2's "validate infrastructure templates before deploying" extended to
custom organizational security rules: a CDK-aware static analysis tool (synthesizing the template
and checking it, or checking constructs directly) run in CI catches issues like overly permissive
security groups or missing encryption *before* `cdk deploy` ever executes — exactly matching
"customizable rules, pre-deploy, in CI" rather than generic syntax checking or after-the-fact
detection.""",
wrong={
1: "`cdk synth` only confirms the CDK app can successfully produce valid CloudFormation syntax — it says nothing about whether the resulting resources follow security best practices.",
2: "Manual review doesn't scale, is inconsistent, and is exactly the kind of check that should be automated and enforced in CI rather than left to individual diligence.",
3: "Catching the misconfiguration only after it's already live in production (via AWS Config) is reactive, not preventive — the question specifically asks for a pre-deploy check.",
},
links=[L("management-governance/cdk.md"), D("domain-3-testing-deployment/README.md")]),

dict(stem="""A developer wants a disposable, pre-configured cloud development environment with the
AWS CLI, SDKs, and a code editor already set up, accessible from any browser, to avoid "works on
my machine" setup drift across a team of contractors who each only need the environment for a few
weeks. Which AWS service is designed for this, as opposed to each contractor configuring their own
local machine?""",
multi=False,
options=[
"AWS Cloud9 — a cloud-based IDE accessible via browser, pre-configured with AWS CLI credentials tied to the launching user's role, requiring no per-contractor local environment setup, and easy to tear down when the engagement ends.",
"Amazon EC2 with no further configuration, since a bare EC2 instance already includes a browser-based IDE by default.",
"AWS CloudShell, which permanently persists all installed custom packages and tools indefinitely with no storage limit.",
"Amazon WorkSpaces, which is a service exclusively for watching streaming video content.",
],
correct=[0],
explain="""Cloud9 is specifically a managed, browser-accessible cloud IDE that comes pre-configured
with the AWS CLI/SDKs and credentials scoped to the user's role — exactly the "no local setup,
consistent environment, easy to provision/tear down per contractor" requirement, standing in
contrast to each person configuring their own machine from scratch.""",
wrong={
1: "A bare EC2 instance has no IDE pre-installed by default; that capability specifically comes from a service like Cloud9 layered on top.",
2: "CloudShell is a browser-based shell with the AWS CLI pre-authenticated, but its persistent storage is limited (1 GB home directory) and it's meant for quick CLI tasks, not a full persistent development environment with an IDE — this statement also mischaracterizes it as having no storage limit.",
3: "Amazon WorkSpaces provides managed virtual desktops; it is not a video-streaming service — this statement is factually wrong about what WorkSpaces does.",
},
links=[L("developer-tools/cloud9-and-cloudshell.md")]),

dict(stem="""A team's CodePipeline deploys a CloudFormation stack. A recent incident revealed that
a stack update unintentionally replaced (destroyed and recreated) a stateful RDS instance because
a property change triggered implicit resource replacement, causing data loss. The team wants this
caught automatically in the pipeline before any such destructive change reaches production. What
should be added?""",
multi=False,
options=[
"A pipeline stage that creates a CloudFormation change set from the proposed template and inspects its output programmatically (or via a manual approval gate shown the change set) specifically checking for any resource marked for `Replacement: True`/`Conditional` on stateful resources, failing/pausing the pipeline if found.",
"Nothing — CloudFormation never replaces a resource unless the developer explicitly requests it via a separate, distinct API call.",
"Remove CloudFormation entirely and manage all infrastructure via the console to avoid replacement risk.",
"Increase the RDS instance's backup retention period, which prevents CloudFormation from ever replacing the instance.",
],
correct=[0],
explain="""Change sets expose exactly this information — per-resource action (`Add`/`Modify`/
`Remove`) and, critically, whether a `Modify` requires replacement — so a pipeline stage that
inspects (or gates manual approval on) the change set's replacement indicators before executing it
catches exactly this class of destructive-update-by-accident, directly addressing Task 3.2's
"validate infrastructure templates before deploying them" for a stateful-resource safety case.""",
wrong={
1: "This is false — many property changes on resources like RDS instances (e.g. changing certain parameters) implicitly require CloudFormation to replace the resource; this isn't a separate explicit action the developer must request, which is exactly what caused the incident.",
2: "Abandoning CloudFormation for manual console management reintroduces all the drift/consistency/audit problems IaC solves, as an overcorrection to a solvable pipeline gap.",
3: "Backup retention period affects how far back restorable backups exist; it has no bearing on whether a CloudFormation update triggers resource replacement.",
},
links=[L("management-governance/cloudformation.md"), D("domain-3-testing-deployment/README.md")]),

dict(stem="""A containerized microservice built in CI needs to be shared with a partner
organization's separate AWS account so their pipeline can pull and deploy the exact same image,
without making the image publicly accessible to the entire internet. What should be configured on
the ECR repository?""",
multi=False,
options=[
"An ECR repository policy granting the partner's specific AWS account (or IAM principal ARN) `ecr:GetDownloadUrlForLayer`, `ecr:BatchGetImage`, and `ecr:BatchCheckLayerAvailability` permissions on that repository, scoping cross-account pull access to exactly that account.",
"Make the ECR repository fully public, since that is the only way to share an image across AWS accounts.",
"Export the image as a `.tar` file and email it to the partner organization's team.",
"Grant the partner account `AdministratorAccess` in the account that owns the ECR repository.",
],
correct=[0],
explain="""ECR repository policies are resource-based policies specifically for granting
cross-account pull (or push) access to a named external account/principal, scoped to exactly the
pull-related actions needed — satisfying "shared with one partner account, not the whole internet"
precisely, without resorting to public visibility or over-granting broad account access.""",
wrong={
1: "Making a repository public exposes the image to anyone on the internet, which is explicitly the opposite of the stated requirement to share with just one partner.",
2: "Emailing a tarball is manual, doesn't scale, loses version/tag integrity, and isn't how a CI/CD pipeline should consume container images.",
3: "Granting `AdministratorAccess` to an external account is a massive, unnecessary over-grant just to let them pull one image — repository-scoped pull permissions are both sufficient and far safer.",
},
links=[L("containers/ecr.md")]),

dict(stem="""A Lambda-based API's test suite currently only runs locally on developers' machines
before they manually deploy, with no consistency guarantee that the same tests ran before a given
production deploy. The team wants every deployment to `prod` to be provably gated on that
specific commit's automated test suite passing, as an unskippable step, not a developer's manual
habit. What should be restructured in the pipeline?""",
multi=False,
options=[
"Move the test execution into a CodeBuild stage inside CodePipeline, positioned before the production deployment stage, so the pipeline itself (not a developer's local habit) runs the tests for that exact commit and the pipeline cannot proceed to the deploy stage unless that CodeBuild stage reports success.",
"Keep tests local-only but add a Slack reminder asking developers to 'please run tests before deploying.'",
"Move testing to occur only after the production deployment completes, as a post-deploy smoke test with no gating effect.",
"Require developers to attach a screenshot of their local test run output to the pull request description as proof.",
],
correct=[0],
explain="""Moving test execution into a pipeline stage (CodeBuild within CodePipeline) makes
passing tests a structural precondition for reaching the deploy stage — the pipeline itself
enforces the gate for the exact commit being deployed, which is fundamentally different from (and
far more reliable than) relying on a developer's local habit or an easily-skipped manual step.""",
wrong={
1: "A reminder is not an enforced gate — it relies entirely on developer discipline and can be silently skipped, which is exactly the unreliability the team wants to eliminate.",
2: "Testing only after production deployment doesn't prevent a broken build from reaching production in the first place — it's detection after the fact, not a gate.",
3: "A screenshot is unverifiable, easy to fake or be stale, and isn't tied programmatically to the specific commit being deployed — it's not a real automated gate.",
},
links=[L("developer-tools/codepipeline.md"), L("developer-tools/codebuild.md"), D("domain-3-testing-deployment/README.md")]),

dict(stem="""A Lambda function's deployment currently replaces 100% of traffic on the alias
immediately (`AllAtOnce`), and a recent bad deploy caused every request to fail for several
minutes before anyone noticed and manually rolled back. The team wants new deployments to shift
traffic gradually in linear increments over 10 minutes, with CloudWatch-alarm-triggered automatic
rollback so a bad deploy affects only a small percentage of traffic briefly rather than everyone.
What CodeDeploy configuration achieves this?""",
multi=False,
options=[
"A CodeDeploy `Linear` deployment configuration for Lambda (e.g. `Linear10PercentEvery1Minute`), which shifts an additional fixed percentage of traffic to the new version at each defined interval, combined with a CloudWatch alarm attached to the deployment group so a triggered alarm automatically halts and rolls back the shift mid-way.",
"Switching the alias's traffic-shifting configuration manually to a new fixed number every few minutes, watching metrics by eye, with no CodeDeploy involvement.",
"Keeping `AllAtOnce` but simply reducing the Lambda function's memory, since smaller functions deploy more safely.",
"Running the exact same deployment five times in a row.",
],
correct=[0],
explain="""CodeDeploy's `Linear` deployment type for Lambda shifts traffic in equal, scheduled
increments (e.g. 10% every minute) rather than all at once, and wiring a CloudWatch alarm to the
deployment group means a detected regression automatically halts the shift and rolls back — exactly
turning "100% blast radius immediately" into "small, bounded exposure with automatic protection,"
addressing both the gradual-shift and automatic-rollback requirements in one configuration.""",
wrong={
1: "Manual traffic adjustment with eyeballed metrics reintroduces the exact unreliable, slow-to-react manual rollback process that caused the incident described.",
2: "Memory size has no relationship to deployment traffic-shifting strategy or blast radius during a bad release.",
3: "Repeating the same deployment doesn't change its traffic-shifting behavior at all; it's an irrelevant action.",
},
links=[L("developer-tools/codedeploy.md"), L("compute/lambda.md")]),

dict(stem="""A team's CloudFormation template currently stores a third-party API key as a plain
string `Default` value in a template `Parameter`, which means it's visible in the CloudFormation
console's parameter history and in the template source committed to version control. They need to
reference this secret from a resource's configuration without ever exposing the plaintext value in
the template, console history, or source control. What should they use instead?""",
multi=False,
options=[
"A CloudFormation dynamic reference to Secrets Manager (e.g. `{{resolve:secretsmanager:MySecretId:SecretString:apiKey}}`) inside the resource property, which CloudFormation resolves at deploy/update time without ever writing the resolved plaintext value into the template, parameter history, or any stored stack configuration that a casual viewer could see.",
"Keep the plaintext default value in the template but add a code comment saying 'DO NOT SHARE THIS FILE.'",
"Base64-encode the API key before putting it in the template's `Default` value, since Base64 is a form of encryption.",
"Store the key in a `NoEcho` parameter with no other change, since `NoEcho` fully removes the value from all storage and history everywhere.",
],
correct=[0],
explain="""Dynamic references to Secrets Manager (or SSM Parameter Store) are exactly
CloudFormation's documented mechanism for this: the template contains only a reference string, not
the secret, and CloudFormation resolves the actual value at deploy time without persisting the
plaintext into the template, change set, or certain parts of the stack's stored configuration —
directly satisfying "never in source control or template" for the actual secret value.""",
wrong={
1: "A comment is not a technical control and does nothing to prevent the plaintext key from being stored in the template and version control history, where it already is.",
2: "Base64 is an encoding, not encryption — it is trivially reversible and provides no actual confidentiality; this is a common, important exam distinction.",
3: "`NoEcho` masks a parameter value from being *displayed* in the console/CLI output, but the underlying template would still need to not contain the plaintext secret as a literal `Default`; `NoEcho` alone, without also removing the literal secret from the template, is an incomplete fix and is commonly over-trusted.",
},
links=[L("security-identity-compliance/secrets-manager-vs-parameter-store.md"), L("management-governance/cloudformation.md")]),

dict(stem="""A developer wants to simulate how their Lambda function responds to an SNS-triggered
event, entirely offline, feeding it a realistic sample SNS notification payload shaped exactly like
what SNS would actually deliver, to catch a parsing bug before ever deploying to AWS. What SAM CLI
feature/workflow supports this specific scenario?""",
multi=False,
options=[
"`sam local invoke` with a generated or hand-crafted SNS-shaped test event JSON file (SAM/AWS provides sample event templates for common triggers like SNS, S3, and SQS) passed via `--event`, invoking the handler locally against that exact payload shape.",
"`sam local invoke` always generates a random, unpredictable test event automatically, with no way to control its shape.",
"Deploy the function to production first and trigger a real SNS notification, since local testing cannot replicate SNS's exact payload shape.",
"`sam package`, which is specifically designed for local event simulation rather than packaging.",
],
correct=[0],
explain="""`sam local invoke --event <file>` is exactly built for feeding a crafted or
template-based test event (SAM ships sample event payload templates per trigger type, including
SNS) into a locally-run handler, letting a developer validate parsing/handling logic against a
realistic payload shape without deploying anything — directly matching Task 3.2's "use mock APIs
and test events to exercise Lambda functions without live dependencies.\"""",
wrong={
1: "The event payload is explicitly developer-supplied via the `--event` flag (or stdin); it is not randomly generated, which is what makes this command useful for targeted, repeatable testing.",
2: "Deploying to production just to test event-handling logic is unnecessary, slow, and risky compared to local testing with a representative test event — exactly what SAM's local tooling avoids.",
3: "`sam package` prepares and uploads a deployment artifact for an actual deployment; it has nothing to do with locally simulating event invocations.",
},
links=[L("developer-tools/sam.md")]),

dict(stem="""A `buildspec.yml` needs to build and push a Docker image to ECR as part of a
CodeBuild stage. The build environment requires access to the Docker daemon (to run `docker build`
and `docker push`), which is not available by default in a standard CodeBuild environment. What
setting must be enabled on the CodeBuild project for this to work?""",
multi=False,
options=[
"Enable privileged mode on the CodeBuild project, which starts a Docker daemon inside the build container so `docker build`/`docker push` commands can run; without it, Docker-in-Docker operations fail.",
"No special configuration is needed — every CodeBuild environment has a running Docker daemon by default with no flags required.",
"Switch the source provider from CodeCommit to GitHub, since Docker builds only work with GitHub-sourced CodeBuild projects.",
"Increase the CodeBuild project's compute type to the largest available size, which automatically enables Docker support.",
],
correct=[0],
explain="""Privileged mode is specifically documented as required when a CodeBuild buildspec
needs to interact with a Docker daemon (building/pushing images) — it's an explicit opt-in project
setting precisely because running a nested Docker daemon needs elevated container privileges that
aren't granted by default.""",
wrong={
1: "This is incorrect — building/pushing Docker images from CodeBuild specifically fails with daemon-connection errors unless privileged mode is enabled; it is not a default-on capability.",
2: "Docker build support is unrelated to which source provider (CodeCommit, GitHub, S3, etc.) triggers the build; this is a red herring not tied to the actual requirement.",
3: "Compute type (general1.small/medium/large, etc.) affects CPU/memory available to the build, not whether a Docker daemon is running inside the container — that's specifically privileged mode's job.",
},
links=[L("developer-tools/codebuild.md"), L("containers/ecr.md")]),

dict(stem="""A team's CodePipeline source stage currently only triggers on pushes directly to
`main`. They've adopted a trunk-based workflow where short-lived feature branches are merged via
pull request, and want a **separate**, lower-stakes pipeline to run build and unit tests (but not
deploy anywhere) on every push to any feature branch, distinct from the main pipeline that builds,
tests, and deploys to production from `main`. What is the correct way to structure this?""",
multi=False,
options=[
"Create a second, separate CodePipeline (or CodeBuild project triggered independently) whose source stage filters on feature branch pushes/pull requests, running only build+test stages with no deployment stages at all — kept entirely distinct from the main-branch pipeline that includes production deployment stages.",
"Add a `main`-only conditional inside the existing production pipeline's deploy stage that silently no-ops when triggered from a feature branch, while keeping everything else about the single pipeline identical.",
"Rename the feature branches to `main` temporarily whenever they need to be tested, then rename them back.",
"Disable the production pipeline entirely whenever any feature branch exists in the repository.",
],
correct=[0],
explain="""A genuinely separate pipeline (or independently triggered CodeBuild project) scoped to
feature branches, containing only build/test stages with no deployment capability at all, cleanly
separates "lower-stakes CI for in-progress work" from "the pipeline that can reach production" —
avoiding any risk that a feature-branch trigger could accidentally exercise a production deployment
stage, which a single shared pipeline with conditional logic risks if the condition is ever
misconfigured.""",
wrong={
1: "A single pipeline with a silent conditional no-op for deployment still includes the deploy stage's permissions/configuration in a pipeline that feature-branch pushes can trigger — a misconfigured condition could accidentally deploy from a feature branch, which a fully separate pipeline avoids structurally.",
2: "Renaming branches as a workaround is operationally absurd and doesn't actually create the described separate, lower-stakes CI process.",
3: "Disabling the entire production pipeline whenever any feature branch exists would block legitimate production deployments constantly, since feature branches typically exist most of the time in active development.",
},
links=[L("developer-tools/codepipeline.md"), L("developer-tools/codecommit.md")]),

dict(stem="""A legacy application packaged as a container needs to run on AWS with the team
explicitly wanting to avoid managing any EC2 instances or Kubernetes control plane at all, while
still using standard ECS task definitions and standard Docker images with no Kubernetes-specific
tooling required. Which combination satisfies this?""",
multi=False,
options=[
"Amazon ECS with the Fargate launch type — ECS's own (non-Kubernetes) task definition model, with Fargate eliminating any EC2 instance or control-plane management for the team.",
"Amazon EKS with the Fargate launch type, since EKS is required whenever Fargate is used.",
"Amazon ECS with the EC2 launch type, since Fargate requires at least one self-managed EC2 instance as a control node.",
"AWS Lambda, since Lambda supports standard ECS task definitions directly with no changes needed.",
],
correct=[0],
explain="""ECS with Fargate is exactly the combination for "container orchestration, zero EC2/
control-plane management, no Kubernetes tooling required": ECS has its own task-definition model
entirely separate from Kubernetes, and the Fargate launch type removes all EC2 instance management
for either ECS or EKS — but since no Kubernetes API/tooling is wanted here, plain ECS (not EKS) is
the right orchestrator.""",
wrong={
1: "Fargate is available as a launch type for *both* ECS and EKS — it does not require EKS specifically, and choosing EKS here would needlessly introduce the Kubernetes API/tooling the requirement explicitly wants to avoid.",
2: "This is backwards — Fargate's entire purpose is to remove the need for any self-managed EC2 instances; the EC2 launch type (not Fargate) is the one that requires the team to manage EC2 instances themselves.",
3: "Lambda has its own packaging/invocation model (ZIP or Lambda-specific container image contract) and does not directly run standard ECS task definitions — this statement is factually incorrect.",
},
links=[L("containers/ecs.md"), L("containers/fargate.md"), L("containers/containers-vs-vms-vs-serverless.md")]),

dict(stem="""A team wants AI assistance reviewing every pull request's code changes for common
issues (missing error handling, potential null dereferences, inconsistent naming) before a human
reviewer looks at it, to surface likely problems faster — but they explicitly do not want AI review
comments to auto-merge a PR or override a human reviewer's final approval decision. How should this
be integrated into the PR workflow, consistent with the documented AI-assisted development pattern?""",
multi=False,
options=[
"Add the AI review as an automated comment/check on the PR (e.g. triggered by the same CI event that runs tests) that surfaces suggestions for the human reviewer's attention, while keeping required human approval as the actual merge gate — AI augments and accelerates the review, but a human still makes the final call.",
"Configure the AI review tool to automatically approve and merge any PR it doesn't flag issues on, removing human reviewers from the loop entirely.",
"Disable human code review entirely now that an AI reviewer exists, since the AI covers everything a human would have checked.",
"Have the AI review silently rewrite the PR's code to fix issues it finds, merging its own changes without the original author's or reviewer's involvement.",
],
correct=[0],
explain="""This matches the documented AI-assisted development pattern across every domain it
appears in (code review, test generation, deployment approvals, error analysis): AI accelerates
and surfaces useful signal, but a human remains the actual decision-maker/gate — here, that means
AI comments inform the reviewer rather than AI output automatically merging code or replacing the
human approval requirement.""",
wrong={
1: "Auto-merging based solely on an AI tool's silence removes the human-in-the-loop safeguard entirely, risking merged code that an AI tool simply failed to flag an issue in.",
2: "Fully removing human review assumes AI review is a complete substitute for human judgment, which is explicitly not the documented pattern — AI assists, it doesn't replace the human reviewer.",
3: "Letting an AI tool silently commit its own fixes without author/reviewer involvement bypasses the entire review process and accountability chain for a code change.",
},
links=[D("domain-1-development/ai-assisted-development.md"), D("domain-3-testing-deployment/README.md")]),

dict(stem="""A team's Lambda functions are currently packaged with every dependency bundled
directly into each function's own deployment .zip, even though five functions share the exact same
50 MB set of third-party libraries. Deployment packages are slow to upload and the team wants to
both shrink each function's own package and have a single place to patch a shared library version
across all five functions at once, without switching to container images. What should they do?""",
multi=False,
options=[
"Extract the shared dependencies into a Lambda layer, publish it once, and attach that layer version to all five functions — each function's own deployment package then only contains its unique handler code, and bumping the shared library means publishing one new layer version instead of re-uploading five full packages.",
"Duplicate the 50 MB of dependencies into each of the five functions' packages, since Lambda has no mechanism for sharing code across functions without switching to containers.",
"Zip all five functions together into a single deployment package with one shared `handler.py` that dispatches by Lambda context, to avoid the problem entirely.",
"Store the dependencies in an S3 bucket and require each function to re-download and reinstall all 50 MB from S3 on every single invocation.",
],
correct=[0],
explain="""This is exactly Task 3.1's "dependency management (bundling, layers, lockfiles)"
scenario: a layer is the correct zip-based mechanism for sharing dependencies across multiple
functions, shrinking each function's own package to just its unique code, and centralizing
version bumps to one layer publish rather than five separate full re-uploads.""",
wrong={
1: "This claim is false — layers are precisely Lambda's built-in zip-based code-sharing mechanism, which does not require switching to container image packaging at all.",
2: "Merging five independent functions into one package with manual dispatch logic conflates unrelated responsibilities, loses independent scaling/permissions/versioning per function, and doesn't actually solve the shared-dependency-versioning problem described.",
3: "Re-downloading 50 MB from S3 on every single invocation adds significant latency to every cold *and* warm invocation and is far worse than a layer, which is attached once per execution environment lifecycle, not re-fetched per call.",
},
links=[L("compute/lambda.md"), D("domain-3-testing-deployment/README.md")]),

dict(stem="""A CDK app currently defines all resources for `dev`, `staging`, and `prod`
environments in a single, monolithic stack with hardcoded environment-specific values scattered
throughout the code via `if` statements, making it error-prone to tell which environment a given
`cdk deploy` will actually target. The team wants a cleaner, safer pattern for managing multiple,
clearly distinguished environment deployments from the same CDK codebase. What should they use?""",
multi=False,
options=[
"Separate CDK Stack instances per environment (e.g. a reusable `Stack` subclass instantiated once per environment with environment-specific props/context), each explicitly deployed with its own `env` (account/Region) and distinguishing context values (e.g. via `cdk deploy MyStack-dev` or `cdk deploy MyStack-prod`), rather than branching logic inside one shared stack based on ambient state.",
"Keep the single monolithic stack exactly as-is, since CDK has no concept of multiple stacks in one app.",
"Hardcode the production AWS account ID as the default for every deploy, and require developers to remember to override it manually for dev/staging every single time.",
"Deploy to production only by directly editing resources in the CloudFormation console after a dev deployment, bypassing CDK for prod entirely.",
],
correct=[0],
explain="""CDK explicitly supports multiple Stack instances within one app, parameterized by
environment-specific props/context and each targeting an explicit `env` (account/Region) —
instantiating one Stack subclass per environment with clear, explicit names (rather than branching
on ambient state inside a single shared stack) is the documented pattern for making "which
environment am I about to deploy to" unambiguous and reduces the risk of accidentally deploying
dev-shaped resources to prod or vice versa.""",
wrong={
1: "CDK apps commonly define many Stack instances; this statement is factually wrong about CDK's capabilities.",
2: "Defaulting to production and requiring manual override for every non-prod deploy is backwards and dangerous — the safer default is the opposite, or (better) explicit, unambiguous stack identifiers per environment as described in the correct answer.",
3: "Manually editing resources in the console for production specifically reintroduces drift between CDK's view of the stack and reality, undermining IaC entirely for the most important environment.",
},
links=[L("management-governance/cdk.md"), D("domain-3-testing-deployment/README.md")]),
]

E2_D4 = [
dict(stem="""A production incident report needs to answer: "across all Lambda functions in this
application, which specific function and which specific log line first mentioned the string
`DatabaseConnectionTimeout` in the last 6 hours?" The team has 12 different Lambda functions, each
with its own log group. What is the fastest way to answer this without opening each log group one
by one?""",
multi=False,
options=[
"A single CloudWatch Logs Insights query run across all 12 log groups simultaneously (Logs Insights supports querying multiple log groups in one query), filtering for the exact string and sorting by `@timestamp` ascending to surface the first occurrence.",
"Open each of the 12 log groups' consoles in 12 separate browser tabs and manually scan each one.",
"Export every log group's full contents to a local file and use a text editor's 'Find in Files' across all 12 files.",
"Assume the error always originates in the same function every time, since errors are deterministic.",
],
correct=[0],
explain="""Logs Insights explicitly supports selecting multiple log groups for a single query, so
one query — filtering for the exact error string and sorting by timestamp — searches all 12
functions' logs simultaneously and surfaces the earliest matching line directly, which is both the
fastest and most reliable approach for a cross-function root-cause timeline question like this.""",
wrong={
1: "Manually scanning 12 separate consoles one at a time is slow, error-prone, and doesn't easily let you compare exact timestamps across functions to determine which came first.",
2: "Exporting and searching locally works but is slower and more manual than a single Insights query that already runs server-side across all the specified log groups at once.",
3: "Assuming deterministic origin without evidence is exactly the kind of unverified guess root-cause analysis should avoid — the question specifically requires finding the actual first occurrence.",
},
links=[L("management-governance/cloudwatch.md"), D("domain-4-troubleshooting-optimization/README.md")]),

dict(stem="""An X-Ray trace shows a `GetUserProfile` request touching four downstream services. The
team wants to tag specific traces with a business-relevant value (`customerId`) so they can later
filter and search traces in the X-Ray console for a specific customer's requests, in addition to
attaching non-searchable debug context (like the full raw request object) to the same trace
segment for engineers reviewing it by hand. Which two X-Ray concepts map to these two needs?""",
multi=False,
options=[
"Annotations — key-value pairs that are indexed and can be used to filter/search traces in the X-Ray console (e.g. `customerId`) — and metadata — arbitrary additional data attached to a segment that is *not* indexed/searchable but is still visible when inspecting a specific trace in detail (e.g. the full raw request object).",
"Annotations and metadata are identical in every way, including both being searchable in the console.",
"Subsegments are the only mechanism for attaching any extra data to an X-Ray trace.",
"X-Ray does not support attaching any custom key-value data to a trace beyond the default segment fields.",
],
correct=[0],
explain="""This is exactly the documented distinction: annotations are indexed and searchable
(the right choice for `customerId`-based trace filtering), while metadata holds richer, non-indexed
context visible when drilling into one specific trace but not usable for search/filter queries —
together they map precisely to "searchable business key" + "rich debug context" in this scenario.""",
wrong={
1: "This is factually wrong — the key documented difference between annotations and metadata is specifically that annotations are indexed/searchable and metadata is not; conflating them loses that distinction.",
2: "Subsegments represent timed sub-operations within a segment (e.g. a downstream call); they aren't the mechanism for attaching arbitrary custom key-value data — annotations and metadata are.",
3: "This is factually incorrect — X-Ray explicitly supports both annotations and metadata as customizable fields on segments/subsegments.",
},
links=[D("domain-4-troubleshooting-optimization/observability-instrumentation.md")]),

dict(stem="""A security review of CloudTrail logs over the past week shows an unusually high
volume of `AssumeRole` calls from a single IAM user, far above that user's historical baseline,
though none of the individual calls look obviously malicious on their own. The team wants
automated detection of this kind of statistical/volume anomaly going forward, rather than manually
eyeballing CloudTrail event counts. What CloudTrail feature is designed for this?""",
multi=False,
options=[
"CloudTrail Insights — it automatically analyzes management event patterns (like API call volume) against a learned baseline and surfaces unusual activity (e.g. spikes in a specific API call's volume) as its own type of finding, without requiring a custom query or manual historical comparison.",
"CloudTrail data events, since they are specifically designed for statistical anomaly detection on API call volume.",
"AWS Config, since it tracks volumetric trends in API call counts by default.",
"Manually exporting CloudTrail logs to a spreadsheet every week and eyeballing the row counts.",
],
correct=[0],
explain="""CloudTrail Insights is specifically the feature built for this: it continuously
analyzes a trail's management event activity against an automatically learned baseline and flags
statistically unusual patterns (like an abnormal spike in a particular API call's volume from a
given actor) as Insights events — exactly "automated volume-anomaly detection" rather than a
manual historical comparison.""",
wrong={
1: "Data events add object/resource-level logging granularity (e.g. S3 `GetObject`); they are not themselves a statistical anomaly detection feature — that's specifically Insights.",
2: "AWS Config evaluates resource configuration compliance; it has no concept of API call volume/statistical anomaly detection — that's outside its scope entirely.",
3: "Manual spreadsheet analysis is exactly the non-automated, easily-missed process the team wants replaced with a standing automated capability.",
},
links=[L("management-governance/cloudtrail.md"), D("domain-4-troubleshooting-optimization/README.md")]),

dict(stem="""A Lambda function is consistently throttled with `TooManyRequestsException` during a
sustained traffic spike, and investigation shows the function's reserved concurrency is set
appropriately high already — the actual constraint is the **account-level** concurrent execution
limit being shared across dozens of other unrelated functions in the same account/Region. What is
the correct, officially supported path to resolve this, as opposed to arbitrarily lowering other
functions' concurrency?""",
multi=False,
options=[
"Request a service quota increase for the account's total concurrent executions limit in that Region via the Service Quotas console/API, which raises the shared ceiling rather than redistributing an already-insufficient pool among competing functions.",
"Manually lower every other function's reserved concurrency to zero so this one function gets effectively unlimited concurrency by default.",
"Delete the other, unrelated functions permanently to free up account-level concurrency.",
"Nothing can be done — AWS account concurrency limits are immutable and can never be increased under any circumstances.",
],
correct=[0],
explain="""The account-level concurrent executions limit is a documented, adjustable service
quota — the correct, supported path when the real constraint is total account capacity (not an
individual function's own reserved concurrency) is to request a quota increase through Service
Quotas, which raises the actual shared ceiling rather than cannibalizing capacity from other
legitimate workloads.""",
wrong={
1: "Setting other functions' reserved concurrency to zero would block those functions from executing at all, trading one team's outage for another's — a destructive workaround rather than the supported fix.",
2: "Permanently deleting unrelated functions to free up concurrency for one workload is a drastic, almost certainly unacceptable operational response to a capacity problem that has a proper request-based solution.",
3: "This is factually wrong — AWS account-level service quotas, including concurrent Lambda executions, are explicitly adjustable via a quota increase request; they are not hard, permanent limits.",
},
links=[L("compute/lambda.md"), D("domain-4-troubleshooting-optimization/README.md")]),

dict(stem="""A team wants a single CloudWatch dashboard giving leadership visibility into key
metrics (API error rate, Lambda duration, DynamoDB throttles) across **three separate AWS accounts**
(dev, staging, prod) without requiring leadership to switch accounts in the console or maintain
three separate dashboards. What CloudWatch capability supports this?""",
multi=False,
options=[
"CloudWatch cross-account, cross-Region dashboards (using CloudWatch's account linking / Observability Access Manager) — a dashboard in a designated monitoring account can display metrics sourced from multiple linked member accounts side by side in one view.",
"CloudWatch dashboards are strictly single-account; the team must have leadership log into three separate accounts and view three separate dashboards.",
"Copy and paste metric values manually into a shared spreadsheet from each account's console once a day.",
"Use AWS Budgets, since it natively aggregates CloudWatch metrics across accounts for dashboard purposes.",
],
correct=[0],
explain="""CloudWatch's cross-account observability feature (built on Observability Access Manager
account linking) is specifically designed for exactly this: a central monitoring account's
dashboard can pull in and display metrics/logs/traces from multiple linked source accounts in one
unified view, which is the documented solution for "one dashboard, several accounts" rather than
maintaining duplicate per-account dashboards or forcing account-switching.""",
wrong={
1: "This is factually wrong — CloudWatch explicitly supports cross-account dashboards via account linking; dashboards are not strictly single-account only.",
2: "Manual copy-paste is slow, error-prone, stale almost immediately, and exactly what a native cross-account feature replaces.",
3: "AWS Budgets is a cost-management/alerting tool; it has no role in cross-account CloudWatch metric dashboard aggregation.",
},
links=[L("management-governance/cloudwatch.md")]),

dict(stem="""An application instruments its Lambda functions with the X-Ray SDK, wrapping all
outbound AWS SDK calls for automatic tracing. The team additionally wants X-Ray to capture a
subsegment specifically around a call to a *third-party* (non-AWS) HTTP API, so that a slow
third-party dependency shows up distinctly in the trace timeline rather than being invisible or
lumped into the handler's own segment duration. What should they add?""",
multi=False,
options=[
"Wrap the third-party HTTP call in an explicit X-Ray subsegment (e.g. using the SDK's `captureHTTPsGlobal`/manual subsegment API, or a custom `beginSubsegment`/`endSubsegment` pair around the call) so that call's duration is recorded and displayed as its own distinct, labeled block in the trace timeline.",
"Do nothing additional — X-Ray automatically instruments every outbound HTTP call to any domain, AWS or third-party, with zero configuration.",
"Switch the third-party API call to use the AWS SDK instead, since only AWS SDK calls can ever appear in an X-Ray trace.",
"Disable X-Ray entirely, since it can only trace calls between AWS services and never third-party dependencies.",
],
correct=[0],
explain="""X-Ray's automatic SDK instrumentation specifically covers calls made through the AWS
SDK; capturing a non-AWS HTTP call as its own visible subsegment requires explicitly wrapping that
call (via the SDK's HTTP capture helpers or manual subsegment begin/end calls) — this is the
documented way to make a third-party dependency's latency visible and attributable in the trace
timeline rather than invisible or folded into the parent segment's total duration.""",
wrong={
1: "Automatic instrumentation specifically covers the AWS SDK clients it wraps; a third-party HTTP call to a non-AWS domain needs to be explicitly captured to show up as its own subsegment — this isn't zero-configuration for arbitrary HTTP calls.",
2: "A third-party dependency generally can't be meaningfully switched to use the AWS SDK (it's not an AWS service), and this doesn't match the actual mechanism X-Ray provides for capturing arbitrary HTTP calls as subsegments.",
3: "X-Ray explicitly supports capturing calls to non-AWS HTTP endpoints as subsegments via its HTTP capture helpers; this statement is factually wrong about X-Ray's capability.",
},
links=[D("domain-4-troubleshooting-optimization/observability-instrumentation.md")]),

dict(stem="""An AWS Config conformance pack is deployed across an Organization to continuously
check that every account's resources comply with a defined baseline (encryption enabled, no
public S3 buckets, etc.). A new account is provisioned and, 10 minutes later, a developer creates
a non-compliant public S3 bucket. What is the expected behavior, and how does this differ from a
one-time compliance audit script run manually once a quarter?""",
multi=False,
options=[
"The conformance pack's underlying Config rules evaluate the new bucket's configuration automatically and flag it as non-compliant close to real-time (as the resource's configuration is recorded), rather than waiting for the next scheduled manual audit — meaning drift is caught within minutes/hours of occurring instead of up to a full quarter later.",
"Conformance packs only evaluate resources that existed at the moment the pack was deployed; resources created afterward are never evaluated.",
"A quarterly manual script and a Config conformance pack are functionally identical in detection latency, since both ultimately just check the same resource properties.",
"Conformance packs require the developer to manually trigger an evaluation via the console after creating each resource.",
],
correct=[0],
explain="""Config's continuous evaluation model (which conformance packs bundle as a reusable set
of rules) is specifically designed to flag new or changed resources as their configuration is
recorded, not just resources that existed at deployment time — this is the core distinction from
a periodic manual audit, which could leave a non-compliant resource undetected for up to the full
audit interval (here, up to a quarter) rather than minutes to hours.""",
wrong={
1: "This is factually wrong — Config rules (including those in a conformance pack) evaluate newly created and changed resources continuously, not only resources that existed at deployment time.",
2: "This mischaracterizes the actual, meaningfully different detection latency between continuous automated evaluation and an infrequent manual audit — they are not functionally identical in practice.",
3: "Config evaluation runs automatically based on configuration-change events (and periodically); it does not require a developer to manually trigger an evaluation after every resource creation.",
},
links=[L("management-governance/aws-config.md"), D("domain-4-troubleshooting-optimization/README.md")]),

dict(stem="""A read-heavy application queries DynamoDB directly for individual item lookups by
primary key, and the team wants to add a cache layer specifically optimized for microsecond-level
read latency in front of DynamoDB, without re-architecting the application's DynamoDB API calls
(`GetItem`/`Query`) or introducing a general-purpose caching service that would need its own
separate cache-invalidation logic written by hand. What AWS service is purpose-built for this exact
case?""",
multi=False,
options=[
"Amazon DynamoDB Accelerator (DAX) — a DynamoDB-specific, in-memory caching layer that is API-compatible with the DynamoDB SDK calls the application already makes, automatically handling cache population/invalidation for `GetItem`/`Query`/`Scan` without the application writing custom cache logic.",
"Amazon ElastiCache for Redis, requiring the application to be rewritten to call a separate Redis client and manually implement cache-aside logic including invalidation.",
"Amazon CloudFront, since it caches DynamoDB API responses automatically by default.",
"AWS Global Accelerator, which caches database query results at the network layer.",
],
correct=[0],
explain="""DAX is specifically purpose-built as a DynamoDB-native caching layer: it's
API-compatible with the existing DynamoDB SDK calls (so the application code barely changes),
delivers microsecond read latency, and manages cache population and invalidation internally —
directly matching "no hand-rolled cache-aside logic, no API rewrite, DynamoDB-specific" far more
precisely than a general-purpose cache like ElastiCache would without custom application code.""",
wrong={
1: "ElastiCache for Redis is a valid general-purpose cache, but using it would require the application to switch to a separate client and hand-write cache-aside/invalidation logic — exactly what the requirement explicitly wants to avoid, unlike DAX's drop-in API compatibility.",
2: "CloudFront caches HTTP(S) content at edge locations for content delivery; it has no native integration with or awareness of DynamoDB API calls.",
3: "Global Accelerator improves network routing/availability for application endpoints; it has no database query caching capability at all.",
},
links=[L("database/dynamodb.md"), L("database/elasticache.md")]),

dict(stem="""A team wants to use an AI assistant to analyze AWS Compute Optimizer and Lambda Power
Tuning output and propose specific rightsizing changes (e.g. "reduce this Lambda's memory from
1024 MB to 512 MB," "resize this RDS instance down one size") across dozens of resources, to save
engineering time versus manually reviewing every recommendation. Consistent with the documented
Task 4.3 "AI-assisted optimization recommendations" pattern, what should happen before any of these
changes are actually applied to production resources?""",
multi=False,
options=[
"An engineer reviews the AI-synthesized recommendations against the actual workload's real requirements (including less-obvious factors like burst capacity needs or SLA headroom) and explicitly approves which specific changes to apply, rather than letting the recommendations auto-apply to production untouched.",
"Apply every AI-generated recommendation automatically and immediately to every production resource with no review, since the underlying tools (Compute Optimizer, Power Tuning) are AWS-provided and therefore inherently production-safe to blindly trust.",
"Ignore the AI-assisted analysis entirely and only ever consider optimization recommendations typed by a human from scratch.",
"Apply the recommendations only to the single most expensive resource and skip reviewing the rest entirely, assuming the AI prioritized correctly with no need to check.",
],
correct=[0],
explain="""Exactly like every other AI-assisted pattern tested on DVA-C03 (test generation, deployment
approvals, error analysis), AI-assisted optimization accelerates the *analysis* step — surfacing
candidate changes faster than manual review of every resource — but a human still verifies and
approves before changes hit production, since the AI output can miss context (burst needs, SLA
margins) that only someone with full workload knowledge would catch.""",
wrong={
1: "Blind, no-review auto-application risks introducing real production regressions (e.g. undersizing a Lambda that actually needs burst memory for occasional spikes) — the documented pattern always keeps a human verification step before production changes.",
2: "Dismissing AI-assisted analysis entirely contradicts Task 4.3's explicit inclusion of 'AI-assisted optimization recommendations' as in-scope exam content — the pattern is to use AI assistance *with* review, not to reject it outright.",
3: "Skipping review of most recommendations just because one was applied doesn't constitute verification of the ones actually being changed, and 'assuming the AI prioritized correctly' is exactly the unverified trust the documented pattern says to avoid.",
},
links=[D("domain-4-troubleshooting-optimization/README.md"), D("domain-1-development/ai-assisted-development.md"), L("management-governance/cost-management-tools.md")]),

dict(stem="""A team suspects a specific Lambda function is the root cause of elevated latency in a
distributed checkout flow, but that function doesn't appear anywhere in the X-Ray service map for
these requests, even though CloudWatch Logs confirm the function is definitely being invoked during
checkout. What is the most likely reason the function is invisible in the trace, and the fix?""",
multi=False,
options=[
"Active tracing is not enabled on that specific Lambda function (or its upstream caller isn't passing the trace context/header along), so no segment is being emitted for it — enable active tracing (and ensure trace context propagation, e.g. via the `_X_AMZN_TRACE_ID` env var /SDK, especially across an async invocation boundary) so the function's segment appears in the trace.",
"X-Ray has an undocumented hard limit of 3 functions per trace, and this is simply the 4th function in the chain.",
"The function's logs appearing in CloudWatch means it is automatically included in every X-Ray trace with no separate configuration needed.",
"X-Ray cannot trace Lambda functions at all; it can only trace EC2 and ECS workloads.",
],
correct=[0],
explain="""A function missing from a trace despite being invoked is a classic trace-context-propagation
or tracing-not-enabled problem: X-Ray only emits a segment for a function if active tracing is
turned on for it and the trace ID context is actually propagated to it (which can silently break
across certain async invocation patterns) — CloudWatch Logs confirming invocation doesn't imply
tracing is configured, since logging and tracing are separate, independently configured features.""",
wrong={
1: "There is no such fixed 3-function-per-trace limit in X-Ray; traces can include many more segments than that.",
2: "Logging and tracing are independent systems — appearing in CloudWatch Logs says nothing about whether X-Ray active tracing is enabled for that function or whether trace context reached it.",
3: "X-Ray explicitly supports Lambda tracing (it's one of the most common ways X-Ray is used) in addition to EC2/ECS/other compute; this statement is factually wrong.",
},
links=[D("domain-4-troubleshooting-optimization/observability-instrumentation.md"), L("compute/lambda.md")]),

dict(stem="""A team's nightly batch Lambda function processes a large S3 export and currently runs
at 256 MB memory, taking 9 minutes and frequently coming close to timing out. Profiling shows the
function is almost entirely CPU-bound (JSON parsing and transformation of a large payload) with
very little I/O wait. The team wants to both reduce the risk of timeout and shorten the nightly
run window. What is the most directly applicable lever, given this specific profile?""",
multi=False,
options=[
"Increase the function's memory allocation significantly — since Lambda allocates CPU proportionally to configured memory, and this workload is CPU-bound, more memory should meaningfully reduce wall-clock duration for the CPU-heavy parsing/transformation work, shrinking both the timeout risk and the run window.",
"Increase only the function's timeout setting to 15 minutes, with memory left at 256 MB, since timeout alone determines how much CPU the function gets.",
"Switch the trigger from a scheduled EventBridge rule to an S3 event notification, since trigger type determines available CPU.",
"Reduce the function's memory further to 128 MB to save cost, since cost should always be minimized regardless of workload profile.",
],
correct=[0],
explain="""Because Lambda scales allocated CPU/vCPU proportionally with configured memory, a
CPU-bound workload (as this profiling shows — most time in actual computation, not waiting on I/O)
is exactly the profile where raising memory tends to meaningfully cut wall-clock duration, directly
addressing both "timeout risk" and "shorten the run" in one lever — a much more targeted fix than
adjusting timeout or trigger type, neither of which changes available compute.""",
wrong={
1: "Timeout only controls how long the function is allowed to run before being killed; it does not add CPU or make computation faster — raising it alone doesn't shrink the run window, it just permits a longer one.",
2: "Trigger type (schedule vs. event) determines *when/how* a function is invoked, not how much CPU/memory is allocated to a given invocation — this is unrelated to the performance profile described.",
3: "Blindly minimizing memory ignores the stated CPU-bound profile; for this workload, lower memory would likely make duration (and often even total cost, given the duration/cost tradeoff) worse, not better.",
},
links=[L("compute/lambda.md"), D("domain-4-troubleshooting-optimization/README.md")]),

dict(stem="""A team wants to know, across their entire multi-service application, the actual
dollar cost attributable specifically to one feature ("video transcoding") that spans Lambda, S3,
and a Step Functions workflow, so they can decide whether to keep or deprecate the feature based on
its real infrastructure cost — not the application's total bill, which also includes unrelated
features. What AWS capability enables this kind of feature-level cost attribution?""",
multi=False,
options=[
"Cost allocation tags — apply a consistent tag (e.g. `feature: video-transcoding`) across every resource (Lambda functions, S3 buckets/prefixes where supported, Step Functions state machines) involved in that feature, activate the tag as a cost allocation tag in Billing, then filter Cost Explorer reports by that tag to see attributed spend.",
"AWS Budgets alone, since budgets automatically know which feature each resource belongs to without any tagging.",
"There is no way to attribute cost to a specific feature spanning multiple resource types; AWS only reports total account-level spend.",
"Amazon CloudWatch Logs, since log volume is a direct, built-in substitute for dollar cost with no further configuration.",
],
correct=[0],
explain="""Cost allocation tags are exactly the documented mechanism for this: consistently
tagging every resource involved in a given feature/project (regardless of resource type), then
activating that tag key for cost allocation in Billing, lets Cost Explorer (and Cost and Usage
Reports) break down and filter spend by that tag — enabling exactly the "cost of this one feature
across Lambda + S3 + Step Functions" attribution the team wants.""",
wrong={
1: "Budgets has no automatic knowledge of which resources belong to a feature; it (like Cost Explorer) relies on cost allocation tags or filters to scope spend meaningfully — it doesn't infer feature ownership on its own.",
2: "This is factually wrong — AWS explicitly supports fine-grained cost attribution via tags (and Cost and Usage Reports), specifically for cases like this where spend spans multiple resource types for one logical feature.",
3: "Log volume is not a reliable or direct proxy for dollar cost across heterogeneous resource types (Lambda duration/memory, S3 storage/requests, Step Functions transitions each price differently) — this isn't a valid cost-attribution method.",
},
links=[L("management-governance/cost-management-tools.md")]),

dict(stem="""A team notices a Lambda function occasionally fails with a connection error against
an RDS instance, correlating with times when the RDS instance's `DatabaseConnections` CloudWatch
metric is near its maximum, caused by Lambda scaling out to many concurrent executions each opening
its own new database connection. The team wants to reduce the number of simultaneous database
connections without artificially capping Lambda's ability to scale for the rest of its workload.
What should they add?""",
multi=False,
options=[
"Amazon RDS Proxy — it sits between the Lambda functions and the RDS instance, pooling and multiplexing a smaller number of actual database connections across many concurrent Lambda executions, so a scaling burst doesn't translate 1:1 into a burst of new database connections.",
"Set the Lambda function's reserved concurrency to 1, so only one invocation can ever run at a time across the entire application.",
"Increase the RDS instance's storage size, since more storage directly increases the maximum connection limit.",
"Disable connection reuse entirely in the Lambda handler, opening and closing a brand-new connection on every single invocation.",
],
correct=[0],
explain="""RDS Proxy is purpose-built for exactly this Lambda-to-RDS connection-management
problem: it maintains a pooled set of actual database connections and multiplexes many concurrent
Lambda executions' logical connections over that smaller pool, directly decoupling "how many Lambda
invocations are running" from "how many real database connections exist" — solving the exhaustion
problem without artificially throttling the function's overall concurrency.""",
wrong={
1: "Capping reserved concurrency to 1 would solve the connection problem by destroying the function's ability to scale at all for its entire workload — exactly the tradeoff the question says to avoid.",
2: "Storage size and maximum connection count are different, largely independent RDS parameters; increasing storage does not directly raise the connection ceiling.",
3: "Opening a brand-new connection on every single invocation (no reuse at all) would make the connection-exhaustion problem worse, not better, since even warm execution environments would stop reusing an existing connection.",
},
links=[L("database/rds.md"), L("compute/lambda.md"), D("domain-4-troubleshooting-optimization/README.md")]),

dict(stem="""A team wants to validate, before committing to a production Lambda memory setting,
whether a specific function's duration (and therefore cost) actually improves meaningfully between
512 MB, 1024 MB, and 1536 MB for their real production-like payload — rather than guessing based on
general advice about CPU-bound workloads. What approach gives them concrete, workload-specific
evidence rather than a generic rule of thumb?""",
multi=False,
options=[
"Run the function at each candidate memory setting against a representative test payload (e.g. using the open-source AWS Lambda Power Tuning tool, which automates invoking the function at multiple memory values and reports actual duration/cost for each) and compare the real measured results for this specific function.",
"Pick 1024 MB because it's a commonly cited 'good default' in blog posts, with no testing against this function's actual payload.",
"Assume duration scales exactly linearly with memory for every Lambda function, so testing more than one memory value is unnecessary.",
"Set memory to the account-wide maximum for every function without measuring, since more memory can never make a function slower.",
],
correct=[0],
explain="""Only an actual empirical test against a representative payload (which is exactly what
Lambda Power Tuning automates — invoking at each candidate memory value and reporting real
duration/cost) gives workload-specific evidence; generic advice or blog-post defaults can be wrong
for a given function's specific CPU/I/O profile, which is precisely why the exam's documented
Task 4.3 guidance is to benchmark rather than assume.""",
wrong={
1: "A generic 'common default' ignores this specific function's actual behavior and may be far from its real optimal point — exactly the untested guess the question wants to avoid.",
2: "Duration vs. memory is frequently non-linear and workload-dependent (I/O-bound workloads may see little to no improvement); assuming strict linearity is an unverified and often incorrect assumption.",
3: "More memory does not strictly guarantee faster performance for every workload profile, and it always increases per-GB-second cost — 'always max, never measure' is not a sound strategy and can raise cost without any performance benefit for some workloads.",
},
links=[L("compute/lambda.md"), D("domain-4-troubleshooting-optimization/README.md")]),
]

# =====================================================================
# RENDERING
# =====================================================================
LETTERS = "ABCDE"

def interleave(domain_lists):
    """Weighted round-robin interleave of {domain_num: [questions]} preserving within-domain order,
    spreading each domain's questions evenly across the 65-slot exam (like a real mixed exam)."""
    counts = {d: len(v) for d, v in domain_lists.items()}
    total = sum(counts.values())
    remaining = dict(counts)
    iters = {d: iter(v) for d, v in domain_lists.items()}
    order = []
    for _ in range(total):
        d = max(remaining, key=lambda k: (remaining[k] / counts[k] if counts[k] else 0, -k))
        order.append((d, next(iters[d])))
        remaining[d] -= 1
    return order

def render_questions_md(title, ordered):
    lines = [f"# {title}", ""]
    lines.append("65 questions. Multiple choice (pick ONE) unless a question explicitly says "
                  "**Choose TWO**. No answers are shown in this file — see the matching "
                  "`*-answer-key.md` file after you finish (or after each section if you're "
                  "reviewing, not simulating).")
    lines.append("")
    lines.append("---")
    lines.append("")
    for i, (domain, q) in enumerate(ordered, start=1):
        lines.append(f"## Q{i}")
        lines.append("")
        lines.append(q["stem"].strip())
        lines.append("")
        for j, opt in enumerate(q["options"]):
            lines.append(f"{LETTERS[j]}. {opt}")
            lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)

def render_answer_key_md(title, ordered):
    lines = [f"# {title}", ""]
    lines.append("Correct answer(s), full explanation, and why each distractor is wrong — "
                  "cross-linked to the relevant service/domain docs. Matches the question numbering "
                  "in the companion `*-questions.md` file exactly.")
    lines.append("")
    lines.append("---")
    lines.append("")
    for i, (domain, q) in enumerate(ordered, start=1):
        correct_letters = " and ".join(LETTERS[idx] for idx in q["correct"])
        lines.append(f"## Q{i} — Domain {domain}")
        lines.append("")
        lines.append(f"**Correct Answer: {correct_letters}**")
        lines.append("")
        lines.append(f"**Explanation:** {q['explain'].strip()}")
        lines.append("")
        wrong_idx_sorted = sorted(q["wrong"].keys())
        if wrong_idx_sorted:
            lines.append("**Why the others are wrong:**")
            for idx in wrong_idx_sorted:
                lines.append(f"- {LETTERS[idx]}: {q['wrong'][idx]}")
            lines.append("")
        if q.get("links"):
            lines.append("**Study links:** " + ", ".join(q["links"]))
            lines.append("")
        lines.append("---")
        lines.append("")
    return "\n".join(lines)

def build_exam(domain_dict):
    ordered = interleave(domain_dict)
    return ordered

def write_exam_files(num, domain_dict, out_dir):
    ordered = build_exam(domain_dict)
    assert len(ordered) == 65, f"Expected 65 questions, got {len(ordered)}"
    q_md = render_questions_md(
        f"DVA-C03 Full Mock Exam {num} — Questions", ordered)
    a_md = render_answer_key_md(
        f"DVA-C03 Full Mock Exam {num} — Answer Key", ordered)
    with open(os.path.join(out_dir, f"exam-{num}-questions.md"), "w") as f:
        f.write(q_md)
    with open(os.path.join(out_dir, f"exam-{num}-answer-key.md"), "w") as f:
        f.write(a_md)
    domain_counts = {}
    for d, _ in ordered:
        domain_counts[d] = domain_counts.get(d, 0) + 1
    multi_count = sum(1 for _, q in ordered if q.get("multi"))
    return {
        "questions_lines": q_md.count("\n") + 1,
        "answer_lines": a_md.count("\n") + 1,
        "domain_counts": domain_counts,
        "multi_count": multi_count,
        "total": len(ordered),
    }

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    r1 = write_exam_files(1, {1: E1_D1, 2: E1_D2, 3: E1_D3, 4: E1_D4}, OUT)
    r2 = write_exam_files(2, {1: E2_D1, 2: E2_D2, 3: E2_D3, 4: E2_D4}, OUT)
    print("EXAM 1:", r1)
    print("EXAM 2:", r2)

