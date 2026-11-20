# Domain 4 Labs — Monitoring, Cost & Security (Floci + Alternatives)

*Companion to [`README.md`](README.md). Floci's genuine strength is here — IAM, KMS, and VPC are
real, well-emulated services in Floci, so most of the security half of this domain can be
practiced directly. SageMaker Model Monitor, Clarify, and Bedrock Guardrails are not emulated at
all; use the alternatives below for those.*

## What Floci can do here (real strength)

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
```

This is directly transferable to the real exam content on least-privilege IAM roles and KMS
encryption — the API shape is the same.

## What Floci can NOT do (and the real alternative)

| Need | Floci? | Use instead |
|---|---|---|
| Run SageMaker Model Monitor and see a real drift report | ❌ not emulated | Compute drift manually with **`scipy.stats.ks_2samp`** (Kolmogorov-Smirnov test, free, local) comparing a "training" distribution to a "live" distribution you generate yourself — the actual statistical test Model Monitor runs under the hood |
| Run SageMaker Inference Recommender's load test | ❌ not emulated | **`locust`** or **`k6`** (free, local load-testing tools) against your own FastAPI-served model (from Domain 3's lab) to measure latency/throughput across different local resource limits — same concept, your own hardware instead of SageMaker's catalog |
| Run SageMaker Clarify bias/explainability reports | ❌ not emulated | **Fairlearn** (`pip install fairlearn`) for bias metrics, **SHAP** (`pip install shap`) for explainability — both are the actual open-source libraries AWS built on top of, so the output concepts map directly |
| Configure/test Bedrock Guardrails | ❌ no Bedrock emulation | A local keyword/regex blocklist plus Hugging Face's free `unitary/toxic-bert` model for a conceptual stand-in for output content filtering |
| Practice VPC network isolation for a training job (no internet access) | ✅ Floci DOES support VPC APIs | `awslocal ec2 create-vpc` / `create-subnet` with no NAT/internet gateway route — the real pattern for "training job must have no internet access" |

## Minimal local drift-detection exercise (no AWS account needed)

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
just run locally on data you control instead of against a live SageMaker endpoint.

## Recommended real-AWS free tier path

1. **Floci first** for IAM/KMS/VPC — this domain's security content is the most faithfully
   reproducible locally of any domain in this cert.
2. **SageMaker Studio Lab** to see a real (free) Model Monitor/Clarify report, if you want the
   authentic console experience rather than the manual statistical equivalent above.
3. **AWS Free Tier account** only if you want to see real Bedrock Guardrails configured in the
   console — budget a few dollars for any actual foundation model calls through it.
