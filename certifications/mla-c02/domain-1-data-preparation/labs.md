# Domain 1 Labs — Data Preparation (Floci + Alternatives)

*Companion to [`README.md`](README.md). Honest note up front: Floci emulates AWS **control-plane
APIs** (S3, Glue's catalog API, Kinesis streams). It does **not** run Glue Spark jobs, SageMaker
Data Wrangler transforms, Feature Store's real backing stores, or any embedding/foundation model
inference. Use Floci for what it's good at (S3 staging, API shape practice) and the alternatives
below for anything that needs real ML compute.*

## Lab map — what you'll build, end to end

| # | Lab | Tooling | Maps to |
|---|---|---|---|
| 1 | S3 raw/curated zone layout + Kinesis API shape | Floci | Task 1.1 — ingest and store |
| 2 | Local pandas ETL (clean, encode, dedupe) | pandas, local | Task 1.2 — transform |
| 3 | Bias/class-imbalance detection | Fairlearn, ydata-profiling | Task 1.3 — data integrity |
| 4 | Local RAG pipeline (chunk → embed → search) | sentence-transformers, FAISS | Task 1.4 — RAG prep |
| 5 | SageMaker Studio Lab: real Data Wrangler-style exploration | SageMaker Studio Lab (free) | Tasks 1.2/1.3 on real infra |
| 6 | Feature Store online/offline mental model | plain Python | Task 1.2 — reusable features |

## Lab 1 — What Floci can do here

- Create buckets/zones (`raw`, `curated`) and upload/list objects — practicing the S3 layout a
  real data lake uses.
- Exercise the Kinesis Data Streams API shape (create stream, put/get records) to practice the
  CLI/SDK calls, not real throughput/shard behavior.

```bash
# Setup (see labs-floci/README.md for the one-time Docker setup)
alias awslocal='aws --endpoint-url=http://localhost:4566 --profile floci'

# Create a raw/curated zone layout
awslocal s3 mb s3://ml-data-raw
awslocal s3 mb s3://ml-data-curated

# Upload a sample raw file
echo '{"id":1,"amount":42.50,"category":"grocery"}' > sample.json
awslocal s3 cp sample.json s3://ml-data-raw/transactions/sample.json

# Exercise Kinesis API shape (not real streaming throughput)
awslocal kinesis create-stream --stream-name tx-events --shard-count 1
awslocal kinesis put-record --stream-name tx-events \
  --partition-key tx1 --data '{"amount":42.50}'

# Practice Glue Data Catalog API shape (not a real crawler/Spark run)
awslocal glue create-database --database-input '{"Name":"ml_curated_db"}'
awslocal glue create-table --database-name ml_curated_db --table-input '{
  "Name": "transactions",
  "StorageDescriptor": {
    "Columns": [
      {"Name": "id", "Type": "int"},
      {"Name": "amount", "Type": "double"},
      {"Name": "category", "Type": "string"}
    ],
    "Location": "s3://ml-data-curated/transactions/"
  }
}'
awslocal glue get-tables --database-name ml_curated_db
```

This last block is the realistic, Floci-supported slice of "cataloging" — it exercises the exact
API calls a real Glue Crawler would make, even though no real crawler runs against your S3 data.

## Lab 2 — Local pandas ETL (the real alternative to Glue DataBrew/Data Wrangler)

```bash
pip install pandas
```

```python
# etl_demo.py — stands in for a Glue ETL Job / Data Wrangler flow
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "customer_id": range(1, 11),
    "monthly_charges": [29.99, None, 54.50, 19.99, None, 89.00, 45.00, 60.00, None, 33.33],
    "contract_type": ["month", "year", "month", "two-year", "month",
                       "year", "two-year", "month", "year", "month"],
    "churned": [0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
})

# 1. Handle missing values (the single most common Data Wrangler/DataBrew transform)
df["monthly_charges"] = df["monthly_charges"].fillna(df["monthly_charges"].median())

# 2. One-hot encode a categorical column (contract_type -> several 0/1 columns)
df = pd.get_dummies(df, columns=["contract_type"], prefix="contract")

# 3. Check class imbalance before writing out — Data Wrangler would flag this automatically
churn_rate = df["churned"].mean()
print(f"Positive class (churned) rate: {churn_rate:.1%}")
if churn_rate < 0.15:
    print("Class imbalance detected — flag for Domain 2 (class weighting / resampling).")

df.to_csv("customers_clean.csv", index=False)
print("Cleaned, ML-ready file written: customers_clean.csv")
```

This reproduces the exact three operations (impute missing values, one-hot encode, flag
imbalance) that the SageMaker Overview document's worked churn example walks through using Data
Wrangler's visual UI — the underlying logic is identical, just hand-written instead of clicked.

## Lab 3 — Bias / class-imbalance detection (the real alternative to Clarify pre-training checks)

```bash
pip install fairlearn ydata-profiling
```

```python
from fairlearn.metrics import MetricFrame, selection_rate
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np

np.random.seed(0)
n = 1000
df = pd.DataFrame({
    "approved": np.random.binomial(1, 0.6, n),
    "zip_group": np.random.choice(["A", "B"], n, p=[0.5, 0.5]),
})
# Simulate a biased outcome: group B approved at a much lower rate
df.loc[df["zip_group"] == "B", "approved"] = np.random.binomial(1, 0.3, (df["zip_group"] == "B").sum())

mf = MetricFrame(
    metrics=selection_rate,
    y_true=df["approved"], y_pred=df["approved"],
    sensitive_features=df["zip_group"],
)
print("Approval (selection) rate by group:")
print(mf.by_group)
print("\nDisparate impact ratio (group B / group A):",
      mf.by_group["B"] / mf.by_group["A"])
```

A disparate impact ratio well below 0.8 (the commonly cited "four-fifths rule" threshold used in
US employment-discrimination law, and a reasonable rule of thumb elsewhere) is exactly the kind
of signal SageMaker Clarify's post-training bias report would surface — Fairlearn is the real,
open-source library computing a directly analogous metric, locally and for free.

## Lab 4 — Minimal local RAG exercise (no AWS account needed)

```bash
pip install sentence-transformers faiss-cpu
```

```python
from sentence_transformers import SentenceTransformer
import faiss, numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")  # free, runs on CPU
chunks = [
    "The return policy allows refunds within 30 days of purchase.",
    "Shipping typically takes 3-5 business days within the country.",
    "Gift cards do not expire and are non-refundable.",
]
embeddings = model.encode(chunks)
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

query = "How long do I have to return something?"
q_emb = model.encode([query])
distances, indices = index.search(np.array(q_emb), k=1)
print("Most relevant chunk:", chunks[indices[0][0]])
print("Distance (lower = more similar):", distances[0][0])
```

This is the exact mechanism `embeddings-and-rag-data-prep.md` describes — chunk, embed, store,
embed the query, nearest-neighbor search — just running on your laptop instead of against
Bedrock + OpenSearch. Once this makes sense, the jump to "swap `SentenceTransformer` for a
Bedrock `InvokeModel` embeddings call, and FAISS for OpenSearch Serverless" is conceptual, not
new mechanics.

**Extension — simulate metadata filtering (multi-tenant isolation):**

```python
# Add a simple tenant filter on top of the same index, as FAISS has no native metadata filter.
chunk_tenants = ["tenant_a", "tenant_a", "tenant_b"]

def search_for_tenant(query, tenant, k=1):
    q_emb = model.encode([query])
    # over-fetch, then filter — a simplified stand-in for a real vector store's metadata filter
    distances, indices = index.search(np.array(q_emb), k=len(chunks))
    for dist, idx in zip(distances[0], indices[0]):
        if chunk_tenants[idx] == tenant:
            return chunks[idx], dist
    return None, None

result, dist = search_for_tenant("What's your return policy?", "tenant_b")
print("Tenant B's visible answer:", result)
```

This over-fetch-then-filter pattern is a simplified stand-in for what a real vector store's
native metadata filtering does in one step — useful for understanding the *concept* before using
OpenSearch's or Bedrock Knowledge Bases' built-in filtering.

## What Floci can NOT do (and the real alternative)

| Need | Floci? | Use instead |
|---|---|---|
| Run a Glue ETL (Spark) transform job | ❌ no Spark backend | **AWS Glue Studio free trial on a real AWS account** (stays in free tier for small jobs), or run the equivalent transform locally with **pandas**/plain Python — same logic, no cluster |
| Visually explore data with bias reports (SageMaker Data Wrangler) | ❌ not emulated | **pandas-profiling / ydata-profiling** (free, local) for exploratory stats; **Fairlearn** (free, local) for bias/fairness metrics — conceptually the same checks Data Wrangler runs |
| SageMaker Feature Store (offline + online) | ❌ not emulated | **SageMaker Studio Lab** (free tier, no AWS account/credit card needed, real SageMaker notebook environment) to try Feature Store's actual API against a real (free-tier-eligible) SageMaker domain; for pure local practice, a plain SQLite/Parquet file plays the "offline store" role conceptually |
| Generate text embeddings | ❌ no Bedrock emulation | **`sentence-transformers`** (free, local, `pip install sentence-transformers`, e.g. `all-MiniLM-L6-v2` model) — produces real embeddings on your own machine, same concept as Titan Embeddings |
| Vector similarity search | ❌ not emulated | **FAISS** (free, local, `pip install faiss-cpu`) or Postgres + `pgvector` in a local Docker container |
| Run a real Glue Crawler against actual data | ❌ not emulated | Any small **AWS Free Tier** account — Glue Crawlers have a modest free tier suitable for learning-scale datasets |

## Feature Store online/offline split, as a bridge to the dedicated Data Wrangler/Feature Store doc

```python
# A tiny mental model of Feature Store's online/offline split, using plain dicts.
offline_store = []  # append-only, full history — mirrors S3-backed Offline Store
online_store = {}    # keyed by record id, latest value only — mirrors the Online Store

def ingest(record_id, event_time, features):
    offline_store.append({"id": record_id, "time": event_time, **features})
    existing = online_store.get(record_id)
    if existing is None or event_time > existing["time"]:
        online_store[record_id] = {"time": event_time, **features}

ingest("cust_1", 100, {"avg_spend": 42.0})
ingest("cust_1", 150, {"avg_spend": 55.0})  # a newer value for the same customer
ingest("cust_1", 120, {"avg_spend": 99.0})  # an OUT-OF-ORDER late-arriving backfill

print("Offline store (full history):", offline_store)
print("Online store (latest only, by event_time, NOT insertion order):", online_store["cust_1"])
```

The third `ingest()` call is deliberately out of order by insertion but *not* the newest by
`event_time` — run this and confirm the Online Store correctly still shows the `event_time=150`
record, not the most recently-inserted one. This is the exact gotcha described in
`sagemaker-data-wrangler-and-feature-store.md`'s troubleshooting section (a backfill job writing
old timestamps silently fails to update what's served) and is worth reproducing locally before
trusting it on the real service.

## Recommended real-AWS free tier path

1. **SageMaker Studio Lab** (https://studiolab.sagemaker.aws) — free, no credit card, no AWS
   account required, gives you a real JupyterLab environment with GPU hours/day for free. Best
   place to actually run SageMaker Data Wrangler-style exploration and small training jobs.
2. **AWS Free Tier account** (if/when you do want real Glue/Kinesis/Bedrock) — Glue has a small
   free tier for crawler/catalog requests; Bedrock charges per token from the first call (no
   meaningful free tier) — budget a few dollars before experimenting with Bedrock directly.
3. **Floci** stays useful throughout purely for S3 staging and practicing CLI/SDK calls for the
   services it does cover — don't skip it, just know its ceiling.

## Self-check before moving to Domain 2

You should be able to, without notes:
- Explain why the Online Store kept the `event_time=150` record in the Feature Store exercise
  above, not the one inserted last.
- Explain, in one sentence, why the disparate impact ratio computed in Lab 3 would concern a
  reviewer even though the model's overall accuracy might look fine.
- Run the Lab 4 RAG exercise with a *different* embedding model for the query than for the
  chunks, observe it still "works" but produces worse/irrelevant results, and explain why in your
  own words (mismatched embedding spaces) — this is deliberately reproducing the exam's favorite
  RAG trap on your own machine.
