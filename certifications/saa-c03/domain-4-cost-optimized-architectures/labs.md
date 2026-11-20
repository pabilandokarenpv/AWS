# Domain 4 Labs — Design Cost-Optimized Architectures (Floci)

Setup once: see [`labs-floci/README.md`](../../../labs-floci/README.md). These labs use S3 and
DynamoDB — genuinely emulated by Floci. Floci does not simulate actual AWS billing, so these labs
practice the **API calls and configuration** behind each cost lever; the dollar savings
themselves are conceptual (see the linked decision-framework docs for the real numbers).

## Lab 1 — S3 lifecycle policy: Standard → IA → Glacier (Task 4.1)

Goal: configure the exact automation that moves aging data into progressively cheaper storage
tiers with zero application changes.

```bash
# 1. Create a bucket and put a test object in it
awslocal s3 mb s3://cost-optimized-archive
awslocal s3 cp README.md s3://cost-optimized-archive/logs/sample-log.txt

# 2. Define a lifecycle configuration: IA after 30 days, Glacier after 90, Deep Archive after 180
cat > lifecycle.json << 'EOF'
{
  "Rules": [
    {
      "ID": "tiered-archive",
      "Status": "Enabled",
      "Filter": { "Prefix": "logs/" },
      "Transitions": [
        { "Days": 30, "StorageClass": "STANDARD_IA" },
        { "Days": 90, "StorageClass": "GLACIER" },
        { "Days": 180, "StorageClass": "DEEP_ARCHIVE" }
      ]
    }
  ]
}
EOF
awslocal s3api put-bucket-lifecycle-configuration --bucket cost-optimized-archive \
  --lifecycle-configuration file://lifecycle.json

# 3. Confirm the rule is attached
awslocal s3api get-bucket-lifecycle-configuration --bucket cost-optimized-archive
```

Why this matters: this is literally the mechanism tested in Task 4.1 — one JSON config
replaces a manual (or custom-scripted) process of moving old data to cheaper storage.

## Lab 2 — DynamoDB on-demand vs. provisioned billing mode (Task 4.3)

Goal: practice switching a table's billing mode — the real-world action behind "this table's
traffic became predictable, switch it to save money" or vice versa.

```bash
# 1. Create a table starting in provisioned mode
awslocal dynamodb create-table --table-name UserProfiles \
  --attribute-definitions AttributeName=userId,AttributeType=S \
  --key-schema AttributeName=userId,KeyType=HASH \
  --billing-mode PROVISIONED --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

# 2. Switch it to on-demand (simulating "traffic became unpredictable, stop guessing capacity")
awslocal dynamodb update-table --table-name UserProfiles --billing-mode PAY_PER_REQUEST

# 3. Confirm the change
awslocal dynamodb describe-table --table-name UserProfiles --query 'Table.BillingModeSummary'
```

Why this matters: this two-way switch is exactly the lever described in
`database-cost-optimization-decision-framework.md` — on-demand for unpredictable/new traffic,
provisioned (ideally with Auto Scaling) once the pattern is well understood and stable.

## Lab 3 — VPC endpoint configuration to bypass NAT Gateway cost (Task 4.4)

Goal: practice creating the control-plane object behind the single most commonly tested network
cost optimization — routing S3 traffic off the NAT Gateway path entirely.

```bash
# 1. Create a VPC and subnet to attach the endpoint to
awslocal ec2 create-vpc --cidr-block 10.0.0.0/16
awslocal ec2 create-subnet --vpc-id <vpc-id> --cidr-block 10.0.1.0/24

# 2. Create an S3 Gateway endpoint (free — no hourly or per-GB charge) attached to the VPC's
#    route table, so traffic to S3 never needs to leave through a NAT Gateway
awslocal ec2 create-vpc-endpoint --vpc-id <vpc-id> --service-name com.amazonaws.us-east-1.s3 \
  --route-table-ids <route-table-id> --vpc-endpoint-type Gateway

# 3. Confirm it's attached
awslocal ec2 describe-vpc-endpoints --filters Name=vpc-id,Values=<vpc-id>
```

Why this matters: this is the concrete fix for the "NAT Gateway data processing charges are the
largest line item, mostly traffic to S3" exam scenario — a Gateway endpoint for S3/DynamoDB costs
nothing and keeps that traffic off the metered NAT path entirely.

## Honest limitation

Floci does not model actual AWS billing, Spot interruption behavior, or Reserved
Instance/Savings Plan discount math — these labs build the configuration muscle memory; read
the four decision-framework docs in this folder for the real cost reasoning and numbers.
