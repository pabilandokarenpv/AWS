# Domain 3 Labs — Deployment & Orchestration (Floci + Alternatives)

*Companion to [`README.md`](README.md). Floci has real strength here: ECS/EKS are Docker-backed
and CodePipeline-adjacent IAM/CloudFormation pieces are genuinely exercisable. What it does
**not** cover is SageMaker endpoints, SageMaker Pipelines, or Bedrock Agents/Knowledge Bases —
nothing emulates actual model-serving infrastructure.*

## Lab map

| # | Lab | Tooling | Maps to |
|---|---|---|---|
| 1 | ECR/ECS + CloudFormation around a pipeline | Floci | Task 3.2/3.3 infra |
| 2 | Train → package → serve behind a real HTTP endpoint | FastAPI, scikit-learn | Task 3.1 |
| 3 | A local DAG runner standing in for SageMaker Pipelines | Airflow or plain Makefile | Task 3.3 |
| 4 | Blue/green and canary traffic shifting, simulated locally | nginx or a small Python router | Task 3.1/3.3 |
| 5 | A minimal local Agent (tool-calling) | LangChain + local model | Task 3.4 |
| 6 | SageMaker Neo stand-in: export/compile for efficient inference | ONNX Runtime | Task 3.1 (edge) |
| 7 | Agent state management with a local key-value store | SQLite | Task 3.2.9 — agent state |
| 8 | Prompt version testing harness | plain Python, pytest | Task 3.3.7/3.3.9 — Prompt Management & testing |

## Lab 1 — What Floci can do here

- Build/push a container image concept to **ECR**, run it on **ECS** (real Docker-backed), and
  practice **CloudFormation** templates for the surrounding infrastructure (IAM roles, Auto
  Scaling-adjacent resources).

```bash
alias awslocal='aws --endpoint-url=http://localhost:4566 --profile floci'

# Practice the container registry + ECS pieces of the pipeline
awslocal ecr create-repository --repository-name ml-inference-demo
awslocal ecs create-cluster --cluster-name ml-inference-cluster

# Practice IaC for the surrounding infra
awslocal cloudformation deploy \
  --template-file inference-infra.yaml \
  --stack-name ml-inference-stack

# Practice EventBridge rule shape (not real SageMaker Pipeline triggering)
awslocal events put-rule --name new-data-arrival \
  --event-pattern '{"source":["aws.s3"],"detail-type":["Object Created"]}'
awslocal events put-targets --rule new-data-arrival \
  --targets '[{"Id":"1","Arn":"arn:aws:lambda:us-east-1:000000000000:function:trigger-retrain"}]'
```

## Lab 2 — Train → package → serve (the real alternative to a SageMaker real-time endpoint)

```bash
pip install fastapi uvicorn scikit-learn joblib
```

```python
# train_and_save.py — stands in for the "train" step of a SageMaker Pipeline
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import joblib

X, y = load_iris(return_X_y=True)
model = RandomForestClassifier().fit(X, y)
joblib.dump(model, "model.joblib")
print("Model trained and saved — this step would be a SageMaker Pipeline 'Train' step")
```

```python
# serve.py — stands in for a SageMaker real-time endpoint
from fastapi import FastAPI
import joblib, numpy as np

app = FastAPI()
model = joblib.load("model.joblib")

@app.get("/ping")
def ping():
    # mirrors SageMaker's required health-check contract for a custom container
    return {"status": "healthy"}

@app.post("/invocations")
def predict(features: list[float]):
    pred = model.predict(np.array(features).reshape(1, -1))
    return {"prediction": int(pred[0])}
```

```bash
python train_and_save.py
uvicorn serve:app --reload --port 8000
# curl localhost:8000/ping
# curl -X POST localhost:8000/invocations -H "Content-Type: application/json" -d "[5.1,3.5,1.4,0.2]"
```

Naming the endpoints `/ping` and `/invocations` is deliberate — this is literally the contract a
real SageMaker Bring Your Own Container must implement, so this lab is directly transferable
vocabulary, not just a loose analogy.

## Lab 3 — A local DAG runner standing in for a SageMaker Pipeline

```bash
pip install apache-airflow  # or skip Airflow and use the Makefile version below
```

**Option A — a plain Makefile DAG (zero extra dependencies):**

```makefile
# Makefile — mirrors a SageMaker Pipeline's process -> train -> evaluate -> register steps
.PHONY: all process train evaluate register

all: register

process:
	python process_data.py

train: process
	python train_and_save.py

evaluate: train
	python evaluate_model.py  # should exit non-zero if metrics are below threshold

register: evaluate
	python register_model.py  # only runs if evaluate succeeded
```

```bash
make register
```

Because `make` stops the chain the moment any step's script exits non-zero, this reproduces the
Condition Step's "stop the pipeline if quality doesn't clear the bar" behavior with nothing more
than standard Unix tooling — a useful, dependency-free way to internalize the DAG concept before
reading SageMaker Pipelines' Python SDK syntax.

**Option B — Airflow** (closer to a real production orchestrator, heavier to set up): define the
same four steps as an Airflow DAG with `>>` dependency operators; Airflow's UI additionally gives
you the visual DAG view SageMaker Studio's Pipelines tab provides for the real service.

## Lab 4 — Simulating blue/green and canary deployments locally

```python
# router.py — a deliberately simplified canary router in front of two local model servers
import random
from fastapi import FastAPI
import httpx

app = FastAPI()
CANARY_TRAFFIC_PERCENT = 10  # 10% of requests go to the "new" version

@app.post("/invocations")
async def route(payload: dict):
    target_port = 8001 if random.random() * 100 < CANARY_TRAFFIC_PERCENT else 8000
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"http://localhost:{target_port}/invocations", json=payload)
    return {"served_by": f"port_{target_port}", **resp.json()}
```

Run two instances of Lab 2's `serve.py` on ports 8000 (the "old" model) and 8001 (the "new"
model), then run this router in front of both on port 9000. Gradually raise
`CANARY_TRAFFIC_PERCENT` from 10 toward 100 over several test runs — this is the exact "ramp up
traffic to the new version only if it behaves well" pattern a real SageMaker canary deployment
automates, just driven by hand here instead of a managed deployment configuration.

## Lab 5 — A minimal local Agent (tool-calling), the free alternative to Bedrock Agents

```bash
pip install langchain langchain-community transformers torch
```

```python
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline

def get_order_status(order_id: str) -> str:
    # stands in for a real Lambda-backed tool call
    return f"Order {order_id} is out for delivery, arriving today."

def search_return_policy(query: str) -> str:
    # stands in for a Knowledge Base / RAG retrieval call
    return "Electronics can be returned within 30 days of purchase with original packaging."

tools = [
    Tool(name="OrderStatus", func=get_order_status,
         description="Look up the live delivery status for an order ID."),
    Tool(name="ReturnPolicy", func=search_return_policy,
         description="Answer questions about the return policy from company documents."),
]

llm = HuggingFacePipeline(pipeline=pipeline("text2text-generation", model="google/flan-t5-base"))
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

print(agent.run("What's the status of order 12345, and can I return it if I don't like it?"))
```

This reproduces the exact two-tool orchestration pattern shown in Domain 1's
`embeddings-and-rag-data-prep.md` sequence diagram — a tool call for live state plus a retrieval
call for policy — with LangChain's agent framework and a small free local model standing in for
Bedrock's Agent + Knowledge Base + foundation model combination.

## Lab 6 — SageMaker Neo stand-in: compiling a model for efficient inference

```bash
pip install skl2onnx onnxruntime
```

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import onnxruntime as rt
import numpy as np

X, y = load_iris(return_X_y=True)
model = RandomForestClassifier().fit(X, y)

# "Compile" the model to ONNX — conceptually the same idea as SageMaker Neo
onnx_model = convert_sklearn(model, initial_types=[("input", FloatTensorType([None, 4]))])
with open("model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())

# Run inference using the compiled artifact, on a lightweight runtime
sess = rt.InferenceSession("model.onnx")
pred = sess.run(None, {"input": np.array([[5.1, 3.5, 1.4, 0.2]], dtype=np.float32)})
print("ONNX Runtime prediction:", pred[0])
```

Just as SageMaker Neo compiles a trained model into an optimized form for a target edge runtime
(paired with IoT Greengrass to actually execute it), this exports the same model into ONNX's
portable, optimized format and runs it with a lightweight runtime — the same "compile once, run
efficiently elsewhere" idea, achievable entirely for free and locally.

## Lab 7 — Agent state management with a local key-value store

```python
# agent_state.py -- a minimal stand-in for a DynamoDB-backed agent session store
import sqlite3, json

conn = sqlite3.connect("agent_sessions.db")
conn.execute("CREATE TABLE IF NOT EXISTS sessions (session_id TEXT PRIMARY KEY, state TEXT)")

def load_state(session_id):
    row = conn.execute("SELECT state FROM sessions WHERE session_id = ?", (session_id,)).fetchone()
    return json.loads(row[0]) if row else {"task": None, "status": "new"}

def save_state(session_id, state):
    conn.execute("INSERT OR REPLACE INTO sessions (session_id, state) VALUES (?, ?)",
                 (session_id, json.dumps(state)))
    conn.commit()

session_id = "user_42_session_1"

# Turn 1
state = load_state(session_id)
state.update({"task": "book_flight", "destination": "Chicago", "date": "next Friday", "status": "searching"})
save_state(session_id, state)
print("After turn 1:", load_state(session_id))

# Turn 2 -- a SEPARATE "request", simulating a new process loading the same session
state = load_state(session_id)
state["date"] = "Thursday"  # user corrected the date
save_state(session_id, state)
print("After turn 2 (loaded fresh, not carried in memory):", load_state(session_id))

# Turn 3 -- confirm the state (destination, date) survived across independent loads
state = load_state(session_id)
assert state["destination"] == "Chicago" and state["date"] == "Thursday"
print("Turn 3 confirms state persisted correctly across independent 'requests'.")
```

Run this twice in two separate Python processes (not just two function calls in the same
script) to really prove the point `README.md`'s agent-state-management section makes: state
survives because it's read from and written to external storage on every turn, not because
anything is held in a single process's memory — exactly the property a real DynamoDB-backed
Bedrock Agent session needs across requests that may hit different compute instances.

## Lab 8 — A prompt version testing harness, the free alternative to Bedrock Prompt Management + automated eval gating

```bash
pip install pytest
```

```python
# prompt_versions.py
PROMPTS = {
    "v1": "Summarize this customer complaint in one sentence: {text}",
    "v2": "Summarize this customer complaint in one sentence, naming the product if mentioned: {text}",
}

def render(version, text):
    return PROMPTS[version].format(text=text)
```

```python
# test_prompts.py -- an automated gate a real agent-deployment pipeline would run before promotion
from prompt_versions import render

TEST_CASES = [
    {"text": "My WidgetPro 3000 broke after a week and nobody has answered my emails.",
     "must_mention": "WidgetPro"},
]

def fake_model_call(prompt):
    # stands in for a real Bedrock InvokeModel call during the test
    if "name the product" in prompt.lower() or "naming the product" in prompt.lower():
        return "Customer's WidgetPro 3000 broke and support hasn't responded."
    return "Customer's product broke and support hasn't responded."

def test_v2_mentions_product_name():
    for case in TEST_CASES:
        prompt = render("v2", case["text"])
        output = fake_model_call(prompt)
        assert case["must_mention"] in output, f"v2 failed to mention product name: {output!r}"

def test_v1_does_not_reliably_mention_product_name():
    for case in TEST_CASES:
        prompt = render("v1", case["text"])
        output = fake_model_call(prompt)
        assert case["must_mention"] not in output, "v1 unexpectedly mentioned the product name"
```

```bash
pytest test_prompts.py -v
```

This reproduces the exact "automated eval suite gates a new prompt version before promotion"
pattern from `README.md`'s Prompt Management diagram — `v2` passes its test (an improvement over
`v1`) and would be promoted to production; a hypothetical `v3` that *failed* a test like this
would be rejected automatically, exactly like the diagram's "scores acceptable?" branch, with no
production traffic ever reaching the rejected version.

## What Floci can NOT do (and the real alternative)

| Need | Floci? | Use instead |
|---|---|---|
| Deploy a real-time/serverless/async/batch SageMaker endpoint | ❌ not emulated | **SageMaker Studio Lab** for a real (free-tier) SageMaker endpoint deploy, or serve a model locally with **FastAPI + Uvicorn** wrapping a scikit-learn/PyTorch model — mirrors the "endpoint receiving requests" concept exactly |
| Run a SageMaker Pipeline (process → train → evaluate → register DAG) | ❌ not emulated | **Apache Airflow** (free, `pip install apache-airflow`, or Docker) or a plain **Makefile**/Python script chaining the same steps locally — same DAG concept, different orchestrator |
| Practice blue/green or canary deployment of a model endpoint | ❌ not emulated | Run two versions of a local FastAPI server on different ports and manually route a percentage of requests with a simple load balancer script (e.g., `nginx` config) — demonstrates the same traffic-shifting concept |
| Orchestrate a Bedrock Agent / Knowledge Base | ❌ no Bedrock emulation | **LangChain or LlamaIndex** (free, local, `pip install langchain`) with a local Hugging Face model standing in for the Bedrock-hosted foundation model — same "agent calls tools, chains steps" concept |
| SageMaker Neo edge compilation | ❌ not emulated | **ONNX Runtime** (free, local, `pip install onnxruntime`) to practice exporting/compiling a model for efficient inference — conceptually the same "compile once, run efficiently elsewhere" idea |
| Auto Scaling policies on a real endpoint | ❌ not emulated | Reason through the policy's math by hand (target tracking: desired instance count to keep a metric like CPU utilization near a target value) — AWS's Application Auto Scaling documentation's worked examples are a good free substitute for hands-on practice |
| Bedrock Prompt Management's version history/promotion UI | ❌ no Bedrock emulation | **Lab 8's plain Python dict + pytest harness** — the same version-then-test-then-promote workflow, minus the managed console |
| A real DynamoDB-backed agent session store | ❌ not emulated | **Lab 7's SQLite-backed store** — the same external, durable key-value persistence pattern, run locally and for free |

## Use Cases — Real Scenarios

1. An engineer new to this domain runs Lab 2's `/ping`/`/invocations` FastAPI server first,
   specifically because implementing that exact contract by hand makes the real SageMaker BYOC
   health-check requirement concrete instead of an abstract rule to memorize.
2. A small team adopts Lab 3's Makefile DAG for their first automated retraining pipeline,
   deliberately choosing it over Airflow because their team's actual scale doesn't yet justify
   Airflow's operational overhead — a direct real-world instance of not over-engineering.
3. A platform engineer runs Lab 4's canary router at increasing traffic percentages against two
   real model versions before ever configuring a production SageMaker canary deployment, building
   confidence in the ramp-up logic on infrastructure they fully control.
4. A solo founder prototypes their support bot's tool-calling logic in Lab 5's LangChain agent
   against a free local model, validating the two-tool orchestration pattern works before paying
   for any real Bedrock Agent usage.
5. An ML engineer runs Lab 6's ONNX export to estimate how much a model shrinks and speeds up
   before compiling, giving a real number to justify (or rule out) investing in SageMaker Neo for
   a specific edge deployment.
6. A team debugging a "forgetful" chatbot in production reproduces Lab 7's two-separate-process
   experiment locally first, to build confidence that the state-persistence pattern itself is
   sound before looking for the bug elsewhere in their real DynamoDB integration.
7. A content team uses Lab 8's pytest harness to gate every prompt change going into their
   production assistant, catching a regression (a prompt edit that stopped including required
   safety language) before it ever reached a real deployment pipeline.
8. A compliance-focused team extends Lab 8 with additional test cases specifically covering
   required disclosures, treating prompt tests with the same seriousness as code unit tests
   rather than as an afterthought.
9. A developer evaluating whether to self-host a fine-tuned model on GPU or use Bedrock
   Provisioned Throughput runs Lab 2's FastAPI server under Lab 4's load-testing-adjacent router
   to estimate real throughput numbers on their own hardware before making the cost comparison.
10. A student preparing for the exam intentionally breaks Lab 7's session-ID handling (hardcoding
    a different session ID on "turn 2") to personally witness the exact "state looks lost" failure
    mode the README's agent-state-management exam trap describes.

## Recommended real-AWS free tier path

1. **SageMaker Studio Lab** for a real (free) SageMaker endpoint deploy experience.
2. **AWS Free Tier account** for CodePipeline/CodeBuild (both have a modest free tier) to
   practice the actual CI/CD trigger chain end to end.
3. **Floci** for ECR/ECS/CloudFormation practice around the pipeline, and for the IAM roles a
   real pipeline would assume.

## Self-check before moving to Domain 4

- Given a one-sentence traffic description, can you place it correctly on the Domain 3 README's
  inference-option decision tree without hesitating?
- Can you explain, from Lab 4's router code, what specifically would need to change to turn a
  canary deployment into a full blue/green cutover?
- Can you explain in your own words why Lab 5's Agent needed two separate tools rather than one
  combined tool, and how that maps to the Knowledge Base vs. Agent distinction from Domain 1?
