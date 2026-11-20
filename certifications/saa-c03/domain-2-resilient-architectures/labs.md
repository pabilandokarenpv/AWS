# Domain 2 Labs — Design Resilient Architectures (Floci)

Setup once: see [`labs-floci/README.md`](../../../labs-floci/README.md). These labs use SQS,
Lambda, API Gateway, Step Functions, and RDS — all genuinely emulated by Floci. (Route 53
failover routing, true Multi-AZ failover physics, and CloudFront are control-plane/global
features Floci does not simulate end-to-end; this file notes where that applies.)

## Lab 1 — Decouple a producer and consumer with SQS (Task 2.1)

Goal: feel the difference between a direct synchronous call and a decoupled, queue-based one —
the core "loosely coupled" pattern.

```bash
# 1. Create the queue
awslocal sqs create-queue --queue-name order-events-queue

# 2. "Producer" sends a message — it does not wait for anyone to process it
awslocal sqs send-message --queue-url http://localhost:4566/000000000000/order-events-queue \
  --message-body '{"orderId": "A-1001", "status": "placed"}'

# 3. "Consumer" polls for work whenever it's ready — completely independent of the producer
awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/order-events-queue \
  --max-number-of-messages 1

# 4. After successfully processing, the consumer deletes the message (capture ReceiptHandle
#    from step 3's output)
awslocal sqs delete-message --queue-url http://localhost:4566/000000000000/order-events-queue \
  --receipt-handle <receipt-handle>

# 5. Check queue depth — this is the metric Auto Scaling would react to in real AWS
awslocal sqs get-queue-attributes --queue-url http://localhost:4566/000000000000/order-events-queue \
  --attribute-names ApproximateNumberOfMessages
```

Why this matters: `ApproximateNumberOfMessages` is exactly the CloudWatch metric a real Auto
Scaling target-tracking policy scales a worker fleet on — queue depth up, add workers; queue
depth down, remove them.

## Lab 2 — Event-driven workflow with API Gateway + Step Functions + Lambda (Task 2.1)

Goal: build the synchronous-entry/asynchronous-orchestration pattern from
`event-driven-microservice-architecture-patterns.md` end to end.

```bash
# 1. Create a simple Lambda function (zip a one-line handler first, e.g. index.py with a
#    lambda_handler returning a fixed response)
awslocal lambda create-function --function-name ProcessOrderStep \
  --runtime python3.12 --handler index.lambda_handler --role arn:aws:iam::000000000000:role/lambda-role \
  --zip-file fileb://function.zip

# 2. Define a Step Functions state machine that calls it
cat > statemachine.json << 'EOF'
{
  "Comment": "Order processing workflow",
  "StartAt": "ProcessOrder",
  "States": {
    "ProcessOrder": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:000000000000:function:ProcessOrderStep",
      "End": true
    }
  }
}
EOF
awslocal stepfunctions create-state-machine --name OrderWorkflow \
  --definition file://statemachine.json --role-arn arn:aws:iam::000000000000:role/sfn-role

# 3. Trigger it the way API Gateway would (via a start-execution call)
awslocal stepfunctions start-execution --state-machine-arn <state-machine-arn> \
  --input '{"orderId": "A-1002"}'

# 4. Check the execution result
awslocal stepfunctions describe-execution --execution-arn <execution-arn>
```

Why this matters: API Gateway's job is just the synchronous front door; the actual multi-step
business logic (with retries/branching) belongs in Step Functions, not stuffed into one giant
Lambda — this is the "why Step Functions exists" lesson the exam tests.

## Lab 3 — RDS primary + read replica (Task 2.1 / 2.2)

Goal: distinguish a read replica (serves live read traffic) from Multi-AZ (pure failover
standby, not readable) — a very commonly confused exam pair.

```bash
# 1. Create a primary RDS instance (Floci backs this with real Docker Postgres)
awslocal rds create-db-instance --db-instance-identifier orders-primary \
  --db-instance-class db.t3.micro --engine postgres --master-username admin \
  --master-user-password StudyPass123! --allocated-storage 20

# 2. Create a read replica pointing at it
awslocal rds create-db-instance-read-replica --db-instance-identifier orders-read-replica \
  --source-db-instance-identifier orders-primary

# 3. Confirm both instances exist and inspect their roles
awslocal rds describe-db-instances --query 'DBInstances[].{Id:DBInstanceIdentifier,Role:ReadReplicaDBInstanceIdentifiers}'
```

Why this matters: in real AWS, point reporting/analytics queries at the read replica's own
endpoint, never the primary's — this offloads read traffic exactly as Task 2.1 expects. Multi-AZ
(a separate RDS setting, not a separate instance you connect to) is the distinct high-availability
failover mechanism covered conceptually in `disaster-recovery-strategies.md`.

## Lab 4 — SNS fan-out to multiple SQS queues (Task 2.1)

Goal: build the "one event, many independent subscribers, each durably buffered" pattern from
`event-driven-microservice-architecture-patterns.md` — the combined SNS+SQS pattern that shows up
constantly in real decoupled systems.

```bash
# 1. Create an SNS topic representing "OrderPlaced" events
awslocal sns create-topic --name order-placed-topic

# 2. Create two separate SQS queues representing two independent subscriber services
awslocal sqs create-queue --queue-name inventory-service-queue
awslocal sqs create-queue --queue-name notification-service-queue

# 3. Subscribe both queues to the topic (each gets its own durable copy of every message)
awslocal sns subscribe --topic-arn arn:aws:sns:us-east-1:000000000000:order-placed-topic \
  --protocol sqs --notification-endpoint arn:aws:sqs:us-east-1:000000000000:inventory-service-queue
awslocal sns subscribe --topic-arn arn:aws:sns:us-east-1:000000000000:order-placed-topic \
  --protocol sqs --notification-endpoint arn:aws:sqs:us-east-1:000000000000:notification-service-queue

# 4. Publish one message to the topic
awslocal sns publish --topic-arn arn:aws:sns:us-east-1:000000000000:order-placed-topic \
  --message '{"orderId": "A-1003", "status": "placed"}'

# 5. Confirm BOTH queues received their own independent copy of the message
awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/inventory-service-queue
awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/notification-service-queue
```

Why this matters: this is the exact mechanism behind "many independent teams' services all react
to the same event" — a new third subscriber can be added later by subscribing one more queue to
the topic, with zero change to the publisher or the existing subscribers.

## Lab 5 — Capstone: decouple, auto-scale, and add a dead-letter queue (Task 2.1 + 2.2)

Goal: combine queue-based decoupling, scale-on-depth reasoning, and failure handling into one
mini-architecture resembling the domain README's StreamVista case study.

```bash
# 1. Create a dead-letter queue first
awslocal sqs create-queue --queue-name order-processing-dlq

# 2. Create the main queue with a redrive policy pointing failed messages at the DLQ after
#    3 failed receive attempts
DLQ_ARN=$(awslocal sqs get-queue-attributes \
  --queue-url http://localhost:4566/000000000000/order-processing-dlq \
  --attribute-names QueueArn --query Attributes.QueueArn --output text)
awslocal sqs create-queue --queue-name order-processing-queue \
  --attributes "RedrivePolicy={\"deadLetterTargetArn\":\"$DLQ_ARN\",\"maxReceiveCount\":\"3\"}"

# 3. Send a normal message and a deliberately "poison" message (e.g., malformed JSON an
#    application would reject every time)
awslocal sqs send-message --queue-url http://localhost:4566/000000000000/order-processing-queue \
  --message-body '{"orderId": "A-2001", "status": "placed"}'
awslocal sqs send-message --queue-url http://localhost:4566/000000000000/order-processing-queue \
  --message-body 'not-valid-json{{{'

# 4. Simulate a worker repeatedly failing to process the poison message by receiving it without
#    deleting it 3 times in a row (each receive increments its receive count)
for i in 1 2 3; do
  awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/order-processing-queue \
    --attribute-names ApproximateReceiveCount
done

# 5. Confirm the poison message has moved to the DLQ instead of looping forever
awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/order-processing-dlq
```

Why this matters: this is the production-grade pattern this domain's README calls out as missing
from a naive queue setup — without a DLQ, one malformed message can consume worker capacity
indefinitely (constantly retried, never succeeding, never cleared), silently degrading the whole
pipeline's throughput exactly like the tight-coupling failures this domain is built to prevent.

## Honest limitation

Floci does not simulate true cross-AZ network failure, Route 53 health-check-driven failover, or
Multi-AZ's actual synchronous-replication failover event — those are described conceptually in
`route53.md`, `rds.md`, and `disaster-recovery-strategies.md`. Use these labs for the API/workflow
muscle memory; read the docs for the resiliency behavior itself.
