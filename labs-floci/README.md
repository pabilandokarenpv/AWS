# Hands-on Labs — Floci

Every domain in this repo pairs with runnable labs against **[Floci](https://github.com/floci-io/floci)**,
a free, open-source, MIT-licensed local AWS emulator. No AWS account, no credit card, no risk
of a surprise bill — same CLI/SDK calls you'd run against real AWS, pointed at `localhost:4566`.

## Setup (one-time)

```bash
# Requires Docker
docker run -d -p 4566:4566 --name floci floci/floci

# Point the AWS CLI at it (create a reusable profile)
aws configure set aws_access_key_id test --profile floci
aws configure set aws_secret_access_key test --profile floci
aws configure set region us-east-1 --profile floci

# Alias for convenience
alias awslocal='aws --endpoint-url=http://localhost:4566 --profile floci'
```

Verify it's up:

```bash
awslocal s3 ls
```

Web UI (service inspector): `http://localhost:4566/_floci/ui`

## What Floci supports (relevant to our 3 certs)

| Category | Services | Notes |
|---|---|---|
| Storage | S3 | Full object API |
| Database | DynamoDB, RDS | RDS backed by real Docker Postgres/MySQL |
| Compute | Lambda, EC2 | EC2 backed by real Docker |
| Containers | ECS, EKS | Real Docker-backed |
| Messaging | SQS, SNS | Full queue/topic semantics |
| API | API Gateway (REST + HTTP/v2) | |
| Auth | IAM, STS, Cognito | |
| Security | KMS | |
| Orchestration | Step Functions, CloudFormation | |
| Streaming | Kinesis, MSK | MSK backed by real Docker |
| ML (limited) | — | Floci emulates AWS's control-plane APIs; actual SageMaker training/inference is NOT emulated — ML labs in this repo use SageMaker Studio Lab (free tier) or local scikit-learn/PyTorch instead; see `certifications/mla-c02/` lab notes |

## Lab index (filled in as each domain is written)

| Domain | Cert | Lab file |
|---|---|---|
| Design Secure Architectures | SAA-C03 | `certifications/saa-c03/domain-1-secure-architectures/labs.md` |
| Design Resilient Architectures | SAA-C03 | `certifications/saa-c03/domain-2-resilient-architectures/labs.md` |
| Design High-Performing Architectures | SAA-C03 | `certifications/saa-c03/domain-3-high-performing-architectures/labs.md` |
| Design Cost-Optimized Architectures | SAA-C03 | `certifications/saa-c03/domain-4-cost-optimized-architectures/labs.md` |
| Development with AWS Services | DVA-C03 | `certifications/dva-c03/domain-1-development/labs.md` |
| Security | DVA-C03 | `certifications/dva-c03/domain-2-security/labs.md` |
| Testing and Deployment | DVA-C03 | `certifications/dva-c03/domain-3-testing-deployment/labs.md` |
| Troubleshooting and Optimization | DVA-C03 | `certifications/dva-c03/domain-4-troubleshooting-optimization/labs.md` |
| Data Preparation | MLA-C02 | `certifications/mla-c02/domain-1-data-preparation/labs.md` |
| Model Development | MLA-C02 | `certifications/mla-c02/domain-2-model-development/labs.md` |
| Deployment & Orchestration | MLA-C02 | `certifications/mla-c02/domain-3-deployment-orchestration/labs.md` |
| Monitoring & Security | MLA-C02 | `certifications/mla-c02/domain-4-monitoring-security/labs.md` |

## Honest limitation

Floci emulates AWS **APIs**, not AWS's actual managed-service internals (no real multi-AZ
failover physics, no real IAM policy evaluation edge cases, no real SageMaker training
infra). It's for learning the *shape* of the API/workflow and practicing CLI/SDK/IaC — not a
substitute for reading how the real service behaves, which is what the exam actually tests.
Use it to build muscle memory, not as your only source of truth.
