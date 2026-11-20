# Domain 1 Practice Questions — Data Preparation for ML and AI (28%)

14 questions covering task statements 1.1–1.4: ingestion/storage, transformation/feature
engineering, data integrity/bias/splitting, and embeddings/RAG data prep. See the
[Domain 1 README](../domain-1-data-preparation/README.md) for the full map.

---

## Q1

A fraud-detection team needs to score each credit card transaction for fraud risk within
seconds of the transaction occurring, using features derived from the live transaction stream.
Which ingestion approach should they use?

A) A nightly AWS Glue batch job that loads the previous day's transactions into S3
B) Amazon Kinesis Data Streams feeding a stream-processing application that computes features in near-real time
C) A weekly manual CSV export from the payments database into Amazon S3
D) Amazon SageMaker Data Wrangler scheduled to run once per day

**Correct Answer: B**

**Explanation:** Near-real-time, continuously arriving data that must produce features within
seconds is the textbook use case for **Amazon Kinesis Data Streams** — it's built for streaming
ingestion with sub-second to second-level latency, letting downstream consumers (e.g., a Kinesis
Data Analytics or Lambda-based feature computation) react to each record as it arrives. See
[`services/analytics/kinesis-family.md`](../../../services/analytics/kinesis-family.md) and the
Domain 1 README's ["streaming clickstream" scenario](../domain-1-data-preparation/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A:** A nightly Glue batch job introduces up to a 24-hour delay — completely incompatible
  with a "within seconds" requirement. Batch is for periodic, non-urgent transformation.
- **C:** A weekly manual export is even slower than the nightly batch job and is also
  operationally fragile (manual process, error-prone, not automated).
- **D:** SageMaker Data Wrangler is a data exploration/cleaning tool for preparing datasets for
  modeling, not a streaming ingestion or real-time feature computation service, and "once per
  day" is itself disqualifying for a seconds-level requirement.

---

## Q2

A model performs very well during offline evaluation but makes noticeably worse predictions in
production. Investigation reveals that the feature values computed for live inference differ
slightly from how the same features were computed during training (different code paths were
used in each place). What is the best long-term fix?

A) Retrain the model more frequently
B) Store and serve all features from a single SageMaker Feature Store, with an Offline Store for training and an Online Store for inference
C) Increase the size of the training dataset
D) Switch the model to a simpler algorithm to reduce variance

**Correct Answer: B**

**Explanation:** This is **training/serving skew** — the same logical feature is computed
differently (or drifts out of sync) between the training pipeline and the live inference path.
**SageMaker Feature Store** fixes this at the root by making the feature computation happen
once and be reused by both the Offline Store (for bulk training jobs) and the Online Store
(low-latency lookups for real-time inference), guaranteeing training and inference see the
identical value for a given feature. See
[`services/machine-learning-ai/sagemaker-data-wrangler-and-feature-store.md`](../../../services/machine-learning-ai/sagemaker-data-wrangler-and-feature-store.md)
and the Domain 1 README's [training/serving skew scenario](../domain-1-data-preparation/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A:** Retraining more often doesn't fix a code-path mismatch between training and serving —
  the next retrain would reproduce the same skew.
- **C:** More training data addresses underfitting/overfitting style generalization problems,
  not a feature-computation inconsistency between environments.
- **D:** This is a mismatch-of-inputs problem, not a bias-variance/model-complexity problem;
  simplifying the algorithm does nothing about two different feature pipelines disagreeing.

---

## Q3

A data science team wants a no-code, visual way to explore a tabular dataset, apply common
cleaning transforms, and get a built-in report flagging potential class imbalance or correlated
sensitive attributes before they start modeling. Which service best fits this need?

A) AWS Glue Jobs (Spark-based ETL)
B) Amazon Athena
C) SageMaker Data Wrangler
D) Amazon EMR

**Correct Answer: C**

**Explanation:** **SageMaker Data Wrangler** is purpose-built for this: a visual, no-code UI for
exploring and transforming data specifically for ML, with built-in data-quality and bias reports
(e.g., class imbalance, correlated sensitive attributes) generated with a few clicks. See
[`services/machine-learning-ai/sagemaker-data-wrangler-and-feature-store.md`](../../../services/machine-learning-ai/sagemaker-data-wrangler-and-feature-store.md).

**Why the others are wrong:**
- **A:** Glue Jobs are code/Spark-driven ETL — powerful for large-scale transforms but not
  no-code, and they have no built-in ML bias reporting.
- **B:** Athena is a serverless SQL query engine for data already in S3; it doesn't offer visual
  cleaning transforms or ML-specific bias detection.
- **D:** EMR is a managed big-data cluster (Spark/Hadoop/Hive) for large-scale code-driven
  processing — not a no-code visual tool, and has no built-in bias-report feature.

---

## Q4 (Choose TWO)

A binary classification training dataset has 97% of samples in the "normal" class and 3% in the
"anomaly" class. The trained model currently predicts "normal" for almost every input. Which TWO
actions would directly help address this class imbalance problem during data preparation?

A) Oversample the minority ("anomaly") class or apply SMOTE-style synthetic augmentation
B) Apply class weighting so misclassifying the minority class is penalized more heavily during training
C) Increase the number of training epochs
D) Decrease the learning rate
E) Reduce the size of the validation set

**Correct Answer: A and B**

**Explanation:** Class imbalance is a **data preparation** problem (Domain 1, task statement
1.3), and the standard fixes are to rebalance the data the model sees — either by **resampling**
(oversampling the minority class, undersampling the majority class, or SMOTE-style synthetic
minority oversampling) or by **class weighting**, which tells the training algorithm to treat
errors on the rare class as more costly, without changing the physical dataset. Both are
legitimate, commonly combined approaches. See the Domain 1 README's
["95%/5% class imbalance" scenario](../domain-1-data-preparation/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **C:** More epochs just means the model sees the same imbalanced data more times — it
  reinforces the existing imbalance rather than fixing it, and can increase overfitting to the
  majority class.
- **D:** Learning rate is a training hyperparameter affecting how fast the model converges; it
  has no mechanism for correcting a data distribution imbalance.
- **E:** Shrinking the validation set only makes evaluation less reliable — it does nothing to
  the imbalance in the training data and the model's learned bias toward the majority class.

---

## Q5

Raw data for an ML project arrives from several systems and lands in different S3 prefixes.
Several teams need Athena and SageMaker to query this data with a consistent, discoverable
schema, without manually defining table structures in each service. What should they set up?

A) An AWS Glue Crawler that scans the S3 prefixes and populates the AWS Glue Data Catalog
B) A separate Amazon RDS database per team, loaded via manual INSERT scripts
C) A SageMaker Data Wrangler flow re-run manually before every query
D) An Amazon Kinesis Data Firehose delivery stream pointed at each prefix

**Correct Answer: A**

**Explanation:** A **Glue Crawler** scans data in S3, infers schema (column names, types,
partitions), and writes that metadata into the **Glue Data Catalog** — a single, shared schema
registry that Athena, Redshift Spectrum, and SageMaker can all read from, so nobody has to define
or maintain the schema separately in each consuming service. See
[`services/analytics/glue.md`](../../../services/analytics/glue.md) and
[`services/analytics/data-lake-concepts.md`](../../../services/analytics/data-lake-concepts.md).

**Why the others are wrong:**
- **B:** Per-team RDS databases with manual inserts creates duplicated, inconsistent copies of
  data and does not solve "one consistent schema discoverable by Athena/SageMaker" — it actively
  works against it.
- **C:** Data Wrangler is for interactive data prep/transformation, not for publishing a shared,
  queryable schema catalog, and manually re-running it before every query isn't how schema
  discovery works.
- **D:** Firehose delivers streaming data into a destination (like S3) — it doesn't scan
  existing S3 data or populate a schema catalog.

---

## Q6

A company wants its customer-support chatbot to answer questions using its internal product
documentation, which is updated weekly. They want answers grounded in the current docs and need
the model to cite which document it used. Which approach best satisfies these requirements?

A) Retrain a foundation model from scratch every week on the latest documentation
B) Fine-tune a foundation model monthly on the documentation set
C) Use Retrieval-Augmented Generation (RAG): embed the documents into a vector store and retrieve relevant chunks at query time
D) Paste the entire documentation set into every prompt sent to the model

**Correct Answer: C**

**Explanation:** **RAG** is designed exactly for this: frequently changing source material plus
a need for traceability/citations. Chunking and embedding the documents into a vector store
(e.g., Bedrock Knowledge Bases or OpenSearch) lets the system retrieve just the relevant pieces
at query time and hand them to the foundation model as grounding context — and because you know
exactly which chunk was retrieved, you can cite the source. See
[`embeddings-and-rag-data-prep.md`](../domain-1-data-preparation/embeddings-and-rag-data-prep.md).

**Why the others are wrong:**
- **A:** Retraining a foundation model from scratch weekly is enormously expensive and slow —
  completely impractical compared to RAG's retrieval step.
- **B:** Fine-tuning changes model *behavior* (tone, format, new skills); it does not reliably
  inject frequently changing facts and gives no natural way to cite the specific source document
  for a given answer.
- **D:** Pasting the entire documentation set into every prompt doesn't scale — most of a large
  document is irrelevant to any one question, and it will eventually exceed the model's context
  window and cost far more per query than retrieving only relevant chunks.

---

## Q7

An engineering team is preparing documents for a RAG pipeline. They choose a chunk size of
4,000 tokens per chunk (an entire multi-topic document per chunk) to minimize the number of
chunks stored. After launch, the chatbot frequently returns answers that blend unrelated topics
and miss the specific detail the user asked about. What is the most likely cause?

A) The embedding model dimensionality is too low
B) Chunks are too large, so each chunk's embedding represents an average of many unrelated ideas, diluting relevance
C) The vector store's similarity search algorithm is misconfigured
D) The foundation model used for generation is undersized

**Correct Answer: B**

**Explanation:** Chunk size is a real design decision in RAG data preparation: chunks that are
too large mix multiple topics into one embedding, so the resulting vector represents a vague
"average" of ideas rather than one focused concept — this makes retrieval less precise, exactly
the symptom described (blended, unfocused answers). The fix is smaller, more topically-focused
chunks (sentence/paragraph-based or semantic chunking), typically with some overlap between
chunks. See [`embeddings-and-rag-data-prep.md`](../domain-1-data-preparation/embeddings-and-rag-data-prep.md#key-features--components).

**Why the others are wrong:**
- **A:** Embedding dimensionality affects how much nuance a vector can capture overall, but the
  specific symptom of "blended unrelated topics" is a chunking-granularity problem, not a
  dimensionality problem.
- **C:** A misconfigured similarity search would typically return clearly irrelevant results
  entirely, not specifically "multi-topic blended" answers — the chunk content itself is the
  issue here.
- **D:** The foundation model only generates from whatever context it's given; if the retrieved
  chunk itself is a muddled multi-topic blob, a bigger model can't fix bad retrieval input.

---

## Q8

A RAG pipeline indexes company documents using the Amazon Titan Embeddings model. Later, an
engineer updates the query-time embedding step to use a different third-party embedding model
for incoming user questions, believing it's a drop-in improvement. After this change, retrieval
quality collapses. What is the most likely explanation?

A) The vector store ran out of storage capacity
B) Different embedding models produce vectors in different, non-comparable numeric spaces, so similarity search between a Titan-embedded document and a differently-embedded query is meaningless
C) The chunk size was too small
D) The foundation model's context window shrank

**Correct Answer: B**

**Explanation:** Embeddings are only comparable when produced by the **same embedding model**
used consistently for both the indexed documents and the incoming queries — each model maps
text into its own learned vector space, and "closeness" between a Titan-embedded vector and a
vector from an unrelated model carries no meaningful signal. This is explicitly flagged as a
common wrong-answer trap in
[`embeddings-and-rag-data-prep.md`](../domain-1-data-preparation/embeddings-and-rag-data-prep.md#exam-tips) —
know that the same embedding model must embed both stored chunks and queries.

**Why the others are wrong:**
- **A:** Running out of storage would cause write failures or missing data, not degraded
  relevance across all queries.
- **C:** Chunk size affects relevance granularity, but wouldn't cause a total retrieval
  collapse the way an incompatible embedding space would — and chunk size wasn't changed here.
- **D:** The foundation model's context window is about how much text it can accept per prompt;
  it has nothing to do with the retrieval step failing before generation even starts.

---

## Q9 (Choose TWO)

A healthcare ML team must ensure that personally identifiable information (PII) is discovered
and removed from a large S3 data lake before any of it is used in a training job. Which TWO
services/approaches should be part of this pipeline?

A) Amazon Macie to automatically discover and classify sensitive data (including PII) in S3
B) AWS Glue or Glue DataBrew transforms to redact/remove the identified PII fields before writing to the curated zone
C) SageMaker Model Monitor to flag PII after the model is already deployed
D) Increasing the model's regularization strength
E) SageMaker Automatic Model Tuning with a wider hyperparameter search range

**Correct Answer: A and B**

**Explanation:** PII handling belongs in the **data preparation** stage, before training ever
happens. **Amazon Macie** uses machine learning and pattern matching to discover and classify
sensitive data (SSNs, names, financial data) across S3; once identified, **Glue/Glue DataBrew**
transforms apply the actual redaction/removal, producing a clean curated dataset. This matches
the Domain 1 README's
["PII must be removed before data reaches a training job" scenario](../domain-1-data-preparation/README.md#common-exam-scenarios).
See [`services/security-identity-compliance/macie.md`](../../../services/security-identity-compliance/macie.md)
and [`services/analytics/glue.md`](../../../services/analytics/glue.md).

**Why the others are wrong:**
- **C:** Model Monitor watches a *live, deployed* model's input/output statistics for drift — by
  the time it could flag anything, the model has already been trained on (and may have memorized)
  the PII; this is far too late in the pipeline.
- **D:** Regularization strength is a training hyperparameter that affects overfitting — it has
  no relationship to detecting or removing PII from source data.
- **E:** Hyperparameter tuning searches for the best model configuration; it has nothing to do
  with discovering or redacting sensitive data before training.

---

## Q10

A data lake ingests files from an upstream system that periodically adds new columns without
notice. Downstream Athena queries and SageMaker Processing jobs that rely on a fixed, hardcoded
schema keep breaking whenever this happens. What is the best fix?

A) Hardcode the new schema into every consuming job each time a change is detected
B) Schedule the Glue Crawler to re-run periodically so the Glue Data Catalog's schema evolves automatically, and have consumers read schema from the Catalog instead of hardcoding it
C) Switch from S3 to Amazon RDS to enforce a rigid, unchanging schema
D) Disable schema validation entirely in all downstream jobs

**Correct Answer: B**

**Explanation:** Re-running the **Glue Crawler** on a schedule keeps the **Glue Data Catalog**
in sync with the data's actual (evolving) structure, and consumers that read schema from the
Catalog (rather than hardcoding it) automatically pick up new columns without manual
intervention. This matches the Domain 1 README's
["schema changes over time" scenario](../domain-1-data-preparation/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A:** Manually hardcoding the schema every time it changes is exactly the brittle,
  high-maintenance process the question describes as already failing — it doesn't scale.
- **C:** Switching to RDS doesn't inherently solve schema evolution (RDS schemas also need
  explicit ALTER TABLE changes), and abandoning a data-lake architecture is a disproportionate,
  unnecessary response to a cataloging problem.
- **D:** Disabling schema validation would stop the breaking errors but at the cost of silently
  processing data incorrectly — it hides the symptom without giving consumers correct schema
  information.

---

## Q11

A distributed deep learning training job needs extremely high-throughput, low-latency,
POSIX-compliant file access to a very large training dataset across many GPU instances
simultaneously. Which storage option is best suited for this phase of the pipeline?

A) Amazon S3 Standard accessed directly by every training instance
B) Amazon FSx for Lustre, linked to the S3 data for high-throughput, low-latency parallel file access during training
C) Amazon Glacier Deep Archive
D) A single Amazon EBS volume shared across all training instances

**Correct Answer: B**

**Explanation:** **Amazon FSx for Lustre** is a high-performance, POSIX-compliant parallel file
system designed for workloads needing very high throughput and low latency across many compute
nodes at once — exactly the profile of large-scale distributed training. It can be linked to an
S3 bucket so files appear instantly without a separate copy step. See the Domain 1 README's
notes on [storage layer selection](../domain-1-data-preparation/README.md#task-statement-level-content-from-the-official-exam-guide).

**Why the others are wrong:**
- **A:** S3 is excellent for durable, cost-effective object storage and is fine for many training
  jobs, but it is not a POSIX file system and doesn't offer the same low-latency, high-throughput
  parallel file access that FSx for Lustre provides for the most demanding distributed-training
  cases.
- **C:** Glacier Deep Archive is for long-term, rarely-accessed cold storage with retrieval times
  measured in hours — the opposite of what a live training job needs.
- **D:** A single EBS volume is attached to one instance at a time (or has limited multi-attach
  support) and isn't designed for high-throughput concurrent access from many distributed
  training nodes simultaneously.

---

## Q12

A dataset for a linear regression model has one numeric feature ("annual income," ranging from
$10,000 to $500,000) and one categorical feature ("region," with 5 possible values). Which
feature engineering steps are most appropriate before training?

A) Leave both features as-is; linear models handle raw text and unscaled numbers automatically
B) Normalize/standardize the numeric income feature, and one-hot encode the categorical region feature
C) One-hot encode the income feature and normalize the region feature
D) Discard the region feature since categorical data cannot be used in ML models

**Correct Answer: B**

**Explanation:** Numeric features with wide ranges typically need to be **normalized or
standardized** (scaled to a common range) so that no single feature dominates the model purely
because of its raw magnitude, and **categorical features** need to be converted into a numeric
representation — **one-hot encoding** creates a binary column per category — before most
algorithms (including linear models) can use them. See the Domain 1 README's description of
transformation/feature engineering ([task statement 1.2](../domain-1-data-preparation/README.md#task-statement-level-content-from-the-official-exam-guide))
and [`services/analytics/glue.md`](../../../services/analytics/glue.md).

**Why the others are wrong:**
- **A:** Linear models (and most ML algorithms) expect numeric input and are sensitive to
  feature scale; raw categorical text can't be consumed directly, and unscaled numeric ranges
  can bias the model toward the feature with the largest raw magnitude.
- **C:** This swaps the correct transform for each feature type — one-hot encoding a continuous
  numeric feature would nonsensically create a separate column per unique income value, and
  "normalizing" a categorical label has no defined meaning.
- **D:** Categorical features are routinely used in ML via encoding techniques (one-hot, ordinal,
  target encoding); discarding useful information like "region" is unnecessary and likely hurts
  model performance.

---

## Q13

An image classification model is being trained on a small dataset of only 500 labeled images
per class. The model achieves near-perfect training accuracy but performs poorly on new images.
Which data-preparation technique would most directly help, independent of changing the model
architecture?

A) Convert all images to grayscale to reduce file size
B) Apply data augmentation (random rotations, flips, crops, brightness changes) to synthetically expand the effective training set
C) Reduce the number of training epochs to zero
D) Remove 80% of the training images to simplify the dataset

**Correct Answer: B**

**Explanation:** A small dataset combined with near-perfect training accuracy but poor
generalization is a classic **overfitting** signature caused by insufficient data diversity.
**Data augmentation** — generating varied versions of existing images through transformations
like rotation, flipping, cropping, and brightness adjustment — synthetically increases the
effective diversity of the training set, which is a core Domain 1 technique (alongside
splitting/shuffling) for improving data quality before modeling. See the Domain 1 README's
section on [data integrity and preparing for modeling](../domain-1-data-preparation/README.md#task-statement-level-content-from-the-official-exam-guide).

**Why the others are wrong:**
- **A:** Converting to grayscale discards color information (potentially useful signal) and does
  nothing to address the lack of training example diversity causing overfitting.
- **C:** Training for zero epochs means the model learns nothing at all — this doesn't address
  overfitting, it just produces an untrained model.
- **D:** Removing most of the training data would make the dataset even smaller, almost
  certainly worsening overfitting rather than helping it.

---

## Q14 (Choose TWO)

A team is designing a RAG pipeline and wants to minimize the amount of custom integration code
they have to write and maintain, while still being able to filter retrieved chunks by metadata
such as department and document date. Which TWO statements about their vector store options are
correct?

A) Amazon Bedrock Knowledge Bases is a managed service that bundles chunking, embedding, vector storage, and retrieval into one workflow, reducing custom integration work
B) Most vector stores (including Bedrock Knowledge Bases) support attaching metadata to chunks and filtering similarity search results by it, which is important for access control and relevance
C) Vector stores only support exact-match keyword search, not semantic similarity search
D) A vector store is required even if the entire knowledge base easily fits inside a single prompt
E) Embedding dimensionality has no effect on storage cost or compute cost

**Correct Answer: A and B**

**Explanation:** **Bedrock Knowledge Bases** is AWS's fully managed end-to-end RAG pipeline —
point it at an S3 data source and it handles chunking, embedding, vector storage, and retrieval,
minimizing custom glue code compared to wiring together S3 + an embedding model + OpenSearch
manually. Most vector stores also support **metadata filtering** (e.g., `department: HR`,
`date: 2026`), which is critical for scoping a search to the right subset of documents and for
preventing one user's query from retrieving another user's private data. See
[`embeddings-and-rag-data-prep.md`](../domain-1-data-preparation/embeddings-and-rag-data-prep.md#key-features--components)
and [`services/analytics/opensearch.md`](../../../services/analytics/opensearch.md).

**Why the others are wrong:**
- **C:** This is backwards — vector stores are specifically built for **semantic similarity
  search** (finding meaning-related content via nearest-neighbor search over embeddings), not
  exact-match keyword search; exact-match lookups belong in a regular database.
- **D:** If the entire knowledge base is small enough to fit directly in a prompt, a vector store
  adds unnecessary complexity with no benefit — the Domain 1 doc explicitly calls this out as a
  case to skip RAG's retrieval infrastructure.
- **E:** Higher embedding dimensionality captures more nuance but does increase both storage
  footprint and the compute cost of each similarity comparison — it's a real cost/accuracy
  tradeoff, not a free dimension to maximize.
