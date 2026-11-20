# Domain 3 Labs — Design High-Performing Architectures (Floci)

Setup once: see [`labs-floci/README.md`](../../../labs-floci/README.md). These labs use Kinesis,
DynamoDB, and EC2 — all genuinely emulated by Floci. (Real throughput/latency numbers, ElastiCache,
and CloudFront edge behavior are not meaningfully testable in a local single-node emulator; this
file notes where that applies.)

## Lab 1 — Stream ingestion with Kinesis + Lambda consumer (Task 3.5)

Goal: build the first half of the ingestion pipeline from this domain's architecture diagram —
producers writing into a stream, a consumer processing records as they arrive.

```bash
# 1. Create a Kinesis data stream
awslocal kinesis create-stream --stream-name iot-events --shard-count 1

# 2. Put a few records in, simulating producers
awslocal kinesis put-record --stream-name iot-events --partition-key device-1 \
  --data '{"deviceId": "device-1", "temp": 21.4}'
awslocal kinesis put-record --stream-name iot-events --partition-key device-2 \
  --data '{"deviceId": "device-2", "temp": 19.8}'

# 3. Read them back the way a consumer would (get a shard iterator, then get-records)
awslocal kinesis get-shard-iterator --stream-name iot-events --shard-id shardId-000000000000 \
  --shard-iterator-type TRIM_HORIZON
awslocal kinesis get-records --shard-iterator <iterator-from-previous-step>
```

Why this matters: this is the exact mechanic behind "Kinesis → Glue/Lambda → S3 data lake" —
practicing shard iterators and polling builds the mental model for why Kinesis consumers (Lambda
event source mappings, KCL apps) work the way they do.

## Lab 2 — DynamoDB throughput modes for performance (Task 3.3)

Goal: compare provisioned vs. on-demand capacity — a direct Task 3.3 performance/scalability
decision.

```bash
# 1. Create a table in on-demand mode (scales automatically, no capacity planning)
awslocal dynamodb create-table --table-name HighTrafficSessions \
  --attribute-definitions AttributeName=sessionId,AttributeType=S \
  --key-schema AttributeName=sessionId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# 2. Write and read items to confirm it behaves normally under PAY_PER_REQUEST
awslocal dynamodb put-item --table-name HighTrafficSessions \
  --item '{"sessionId": {"S": "sess-001"}, "userId": {"S": "u-42"}}'
awslocal dynamodb get-item --table-name HighTrafficSessions --key '{"sessionId": {"S": "sess-001"}}'

# 3. Create a second table in provisioned mode instead, to compare the two models directly
awslocal dynamodb create-table --table-name PredictableWorkload \
  --attribute-definitions AttributeName=sessionId,AttributeType=S \
  --key-schema AttributeName=sessionId,KeyType=HASH \
  --billing-mode PROVISIONED --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

Why this matters: on-demand suits unpredictable, spiky traffic (no capacity planning, scales
instantly); provisioned suits steady, predictable traffic where you can tune capacity precisely
and cheaper — this is the Task 3.3/4.3 overlap between performance and cost.

## Lab 3 — EC2 instance and Auto Scaling for compute elasticity (Task 3.2)

Goal: practice the launch-template/Auto-Scaling-group mechanics behind "elastic compute."

```bash
# 1. Launch an EC2 instance (Floci backs this with real Docker containers)
awslocal ec2 run-instances --image-id ami-00000000 --instance-type t3.micro --count 1

# 2. Create a launch template based on the same config
awslocal ec2 create-launch-template --launch-template-name study-app-lt \
  --launch-template-data '{"ImageId":"ami-00000000","InstanceType":"t3.micro"}'

# 3. Inspect running instances to confirm they're up
awslocal ec2 describe-instances --query 'Reservations[].Instances[].{Id:InstanceId,Type:InstanceType,State:State.Name}'
```

Why this matters: a launch template is what an Auto Scaling group actually scales — practicing
its structure is the foundation for understanding target-tracking scaling policies described in
`ec2-auto-scaling.md` and `compute-performance-decision-framework.md`.

## Lab 4 — Cache-aside pattern with ElastiCache in front of DynamoDB (Task 3.3)

Goal: practice the read-through caching pattern from the domain README's cache-aside diagram —
check the cache first, fall back to the database on a miss, then populate the cache.

```bash
# 1. Create the "database" table
awslocal dynamodb create-table --table-name UserProfiles \
  --attribute-definitions AttributeName=userId,AttributeType=S \
  --key-schema AttributeName=userId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# 2. Seed a row representing a user profile
awslocal dynamodb put-item --table-name UserProfiles \
  --item '{"userId": {"S": "u-42"}, "name": {"S": "Dana"}, "plan": {"S": "pro"}}'

# 3. Create a Redis-compatible cache cluster (Floci emulates ElastiCache control-plane APIs;
#    for the actual read/write cache behavior, a local Redis container stands in — see
#    labs-floci/README.md for the exact setup)
awslocal elasticache create-cache-cluster --cache-cluster-id study-app-cache \
  --cache-node-type cache.t3.micro --engine redis --num-cache-nodes 1

# 4. Simulate the cache-aside read path in application pseudocode:
#      GET user:u-42 from Redis
#      IF miss: DynamoDB GetItem userId=u-42, then SET user:u-42 in Redis with a TTL
#      IF hit: return cached value directly, skip DynamoDB entirely
awslocal dynamodb get-item --table-name UserProfiles --key '{"userId": {"S": "u-42"}}'
```

Why this matters: this is the exact pattern tested whenever a scenario describes "read-heavy
traffic overwhelming the database" — the cache absorbs repeated reads for the same key, and only
a cache miss ever reaches the database at all.

## Lab 5 — Capstone: ingestion-to-query pipeline matching the domain architecture (Task 3.5)

Goal: chain Kinesis ingestion through to a DynamoDB-backed "query layer," mirroring (at small
scale) the Kinesis → Glue → S3 → Athena pipeline from the domain README's architecture diagram.

```bash
# 1. Create the stream and a table to hold processed results
awslocal kinesis create-stream --stream-name sensor-readings --shard-count 1
awslocal dynamodb create-table --table-name ProcessedReadings \
  --attribute-definitions AttributeName=deviceId,AttributeType=S \
  --key-schema AttributeName=deviceId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# 2. Put several raw records into the stream
awslocal kinesis put-record --stream-name sensor-readings --partition-key device-7 \
  --data '{"deviceId": "device-7", "tempC": 24.1, "ts": "2026-01-01T00:00:00Z"}'
awslocal kinesis put-record --stream-name sensor-readings --partition-key device-7 \
  --data '{"deviceId": "device-7", "tempC": 24.6, "ts": "2026-01-01T00:01:00Z"}'

# 3. Read the records back (simulating a Lambda consumer reading from the stream) and write
#    the latest reading per device into the "query layer" table
awslocal kinesis get-shard-iterator --stream-name sensor-readings --shard-id shardId-000000000000 \
  --shard-iterator-type TRIM_HORIZON
awslocal kinesis get-records --shard-iterator <iterator-from-previous-step>
awslocal dynamodb put-item --table-name ProcessedReadings \
  --item '{"deviceId": {"S": "device-7"}, "latestTempC": {"N": "24.6"}, "ts": {"S": "2026-01-01T00:01:00Z"}}'

# 4. Query the processed table the way a dashboard would — fast, single-digit-millisecond
#    lookups instead of re-scanning raw stream data every time
awslocal dynamodb get-item --table-name ProcessedReadings --key '{"deviceId": {"S": "device-7"}}'
```

Why this matters: this capstone demonstrates the core performance lesson of Task 3.5 — raw
streamed/ingested data is rarely queried directly at scale; a processing step (here, a simple
Lambda-style consumer; in the real architecture, Glue transforming CSV to Parquet) produces a
query-optimized shape that a dashboard or API can read quickly and cheaply, which is the entire
reason the PixelForge Analytics case study in the domain README moves off scanning raw CSV
directly.

## Use Cases — Real Scenarios (these labs' skills applied for real)

- **IoT platform engineer sizing Kinesis shard count for a new product launch.** Lab 1's
  shard-iterator/get-records exercise builds the mental model needed to reason about why a
  consumer "falls behind" the producer when shard count is undersized for the actual write rate.
- **Startup choosing a DynamoDB billing mode for a brand-new, unproven feature.** Lab 2's
  on-demand-table exercise is literally the decision a team makes on day one of a new feature with
  no usage data yet — on-demand first, revisit provisioned once traffic is well understood.
- **DevOps engineer building the launch-template foundation for a future Auto Scaling group.**
  Lab 3's launch-template exercise is the exact artifact a real Auto Scaling group references when
  it scales out — understanding its structure is the prerequisite for tuning any scaling policy
  later.
- **Backend engineer implementing cache-aside for the first time.** Lab 4's manual "check cache,
  fall back to database, populate cache" walkthrough is the mental checklist every cache-aside
  implementation in a real codebase follows, regardless of language or framework.
- **Data engineer building their first ingestion-to-query pipeline end to end.** The capstone lab's
  stream-to-table flow is a miniature version of the exact Kinesis → Glue → S3 → Athena pipeline a
  real data engineering team stands up when a product manager asks for "a dashboard of what's
  happening right now."
- **SRE diagnosing why a Kinesis consumer is falling behind during a traffic spike.** Lab 1's
  shard-iterator exercise is the exact mental model used to confirm whether the fix is "add more
  shards" or "fix a slow consumer" — reading the shard iterator and get-records cadence manually
  once makes the automated CloudWatch alarm's meaning obvious afterward.
- **Growth team deciding whether a new feature's DynamoDB table should start on-demand.** Lab 2's
  provisioned-vs-on-demand comparison is run as a literal bake-off before a feature launch,
  with the team defaulting to on-demand for the first month and only moving to provisioned once
  real traffic data from that first month exists to size it against.
- **Platform engineer onboarding new hires to the cache-aside pattern.** Lab 4's manual "check
  cache, fall back to database, populate cache" walkthrough is used as a short onboarding exercise
  for every new backend hire, specifically because the pattern is simple to state but easy to
  implement with a subtle bug (e.g., forgetting the TTL) the first time.

## Honest limitation

Floci does not model real network latency, true multi-shard Kinesis throughput limits, or
ElastiCache/CloudFront edge behavior — these labs build CLI/API muscle memory for the services
involved, not a performance benchmark. Read `storage-performance-decision-framework.md`,
`compute-performance-decision-framework.md`, and `network-performance-architecture-patterns.md`
for the actual tested reasoning.
