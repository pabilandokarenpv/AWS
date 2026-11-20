# Domain 2 Labs — Model Development (Floci + Alternatives)

*Companion to [`README.md`](README.md). Honest note up front: Floci emulates control-plane APIs
(IAM, S3, Lambda) — it does **not** run SageMaker training jobs, Automatic Model Tuning, or
Bedrock foundation model inference/fine-tuning. There is no local emulator for actual ML
compute; the real alternatives below run real training, just on free or local resources instead
of paid SageMaker infrastructure.*

## What Floci can do here

- Stage training data and model artifacts in S3 (the input/output locations a real SageMaker
  Training Job would read from and write to) and practice the IAM role/policy a training job
  would assume.

```bash
alias awslocal='aws --endpoint-url=http://localhost:4566 --profile floci'

awslocal s3 mb s3://ml-model-artifacts
awslocal iam create-role --role-name SageMakerExecutionRole-Practice \
  --assume-role-policy-document file://trust-policy.json
```

## What Floci can NOT do (and the real alternative)

| Need | Floci? | Use instead |
|---|---|---|
| Run an actual SageMaker built-in algorithm or script-mode training job | ❌ not emulated | **SageMaker Studio Lab** (free, no AWS account/card, real training environment with free GPU hours/day) — run the real `sagemaker` Python SDK against it |
| Practice hyperparameter tuning (Automatic Model Tuning) | ❌ not emulated | Run **scikit-learn's `GridSearchCV` / `RandomizedSearchCV`** or **Optuna** (free, local, Bayesian-style search) on a small dataset — same concept (systematic search over hyperparameter space), different infra |
| Diagnose overfitting/underfitting on a real training curve | ❌ not emulated | Train any small model locally with **scikit-learn** or **PyTorch** on a public dataset (e.g., `sklearn.datasets`) and plot train vs. validation loss with `matplotlib` — the exact curves `ml-fundamentals-glossary.md` describes |
| Access/fine-tune a foundation model (Bedrock/JumpStart) | ❌ no Bedrock/JumpStart emulation | **Hugging Face free inference** (`transformers` library, small open models like `distilbert`/`flan-t5-small` run on CPU) to practice the *concept* of prompting and lightweight fine-tuning; **SageMaker JumpStart's free-tier-eligible smaller models** via Studio Lab for something closer to the real AWS workflow |
| Register/version models (Model Registry) | ❌ not emulated | Treat a local `models/` folder with a simple CSV/JSON "registry" (model name, version, metrics, approval status) as a stand-in for the concept — or use **MLflow** (free, local or Docker) which has a real, open-source Model Registry with the same approve/stage/version workflow |

## Minimal local train/evaluate/tune exercise (no AWS account needed)

```bash
pip install scikit-learn matplotlib
```

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

X, y = load_breast_cancer(return_X_y=True)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# "Hyperparameter tuning" — the local equivalent of SageMaker Automatic Model Tuning
param_grid = {"n_estimators": [50, 100, 200], "max_depth": [3, 5, None]}
search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=3)
search.fit(X_train, y_train)

best_model = search.best_estimator_
preds = best_model.predict(X_val)
probs = best_model.predict_proba(X_val)[:, 1]

print("Best params:", search.best_params_)
print(confusion_matrix(y_val, preds))          # the confusion matrix, for real
print(classification_report(y_val, preds))      # precision, recall, F1 per class
print("AUC:", roc_auc_score(y_val, probs))
```

Running this with `max_depth=None` and many estimators, then comparing training accuracy
(`best_model.score(X_train, y_train)`) against validation accuracy, is a hands-on way to
reproduce the overfitting signature from `ml-fundamentals-glossary.md` directly.

## Recommended real-AWS free tier path

1. **SageMaker Studio Lab** for the closest free experience to real SageMaker training/tuning
   workflows.
2. **AWS Free Tier account** for a genuinely tiny, cheap Bedrock fine-tuning/inference experiment
   once comfortable with costs (Bedrock has no meaningful free tier — budget a few dollars).
3. **Floci** for S3 artifact staging and IAM role practice around the training job, not the
   training itself.
