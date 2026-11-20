# Domain 3 Labs — Deployment & Orchestration (Floci + Alternatives)

*Companion to [`README.md`](README.md). Floci has real strength here: ECS/EKS are Docker-backed
and CodePipeline-adjacent IAM/CloudFormation pieces are genuinely exercisable. What it does
**not** cover is SageMaker endpoints, SageMaker Pipelines, or Bedrock Agents/Knowledge Bases —
nothing emulates actual model-serving infrastructure.*

## What Floci can do here

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
```

## What Floci can NOT do (and the real alternative)

| Need | Floci? | Use instead |
|---|---|---|
| Deploy a real-time/serverless/async/batch SageMaker endpoint | ❌ not emulated | **SageMaker Studio Lab** for a real (free-tier) SageMaker endpoint deploy, or serve a model locally with **FastAPI + Uvicorn** wrapping a scikit-learn/PyTorch model — mirrors the "endpoint receiving requests" concept exactly |
| Run a SageMaker Pipeline (process → train → evaluate → register DAG) | ❌ not emulated | **Apache Airflow** (free, `pip install apache-airflow`, or Docker) or a plain **Makefile**/Python script chaining the same steps locally — same DAG concept, different orchestrator |
| Practice blue/green or canary deployment of a model endpoint | ❌ not emulated | Run two versions of a local FastAPI server on different ports and manually route a percentage of requests with a simple load balancer script (e.g., `nginx` config) — demonstrates the same traffic-shifting concept |
| Orchestrate a Bedrock Agent / Knowledge Base | ❌ no Bedrock emulation | **LangChain or LlamaIndex** (free, local, `pip install langchain`) with a local Hugging Face model standing in for the Bedrock-hosted foundation model — same "agent calls tools, chains steps" concept |
| SageMaker Neo edge compilation | ❌ not emulated | **ONNX Runtime** (free, local, `pip install onnxruntime`) to practice exporting/compiling a model for efficient inference — conceptually the same "compile once, run efficiently elsewhere" idea |

## Minimal local CI/CD-for-ML exercise (no AWS account needed)

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

@app.post("/predict")
def predict(features: list[float]):
    pred = model.predict(np.array(features).reshape(1, -1))
    return {"prediction": int(pred[0])}
```

```bash
python train_and_save.py
uvicorn serve:app --reload --port 8000
# curl -X POST localhost:8000/predict -H "Content-Type: application/json" -d "[5.1,3.5,1.4,0.2]"
```

This reproduces the "train → package → serve behind an HTTP endpoint" shape of Domain 3 end to
end locally, before translating the same steps to real SageMaker Pipelines/endpoints.

## Recommended real-AWS free tier path

1. **SageMaker Studio Lab** for a real (free) SageMaker endpoint deploy experience.
2. **AWS Free Tier account** for CodePipeline/CodeBuild (both have a modest free tier) to
   practice the actual CI/CD trigger chain end to end.
3. **Floci** for ECR/ECS/CloudFormation practice around the pipeline, and for the IAM roles a
   real pipeline would assume.
