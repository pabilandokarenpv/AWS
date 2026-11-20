# Glossary

An A–Z index of every term used across this repo. Each entry is one line (plain definition) +
a link to the full doc where it's explained in depth. This file is the fast lookup; the linked
doc is the deep dive.

> This glossary grows as domains are written. Alphabetical, service-and-concept terms mixed.

## A
- **Availability Zone (AZ)** — one or more physically separate data centers within an AWS Region, each with independent power/cooling/networking. → [`00-fundamentals/aws-global-infrastructure.md`](../00-fundamentals/aws-global-infrastructure.md)
- **AMI (Amazon Machine Image)** — a template (OS + software config) used to launch an EC2 instance. → `services/compute/ec2.md`
- **ARN (Amazon Resource Name)** — the globally unique identifier format for every AWS resource. → `services/security-identity-compliance/iam.md`
- **Auto Scaling Group (ASG)** — a group of EC2 instances that automatically grows/shrinks based on demand or schedule. → `services/compute/ec2-auto-scaling.md`

## B
- **Bedrock** — AWS's managed service for accessing and customizing foundation models (GenAI). → `services/machine-learning-ai/bedrock.md`

## C
- **CloudFormation** — AWS's native Infrastructure-as-Code service; define infrastructure in JSON/YAML templates. → `services/management-governance/cloudformation.md`
- **CloudFront** — AWS's global CDN (content delivery network). → `services/networking-content-delivery/cloudfront.md`
- **CloudTrail** — logs every API call made in your AWS account, for audit/compliance. → `services/management-governance/cloudtrail.md`
- **CloudWatch** — AWS's monitoring/observability service (metrics, logs, alarms, dashboards). → `services/management-governance/cloudwatch.md`

## D
- **DynamoDB** — AWS's fully managed, serverless NoSQL key-value/document database. → `services/database/dynamodb.md`

## E
- **EC2 (Elastic Compute Cloud)** — AWS's virtual server (compute instance) service. → `services/compute/ec2.md`
- **ECS / EKS** — AWS's container orchestration services (ECS = AWS-native, EKS = managed Kubernetes). → `services/containers/`

## I
- **IAM (Identity and Access Management)** — controls who can do what to which AWS resource. → `services/security-identity-compliance/iam.md`

## K
- **KMS (Key Management Service)** — managed service for creating/controlling encryption keys. → `services/security-identity-compliance/kms.md`

## L
- **Lambda** — AWS's serverless compute service; runs code in response to events, no server management. → `services/compute/lambda.md`

## R
- **Region** — a physical geographic location containing multiple Availability Zones. → `00-fundamentals/aws-global-infrastructure.md`
- **RDS (Relational Database Service)** — AWS's managed relational database service (Postgres, MySQL, etc.). → `services/database/rds.md`

## S
- **S3 (Simple Storage Service)** — AWS's object storage service. → `services/storage/s3.md`
- **SageMaker** — AWS's fully managed machine learning platform (build, train, deploy models). → `services/machine-learning-ai/sagemaker.md`
- **Shared Responsibility Model** — the split between what AWS secures ("of the cloud") and what you secure ("in the cloud"). → `00-fundamentals/shared-responsibility-model.md`

## V
- **VPC (Virtual Private Cloud)** — your own logically isolated network within AWS. → `services/networking-content-delivery/vpc.md`

## W
- **Well-Architected Framework** — AWS's 6-pillar framework for evaluating architecture quality (Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability). → `00-fundamentals/well-architected-framework.md`
