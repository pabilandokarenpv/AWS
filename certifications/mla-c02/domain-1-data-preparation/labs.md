# Domain 1 Labs — Data Preparation (Floci + Alternatives)

*Companion to [`README.md`](README.md). Honest note up front: Floci emulates AWS **control-plane
APIs** (S3, Glue's catalog API, Kinesis streams). It does **not** run Glue Spark jobs, SageMaker
Data Wrangler transforms, Feature Store's real backing stores, or any embedding/foundation model
inference. Use Floci for what it's good at (S3 staging, API shape practice) and the alternatives
below for anything that needs real ML compute.*

## What Floci can do here

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
```

## What Floci can NOT do (and the real alternative)

| Need | Floci? | Use instead |
|---|---|---|
| Run a Glue ETL (Spark) transform job | ❌ no Spark backend | **AWS Glue Studio free trial on a real AWS account** (stays in free tier for small jobs), or run the equivalent transform locally with **pandas**/plain Python — same logic, no cluster |
| Visually explore data with bias reports (SageMaker Data Wrangler) | ❌ not emulated | **pandas-profiling / ydata-profiling** (free, local) for exploratory stats; **Fairlearn** (free, local) for bias/fairness metrics — conceptually the same checks Data Wrangler runs |
| SageMaker Feature Store (offline + online) | ❌ not emulated | **SageMaker Studio Lab** (free tier, no AWS account/credit card needed, real SageMaker notebook environment) to try Feature Store's actual API against a real (free-tier-eligible) SageMaker domain; for pure local practice, a plain SQLite/Parquet file plays the "offline store" role conceptually |
| Generate text embeddings | ❌ no Bedrock emulation | **`sentence-transformers`** (free, local, `pip install sentence-transformers`, e.g. `all-MiniLM-L6-v2` model) — produces real embeddings on your own machine, same concept as Titan Embeddings |
| Vector similarity search | ❌ not emulated | **FAISS** (free, local, `pip install faiss-cpu`) or Postgres + `pgvector` in a local Docker container |

## Minimal local RAG exercise (no AWS account needed)

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
```

This is the exact mechanism `embeddings-and-rag-data-prep.md` describes — chunk, embed, store,
embed the query, nearest-neighbor search — just running on your laptop instead of against
Bedrock + OpenSearch. Once this makes sense, the jump to "swap `SentenceTransformer` for a
Bedrock `InvokeModel` embeddings call, and FAISS for OpenSearch Serverless" is conceptual, not
new mechanics.

## Recommended real-AWS free tier path

1. **SageMaker Studio Lab** (https://studiolab.sagemaker.aws) — free, no credit card, no AWS
   account required, gives you a real JupyterLab environment with GPU hours/day for free. Best
   place to actually run SageMaker Data Wrangler-style exploration and small training jobs.
2. **AWS Free Tier account** (if/when you do want real Glue/Kinesis/Bedrock) — Glue has a small
   free tier for crawler/catalog requests; Bedrock charges per token from the first call (no
   meaningful free tier) — budget a few dollars before experimenting with Bedrock directly.
3. **Floci** stays useful throughout purely for S3 staging and practicing CLI/SDK calls for the
   services it does cover — don't skip it, just know its ceiling.
