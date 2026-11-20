# SAA-C03 — AWS Certified Solutions Architect – Associate

## Exam Overview

| | |
|---|---|
| Who it's for | Anyone who designs AWS architectures — validates ability to design solutions aligned with the AWS Well-Architected Framework |
| Questions | 65 total (50 scored, 15 unscored — you can't tell which is which) |
| Time | 130 minutes |
| Format | Multiple choice & multiple response |
| Passing score | 720 / 1000 (scaled score) |
| Cost | $150 USD |
| Delivery | Pearson VUE test center or online proctored |
| Valid for | 3 years |
| Official guide | https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Exam-Guide.pdf |

## Domains & Weights

| # | Domain | Weight | Folder |
|---|---|---|---|
| 1 | Design Secure Architectures | **30%** | [`domain-1-secure-architectures/`](domain-1-secure-architectures) |
| 2 | Design Resilient Architectures | **26%** | [`domain-2-resilient-architectures/`](domain-2-resilient-architectures) |
| 3 | Design High-Performing Architectures | **24%** | [`domain-3-high-performing-architectures/`](domain-3-high-performing-architectures) |
| 4 | Design Cost-Optimized Architectures | **20%** | [`domain-4-cost-optimized-architectures/`](domain-4-cost-optimized-architectures) |

## Domain 1: Design Secure Architectures (30%)

- **Task 1.1** — Design secure access to AWS resources (IAM, IAM Identity Center/SSO, federated access, multi-account strategy, least privilege, MFA, STS/role switching, SCPs, Control Tower)
- **Task 1.2** — Design secure workloads and applications (VPC security — security groups, NACLs, route tables, NAT gateways, public/private subnet segmentation, Shield, WAF, Secrets Manager, Cognito, GuardDuty, Macie, VPN, Direct Connect)
- **Task 1.3** — Determine appropriate data security controls (KMS encryption at rest, ACM/TLS encryption in transit, key rotation, certificate renewal, backup/replication, data lifecycle policies)

## Domain 2: Design Resilient Architectures (26%)

- **Task 2.1** — Design scalable and loosely coupled architectures (API Gateway, SQS, microservices, event-driven patterns, horizontal/vertical scaling, CDN, containers, ECS/EKS, load balancing, multi-tier architecture, Step Functions, read replicas)
- **Task 2.2** — Design highly available and/or fault-tolerant architectures (Multi-AZ, Auto Scaling, Route 53 routing/failover, backup/DR strategies)

## Domain 3: Design High-Performing Architectures (24%)

- **Task 3.1** — Determine high-performing and/or scalable storage solutions (S3, EFS, EBS — object/file/block tradeoffs)
- **Task 3.2** — Design high-performing and elastic compute solutions
- **Task 3.3** — Determine high-performing database solutions
- **Task 3.4** — Determine high-performing and/or scalable network architectures
- **Task 3.5** — Determine high-performing data ingestion and transformation solutions (Kinesis, Glue, EMR, data lakes, CSV→Parquet)

## Domain 4: Design Cost-Optimized Architectures (20%)

- **Task 4.1** — Design cost-optimized storage solutions (lifecycle policies, storage classes, backup strategy)
- **Task 4.2** — Design cost-optimized compute solutions (Spot/Reserved/Savings Plans, auto scaling, serverless, containers)
- **Task 4.3** — Design cost-optimized database solutions (engine choice, DynamoDB vs RDS, serverless options)
- **Task 4.4** — Design cost-optimized network architectures (NAT gateway cost, Direct Connect vs VPN vs internet, VPC endpoints, Transit Gateway, data transfer cost minimization)

## Study order

1. [`00-fundamentals/`](../../00-fundamentals) if you haven't already
2. Domain 1 (biggest weight, and security concepts recur in every other domain)
3. Domain 2 (resiliency patterns build directly on Domain 1's networking)
4. Domain 3 (performance — assumes you already know the services from 1 & 2)
5. Domain 4 (cost — the "which service is cheaper for this case" layer on top of everything else)

## Status

🚧 Scaffolded — domain folders contain topic checklists; full topic docs being filled in.
See each `domain-*/README.md` for what's covered and what's pending.
