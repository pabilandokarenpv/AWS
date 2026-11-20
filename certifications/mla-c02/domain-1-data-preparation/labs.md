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
| 7 | `pgvector`-on-Docker vs. FAISS — the real vector-DB tradeoff | Docker, Postgres + pgvector | Task 1.1.7 — configure vector DBs |
| 8 | PII detection and masking/redaction | Microsoft Presidio | Task 1.2.8 — mask/redact/anonymize |
| 9 | Outlier detection + near-duplicate text detection | scipy, datasketch (MinHash) | Task 1.3.7 — clean data |
| 10 | Build + validate FM fine-tuning prompt-completion pairs | plain Python, jsonschema | Task 1.2.9 / 1.3.6 — FM data prep & integrity |
| 11 | Feature engineering: encoding, scaling, interaction features | pandas, scikit-learn | Task 1.2 — feature engineering deep dive |
| 12 | Multimodal ingestion: OCR + transcription + image embeddings | pytesseract, SpeechRecognition, sentence-transformers | Task 1.1.8 / 1.2.5 — multimodal data prep |

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

## Lab 7 — `pgvector`-on-Docker vs. FAISS, the real vector-DB configuration tradeoff

```bash
docker run --name pgvector-demo -e POSTGRES_PASSWORD=demo -p 5432:5432 -d ankane/pgvector
pip install psycopg2-binary sentence-transformers
```

```python
import psycopg2
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres", password="demo")
cur = conn.cursor()
cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
cur.execute("CREATE TABLE IF NOT EXISTS chunks (id serial PRIMARY KEY, content text, embedding vector(384));")

chunks = [
    "The return policy allows refunds within 30 days of purchase.",
    "Shipping typically takes 3-5 business days within the country.",
    "Gift cards do not expire and are non-refundable.",
]
for c in chunks:
    emb = model.encode(c).tolist()
    cur.execute("INSERT INTO chunks (content, embedding) VALUES (%s, %s)", (c, emb))
conn.commit()

# Build an HNSW index -- the real configuration knob task statement 1.1.7 tests
cur.execute("CREATE INDEX IF NOT EXISTS chunks_hnsw ON chunks USING hnsw (embedding vector_cosine_ops);")
conn.commit()

query_emb = model.encode("How long do I have to return something?").tolist()
cur.execute("SELECT content, embedding <=> %s::vector AS distance FROM chunks ORDER BY distance LIMIT 1;",
            (query_emb,))
print("pgvector nearest match:", cur.fetchone())
```

This is the real `pgvector` HNSW index-creation step described in
`embeddings-and-rag-data-prep.md`'s vector database comparison — notice it required standing up a
real Postgres instance and an explicit `CREATE INDEX` statement, versus Lab 4's FAISS version
which needed neither a server nor an index-creation step. Running both labs back to back is the
fastest way to internalize *why* the comparison table calls `pgvector` "DBA overhead if you don't
already run Postgres" — you just did that overhead yourself, in miniature.

## Lab 8 — PII detection and masking/redaction (the real alternative to Comprehend PII + Macie)

```bash
pip install presidio-analyzer presidio-anonymizer
python -m spacy download en_core_web_lg
```

```python
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

text = "Hi, this is John Smith, SSN 078-05-1120, calling about my claim. Email me at john.smith@example.com."

analyzer = AnalyzerEngine()
results = analyzer.analyze(text=text, language="en")
print("Detected entities:", [(r.entity_type, r.start, r.end) for r in results])

anonymizer = AnonymizerEngine()

# Redaction -- delete entirely
redacted = anonymizer.anonymize(text=text, analyzer_results=results,
                                 operators={"DEFAULT": OperatorConfig("redact")})
print("Redacted:", redacted.text)

# Masking -- consistent, realistic-looking synthetic replacement
masked = anonymizer.anonymize(text=text, analyzer_results=results,
                               operators={"PERSON": OperatorConfig("replace", {"new_value": "Jane Doe"}),
                                          "DEFAULT": OperatorConfig("replace", {"new_value": "[MASKED]"})})
print("Masked:", masked.text)
```

Presidio (Microsoft's free, open-source PII toolkit) runs the exact same two-step pattern —
detect entities, then apply a redaction or masking operator — that Amazon Comprehend's PII
detection API performs as a managed service; this lab is a real, hands-on way to see the
redact-vs-mask distinction `README.md`'s "Masking, Redacting, and Anonymizing Data" section
describes, rather than only reading about it.

## Lab 9 — Outlier detection and near-duplicate text detection

```bash
pip install scipy datasketch
```

```python
import numpy as np
from scipy import stats

# Outlier detection via IQR -- the simple, single-feature method
values = np.array([42, 45, 41, 44, 43, 400, 46, 40])  # 400 is an obvious data-entry error
q1, q3 = np.percentile(values, [25, 75])
iqr = q3 - q1
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
outliers = values[(values < lower) | (values > upper)]
print("IQR bounds:", lower, upper, "-- outliers found:", outliers)
```

```python
from datasketch import MinHash, MinHashLSH

docs = {
    "ticket_1": "My order hasn't arrived and it's been two weeks.",
    "ticket_2": "My order has not arrived, it has been two weeks now.",   # near-duplicate of ticket_1
    "ticket_3": "I want to change my shipping address before it ships.",  # genuinely different
}

lsh = MinHashLSH(threshold=0.6, num_perm=128)
minhashes = {}
for key, text in docs.items():
    mh = MinHash(num_perm=128)
    for word in text.lower().split():
        mh.update(word.encode("utf8"))
    minhashes[key] = mh
    lsh.insert(key, mh)

print("Near-duplicates of ticket_1:", lsh.query(minhashes["ticket_1"]))
```

Run this and confirm `ticket_2` (a near-identical paraphrase) is flagged as a near-duplicate of
`ticket_1` while `ticket_3` is not — this is the exact MinHash/LSH mechanism
`README.md`'s "Cleaning Data" section names as the scalable alternative to exact-match
deduplication, here running on three documents instead of millions, but the same algorithm.

## Lab 10 — Building and validating FM fine-tuning prompt-completion pairs

```python
import json

# Build a small, deliberately-malformed-in-one-place fine-tuning dataset,
# to practice the integrity validation task statement 1.3.6 describes.
raw_pairs = [
    {"prompt": "Summarize: Our return policy allows 30-day refunds.", "completion": "30-day refund policy."},
    {"prompt": "Summarize: Shipping takes 3-5 business days.", "completion": "3-5 day shipping."},
    {"prompt": "Summarize: Gift cards never expire.", "completion": ""},   # empty completion -- a real defect
    {"prompt": "Summarize: Our return policy allows 30-day refunds.", "completion": "30-day refund policy."},  # exact duplicate of pair 1
]

def validate_pairs(pairs):
    seen = set()
    errors = []
    for i, pair in enumerate(pairs):
        if not pair.get("prompt") or not pair.get("completion"):
            errors.append(f"Pair {i}: empty prompt or completion -- drop before training.")
        key = (pair.get("prompt"), pair.get("completion"))
        if key in seen:
            errors.append(f"Pair {i}: exact duplicate of an earlier pair -- drop before training.")
        seen.add(key)
    return errors

issues = validate_pairs(raw_pairs)
for issue in issues:
    print("VALIDATION FAILURE:", issue)

clean_pairs = [p for i, p in enumerate(raw_pairs)
               if p.get("prompt") and p.get("completion")
               and raw_pairs.index(p) == i]  # keep only first occurrence of each pair
with open("fine_tune_data.jsonl", "w") as f:
    for p in clean_pairs[:2]:  # the two genuinely valid, unique pairs
        f.write(json.dumps(p) + "\n")
print("Wrote validated fine-tuning dataset: fine_tune_data.jsonl")
```

This deliberately reproduces both failure modes task statement 1.3.6 names — an empty/malformed
pair and an exact-duplicate pair — so you can see a validation script catch them *before* they'd
silently degrade a real Bedrock or SageMaker JumpStart fine-tuning job's quality.

## Lab 11 — Feature engineering: encoding, scaling, and interaction features

```bash
pip install pandas scikit-learn
```

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder

df = pd.DataFrame({
    "customer_id": range(1, 7),
    "age": [25, 42, 68, 31, 55, 90],
    "annual_income": [45000, 120000, 38000, 95000, 210000, 31000],
    "contract_type": ["month", "two-year", "month", "one-year", "two-year", "month"],
})

# 1. Standard (z-score) scaling -- puts age and income on a comparable scale
scaler = StandardScaler()
df[["age_scaled", "income_scaled"]] = scaler.fit_transform(df[["age", "annual_income"]])
print("Scaled age/income (mean 0, std 1):")
print(df[["age", "age_scaled", "annual_income", "income_scaled"]])

# 2. One-hot encoding -- contract_type has no natural order, so one-hot avoids implying one
encoded = pd.get_dummies(df["contract_type"], prefix="contract")
df = pd.concat([df, encoded], axis=1)

# 3. Interaction feature -- income per year of age, a ratio neither raw column exposes alone
df["income_per_age_year"] = df["annual_income"] / df["age"]

print("\nFinal engineered feature table:")
print(df[["customer_id", "age_scaled", "income_scaled", "contract_month",
          "contract_one-year", "contract_two-year", "income_per_age_year"]])
```

Run this and confirm the scaled columns have roughly mean 0 — this is the exact standard-scaling
mechanic `feature-engineering-deep-dive.md`'s Worked Example 2 walks through by hand with real
numbers; here it's the same math, computed by a library instead of arithmetic on paper.

**Extension — target encoding with k-fold leakage avoidance (the real, leak-free version):**

```python
from sklearn.model_selection import KFold
import numpy as np

# Simulate a high-cardinality categorical column + a binary label
np.random.seed(0)
n = 200
df2 = pd.DataFrame({
    "zip_code": np.random.choice([f"Z{i}" for i in range(40)], n),
    "churned": np.random.binomial(1, 0.2, n),
})

def kfold_target_encode(frame, cat_col, target_col, n_splits=5):
    frame = frame.copy()
    frame[f"{cat_col}_te"] = np.nan
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=0)
    for train_idx, val_idx in kf.split(frame):
        means = frame.iloc[train_idx].groupby(cat_col)[target_col].mean()
        frame.loc[frame.index[val_idx], f"{cat_col}_te"] = (
            frame.iloc[val_idx][cat_col].map(means)
        )
    # Fill any category unseen in a given fold's training split with the overall mean
    overall_mean = frame[target_col].mean()
    frame[f"{cat_col}_te"] = frame[f"{cat_col}_te"].fillna(overall_mean)
    return frame

encoded_df = kfold_target_encode(df2, "zip_code", "churned")
print("\nk-fold target-encoded zip_code (leak-free):")
print(encoded_df.head(10))
```

This reproduces the exact leakage-avoidance mechanic `feature-engineering-deep-dive.md`'s Worked
Example 1 describes in prose — each row's encoded value is computed only from *other* folds'
data, never including that row's own label, the real fix for the "unrealistically high validation
accuracy that collapses on fresh data" symptom that naive full-dataset target encoding produces.

## Lab 12 — Multimodal ingestion: OCR, speech-to-text, and image embeddings locally

```bash
pip install pytesseract pillow SpeechRecognition sentence-transformers
# pytesseract also requires the Tesseract OCR binary installed separately:
#   macOS: brew install tesseract   |   Ubuntu: sudo apt install tesseract-ocr
```

```python
# Stand-in for Amazon Textract: local OCR on an image containing text
from PIL import Image, ImageDraw, ImageFont
import pytesseract

# Create a simple synthetic "scanned form" image with text, for a reproducible local demo
img = Image.new("RGB", (400, 100), color="white")
draw = ImageDraw.Draw(img)
draw.text((10, 40), "Tracking Number: 1Z999AA10123456784", fill="black")
img.save("sample_form.png")

extracted_text = pytesseract.image_to_string(Image.open("sample_form.png"))
print("OCR-extracted text (Textract stand-in):", extracted_text.strip())
```

```python
# Stand-in for Amazon Transcribe: local speech-to-text on a short audio clip
# (requires a real .wav file in practice; this shows the exact API shape)
import speech_recognition as sr

recognizer = sr.Recognizer()
# with sr.AudioFile("sample_call.wav") as source:
#     audio = recognizer.record(source)
# transcript = recognizer.recognize_google(audio)
# print("Transcribed text (Transcribe stand-in):", transcript)
print("(Swap in a real .wav file to see this produce a real transcript locally,")
print(" using the exact same chunk-after-transcribe pattern Transcribe uses on AWS.)")
```

```python
# Stand-in for a multimodal embedding model: embedding both the OCR'd text AND
# a plain-text description into the SAME vector space, to search across both
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")
sources = {
    "ocr_tracking_number": extracted_text.strip(),
    "typed_complaint": "My package with tracking 1Z999AA10123456784 never arrived.",
    "unrelated_ticket": "How do I reset my account password?",
}
embeddings = {k: model.encode(v) for k, v in sources.items()}

query = "Where is my shipment with that tracking number?"
q_emb = model.encode(query)

for name, emb in embeddings.items():
    similarity = np.dot(q_emb, emb) / (np.linalg.norm(q_emb) * np.linalg.norm(emb))
    print(f"Similarity to '{name}': {similarity:.3f}")
```

Run this and confirm the query scores highest against `typed_complaint` and `ocr_tracking_number`
(both genuinely about the shipment) and lowest against `unrelated_ticket` — this is the exact
"OCR'd text and native text land in the same searchable space" mechanic
`multimodal-data-ingestion-patterns.md`'s Worked Pipeline 1 describes, reproduced locally with a
free embedding model standing in for Bedrock Titan Embeddings and a real (if synthetic) OCR step
standing in for Textract.

## What Floci can NOT do (and the real alternative)

| Need | Floci? | Use instead |
|---|---|---|
| Run a Glue ETL (Spark) transform job | ❌ no Spark backend | **AWS Glue Studio free trial on a real AWS account** (stays in free tier for small jobs), or run the equivalent transform locally with **pandas**/plain Python — same logic, no cluster |
| Visually explore data with bias reports (SageMaker Data Wrangler) | ❌ not emulated | **pandas-profiling / ydata-profiling** (free, local) for exploratory stats; **Fairlearn** (free, local) for bias/fairness metrics — conceptually the same checks Data Wrangler runs |
| SageMaker Feature Store (offline + online) | ❌ not emulated | **SageMaker Studio Lab** (free tier, no AWS account/credit card needed, real SageMaker notebook environment) to try Feature Store's actual API against a real (free-tier-eligible) SageMaker domain; for pure local practice, a plain SQLite/Parquet file plays the "offline store" role conceptually |
| Generate text embeddings | ❌ no Bedrock emulation | **`sentence-transformers`** (free, local, `pip install sentence-transformers`, e.g. `all-MiniLM-L6-v2` model) — produces real embeddings on your own machine, same concept as Titan Embeddings |
| Vector similarity search | ❌ not emulated | **FAISS** (free, local, `pip install faiss-cpu`) or Postgres + `pgvector` in a local Docker container |
| Run a real Glue Crawler against actual data | ❌ not emulated | Any small **AWS Free Tier** account — Glue Crawlers have a modest free tier suitable for learning-scale datasets |
| Configure a real OpenSearch/S3 Vector Buckets index at scale | ❌ not emulated | **Lab 7's local `pgvector`-on-Docker** for the real index-creation/configuration mechanics, or a small **AWS Free Tier** OpenSearch Serverless collection to see the managed-service console experience |
| Run Amazon Comprehend PII detection or Macie classification | ❌ not emulated | **Presidio** (`pip install presidio-analyzer presidio-anonymizer`, Lab 8) — the real open-source PII detection/anonymization library with an equivalent detect-then-redact-or-mask workflow |

## Use Cases — Real Scenarios

1. A new hire studying this domain runs Lab 1's Glue Data Catalog commands to understand exactly
   what a crawler registers, before ever touching a real AWS bill.
2. A data engineer prototypes an ETL pipeline's imputation and encoding logic in Lab 2's pandas
   script locally, in minutes, before committing to writing and running a paid Glue job.
3. A fairness reviewer runs Lab 3's Fairlearn disparate-impact check against a synthetic loan
   dataset to build intuition for what SageMaker Clarify's real pre-training bias report means,
   before interpreting one on an actual regulated dataset.
4. A solo developer builds Lab 4's local FAISS RAG pipeline to validate a chunking strategy on
   their own documents for free, before provisioning any real OpenSearch or Bedrock Knowledge
   Base infrastructure that starts billing immediately.
5. A platform team runs Lab 6's offline/online store simulation to train new engineers on the
   late-arriving-data gotcha before they ever touch a real SageMaker Feature Store and risk a
   production incident from the same mistake.
6. A compliance team uses Lab 7's `pgvector` index-creation exercise to decide, with real hands-on
   evidence rather than a vendor's marketing claim, whether their team can realistically operate a
   self-managed vector database or should default to a fully managed option instead.
7. A healthcare startup runs Lab 8's Presidio PII detection against sample intake forms to
   estimate, before any AWS spend, roughly how much manual review a real Comprehend PII rollout
   would still require for edge cases the automated detector misses.
8. A support operations lead runs Lab 9's MinHash deduplication against a sample of real
   historical tickets to quantify, with actual numbers, how much a RAG knowledge base's retrieval
   quality is currently being degraded by near-duplicate content before committing engineering
   time to a full cleanup project.
9. An ML engineer preparing a first Bedrock fine-tuning job runs Lab 10's validation script
   against their actual candidate dataset first, catching malformed or duplicate pairs for free
   instead of discovering the same problems only after a paid fine-tuning job underperforms.
10. A student preparing for the exam deliberately breaks Lab 4's embedding-model consistency (one
    model for chunks, a different one for the query) to personally witness the "mismatched
    embedding spaces" failure mode the exam tests conceptually, rather than only memorizing that
    it's a trap.

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
