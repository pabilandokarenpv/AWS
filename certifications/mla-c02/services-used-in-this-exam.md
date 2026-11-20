# Services Used in MLA-C02

A fast-reference index of every AWS service this repo documents that actually shows up in **MLA-C02**, grouped by the domain that tests it. This is derived directly from the cross-links in this cert's own domain docs — if a service is listed here, a task statement in this exam covers it. Official source of truth: [MLA-C02 Exam Guide](https://docs.aws.amazon.com/pdfs/aws-certification/latest/machine-learning-engineer-associate-02/machine-learning-engineer-associate-02.pdf).

> Use this page as your checklist: before exam day, you should be able to open every linked doc from memory and explain what it does, when to use it, and how it shows up in a scenario question.

**Total services/topics mapped to this cert: 35** (a service can appear in more than one domain if it's tested from multiple angles).

## Domain 1: Data Preparation for ML and AI (28%)

[Full domain guide →](../../certifications/mla-c02/domain-1-data-preparation/README.md)

| Service / Topic | Doc |
|---|---|
| AWS Glue (Glue ETL, Glue DataBrew, Glue Data Catalog) | [glue.md](../../services/analytics/glue.md) |
| AWS Lake Formation | [lake-formation.md](../../services/analytics/lake-formation.md) |
| Amazon Athena | [athena.md](../../services/analytics/athena.md) |
| Amazon Bedrock | [bedrock.md](../../services/machine-learning-ai/bedrock.md) |
| Amazon Data Firehose | [data-firehose.md](../../services/analytics/data-firehose.md) |
| Amazon EMR (Elastic MapReduce) | [emr.md](../../services/analytics/emr.md) |
| Amazon Kinesis Family (Data Streams, Data Firehose, Data Analytics) | [kinesis-family.md](../../services/analytics/kinesis-family.md) |
| Amazon OpenSearch Service | [opensearch.md](../../services/analytics/opensearch.md) |
| Amazon SageMaker — Overview | [sagemaker-overview.md](../../services/machine-learning-ai/sagemaker-overview.md) |
| Data Lake Concepts (S3 as a Data Lake, Lake House Architecture) | [data-lake-concepts.md](../../services/analytics/data-lake-concepts.md) |
| SageMaker Data Wrangler & Feature Store | [sagemaker-data-wrangler-and-feature-store.md](../../services/machine-learning-ai/sagemaker-data-wrangler-and-feature-store.md) |

## Domain 2: ML Model and Foundation Model Development (24%)

[Full domain guide →](../../certifications/mla-c02/domain-2-model-development/README.md)

| Service / Topic | Doc |
|---|---|
| Amazon Bedrock | [bedrock.md](../../services/machine-learning-ai/bedrock.md) |
| Amazon SageMaker — Overview | [sagemaker-overview.md](../../services/machine-learning-ai/sagemaker-overview.md) |
| SageMaker JumpStart | [jumpstart.md](../../services/machine-learning-ai/jumpstart.md) |
| SageMaker Model Monitor & Model Registry | [sagemaker-model-monitor-and-registry.md](../../services/machine-learning-ai/sagemaker-model-monitor-and-registry.md) |
| SageMaker Training & Tuning | [sagemaker-training-and-tuning.md](../../services/machine-learning-ai/sagemaker-training-and-tuning.md) |

## Domain 3: Deployment and Orchestration of ML and AI Workflows (24%)

[Full domain guide →](../../certifications/mla-c02/domain-3-deployment-orchestration/README.md)

| Service / Topic | Doc |
|---|---|
| AWS CodePipeline | [codepipeline.md](../../services/developer-tools/codepipeline.md) |
| Amazon Bedrock | [bedrock.md](../../services/machine-learning-ai/bedrock.md) |
| Amazon Elastic Container Registry (ECR) | [ecr.md](../../services/containers/ecr.md) |
| Amazon Elastic Container Service (ECS) | [ecs.md](../../services/containers/ecs.md) |
| Amazon Elastic Kubernetes Service (EKS) | [eks.md](../../services/containers/eks.md) |
| Amazon MWAA (Managed Workflows for Apache Airflow) | [mwaa.md](../../services/application-integration/mwaa.md) |
| Amazon SageMaker — Overview | [sagemaker-overview.md](../../services/machine-learning-ai/sagemaker-overview.md) |
| SageMaker Deployment & Endpoints | [sagemaker-deployment-endpoints.md](../../services/machine-learning-ai/sagemaker-deployment-endpoints.md) |
| SageMaker Pipelines | [sagemaker-pipelines.md](../../services/machine-learning-ai/sagemaker-pipelines.md) |

## Domain 4: Operating, Monitoring, and Securing ML and AI Solutions (24%)

[Full domain guide →](../../certifications/mla-c02/domain-4-monitoring-security/README.md)

| Service / Topic | Doc |
|---|---|
| AWS Cost Management Tools | [cost-management-tools.md](../../services/management-governance/cost-management-tools.md) |
| AWS Identity and Access Management (IAM) | [iam.md](../../services/security-identity-compliance/iam.md) |
| AWS Key Management Service (KMS) | [kms.md](../../services/security-identity-compliance/kms.md) |
| AWS X-Ray | [x-ray.md](../../services/developer-tools/x-ray.md) |
| Additional AI/AI-Adjacent Services for MLA-C02 (Lex, CodeGuru, Comprehend Medical, DevOps Guru, HealthLake) | [additional-ai-services-mla.md](../../services/machine-learning-ai/additional-ai-services-mla.md) |
| Amazon Bedrock | [bedrock.md](../../services/machine-learning-ai/bedrock.md) |
| Amazon VPC (Virtual Private Cloud) | [vpc.md](../../services/networking-content-delivery/vpc.md) |
| SageMaker Deployment & Endpoints | [sagemaker-deployment-endpoints.md](../../services/machine-learning-ai/sagemaker-deployment-endpoints.md) |
| SageMaker Model Monitor & Model Registry | [sagemaker-model-monitor-and-registry.md](../../services/machine-learning-ai/sagemaker-model-monitor-and-registry.md) |
| SageMaker Training & Tuning | [sagemaker-training-and-tuning.md](../../services/machine-learning-ai/sagemaker-training-and-tuning.md) |

## How to use this page

1. Go domain by domain (they're ordered by weight — Domain with the highest % first).
2. For each service, read its full doc once, run its Floci lab, then come back here and check it off mentally.
3. Cross-reference against the [official MLA-C02 in-scope services list](https://docs.aws.amazon.com/pdfs/aws-certification/latest/machine-learning-engineer-associate-02/machine-learning-engineer-associate-02.pdf) periodically — AWS updates exam guides, and a service appearing in the official list but not yet linked here is a gap to flag.
4. This page only lists services this REPO has already cross-linked from MLA-C02's domain docs — it is not a substitute for the official exam guide's appendix, which is the final authority on what's in/out of scope.
