# Domain 4 Practice Questions — Operating, Monitoring, and Securing ML and AI Solutions (24%)

12 questions covering task statements 4.1–4.4: monitoring model/infrastructure health, cost
optimization, security, and responsible AI/GenAI guardrails. See the
[Domain 4 README](../domain-4-monitoring-security/README.md),
[`ml-cost-optimization.md`](../domain-4-monitoring-security/ml-cost-optimization.md), and
[`responsible-ai-and-guardrails.md`](../domain-4-monitoring-security/responsible-ai-and-guardrails.md).

---

## Q1

SageMaker Model Monitor reports that the statistical distribution of a deployed model's input
features has shifted noticeably compared to training time, but it's not yet clear whether
prediction accuracy has actually dropped. What is this phenomenon called?

A) Concept drift
B) Data drift
C) Overfitting
D) Model parallelism

**Correct Answer: B**

**Explanation:** **Data drift** means the *inputs* look statistically different now than during
training (e.g., a new customer segment shifting the age distribution) — the model may still be
making reasonable predictions, but it's now operating outside the data it was validated on. Model
Monitor detects this by comparing live input statistics against a training-time baseline. See
[`services/machine-learning-ai/sagemaker-model-monitor-and-registry.md`](../../../services/machine-learning-ai/sagemaker-model-monitor-and-registry.md)
and the Domain 4 README's [data drift scenario](../domain-4-monitoring-security/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A:** Concept drift specifically means the *relationship* between inputs and the correct
  output has changed (detected via fresh labeled ground truth), not just that input statistics
  shifted — the question explicitly says accuracy impact isn't yet confirmed, pointing to data
  drift instead.
- **C:** Overfitting is a training-time model-fit problem (train vs. validation gap), unrelated
  to live input distribution shifts after deployment.
- **D:** Model parallelism is a distributed-training technique for splitting a model across GPUs
  — entirely unrelated to drift monitoring.

---

## Q2

A fraud model's accuracy on freshly labeled ground-truth samples has been steadily falling, even
though the statistical shape of incoming transactions looks similar to training time. A new
fraud pattern has emerged that the model wasn't trained to recognize. What is this phenomenon
called?

A) Data drift
B) Concept drift
C) Underfitting
D) Class imbalance

**Correct Answer: B**

**Explanation:** **Concept drift** means the relationship between inputs and the correct label
has changed — the same-looking inputs now warrant a different "correct" answer (a new fraud
pattern the model was never trained to recognize) — detected by periodically scoring the model
against fresh labeled ground truth rather than just watching input statistics. See
[`services/machine-learning-ai/sagemaker-model-monitor-and-registry.md`](../../../services/machine-learning-ai/sagemaker-model-monitor-and-registry.md)
and the Domain 4 README's [concept drift scenario](../domain-4-monitoring-security/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A:** Data drift is about the *input* statistics changing; the question explicitly states
  inputs look statistically similar — the problem is the input-to-label relationship, which is
  concept drift's definition.
- **C:** Underfitting is a training-time diagnosis (poor performance on both train and validation
  data at training time), not a post-deployment degradation over time.
- **D:** Class imbalance is a data-preparation-stage issue (disproportionate class
  representation), not the specific "world changed, model is now stale" phenomenon described.

---

## Q3

A team runs frequent SageMaker training jobs, each lasting a few hours, and the jobs checkpoint
progress so they can resume if interrupted. Minimizing training cost matters more than
guaranteeing an exact completion time. Which purchasing option should they use?

A) On-Demand instances
B) Managed Spot Training
C) A 3-year SageMaker Savings Plan
D) Reserved EC2 Instances for the training fleet

**Correct Answer: B**

**Explanation:** **Managed Spot Training** uses AWS's spare, unused EC2 capacity at a steep
discount (commonly cited up to ~90% off On-Demand), with SageMaker automatically handling
checkpoint/resume if the spare capacity is reclaimed — ideal for interruption-tolerant,
cost-sensitive training jobs. See
[`ml-cost-optimization.md`](../domain-4-monitoring-security/ml-cost-optimization.md) and the
Domain 4 README's [Spot Training scenario](../domain-4-monitoring-security/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A:** On-Demand guarantees the job won't be interrupted but costs significantly more — an
  unnecessary premium given the job explicitly tolerates interruption and cost minimization is
  the priority.
- **C:** SageMaker Savings Plans are built for steady, predictable, always-on usage (like an
  inference endpoint), not short-lived, intermittent training jobs — a 3-year commitment doesn't
  fit a bursty training workload.
- **D:** Reserved EC2 Instances are also designed for steady-state, long-running usage
  commitments, not temporary, bursty training jobs that come and go.

---

## Q4

A real-time inference endpoint runs 24/7 with steady, predictable traffic volume, and the team
wants the lowest sustained cost for this always-on usage. Which option is most appropriate?

A) Managed Spot Training applied to the endpoint
B) SageMaker Savings Plan, committing to a consistent usage level in exchange for a discount
C) On-Demand pricing with no commitment
D) Running the endpoint only during business hours to save money, accepting downtime

**Correct Answer: B**

**Explanation:** A **SageMaker Savings Plan** is a 1- or 3-year commitment to a consistent
amount of compute usage ($/hour) in exchange for a discount (AWS cites up to ~64% vs. On-Demand)
— ideal for steady, predictable, always-on endpoints, unlike Spot (not reliable for an always-on
production service). See
[`ml-cost-optimization.md`](../domain-4-monitoring-security/ml-cost-optimization.md) and the
Domain 4 README's [Savings Plan scenario](../domain-4-monitoring-security/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A:** Spot capacity can be reclaimed at any time — entirely unsuitable for an always-on,
  continuously-serving production endpoint that must stay up.
- **C:** On-Demand with no commitment is the most flexible but most expensive option; it doesn't
  capture the available discount for genuinely steady, predictable usage.
- **D:** Running the endpoint only during business hours introduces downtime and contradicts the
  stated requirement of 24/7 operation — this trades away the actual requirement rather than
  optimizing cost within it.

---

## Q5

Before launching a new SageMaker endpoint, a team is unsure which instance type and size will
meet their latency/throughput requirements at the lowest cost. What should they use to decide?

A) SageMaker Inference Recommender, which load-tests instance options and reports a cost/latency tradeoff
B) Guessing based on the largest available instance type to be safe
C) AWS Budgets
D) Amazon Macie

**Correct Answer: A**

**Explanation:** **SageMaker Inference Recommender** runs load tests across candidate instance
types/configurations and recommends the option that meets latency/throughput requirements at the
lowest cost, removing the guesswork from instance sizing before launch. See
[`ml-cost-optimization.md`](../domain-4-monitoring-security/ml-cost-optimization.md) and the
Domain 4 README's [instance-sizing scenario](../domain-4-monitoring-security/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **B:** Guessing the largest instance type "to be safe" wastes money on unnecessary capacity and
  isn't a measured, repeatable decision process — the opposite of what the scenario asks for.
- **C:** AWS Budgets tracks and alerts on spend after the fact; it doesn't recommend which
  instance type to use for a new workload before launch.
- **D:** Amazon Macie discovers and classifies sensitive data in S3 — entirely unrelated to
  inference instance sizing or cost/latency tradeoffs.

---

## Q6

A training job processes highly sensitive data and the security team requires that the job have
zero outbound or inbound internet access. How should this be configured?

A) Attach an internet gateway but restrict it with a security group
B) Run the training job inside a VPC using private subnets with no NAT gateway or internet gateway route
C) Disable IAM entirely for the training job's role
D) Use a public S3 bucket so the job can always reach its data

**Correct Answer: B**

**Explanation:** Running the training job inside a **VPC** using **private subnets** with no NAT
gateway or internet gateway route ensures there is no network path to or from the public
internet at all — the standard pattern for "must have zero internet access" requirements. See
[`services/networking-content-delivery/vpc.md`](../../../services/networking-content-delivery/vpc.md)
and the Domain 4 README's [zero-internet-access scenario](../domain-4-monitoring-security/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A:** Attaching an internet gateway, even with a restrictive security group, still creates a
  potential path to/from the internet at the network layer — the requirement is zero internet
  access, which an IGW presence contradicts regardless of security group rules.
- **C:** Disabling IAM entirely would remove access control altogether (a severe security
  regression) and has nothing to do with network-layer internet access — these are two different
  control planes.
- **D:** A public S3 bucket is explicitly the opposite of restricting access — it exposes
  sensitive data publicly rather than isolating the training job from the internet.

---

## Q7

A SageMaker training job's IAM role currently has `s3:*` permissions across the entire AWS
account's S3 resources. A security review flags this as a problem. What change aligns with best
practice?

A) Leave it as-is since training jobs need broad access to function
B) Scope the role down to only the specific S3 bucket(s)/prefixes the training job actually needs, following least privilege
C) Remove the IAM role entirely and run the job with root account credentials
D) Grant the role full administrator access instead, to simplify future changes

**Correct Answer: B**

**Explanation:** **IAM least privilege** means a role should only have permission to touch the
exact resources (e.g., specific S3 paths) it actually needs — nothing broader — which limits the
blast radius if credentials are ever compromised or the job is misconfigured. See
[`services/security-identity-compliance/iam.md`](../../../services/security-identity-compliance/iam.md)
and the Domain 4 README's [least-privilege description](../domain-4-monitoring-security/README.md#linked-service-docs--the-deep-dives).

**Why the others are wrong:**
- **A:** Broad `s3:*` account-wide access is precisely the anti-pattern least privilege exists
  to prevent — "it currently works" doesn't make overly broad permissions acceptable practice.
- **C:** Root account credentials have unrestricted access to the entire AWS account and should
  never be used for routine workloads like training jobs — this is a severe security
  anti-pattern, not a fix.
- **D:** Granting full administrator access makes the permissions problem dramatically worse,
  not better — the opposite direction from least privilege.

---

## Q8

Training data, model artifacts, and endpoint storage volumes all need to be protected so that
even if the underlying storage were somehow accessed improperly, the data would remain
unreadable without proper authorization. Which AWS service directly provides this protection?

A) AWS Budgets
B) AWS KMS (Key Management Service), encrypting data at rest
C) Amazon CloudWatch
D) AWS CodeBuild

**Correct Answer: B**

**Explanation:** **KMS** manages encryption keys used to encrypt data at rest (and supports
encryption in transit workflows) across S3 training data, model artifacts, and endpoint storage
volumes — ensuring that even improperly accessed raw storage remains unreadable without the
proper key and permissions. See
[`services/security-identity-compliance/kms.md`](../../../services/security-identity-compliance/kms.md)
and the Domain 4 README's [encryption description](../domain-4-monitoring-security/README.md#linked-service-docs--the-deep-dives).

**Why the others are wrong:**
- **A:** AWS Budgets tracks and alerts on cost; it has no role in data encryption.
- **C:** CloudWatch is for monitoring logs/metrics; it doesn't encrypt storage.
- **D:** CodeBuild builds and tests code/container images as part of CI/CD; it's unrelated to
  encryption at rest.

---

## Q9

A customer-facing chatbot is built on a Bedrock foundation model. The business requires it to
refuse to discuss certain competitor products and medical advice topics, and to never leak PII
that might appear in a generated response. Which Bedrock feature should be configured?

A) Bedrock Titan Embeddings with a larger dimensionality
B) Bedrock Guardrails, configured with denied topics and PII filters on both input and output
C) SageMaker Clarify post-training bias metrics
D) SageMaker Model Registry approval workflow

**Correct Answer: B**

**Explanation:** **Bedrock Guardrails** are configurable filters sitting between the user and
the foundation model: **denied topics** block disallowed subjects (competitor comparisons,
medical advice) and **PII filters** detect and mask/block personal information, applied to both
what goes into the model and what comes out — exactly matching this requirement. See
[`responsible-ai-and-guardrails.md`](../domain-4-monitoring-security/responsible-ai-and-guardrails.md#key-features--components)
and its ["chatbot needs to refuse topics" exam tip](../domain-4-monitoring-security/responsible-ai-and-guardrails.md#exam-tips).

**Why the others are wrong:**
- **A:** Embedding dimensionality affects how much nuance a vector captures for similarity
  search; it has no content-filtering or topic-refusal capability.
- **C:** SageMaker Clarify measures bias/fairness in *classic ML model* predictions (group-level
  disparate impact) — it is not a GenAI content-safety filter for chatbot input/output; the exam
  tests this exact distinction.
- **D:** Model Registry manages versioning and approval status of trained models — it has no
  content-filtering role at inference time.

---

## Q10 (Choose TWO)

A team is using SageMaker Clarify as part of a loan-approval model's responsible-AI process.
Which TWO statements correctly distinguish pre-training vs. post-training bias metrics?

A) Pre-training bias metrics examine the training data itself — e.g., class imbalance or a sensitive attribute correlated with the label — before any model is trained
B) Post-training bias metrics examine the trained model's actual predictions across groups — e.g., disparate impact — after training is complete
C) Pre-training bias metrics can only be computed after the model has been deployed to a live endpoint
D) Post-training bias metrics check whether the training code compiles without errors
E) Pre-training and post-training bias metrics both ignore any notion of protected/sensitive attributes

**Correct Answer: A and B**

**Explanation:** **Pre-training bias metrics** (SageMaker Clarify) check the raw dataset before
any model exists — class imbalance, correlated sensitive attributes. **Post-training bias
metrics** check the trained model's actual predictions across groups — e.g., **disparate
impact** (does one group receive a favorable outcome at a notably lower rate). Keeping these two
stages distinct is explicitly called out as an exam trap. See
[`responsible-ai-and-guardrails.md`](../domain-4-monitoring-security/responsible-ai-and-guardrails.md#how-it-works)
and its [exam tips](../domain-4-monitoring-security/responsible-ai-and-guardrails.md#exam-tips).

**Why the others are wrong:**
- **C:** This reverses the definition — pre-training metrics are computed on the *data*, before
  a model is trained at all, not after deployment.
- **D:** Checking whether code compiles is a software build/CI concern (e.g., CodeBuild), not
  what Clarify's post-training bias metrics measure (which focus on prediction fairness across
  groups).
- **E:** Both pre- and post-training bias metrics are explicitly built around examining
  sensitive/protected attributes (e.g., correlation with class imbalance, disparate impact
  across groups) — ignoring them entirely would defeat the purpose of bias detection.

---

## Q11

Regulators ask a lending company why a specific loan applicant was rejected by its ML model.
They want to understand the reasoning behind that one individual decision, in human-
understandable terms. What should the team use to answer this?

A) SageMaker Clarify's explainability reports (e.g., SHAP values) for that specific prediction
B) SageMaker Clarify's pre-training class-imbalance report
C) Bedrock Guardrails' content filter logs
D) CloudWatch billing alarms

**Correct Answer: A**

**Explanation:** **Explainability** (SageMaker Clarify, using SHAP values) answers "why did the
model make this specific prediction" by reporting how much each input feature contributed to
that individual result (e.g., "income contributed +0.3 toward approval, zip code contributed
-0.1") — exactly what's needed to answer an individual-level regulatory question. See
[`responsible-ai-and-guardrails.md`](../domain-4-monitoring-security/responsible-ai-and-guardrails.md#how-it-works)
and the Domain 4 README's
[explainability scenario](../domain-4-monitoring-security/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **B:** Pre-training class-imbalance reports describe the *dataset* as a whole (group-level),
  not the reasoning behind one specific individual's prediction.
- **C:** Guardrails content filter logs record what input/output was blocked for safety reasons
  in a GenAI chatbot — unrelated to explaining a classic ML loan-approval decision.
- **D:** CloudWatch billing alarms track cost thresholds; they have no relationship to model
  explainability.

---

## Q12 (Choose TWO)

A team is reviewing their ML cost-optimization strategy across both training and inference
workloads. Which TWO pairings correctly match a usage pattern to the appropriate purchasing
option?

A) Frequent, interruption-tolerant training jobs → Managed Spot Training
B) Always-on, steady-traffic inference endpoint → SageMaker Savings Plan
C) Always-on, steady-traffic inference endpoint → Managed Spot Training
D) One-time batch scoring job → a 3-year SageMaker Savings Plan commitment
E) Frequent, interruption-tolerant training jobs → a 3-year Reserved Instance commitment on the training fleet

**Correct Answer: A and B**

**Explanation:** These are the two canonical, correctly-matched pairings from
[`ml-cost-optimization.md`](../domain-4-monitoring-security/ml-cost-optimization.md#how-it-works):
interruption-tolerant, bursty training jobs get the steepest discount from **Managed Spot
Training** (since checkpointing lets them resume if reclaimed), while an **always-on, predictable
inference endpoint** benefits from a **SageMaker Savings Plan**'s committed-usage discount, since
its usage pattern is genuinely steady.

**Why the others are wrong:**
- **C:** Spot capacity can be reclaimed at any time and is unsuitable for an always-on production
  endpoint that must stay continuously available — this pairing is backwards.
- **D:** A one-time batch job is, by definition, not steady or long-term usage — committing to a
  3-year Savings Plan for a single one-off job locks in a long-term discount structure for usage
  that won't recur, wasting the commitment.
- **E:** A 3-year Reserved Instance commitment assumes steady, continuous usage — exactly wrong
  for training jobs that are frequent but short-lived and interruption-tolerant, where Spot's
  per-job discount is both cheaper and better matched to the actual usage shape.
