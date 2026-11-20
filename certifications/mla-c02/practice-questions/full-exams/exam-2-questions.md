# MLA-C02 Full Mock Exam 2 — Questions

65 questions mixing all four MLA-C02 domains in one sitting, matching the real exam's associate-level format (multiple choice and multiple response only). See [`index.md`](index.md) for instructions and scoring. Do not peek at [`exam-2-answer-key.md`](exam-2-answer-key.md) until you have answered every question.

---

## Q1

A logistics company streams GPS location pings from 50,000 delivery vehicles and wants the pings durably delivered into S3 as compressed Parquet files every 5 minutes, without writing or operating any custom consumer code. Which service fits best?

A) Amazon Kinesis Data Firehose with a Parquet conversion configuration and a 5-minute buffering hint
B) Amazon Kinesis Data Streams with a self-managed EC2 consumer fleet
C) AWS Glue Crawler run manually every 5 minutes
D) Amazon SNS with email notifications per ping

---

## Q2

A data scientist runs 5-fold cross-validation on a dataset and gets accuracy scores of 91%, 62%, 88%, 90%, 89% across the five folds — one fold is a dramatic outlier. What does this most likely indicate, and what should be investigated first?

A) The model is simply unlucky; no further investigation is needed
B) That particular fold's split may contain a data quality issue, an unrepresentative subset, or leakage inconsistency; inspect that fold's data before trusting the aggregate CV score
C) The learning rate must be doubled
D) The dataset needs more training epochs across all folds

---

## Q3

A retailer needs to score its entire 10-million-row product catalog for predicted demand once every night, with results consumed downstream the next morning. No synchronous request/response pattern is needed. Which SageMaker inference option is the right fit?

A) SageMaker Batch Transform run on a nightly schedule
B) A real-time endpoint kept running 24/7
C) SageMaker Asynchronous Inference invoked once per row
D) SageMaker Serverless Inference with a provisioned concurrency setting

---

## Q4

A team needs to search recent SageMaker endpoint inference logs in CloudWatch Logs for a specific pattern of error messages across the last 6 hours, using an interactive query language rather than downloading and grepping raw log files. Which service fits?

A) CloudWatch Logs Insights
B) AWS Glue Data Catalog
C) Amazon Macie
D) AWS Direct Connect

---

## Q5

A data engineer needs to write a complex Spark transformation job with custom Python/Scala logic, heavy joins, and conditional branching logic that a visual, no-code tool cannot express, over data in S3. Which AWS service is the right fit?

A) AWS Glue ETL jobs (Spark script mode)
B) Amazon QuickSight calculated fields
C) SageMaker Data Wrangler's drag-and-drop transforms only
D) Amazon CloudWatch Logs Insights queries

---

## Q6

A team compares Gradient Boosting (e.g., XGBoost) and Random Forest on the same tabular dataset. Random Forest trains multiple decision trees independently on bootstrapped samples and averages their predictions, while Gradient Boosting trains trees sequentially, each correcting the errors of the previous ones. What is a key practical trade-off between the two?

A) Random Forest trees train independently and parallelize easily, often with less hyperparameter sensitivity; Gradient Boosting trains sequentially (harder to parallelize per-tree) but often achieves higher accuracy with careful tuning
B) There is no meaningful difference between the two approaches
C) Random Forest can only be used for regression, never classification
D) Gradient Boosting cannot overfit under any configuration

---

## Q7

A fraud-scoring pipeline needs raw transaction data to pass through a custom preprocessing step, then a trained XGBoost model, then a custom postprocessing step that converts the raw score into a business-friendly risk category — all as one deployed inference unit with minimal latency overhead between steps. Which SageMaker capability fits?

A) A SageMaker Inference Pipeline chaining multiple containers (preprocessing, model, postprocessing) behind one endpoint
B) Three entirely separate endpoints the client must call in sequence over the network
C) SageMaker Ground Truth
D) AWS Glue DataBrew

---

## Q8

(Choose TWO) A team wants a fully automated retraining pipeline that kicks off whenever SageMaker Model Monitor detects data drift exceeding a defined threshold, with no manual trigger required. Which TWO services/features should be combined to build this?

A) A CloudWatch Alarm configured against the Model Monitor drift metric, breaching when the threshold is exceeded
B) Amazon EventBridge (or the alarm's action) triggering a Lambda function or Step Functions execution that starts the retraining SageMaker Pipelines run
C) Amazon QuickSight dashboards as the automated trigger
D) AWS Direct Connect
E) Amazon Route 53 health checks

---

## Q9

A training dataset of customer orders contains thousands of exact duplicate rows caused by a retry bug in the upstream order system, artificially inflating certain patterns the model is learning. What data preparation step should be applied first?

A) Deduplicate the dataset by identifying and removing exact (or near-exact) duplicate records before training
B) Apply SMOTE oversampling to the minority class
C) Increase the model's regularization strength
D) Switch to a different training algorithm

---

## Q10

During training, the loss suddenly spikes to NaN (not a number) after several stable epochs, and the model's weights become unusable. What is the most likely cause and immediate fix?

A) The learning rate is too high, causing unstable/divergent weight updates; reduce the learning rate and/or add gradient clipping
B) The validation set is too small
C) The model needs more layers
D) The batch size is too small and should be reduced further

---

## Q11

A company's SageMaker real-time endpoint for a deep learning model runs steadily and predictably 24/7 for the next 3 years, with well-understood compute needs. Which purchasing approach minimizes cost for this workload?

A) A SageMaker Savings Plan committing to a consistent usage level for a 1- or 3-year term
B) On-Demand pricing with no commitment
C) SageMaker Serverless Inference
D) Running the workload exclusively on Spot Instances

---

## Q12

A customer-facing GenAI assistant must avoid generating responses that contradict or go beyond the specific grounding documents provided to it, flagging or blocking answers that appear to be ungrounded speculation. Which Bedrock Guardrails capability addresses this specific concern, distinct from simple denied-topic filtering?

A) Contextual grounding checks, which evaluate whether a response is sufficiently supported by the provided source/reference content
B) Word filters that block a static list of profanity
C) Increasing the model's context window size
D) SageMaker Ground Truth labeling

---

## Q13

A continuous 'customer age' feature ranging from 18 to 95 shows a noisy, non-linear relationship with loan default risk that a linear model struggles to capture directly. The team wants a simple data preparation step to help a linear model capture non-linear age effects. What should they do?

A) Bin the continuous age feature into discrete ranges (e.g., 18-25, 26-35, ...) and one-hot encode the bins
B) Remove the age feature entirely
C) Convert age to a boolean (over 50 / under 50) and discard all other information
D) Leave age as a raw continuous feature with no transformation

---

## Q14

A fraud classifier trained with a standard cross-entropy loss on a 99.5%/0.5% imbalanced dataset still performs poorly on the rare fraud class even after oversampling. The team wants the loss function itself to down-weight easy, well-classified majority examples and focus learning on hard, misclassified minority examples. What should they consider?

A) Switching to focal loss, which reduces the loss contribution of easily classified examples and emphasizes hard-to-classify ones
B) Switching to mean squared error for a classification problem
C) Increasing the test set size
D) Reducing the number of features

---

## Q15

A team wants to test a new model version by routing a copy of live production traffic to it and comparing its predictions against the current production model's predictions, without the new model's output ever being returned to real users, to assess risk-free real-world performance. What is this deployment pattern called?

A) Shadow deployment/shadow testing
B) Blue/green deployment with full cutover
C) Batch Transform scoring
D) Canary deployment with user-facing traffic

---

## Q16

A company wants strict separation of duties: data scientists should be able to experiment freely in a sandbox SageMaker environment, but only a separate MLOps/release role should be able to approve and deploy models into the production endpoint. What IAM approach achieves this?

A) Define distinct IAM roles (e.g., a data-scientist role scoped to sandbox resources, and a separate deployment role with permissions to approve registry entries and update production endpoints) following least privilege and separation of duties
B) Give every team member the same broad IAM role with full SageMaker and production access
C) Remove IAM entirely and rely on network firewalls only
D) Grant AdministratorAccess to all data scientists for convenience

---

## Q17

Using SageMaker Data Wrangler's Quick Model feature on a prepared dataset, a data scientist gets an estimated feature importance ranking before committing to a full training job. What is the primary purpose of this capability?

A) To quickly validate that the current set of engineered features has meaningful predictive signal and to spot clearly unhelpful features before investing in full training
B) To replace the need for any further model training entirely
C) To encrypt the dataset automatically
D) To deploy the dataset as a production inference endpoint

---

## Q18

A team training a large deep learning model finds a single GPU's memory cannot hold the full model, so they split different layers of the model across multiple GPUs, each GPU computing a different part of the forward/backward pass. What is this technique called?

A) Model parallelism
B) Data parallelism
C) K-fold cross-validation
D) Transfer learning

---

## Q19

A team wants an automated MLOps pipeline where a code commit to a model-training repository triggers a build, test, then a SageMaker Pipelines execution, followed by approval gates before production deployment — all using CI/CD tooling they already use for software. Which combination of services fits?

A) AWS CodePipeline and AWS CodeBuild orchestrating the CI/CD stages, invoking a SageMaker Pipelines execution as part of the workflow (e.g., via SageMaker Projects)
B) Amazon QuickSight dashboards triggering deployments
C) Manually running scripts from a developer's laptop on every commit
D) Amazon Route 53 health checks as the CI/CD trigger

---

## Q20

A company in AWS Account A trains models and stores encrypted artifacts in S3 using a KMS customer-managed key. A separate deployment pipeline in AWS Account B needs to read and decrypt those artifacts to deploy them. What must be configured to allow this cross-account access securely?

A) Update the KMS key policy in Account A to grant Account B's IAM role `kms:Decrypt` permission (and the S3 bucket policy to allow the cross-account read), rather than making the key or bucket public
B) Make the S3 bucket and KMS key fully public so any account can access them
C) Disable encryption on the artifacts so no cross-account key permissions are needed
D) Copy the KMS key's private material into Account B manually

---

## Q21

A SageMaker Ground Truth labeling job for text classification is configured so that once the automated labeling model reaches high enough confidence on a given example, it labels that example automatically, sending only lower-confidence examples to human labelers. What is this capability called, and why does it help?

A) Active learning, which reduces total human labeling cost and time by automating the 'easy' majority of examples
B) Data drift, which has nothing to do with labeling cost
C) Regularization, which prevents overfitting during labeling
D) Batch Transform, which runs inference on unlabeled data only

---

## Q22

(Choose TWO) A team needs automatic metrics to score GenAI-generated text (summaries and translations) against human-written reference text, based on n-gram overlap. Which TWO are standard, widely-used metrics for this?

A) ROUGE (Recall-Oriented Understudy for Gisting Evaluation) — recall-oriented overlap, common for summarization
B) BLEU (Bilingual Evaluation Understudy) — precision-oriented overlap with a brevity penalty, common for translation
C) RMSE
D) AUC-ROC
E) F1 score for binary classification

---

## Q23

A team wants to orchestrate a workflow spanning a Glue ETL job, then a SageMaker training job, then a human-approval wait state, then conditional deployment — all with visual state tracking, built-in retry/error handling, and support for steps that can run for hours. Which service is purpose-built for this cross-service orchestration?

A) AWS Step Functions
B) Amazon CloudFront
C) AWS Direct Connect
D) Amazon Route 53

---

## Q24

A tabular dataset has two highly correlated features ('total_revenue' and 'total_revenue_minus_tax') that are nearly redundant and are causing unstable coefficient estimates in a linear regression model (multicollinearity). What data preparation technique directly addresses this?

A) Remove one of the redundant correlated features, or apply dimensionality reduction (e.g., PCA) to combine correlated features
B) Apply more aggressive oversampling of the minority class
C) Increase the number of training epochs
D) Convert both features to one-hot encoded categories

---

## Q25

A security-conscious ML team wants all traffic between a SageMaker notebook instance and the SageMaker Runtime API (for invoking an endpoint) to stay off the public internet entirely, while the notebook runs inside a private VPC subnet with no NAT gateway. What should they configure?

A) A VPC interface endpoint (AWS PrivateLink) for the SageMaker Runtime API
B) A public subnet with an internet gateway for the notebook instance
C) An S3 bucket policy allowing public read access
D) Disabling TLS on the endpoint for simplicity

---

## Q26

A RAG system embeds a user's question and retrieves the top-k document chunks whose embeddings are closest to the question's embedding using cosine similarity. One retrieved chunk has a cosine similarity of 0.91 to the question, another has 0.42. What does this comparison tell the engineer?

A) The chunk with similarity 0.91 is semantically much closer to the question's meaning than the chunk at 0.42, and is far more likely to be relevant context for the model to use
B) The chunk with similarity 0.42 should always be preferred because lower scores indicate more diverse information
C) Cosine similarity scores have no relationship to semantic relevance
D) Both chunks are equally relevant because both were retrieved in the top-k

---

## Q27

A company sets up a Bedrock Knowledge Base backed by documents in S3. After the team uploads 500 new documents to the S3 bucket, the chatbot's answers still don't reflect the new content. What is most likely missing, and what should they do?

A) They need to trigger (or schedule) a Knowledge Base ingestion/sync job so the new S3 documents are chunked, embedded, and added to the vector store
B) Nothing; new documents in S3 are automatically reflected instantly with no sync step
C) They should instead fine-tune the entire foundation model on the new documents
D) They should increase the foundation model's temperature setting

---

## Q28

A company must retain 7 years of raw historical training data for compliance, but needs it accessible within minutes only a few times a year, if ever, and wants to minimize storage cost over that long retention period. Which S3 storage class fits?

A) S3 Standard
B) S3 Glacier Flexible Retrieval or Glacier Deep Archive, depending on exactly how rarely and how fast access must be
C) S3 Standard-Infrequent Access used identically to S3 Standard with no lifecycle policy
D) Amazon EFS

---

## Q29

A security team wants continuous, automated detection of anomalous behavior across the AWS accounts hosting ML infrastructure — such as an EC2 training instance suddenly making outbound connections associated with known malicious IP ranges. Which service should be enabled?

A) Amazon GuardDuty
B) AWS Glue DataBrew
C) Amazon QuickSight
D) AWS CodeCommit

---

## Q30

A customer-support chatbot built on a raw foundation model frequently 'hallucinates' confident-sounding but factually wrong answers about the company's current return policy. Which architectural change most directly reduces this specific failure mode?

A) Ground the model's answers in retrieved, current policy documents via RAG, so it generates from actual retrieved text instead of relying on frozen training-time knowledge
B) Increase the model's temperature setting to make answers more varied
C) Decrease the context window size
D) Switch to a smaller foundation model with fewer parameters

---

## Q31

A Bedrock Agent for a travel-booking assistant must, across a multi-turn conversation, call a 'check flight availability' action, then conditionally call a 'hold seat' action only if the user confirms, maintaining context about which flight was discussed earlier in the conversation. Which TWO Bedrock Agent concepts are directly responsible for this behavior?

A) Action groups backed by Lambda functions/APIs, which define the callable actions (check availability, hold seat) the agent can invoke
B) Session/conversation state management, which lets the agent retain context (the previously discussed flight) across multiple turns
C) SageMaker Ground Truth labeling jobs
D) AWS Glue crawlers
E) Amazon Route 53 routing policies

---

## Q32

A feature engineering pipeline accidentally includes a column called 'days_until_cancellation' when training a churn-prediction model meant to predict churn *before* it happens. What problem does this illustrate, and what should be done?

A) This is data leakage — the feature directly encodes information that would only be known after the outcome occurs, and it must be removed
B) This is normal feature engineering and should be kept as-is
C) This is class imbalance and should be fixed with SMOTE
D) This is overfitting and should be fixed with dropout

---

## Q33

(Choose TWO) A finance team wants to understand and control ML-related AWS spending: they need to see cost broken down by team/project tag, and they want a discounted rate for Bedrock usage they can predict and commit to in advance. Which TWO approaches should they use?

A) Apply consistent cost allocation tags (e.g., team, project) to ML resources and review them in AWS Cost Explorer / Cost and Usage Reports
B) Purchase Bedrock Provisioned Throughput (or an equivalent commitment-based option) for predictable, high-volume usage to get a better rate than On-Demand
C) Disable all CloudWatch metrics to reduce monitoring costs
D) Grant every team AdministratorAccess so they can self-manage costs
E) Avoid tagging resources to simplify account structure

---

## Q34

A RAG system over legal contracts needs to choose a chunking strategy. Contracts have clearly defined sections and clauses. Which chunking approach is most likely to preserve retrieval quality compared to a fixed-size, context-blind chunk split?

A) Semantic/structure-aware chunking that splits along natural section/clause boundaries rather than a fixed character count
B) Splitting every document into exactly 50-character chunks regardless of content
C) Embedding the entire 100-page contract as a single chunk
D) Randomly shuffling sentences before chunking

---

## Q35

A team running k-means clustering on customer behavior data needs to choose the number of clusters, k, without labeled ground truth. Which technique is commonly used to pick a reasonable k?

A) The elbow method, plotting within-cluster variance (inertia) against different values of k and choosing the point where the improvement rate sharply diminishes
B) Precision and recall curves
C) ROC-AUC analysis
D) Cross-entropy loss minimization

---

## Q36

A team training a large deep learning model needs GPU instances, while a separate lightweight real-time endpoint serving a small XGBoost model only needs CPU. What is the most cost-appropriate instance family choice for each workload?

A) GPU-accelerated instances (e.g., P-family) for the deep learning training job; CPU-based instances (e.g., M/C-family) for the lightweight XGBoost endpoint
B) GPU instances for both workloads regardless of model type
C) CPU instances for both workloads regardless of model type
D) The smallest available instance type for both, regardless of workload

---

## Q37

A regulator requires proof that every configuration change to a production SageMaker endpoint (instance type changes, IAM role changes) over the past year is tracked with before/after state and timestamps, for an audit. Which combination of services provides this?

A) AWS Config (resource configuration history/timeline) together with AWS CloudTrail (API call record of who made each change and when)
B) Amazon QuickSight dashboards alone
C) Deleting old endpoint versions to simplify the audit
D) Amazon Comprehend

---

## Q38

A team is choosing a vector store for a RAG application already heavily invested in PostgreSQL/Aurora for their relational data, and wants to add vector similarity search without introducing an entirely new database technology to operate. Which option fits best?

A) Amazon Aurora PostgreSQL with the pgvector extension
B) Amazon SQS
C) AWS Glue Data Catalog
D) Amazon Route 53

---

## Q39

A team runs 200 different hyperparameter configurations, selecting the single best one based on validation set performance, then reports that exact validation score as the expected production performance. What is the risk with this practice, and what should be done instead?

A) Repeatedly selecting the best of many configurations on the same validation set causes the reported score to be optimistically biased; a separate, untouched held-out test set should be used for the final, honest performance estimate
B) There is no risk; the validation score is always a reliable final performance estimate
C) The fix is to increase the learning rate on the winning configuration
D) The fix is to remove the validation set from future use entirely

---

## Q40

A SageMaker real-time endpoint's SLA requires it to automatically add capacity when the number of invocations per instance exceeds a target threshold, and remove capacity when demand drops, without manual intervention. Which configuration achieves this?

A) Application Auto Scaling with a target-tracking scaling policy based on `SageMakerVariantInvocationsPerInstance`
B) A fixed instance count configured once and never changed
C) Manually watching CloudWatch dashboards and resizing the endpoint by hand each time
D) SageMaker Ground Truth active learning

---

## Q41

SageMaker Clarify computes a pre-training bias report on a loan dataset and flags that the 'approved' label is statistically correlated with the applicant's zip code, a known proxy for a protected demographic attribute. What does this pre-training metric tell the team, and what is the next correct step before training?

A) The raw data itself contains a potential bias signal the model could learn as a shortcut; the team should investigate and consider mitigations (resampling, removing/transforming the proxy feature, reweighting) before training a model on this data
B) This is irrelevant because only post-training metrics matter
C) This means the model has already learned to discriminate
D) This means the dataset has a data leakage problem unrelated to bias

---

## Q42

(Choose TWO) A multi-class product-categorization dataset has 30 categories; the top 3 categories make up 85% of records, and the remaining 27 categories share the other 15%, with several categories having fewer than 20 examples each. Which TWO actions directly address this severe multi-class imbalance?

A) Apply class weighting so the training algorithm penalizes misclassifying rare categories more heavily
B) Oversample the rarest categories (and/or consider merging extremely rare categories if acceptable for the business use case)
C) Take no action since multi-class datasets are expected to have unequal categories
D) Increase only the learning rate
E) Report overall accuracy as the sole evaluation metric

---

## Q43

A team wants to quickly try several algorithms and hyperparameter configurations on a new tabular dataset with minimal manual coding, including automatic feature engineering suggestions and a leaderboard of candidate models ranked by performance. Which SageMaker capability is designed for this?

A) SageMaker Autopilot (AutoML)
B) SageMaker Ground Truth
C) AWS Glue DataBrew
D) Amazon Comprehend custom classification only

---

## Q44

After deploying a new model version, CloudWatch alarms show the new version's error rate rising sharply compared to the previous version, while only 10% of traffic has been shifted to it so far via a linear/canary deployment configuration. What should happen next?

A) The deployment should automatically roll back to the previous model version based on the configured alarm-triggered rollback policy, limiting the blast radius to the small fraction of traffic already shifted
B) Traffic should immediately be shifted to 100% on the new version to finish the rollout faster
C) The alarm should be ignored since only 10% of traffic is affected
D) The endpoint should be deleted entirely with no model serving any traffic

---

## Q45

An image classification training set has only 2,000 images for a rare manufacturing-defect category, and the team wants to artificially expand effective training diversity without collecting new photos. Which data preparation technique is appropriate?

A) Data augmentation — applying random rotations, flips, crops, and color jitter to generate varied versions of existing images
B) Deleting 1,000 of the 2,000 images to simplify the dataset
C) Converting all images to grayscale and reducing resolution to 8x8 pixels
D) Re-labeling all images as the majority class

---

## Q46

A content-moderation system built on a Bedrock foundation model occasionally produces borderline decisions on sensitive flagged content. Before any content is published or removed based on these borderline calls, the company wants a human moderator to review and confirm the decision. Which AWS capability supports this workflow?

A) Amazon Augmented AI (A2I) human review workflow
B) AWS Config
C) Amazon Route 53
D) AWS Direct Connect

---

## Q47

A regulator asks why a loan model denied a specific applicant. The team runs SageMaker Clarify and gets a report showing 'income contributed +0.4, zip code contributed -0.25, employment length contributed +0.1' toward the decision. What kind of explainability output is this, and how does it differ from a global feature-importance ranking?

A) This is a local (per-prediction) SHAP explanation, showing feature contributions for one specific individual's outcome, as opposed to a global ranking of average feature importance across the whole dataset
B) This is a global explanation identical to average feature importance across all customers
C) This is a confusion matrix
D) This is a precision-recall curve

---

## Q48

A company manages dozens of related model versions across multiple projects and needs to group them logically (e.g., all versions of the 'fraud-v2' model together), track their lineage/metadata, and gate promotion between dev, staging, and production environments. Which SageMaker feature organizes this?

A) SageMaker Model Registry, using model package groups to logically group versions of the same model and approval status to gate promotion
B) Amazon S3 folders with no additional tooling
C) AWS Glue Data Catalog
D) Amazon CloudFront distributions

---

## Q49

A team wants reproducible lineage: given a specific trained model, be able to trace exactly which feature values and feature-store version were used at training time, months later, for audit purposes. Which SageMaker Feature Store capability supports this?

A) The Offline Store's time-travel/point-in-time queries against historical feature values
B) Deleting old feature values once a model is trained
C) SageMaker Ground Truth
D) Amazon CloudFront caching

---

## Q50

A healthcare application calling a SageMaker endpoint over the internet must ensure patient data in each inference request and response cannot be intercepted or read in transit by a network eavesdropper. What should be verified/enforced?

A) HTTPS/TLS encryption is enforced for all calls to the SageMaker endpoint (encryption in transit)
B) Only encryption at rest on the model artifacts, with plaintext HTTP allowed for requests
C) IAM permissions alone, with no transport-layer encryption
D) Disabling logging entirely to reduce data exposure

---

## Q51

A team combines predictions from five different models (a gradient-boosted tree, a random forest, a neural network, and two linear models) by averaging their outputs, observing the ensemble generalizes better than any single model alone. What is the primary statistical reason ensembling tends to help?

A) Averaging multiple diverse models tends to cancel out each individual model's uncorrelated errors/variance, improving overall generalization
B) Ensembling always doubles training speed
C) Ensembling eliminates the need for a validation set
D) Ensembling guarantees zero bias in the final prediction

---

## Q52

A global company serves users in the US and Europe and needs ML inference latency to stay low for both regions while maintaining disaster-recovery resilience if one AWS Region has an outage. Which deployment strategy fits?

A) Deploy SageMaker endpoints in multiple AWS Regions (e.g., us-east-1 and eu-west-1) and route users to the nearest healthy Region
B) Deploy a single endpoint in one Region and accept higher latency for the other continent
C) Use only SageMaker Batch Transform for all inference needs
D) Deploy the model exclusively to AWS Outposts with no regional AWS deployment

---

## Q53

A vision model trains on satellite images where object orientation (rotation) in the real world is arbitrary, but color intensity does carry real meaning (e.g., vegetation health). Which augmentation choices are most appropriate?

A) Apply rotation and flip augmentations freely, but avoid aggressive color/intensity distortions that would corrupt a meaningful signal
B) Apply aggressive random color inversion to every image with no restriction
C) Apply no augmentation at all under any circumstances
D) Only ever augment the test set, never the training set

---

## Q54

A finance team wants to be proactively alerted via email/Slack when their cumulative Bedrock token-usage cost for the month is projected to exceed a set budget, before the month ends. Which AWS capability should they configure?

A) An AWS Budgets alert with a forecasted-spend threshold, notifying via SNS
B) A SageMaker Model Monitor schedule
C) AWS Glue DataBrew
D) Amazon Comprehend

---

## Q55

A team wants to improve semantic search relevance for a RAG system and is choosing between two Bedrock embedding models based on benchmark retrieval quality for their specific document domain (legal text). What is the most important consideration when selecting an embedding model for this use case?

A) Choosing an embedding model validated for strong semantic retrieval performance on domain-relevant text, and using the exact same embedding model consistently for both documents and queries
B) Choosing the embedding model with the largest output vector dimensionality regardless of retrieval quality
C) Choosing a different embedding model for documents than for queries to add variety
D) Choosing the cheapest model with no regard to retrieval accuracy

---

## Q56

A startup's GenAI application calls a Bedrock foundation model with highly variable request volume, sometimes near zero for hours, and wants to pay strictly per token/request processed with no capacity to provision or manage. Which Bedrock consumption model fits?

A) On-Demand Bedrock model invocation, billed per input/output token with no provisioning
B) Provisioned Throughput committing to a fixed amount of model capacity for a term
C) A dedicated SageMaker real-time endpoint running the foundation model 24/7
D) Reserved EC2 Instances

---

## Q57

A team building a k-fold cross-validation setup for a small (3,000-row) imbalanced binary classification dataset wants each fold to preserve the original class ratio, to get a reliable estimate of the model's performance on the minority class. Which cross-validation variant should they use?

A) Stratified k-fold cross-validation
B) Plain k-fold cross-validation with random, unstratified folds
C) Leave-one-out cross-validation with no attention to class balance
D) A single random train/test split only, no cross-validation

---

## Q58

A team configures SageMaker Model Monitor to run an hourly data-quality check against a deployed endpoint's captured inference traffic, with CloudWatch alarms tied to the monitor's violation metrics. What is the primary operational benefit of running this on a recurring schedule rather than as a one-time check?

A) It continuously catches drift or data-quality issues that emerge after deployment, as live traffic patterns evolve over time, rather than only validating the model once at launch
B) It eliminates the need for any CloudWatch alarms
C) It replaces the need for a model retraining process entirely
D) It guarantees the model will never need to be redeployed

---

## Q59

(Choose TWO) A fine-tuned foundation model has become excellent at a new narrow task but has noticeably lost some of its general-purpose capabilities it had before fine-tuning (general conversation quality has degraded) — a phenomenon called catastrophic forgetting. Which TWO are valid mitigations?

A) Use parameter-efficient fine-tuning (e.g., LoRA/PEFT), updating only a small added set of parameters and leaving most of the original model weights intact
B) Mix some general-purpose training examples into the fine-tuning dataset alongside the narrow-task examples
C) Remove the validation set so training can use 100% of the data
D) Apply SMOTE oversampling to the fine-tuning dataset
E) Switch to SageMaker Model Monitor for drift detection

---

## Q60

A team deploying SageMaker Serverless Inference for a GenAI embedding model notices the first request after a period of inactivity has noticeably higher latency than subsequent requests. What causes this, and is it a significant concern for their use case (a background batch-like job tolerant of some delay)?

A) This is a cold start, where the serverless environment must initialize before serving the first request after idling; it's an acceptable trade-off given their traffic is tolerant of some delay, in exchange for not paying for idle capacity
B) This indicates the model is broken and must be redeployed
C) This is data drift and requires retraining
D) This is caused by insufficient IAM permissions

---

## Q61

A healthcare ML team must encrypt all raw training data at rest in S3, and separately wants the ability to immediately and centrally revoke all access to that data (including any cached decrypted copies becoming newly inaccessible going forward) in response to a security incident. Which encryption setup best supports this?

A) SSE-KMS with a customer-managed CMK, so the key policy can be modified or the key disabled to immediately cut off decryption for all objects encrypted under it
B) SSE-S3 with Amazon-owned keys, which the company cannot directly control or revoke
C) No encryption, relying solely on IAM bucket policies
D) Client-side encryption with a hard-coded key embedded in application code

---

## Q62

A security team wants one centralized dashboard that aggregates and prioritizes findings from GuardDuty (threat detection), Macie (sensitive data discovery), and AWS Config (configuration compliance) across all accounts in an organization, rather than checking each service's console separately. Which service fits?

A) AWS Security Hub
B) Amazon QuickSight
C) AWS Direct Connect
D) Amazon Route 53

---

## Q63

A team is designing a GenAI application that must plan and execute a variable sequence of steps (look up an order, check inventory, decide whether to escalate to a human, then respond) where the sequence of actions cannot be fully hard-coded in advance because it depends on intermediate results. During model/solution development, which architectural approach should they design around, versus a single fixed prompt chain?

A) An agent-based architecture where the foundation model reasons step-by-step, decides which tool/action to invoke next based on intermediate results, and can branch dynamically (as opposed to a rigid, pre-defined linear prompt chain)
B) A single prompt with no tool access that tries to generate the entire multi-step outcome in one shot
C) A regression model predicting a numeric escalation score only
D) A k-means clustering step to decide the action sequence

---

## Q64

A team configuring a SageMaker endpoint deployment wants to choose between shifting all traffic to the new version instantly, shifting it gradually over equal increments on a schedule, or shifting a small fixed percentage first and then the rest after a bake time. Which deployment configuration options do these three correspond to?

A) All-at-once, Linear, and Canary deployment configurations, respectively
B) Batch Transform, Serverless Inference, and Asynchronous Inference, respectively
C) Three unrelated IAM policy types
D) Three different SageMaker Pipelines step types with no relation to traffic shifting

---

## Q65

A tabular dataset has a numeric 'last_purchase_amount' column where 12% of rows are missing because those customers made no prior purchase (a meaningful signal, not random noise), while a separate 'shipping_zip' column has 0.3% missing values from sporadic data-entry errors. What is the most appropriate handling for each?

A) For 'last_purchase_amount', add a missing-value indicator flag and impute with a sentinel/median value since the missingness itself is meaningful; for 'shipping_zip', impute the rare random errors with the mode or drop those few rows
B) Drop every row with any missing value in either column
C) Replace all missing values in both columns with zero and take no further action
D) Delete both columns entirely from the dataset

---
