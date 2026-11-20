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

## What Floci can NOT do (and the real alternative)

| Need | Floci? | Use instead |
|---|---|---|
| Run SageMaker Model Monitor and see a real drift report | ❌ not emulated | Compute drift manually with **`scipy.stats.ks_2samp`** (Kolmogorov-Smirnov test, free, local) comparing a "training" distribution to a "live" distribution you generate yourself — the actual statistical test Model Monitor runs under the hood |
| Run SageMaker Inference Recommender's load test | ❌ not emulated | **`locust`** or **`k6`** (free, local load-testing tools) against your own FastAPI-served model (from Domain 3's lab) to measure latency/throughput across different local resource limits — same concept, your own hardware instead of SageMaker's catalog |
| Run SageMaker Clarify bias/explainability reports | ❌ not emulated | **Fairlearn** (`pip install fairlearn`) for bias metrics, **SHAP** (`pip install shap`) for explainability — both are the actual open-source libraries AWS built on top of, so the output concepts map directly |
| Configure/test Bedrock Guardrails | ❌ no Bedrock emulation | A local keyword/regex blocklist plus Hugging Face's free `unitary/toxic-bert` model for a conceptual stand-in for output content filtering |
| Practice VPC network isolation for a training job (no internet access) | ✅ Floci DOES support VPC APIs | `awslocal ec2 create-vpc` / `create-subnet` with no NAT/internet gateway route — the real pattern for "training job must have no internet access" |
| See real SageMaker Savings Plan / Spot discount percentages | ❌ not emulated | Check the live SageMaker pricing page, or practice the *decision* (steady vs. bursty vs. interruption-tolerant) using real EC2 Spot Instances, which Floci's compute emulation does cover conceptually |

## Recommended real-AWS free tier path

1. **Floci first** for IAM/KMS/VPC — this domain's security content is the most faithfully
   reproducible locally of any domain in this cert.
2. **SageMaker Studio Lab** to see a real (free) Model Monitor/Clarify report, if you want the
   authentic console experience rather than the manual statistical equivalent above.
3. **AWS Free Tier account** only if you want to see real Bedrock Guardrails configured in the
   console — budget a few dollars for any actual foundation model calls through it.

## Self-check before your practice exam

- Can you explain, using your own Lab 2 vs. Lab 3 output, why data drift could show "no drift"
  while concept drift is actively happening at the same time?
- Can you point at one specific line in Lab 1's VPC commands that's responsible for the "no
  internet access" guarantee, and explain what you'd need to add (and why you wouldn't) to
  restore internet access?
- Can you explain, from Lab 5's output, the difference between what the first printed array (one
  record's SHAP values) tells you versus what `top_features` (the aggregated ranking) tells you?
