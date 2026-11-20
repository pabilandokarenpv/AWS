# Domain 4 Labs — Monitoring, Cost & Security (Floci + Alternatives)

*Companion to [`README.md`](README.md). Floci's genuine strength is here — IAM, KMS, and VPC are
real, well-emulated services in Floci, so most of the security half of this domain can be
practiced directly. SageMaker Model Monitor, Clarify, and Bedrock Guardrails are not emulated at
all; use the alternatives below for those.*

## Lab map

| # | Lab | Tooling | Maps to |
|---|---|---|---|
| 1 | IAM least privilege + KMS encryption + VPC isolation | Floci | Task 4.3 |
| 2 | Detect data drift with a real statistical test | scipy | Task 4.1 |
| 3 | Detect concept drift with simulated ground truth | scikit-learn | Task 4.1 |
| 4 | Load-test a local endpoint, the Inference Recommender way | locust | Task 4.2 |
| 5 | Bias + explainability on a real model | Fairlearn, SHAP | Task 4.4 |
| 6 | A local Guardrails stand-in | regex + Hugging Face toxicity model | Task 4.4 |
| 7 | Simulating agent coordination failures and tool-call tracing | plain Python | Task 4.1.5 — agent observability |
| 8 | Static code + dependency vulnerability scanning | bandit, pip-audit | Task 4.3.1 — secure ML/AI CI/CD |
| 9 | Simulating Cost Anomaly Detection with a statistical baseline | pandas, numpy | Task 4.2.10 — AI-specific cost patterns |
| 10 | Validating a local Guardrails-style policy configuration against test cases | plain Python + pytest | Task 4.3.9 / 4.4 — responsible-AI safeguards |

## Lab 1 — What Floci can do here (real strength)

```bash
alias awslocal='aws --endpoint-url=http://localhost:4566 --profile floci'

# IAM least privilege for a training job role
awslocal iam create-role --role-name SageMakerTrainingRole \
  --assume-role-policy-document file://trust-policy.json
awslocal iam put-role-policy --role-name SageMakerTrainingRole \
  --policy-name S3ReadOnlyTrainingData \
  --policy-document file://s3-readonly-policy.json

# KMS key for encrypting training data / model artifacts at rest
awslocal kms create-key --description "ML training data encryption key"
awslocal kms create-alias --alias-name alias/ml-training-key \
  --target-key-id <key-id-from-above>

# S3 bucket encrypted with that key (practicing "data at rest" encryption)
awslocal s3api put-bucket-encryption --bucket ml-training-data \
  --server-side-encryption-configuration '{
    "Rules": [{"ApplyServerSideEncryptionByDefault":
      {"SSEAlgorithm": "aws:kms", "KMSMasterKeyID": "alias/ml-training-key"}}]}'

# VPC isolation: private subnet with NO internet/NAT gateway route
awslocal ec2 create-vpc --cidr-block 10.0.0.0/16
awslocal ec2 create-subnet --vpc-id <vpc-id> --cidr-block 10.0.1.0/24
# Deliberately skip creating/attaching an internet gateway or NAT gateway —
# this subnet has no route to the public internet, exactly the pattern
# task statement 4.3 tests for sensitive training data.
awslocal ec2 describe-route-tables --filters "Name=vpc-id,Values=<vpc-id>"
```

This is directly transferable to the real exam content on least-privilege IAM roles, KMS
encryption, and VPC network isolation — the API shape is the same, and reasoning about *why* no
route table entry points to an internet/NAT gateway is exactly the Domain 4 security skill being
tested.

## Lab 2 — Detect data drift with the real statistical test Model Monitor uses

```bash
pip install scipy numpy
```

```python
from scipy import stats
import numpy as np

# "Training-time" feature distribution (what Model Monitor saved as baseline)
training_ages = np.random.normal(loc=35, scale=10, size=1000)

# "Live" feature distribution months later — simulating a demographic shift
live_ages = np.random.normal(loc=45, scale=10, size=1000)

stat, p_value = stats.ks_2samp(training_ages, live_ages)
print(f"KS statistic: {stat:.3f}, p-value: {p_value:.5f}")
if p_value < 0.05:
    print("Distributions are significantly different — this IS data drift.")
else:
    print("No significant drift detected.")
```

This is the same statistical idea SageMaker Model Monitor's data-quality drift check performs —
just run locally on data you control instead of against a live SageMaker endpoint. Re-run with
`loc=36` (a tiny, realistic shift) instead of `loc=45` and observe the p-value likely stays above
0.05 — a direct, hands-on demonstration that drift detection is about *statistically significant*
change, not any change at all.

## Lab 3 — Detect concept drift (requires fresh ground truth, unlike Lab 2)

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score
import numpy as np

# Simulate "training-time" data and relationship
np.random.seed(0)
X_train, y_train = make_classification(n_samples=1000, n_features=5, random_state=0)
model = RandomForestClassifier(random_state=0).fit(X_train, y_train)
print("Accuracy on training-era data:", accuracy_score(y_train, model.predict(X_train)))

# Simulate "live, months-later" data where the INPUT distribution looks similar,
# but the true relationship between inputs and the correct label has flipped
# for one feature (concept drift: same-looking inputs, different correct answer)
X_live, y_live_true = make_classification(n_samples=1000, n_features=5, random_state=0)
y_live_true_drifted = 1 - y_live_true  # the "correct answer" relationship inverted

print("Accuracy on live data vs. ORIGINAL labels:",
      accuracy_score(y_live_true, model.predict(X_live)))
print("Accuracy on live data vs. DRIFTED (true, current) labels:",
      accuracy_score(y_live_true_drifted, model.predict(X_live)))
```

The second accuracy number collapsing (likely near the inverse of the first) while the input
features themselves are statistically identical to training is exactly what makes concept drift
harder to detect than data drift in practice — Lab 2's input-distribution test would show *no*
drift here at all, because nothing about the inputs changed; only fresh, correctly-labeled live
data (simulated here, collected for real via a periodic labeled sample in production) can reveal
concept drift.

## Lab 4 — Load-testing a local endpoint, the Inference Recommender way

```bash
pip install locust fastapi uvicorn scikit-learn joblib
```

Reuse Domain 3 Lab 2's `serve.py` FastAPI endpoint, then:

```python
# locustfile.py
from locust import HttpUser, task, between

class InferenceUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def predict(self):
        self.client.post("/invocations", json=[5.1, 3.5, 1.4, 0.2])
```

```bash
uvicorn serve:app --port 8000 &
locust -f locustfile.py --host http://localhost:8000 --headless -u 50 -r 10 --run-time 30s
```

Locust's summary output (requests/sec, median/p95 latency, failure rate) is conceptually the
exact report SageMaker Inference Recommender produces across candidate instance types — here,
you're load-testing your own hardware instead of SageMaker's instance catalog, but the "measure,
don't guess" discipline transfers directly.

## Lab 5 — Bias and explainability on a real model

```bash
pip install fairlearn shap scikit-learn
```

```python
import shap
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

X, y = load_breast_cancer(return_X_y=True)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(random_state=42).fit(X_train, y_train)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_val)

# Local explainability: why was THIS ONE prediction made?
print("SHAP values for the first validation record (per feature):")
print(shap_values[1][0] if isinstance(shap_values, list) else shap_values[0])

# Global explainability: which features matter most OVERALL?
import numpy as np
mean_abs_shap = np.abs(shap_values[1] if isinstance(shap_values, list) else shap_values).mean(axis=0)
top_features = np.argsort(mean_abs_shap)[::-1][:5]
print("Top 5 globally important features (by index):", top_features)
```

This is the real, open-source library SageMaker Clarify builds its SHAP explainability on top of
— running it directly here produces the exact local/global distinction described in
`responsible-ai-and-guardrails.md`, for free, against a real trained model.

## Lab 6 — A local Guardrails stand-in

```bash
pip install transformers torch
```

```python
from transformers import pipeline

DENIED_TOPICS = ["competitor pricing", "medical dosage", "legal advice"]
toxicity_classifier = pipeline("text-classification", model="unitary/toxic-bert")

def input_filter(user_message: str) -> tuple[bool, str]:
    lowered = user_message.lower()
    for topic in DENIED_TOPICS:
        if topic in lowered:
            return False, f"Blocked: denied topic '{topic}' detected."
    return True, "Passed input filter."

def output_filter(model_response: str) -> tuple[bool, str]:
    result = toxicity_classifier(model_response)[0]
    if result["label"] == "toxic" and result["score"] > 0.5:
        return False, f"Blocked: toxic content detected (score={result['score']:.2f})."
    return True, "Passed output filter."

# Simulate the two-sided check described in responsible-ai-and-guardrails.md
test_input = "Can you give me medical dosage advice for ibuprofen?"
passed, reason = input_filter(test_input)
print(f"Input check: {passed} — {reason}")

test_output = "You're clearly too stupid to understand basic instructions."
passed, reason = output_filter(test_output)
print(f"Output check: {passed} — {reason}")
```

This is a deliberately simplified stand-in (a real Bedrock Guardrail is far more sophisticated —
ML-based classifiers plus pattern matching plus, for some checks, formal logic), but it reproduces
the exact two-sided (input AND output) filtering architecture from this domain's dedicated topic
doc using entirely free, local tooling.

## Lab 7 — Simulating agent coordination failures and tool-call tracing

```python
import time, random, json

def traced_tool_call(tool_name, fn, *args, **kwargs):
    start = time.time()
    try:
        result = fn(*args, **kwargs)
        status = "success"
    except Exception as e:
        result = str(e)
        status = "failure"
    trace_event = {
        "tool": tool_name,
        "status": status,
        "latency_ms": round((time.time() - start) * 1000, 1),
        "result": result,
    }
    print("TRACE:", json.dumps(trace_event))
    return trace_event

def flaky_order_lookup(order_id):
    if random.random() < 0.3:  # simulate a real ~30% intermittent failure rate
        raise TimeoutError(f"order-status API timed out for {order_id}")
    return f"Order {order_id} is out for delivery."

def run_agent_turn(order_id, run_number):
    print(f"\n--- Agent run {run_number} ---")
    trace = traced_tool_call("OrderStatusAPI", flaky_order_lookup, order_id)
    if trace["status"] == "failure":
        print("Agent falls back to: 'I'm having trouble checking that right now, please try again.'")
    else:
        print(f"Agent responds: {trace['result']}")
    return trace

traces = [run_agent_turn("ORD-1001", i) for i in range(10)]
failure_rate = sum(1 for t in traces if t["status"] == "failure") / len(traces)
print(f"\nObserved tool-call failure rate across 10 runs: {failure_rate:.0%}")
if failure_rate > 0.15:
    print("ALERT: tool-call failure rate exceeds 15% threshold -- investigate OrderStatusAPI reliability.")
```

This reproduces the exact tool-call tracing and threshold-alerting pattern `README.md`'s agent
observability section describes — each tool call is logged with status and latency (what
AgentCore Observability captures automatically for a real Bedrock Agent), and a simple threshold
check demonstrates the "alert when coordination-failure rate trends up" behavior described there,
entirely with plain Python and no managed observability service required to see the concept work.

## Lab 8 — Static code and dependency vulnerability scanning, the real alternative to CodeGuru + Inspector

```bash
pip install bandit pip-audit
```

```python
# vulnerable_inference.py -- deliberately includes two real, detectable issues
import subprocess

AWS_SECRET_KEY = "AKIAIOSFODNN7EXAMPLE"  # hardcoded credential -- a real CodeGuru-style finding

def run_preprocessing(user_supplied_filename):
    # shell=True with unsanitized input -- a real injection risk
    subprocess.run(f"cat {user_supplied_filename}", shell=True)
```

```bash
bandit vulnerable_inference.py
```

Run this and confirm Bandit (a free, open-source Python static-analysis security scanner) flags
both issues — a hardcoded credential and a shell-injection risk — the same category of findings
Amazon CodeGuru Reviewer surfaces for training/inference code inside a real CI/CD pipeline.

```bash
pip-audit
```

Run `pip-audit` against any project's installed dependencies to get a real, free list of known
CVEs in your current package versions — the dependency-scanning half of what Amazon Inspector
does for a built container image, here run directly against a Python environment instead of a
container.

## Lab 9 — Simulating Cost Anomaly Detection with a statistical baseline

```bash
pip install pandas numpy
```

```python
import numpy as np
import pandas as pd

# Simulate 60 days of "normal" daily GenAI spend (realistic day-to-day noise)
np.random.seed(42)
normal_days = np.random.normal(loc=120, scale=15, size=60)  # ~$120/day, some natural variance

# Day 61: a real anomaly -- a one-time full-corpus re-embedding event
anomaly_day = 420.0

spend = pd.Series(list(normal_days) + [anomaly_day])

# A simple, real anomaly-detection approach: flag any day more than 3 standard
# deviations above the ROLLING mean of the days seen so far (not the whole series,
# since Cost Anomaly Detection learns a baseline from HISTORY, not from data it hasn't
# seen yet -- an important distinction from simply eyeballing the full series after the fact)
rolling_mean = spend.expanding(min_periods=10).mean()
rolling_std = spend.expanding(min_periods=10).std()
z_scores = (spend - rolling_mean) / rolling_std

threshold = 3.0
anomalies = spend[z_scores > threshold]
print(f"Flagged anomalies (z-score > {threshold}):")
print(anomalies)
print(f"\nDay 61's z-score: {z_scores.iloc[-1]:.2f} -- {'FLAGGED' if z_scores.iloc[-1] > threshold else 'not flagged'}")
```

Run this and confirm day 61 (the simulated anomaly) is correctly flagged while none of the 60
"normal" days are -- a direct, hands-on demonstration of the exact statistical idea behind AWS
Cost Anomaly Detection: learn what normal day-to-day variation looks like from an account's own
history, then flag a statistically significant deviation from *that specific account's* learned
pattern, not from an arbitrary fixed dollar threshold a human had to guess in advance (the AWS
Budgets approach, by contrast). Re-run with the anomaly day set to `135.0` instead of `420.0` and
observe the z-score likely stays below the threshold -- confirming the detector correctly
distinguishes real drift from the kind of day-to-day noise already present in the 60-day baseline.

## Lab 10 — Validating a local Guardrails-style policy configuration against test cases

```bash
pip install pytest
```

```python
# guardrail_policy.py -- a simplified, local stand-in for testing Guardrails-style
# policy configuration BEFORE paying for real Bedrock Guardrails API calls
DENIED_TOPICS = {
    "medical_dosage": ["dosage", "how many mg", "milligrams of"],
    "competitor_pricing": ["competitor price", "cheaper than us"],
}

PII_PATTERNS = {
    "ssn": r"\d{3}-\d{2}-\d{4}",
    "email": r"[\w\.-]+@[\w\.-]+\.\w+",
}

def check_denied_topics(text: str) -> list[str]:
    hits = []
    lowered = text.lower()
    for topic, phrases in DENIED_TOPICS.items():
        if any(p in lowered for p in phrases):
            hits.append(topic)
    return hits

def check_pii(text: str) -> list[str]:
    import re
    hits = []
    for pii_type, pattern in PII_PATTERNS.items():
        if re.search(pattern, text):
            hits.append(pii_type)
    return hits
```

```python
# test_guardrail_policy.py -- real pytest test cases validating the policy BEFORE
# it's ever attached to a real, billed Bedrock Guardrail
from guardrail_policy import check_denied_topics, check_pii

def test_denied_topic_exact_phrase():
    assert "medical_dosage" in check_denied_topics("What dosage of ibuprofen should I take?")

def test_denied_topic_paraphrased_still_misses_without_semantic_matching():
    # This SHOULD fail with simple keyword matching -- demonstrating exactly why
    # real Bedrock Guardrails uses semantic matching (via a definition + examples),
    # not literal keyword lists, for denied topics
    result = check_denied_topics("Could you tell me the right amount of medicine for a headache?")
    assert "medical_dosage" not in result  # keyword matching misses the paraphrase

def test_pii_ssn_detected():
    assert "ssn" in check_pii("My SSN is 123-45-6789, please update my file.")

def test_pii_email_detected():
    assert "email" in check_pii("Contact me at jane.doe@example.com")

def test_clean_text_passes():
    assert check_denied_topics("What's the weather like today?") == []
    assert check_pii("What's the weather like today?") == []
```

```bash
pytest test_guardrail_policy.py -v
```

Run this and confirm `test_denied_topic_paraphrased_still_misses_without_semantic_matching`
actually passes (meaning the simple keyword approach *did* miss the paraphrase) -- a deliberately
built-in failure case proving, with real executed code, exactly why
`bedrock-guardrails-deep-dive.md`'s real Guardrails denied-topics configuration uses semantic
matching (a natural-language definition plus example phrasings) rather than a literal keyword
list: a keyword list provably misses a rephrased version of the exact same disallowed question,
which real Guardrails is specifically designed to still catch.

## What Floci can NOT do (and the real alternative)

| Need | Floci? | Use instead |
|---|---|---|
| Run SageMaker Model Monitor and see a real drift report | ❌ not emulated | Compute drift manually with **`scipy.stats.ks_2samp`** (Kolmogorov-Smirnov test, free, local) comparing a "training" distribution to a "live" distribution you generate yourself — the actual statistical test Model Monitor runs under the hood |
| Run SageMaker Inference Recommender's load test | ❌ not emulated | **`locust`** or **`k6`** (free, local load-testing tools) against your own FastAPI-served model (from Domain 3's lab) to measure latency/throughput across different local resource limits — same concept, your own hardware instead of SageMaker's catalog |
| See real SageMaker Clarify bias/explainability reports | ❌ not emulated | **Fairlearn** (`pip install fairlearn`) for bias metrics, **SHAP** (`pip install shap`) for explainability — both are the actual open-source libraries AWS built on top of, so the output concepts map directly |
| Configure/test Bedrock Guardrails | ❌ no Bedrock emulation | A local keyword/regex blocklist plus Hugging Face's free `unitary/toxic-bert` model for a conceptual stand-in for output content filtering (Lab 6), or Lab 10's pytest-driven policy validation approach for testing configuration logic before it's ever attached to a real, billed Guardrail |
| Practice VPC network isolation for a training job (no internet access) | ✅ Floci DOES support VPC APIs | `awslocal ec2 create-vpc` / `create-subnet` with no NAT/internet gateway route — the real pattern for "training job must have no internet access" |
| See real SageMaker Savings Plan / Spot discount percentages | ❌ not emulated | Check the live SageMaker pricing page, or practice the *decision* (steady vs. bursty vs. interruption-tolerant) using real EC2 Spot Instances, which Floci's compute emulation does cover conceptually |
| Run Amazon CodeGuru Reviewer / Amazon Inspector against real CI/CD artifacts | ❌ not emulated | **Lab 8's bandit + pip-audit** — real, free, open-source static-analysis and dependency-CVE scanners catching the same category of issues |
| See a real AgentCore Observability trace for a live Bedrock Agent | ❌ no Bedrock emulation | **Lab 7's traced tool-call simulation** — the same status/latency/failure-rate tracing concept, run against a local flaky function instead of a real agent |
| See a real AWS Cost Anomaly Detection alert fire | ❌ not emulated | **Lab 9's rolling z-score detector** — the same core statistical idea (learn a baseline from history, flag statistically significant deviations), run against simulated daily spend instead of a real billing feed |

## Use Cases — Real Scenarios

1. A student reproduces Lab 2's KS-test drift detection with a deliberately tiny, realistic shift
   (`loc=36` vs. training's `loc=35`) to personally confirm the test correctly reports "no
   significant drift," building intuition for why drift detection isn't triggered by any change
   at all, only a statistically meaningful one.
2. An ML platform team adopts Lab 1's VPC-with-no-route-table pattern as their default template
   for any new sensitive-data training job, copy-pasting the exact "deliberately skip the
   internet/NAT gateway" step as a checklist item for every new project.
3. A fairness reviewer runs Lab 5's SHAP explainability against their own trained model before a
   compliance review, generating a real local-explanation example to show auditors rather than
   only describing the concept abstractly.
4. A support engineering team builds Lab 6's keyword+toxicity-classifier Guardrails stand-in to
   prototype content-filtering rules cheaply before committing to the exact rule set they'll
   later configure in real Bedrock Guardrails.
5. A platform reliability engineer runs Lab 7's agent-tracing simulation with the failure rate
   dialed up to 50% to see how quickly the alerting threshold fires, calibrating their own
   production alert threshold against a known, controlled failure rate first.
6. A security-conscious startup runs Lab 8's bandit scan against their actual training pipeline
   code before their first production deployment, catching a hardcoded credential their own code
   review had missed.
7. A finance team uses Lab 4's locust load test to generate real latency/throughput numbers
   before approving a SageMaker Inference Recommender job against the same model on paid infra,
   validating the testing approach costs nothing before scaling it up.
8. A compliance team reproduces Lab 3's concept-drift simulation to explain to a non-technical
   stakeholder, using real printed numbers, why "the inputs look the same" doesn't guarantee "the
   model is still correct" — a distinction that's hard to convey without a concrete example.
9. A DevOps engineer runs `pip-audit` (Lab 8) against a real, already-deployed inference
   container's dependency manifest and discovers an unpatched CVE in a transitive dependency
   nobody on the team had flagged, triggering an unplanned but necessary patch cycle.
10. A new hire runs all three of Labs 1, 7, and 8 in their first week specifically because they
    cover this domain's three "rings" (security, agent health, pipeline security) with the least
    AWS-account setup required of any domain's labs, making them the fastest path to real,
    hands-on understanding before touching a paid account.
11. A FinOps-focused platform engineer runs Lab 9 with the anomaly day's spend dialed down
    progressively (from $420 to $200 to $135) to find the exact point where their chosen z-score
    threshold stops flagging it, building direct intuition for the threshold-sensitivity tradeoff
    before configuring a real Cost Anomaly Detection monitor.
12. A GenAI application team writes Lab 10's pytest suite for their actual planned denied-topics
    and PII rules *before* configuring real Bedrock Guardrails, using the deliberately-failing
    paraphrase test as evidence for why they need semantic (not keyword) topic matching in the
    real configuration — directly informing the policy JSON they write following
    `bedrock-guardrails-deep-dive.md`.

## Recommended real-AWS free tier path

1. **Floci first** for IAM/KMS/VPC — this domain's security content is the most faithfully
   reproducible locally of any domain in this cert.
2. **SageMaker Studio Lab** to see a real (free) Model Monitor/Clarify report, if you want the
   authentic console experience rather than the manual statistical equivalent above.
3. **AWS Free Tier account** only if you want to see real Bedrock Guardrails and Cost Anomaly
   Detection configured in the console — budget a few dollars for any actual foundation model
   calls through it.

## Self-check before your practice exam

- Can you explain, using your own Lab 2 vs. Lab 3 output, why data drift could show "no drift"
  while concept drift is actively happening at the same time?
- Can you point at one specific line in Lab 1's VPC commands that's responsible for the "no
  internet access" guarantee, and explain what you'd need to add (and why you wouldn't) to
  restore internet access?
- Can you explain, from Lab 5's output, the difference between what the first printed array (one
  record's SHAP values) tells you versus what `top_features` (the aggregated ranking) tells you?
- Can you explain, from Lab 9's output, why the z-score is computed against an *expanding* window
  of history rather than the full dataset including days that haven't happened yet — and why that
  distinction matters for a real, live anomaly detector that can only ever see the past?
- Can you explain, from Lab 10's deliberately-failing paraphrase test, exactly why real Bedrock
  Guardrails denied topics need semantic matching rather than a literal keyword list — and name
  one other Guardrails filter type (from `bedrock-guardrails-deep-dive.md`) where literal keyword
  matching genuinely is the right approach instead?

## Related Terms

- [`README.md`](README.md) — the domain-level content these labs reproduce hands-on.
- [`model-drift-deep-dive.md`](model-drift-deep-dive.md) — Labs 2 and 3's statistical tests are
  the runnable version of this doc's full drift mechanics and worked numeric example.
- [`iam-least-privilege-ml-pipelines.md`](iam-least-privilege-ml-pipelines.md) — Lab 1's IAM/KMS/
  VPC commands are the runnable version of this doc's real policy JSON patterns.
- [`bedrock-guardrails-deep-dive.md`](bedrock-guardrails-deep-dive.md) — Labs 6 and 10 are local,
  free stand-ins for this doc's real Guardrails filter-type configuration JSON.
- [`finops-for-ml-token-cost-tracking.md`](finops-for-ml-token-cost-tracking.md) — Lab 9 is the
  runnable version of this doc's Cost Anomaly Detection coverage.
- [`MASTER-CHUNK.md`](MASTER-CHUNK.md) — Section 18's hands-on command reference is the real-AWS-
  CLI counterpart to this doc's free/local lab exercises.
