# DVA-C03 — AWS Certified Developer – Associate

> **Exam transition:** DVA-C03 registration opened Oct 27, 2026. DVA-C02 retires Nov 30, 2026.
> DVA-C03 is live from **Dec 1, 2026**. This repo targets DVA-C03 since that's the version en
> will actually sit.

## Exam Overview

| | |
|---|---|
| Who it's for | Developers building, testing, deploying, and debugging AWS Cloud applications (incl. AI-assisted development tools) |
| Questions | 65 total (50 scored, 15 unscored) |
| Time | 130 minutes |
| Format | Multiple choice & multiple response |
| Passing score | 720 / 1000 |
| Cost | $150 USD |
| Official guide | https://docs.aws.amazon.com/pdfs/aws-certification/latest/developer-associate-03/developer-associate-03.pdf |

## What's new vs DVA-C02

- New **Task 2.3**: security risks of using/integrating AI services (access control for AI
  services, data privacy controls like VPC endpoints, keeping inputs/outputs out of model
  training, content filtering, prompt-injection protection, AI agent security, sensitive data
  in logs).
- **AI-assisted development** now assessed across all 4 domains: code generation/review
  (Domain 1), test generation/regression automation (Domain 3), CI/CD automation (Domain 3),
  error analysis/optimization recommendations (Domain 4).
- **Containers** now directly tested: ECR image build/tag/lifecycle, ECS/EKS/Fargate deployment.
- New in-scope services: **Amazon Bedrock, Bedrock AgentCore, Amazon Q, Kiro, Data Firehose,
  AWS PrivateLink**. SageMaker AI and Strands Agents are explicitly **out of scope** (that's
  MLA-C02 territory).

## Domains & Weights

| # | Domain | Weight | Folder |
|---|---|---|---|
| 1 | Development with AWS Services | **30%** | [`domain-1-development/`](domain-1-development) |
| 2 | Security | **26%** | [`domain-2-security/`](domain-2-security) |
| 3 | Testing and Deployment | **22%** | [`domain-3-testing-deployment/`](domain-3-testing-deployment) |
| 4 | Troubleshooting and Optimization | **22%** | [`domain-4-troubleshooting-optimization/`](domain-4-troubleshooting-optimization) |

## Domain 1: Development with AWS Services (30%)

- **Task 1.1** — Develop code for applications hosted on AWS (AWS SDKs/APIs, streaming data,
  serialize/deserialize, event-driven patterns with EventBridge/S3 events, API Gateway stages)
- **Task 1.2** — Develop code for AWS Lambda (VPC access to private resources, layers, concurrency, triggers)
- **Task 1.3** — Use data stores in application development (DynamoDB, S3, RDS/Aurora — access patterns, consistency models, SDK integration)

## Domain 2: Security (26%)

- **Task 2.1** — Implement authentication/authorization for apps and AWS services (IAM, Cognito, STS)
- **Task 2.2** — Implement encryption and manage sensitive data (at-rest/in-transit encryption, ACM/Private CA, KMS, PII masking)
- **Task 2.3** *(new)* — Identify and mitigate security risks of using/integrating AI services (access control, data privacy via VPC endpoints, content filtering, agent security, log hygiene)

## Domain 3: Testing and Deployment (22%)

- **Task 3.1** — Prepare application artifacts for deployment (dependency management, ECR container images, Dockerfiles, config via AppConfig/Parameter Store/Secrets Manager, API Gateway stages)
- **Task 3.2** — Implement and automate application testing (SAM/CDK/CloudFormation test validation, mock APIs, test events, AI-assisted test generation/regression automation)
- **Task 3.3** — Deploy code via CI/CD (Lambda packaging, ECS/EKS/Fargate deployment, IaC templates, CodeDeploy, CodePipeline, blue/green/canary/rolling strategies, rollback, AI-assisted deployment approvals)

## Domain 4: Troubleshooting and Optimization (22%)

- **Task 4.1** — Assist in root cause analysis (CloudWatch Logs/Metrics, X-Ray tracing, CloudTrail, AI-assisted error analysis)
- **Task 4.2** — Instrument code for observability
- **Task 4.3** — Optimize applications on AWS (Lambda performance tuning, cost/performance tradeoffs, AI-assisted optimization recommendations)

## Study order

1. [`00-fundamentals/`](../../00-fundamentals) and ideally SAA-C03 Domain 1 first (shared IAM/VPC/security vocabulary)
2. Domain 1 (core development patterns)
3. Domain 2 (security — builds directly on Domain 1's data stores and APIs)
4. Domain 3 (testing/deployment — assumes you can already write the code from Domains 1-2)
5. Domain 4 (troubleshooting — the "something's wrong with what I built in 1-3" layer)

## Status

🚧 Scaffolded — domain folders contain topic checklists; full topic docs being filled in.
