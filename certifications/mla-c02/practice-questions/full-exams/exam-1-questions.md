# MLA-C02 Full Mock Exam 1 — Questions

65 questions mixing all four MLA-C02 domains in one sitting, matching the real exam's associate-level format (multiple choice and multiple response only). See [`index.md`](index.md) for instructions and scoring. Do not peek at [`exam-1-answer-key.md`](exam-1-answer-key.md) until you have answered every question.

---

## Q1

A payments company wants to score every credit card swipe for fraud risk within 2 seconds of the swipe happening, using features computed from the live transaction feed. Which approach should the ML engineer choose?

A) A nightly AWS Glue Spark job that batches the previous day's transactions from S3
B) Amazon Kinesis Data Streams feeding a stream-processing application that computes features in near real time
C) A weekly manual CSV export from the payments database
D) Amazon SageMaker Data Wrangler scheduled to run once per day

---

## Q2

A model achieves 99% accuracy on training data but only 72% on validation data, with the gap widening as training continues. What is this phenomenon and what is the most direct fix?

A) Underfitting; increase model complexity
B) Overfitting; apply regularization (L1/L2, dropout), early stopping, or get more training data
C) Data drift; retrain on newer data
D) Class imbalance; apply SMOTE

---

## Q3

A model must score large batches of 2 million records once per night, with no requirement for sub-second response and no need for a persistently running endpoint. Which SageMaker inference option is most cost-effective?

A) A real-time SageMaker endpoint kept running 24/7
B) SageMaker Batch Transform
C) SageMaker Serverless Inference
D) SageMaker Asynchronous Inference

---

## Q4

SageMaker Model Monitor reports that the statistical distribution of a deployed model's input features has shifted compared to training time, but it isn't yet clear whether prediction accuracy has dropped. What is this phenomenon called?

A) Concept drift
B) Data drift
C) Overfitting
D) Model parallelism

---

## Q5

A team stores raw clickstream, product catalog, and order data as Parquet files across multiple S3 prefixes. Several groups need Athena, Redshift Spectrum, and SageMaker Processing to query this data with one consistent, discoverable schema, without each team hand-defining table DDL. What should they set up?

A) An AWS Glue Crawler that scans the S3 prefixes and populates the AWS Glue Data Catalog
B) A separate Amazon RDS database per team, loaded with manual INSERT scripts
C) A SageMaker Data Wrangler flow that each team re-runs manually before querying
D) An Amazon Kinesis Data Firehose delivery stream pointed at each prefix

---

## Q6

Both training and validation accuracy are poor (60%) and nearly identical for a linear regression model applied to a dataset with clearly non-linear relationships. What is the most likely cause and fix?

A) Overfitting; add dropout
B) Underfitting; increase model complexity (e.g., add polynomial features or switch to a more expressive algorithm) or add more informative features
C) Data leakage; remove the leaking feature
D) Vanishing gradients; switch activation function

---

## Q7

A company hosts 200 small, lightly-used ML models, each receiving only a handful of requests per day, and wants to avoid paying for 200 separate always-on endpoints. Which approach minimizes cost while keeping all models servable?

A) A SageMaker multi-model endpoint that dynamically loads models from S3 onto shared instances as needed
B) 200 separate real-time endpoints, each on its own instance
C) Combine all 200 models into a single model file
D) Retrain all models as a single multi-class classifier

---

## Q8

A customer-facing GenAI chatbot occasionally discusses competitor products and political topics the company wants to strictly avoid, and sometimes leaks fragments of PII from retrieved documents in its answers. Which Bedrock feature should be configured to block this at both the input and output stage?

A) Bedrock Guardrails with denied topics and PII redaction policies
B) SageMaker Clarify
C) Increasing the model's context window
D) AWS WAF

---

## Q9

Before training, a data scientist runs SageMaker Data Wrangler's built-in analysis on a loan-approval dataset and wants a no-code report flagging class imbalance and sensitive attributes that correlate with the label. Which capability should they use?

A) AWS Glue Jobs (Spark-based ETL scripts)
B) Amazon Athena ad hoc SQL queries
C) Data Wrangler's built-in Data Quality and Insights report / bias report
D) Amazon EMR with a custom PySpark notebook

---

## Q10

A medical screening model must minimize missed-disease cases (false negatives) even if it means flagging more healthy patients for a follow-up test (false positives). Which metric should be prioritized when tuning the decision threshold?

A) Precision
B) Recall (sensitivity)
C) Specificity
D) Raw accuracy

---

## Q11

An inference workload has highly unpredictable, spiky traffic — sometimes zero requests for hours, then sudden bursts — and the team wants to avoid managing instance counts or paying for idle capacity, tolerating occasional cold-start latency. Which deployment option fits best?

A) SageMaker Serverless Inference
B) A fixed-size real-time endpoint provisioned for peak load at all times
C) SageMaker Batch Transform run every hour
D) A single large EC2 instance with manual scaling scripts

---

## Q12

An ML engineer needs to create an execution role for SageMaker training jobs that can only read from one specific S3 bucket/prefix and decrypt objects with one specific KMS key, following least-privilege principles. What should the IAM policy attached to this role do?

A) Grant `s3:*` and `kms:*` across all resources for simplicity
B) Scope `s3:GetObject`/`s3:ListBucket` to the specific bucket/prefix ARN and `kms:Decrypt` to the specific key ARN only
C) Attach the AWS-managed `AdministratorAccess` policy
D) Grant no permissions and rely on public bucket access instead

---

## Q13

(Choose TWO) A binary fraud classifier is trained on data that is 98% 'legitimate' and 2% 'fraud'. The model currently predicts 'legitimate' almost every time. Which TWO actions directly address this class imbalance during data preparation?

A) Oversample the minority ('fraud') class, including SMOTE-style synthetic augmentation
B) Apply class weighting so the training algorithm penalizes misclassifying the minority class more heavily
C) Increase the number of training epochs
D) Decrease the learning rate
E) Shrink the validation set to speed up iteration

---

## Q14

A churn model is evaluated on a dataset where only 4% of customers actually churn. The team reports 96% accuracy and is confident the model is excellent. What is the issue with this evaluation, and what should they use instead?

A) Nothing is wrong; 96% accuracy is strong evidence of a good model
B) Accuracy is misleading on imbalanced data (a model predicting 'no churn' for everyone would also score ~96%); use precision, recall, F1, or AUC-PR instead
C) They should lower the learning rate
D) They should increase the batch size

---

## Q15

A document-processing model takes up to 10 minutes to process a single large PDF and the caller does not need an immediate synchronous response, just eventual results with a callback/notification. Which SageMaker inference option is designed for this?

A) SageMaker Real-Time Inference with a 1-second timeout
B) SageMaker Asynchronous Inference
C) SageMaker Serverless Inference with default settings
D) A synchronous REST API Gateway call that waits for the full 10 minutes

---

## Q16

(Choose TWO) A company's security policy forbids SageMaker training jobs and endpoints from having any direct path to the public internet, while still needing to reach S3 and other AWS services. Which TWO architectural choices achieve this?

A) Run SageMaker resources inside a VPC with no internet gateway attached
B) Use VPC endpoints (AWS PrivateLink) so traffic to S3 and other AWS service APIs stays on the AWS private network
C) Run SageMaker resources in the default VPC with a public IP and an open security group
D) Disable all encryption to simplify networking
E) Use a NAT Gateway with full outbound internet access to reach S3

---

## Q17

A SageMaker Feature Store is being evaluated for a team whose model performs well offline but degrades in production because the live inference code computes a feature slightly differently from the training pipeline. Which Feature Store capability directly fixes this?

A) The Offline Store alone, used for both training and inference lookups
B) A combination of an Offline Store for training and an Online Store for low-latency inference, both fed by the same feature definitions
C) Re-running the training job more frequently
D) Switching the model to a simpler algorithm

---

## Q18

An ML engineer wants to tune five hyperparameters of an XGBoost model and needs an efficient search method that uses results of previous trials to intelligently choose the next set of values to try, minimizing the number of expensive training runs. Which SageMaker capability fits?

A) SageMaker Automatic Model Tuning with Bayesian search strategy
B) A manual grid search coded by hand with no automation
C) Running the exact same hyperparameters 100 times
D) SageMaker Ground Truth

---

## Q19

A team wants to automate a repeatable ML workflow: pull fresh data, run a Processing job, train a model, evaluate it against a baseline, and conditionally register it in the Model Registry only if it beats the baseline — all as a versioned, trackable pipeline. Which service is purpose-built for this?

A) AWS Lambda functions chained manually with no orchestration service
B) Amazon SageMaker Pipelines
C) Amazon QuickSight
D) AWS Glue DataBrew

---

## Q20

(Choose TWO) A compliance team requires that all model artifacts in S3 and all SageMaker endpoint storage volumes be encrypted at rest using customer-managed keys the company controls, with a full audit trail of key usage. Which TWO should be configured to satisfy both requirements?

A) Encrypt S3 model artifacts and endpoint EBS volumes using AWS KMS customer-managed keys (CMKs)
B) Enable AWS CloudTrail to log all KMS key usage (every Encrypt/Decrypt API call)
C) Rely on default S3 server-side encryption with AWS-managed keys and no further configuration
D) Store model artifacts unencrypted but behind a private subnet
E) Use client-side encryption only, with no AWS-side encryption of the volumes

---

## Q21

A team has 400 TB of raw training images in S3 that are accessed heavily for the first month after upload, then almost never, but must be retrievable within minutes if ever needed again. Which storage approach minimizes cost while meeting this access pattern?

A) Keep everything in S3 Standard indefinitely
B) Move everything to S3 Glacier Deep Archive immediately on upload
C) Use an S3 Lifecycle policy transitioning to S3 Intelligent-Tiering or Standard-IA/Glacier Instant Retrieval after the access-heavy window
D) Delete the data after 30 days and re-collect it if needed

---

## Q22

A team needs to classify structured tabular data (numeric + categorical columns) for a credit risk model, prioritizing strong out-of-the-box accuracy with minimal custom algorithm engineering. Which SageMaker built-in algorithm is the most natural first choice?

A) XGBoost
B) A from-scratch convolutional neural network
C) Seq2Seq
D) Object2Vec for embeddings-only use

---

## Q23

(Choose TWO) A new model version is ready, and the team wants to validate it against real production traffic before fully replacing the current model, with the ability to compare real-world performance safely before a full cutover. Which TWO SageMaker deployment capabilities support this?

A) Production variants with weighted traffic splitting (A/B testing) on a single endpoint, gradually shifting more traffic to the new version
B) Shadow testing / canary-style rollout, where the new model's predictions are logged and compared without (or with minimal) impact on what's actually returned to users
C) Deleting the old endpoint immediately and deploying only the new model
D) SageMaker Ground Truth labeling jobs
E) AWS Glue crawlers

---

## Q24

A tabular dataset has a numeric 'annual_income' column with occasional extreme values (e.g., $50,000,000) that are data-entry errors, badly skewing a linear regression model's training. What data preparation step should be applied first?

A) One-hot encode the income column
B) Apply outlier detection/capping (winsorizing) or remove the erroneous extreme values before training
C) Increase the model's learning rate to compensate
D) Add more training epochs

---

## Q25

A team wants to run a large SageMaker training job on a model that takes 10 hours to train, is fault-tolerant via periodic checkpointing, and is not time-critical. Which compute purchasing option minimizes cost?

A) Managed Spot Training with checkpointing enabled
B) On-Demand instances at full price for the entire 10 hours
C) A 3-year All Upfront Reserved Instance for a one-time job
D) Provisioned Concurrency

---

## Q26

A company wants a foundation model to adopt a very specific customer-support tone, format, and vocabulary consistently across thousands of conversations, a behavior change that prompting alone hasn't reliably achieved. Minimal need to inject new facts. Which customization approach is most appropriate?

A) Retrieval-Augmented Generation (RAG) connected to a knowledge base
B) Fine-tuning the foundation model on examples of the desired tone/format/vocabulary
C) Increasing the model's temperature setting
D) Switching to a smaller context window

---

## Q27

A SageMaker real-time endpoint experiences request spikes during business hours and near-zero traffic overnight, but the team wants it to remain near-instantly responsive (unlike serverless cold starts) while still saving cost. Which feature should they configure?

A) Auto Scaling for the SageMaker endpoint, scaling instance count based on a target-tracking metric like invocations per instance
B) A fixed single instance sized for peak traffic, running unchanged at all hours
C) Switching to Batch Transform
D) Deleting the endpoint every night and recreating it every morning manually

---

## Q28

A dataset has a categorical feature 'shipping_carrier' with 4 unrelated values (UPS, FedEx, USPS, DHL) with no inherent order. Which encoding is most appropriate before feeding this feature into a gradient-boosted tree or linear model?

A) Label encoding (assigning 0, 1, 2, 3 arbitrarily)
B) One-hot encoding (a binary column per carrier)
C) Leaving the text values as-is
D) Min-max scaling

---

## Q29

A real-time SageMaker endpoint handles steady, predictable traffic 24/7 for the next 2 years. Which pricing/commitment option minimizes cost for this long-term, stable workload?

A) SageMaker Savings Plans committing to a consistent amount of usage over a 1- or 3-year term
B) Managed Spot Training
C) On-Demand pricing with no commitment
D) SageMaker Serverless Inference

---

## Q30

Two binary classifiers are compared using ROC curves. Classifier A has an AUC of 0.92 and Classifier B has an AUC of 0.68. What does this indicate?

A) Classifier B trains faster, so it should be preferred
B) Classifier A has a substantially better ability to rank positive examples above negative examples across all thresholds
C) AUC only matters for regression models, not classifiers
D) Both are equivalent because AUC doesn't reflect real performance

---

## Q31

A company wants to build a RAG-based support chatbot grounded in their product documentation stored in S3, without standing up and managing their own vector database, embedding pipeline, or retrieval code. Which Bedrock feature is designed exactly for this?

A) Bedrock Guardrails
B) Bedrock Knowledge Bases
C) Bedrock Agents only, with no retrieval component
D) SageMaker Ground Truth

---

## Q32

A neural network trained on raw, unscaled features (one ranging 0-1, another ranging 0-1,000,000) converges extremely slowly with gradient descent. What data preparation step addresses this directly?

A) Feature scaling (standardization or min-max normalization) so features share a comparable numeric range
B) One-hot encoding all numeric features
C) Removing the feature with the larger range entirely
D) Increasing the batch size only

---

## Q33

An auditor needs a complete, immutable history of every SageMaker API call made in the account (who created which training job, who deployed which endpoint, from which IP, and when) for a compliance review. Which service provides this?

A) AWS CloudTrail
B) Amazon CloudWatch Metrics only
C) AWS Cost Explorer
D) Amazon Macie

---

## Q34

(Choose TWO) A dataset for a rare-disease classifier has only 500 positive examples out of 200,000 total. The team must create train/validation/test splits and choose how to evaluate the model reliably on the minority class. Which TWO practices should they follow?

A) Use a stratified split that preserves the same ~0.25% positive class ratio in train, validation, and test sets
B) Evaluate using minority-class-aware metrics (recall, F1, AUC-PR) rather than relying on aggregate accuracy alone
C) Use a simple random 80/10/10 split with no regard to class proportions
D) Put all positive examples into the training set only, leaving none for validation/test
E) Sort the data alphabetically before splitting

---

## Q35

A team wants to build an image classifier for a niche product category with only 800 labeled images, far too few to train a deep CNN from scratch effectively. Which approach gives the best results with limited data and training time?

A) Train a brand-new deep CNN from randomly initialized weights
B) Use transfer learning: start from a pre-trained model (e.g., via SageMaker JumpStart) and fine-tune on the 800 images
C) Use k-means clustering instead of a classifier
D) Train only on 10 of the 800 images to reduce noise

---

## Q36

A company wants a GenAI assistant that can not just answer questions, but also take multi-step actions — check an order status via an internal API, and if needed call a Lambda function to issue a refund — reasoning about which tool to invoke and in what order. Which Bedrock capability is purpose-built for this?

A) Bedrock Agents, using action groups backed by Lambda functions/APIs
B) Plain prompt engineering with no tool integration
C) Bedrock Guardrails
D) SageMaker Batch Transform

---

## Q37

A team needs to detect bias in a trained credit-scoring model's actual predictions across demographic groups (e.g., disparate impact), separate from checking the raw training data for imbalance. Which SageMaker feature performs this post-training bias analysis?

A) SageMaker Clarify post-training bias metrics
B) Bedrock Guardrails
C) AWS Config
D) Amazon Comprehend sentiment analysis

---

## Q38

A healthcare ML team discovers that a training dataset exported to S3 contains unredacted patient names and SSNs in free-text fields, which must be identified and removed before any model can touch the data. Which AWS service should they use to automatically discover this sensitive data?

A) Amazon Macie
B) AWS Glue Data Catalog
C) Amazon Athena
D) SageMaker Ground Truth

---

## Q39

(Choose TWO) A linear regression model is overfitting on a dataset with 200 features, many of which are irrelevant or redundant. Which TWO regularization approaches directly help, and what distinguishes them?

A) L1 (Lasso) regularization, which can shrink irrelevant feature coefficients to exactly zero, effectively performing feature selection
B) L2 (Ridge) regularization, which shrinks coefficients toward zero without necessarily eliminating any, reducing variance
C) Increasing the polynomial degree of every feature
D) Removing the validation set to train on more data
E) Increasing the number of training epochs without bound

---

## Q40

A regulated-industry team requires every model version promoted to production to first pass a manual sign-off by a model risk officer, with a clear versioned history of what was approved and when. Which SageMaker feature should they integrate into their pipeline?

A) SageMaker Model Registry with model package groups and a manual approval status step
B) Deploying directly from a notebook with no tracking
C) AWS Glue Data Catalog
D) Amazon CloudFront

---

## Q41

A regulator asks a lending company to explain, for a specific denied applicant, exactly how much each input feature contributed to the model's decision. Which SageMaker capability directly answers this?

A) SageMaker Clarify explainability (SHAP values) for the specific prediction
B) SageMaker Ground Truth
C) Amazon QuickSight dashboards
D) AWS Trusted Advisor

---

## Q42

A team is building a RAG system over a 2,000-page internal policy manual. Early tests show the model's answers are often missing context because relevant information got split across chunk boundaries. What is the most direct fix during the data preparation step?

A) Switch to a larger foundation model for generation
B) Reduce chunk size to the smallest possible value
C) Tune chunk size and add overlap between consecutive chunks so related content isn't orphaned at a boundary
D) Skip embeddings and paste the entire manual into every prompt

---

## Q43

A hiring model shows a confusion matrix with many false negatives (qualified candidates predicted as 'reject') but very few false positives. The business says missing qualified candidates is costly, but wrongly advancing unqualified ones is only a minor inconvenience. What should the team do?

A) Leave the threshold unchanged since overall accuracy is already high
B) Lower the classification decision threshold for the 'advance' class to reduce false negatives, accepting more false positives
C) Raise the classification decision threshold to reduce false positives further
D) Switch to an unsupervised clustering approach

---

## Q44

A team isn't sure which instance type and configuration will give the best latency/cost tradeoff for their trained model in production. Which SageMaker feature automates benchmark testing across instance types and recommends an optimal configuration?

A) SageMaker Inference Recommender
B) AWS Trusted Advisor
C) Amazon CloudWatch Logs Insights
D) AWS Cost Explorer alone

---

## Q45

A team needs to choose an embedding model and vector store for a RAG application that must support millisecond-latency nearest-neighbor search over 50 million document chunks on AWS, fully managed. Which combination best fits?

A) A Bedrock embedding model (e.g., Titan Embeddings) paired with Amazon OpenSearch Service's vector engine or Bedrock Knowledge Bases
B) A Bedrock embedding model paired with Amazon Redshift as the vector store
C) No embedding model; store raw text in DynamoDB and use string matching
D) A Bedrock embedding model paired with Amazon SQS to hold the vectors

---

## Q46

SageMaker Model Monitor is scheduled to run bias-drift checks on a deployed model's live predictions over time. Which outcome would this specifically catch that a one-time pre-deployment Clarify check would not?

A) The model's fairness profile degrading after deployment as the live population shifts, even though the original pre-deployment bias checks passed
B) Typos in the training dataset column names
C) Whether the S3 bucket storing training data is public
D) CPU utilization of the training instance

---

## Q47

(Choose TWO) A forecasting model's quality is measured by how far its predicted numeric values are from the actual numeric sales figures, in the same units as sales (dollars). Which TWO metrics are appropriate?

A) RMSE (Root Mean Squared Error)
B) MAE (Mean Absolute Error)
C) F1 score
D) Precision and recall
E) AUC-ROC

---

## Q48

A computer-vision model uses custom Python preprocessing code and a custom-trained PyTorch model not matching any SageMaker built-in container. How should the team package this for a SageMaker real-time endpoint?

A) Build a custom Docker container with the inference code and dependencies, push it to Amazon ECR, and deploy it as a SageMaker Bring-Your-Own-Container (BYOC) model
B) It cannot be deployed on SageMaker since it isn't a built-in algorithm
C) Convert the custom model into a SageMaker Data Wrangler flow
D) Deploy it directly to Lambda with no container required and no size limits

---

## Q49

A team needs 50,000 images labeled with bounding boxes for an object-detection model, and wants human reviewers in the loop with built-in quality control and the option to blend in automated labeling as confidence improves. Which service fits?

A) Amazon Mechanical Turk accessed directly with no tooling
B) Amazon SageMaker Ground Truth
C) AWS Glue DataBrew
D) Amazon Comprehend

---

## Q50

An ML pipeline's Lambda function needs to call a third-party sentiment-analysis API using an API key, and the team wants to avoid hard-coding the key in source code while also getting automatic key rotation support. Which service is the best fit?

A) AWS Secrets Manager, which supports automatic rotation of stored secrets
B) Storing the API key as a plaintext environment variable committed to source control
C) Amazon S3 with public read access to a key file
D) Hard-coding the key directly in the Lambda function body

---

## Q51

A company is choosing between two Bedrock foundation models for a customer-facing summarization task and wants a structured, repeatable way to compare their output quality on a held-out set of prompts, including both automatic metrics and optional human judgment. Which Bedrock capability fits?

A) Bedrock Guardrails
B) Bedrock model evaluation jobs (automatic and human-based)
C) Bedrock Agents
D) SageMaker Ground Truth labeling jobs only

---

## Q52

A team wants a new SageMaker Pipelines training run to automatically trigger whenever a new labeled dataset lands in a specific S3 prefix, without a human manually starting the job. Which service should they use to detect the event and trigger the pipeline?

A) Amazon EventBridge rule watching for S3 object-created events, invoking the pipeline execution
B) A person checking the S3 console every morning
C) Amazon CloudFront
D) AWS Direct Connect

---

## Q53

A retail company has 5 years of daily sales data and wants to train a forecasting model, then validate it in a way that avoids data leakage from the future into the past. Which train/test split strategy is correct?

A) A random 80/20 shuffle split across all 5 years
B) A time-based split: train on earlier years, validate/test on the most recent period, preserving chronological order
C) K-fold cross-validation with folds shuffled randomly across years
D) Stratified split by product category only

---

## Q54

A model making low-confidence predictions on sensitive content (e.g., content moderation decisions near the classifier's confidence threshold) should be routed to a human reviewer before any action is taken. Which AWS capability supports this human-in-the-loop review workflow?

A) Amazon Augmented AI (A2I)
B) AWS Config
C) Amazon CloudFront
D) AWS Direct Connect

---

## Q55

A team needs a foundation model to answer questions that require up-to-the-minute, frequently changing internal pricing data, with minimal engineering effort and without retraining whenever prices change. Which approach is most appropriate and cost-effective?

A) Fine-tune the model nightly on the latest pricing data
B) Use RAG: store current pricing data in a retrievable knowledge base and let the model ground its answers in retrieved content at query time
C) Hard-code the prices into the model weights permanently
D) Increase the model's temperature to improve accuracy

---

## Q56

A manufacturing company needs model inference to run on factory-floor edge devices with intermittent or no internet connectivity, using a model trained in SageMaker in the cloud. Which service lets them compile and deploy the trained model to run efficiently on edge hardware?

A) SageMaker Neo (model compilation) with SageMaker Edge Manager/edge deployment capabilities
B) A real-time SageMaker endpoint accessed over the factory's unreliable internet connection
C) Amazon QuickSight
D) AWS Glue Crawler

---

## Q57

A data engineering team must join and transform 80 TB of semi-structured JSON logs distributed across thousands of S3 objects, requiring custom Spark code and complex joins across several large datasets. Which service is best suited for this large-scale, code-driven transformation?

A) Amazon QuickSight
B) AWS Glue ETL jobs or Amazon EMR running Spark
C) SageMaker Data Wrangler's visual UI only
D) AWS Lambda functions processing one file at a time

---

## Q58

A security team wants continuous, automated threat detection across an ML pipeline's AWS accounts — flagging things like unusual API calls, compromised credentials being used to spin up GPU training instances for cryptomining, or anomalous data exfiltration patterns. Which service is designed for this?

A) Amazon GuardDuty
B) AWS Glue
C) Amazon SageMaker Model Monitor
D) Amazon Kinesis Data Firehose

---

## Q59

An NLP model for text classification shows excellent performance on the training language style but fails badly on slightly reworded customer messages at inference time, despite the underlying intent being identical. The team suspects the model memorized surface wording rather than learning semantic intent. What combination of actions best addresses this?

A) Use data augmentation (paraphrasing, synonym substitution) during training plus stronger regularization to encourage learning general patterns over memorized phrasing
B) Increase the vocabulary size only
C) Remove regularization entirely to let the model fit the data more closely
D) Reduce the training dataset to only the cleanest examples

---

## Q60

A Bedrock Agent powers a multi-turn customer support conversation and must remember earlier details the customer provided (like an order number) across several back-and-forth turns within the same session. Which concept/feature is responsible for this?

A) Session state/context management maintained by the Bedrock Agent across turns in a conversation
B) Re-sending the entire company knowledge base on every single turn
C) Bedrock Guardrails
D) SageMaker Model Monitor

---

## Q61

A team ingesting IoT sensor telemetry at extremely high throughput wants the simplest fully-managed way to continuously land the raw stream into S3 in batched, compressed files, with optional format conversion to Parquet, without writing custom stream-processing code.

A) Amazon Kinesis Data Firehose
B) Amazon Kinesis Data Streams with a custom consumer application
C) AWS Glue Crawler
D) Amazon Redshift Spectrum

---

## Q62

A company must demonstrate to auditors that a specific SageMaker endpoint's configuration (e.g., encryption enabled, specific instance type, specific IAM role) has not drifted from an approved baseline over the past 6 months, and must be alerted if it ever does. Which service fits?

A) AWS Config with a custom or managed rule evaluating the endpoint's configuration against the approved baseline
B) Amazon QuickSight
C) AWS Direct Connect
D) Amazon Comprehend

---

## Q63

During training, a deep neural network's validation loss steadily improves for the first 40 epochs, then starts climbing again while training loss keeps falling, through epoch 200. The team wants to automatically stop training at the best point without manually watching the loss curve. Which technique should they enable?

A) Early stopping, halting training once validation loss stops improving for a set number of rounds and keeping the best checkpoint
B) Increasing the number of epochs to 500 to let it train longer
C) Removing the validation set so training can use 100% of the data
D) Switching to a larger batch size only

---

## Q64

(Choose TWO) A team is designing an MLOps workflow to orchestrate steps across multiple AWS services — a Glue ETL job, then a SageMaker training job, then a conditional branch to either deploy or alert a human — with built-in retries, visual workflow tracking, and support for long-running (multi-hour) steps. Which TWO services/features are appropriate building blocks?

A) AWS Step Functions to orchestrate the cross-service state machine
B) SageMaker Pipelines as the ML-specific portion of the orchestrated workflow
C) Amazon QuickSight dashboards as the orchestration engine
D) A single Lambda function containing all steps inline with a 15-minute execution limit
E) Amazon Route 53 health checks

---

## Q65

A fraud-detection feature pipeline joins real-time account data with historical aggregates. The team notices the historical aggregate feature was accidentally computed using data that includes the very label it's trying to predict (future fraud outcomes). What problem is this, and what should be done?

A) This is normal and does not need correcting
B) This is data leakage; the feature must be recomputed using only information available strictly before the prediction point in time
C) This is overfitting; add dropout to the model
D) This is class imbalance; apply SMOTE

---
