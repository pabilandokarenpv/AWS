# Domain 3 Practice Questions — Deployment and Orchestration of ML and AI Workflows (24%)

12 questions covering task statements 3.1–3.4: deployment infrastructure selection,
containerization, CI/CD automation, and GenAI workflow orchestration. See the
[Domain 3 README](../domain-3-deployment-orchestration/README.md) for the full map.

---

## Q1

An application needs predictions back within milliseconds, continuously, around the clock, with
traffic volume that is unpredictable but never drops to zero. Which SageMaker deployment option
fits best?

A) Batch transform
B) A real-time inference endpoint with Auto Scaling
C) Asynchronous inference
D) SageMaker Neo compiled edge inference

**Correct Answer: B**

**Explanation:** Continuous, unpredictable, always-present traffic requiring millisecond
latency is exactly what a **real-time endpoint** is for — an always-on, provisioned endpoint
that responds synchronously, paired with **Auto Scaling** so capacity adjusts to the
unpredictable volume without over- or under-provisioning. See
[`services/machine-learning-ai/sagemaker-deployment-endpoints.md`](../../../services/machine-learning-ai/sagemaker-deployment-endpoints.md)
and the Domain 3 README's [real-time endpoint scenario](../domain-3-deployment-orchestration/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A:** Batch transform scores an entire static dataset at once with no persistent endpoint —
  incompatible with continuous, always-on, millisecond-latency live traffic.
- **C:** Asynchronous inference is for large payloads/long processing where the caller can wait;
  it doesn't guarantee millisecond response times for continuous live traffic.
- **D:** SageMaker Neo compiles a model for edge hardware without a live cloud endpoint — not
  relevant when the architecture clearly needs a continuously-available cloud endpoint.

---

## Q2

A model processes large PDF documents (sometimes hundreds of pages) submitted by users, and the
application design allows the user to receive the result a few minutes later rather than
instantly. Which deployment option is most appropriate?

A) A real-time endpoint sized for the largest possible payload
B) Asynchronous inference endpoint
C) Batch transform run once per day on a fixed schedule
D) A serverless endpoint with a 1-second timeout

**Correct Answer: B**

**Explanation:** **Asynchronous inference** endpoints are built for exactly this pattern: large
payloads and/or longer processing times where the caller doesn't need an instant synchronous
response — the request is queued, processed, and the result retrieved afterward, without having
to provision for worst-case latency on every request. See
[`services/machine-learning-ai/sagemaker-deployment-endpoints.md`](../../../services/machine-learning-ai/sagemaker-deployment-endpoints.md)
and the Domain 3 README's [large-PDF scenario](../domain-3-deployment-orchestration/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A:** A real-time endpoint provisioned for worst-case large payloads wastes capacity most of
  the time and still isn't designed for long-running, large-document processing the way
  asynchronous inference is.
- **C:** Batch transform scores a bulk, static dataset on a schedule; it's not designed for
  on-demand, per-user document submissions that need an individual result returned per request.
- **D:** A serverless endpoint with a 1-second timeout is the opposite of what's needed for
  potentially long document processing — it would fail on exactly the large documents described.

---

## Q3

A team needs to score an entire 10 TB historical dataset once, with no live traffic involved,
and wants to minimize cost since there's no need for a persistent endpoint afterward.

A) Real-time endpoint scaled to zero when idle
B) Asynchronous inference endpoint
C) Batch transform
D) Serverless inference endpoint

**Correct Answer: C**

**Explanation:** **Batch transform** scores an entire dataset in one job with no persistent
endpoint kept running afterward — it's the most cost-efficient option for a one-time, large-scale
scoring job with no live-traffic requirement. See
[`services/machine-learning-ai/sagemaker-deployment-endpoints.md`](../../../services/machine-learning-ai/sagemaker-deployment-endpoints.md)
and the Domain 3 README's [10TB scoring scenario](../domain-3-deployment-orchestration/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A:** Real-time endpoints are not designed to "scale to zero" in the way serverless is, and
  maintaining any persistent endpoint for a single one-time batch job is unnecessary overhead.
- **B:** Asynchronous inference is designed around individual queued requests with a response
  retrieval step, not bulk scoring of an entire static dataset as one job.
- **D:** Serverless inference is optimized for sporadic, per-request invocation patterns with
  cold starts — not the most cost-efficient shape for scoring one enormous dataset in bulk.

---

## Q4

Traffic to an endpoint is zero for hours at a time, then spikes unpredictably. A few seconds of
cold-start latency on the first request after idle periods is acceptable to the business. Which
deployment option minimizes cost for this pattern?

A) Real-time endpoint with a fixed minimum instance count
B) Serverless inference endpoint
C) Batch transform run hourly
D) SageMaker Neo on a dedicated edge device

**Correct Answer: B**

**Explanation:** **Serverless inference** endpoints scale down to zero during idle periods
(so you pay nothing when there's no traffic) and scale up automatically when requests arrive,
accepting a few seconds of cold-start latency in exchange — exactly matching a bursty,
zero-for-hours-then-spikes traffic pattern where cold start is tolerable. See
[`services/machine-learning-ai/sagemaker-deployment-endpoints.md`](../../../services/machine-learning-ai/sagemaker-deployment-endpoints.md)
and the Domain 3 README's [bursty-traffic scenario](../domain-3-deployment-orchestration/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A:** A real-time endpoint with a fixed minimum instance count keeps paying for provisioned
  capacity even during the hours of zero traffic — directly contradicting the cost-minimization
  goal.
- **C:** Hourly batch transform runs introduce delay (results only ready at the next scheduled
  run) and don't match a live, on-demand request pattern with spikes at unpredictable times.
- **D:** SageMaker Neo targets edge/local inference hardware, not a cloud traffic-pattern cost
  problem — it's solving a different deployment challenge entirely.

---

## Q5 (Choose TWO)

A team is about to deploy a new model version and wants to minimize the risk of a bad deployment
affecting all production traffic at once, while also being able to roll back quickly if problems
appear. Which TWO deployment strategies directly address this?

A) Blue/green deployment, standing up the new version fully while keeping the old version briefly available for instant rollback
B) Canary deployment, routing a small percentage of real traffic to the new version first before ramping up
C) An in-place update that immediately replaces 100% of traffic with the new version with no rollback path
D) Disabling Auto Scaling during the deployment window
E) Deleting the old model artifact immediately after deploying the new one

**Correct Answer: A and B**

**Explanation:** **Blue/green** and **canary** are the two standard low-risk deployment
strategies: blue/green keeps the previous version standing by so a rollback is immediate if the
new version misbehaves, and canary limits exposure by sending only a small slice of real traffic
to the new version first, ramping up only if it performs well. Both exist specifically to avoid
an instant, all-or-nothing cutover. See the Domain 3 README's
["rollback instantly" and "limit exposure" scenarios](../domain-3-deployment-orchestration/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **C:** An in-place, no-rollback-path cutover is precisely the risky pattern blue/green and
  canary exist to avoid — it's the wrong-answer baseline, not a mitigation.
- **D:** Disabling Auto Scaling during a deployment doesn't reduce the risk of a bad model
  version serving traffic; it could instead cause capacity problems unrelated to deployment
  safety.
- **E:** Deleting the old model artifact immediately removes your rollback option entirely —
  it's the opposite of what either blue/green or canary deployments are designed to preserve.

---

## Q6

New labeled training data lands in an S3 bucket every day, and the team wants the model to
retrain automatically whenever this happens, without a human manually kicking off the process.
What should they configure?

A) A human must log in daily and manually start a new SageMaker training job
B) An Amazon EventBridge rule that triggers the SageMaker Pipeline when the S3 "new object" event fires
C) A fixed CloudWatch alarm that pages an on-call engineer to restart training weekly
D) Store the data in DynamoDB instead of S3 so training starts automatically

**Correct Answer: B**

**Explanation:** **EventBridge** is AWS's event bus for "when X happens, trigger Y" — an
EventBridge rule watching for new S3 objects in the designated prefix can automatically start
the **SageMaker Pipeline** (process → train → evaluate → register), fully automating retraining
without manual intervention. See
[`services/machine-learning-ai/sagemaker-pipelines.md`](../../../services/machine-learning-ai/sagemaker-pipelines.md)
and the Domain 3 README's [automatic retraining scenario](../domain-3-deployment-orchestration/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A:** Manual daily logins directly contradict the stated requirement ("without a human
  manually kicking it off") — it's a process, not an automation.
- **C:** A weekly alarm that pages a human to restart training is neither automatic (a human
  still has to act) nor responsive to the actual daily data-arrival event — it's on the wrong
  schedule and still manual.
- **D:** Simply switching storage services (S3 to DynamoDB) does nothing by itself to trigger a
  training pipeline; it's the event-driven trigger (EventBridge) that provides automation, not
  the choice of storage backend.

---

## Q7

A factory needs to run inference on sensor data using a local edge gateway device with no
reliable connection back to AWS. Which service compiles the trained model for this target
hardware so inference can run locally without a live endpoint call?

A) Amazon API Gateway
B) SageMaker Neo
C) AWS Direct Connect
D) Amazon CloudFront

**Correct Answer: B**

**Explanation:** **SageMaker Neo** compiles a trained model to run efficiently on specific
target hardware (including edge devices), enabling local inference with no dependency on a live
network call back to a cloud-hosted endpoint — exactly suited for unreliable-connectivity edge
scenarios. See the Domain 3 README's [edge inference scenario](../domain-3-deployment-orchestration/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A:** API Gateway manages and routes API requests to backend services over a network — it
  requires connectivity and doesn't solve "run inference locally with no reliable connection."
- **C:** Direct Connect provides a dedicated, more reliable network link between on-premises
  infrastructure and AWS — it still requires a working connection and is the opposite approach
  of running fully disconnected local inference.
- **D:** CloudFront is a content delivery network (CDN) for caching and distributing web
  content/API responses — it's unrelated to compiling an ML model for offline edge inference.

---

## Q8 (Choose TWO)

A team is building a CI/CD pipeline for ML. Which TWO statements correctly describe the roles of
AWS services commonly used in this pipeline?

A) AWS CodeBuild compiles/tests code and builds the container image that training or inference will run
B) A SageMaker Pipeline defines a repeatable, versioned DAG of ML-specific steps (process data → train → evaluate → conditionally register/deploy)
C) AWS Glue DataBrew is the standard tool for orchestrating blue/green endpoint cutovers
D) SageMaker Clarify triggers container image builds whenever new code is committed
E) Amazon ECR is used exclusively for storing structured relational database tables

**Correct Answer: A and B**

**Explanation:** **CodeBuild** handles the compile/test/build step, producing the container
image used downstream, while a **SageMaker Pipeline** is the ML-specific CI/CD orchestrator: a
versioned, repeatable DAG that chains process data → train → evaluate → conditionally register/
deploy, halting automatically if a model doesn't clear the quality bar. See
[`services/machine-learning-ai/sagemaker-pipelines.md`](../../../services/machine-learning-ai/sagemaker-pipelines.md)
and the Domain 3 README's [CI/CD walkthrough](../domain-3-deployment-orchestration/README.md#how-it-works--full-mlops-cicd-with-sagemaker-pipelines).

**Why the others are wrong:**
- **C:** Glue DataBrew is a visual data-cleaning tool for ML data preparation (Domain 1); it has
  no role in orchestrating endpoint deployment cutovers, which is handled by CodeDeploy with
  blue/green or canary strategies.
- **D:** SageMaker Clarify produces bias and explainability reports (Domain 4) — it does not
  trigger container builds; that's CodeBuild's role, typically kicked off by CodePipeline.
- **E:** Amazon ECR stores container images (for training/inference containers), not relational
  database tables — that description applies to a service like RDS, not ECR.

---

## Q9

A team has built a custom inference container with specific Python library versions not
available in any SageMaker built-in image. Where should this custom container image be stored so
SageMaker, ECS, or EKS can pull it for deployment?

A) Amazon S3, as a compressed zip file
B) Amazon Elastic Container Registry (ECR)
C) AWS Systems Manager Parameter Store
D) Amazon CloudWatch Logs

**Correct Answer: B**

**Explanation:** **Amazon ECR** is purpose-built for storing and versioning container images
(via tags), which SageMaker, ECS, and EKS can all pull directly when launching training jobs or
serving containers — the standard location for any custom "Bring Your Own Container" image. See
[`services/containers/ecr.md`](../../../services/containers/ecr.md) and the Domain 3 README's
[containerization section](../domain-3-deployment-orchestration/README.md#linked-service-docs--the-deep-dives).

**Why the others are wrong:**
- **A:** While container images are technically layered filesystems, S3 is not how
  SageMaker/ECS/EKS expect to pull container images — they expect an OCI/Docker-compatible
  registry like ECR, not a generic zip file in object storage.
- **C:** Parameter Store is for storing configuration values and secrets, not multi-gigabyte
  container images.
- **D:** CloudWatch Logs stores log output from running services; it has no capability to store
  or serve container images at all.

---

## Q10

A SageMaker Pipeline includes a step that compares a newly trained model's evaluation metrics
against a defined quality threshold before the model can proceed to registration. What is the
purpose of this design?

A) To intentionally slow down the pipeline for no functional reason
B) To prevent an automated pipeline from promoting a worse-performing model into production without anyone noticing
C) To reduce the storage cost of the Model Registry
D) To satisfy a requirement that every pipeline must have exactly 5 steps

**Correct Answer: B**

**Explanation:** The evaluation-threshold check is a genuine fork in the automated pipeline: if
the new model doesn't clear the bar, the **SageMaker Pipeline** halts and alerts instead of
quietly registering/deploying a regression — ensuring automation doesn't silently degrade
production quality. See the Domain 3 README's
[CI/CD walkthrough step 5](../domain-3-deployment-orchestration/README.md#how-it-works--full-mlops-cicd-with-sagemaker-pipelines).

**Why the others are wrong:**
- **A:** The check has a concrete functional purpose (quality gating); it isn't arbitrary
  friction.
- **C:** The evaluation step is about model quality control, not about Model Registry storage
  costs, which aren't meaningfully affected by this check.
- **D:** There's no fixed requirement that pipelines have exactly 5 steps; a pipeline's step
  count depends entirely on the actual process being automated.

---

## Q11

A company wants to deploy a RAG-based chatbot where document chunking, embedding, vector
storage, and retrieval are all handled by a single managed AWS component they can point directly
at an S3 data source, rather than hand-wiring separate services together. Which component should
they orchestrate as part of their deployment?

A) Amazon Bedrock Knowledge Bases
B) AWS Direct Connect
C) Amazon CloudFront
D) AWS Certificate Manager

**Correct Answer: A**

**Explanation:** **Bedrock Knowledge Bases** is the managed, deployable RAG component referenced
by Domain 3's GenAI orchestration task statement (3.4): it bundles chunking, embedding, vector
storage, and retrieval into a single pointed-at-S3 workflow, exposing a simple "ask a question,
get a grounded, cited answer" API — avoiding manual integration of separate services. See
[`services/machine-learning-ai/bedrock.md`](../../../services/machine-learning-ai/bedrock.md)
and [`embeddings-and-rag-data-prep.md`](../domain-1-data-preparation/embeddings-and-rag-data-prep.md#key-features--components).

**Why the others are wrong:**
- **B:** Direct Connect provides a dedicated network link between on-premises infrastructure and
  AWS — unrelated to RAG orchestration.
- **C:** CloudFront is a content delivery network for caching/distributing content globally; it
  plays no role in chunking, embedding, or retrieval.
- **D:** Certificate Manager issues and manages TLS/SSL certificates — unrelated to GenAI
  workflow orchestration.

---

## Q12

A GenAI application needs to answer a multi-step customer request that requires calling an
internal order-status API, then a refund-processing API, chaining the results together with
reasoning in between — not just answering from static retrieved documents. Which Bedrock
component is designed for this kind of multi-step, tool-using orchestration?

A) Bedrock Titan Embeddings
B) Bedrock Agents
C) Bedrock Guardrails
D) Bedrock Knowledge Bases alone, with no other components

**Correct Answer: B**

**Explanation:** **Bedrock Agents** are designed for multi-step, tool-using GenAI workflows: an
agent can call external APIs/tools, chain reasoning steps, and orchestrate a sequence of actions
to fulfill a complex request — the GenAI analog to a SageMaker Pipeline's step-by-step
orchestration, referenced directly in Domain 3's task statement 3.4. See
[`services/machine-learning-ai/bedrock.md`](../../../services/machine-learning-ai/bedrock.md)
and the Domain 3 README's [GenAI orchestration section](../domain-3-deployment-orchestration/README.md#linked-service-docs--the-deep-dives).

**Why the others are wrong:**
- **A:** Titan Embeddings converts text into vectors for similarity search — it has no tool-
  calling or multi-step reasoning capability of its own.
- **C:** Guardrails filter/block disallowed input and output content for safety — they don't
  orchestrate calling external APIs or chaining reasoning steps.
- **D:** Knowledge Bases alone only retrieves and grounds answers in static documents; by itself
  it cannot call external order-status/refund APIs or chain multi-step actions the way an Agent
  can (Agents and Knowledge Bases are often combined, but the orchestration capability described
  here specifically requires Agents).
