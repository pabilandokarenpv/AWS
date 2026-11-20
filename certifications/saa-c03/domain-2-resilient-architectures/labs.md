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

## Honest limitation

Floci does not simulate true cross-AZ network failure, Route 53 health-check-driven failover, or
Multi-AZ's actual synchronous-replication failover event — those are described conceptually in
`route53.md`, `rds.md`, and `disaster-recovery-strategies.md`. Use these labs for the API/workflow
muscle memory; read the docs for the resiliency behavior itself.
