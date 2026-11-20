# MLA-C02 — AWS Certified Machine Learning Engineer – Associate

> **Exam transition:** MLA-C01 retired (English) Sept 28, 2026. **MLA-C02** entered beta
> Sept 29, 2026 and goes **GA Jan 14, 2027** — adding generative AI (Bedrock, RAG, fine-tuning
> foundation models, agents, AI cost monitoring) throughout all 4 domains. This repo targets
> MLA-C02. Where the official C02 guide isn't fully public yet, content is based on the
> confirmed C01→C02 domain mapping plus publicly announced additions; flagged inline where still
> provisional.

## Exam Overview

| | |
|---|---|
| Who it's for | ML engineers who build, operationalize, deploy, and maintain ML/AI solutions and pipelines on AWS |
| Question types | Multiple choice & multiple response **only** (C01 also had ordering/matching/case studies — C02 simplified to MC/MR) |
| Passing score | 720 / 1000 (AWS standard scale) |
| Cost | $150 USD (standard AWS associate pricing) |
| Official guide (C01, superseded) | https://d1.awsstatic.com/training-and-certification/docs-machine-learning-engineer-associate/AWS-Certified-Machine-Learning-Engineer-Associate_Exam-Guide.pdf |

## What's new vs MLA-C01

| Domain | C01 | C02 |
|---|---|---|
| 1 | Data Preparation for ML (28%) | Data Preparation for ML **and AI** (28%) — adds embeddings, RAG data prep |
| 2 | ML Model Development (26%) | ML Model **and Foundation Model** Development (24%) — adds FM selection, fine-tuning |
| 3 | Deployment and Orchestration of ML Workflows (22%) | Deployment and Orchestration of ML **and AI** Workflows (24%) — adds Knowledge Bases, agents |
| 4 | ML Solution Monitoring, Maintenance, and Security (24%) | **Operating**, Monitoring and Securing ML and AI Solutions (24%) — adds Guardrails, GenAI cost monitoring |

## Domains & Weights (C02)

| # | Domain | Weight | Folder |
|---|---|---|---|
| 1 | Data Preparation for ML and AI | **28%** | [`domain-1-data-preparation/`](domain-1-data-preparation) |
| 2 | ML Model and Foundation Model Development | **24%** | [`domain-2-model-development/`](domain-2-model-development) |
| 3 | Deployment and Orchestration of ML and AI Workflows | **24%** | [`domain-3-deployment-orchestration/`](domain-3-deployment-orchestration) |
| 4 | Operating, Monitoring, and Securing ML and AI Solutions | **24%** | [`domain-4-monitoring-security/`](domain-4-monitoring-security) |

## Domain 1: Data Preparation for ML and AI (28%)

Ingest and store data (S3, EFS, FSx, Kinesis streaming) → transform (Glue, Glue DataBrew, EMR
Spark, SageMaker Data Wrangler) → feature engineering (SageMaker Feature Store) → data quality,
bias detection, class imbalance handling (splitting, shuffling, augmentation) → embeddings and
RAG data preparation (new for GenAI workflows).

## Domain 2: ML Model and Foundation Model Development (24%)

Select algorithm/approach (SageMaker built-in algorithms, script mode w/ TensorFlow/PyTorch, vs.
selecting/fine-tuning a foundation model via Bedrock/SageMaker JumpStart) → train and tune
(epochs, batch size, early stopping, distributed training, hyperparameter tuning — random
search/Bayesian) → evaluate (metrics selection, bias detection, overfitting diagnosis) → manage
model versions (SageMaker Model Registry).

## Domain 3: Deployment and Orchestration of ML and AI Workflows (24%)

Choose deployment infra (real-time / serverless / asynchronous / batch transform endpoints,
CPU vs GPU, SageMaker Neo for edge) → containerize (ECR, custom containers) → IaC (CloudFormation,
CDK) → auto scaling endpoints → CI/CD for ML (CodePipeline/CodeBuild/CodeDeploy, SageMaker
Pipelines, EventBridge-triggered retraining) → GenAI orchestration (Bedrock Knowledge Bases,
agents).

## Domain 4: Operating, Monitoring, and Securing ML and AI Solutions (24%)

Monitor model/data/infra health (SageMaker Model Monitor for drift, X-Ray for latency, Inference
Recommender for right-sizing) → cost optimization (Spot/On-Demand/Reserved, SageMaker Savings
Plans, Cost Explorer/Budgets) → security (IAM least privilege, VPC isolation, KMS encryption,
Bedrock Guardrails for content filtering).

## Study order

1. [`00-fundamentals/`](../../00-fundamentals) and ideally SAA-C03 (networking/security/storage
   vocabulary this cert assumes) and DVA-C03 Domain 3 (CI/CD — ML pipelines reuse it)
2. Domain 1 (you can't model what you haven't prepared)
3. Domain 2 (the actual ML/FM work)
4. Domain 3 (getting the model into production)
5. Domain 4 (keeping it healthy, cheap, and secure once it's live)

## Status

🚧 Scaffolded — domain folders contain topic checklists; full topic docs being filled in as the
official C02 exam guide finalizes ahead of Jan 2027 GA.
