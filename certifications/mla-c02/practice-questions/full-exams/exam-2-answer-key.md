# MLA-C02 Full Mock Exam 2 — Answer Key

Answers and full explanations for [`exam-2-questions.md`](exam-2-questions.md). Score yourself out of 1000 (points per question ≈ 1000/65 ≈ 15.4; AWS scales 100–1000, passing is 720/1000 — see [`index.md`](index.md)).

## Domain mix in this exam

| Domain | Questions | Target weight |
|---|---|---|
| 1 — Data Preparation for ML and AI | 18 | 28% |
| 2 — ML Model and Foundation Model Development | 16 | 24% |
| 3 — Deployment and Orchestration of ML Workflows | 16 | 24% |
| 4 — Operating, Monitoring, and Securing ML Solutions | 15 | 24% |
| **Total** | **65** | **100%** |

Multi-select ("Choose TWO") questions: 6/65 (9%).

---

## Q1 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A**

**Explanation:** **Kinesis Data Firehose** is the fully managed delivery stream that batches/buffers incoming records on a time or size basis, optionally converts to Parquet, and writes to S3 with zero consumer code to operate — the correct fit for 'deliver into S3 periodically, no custom code.' See [`services/analytics/kinesis-family.md`](../../../../services/analytics/kinesis-family.md).

**Why the others are wrong:**
- **B:** Kinesis Data Streams requires you to build and run your own consumer application to actually land data anywhere, which is exactly the operational burden the team wants to avoid.
- **C:** A Glue Crawler discovers schema for data already resting in S3; it does not ingest a live streaming feed.
- **D:** SNS is a pub/sub notification service for small messages/alerts, not a durable high-throughput data-landing pipeline.

---

## Q2 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: B**

**Explanation:** A single dramatically divergent fold in cross-validation is a strong signal of a **fold-specific data issue** (an unusual subset of rows, a quality problem, or inconsistent class representation in that split) rather than random noise, and should be investigated directly before trusting the average CV score as representative.

**Why the others are wrong:**
- **A:** Dismissing a 29-point swing as 'unlucky' risks hiding a real data problem that would also affect production performance.
- **C:** Learning rate is a training hyperparameter; it wouldn't explain why one specific data fold diverges so sharply from the other four.
- **D:** More epochs across all folds doesn't address why one particular fold's data behaves so differently from the others.

---

## Q3 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** **Batch Transform** is designed exactly for scheduled, large-scale, non-interactive scoring jobs: it spins up compute to process the entire dataset, writes results, and shuts down, with no persistent endpoint cost. See [`services/machine-learning-ai/sagemaker-deployment-endpoints.md`](../../../../services/machine-learning-ai/sagemaker-deployment-endpoints.md).

**Why the others are wrong:**
- **B:** A 24/7 real-time endpoint bills continuously even when idle most of the day, which is wasteful for a once-nightly batch scoring job.
- **C:** Asynchronous Inference is meant for individual large-payload/long-running requests, not for efficiently processing 10 million rows as a single batch job.
- **D:** Serverless Inference targets intermittent real-time request traffic; it isn't the right tool for a single large scheduled nightly batch run.

---

## Q4 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** **CloudWatch Logs Insights** provides an interactive query language purpose-built for searching and analyzing log data stored in CloudWatch Logs, including filtering by time range and pattern-matching error messages, without needing to export and grep raw files. See [`services/management-governance/cloudwatch.md`](../../../../services/management-governance/cloudwatch.md).

**Why the others are wrong:**
- **B:** The Glue Data Catalog stores table/schema metadata for structured datasets, not an interactive log-querying tool.
- **C:** Macie discovers sensitive data in S3; it has no log-query capability.
- **D:** Direct Connect is a dedicated network connection service, unrelated to log analysis.

---

## Q5 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A**

**Explanation:** **AWS Glue ETL jobs in script mode** let you write full Spark code (Python/Scala) for arbitrarily complex joins and branching logic, beyond what a visual/no-code tool can express, while still running as managed, serverless Spark. See [`services/analytics/glue.md`](../../../../services/analytics/glue.md).

**Why the others are wrong:**
- **B:** QuickSight calculated fields are simple formulas for BI visualizations, not a general-purpose data transformation engine.
- **C:** Data Wrangler's visual transforms are powerful for common operations but can't express arbitrary custom code logic the way a Spark script can.
- **D:** CloudWatch Logs Insights queries log data for operational troubleshooting; it isn't a data transformation/ETL engine.

---

## Q6 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: A**

**Explanation:** **Random Forest's** trees are built independently on bootstrapped samples, so training parallelizes naturally and it's relatively robust to hyperparameter choices; **Gradient Boosting's** trees are built sequentially, each fitting the residual error of the prior ensemble, which often yields higher accuracy but is more sensitive to hyperparameters (learning rate, tree depth, number of rounds) and harder to parallelize per-tree.

**Why the others are wrong:**
- **B:** The sequential vs. independent tree-building distinction is a real, exam-relevant structural difference with practical consequences for tuning and parallelism.
- **C:** Random Forest supports both classification and regression tasks.
- **D:** Gradient Boosting absolutely can overfit, especially with too many boosting rounds or too-high learning rate without regularization/early stopping.

---

## Q7 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** A **SageMaker Inference Pipeline** lets you chain multiple containers (e.g., preprocessing, model, postprocessing) behind a single endpoint, with data passed directly between containers on the same instance, minimizing network latency overhead compared to separate round-trips.

**Why the others are wrong:**
- **B:** Calling three separate endpoints sequentially over the network adds multiple round-trip latencies and operational complexity that an inference pipeline avoids.
- **C:** Ground Truth is a labeling service, unrelated to chaining inference containers.
- **D:** Glue DataBrew is a visual data-prep tool, not an inference-serving capability.

---

## Q8 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A and B**

**Explanation:** A **CloudWatch Alarm** watching the Model Monitor drift metric detects the threshold breach, and **EventBridge** (or the alarm action directly) triggers a **Lambda function or Step Functions execution** that kicks off the retraining **SageMaker Pipelines** run — the standard event-driven automated retraining pattern, with no manual trigger. See [`services/machine-learning-ai/sagemaker-model-monitor-and-registry.md`](../../../../services/machine-learning-ai/sagemaker-model-monitor-and-registry.md) and [`services/application-integration/eventbridge.md`](../../../../services/application-integration/eventbridge.md).

**Why the others are wrong:**
- **C:** QuickSight is a BI/visualization tool for dashboards, not an automated event-driven trigger mechanism.
- **D:** Direct Connect is a dedicated network connection, unrelated to triggering automated workflows from a metric breach.
- **E:** Route 53 health checks monitor DNS/endpoint availability, unrelated to triggering a retraining pipeline from a drift metric.

---

## Q9 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A**

**Explanation:** Exact duplicate records from a retry bug directly distort the learned data distribution; the correct data-preparation fix is **deduplication** — identifying and removing the duplicate rows before training so the model doesn't overweight artificially repeated patterns.

**Why the others are wrong:**
- **B:** SMOTE addresses class imbalance in genuinely scarce minority classes; it's unrelated to and doesn't fix duplicate-record pollution.
- **C:** Regularization addresses overfitting to noise in model training; it doesn't remove duplicate rows from the underlying dataset.
- **D:** Changing the algorithm doesn't fix a data-quality problem — any algorithm trained on duplicated data will still learn a skewed distribution.

---

## Q10 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: A**

**Explanation:** A sudden **NaN loss** after previously stable training is a classic sign the **learning rate is too high**, causing weight updates to overshoot and diverge into numerical instability; the standard fixes are lowering the learning rate and/or applying **gradient clipping** to cap update magnitude.

**Why the others are wrong:**
- **B:** Validation set size affects how reliable the evaluation metric is, not why training weights diverge to NaN.
- **C:** Adding more layers increases model complexity/capacity but doesn't address a numerical instability in the optimization process.
- **D:** Reducing batch size further doesn't fix a learning-rate-driven divergence and can make gradient noise worse.

---

## Q11 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** A **SageMaker Savings Plan** trades a committed, consistent usage level over 1 or 3 years for a meaningfully discounted rate, which fits a steady, predictable, long-running real-time endpoint far better than paying full On-Demand rates. See [`ml-cost-optimization.md`](../../domain-4-monitoring-security/ml-cost-optimization.md).

**Why the others are wrong:**
- **B:** On-Demand with no commitment is the most expensive option for a workload whose usage is steady and predictable — exactly the scenario a Savings Plan is discounted for.
- **C:** Serverless Inference is optimized for intermittent/spiky traffic, not steady 24/7 load, and isn't the most cost-efficient choice here.
- **D:** Spot Instances can be reclaimed with short notice, which is risky for a persistent real-time inference endpoint that must always be available to serve requests.

---

## Q12 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** Bedrock Guardrails' **contextual grounding checks** specifically evaluate whether a generated response is adequately supported by the reference/source content provided (e.g., retrieved RAG passages), which is a distinct capability from simple denied-topic or profanity filtering, aimed squarely at reducing hallucination/ungrounded speculation. See [`responsible-ai-and-guardrails.md`](../../domain-4-monitoring-security/responsible-ai-and-guardrails.md).

**Why the others are wrong:**
- **B:** Static word filters catch specific disallowed words/phrases; they don't evaluate whether an entire response is factually grounded in the provided source content.
- **C:** A larger context window changes how much text the model can process, not whether Guardrails evaluates grounding of the output.
- **D:** Ground Truth is a labeling service for training data, unrelated to real-time GenAI output grounding checks.

---

## Q13 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A**

**Explanation:** **Binning (discretization)** a continuous feature into ranges and one-hot (or ordinal) encoding the bins lets a linear model assign a separate coefficient per range, letting it approximate a non-linear relationship that a single linear term on raw age cannot.

**Why the others are wrong:**
- **B:** Removing age discards a feature with real predictive signal rather than reshaping it to be usable.
- **C:** Collapsing to a single boolean cutoff loses most of the granularity the binning approach preserves, likely discarding useful signal.
- **D:** Leaving age raw and continuous is exactly what already fails to capture the non-linear relationship described in the scenario.

---

## Q14 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: A**

**Explanation:** **Focal loss** modifies standard cross-entropy to down-weight the contribution of easy, confidently-correct examples (often the abundant majority class) and focus gradient signal on hard, misclassified examples (often the rare class), complementing data-level fixes like oversampling for severe imbalance.

**Why the others are wrong:**
- **B:** Mean squared error is designed for regression targets, not for a probabilistic binary classification loss, and doesn't address the class-imbalance weighting issue described.
- **C:** Test set size affects evaluation reliability, not the training loss function's behavior on imbalanced classes.
- **D:** Reducing feature count is a dimensionality decision unrelated to how the loss function weights hard vs. easy examples.

---

## Q15 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** **Shadow deployment (shadow testing)** sends a copy of real production traffic to the candidate model so its predictions can be logged and compared against the production model's outputs, without ever exposing users to the candidate model's results — a zero-user-risk way to validate real-world performance.

**Why the others are wrong:**
- **B:** Blue/green with full cutover switches all live traffic to the new version at once (after validation elsewhere), not the side-by-side, hidden-from-users comparison described.
- **C:** Batch Transform is offline bulk scoring, not a live-traffic comparison deployment pattern.
- **D:** Canary deployment deliberately exposes a small fraction of real users to the new version's actual output, unlike shadow testing which keeps the new model's output hidden from users entirely.

---

## Q16 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** **Separation of duties** via distinct, narrowly scoped IAM roles — one for data-scientist sandbox experimentation, a different one with the specific permissions needed to approve Model Registry entries and update production endpoints — enforces that no single broad role can both experiment and unilaterally push to production. See [`services/security-identity-compliance/iam.md`](../../../../services/security-identity-compliance/iam.md).

**Why the others are wrong:**
- **B:** A single broad shared role for everyone eliminates any separation of duties and violates least privilege.
- **C:** IAM is the primary access-control mechanism for AWS APIs; network firewalls alone don't control who can call SageMaker/registry APIs.
- **D:** Granting AdministratorAccess broadly defeats both least privilege and separation of duties entirely.

---

## Q17 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A**

**Explanation:** **Data Wrangler's Quick Model** trains a fast, rough baseline model on the current transformed data to estimate feature importance and ballpark performance, letting a data scientist sanity-check their feature engineering before investing in a full SageMaker training job. See [`services/machine-learning-ai/sagemaker-data-wrangler-and-feature-store.md`](../../../../services/machine-learning-ai/sagemaker-data-wrangler-and-feature-store.md).

**Why the others are wrong:**
- **B:** Quick Model is a fast sanity check, not a substitute for proper model development, tuning, and evaluation.
- **C:** Quick Model has nothing to do with data encryption.
- **D:** Quick Model produces a rough diagnostic estimate, not a deployable inference endpoint.

---

## Q18 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: A**

**Explanation:** **Model parallelism** splits a single model's layers/parameters across multiple devices when the model itself is too large to fit on one GPU, with each device handling a different portion of the computation for every training step — distinct from splitting the *data* across devices.

**Why the others are wrong:**
- **B:** Data parallelism keeps a full copy of the model on each device and splits the *training data* across devices instead, which doesn't help when the model itself can't fit on a single GPU.
- **C:** K-fold cross-validation is an evaluation technique for estimating generalization error, unrelated to distributing model computation across GPUs.
- **D:** Transfer learning reuses a pre-trained model's learned weights as a starting point; it's unrelated to how training computation is distributed across hardware.

---

## Q19 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** **AWS CodePipeline** (orchestration) and **AWS CodeBuild** (build/test) are the standard CI/CD building blocks, and **SageMaker Projects** provides pre-built MLOps templates that wire these together with SageMaker Pipelines executions and approval gates, giving code-commit-triggered, auditable ML CI/CD.

**Why the others are wrong:**
- **B:** QuickSight is a BI/visualization tool with no CI/CD or deployment-triggering capability.
- **C:** Manual script execution from a laptop is exactly the unautomated, non-reproducible process CI/CD is meant to replace.
- **D:** Route 53 health checks monitor DNS/endpoint availability; they have no role in triggering a CI/CD pipeline from a code commit.

---

## Q20 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** Cross-account access to KMS-encrypted data requires explicitly granting the other account's principal `kms:Decrypt` (and related) permissions in the **key policy**, plus a matching S3 **bucket policy** permission — scoped, auditable cross-account trust, not public exposure. See [`services/security-identity-compliance/kms.md`](../../../../services/security-identity-compliance/kms.md).

**Why the others are wrong:**
- **B:** Making the bucket/key public exposes the data to the entire internet, far beyond the specific trusted account that needs access — a serious security anti-pattern.
- **C:** Disabling encryption removes a required compliance/security control rather than solving the access-sharing problem correctly.
- **D:** KMS key material cannot be (and should not be) manually copied between accounts; KMS keys are managed via policy-based permissions, not key export.

---

## Q21 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A**

**Explanation:** This is **active learning** within SageMaker Ground Truth: an automated labeling model progressively takes over confidently-classifiable examples, while uncertain/ambiguous examples still route to human reviewers, substantially cutting the human labeling workload and cost without sacrificing quality on hard cases.

**Why the others are wrong:**
- **B:** Data drift describes post-deployment input distribution shifts, unrelated to a labeling-job's automation feature.
- **C:** Regularization is a model-training technique to reduce overfitting, unrelated to labeling workflow automation.
- **D:** Batch Transform is a SageMaker inference feature for scoring data with an already-trained model, not a labeling-job capability.

---

## Q22 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: A and B**

**Explanation:** **ROUGE** and **BLEU** are the two standard n-gram-overlap metrics for automatically scoring generated text against human references: ROUGE is recall-oriented and common for summarization, while BLEU is precision-oriented (with a brevity penalty) and historically standard for machine translation.

**Why the others are wrong:**
- **C:** RMSE is a regression error metric for continuous numeric targets, not applicable to comparing generated text against reference text.
- **D:** AUC-ROC is a classification-ranking metric; it has no defined way to compare two pieces of generated text.
- **E:** F1 score for binary classification requires discrete positive/negative labels, not free-form generated text comparison.

---

## Q23 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** **AWS Step Functions** orchestrates multi-service workflows as a visual state machine, with native support for retries, error handling, wait states (including for human approval via a callback pattern), and long-running steps — the correct fit for stitching Glue, SageMaker, approval, and deployment steps together. See [`services/application-integration/step-functions.md`](../../../../services/application-integration/step-functions.md).

**Why the others are wrong:**
- **B:** CloudFront is a content delivery network, with no workflow-orchestration capability.
- **C:** Direct Connect is a dedicated network connection service, unrelated to orchestrating a multi-step ML workflow.
- **D:** Route 53 is a DNS service, unrelated to workflow orchestration.

---

## Q24 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A**

**Explanation:** **Multicollinearity** (near-redundant, highly correlated numeric features) causes unstable coefficient estimates in linear models; the standard fixes are dropping one of the redundant features or using **dimensionality reduction (e.g., PCA)** to combine correlated features into fewer, independent components.

**Why the others are wrong:**
- **B:** Oversampling addresses class imbalance in the target label, unrelated to feature-to-feature correlation.
- **C:** More epochs doesn't address a structural instability caused by redundant input features.
- **D:** One-hot encoding is for unordered categorical variables; applying it to already-numeric, highly-correlated features doesn't resolve multicollinearity.

---

## Q25 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** A **VPC interface endpoint (AWS PrivateLink)** for the SageMaker Runtime API lets a notebook instance in a private subnet with no NAT gateway invoke an endpoint entirely over the AWS private network, with no public internet path required. See [`services/networking-content-delivery/vpc-endpoints-privatelink.md`](../../../../services/networking-content-delivery/vpc-endpoints-privatelink.md).

**Why the others are wrong:**
- **B:** Putting the notebook in a public subnet with an internet gateway is the opposite of keeping traffic off the public internet.
- **C:** A public S3 bucket policy is unrelated to private API connectivity and would introduce an unrelated data exposure risk.
- **D:** Disabling TLS removes encryption-in-transit protection and has nothing to do with keeping traffic off the public internet path.

---

## Q26 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: A**

**Explanation:** **Cosine similarity** between embeddings measures how close two vectors point in the same direction, which corresponds to semantic closeness in meaning; a score of 0.91 indicates much stronger semantic alignment with the question than 0.42, so the engineer should weight or filter retrieved chunks using this score rather than treating all top-k results as equally relevant.

**Why the others are wrong:**
- **B:** Lower cosine similarity means *less* semantic alignment with the question, not more diversity of useful information — it's generally a weaker, less relevant match.
- **C:** Cosine similarity is specifically designed to proxy semantic relevance in embedding space; dismissing the relationship is incorrect and is the entire mechanism RAG retrieval relies on.
- **D:** Being in the top-k only means these were the closest matches found; their individual similarity scores still differ meaningfully and shouldn't be treated as uniformly relevant.

---

## Q27 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** Bedrock Knowledge Bases require an **ingestion (sync) job** to actually pick up new or changed documents from the S3 data source, chunk and embed them, and add them to the underlying vector store — simply uploading files to S3 does not automatically update the knowledge base until a sync runs (on-demand or scheduled). See [`services/machine-learning-ai/bedrock.md`](../../../../services/machine-learning-ai/bedrock.md).

**Why the others are wrong:**
- **B:** Uploading to S3 alone does not automatically propagate into the Knowledge Base's vector index; an ingestion job is required.
- **C:** Fine-tuning the entire foundation model is unnecessary, slow, and expensive compared to simply running a Knowledge Base sync — RAG's whole advantage is avoiding retraining when facts change.
- **D:** Temperature controls output randomness, not whether the knowledge base has indexed new documents.

---

## Q28 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: B**

**Explanation:** For data accessed rarely over years with retrieval times measured in minutes to hours being acceptable, **S3 Glacier Flexible Retrieval** (minutes to hours) or **Glacier Deep Archive** (lowest cost, longer retrieval) are the cost-minimizing choices for long-term compliance retention. See [`services/storage/s3-glacier.md`](../../../../services/storage/s3-glacier.md).

**Why the others are wrong:**
- **A:** S3 Standard is priced for frequent access and is far more expensive than necessary for data accessed a few times a year over 7 years.
- **C:** Standard-IA still costs more than Glacier tiers for data this infrequently accessed, and using it without any further lifecycle transition misses additional savings.
- **D:** EFS is a network file system for active workloads needing POSIX file access, not a cost-optimized long-term archival store for S3-resident training data.

---

## Q29 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** **Amazon GuardDuty** continuously analyzes VPC flow logs, DNS logs, and account activity against threat intelligence feeds to detect anomalies like connections to known-malicious IP ranges, exactly the automated threat-detection need described. See [`services/security-identity-compliance/guardduty.md`](../../../../services/security-identity-compliance/guardduty.md).

**Why the others are wrong:**
- **B:** Glue DataBrew is a visual data-prep tool, with no security threat-detection capability.
- **C:** QuickSight is a BI/visualization tool, unrelated to threat detection.
- **D:** CodeCommit is a source-control hosting service, unrelated to network threat detection.

---

## Q30 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: A**

**Explanation:** **RAG** reduces hallucination by grounding the model's generated answer in retrieved, current, factual source text (the actual return policy document) rather than having the model recall facts purely from frozen training-time parameters, which is the primary mechanism by which RAG improves factual accuracy. See [`embeddings-and-rag-data-prep.md`](../../domain-1-data-preparation/embeddings-and-rag-data-prep.md).

**Why the others are wrong:**
- **B:** Higher temperature increases output randomness/creativity, which would make hallucination risk worse, not better, for a factual question.
- **C:** A smaller context window reduces how much information the model can consider per call, which works against (not toward) grounding it in retrieved policy text.
- **D:** Model size alone doesn't fix hallucination caused by lacking access to current facts; even very large models hallucinate without grounding.

---

## Q31 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A and B**

**Explanation:** **Action groups** (Lambda/API-backed) give the agent concrete callable tools like 'check availability' and 'hold seat,' while **session state management** lets the agent retain conversational context (the flight discussed earlier) across turns so it can conditionally invoke the right action at the right time — both are core Bedrock Agents building blocks. See [`services/machine-learning-ai/bedrock.md`](../../../../services/machine-learning-ai/bedrock.md).

**Why the others are wrong:**
- **C:** Ground Truth is a labeling service, unrelated to agent action orchestration or conversational memory.
- **D:** Glue crawlers discover data schema; they have no role in agent tool invocation or conversation state.
- **E:** Route 53 routing policies manage DNS traffic routing, unrelated to conversational agent state or action groups.

---

## Q32 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A**

**Explanation:** A feature like 'days_until_cancellation' is only knowable *after* a customer has already decided to cancel — including it is a severe form of **data leakage** that would make the model look artificially accurate during training/validation while being useless at real prediction time, since that value doesn't exist yet for a customer who hasn't churned.

**Why the others are wrong:**
- **B:** This is a textbook leakage trap, not legitimate feature engineering — the feature cannot exist at the time a real prediction would need to be made.
- **C:** Class imbalance concerns the proportion of churn vs. non-churn labels, unrelated to a feature that encodes future outcome information.
- **D:** Dropout is a neural-network regularization technique for reducing overfitting; it does not address a feature that structurally leaks the label.

---

## Q33 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A and B**

**Explanation:** **Cost allocation tags** reviewed in Cost Explorer/Cost and Usage Reports give the team-by-team spending visibility needed, and committing to **Provisioned Throughput** (or a similar commitment option) for predictable high-volume Bedrock usage secures a better rate than pure On-Demand — together addressing both visibility and cost-optimization goals. See [`ml-cost-optimization.md`](../../domain-4-monitoring-security/ml-cost-optimization.md) and [`services/management-governance/cost-management-tools.md`](../../../../services/management-governance/cost-management-tools.md).

**Why the others are wrong:**
- **C:** Disabling CloudWatch metrics removes operational visibility and doesn't meaningfully reduce overall ML spend in a way relevant to the stated goals.
- **D:** Broad AdministratorAccess has nothing to do with cost visibility or securing a discounted usage rate, and is a security anti-pattern besides.
- **E:** Avoiding tagging would make the requested team/project cost breakdown impossible to produce.

---

## Q34 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A**

**Explanation:** **Structure-aware (semantic) chunking** that respects natural boundaries like sections/clauses keeps each chunk's embedding representing one coherent idea, which improves retrieval precision compared to blindly cutting at a fixed character count that can split a clause mid-sentence. See [`embeddings-and-rag-data-prep.md`](../../domain-1-data-preparation/embeddings-and-rag-data-prep.md).

**Why the others are wrong:**
- **B:** Extremely small, context-blind fixed chunks (50 characters) fragment meaning so badly that retrieved chunks are nearly useless without surrounding context.
- **C:** A single chunk covering an entire 100-page contract dilutes the embedding's specificity so much that similarity search can't distinguish which part of the contract is actually relevant.
- **D:** Randomly shuffling sentences destroys coherent meaning entirely and would make both chunking and retrieval nonsensical.

---

## Q35 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: A**

**Explanation:** The **elbow method** plots a clustering quality measure (like within-cluster sum of squares / inertia) across a range of k values; the 'elbow' point where adding more clusters stops meaningfully reducing inertia is a commonly used heuristic for choosing k in unsupervised k-means clustering.

**Why the others are wrong:**
- **B:** Precision/recall require labeled ground truth and defined positive/negative classes, which don't exist in unsupervised clustering.
- **C:** ROC-AUC is a supervised classification-ranking metric, not applicable to choosing k in unsupervised clustering.
- **D:** Cross-entropy loss is used in supervised classification training, not for selecting the number of clusters in k-means.

---

## Q36 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** **GPU-accelerated instances** dramatically speed up deep learning training (matrix-heavy parallel computation), while a small, CPU-friendly algorithm like **XGBoost** typically doesn't need or benefit from GPU acceleration at inference time, so standard CPU-based instances are the more cost-appropriate choice for that lightweight endpoint.

**Why the others are wrong:**
- **B:** Using GPU instances for the lightweight XGBoost endpoint wastes money paying for acceleration the workload doesn't need.
- **C:** Using only CPU instances for the deep learning training job would make training dramatically slower and often more expensive overall due to extended training time.
- **D:** Undersizing both workloads risks out-of-memory failures or unacceptably slow training/inference, regardless of cost savings intent.

---

## Q37 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** **AWS Config** records a timeline of resource configuration changes (before/after state), and **AWS CloudTrail** records exactly which API call (and which principal) made each change and when — together providing the full audit trail of configuration drift and who caused it. See [`services/management-governance/aws-config.md`](../../../../services/management-governance/aws-config.md) and [`services/management-governance/cloudtrail.md`](../../../../services/management-governance/cloudtrail.md).

**Why the others are wrong:**
- **B:** QuickSight visualizes data; it doesn't natively track resource configuration history or API-level change attribution.
- **C:** Deleting old versions would destroy the historical record needed for an audit, not produce one.
- **D:** Comprehend is an NLP text-analysis service, unrelated to configuration change tracking.

---

## Q38 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A**

**Explanation:** **Aurora PostgreSQL with the pgvector extension** adds vector similarity search capability directly inside the existing relational database the team already operates, avoiding the need to introduce and operate a brand-new dedicated vector database technology. See [`services/database/aurora.md`](../../../../services/database/aurora.md) and [`embeddings-and-rag-data-prep.md`](../../domain-1-data-preparation/embeddings-and-rag-data-prep.md).

**Why the others are wrong:**
- **B:** SQS is a message queue with no vector storage or similarity-search capability.
- **C:** The Glue Data Catalog stores table/schema metadata; it has no vector search capability.
- **D:** Route 53 is a DNS service, entirely unrelated to vector storage.

---

## Q39 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: A**

**Explanation:** Running many configurations and cherry-picking the best validation score effectively 'overfits' to the validation set itself (the winning model was selected partly because it got lucky on that specific set), inflating the reported number; the standard remedy is a separate, untouched **test set** used only once, for the final unbiased performance estimate.

**Why the others are wrong:**
- **B:** This directly contradicts a well-known pitfall (hyperparameter search overfitting to the validation set); the reported score is optimistically biased.
- **C:** Changing the learning rate on the winning configuration doesn't address the statistical bias introduced by selection-over-many-trials.
- **D:** The validation set should still be used during tuning; the fix is adding a held-out test set for the final estimate, not removing validation entirely.

---

## Q40 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** **Application Auto Scaling** for SageMaker endpoints supports target-tracking policies on metrics like `SageMakerVariantInvocationsPerInstance`, automatically adding or removing instances to keep that metric near the target — exactly the automated scale-up/scale-down behavior described. See [`services/machine-learning-ai/sagemaker-deployment-endpoints.md`](../../../../services/machine-learning-ai/sagemaker-deployment-endpoints.md).

**Why the others are wrong:**
- **B:** A fixed instance count can't adapt to changing demand, risking either overprovisioning (wasted cost) or underprovisioning (SLA violations).
- **C:** Manual resizing is slow, error-prone, and explicitly the opposite of the 'without manual intervention' requirement.
- **D:** Ground Truth active learning is a labeling-workflow feature, unrelated to endpoint capacity scaling.

---

## Q41 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** A **pre-training Clarify bias report** examines the *data itself*, before any model exists, so a flagged correlation between zip code (a protected-attribute proxy) and the label indicates the model could learn an unfair shortcut if trained as-is; the correct response is to investigate and apply data-level mitigations before training, not after. See [`responsible-ai-and-guardrails.md`](../../domain-4-monitoring-security/responsible-ai-and-guardrails.md).

**Why the others are wrong:**
- **B:** Pre-training metrics are specifically valuable because they catch bias risk *before* any model is trained, which is cheaper and earlier to fix than discovering it post-training.
- **C:** No model has been trained yet at this stage — this metric describes a property of the raw data, not of a trained model's behavior.
- **D:** This is a bias/fairness signal (a sensitive-attribute proxy correlated with the label), not a label-leakage problem (a feature containing the literal outcome information).

---

## Q42 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A and B**

**Explanation:** This is **multi-class imbalance**, an extension of the binary case to many categories; the same core remedies apply — **class weighting** and **targeted oversampling** of rare classes (with merging extremely rare categories as a judgment call) — to keep the model from collapsing onto the dominant 3 categories.

**Why the others are wrong:**
- **C:** An 85%/15% split across 3 vs. 27 categories, with several classes under 20 examples, is a significant imbalance that will likely hurt minority-class performance if untreated.
- **D:** Learning rate is a training hyperparameter unrelated to fixing a skewed class distribution.
- **E:** Overall accuracy on a heavily imbalanced multi-class dataset can look high while completely failing the rare categories — it should be paired with per-class metrics, not used alone.

---

## Q43 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: A**

**Explanation:** **SageMaker Autopilot** automates exploring multiple algorithms and hyperparameter configurations on a tabular dataset, performing automatic feature engineering and producing a ranked leaderboard of candidate models with full visibility into generated training code — the AutoML capability described.

**Why the others are wrong:**
- **B:** Ground Truth is a data-labeling service, unrelated to automated model/algorithm search.
- **C:** Glue DataBrew is a visual data-cleaning tool, not an AutoML model-search capability.
- **D:** Comprehend custom classification is a managed NLP classification feature for text, not a general tabular AutoML leaderboard tool.

---

## Q44 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** A properly configured canary/linear deployment with **CloudWatch alarm-based automatic rollback** detects the error-rate spike early (while exposure is still limited to a small traffic percentage) and rolls back to the known-good previous version, which is exactly the safety benefit of a gradual rollout strategy instead of an all-at-once cutover.

**Why the others are wrong:**
- **B:** Shifting to 100% traffic while the new version is already showing elevated errors would expose all users to the problem instead of limiting the blast radius.
- **C:** Ignoring a real error-rate spike risks the problem worsening as more traffic shifts to the new version over time.
- **D:** Deleting the endpoint entirely causes a complete outage, which is a far more disruptive response than simply rolling back to the previous known-good version.

---

## Q45 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A**

**Explanation:** **Data augmentation** (rotations, flips, crops, color jitter) synthetically expands the effective diversity of a small image dataset without needing new photos, which commonly improves a vision model's ability to generalize for scarce categories like rare manufacturing defects.

**Why the others are wrong:**
- **B:** Deleting half the already-scarce data makes the scarcity problem worse, not better.
- **C:** Reducing to 8x8 grayscale destroys the visual detail needed to detect subtle manufacturing defects.
- **D:** Re-labeling the defect images as the majority class would erase the minority class entirely, defeating the purpose of training a defect detector.

---

## Q46 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** **Amazon Augmented AI (A2I)** is built specifically to route low-confidence or sensitive model outputs (including Bedrock-generated content decisions) to human reviewers for confirmation before a final action, which is exactly the human-in-the-loop gate the content-moderation workflow needs.

**Why the others are wrong:**
- **B:** AWS Config tracks resource configuration compliance, unrelated to routing content decisions for human review.
- **C:** Route 53 is a DNS service, with no human-review workflow capability.
- **D:** Direct Connect is a dedicated network link, unrelated to human-in-the-loop review.

---

## Q47 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: A**

**Explanation:** A **local SHAP explanation** attributes contribution values to each feature for one specific prediction (this applicant), which is different from a **global** feature-importance ranking that summarizes average influence across the entire dataset — local explanations are what regulators asking about one specific denied applicant actually need.

**Why the others are wrong:**
- **B:** A global explanation would report average importance across all applicants, not per-feature contributions for one specific individual's decision.
- **C:** A confusion matrix tabulates true/false positive/negative counts across a dataset; it isn't a per-prediction feature-contribution explanation.
- **D:** A precision-recall curve summarizes classifier performance across thresholds; it has no per-feature attribution content.

---

## Q48 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** **SageMaker Model Registry** organizes related model versions into **model package groups** (e.g., all 'fraud-v2' versions together), tracks lineage and metadata, and supports an approval-status gate that controls promotion between environments. See [`services/machine-learning-ai/sagemaker-model-monitor-and-registry.md`](../../../../services/machine-learning-ai/sagemaker-model-monitor-and-registry.md).

**Why the others are wrong:**
- **B:** Plain S3 folders provide no structured versioning, lineage tracking, or approval-gate semantics on their own.
- **C:** The Glue Data Catalog stores data table schema metadata, not model version/package group organization.
- **D:** CloudFront is a content delivery network, with no role in model version governance.

---

## Q49 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A**

**Explanation:** SageMaker Feature Store's **Offline Store** retains historical feature records with timestamps, supporting **point-in-time ('time travel') queries** that reconstruct exactly what feature values existed at a given training time — the basis for reproducible lineage and audit. See [`services/machine-learning-ai/sagemaker-data-wrangler-and-feature-store.md`](../../../../services/machine-learning-ai/sagemaker-data-wrangler-and-feature-store.md).

**Why the others are wrong:**
- **B:** Deleting old feature values destroys the exact history needed for lineage reconstruction — the opposite of what's required.
- **C:** Ground Truth is a labeling service with no feature-history/versioning capability.
- **D:** CloudFront is a content delivery cache, unrelated to feature value lineage tracking.

---

## Q50 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** **TLS/HTTPS (encryption in transit)** is what prevents a network eavesdropper from reading request/response payloads as they travel between the client and the SageMaker endpoint; AWS SageMaker Runtime API calls are made over HTTPS, and this must not be downgraded or bypassed for sensitive payloads like patient data.

**Why the others are wrong:**
- **B:** Encryption at rest protects stored artifacts, but plaintext HTTP in transit would still let an eavesdropper read live request/response payloads over the network — a distinct protection.
- **C:** IAM controls *who* is authorized to call the API; it doesn't protect data as it travels across the network from interception.
- **D:** Disabling logging doesn't protect data in transit at all, and removing logs can actually hurt auditability without solving the stated eavesdropping risk.

---

## Q51 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: A**

**Explanation:** When individual models make somewhat **uncorrelated errors**, averaging their predictions tends to cancel out individual variance/noise while preserving the shared signal, which is the core statistical reason **ensembling** often outperforms any single constituent model.

**Why the others are wrong:**
- **B:** Ensembling multiple models typically increases total compute/training time (you must train several models), not decrease it.
- **C:** A validation set is still needed to tune and evaluate the ensemble itself; ensembling doesn't remove this requirement.
- **D:** Ensembling reduces variance from averaging diverse models but does not guarantee zero bias — a systematic bias shared across all constituent models would still persist.

---

## Q52 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** **Multi-Region deployment** (endpoints running in multiple Regions close to each user population, with routing/failover logic) reduces latency for geographically distributed users and provides resilience if one Region experiences an outage — the standard pattern for global low-latency, DR-resilient inference.

**Why the others are wrong:**
- **B:** A single-Region deployment accepts exactly the latency and single-point-of-failure risk the requirement is trying to avoid.
- **C:** Batch Transform is for offline, non-interactive scoring; it doesn't serve low-latency real-time requests for global users at all.
- **D:** Outposts extends AWS infrastructure on-premises, which doesn't by itself solve multi-continent public-user latency or Region-level DR the way a multi-Region cloud deployment does.

---

## Q53 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A**

**Explanation:** Augmentation choices should respect which transformations are 'label-preserving' for the problem: since orientation is genuinely arbitrary here, rotation/flip augmentation is safe and helpful, but since color intensity carries real predictive signal (vegetation health), aggressive color distortion risks destroying that meaningful information.

**Why the others are wrong:**
- **B:** Unrestricted aggressive color inversion would corrupt the very signal (color-based vegetation health) the model needs to learn from, given the scenario's stated meaning of color.
- **C:** Applying no augmentation at all forgoes a free, well-understood way to improve generalization for the orientation-invariant parts of this problem.
- **D:** Augmentation is applied to training data to improve the model's learned generalization; augmenting only the test set would distort evaluation rather than help training.

---

## Q54 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** **AWS Budgets** supports forecasted-spend alerts that notify (via SNS, which can fan out to email/Slack integrations) when projected spend is on track to exceed a defined threshold before the billing period ends, directly matching the proactive cost-alerting need. See [`services/management-governance/cost-management-tools.md`](../../../../services/management-governance/cost-management-tools.md).

**Why the others are wrong:**
- **B:** Model Monitor tracks data/model quality drift, not billing/cost forecasts.
- **C:** Glue DataBrew is a data-prep tool, unrelated to cost budgeting/alerting.
- **D:** Comprehend is an NLP text-analysis service, unrelated to cost monitoring.

---

## Q55 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: A**

**Explanation:** Embedding model choice should prioritize **retrieval quality for the target domain**, and critically, the **same embedding model** must be used consistently to embed both the documents and the incoming queries — mixing embedding models breaks the geometric consistency that similarity search depends on. See [`embeddings-and-rag-data-prep.md`](../../domain-1-data-preparation/embeddings-and-rag-data-prep.md).

**Why the others are wrong:**
- **B:** Higher dimensionality alone doesn't guarantee better retrieval quality and increases storage/compute cost; it's not the primary selection criterion.
- **C:** Using a different embedding model for documents than for queries breaks similarity search, since the two sets of vectors would exist in geometrically inconsistent spaces.
- **D:** Ignoring retrieval accuracy entirely in favor of lowest cost risks a RAG system that retrieves irrelevant context, undermining the entire point of the system.

---

## Q56 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** **On-Demand Bedrock invocation** charges per token processed with zero infrastructure to provision or manage, which fits highly variable, unpredictable traffic far better than a capacity commitment, matching the startup's stated need to avoid provisioning anything.

**Why the others are wrong:**
- **B:** Provisioned Throughput requires committing to a fixed capacity level for a term, which is cost-inefficient for traffic that is near-zero for long stretches and spikes unpredictably.
- **C:** Running a dedicated 24/7 endpoint for the foundation model reintroduces the provisioning/management burden and idle cost the team explicitly wants to avoid, and isn't how Bedrock's own hosted models are typically consumed.
- **D:** Reserved EC2 Instances are a compute commitment unrelated to Bedrock's managed, serverless foundation model invocation billing model.

---

## Q57 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A**

**Explanation:** **Stratified k-fold cross-validation** ensures every fold preserves approximately the same class ratio as the full dataset, which is especially important on a small, imbalanced dataset where a plain random fold could, by chance, end up with very few or zero minority-class examples in some folds.

**Why the others are wrong:**
- **B:** Plain unstratified k-fold can produce folds with wildly different class ratios by chance, especially on a small, imbalanced dataset, making per-fold metrics unreliable.
- **C:** Leave-one-out without class-ratio attention doesn't specifically solve the stratification need, and is also computationally expensive for not much benefit here.
- **D:** A single train/test split gives only one performance estimate with higher variance, and still doesn't guarantee a representative split of the minority class on its own.

---

## Q58 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** Running Model Monitor on a **recurring schedule** means data-quality/drift issues that emerge *after* initial deployment — as live traffic evolves over weeks or months — are continuously caught, instead of only validating the model's behavior once at launch and then flying blind. See [`services/machine-learning-ai/sagemaker-model-monitor-and-registry.md`](../../../../services/machine-learning-ai/sagemaker-model-monitor-and-registry.md).

**Why the others are wrong:**
- **B:** Scheduled monitoring works together with CloudWatch alarms (which fire on the monitor's violation metrics); it doesn't eliminate the need for alarms.
- **C:** Monitoring detects when something has gone wrong; it doesn't replace the retraining process itself, which is still a separate necessary step once drift is detected.
- **D:** Scheduled monitoring increases the chance of catching problems needing a redeploy/retrain — it doesn't guarantee the model will never need one.

---

## Q59 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: A and B**

**Explanation:** **Catastrophic forgetting** describes a fine-tuned model losing previously learned general capabilities while gaining a new narrow skill. **Parameter-efficient fine-tuning (LoRA/PEFT)**, which updates only a small added set of parameters rather than the full model, and **mixing general-purpose examples** into the fine-tuning data are both standard, complementary mitigations that preserve more of the original behavior.

**Why the others are wrong:**
- **C:** Removing the validation set eliminates the ability to detect overfitting/forgetting during fine-tuning; it doesn't mitigate forgetting itself.
- **D:** SMOTE addresses class imbalance in classification datasets; it has no relevance to a foundation model losing general conversational ability after fine-tuning.
- **E:** Model Monitor detects post-deployment data/model drift in classic ML; it doesn't mitigate forgetting during a fine-tuning run.

---

## Q60 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** **Cold start** latency occurs when a serverless endpoint must spin up a fresh execution environment after a period with no traffic; it's an inherent, well-understood trade-off of Serverless Inference's pay-only-for-what-you-use model, and is an acceptable cost for a workload tolerant of occasional added latency. See [`services/machine-learning-ai/sagemaker-deployment-endpoints.md`](../../../../services/machine-learning-ai/sagemaker-deployment-endpoints.md).

**Why the others are wrong:**
- **B:** Elevated first-request latency after idling is expected serverless behavior, not an indication of a broken model.
- **C:** Data drift is a statistical input-distribution shift issue, unrelated to the infrastructure cold-start latency pattern described.
- **D:** IAM permission problems would typically cause outright authorization failures/errors, not a latency pattern specifically tied to post-idle requests.

---

## Q61 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A**

**Explanation:** **SSE-KMS with a customer-managed key (CMK)** lets the company control the key's policy and **disable or revoke the key** at any time, immediately blocking all future decryption of data encrypted under it — a centralized kill switch SSE-S3 (AWS-owned keys) cannot offer since the company has no control over those keys.

**Why the others are wrong:**
- **B:** SSE-S3 uses AWS-owned keys that the customer cannot view, control, or disable, so there's no way to centrally revoke access on demand.
- **C:** Relying only on IAM/bucket policies without encryption at rest fails the explicit encryption requirement and offers no cryptographic revocation capability.
- **D:** A hard-coded key in application code is a serious security anti-pattern with no centralized revocation mechanism and high leak risk.

---

## Q62 — Domain 4 (Operating, Monitoring, and Securing ML Solutions)

**Correct Answer: A**

**Explanation:** **AWS Security Hub** aggregates, normalizes, and prioritizes security findings from GuardDuty, Macie, Config, Inspector, and other services into one centralized dashboard across accounts/regions, exactly matching the centralized-view requirement. See [`services/security-identity-compliance/security-hub-and-inspector.md`](../../../../services/security-identity-compliance/security-hub-and-inspector.md).

**Why the others are wrong:**
- **B:** QuickSight is a general BI/visualization tool; it has no built-in security-findings aggregation across GuardDuty/Macie/Config.
- **C:** Direct Connect is a dedicated network connection service, unrelated to security finding aggregation.
- **D:** Route 53 is a DNS service, unrelated to security finding aggregation.

---

## Q63 — Domain 2 (ML Model and Foundation Model Development)

**Correct Answer: A**

**Explanation:** When the correct sequence of actions genuinely depends on intermediate results and can't be fully fixed in advance, the right design is an **agent-based architecture**: the model reasons iteratively, selects which action/tool to invoke next based on what it has learned so far, and can branch dynamically — fundamentally different from a rigid, pre-defined linear prompt chain that assumes a fixed sequence.

**Why the others are wrong:**
- **B:** A single one-shot prompt with no tool access cannot actually look up live order/inventory data or take real actions; it can only generate text describing what it imagines happened.
- **C:** A numeric regression score doesn't provide the dynamic, multi-step tool orchestration and decision logic the scenario requires.
- **D:** K-means clustering is an unsupervised grouping technique with no mechanism for sequential decision-making or tool invocation.

---

## Q64 — Domain 3 (Deployment and Orchestration of ML Workflows)

**Correct Answer: A**

**Explanation:** SageMaker endpoint deployment guardrails offer **All-at-once** (instant full cutover), **Linear** (traffic shifted in equal increments over set intervals), and **Canary** (a small fixed percentage first, then the remainder after a bake-time with no alarms triggered) — each trading off rollout speed against risk exposure, with CloudWatch alarms able to trigger automatic rollback during Linear or Canary shifts.

**Why the others are wrong:**
- **B:** Batch Transform, Serverless Inference, and Asynchronous Inference are inference *invocation* patterns, not traffic-shifting deployment strategies for rolling out a new model version.
- **C:** These are endpoint deployment configuration options, not IAM policy types.
- **D:** These are deployment-time traffic-shifting strategies for an endpoint, unrelated to SageMaker Pipelines step types.

---

## Q65 — Domain 1 (Data Preparation for ML and AI)

**Correct Answer: A**

**Explanation:** When missingness itself carries signal (no prior purchase), it's best preserved via a **missing-value indicator flag** plus a reasonable imputed value, rather than erased; when missingness is rare and essentially random (data-entry typos), simple **mode imputation or dropping the few affected rows** is adequate since there's no meaningful pattern to preserve.

**Why the others are wrong:**
- **B:** Dropping every row with any missing value would discard 12% of the dataset for a column where the missingness itself is informative, losing both data and signal unnecessarily.
- **C:** Blindly zero-filling 'last_purchase_amount' conflates 'no prior purchase' with 'spent $0,' destroying the meaningful distinction, and ignores that the two columns have very different missingness causes.
- **D:** Deleting the columns entirely discards predictive signal (especially the meaningful missingness pattern in purchase amount) that could help the model.

---
