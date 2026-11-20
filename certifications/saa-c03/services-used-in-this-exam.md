# Services Used in SAA-C03

A fast-reference index of every AWS service this repo documents that actually shows up in **SAA-C03**, grouped by the domain that tests it. This is derived directly from the cross-links in this cert's own domain docs — if a service is listed here, a task statement in this exam covers it. Official source of truth: [SAA-C03 Exam Guide](https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Exam-Guide.pdf).

> Use this page as your checklist: before exam day, you should be able to open every linked doc from memory and explain what it does, when to use it, and how it shows up in a scenario question.

**Total services/topics mapped to this cert: 94** (a service can appear in more than one domain if it's tested from multiple angles).

## Domain 1: Design Secure Architectures (30%)

[Full domain guide →](../../certifications/saa-c03/domain-1-secure-architectures/README.md)

| Service / Topic | Doc |
|---|---|
| AWS Backup | [aws-backup.md](../../services/storage/aws-backup.md) |
| AWS Certificate Manager (ACM) & Private CA | [acm-and-private-ca.md](../../services/security-identity-compliance/acm-and-private-ca.md) |
| AWS Direct Connect | [direct-connect.md](../../services/networking-content-delivery/direct-connect.md) |
| AWS IAM Identity Center (SSO) | [iam-identity-center-sso.md](../../services/security-identity-compliance/iam-identity-center-sso.md) |
| AWS Identity and Access Management (IAM) | [iam.md](../../services/security-identity-compliance/iam.md) |
| AWS Key Management Service (KMS) | [kms.md](../../services/security-identity-compliance/kms.md) |
| AWS Organizations & Service Control Policies (SCPs) | [organizations-and-scps.md](../../services/security-identity-compliance/organizations-and-scps.md) |
| AWS STS & Role Switching (AssumeRole) | [sts-and-role-switching.md](../../services/security-identity-compliance/sts-and-role-switching.md) |
| AWS Secrets Manager vs. Systems Manager Parameter Store | [secrets-manager-vs-parameter-store.md](../../services/security-identity-compliance/secrets-manager-vs-parameter-store.md) |
| AWS Security Hub & Amazon Inspector | [security-hub-and-inspector.md](../../services/security-identity-compliance/security-hub-and-inspector.md) |
| AWS Shield (Standard & Advanced) | [shield.md](../../services/security-identity-compliance/shield.md) |
| AWS Site-to-Site VPN & Client VPN | [vpn.md](../../services/networking-content-delivery/vpn.md) |
| AWS Systems Manager | [systems-manager.md](../../services/management-governance/systems-manager.md) |
| AWS WAF (Web Application Firewall) | [waf.md](../../services/security-identity-compliance/waf.md) |
| Amazon Cognito | [cognito.md](../../services/security-identity-compliance/cognito.md) |
| Amazon GuardDuty | [guardduty.md](../../services/security-identity-compliance/guardduty.md) |
| Amazon Macie | [macie.md](../../services/security-identity-compliance/macie.md) |
| Amazon S3 (Simple Storage Service) | [s3.md](../../services/storage/s3.md) |
| Amazon VPC (Virtual Private Cloud) | [vpc.md](../../services/networking-content-delivery/vpc.md) |
| S3 Storage Classes | [s3-storage-classes.md](../../services/storage/s3-storage-classes.md) |
| Security Groups vs. Network ACLs (NACLs) | [security-groups-vs-nacls.md](../../services/networking-content-delivery/security-groups-vs-nacls.md) |
| Subnets, Route Tables, Internet Gateway & NAT Gateway | [subnets-route-tables-igw-natgw.md](../../services/networking-content-delivery/subnets-route-tables-igw-natgw.md) |
| VPC Endpoints & AWS PrivateLink | [vpc-endpoints-privatelink.md](../../services/networking-content-delivery/vpc-endpoints-privatelink.md) |

## Domain 2: Design Resilient Architectures (26%)

[Full domain guide →](../../certifications/saa-c03/domain-2-resilient-architectures/README.md)

| Service / Topic | Doc |
|---|---|
| AWS Backup | [aws-backup.md](../../services/storage/aws-backup.md) |
| AWS Fargate | [fargate.md](../../services/containers/fargate.md) |
| AWS Step Functions | [step-functions.md](../../services/application-integration/step-functions.md) |
| Amazon API Gateway | [api-gateway.md](../../services/networking-content-delivery/api-gateway.md) |
| Amazon Aurora | [aurora.md](../../services/database/aurora.md) |
| Amazon CloudFront | [cloudfront.md](../../services/networking-content-delivery/cloudfront.md) |
| Amazon EC2 Auto Scaling | [ec2-auto-scaling.md](../../services/compute/ec2-auto-scaling.md) |
| Amazon Elastic Container Service (ECS) | [ecs.md](../../services/containers/ecs.md) |
| Amazon Elastic Kubernetes Service (EKS) | [eks.md](../../services/containers/eks.md) |
| Amazon EventBridge | [eventbridge.md](../../services/application-integration/eventbridge.md) |
| Amazon RDS (Relational Database Service) | [rds.md](../../services/database/rds.md) |
| Amazon Route 53 | [route53.md](../../services/networking-content-delivery/route53.md) |
| Amazon SNS (Simple Notification Service) | [sns.md](../../services/application-integration/sns.md) |
| Amazon SQS (Simple Queue Service) | [sqs.md](../../services/application-integration/sqs.md) |
| Containers vs. VMs vs. Serverless — A Conceptual Comparison | [containers-vs-vms-vs-serverless.md](../../services/containers/containers-vs-vms-vs-serverless.md) |
| Elastic Load Balancing (ALB / NLB / GWLB / CLB) | [elastic-load-balancing.md](../../services/networking-content-delivery/elastic-load-balancing.md) |
| Messaging Patterns Overview — SQS, SNS, EventBridge & Step Functions Together | [messaging-patterns-overview.md](../../services/application-integration/messaging-patterns-overview.md) |

## Domain 3: Design High-Performing Architectures (24%)

[Full domain guide →](../../certifications/saa-c03/domain-3-high-performing-architectures/README.md)

| Service / Topic | Doc |
|---|---|
| AWS Batch | [aws-batch.md](../../services/compute/aws-batch.md) |
| AWS Direct Connect | [direct-connect.md](../../services/networking-content-delivery/direct-connect.md) |
| AWS Fargate | [fargate.md](../../services/compute/fargate.md) |
| AWS Global Accelerator | [global-accelerator.md](../../services/networking-content-delivery/global-accelerator.md) |
| AWS Glue (Glue ETL, Glue DataBrew, Glue Data Catalog) | [glue.md](../../services/analytics/glue.md) |
| AWS Lambda | [lambda.md](../../services/compute/lambda.md) |
| Amazon Athena | [athena.md](../../services/analytics/athena.md) |
| Amazon Aurora | [aurora.md](../../services/database/aurora.md) |
| Amazon CloudFront | [cloudfront.md](../../services/networking-content-delivery/cloudfront.md) |
| Amazon DocumentDB (with MongoDB compatibility) | [documentdb.md](../../services/database/documentdb.md) |
| Amazon DynamoDB | [dynamodb.md](../../services/database/dynamodb.md) |
| Amazon EBS (Elastic Block Store) | [ebs.md](../../services/storage/ebs.md) |
| Amazon EC2 (Elastic Compute Cloud) | [ec2.md](../../services/compute/ec2.md) |
| Amazon EC2 Auto Scaling | [ec2-auto-scaling.md](../../services/compute/ec2-auto-scaling.md) |
| Amazon EFS (Elastic File System) | [efs.md](../../services/storage/efs.md) |
| Amazon EMR (Elastic MapReduce) | [emr.md](../../services/analytics/emr.md) |
| Amazon ElastiCache | [elasticache.md](../../services/database/elasticache.md) |
| Amazon Elastic Container Service (ECS) | [ecs.md](../../services/containers/ecs.md) |
| Amazon Elastic Kubernetes Service (EKS) | [eks.md](../../services/containers/eks.md) |
| Amazon FSx | [fsx.md](../../services/storage/fsx.md) |
| Amazon Kinesis Family (Data Streams, Data Firehose, Data Analytics) | [kinesis-family.md](../../services/analytics/kinesis-family.md) |
| Amazon Neptune | [neptune.md](../../services/database/neptune.md) |
| Amazon RDS (Relational Database Service) | [rds.md](../../services/database/rds.md) |
| Amazon Redshift | [redshift.md](../../services/database/redshift.md) |
| Amazon S3 (Simple Storage Service) | [s3.md](../../services/storage/s3.md) |
| Amazon VPC (Virtual Private Cloud) | [vpc.md](../../services/networking-content-delivery/vpc.md) |
| Containers vs. VMs vs. Serverless — A Conceptual Comparison | [containers-vs-vms-vs-serverless.md](../../services/containers/containers-vs-vms-vs-serverless.md) |
| Data Lake Concepts (S3 as a Data Lake, Lake House Architecture) | [data-lake-concepts.md](../../services/analytics/data-lake-concepts.md) |
| Database Selection Guide — Choosing the Right AWS Database | [database-selection-guide.md](../../services/database/database-selection-guide.md) |
| Elastic Load Balancing (ALB / NLB / GWLB / CLB) | [elastic-load-balancing.md](../../services/networking-content-delivery/elastic-load-balancing.md) |
| S3 Storage Classes | [s3-storage-classes.md](../../services/storage/s3-storage-classes.md) |
| Transit Gateway & VPC Peering | [transit-gateway-and-peering.md](../../services/networking-content-delivery/transit-gateway-and-peering.md) |
| VPC Endpoints & AWS PrivateLink | [vpc-endpoints-privatelink.md](../../services/networking-content-delivery/vpc-endpoints-privatelink.md) |

## Domain 4: Design Cost-Optimized Architectures (20%)

[Full domain guide →](../../certifications/saa-c03/domain-4-cost-optimized-architectures/README.md)

| Service / Topic | Doc |
|---|---|
| AWS Backup | [aws-backup.md](../../services/storage/aws-backup.md) |
| AWS Cost Management Tools | [cost-management-tools.md](../../services/management-governance/cost-management-tools.md) |
| AWS Direct Connect | [direct-connect.md](../../services/networking-content-delivery/direct-connect.md) |
| AWS Fargate | [fargate.md](../../services/compute/fargate.md) |
| AWS Lambda | [lambda.md](../../services/compute/lambda.md) |
| AWS Site-to-Site VPN & Client VPN | [vpn.md](../../services/networking-content-delivery/vpn.md) |
| AWS Trusted Advisor | [trusted-advisor.md](../../services/management-governance/trusted-advisor.md) |
| Amazon Aurora | [aurora.md](../../services/database/aurora.md) |
| Amazon CloudFront | [cloudfront.md](../../services/networking-content-delivery/cloudfront.md) |
| Amazon DynamoDB | [dynamodb.md](../../services/database/dynamodb.md) |
| Amazon EBS (Elastic Block Store) | [ebs.md](../../services/storage/ebs.md) |
| Amazon EC2 (Elastic Compute Cloud) | [ec2.md](../../services/compute/ec2.md) |
| Amazon EC2 Auto Scaling | [ec2-auto-scaling.md](../../services/compute/ec2-auto-scaling.md) |
| Amazon RDS (Relational Database Service) | [rds.md](../../services/database/rds.md) |
| Amazon S3 Glacier | [s3-glacier.md](../../services/storage/s3-glacier.md) |
| Containers vs. VMs vs. Serverless — A Conceptual Comparison | [containers-vs-vms-vs-serverless.md](../../services/containers/containers-vs-vms-vs-serverless.md) |
| Data Transfer Pricing (Networking Cost Model) | [data-transfer-pricing.md](../../services/networking-content-delivery/data-transfer-pricing.md) |
| Database Selection Guide — Choosing the Right AWS Database | [database-selection-guide.md](../../services/database/database-selection-guide.md) |
| S3 Storage Classes | [s3-storage-classes.md](../../services/storage/s3-storage-classes.md) |
| Transit Gateway & VPC Peering | [transit-gateway-and-peering.md](../../services/networking-content-delivery/transit-gateway-and-peering.md) |
| VPC Endpoints & AWS PrivateLink | [vpc-endpoints-privatelink.md](../../services/networking-content-delivery/vpc-endpoints-privatelink.md) |

## How to use this page

1. Go domain by domain (they're ordered by weight — Domain with the highest % first).
2. For each service, read its full doc once, run its Floci lab, then come back here and check it off mentally.
3. Cross-reference against the [official SAA-C03 in-scope services list](https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Exam-Guide.pdf) periodically — AWS updates exam guides, and a service appearing in the official list but not yet linked here is a gap to flag.
4. This page only lists services this REPO has already cross-linked from SAA-C03's domain docs — it is not a substitute for the official exam guide's appendix, which is the final authority on what's in/out of scope.
