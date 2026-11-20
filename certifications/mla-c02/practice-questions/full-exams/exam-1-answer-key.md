# MLA-C02 Full Mock Exam 1 — Answer Key

Answers and full explanations for [`exam-1-questions.md`](exam-1-questions.md). Score yourself out of 1000 (points per question ≈ 1000/65 ≈ 15.4; AWS scales 100–1000, passing is 720/1000 — see [`index.md`](index.md)).

## Domain mix in this exam

| Domain | Questions | Target weight |
|---|---|---|
| 1 — Data Preparation for ML and AI | 18 | 28% |
| 2 — ML Model and Foundation Model Development | 16 | 24% |
| 3 — Deployment and Orchestration of ML Workflows | 16 | 24% |
| 4 — Operating, Monitoring, and Securing ML Solutions | 15 | 24% |
| **Total** | **65** | **100%** |

Multi-select ("Choose TWO") questions: 8/65 (12%).

---

## Q1 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: B**

**Explanation:** A sub-2-second, continuously arriving workload is the textbook case for **Amazon Kinesis Data Streams**: it ingests records as they occur and lets a downstream consumer (Lambda, KDA, or a custom app) compute features and react within milliseconds to seconds. See [`services/analytics/kinesis-family.md`](../../../../services/analytics/kinesis-family.md) and the [Domain 1 README](../../domain-1-data-preparation/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A:** A nightly Glue batch job introduces up to a 24-hour delay, completely incompatible with a 2-second requirement; batch is for periodic, non-urgent transformation.
- **C:** A weekly manual export is even slower and operationally fragile — no automation, prone to error, nowhere near real-time.
- **D:** Data Wrangler is for interactively exploring/cleaning a dataset before modeling, not for streaming ingestion or low-latency feature computation, and 'once per day' alone disqualifies it.

---

## Q2 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: B**

**Explanation:** A large and widening train/validation gap is the definition of **overfitting** — the model has started memorizing training-set noise instead of the general pattern. Standard fixes are **regularization** (L1/L2, dropout), **early stopping**, or increasing training data diversity. See [`ml-fundamentals-glossary.md`](../../domain-2-model-development/ml-fundamentals-glossary.md).

**Why the others are wrong:**
- **A:** Underfitting shows *both* training and validation performance as poor; here training performance is excellent, which rules out underfitting.
- **C:** Data drift is a post-deployment phenomenon affecting live inference inputs, not a train/validation gap observed during model development.
- **D:** Class imbalance would show up as a skewed confusion matrix, not specifically as a widening train/validation accuracy gap.

---

## Q3 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: B**

**Explanation:** **Batch Transform** is designed exactly for this: it spins up compute, processes an entire dataset, writes results, and tears down, with no persistent endpoint cost — ideal for scheduled, non-interactive bulk scoring. See [`services/machine-learning-ai/sagemaker-deployment-endpoints.md`](../../../../services/machine-learning-ai/sagemaker-deployment-endpoints.md).

**Why the others are wrong:**
- **A:** A 24/7 real-time endpoint bills continuously even when idle most of the day, which is wasteful for a once-nightly batch job.
- **C:** Serverless Inference is built for intermittent *real-time* request/response traffic with cold-start tolerance, not for a single large scheduled batch job.
- **D:** Asynchronous Inference is for individual large-payload or long-running requests queued one at a time, not for efficiently processing a 2-million-record batch job.

---

## Q4 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: B**

**Explanation:** **Data drift** means the *inputs* look statistically different now than during training; Model Monitor detects this by comparing live input statistics against a training-time baseline, independent of whether accuracy has actually changed. See [`services/machine-learning-ai/sagemaker-model-monitor-and-registry.md`](../../../../services/machine-learning-ai/sagemaker-model-monitor-and-registry.md).

**Why the others are wrong:**
- **A:** Concept drift specifically means the relationship between inputs and the correct output has changed, detected via fresh ground truth labels — not just input-statistics shift.
- **C:** Overfitting is a training-time train/validation gap problem, unrelated to post-deployment input shifts.
- **D:** Model parallelism is a distributed-training technique, unrelated to drift monitoring.

---

## Q5 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A**

**Explanation:** A **Glue Crawler** inspects data in S3, infers schema/partitions, and writes that metadata into the **Glue Data Catalog** — a single shared catalog that Athena, Redshift Spectrum, EMR, and SageMaker can all read, eliminating per-team schema duplication. See [`services/analytics/glue.md`](../../../../services/analytics/glue.md) and [`services/analytics/data-lake-concepts.md`](../../../../services/analytics/data-lake-concepts.md).

**Why the others are wrong:**
- **B:** Standing up a separate RDS database per team duplicates data, adds operational overhead, and still doesn't give a shared catalog for the S3-resident data.
- **C:** Data Wrangler flows are per-user visual prep sessions, not a durable, queryable shared metadata catalog.
- **D:** Firehose delivers streaming data *into* S3; it doesn't crawl existing S3 data or populate a schema catalog.

---

## Q6 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: B**

**Explanation:** Poor performance on *both* training and validation sets is **underfitting** — the model is too simple to capture the true pattern. The fix is to increase model capacity (more expressive algorithm, polynomial/interaction features) or add more informative features. See [`ml-fundamentals-glossary.md`](../../domain-2-model-development/ml-fundamentals-glossary.md).

**Why the others are wrong:**
- **A:** Dropout reduces model capacity further, which would make underfitting worse, not better.
- **C:** Data leakage typically causes *suspiciously high* performance, not uniformly poor performance across both sets.
- **D:** Vanishing gradients is a deep-neural-network training pathology; it wouldn't explain poor fit in a simple linear regression on non-linear data.

---

## Q7 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** A **SageMaker multi-model endpoint** hosts many models behind one endpoint on shared instances, loading each model into memory on demand and caching it, which is the standard cost-efficient pattern for many low-traffic models. See [`services/machine-learning-ai/sagemaker-deployment-endpoints.md`](../../../../services/machine-learning-ai/sagemaker-deployment-endpoints.md).

**Why the others are wrong:**
- **B:** 200 separate always-on endpoints each billed independently is exactly the expensive pattern the team wants to avoid.
- **C:** Models generally cannot simply be concatenated into one file without re-architecting training entirely, and this isn't how SageMaker model packaging works.
- **D:** Retraining as a single multi-class classifier requires completely different training data/labels and changes the underlying ML problem, not just the deployment pattern.

---

## Q8 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** **Bedrock Guardrails** sit between the user and the foundation model, enforcing denied-topic filters and PII detection/redaction on both input and output, exactly addressing off-limits topics and leaked PII. See [`responsible-ai-and-guardrails.md`](../../domain-4-monitoring-security/responsible-ai-and-guardrails.md).

**Why the others are wrong:**
- **B:** SageMaker Clarify measures bias/explainability for classic ML models; it doesn't filter GenAI conversational input/output content.
- **C:** Context window size affects how much text a model can process; it has no content-filtering capability.
- **D:** AWS WAF protects web applications from common exploits (SQL injection, XSS) at the network/HTTP layer; it doesn't understand or filter conversational content topics.

---

## Q9 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: C**

**Explanation:** **Data Wrangler's Data Quality and Insights report** is purpose-built for this: a few clicks produce a report on missing values, class imbalance, and correlation between sensitive attributes and the target, with no code required. See [`services/machine-learning-ai/sagemaker-data-wrangler-and-feature-store.md`](../../../../services/machine-learning-ai/sagemaker-data-wrangler-and-feature-store.md).

**Why the others are wrong:**
- **A:** Glue Jobs are code/Spark-driven ETL; they have no built-in bias/imbalance reporting UI.
- **B:** Athena runs SQL over data already in S3 — it can help you *write* a bias query manually, but it has no built-in bias-report feature.
- **D:** EMR is a managed big-data cluster for code-driven processing; it isn't a no-code tool and has no built-in bias report.

---

## Q10 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: B**

**Explanation:** **Recall** (true positives / (true positives + false negatives)) measures how many actual positive cases the model catches. Prioritizing recall is correct when missing a true case (false negative) is far costlier than a false alarm, as in disease screening. See [`ml-fundamentals-glossary.md`](../../domain-2-model-development/ml-fundamentals-glossary.md).

**Why the others are wrong:**
- **A:** Precision measures how many *flagged* cases are truly positive; optimizing for precision alone would make the model more conservative about flagging, increasing missed cases — the opposite of what's needed here.
- **C:** Specificity measures how well the model identifies true negatives; prioritizing it would also push toward fewer positive flags, increasing false negatives.
- **D:** Raw accuracy on an imbalanced disease dataset (most patients healthy) can look high while still missing most true disease cases — it hides exactly the failure mode described.

---

## Q11 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** **SageMaker Serverless Inference** automatically scales capacity up and down (including to zero) based on traffic and charges only for compute used, trading some cold-start latency for no idle-capacity cost — the right fit for spiky, intermittent traffic. See [`services/machine-learning-ai/sagemaker-deployment-endpoints.md`](../../../../services/machine-learning-ai/sagemaker-deployment-endpoints.md).

**Why the others are wrong:**
- **B:** Provisioning for peak load 24/7 means paying for capacity that sits idle during the long zero-traffic periods, which is wasteful.
- **C:** Batch Transform is for offline bulk scoring jobs, not responding to unpredictable real-time request bursts.
- **D:** Manual EC2 scaling scripts reintroduce operational overhead the team explicitly wants to avoid managing.

---

## Q12 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: B**

**Explanation:** **Least privilege** means scoping IAM policy actions and resources as narrowly as possible: specific S3 actions limited to the exact bucket/prefix ARN, and `kms:Decrypt` limited to the specific key ARN the job actually needs — nothing broader. See [`services/security-identity-compliance/iam.md`](../../../../services/security-identity-compliance/iam.md) and [`services/security-identity-compliance/kms.md`](../../../../services/security-identity-compliance/kms.md).

**Why the others are wrong:**
- **A:** Wildcard `s3:*`/`kms:*` across all resources grants vastly more access than needed, violating least privilege and creating unnecessary blast radius.
- **C:** AdministratorAccess grants full control over the entire AWS account — the opposite of least privilege for a training job role.
- **D:** Public bucket access for training data is a serious security exposure, not a substitute for a properly scoped IAM role.

---

## Q13 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A and B**

**Explanation:** Class imbalance is fixed by rebalancing what the model sees: **resampling** (oversampling the minority class, SMOTE) or **class weighting** (penalizing minority-class errors more) are the two standard data-preparation remedies. See the [Domain 1 README's class imbalance scenario](../../domain-1-data-preparation/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **C:** More epochs just replays the same imbalanced data more times — it reinforces, rather than fixes, the skew and risks overfitting the majority class.
- **D:** Learning rate controls convergence speed; it has no mechanism for correcting a data distribution problem.
- **E:** Shrinking the validation set only makes evaluation less reliable — it does nothing to the training distribution's imbalance.

---

## Q14 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: B**

**Explanation:** On a 96%/4% imbalanced dataset, a trivial model that always predicts the majority class also scores ~96% accuracy, so accuracy alone doesn't indicate real predictive skill on the minority class. **Precision, recall, F1, or AUC-PR** reveal whether the model actually identifies churners. See [`ml-fundamentals-glossary.md`](../../domain-2-model-development/ml-fundamentals-glossary.md).

**Why the others are wrong:**
- **A:** This is the classic accuracy trap on imbalanced data — the number looks good but conveys almost no information about minority-class performance.
- **C:** Learning rate is a training hyperparameter, unrelated to which evaluation metric is meaningful.
- **D:** Batch size affects training dynamics, not which metric correctly evaluates an imbalanced classification problem.

---

## Q15 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: B**

**Explanation:** **SageMaker Asynchronous Inference** queues requests, processes large payloads or long-running inference (minutes, not milliseconds) in the background, and can notify the caller via SNS when complete — purpose-built for exactly this pattern. See [`services/machine-learning-ai/sagemaker-deployment-endpoints.md`](../../../../services/machine-learning-ai/sagemaker-deployment-endpoints.md).

**Why the others are wrong:**
- **A:** Real-time endpoints enforce short request timeouts (seconds, not 10 minutes) and are built for low-latency synchronous responses.
- **C:** Serverless Inference also targets short-duration real-time requests; it isn't designed for multi-minute processing per request.
- **D:** Holding a synchronous HTTP connection open for 10 minutes is fragile, resource-wasteful, and against the design of most API gateways/load balancers.

---

## Q16 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A and B**

**Explanation:** Running SageMaker in a **VPC with no internet gateway**, paired with **VPC endpoints (AWS PrivateLink)** for S3 and other AWS service APIs, together let jobs/endpoints communicate with AWS services entirely over the AWS private network, without any public internet path. See [`services/networking-content-delivery/vpc-endpoints-privatelink.md`](../../../../services/networking-content-delivery/vpc-endpoints-privatelink.md) and [`services/networking-content-delivery/vpc.md`](../../../../services/networking-content-delivery/vpc.md).

**Why the others are wrong:**
- **C:** A public IP with an open security group directly contradicts the 'no direct path to the public internet' requirement.
- **D:** Disabling encryption is a security regression unrelated to network path isolation, and doesn't address the internet-access requirement at all.
- **E:** A NAT Gateway with full outbound internet access still permits general internet egress, which the policy explicitly disallows.

---

## Q17 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: B**

**Explanation:** This is **training/serving skew**. SageMaker Feature Store computes a feature once and serves it from both an **Offline Store** (bulk training) and an **Online Store** (millisecond lookups for real-time inference), guaranteeing the two paths see the identical value. See [`services/machine-learning-ai/sagemaker-data-wrangler-and-feature-store.md`](../../../../services/machine-learning-ai/sagemaker-data-wrangler-and-feature-store.md).

**Why the others are wrong:**
- **A:** The Offline Store has batch-level latency and isn't designed for real-time inference lookups, so using it alone doesn't solve the serving-path mismatch.
- **C:** Retraining more often reproduces the same skew each time, since the code paths are still inconsistent.
- **D:** This is a feature-computation mismatch, not a model-complexity/bias-variance problem; a simpler algorithm doesn't touch it.

---

## Q18 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: A**

**Explanation:** **SageMaker Automatic Model Tuning** (hyperparameter optimization) supports a **Bayesian search strategy** that models the relationship between hyperparameters and objective metric, using past trial results to pick more promising values next — far more sample-efficient than grid or random search for expensive training jobs. See [`services/machine-learning-ai/sagemaker-training-and-tuning.md`](../../../../services/machine-learning-ai/sagemaker-training-and-tuning.md).

**Why the others are wrong:**
- **B:** A hand-coded grid search tries combinations exhaustively (or on a fixed grid) without learning from prior results, and is far less efficient and harder to operate at scale.
- **C:** Repeating identical hyperparameters provides no new information and wastes compute.
- **D:** Ground Truth is a data-labeling service; it has no role in hyperparameter tuning.

---

## Q19 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: B**

**Explanation:** **SageMaker Pipelines** is the native CI/CD-for-ML orchestration service: it chains processing, training, evaluation, and conditional registration steps into a versioned, repeatable, trackable workflow with native Model Registry integration. See [`services/machine-learning-ai/sagemaker-pipelines.md`](../../../../services/machine-learning-ai/sagemaker-pipelines.md).

**Why the others are wrong:**
- **A:** Manually chaining Lambda functions with no orchestration layer means building your own state tracking, retries, and conditional logic from scratch.
- **C:** QuickSight is a BI/dashboarding tool with no role in orchestrating training pipelines.
- **D:** Glue DataBrew is a visual data-prep tool, not a pipeline-orchestration or model-registry service.

---

## Q20 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A and B**

**Explanation:** **KMS customer-managed keys (CMKs)** give the company control over key policies, rotation, and the ability to revoke access, which satisfies the encryption/control requirement, and enabling **CloudTrail** to log every KMS key API call satisfies the audit-trail requirement — the two together fully meet the stated compliance need. See [`services/security-identity-compliance/kms.md`](../../../../services/security-identity-compliance/kms.md) and [`services/management-governance/cloudtrail.md`](../../../../services/management-governance/cloudtrail.md).

**Why the others are wrong:**
- **C:** AWS-managed keys (SSE-S3/SSE-KMS with AWS-owned keys) don't give the company control over the key or its policy, which the requirement explicitly calls for (customer-managed).
- **D:** Network isolation (private subnet) doesn't substitute for encryption at rest, which is a separate compliance requirement.
- **E:** Client-side-only encryption misses the requirement to also encrypt the SageMaker endpoint's underlying storage volumes server-side.

---

## Q21 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: C**

**Explanation:** An **S3 Lifecycle policy** that transitions objects to **Intelligent-Tiering** (or explicitly to Standard-IA / Glacier Instant Retrieval) after the hot period automatically lowers storage cost once access drops off, while keeping minutes-level retrieval. See [`services/storage/s3-storage-classes.md`](../../../../services/storage/s3-storage-classes.md).

**Why the others are wrong:**
- **A:** S3 Standard is priced for frequent access; paying that rate indefinitely for rarely-accessed data wastes money.
- **B:** Glacier Deep Archive has multi-hour to ~12-hour retrieval times, which fails the 'minutes' requirement, and moving data there immediately also loses the cheap-enough tier for the first active month.
- **D:** Deleting training data that might be needed again is operationally risky and isn't a storage-tiering decision at all.

---

## Q22 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: A**

**Explanation:** **XGBoost** is the standard, high-performing built-in choice for structured/tabular classification and regression problems on SageMaker, frequently winning out over deep learning for this kind of data with far less tuning effort.

**Why the others are wrong:**
- **B:** CNNs are designed for grid-like data such as images; they are not the natural fit for tabular credit data and require substantially more engineering.
- **C:** Seq2Seq is for sequence-to-sequence tasks like translation/summarization, not tabular classification.
- **D:** Object2Vec produces embeddings for a variety of inputs but isn't the standard off-the-shelf solution for a straightforward tabular credit risk classifier.

---

## Q23 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A and B**

**Explanation:** SageMaker endpoints support multiple **production variants** with configurable **traffic weighting** for gradual A/B rollout, and separately support **shadow testing** patterns where a candidate model's predictions are captured and compared against the live model with little or no effect on the response the user actually receives — both are standard safe-rollout techniques before a full cutover. See [`services/machine-learning-ai/sagemaker-deployment-endpoints.md`](../../../../services/machine-learning-ai/sagemaker-deployment-endpoints.md).

**Why the others are wrong:**
- **C:** Immediately replacing the old model with no gradual rollout removes any safety net if the new model underperforms in production.
- **D:** Ground Truth is a labeling service; it has no role in traffic-splitting or shadow deployment strategies.
- **E:** Glue crawlers discover data schema; they are unrelated to endpoint deployment traffic management.

---

## Q24 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: B**

**Explanation:** Extreme, erroneous values are an **outlier** problem, best handled in data preparation by detecting and either removing or **capping (winsorizing)** them so they stop dominating the loss function, especially for models sensitive to scale like linear regression.

**Why the others are wrong:**
- **A:** One-hot encoding is for categorical variables, not for fixing extreme numeric outliers.
- **C:** A higher learning rate changes how fast the model converges; it doesn't address a data-quality problem and can make training less stable.
- **D:** More epochs just lets the model fit the bad outliers more, not less.

---

## Q25 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** **SageMaker Managed Spot Training** can cut training costs significantly (up to ~90%) by using spare EC2 capacity, and because the job isn't time-critical and supports **checkpointing**, any Spot interruption simply resumes from the last checkpoint rather than losing all progress. See [`services/machine-learning-ai/sagemaker-training-and-tuning.md`](../../../../services/machine-learning-ai/sagemaker-training-and-tuning.md) and [`ml-cost-optimization.md`](../../domain-4-monitoring-security/ml-cost-optimization.md).

**Why the others are wrong:**
- **B:** On-Demand at full price pays the highest rate for a workload that explicitly tolerates interruption, wasting the Spot savings opportunity.
- **C:** A 3-year Reserved Instance commitment doesn't make sense for a single one-time 10-hour training job; RIs are for sustained, predictable long-term usage.
- **D:** Provisioned Concurrency is a Lambda cold-start feature; it has no relevance to SageMaker training cost optimization.

---

## Q26 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: B**

**Explanation:** **Fine-tuning** changes *how* a model behaves — tone, format, persona, domain vocabulary — which is exactly the need here, versus RAG, which changes what facts the model has access to. See [`embeddings-and-rag-data-prep.md`](../../domain-1-data-preparation/embeddings-and-rag-data-prep.md#rag-vs-fine-tuning-vs-prompting--a-direct-comparison).

**Why the others are wrong:**
- **A:** RAG is for grounding answers in current/private facts/documents; it doesn't reliably change the model's tone or output format on its own.
- **C:** Higher temperature increases output randomness/creativity; it does not impose a consistent tone or format.
- **D:** Context window size is a capacity limit on how much text the model can see per call; it has no bearing on enforcing a consistent tone.

---

## Q27 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** **Application Auto Scaling for SageMaker endpoints** adjusts the instance count up or down based on a target-tracking metric (e.g., `SageMakerVariantInvocationsPerInstance`), keeping always-warm instances for low latency while scaling down during quiet periods to save cost. See [`services/machine-learning-ai/sagemaker-deployment-endpoints.md`](../../../../services/machine-learning-ai/sagemaker-deployment-endpoints.md).

**Why the others are wrong:**
- **B:** Sizing permanently for peak traffic wastes money overnight when traffic is near zero.
- **C:** Batch Transform doesn't serve real-time, instantly-responsive requests at all; it's for offline bulk scoring.
- **D:** Manually deleting/recreating the endpoint daily is operationally fragile and causes downtime windows, unlike automated scaling.

---

## Q28 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: B**

**Explanation:** **One-hot encoding** is correct for nominal (unordered) categories: it avoids implying a false numeric order between categories that plain label encoding would introduce (e.g., implying DHL > UPS).

**Why the others are wrong:**
- **A:** Label encoding imposes an artificial ordinal relationship (0 < 1 < 2 < 3) between categories that have no real order, which many models (especially linear ones) will misinterpret as meaningful magnitude.
- **C:** Most ML algorithms require numeric input; raw text categories generally cannot be consumed directly.
- **D:** Min-max scaling is for numeric continuous features, not categorical ones.

---

## Q29 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** **SageMaker Savings Plans** offer a discounted rate in exchange for a committed, consistent amount of usage over 1 or 3 years, which fits a steady, predictable, long-running real-time endpoint far better than On-Demand pricing. See [`ml-cost-optimization.md`](../../domain-4-monitoring-security/ml-cost-optimization.md).

**Why the others are wrong:**
- **B:** Managed Spot Training applies to training jobs, which tolerate interruption; it doesn't apply to a persistent real-time inference endpoint needing continuous availability.
- **C:** On-Demand with no commitment is the most expensive option for a workload whose steady, predictable usage is exactly what a Savings Plan is discounted for.
- **D:** Serverless Inference is optimized for intermittent/spiky traffic, not for a workload that's steady and predictable 24/7 — a provisioned endpoint under a Savings Plan is more cost-effective here.

---

## Q30 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: B**

**Explanation:** **AUC-ROC** summarizes a classifier's ability to rank a randomly chosen positive example above a randomly chosen negative one, across every possible decision threshold. A 0.92 vs. 0.68 AUC is a large, meaningful gap favoring Classifier A's discriminative power. See [`ml-fundamentals-glossary.md`](../../domain-2-model-development/ml-fundamentals-glossary.md).

**Why the others are wrong:**
- **A:** Training speed is unrelated to AUC, which measures discriminative quality, not computational cost.
- **C:** AUC-ROC is specifically a classification metric; it doesn't apply to regression at all.
- **D:** AUC is a well-established, meaningful discriminative-power metric — dismissing a 0.92 vs 0.68 gap as meaningless is incorrect.

---

## Q31 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: B**

**Explanation:** **Bedrock Knowledge Bases** manages the entire RAG pipeline for you: ingesting documents from a data source like S3, chunking and embedding them, storing vectors in a managed vector store, and handling retrieval at query time — no custom vector database or embedding pipeline to operate. See [`services/machine-learning-ai/bedrock.md`](../../../../services/machine-learning-ai/bedrock.md) and [`embeddings-and-rag-data-prep.md`](../../domain-1-data-preparation/embeddings-and-rag-data-prep.md).

**Why the others are wrong:**
- **A:** Guardrails filters unsafe input/output content; it has no retrieval or document-grounding capability.
- **C:** Bedrock Agents orchestrate actions/tools and can call a Knowledge Base, but on their own (without one) they have no built-in document retrieval pipeline.
- **D:** Ground Truth is for labeling training data, unrelated to RAG document retrieval.

---

## Q32 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A**

**Explanation:** **Feature scaling** (standardization to zero mean/unit variance, or min-max normalization to a [0,1] range) puts features on comparable scales so gradient descent converges efficiently instead of being dominated by the feature with the largest raw magnitude.

**Why the others are wrong:**
- **B:** One-hot encoding applies to categorical variables, not to rescaling continuous numeric ranges.
- **C:** Discarding a potentially predictive feature to work around a scaling problem throws away information unnecessarily.
- **D:** Batch size affects how many examples are used per gradient update; it doesn't correct the underlying feature-scale imbalance.

---

## Q33 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** **AWS CloudTrail** records every API call made in the account (the caller identity, source IP, request parameters, and timestamp), providing exactly the kind of immutable governance/audit trail an auditor needs for SageMaker API activity. See [`services/management-governance/cloudtrail.md`](../../../../services/management-governance/cloudtrail.md).

**Why the others are wrong:**
- **B:** CloudWatch Metrics tracks numeric performance data (invocation counts, latency) over time, not a detailed record of who called which API and when.
- **C:** Cost Explorer analyzes billing/cost trends, not API call history.
- **D:** Macie discovers sensitive data in S3; it has no API call auditing function.

---

## Q34 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A and B**

**Explanation:** A **stratified split** keeps the same minority/majority class ratio in each partition so validation and test sets still contain a representative number of positive examples, and pairing that with **minority-class-aware metrics** (recall, F1, AUC-PR) ensures the evaluation actually reflects performance on the rare class rather than being dominated by the easy majority class.

**Why the others are wrong:**
- **C:** A naive random split can, by chance, leave validation/test sets with almost no positive examples, making evaluation metrics meaningless.
- **D:** Holding out zero positive examples for validation/test makes it impossible to measure how well the model generalizes to the minority class.
- **E:** Alphabetical sorting has nothing to do with preserving class ratios and could introduce its own ordering bias.

---

## Q35 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: B**

**Explanation:** **Transfer learning** — starting from a model pre-trained on a large, general dataset (easily accessed via **SageMaker JumpStart**) and fine-tuning its later layers on the small, specific dataset — reaches strong accuracy with far less data and training time than training from scratch. See [`services/machine-learning-ai/jumpstart.md`](../../../../services/machine-learning-ai/jumpstart.md).

**Why the others are wrong:**
- **A:** Training a deep CNN from scratch typically needs tens of thousands to millions of labeled examples to generalize well; 800 images will badly overfit.
- **C:** K-means is unsupervised clustering, not a solution for a supervised labeled classification task.
- **D:** Using even fewer images (10) sharply worsens the data scarcity problem instead of addressing it.

---

## Q36 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** **Bedrock Agents** orchestrate multi-step reasoning and tool use: you define **action groups** backed by Lambda functions or APIs, and the agent decides which actions to invoke and in what sequence to fulfill a user's request — exactly the order-status-then-refund workflow described. See [`services/machine-learning-ai/bedrock.md`](../../../../services/machine-learning-ai/bedrock.md).

**Why the others are wrong:**
- **B:** Plain prompting has no mechanism to actually call external APIs or Lambda functions; it can only generate text.
- **C:** Guardrails filters content for safety; it doesn't orchestrate multi-step actions or tool invocation.
- **D:** Batch Transform is for offline batch inference scoring, with no concept of interactive multi-step tool orchestration.

---

## Q37 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** **SageMaker Clarify** computes post-training bias metrics (such as disparate impact) by examining the trained model's actual predictions across groups, distinct from its pre-training metrics which examine the raw data before any model exists. See [`responsible-ai-and-guardrails.md`](../../domain-4-monitoring-security/responsible-ai-and-guardrails.md).

**Why the others are wrong:**
- **B:** Bedrock Guardrails is a GenAI content-filtering feature for foundation models, not a bias-metric tool for a classic trained credit model.
- **C:** AWS Config tracks resource configuration compliance (e.g., is encryption enabled), not statistical bias in model predictions.
- **D:** Comprehend sentiment analysis analyzes text sentiment/entities; it has no bias-detection function for a credit-scoring model's predictions.

---

## Q38 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A**

**Explanation:** **Amazon Macie** uses machine learning and pattern matching to automatically discover and classify sensitive data (PII, SSNs, credentials) stored in S3, which is exactly the discovery step needed before a compliant training pipeline can proceed. See [`services/security-identity-compliance/macie.md`](../../../../services/security-identity-compliance/macie.md).

**Why the others are wrong:**
- **B:** The Glue Data Catalog stores schema metadata; it doesn't scan content for sensitive data patterns.
- **C:** Athena can be used to query data once you know what to look for, but it has no automated sensitive-data discovery/classification capability of its own.
- **D:** Ground Truth is for generating labeled training data, not for detecting PII.

---

## Q39 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: A and B**

**Explanation:** **L1 (Lasso)** and **L2 (Ridge)** are the two classic regularization techniques: L1 can zero out coefficients entirely (built-in feature selection), while L2 shrinks all coefficients smoothly without necessarily eliminating any — both reduce overfitting by constraining coefficient magnitude. See [`ml-fundamentals-glossary.md`](../../domain-2-model-development/ml-fundamentals-glossary.md).

**Why the others are wrong:**
- **C:** Increasing polynomial degree adds model complexity, which worsens overfitting rather than reducing it.
- **D:** Removing the validation set eliminates your ability to detect overfitting; it doesn't regularize the model at all.
- **E:** Unbounded additional epochs on an already-overfitting model increases memorization of training noise.

---

## Q40 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** **SageMaker Model Registry** groups model versions into model package groups, tracks metadata/lineage, and supports an approval status (Pending/Approved/Rejected) that a pipeline can gate production deployment on, giving the auditable manual sign-off step required. See [`services/machine-learning-ai/sagemaker-model-monitor-and-registry.md`](../../../../services/machine-learning-ai/sagemaker-model-monitor-and-registry.md).

**Why the others are wrong:**
- **B:** Deploying directly from a notebook bypasses any approval gate or versioned history entirely.
- **C:** The Glue Data Catalog stores data schema metadata, not model version approval workflows.
- **D:** CloudFront is a content delivery network; it has no role in model governance or approval tracking.

---

## Q41 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** **SageMaker Clarify's explainability feature (SHAP values)** computes, for an individual prediction, how much each input feature contributed positively or negatively to that specific outcome — exactly what's needed to answer a regulator's per-applicant 'why was this decision made' question. See [`responsible-ai-and-guardrails.md`](../../domain-4-monitoring-security/responsible-ai-and-guardrails.md).

**Why the others are wrong:**
- **B:** Ground Truth is a data-labeling service; it has no explainability function for existing model predictions.
- **C:** QuickSight visualizes data/dashboards; it doesn't compute per-prediction feature attribution.
- **D:** Trusted Advisor gives account-level best-practice checks, unrelated to per-prediction model explainability.

---

## Q42 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: C**

**Explanation:** RAG data-prep quality depends heavily on **chunking strategy**: choosing an appropriately sized chunk for the content and adding **overlap** between consecutive chunks prevents a single idea from being split awkwardly across a hard boundary, improving retrieval relevance. See [`embeddings-and-rag-data-prep.md`](../../domain-1-data-preparation/embeddings-and-rag-data-prep.md).

**Why the others are wrong:**
- **A:** A larger generation model can't compensate for retrieval that never surfaced the needed context in the first place — this is a data-prep problem, not a generation-model problem.
- **B:** Making chunks as small as possible can split ideas even more aggressively and lose surrounding context, worsening the exact symptom described.
- **D:** Pasting the whole 2,000-page document into every prompt blows past context window limits and defeats the purpose of using RAG at all.

---

## Q43 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: B**

**Explanation:** Since false negatives (missed qualified candidates) are the costlier error here, the team should **lower the decision threshold for the positive/'advance' class**, which increases recall at the expense of precision — trading more false positives (low-cost) for fewer false negatives (high-cost), matching the stated business cost asymmetry.

**Why the others are wrong:**
- **A:** Overall accuracy doesn't reflect the business's asymmetric cost structure between false negatives and false positives described in the scenario.
- **C:** Raising the threshold reduces false positives but increases false negatives — the opposite of what the stated business priority requires.
- **D:** This is a supervised classification problem with labeled outcomes; switching to unsupervised clustering abandons the labels and the whole point of the task.

---

## Q44 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** **SageMaker Inference Recommender** runs automated load tests of your model across a range of instance types/configurations and recommends the one that best balances latency, throughput, and cost for your specific model and traffic pattern. See [`services/machine-learning-ai/sagemaker-deployment-endpoints.md`](../../../../services/machine-learning-ai/sagemaker-deployment-endpoints.md).

**Why the others are wrong:**
- **B:** Trusted Advisor gives general account-level best-practice checks (cost, security, fault tolerance); it doesn't run model-specific inference benchmarking.
- **C:** CloudWatch Logs Insights queries log data after the fact; it doesn't proactively benchmark instance types for a model.
- **D:** Cost Explorer analyzes historical spend; it has no model-performance benchmarking capability.

---

## Q45 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A**

**Explanation:** A Bedrock embedding model (Titan Embeddings or Cohere Embed) produces the vectors, and **OpenSearch Service's vector engine** (or **Bedrock Knowledge Bases**, which manages this under the hood) provides managed, low-latency approximate nearest-neighbor search at scale — the standard AWS RAG pattern. See [`embeddings-and-rag-data-prep.md`](../../domain-1-data-preparation/embeddings-and-rag-data-prep.md) and [`services/analytics/opensearch.md`](../../../../services/analytics/opensearch.md).

**Why the others are wrong:**
- **B:** Redshift is a SQL data warehouse for analytics workloads; it isn't built for millisecond vector similarity search at this scale.
- **C:** String matching can't capture semantic similarity (synonyms, paraphrasing) — the entire reason embeddings exist is to go beyond exact text matches.
- **D:** SQS is a message queue, not a searchable data store; it cannot support similarity search at all.

---

## Q46 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** **Scheduled Model Monitor bias-drift checks** catch fairness degrading *after* deployment as the live population or behavior shifts over time — something a single point-in-time pre-deployment Clarify check cannot catch, since bias (like accuracy) can drift. See [`responsible-ai-and-guardrails.md`](../../domain-4-monitoring-security/responsible-ai-and-guardrails.md#how-it-works) and [`services/machine-learning-ai/sagemaker-model-monitor-and-registry.md`](../../../../services/machine-learning-ai/sagemaker-model-monitor-and-registry.md).

**Why the others are wrong:**
- **B:** Column-name typos are a data-quality/schema issue caught earlier in data prep, not a bias-drift monitoring concern.
- **C:** Public bucket exposure is a security misconfiguration issue, not something bias-drift monitoring checks for.
- **D:** CPU utilization is an infrastructure health metric tracked via CloudWatch, unrelated to bias-drift monitoring.

---

## Q47 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: A and B**

**Explanation:** **RMSE** and **MAE** are both regression metrics that express prediction error in the same units as the target variable (dollars here); RMSE penalizes large errors more heavily (squares them) while MAE weights all errors linearly, and both directly answer 'how far off are the numeric predictions.' See [`ml-fundamentals-glossary.md`](../../domain-2-model-development/ml-fundamentals-glossary.md).

**Why the others are wrong:**
- **C:** F1 score combines precision and recall for classification problems with discrete classes; it doesn't apply to continuous numeric forecasting error.
- **D:** Precision/recall require a notion of positive/negative classes, which doesn't exist in a continuous sales-forecasting regression problem.
- **E:** AUC-ROC is a classification-ranking metric; it has no defined meaning for a continuous-valued regression target.

---

## Q48 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** SageMaker fully supports **Bring Your Own Container (BYOC)**: package arbitrary inference code and framework dependencies into a Docker image, push it to **Amazon ECR**, and point a SageMaker model/endpoint configuration at that image — the standard path for custom frameworks or preprocessing not covered by built-in containers.

**Why the others are wrong:**
- **B:** SageMaker explicitly supports custom containers; built-in algorithms are a convenience, not a hard requirement.
- **C:** Data Wrangler is a data-prep tool with no mechanism for packaging a custom trained model for serving.
- **D:** Lambda has package size and runtime limits that often make it unsuitable for larger custom ML containers without careful workarounds, and it is not the standard SageMaker deployment path described here.

---

## Q49 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: B**

**Explanation:** **SageMaker Ground Truth** is built exactly for this: managed human labeling workflows (including bounding boxes), built-in quality/consensus checks, and **active learning** that progressively hands easy examples to an automated labeling model while routing harder ones to humans.

**Why the others are wrong:**
- **A:** Using Mechanical Turk directly with no tooling means building your own quality control, task routing, and UI from scratch.
- **C:** Glue DataBrew is a visual data-cleaning tool for tabular data, not an image-labeling workflow service.
- **D:** Comprehend is an NLP service (text analysis); it has no role in labeling images for object detection.

---

## Q50 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** **AWS Secrets Manager** stores credentials securely, supports **automatic rotation**, and is retrievable at runtime via IAM-controlled API calls, directly satisfying both the 'no hard-coding' and 'automatic rotation' requirements. See [`services/security-identity-compliance/secrets-manager-vs-parameter-store.md`](../../../../services/security-identity-compliance/secrets-manager-vs-parameter-store.md).

**Why the others are wrong:**
- **B:** Committing a plaintext key to source control is a serious security exposure and provides no rotation capability.
- **C:** A publicly readable S3 object exposes the key to anyone on the internet — the opposite of secure secret storage.
- **D:** Hard-coding the key in code means it ends up in version control history and requires a code deployment to rotate, satisfying neither requirement.

---

## Q51 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: B**

**Explanation:** **Bedrock model evaluation** lets you run a structured evaluation job comparing models on a prompt dataset, using either built-in automatic metrics or human reviewer workflows, giving a repeatable way to choose between candidate foundation models. See [`services/machine-learning-ai/bedrock.md`](../../../../services/machine-learning-ai/bedrock.md).

**Why the others are wrong:**
- **A:** Guardrails filters input/output content for safety; it isn't an evaluation/benchmarking tool for comparing model quality.
- **C:** Bedrock Agents orchestrate multi-step tool use and reasoning; they aren't an evaluation feature for comparing summarization quality.
- **D:** Ground Truth labeling jobs produce training labels; they aren't designed as a built-in model-comparison evaluation workflow for FMs.

---

## Q52 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** **Amazon EventBridge** can match S3 'Object Created' events and trigger a target (e.g., starting a SageMaker Pipelines execution via a Lambda function or direct integration), fully automating the retrain-on-new-data workflow without manual intervention. See [`services/application-integration/eventbridge.md`](../../../../services/application-integration/eventbridge.md).

**Why the others are wrong:**
- **B:** Manual checking is error-prone, slow, and defeats the goal of an automated trigger.
- **C:** CloudFront is a CDN for content delivery; it has no event-driven workflow triggering capability relevant here.
- **D:** Direct Connect is a dedicated network connection service, unrelated to event-driven pipeline triggering.

---

## Q53 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: B**

**Explanation:** Time-series forecasting requires a **chronological (time-based) split** — training on the past and validating/testing on a later period — because a random shuffle would let the model 'see the future' during training (data leakage), producing an overly optimistic and unrealistic evaluation.

**Why the others are wrong:**
- **A:** A random shuffle split mixes future and past data into training, letting the model implicitly learn from dates that should be unseen at evaluation time.
- **C:** Standard shuffled k-fold has the same future-leakage problem as a one-time random split; time series needs a chronological or rolling-origin variant instead.
- **D:** Splitting only by product category ignores the chronological leakage risk entirely.

---

## Q54 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** **Amazon Augmented AI (A2I)** is built specifically to route low-confidence or sensitive predictions to human reviewers before a final action is taken, integrating with both custom ML models and AWS AI services for human-in-the-loop review workflows.

**Why the others are wrong:**
- **B:** AWS Config tracks resource configuration compliance, unrelated to routing predictions for human review.
- **C:** CloudFront is a content delivery network, with no role in human review workflows for model predictions.
- **D:** Direct Connect is a dedicated network connection service, unrelated to human-in-the-loop review.

---

## Q55 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: B**

**Explanation:** Frequently changing facts are the textbook case for **RAG** rather than fine-tuning: updating a knowledge base/vector index is cheap and immediate, whereas RAG grounds the answer in retrieved, current content instead of relying on frozen model knowledge. See [`embeddings-and-rag-data-prep.md`](../../domain-1-data-preparation/embeddings-and-rag-data-prep.md#rag-vs-fine-tuning-vs-prompting--a-direct-comparison).

**Why the others are wrong:**
- **A:** Nightly fine-tuning on fast-changing data is expensive, slow to pipeline, and still stale between runs — exactly the weakness RAG is designed to avoid.
- **C:** Model weights aren't a place to 'hard-code' facts in a retrievable, updatable way, and this isn't how foundation models represent information.
- **D:** Temperature controls output randomness, not factual accuracy or recency of information.

---

## Q56 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** **SageMaker Neo** compiles a trained model to run efficiently on specific edge hardware (optimizing for the target chip/runtime), and edge deployment tooling manages getting that compiled model onto disconnected or intermittently connected devices — the correct pattern for offline/edge inference.

**Why the others are wrong:**
- **B:** A cloud-hosted real-time endpoint requires reliable connectivity, which directly conflicts with the intermittent/no-connectivity requirement.
- **C:** QuickSight is a BI/visualization tool, unrelated to edge model deployment.
- **D:** A Glue Crawler discovers data schema in S3; it has no role in compiling or deploying models to edge devices.

---

## Q57 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: B**

**Explanation:** **AWS Glue ETL (Spark-based) jobs** or **Amazon EMR** are designed for large-scale, code-driven distributed transformation of semi-structured data across massive S3 datasets, including complex joins that need full Spark capability. See [`services/analytics/glue.md`](../../../../services/analytics/glue.md) and [`services/analytics/emr.md`](../../../../services/analytics/emr.md).

**Why the others are wrong:**
- **A:** QuickSight is a BI/visualization tool for dashboards, not a data transformation engine.
- **C:** Data Wrangler's visual UI is meant for exploratory, smaller-scale data prep sampling, not production-scale 80 TB distributed joins.
- **D:** Processing one file at a time in Lambda doesn't parallelize complex cross-dataset joins efficiently and risks timeouts at this scale.

---

## Q58 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** **Amazon GuardDuty** continuously analyzes account activity, VPC flow logs, and DNS logs using threat intelligence and machine learning to detect anomalies like compromised credentials, unusual API activity, or cryptomining-pattern instance usage, across an AWS account/organization. See [`services/security-identity-compliance/guardduty.md`](../../../../services/security-identity-compliance/guardduty.md).

**Why the others are wrong:**
- **B:** Glue is an ETL/data-cataloging service, with no security threat-detection capability.
- **C:** Model Monitor detects data/model quality drift in ML workloads specifically, not general account-level security threats.
- **D:** Kinesis Data Firehose delivers streaming data to destinations like S3; it has no threat-detection function.

---

## Q59 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: A**

**Explanation:** This is overfitting to surface-level wording rather than learning the underlying semantics. **Data augmentation** (paraphrases, synonyms) exposes the model to more linguistic variety of the same intent, and **regularization** discourages memorizing exact phrasing — together pushing the model toward generalizable semantic understanding.

**Why the others are wrong:**
- **B:** A larger vocabulary alone doesn't force the model to generalize across rewordings; it can still memorize per-token patterns.
- **C:** Removing regularization would make the model fit the training wording even more tightly, worsening the generalization problem.
- **D:** Shrinking to only the cleanest examples reduces linguistic diversity further, making the memorization problem worse, not better.

---

## Q60 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** Bedrock Agents maintain **session/conversation state** for the duration of a session, retaining context (like a previously mentioned order number) across multiple turns so the agent doesn't need the user to repeat themselves and can reason using accumulated context.

**Why the others are wrong:**
- **B:** Re-sending the entire knowledge base every turn is not how agent memory works and would be extremely inefficient and unnecessary.
- **C:** Guardrails filters content safety, not conversational memory/state.
- **D:** Model Monitor tracks data/model quality drift post-deployment; it has nothing to do with maintaining conversational state.

---

## Q61 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A**

**Explanation:** **Kinesis Data Firehose** is the fully managed delivery service built exactly for this: it buffers and batches streaming records and writes them to S3 (optionally converting to Parquet/ORC) with no consumer code to write, unlike raw Kinesis Data Streams. See [`services/analytics/kinesis-family.md`](../../../../services/analytics/kinesis-family.md).

**Why the others are wrong:**
- **B:** Kinesis Data Streams requires you to build and operate a consumer application yourself to land data anywhere; it's the lower-level streaming primitive, not the managed delivery layer.
- **C:** A Glue Crawler discovers schema in data that already exists in S3; it doesn't ingest or deliver streaming data there.
- **D:** Redshift Spectrum queries data already in S3 from Redshift; it has no role in landing an incoming IoT stream.

---

## Q62 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** **AWS Config** continuously records resource configuration state and evaluates it against rules (managed or custom), flagging configuration drift from an approved baseline and retaining historical configuration snapshots for audit purposes. See [`services/management-governance/aws-config.md`](../../../../services/management-governance/aws-config.md).

**Why the others are wrong:**
- **B:** QuickSight is for building visualizations/dashboards over data, not for continuous resource-configuration compliance evaluation.
- **C:** Direct Connect is a dedicated network link, unrelated to configuration compliance tracking.
- **D:** Comprehend is an NLP text-analysis service, unrelated to infrastructure configuration auditing.

---

## Q63 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: A**

**Explanation:** **Early stopping** monitors validation loss during training and automatically halts (restoring the best-performing checkpoint) once validation performance stops improving for a patience window, directly preventing the overfitting shown by the climbing validation loss after epoch 40. See [`ml-fundamentals-glossary.md`](../../domain-2-model-development/ml-fundamentals-glossary.md).

**Why the others are wrong:**
- **B:** Training for even more epochs (500) would let the model overfit further past epoch 40, worsening the exact problem described.
- **C:** Removing the validation set eliminates the only signal that detects when overfitting begins, making it impossible to know when to stop.
- **D:** Batch size affects gradient update granularity and training speed, not whether the model continues to overfit past its best epoch.

---

## Q64 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A and B**

**Explanation:** **AWS Step Functions** is built for orchestrating multi-service workflows with retries, branching, and long-running steps via a visual state machine, and **SageMaker Pipelines** is the ML-native way to represent the training/evaluation portion of that workflow — the two combine naturally, with Step Functions able to invoke a Pipelines execution as one state. See [`services/application-integration/step-functions.md`](../../../../services/application-integration/step-functions.md) and [`services/machine-learning-ai/sagemaker-pipelines.md`](../../../../services/machine-learning-ai/sagemaker-pipelines.md).

**Why the others are wrong:**
- **C:** QuickSight is a BI/visualization tool; it has no workflow-orchestration capability.
- **D:** A single Lambda function is capped at 15 minutes of execution time and isn't designed for multi-hour training jobs or durable cross-service orchestration.
- **E:** Route 53 health checks monitor DNS/endpoint availability; they have no role in orchestrating a multi-step ML pipeline.

---

## Q65 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: B**

**Explanation:** A feature that incorporates information from the outcome it's predicting (or from the future relative to the prediction point) is classic **data leakage** — it must be recomputed so that only information available *before* the prediction timestamp is used, or the model will show unrealistically good offline metrics that collapse in production.

**Why the others are wrong:**
- **A:** Leaving leakage in place produces a model that looks excellent offline but fails in production once the leaked signal is unavailable at inference time.
- **C:** Dropout is a regularization technique for reducing overfitting in neural networks; it does not address a feature that structurally contains the label.
- **D:** SMOTE addresses class imbalance, an unrelated problem to a feature leaking future/label information.

---
