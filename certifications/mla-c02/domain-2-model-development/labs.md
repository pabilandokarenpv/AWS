# Domain 2 Labs — Model Development (Floci + Alternatives)

*Companion to [`README.md`](README.md). Honest note up front: Floci emulates control-plane APIs
(IAM, S3, Lambda) — it does **not** run SageMaker training jobs, Automatic Model Tuning, or
Bedrock foundation model inference/fine-tuning. There is no local emulator for actual ML
compute; the real alternatives below run real training, just on free or local resources instead
of paid SageMaker infrastructure.*

## Lab map

| # | Lab | Tooling | Maps to |
|---|---|---|---|
| 1 | S3/IAM staging for a training job | Floci | Infrastructure around 2.1/2.2 |
| 2 | Train + evaluate a classifier, full metrics | scikit-learn | Task 2.2/2.3 |
| 3 | Hyperparameter tuning: grid vs. random vs. Bayesian | scikit-learn, Optuna | Task 2.2 |
| 4 | Reproduce overfitting/underfitting on a real learning curve | scikit-learn, matplotlib | Task 2.3 |
| 5 | Prompt a local open model, then "fine-tune" conceptually | Hugging Face `transformers` | Task 2.1/2.2 (FM) |
| 6 | A minimal local Model Registry | MLflow or a CSV stand-in | Task 2.4 |

## Lab 1 — What Floci can do here

- Stage training data and model artifacts in S3 (the input/output locations a real SageMaker
  Training Job would read from and write to) and practice the IAM role/policy a training job
  would assume.

```bash
alias awslocal='aws --endpoint-url=http://localhost:4566 --profile floci'

awslocal s3 mb s3://ml-model-artifacts
awslocal iam create-role --role-name SageMakerExecutionRole-Practice \
  --assume-role-policy-document file://trust-policy.json
awslocal iam put-role-policy --role-name SageMakerExecutionRole-Practice \
  --policy-name ReadTrainWriteModel --policy-document file://s3-rw-policy.json
```

## Lab 2 — Train/evaluate a real classifier, with every metric from the glossary

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

# Compare against the training set itself, to see overfitting signal directly
print("Train accuracy:", best_model.score(X_train, y_train))
print("Val accuracy:  ", best_model.score(X_val, y_val))
```

Running this with `max_depth=None` and many estimators, then comparing training accuracy
against validation accuracy, is a hands-on way to reproduce the overfitting signature from
`ml-fundamentals-glossary.md` directly. Deliberately set `max_depth=1` and re-run to reproduce
underfitting instead — both numbers should now be mediocre and close together, the opposite
signature.

## Lab 3 — Grid vs. random vs. Bayesian search, timed and compared

```bash
pip install optuna
```

```python
import time
import optuna
from sklearn.model_selection import cross_val_score, RandomizedSearchCV, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_breast_cancer

X, y = load_breast_cancer(return_X_y=True)

# Grid search — exhaustive
t0 = time.time()
grid = GridSearchCV(RandomForestClassifier(random_state=42),
                     {"n_estimators": [50, 100, 150, 200], "max_depth": [3, 5, 7, None]}, cv=3)
grid.fit(X, y)
print(f"Grid search: {len(grid.cv_results_['params'])} combos tried, "
      f"best={grid.best_score_:.4f}, took {time.time()-t0:.1f}s")

# Random search — sampled
t0 = time.time()
rand = RandomizedSearchCV(RandomForestClassifier(random_state=42),
                           {"n_estimators": range(50, 300), "max_depth": [3, 5, 7, 9, None]},
                           n_iter=12, cv=3, random_state=42)
rand.fit(X, y)
print(f"Random search: 12 combos tried, best={rand.best_score_:.4f}, took {time.time()-t0:.1f}s")

# Bayesian search (Optuna) — adaptive
def objective(trial):
    n_estimators = trial.suggest_int("n_estimators", 50, 300)
    max_depth = trial.suggest_categorical("max_depth", [3, 5, 7, 9, None])
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    return cross_val_score(model, X, y, cv=3).mean()

t0 = time.time()
study = optuna.create_study(direction="maximize")
study.optimize(objective, n_trials=12)
print(f"Bayesian (Optuna): 12 trials, best={study.best_value:.4f}, took {time.time()-t0:.1f}s")
```

Run this and compare: Bayesian search with the *same* trial budget as random search (12 trials
each) typically reaches a comparable or better best score, because each new trial is chosen using
information from prior trials rather than sampled blindly — a direct, hands-on confirmation of
the sample-efficiency table in `ml-fundamentals-glossary.md`.

## Lab 4 — Reproducing a real overfitting learning curve

```python
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=300, n_features=20, n_informative=5, random_state=42)

train_sizes, train_scores, val_scores = learning_curve(
    DecisionTreeClassifier(max_depth=None, random_state=42),  # deliberately unconstrained -> overfits
    X, y, cv=5, train_sizes=[0.1, 0.3, 0.5, 0.7, 1.0],
)

plt.plot(train_sizes, train_scores.mean(axis=1), label="Training score")
plt.plot(train_sizes, val_scores.mean(axis=1), label="Validation score")
plt.xlabel("Training set size")
plt.ylabel("Accuracy")
plt.legend()
plt.title("Overfitting signature: training score stays near 1.0, validation score lags behind")
plt.savefig("learning_curve.png")
print("Saved learning_curve.png — training score should sit near 1.0 while validation lags.")
```

Re-run with `max_depth=3` (a constrained, simpler tree) and compare — the gap between the two
curves should shrink substantially, the visual signature of trading variance for bias.

## Lab 5 — Local foundation-model prompting (free, CPU-only, no Bedrock account needed)

```bash
pip install transformers torch --quiet
```

```python
from transformers import pipeline

# A small, free, open model standing in for a Bedrock foundation model
generator = pipeline("text2text-generation", model="google/flan-t5-small")

prompt = "Summarize in one sentence: SageMaker lets you train, tune, deploy, and monitor ML models without managing your own infrastructure."
result = generator(prompt, max_new_tokens=40)
print(result[0]["generated_text"])

# Few-shot prompting — the cheapest customization lever, per the glossary/README decision tree
few_shot_prompt = """Classify the sentiment as positive or negative.
Review: "Shipping was fast and the product works great." Sentiment: positive
Review: "It broke after one day and support never responded." Sentiment: negative
Review: "Decent for the price, nothing special." Sentiment:"""
result = generator(few_shot_prompt, max_new_tokens=5)
print(result[0]["generated_text"])
```

This is conceptually identical to calling Bedrock's `InvokeModel` with a prompt — same mechanics
(tokenize, generate, decode), different (free, local, smaller) model behind the API shape. It's
the right first lab before attempting any real fine-tuning, since prompt engineering is the
cheapest lever on the Domain 2 README's fine-tuning decision diagram.

## Lab 6 — A minimal local Model Registry

```bash
pip install mlflow
```

```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

X, y = load_breast_cancer(return_X_y=True)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

mlflow.set_experiment("churn-detector")
with mlflow.start_run():
    model = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train, y_train)
    preds = model.predict(X_val)
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", accuracy_score(y_val, preds))
    mlflow.log_metric("f1", f1_score(y_val, preds))
    mlflow.sklearn.log_model(model, "model")
    print("Logged a versioned run — this is the open-source analog of SageMaker Model Registry.")
```

Run `mlflow ui` afterward to browse logged runs, parameters, and metrics side by side in a
browser — the same conceptual "version, compare, and (with MLflow's Model Registry feature)
approve/stage" workflow SageMaker's Model Registry provides, running entirely locally and for
free.

## What Floci can NOT do (and the real alternative)

| Need | Floci? | Use instead |
|---|---|---|
| Run an actual SageMaker built-in algorithm or script-mode training job | ❌ not emulated | **SageMaker Studio Lab** (free, no AWS account/card, real training environment with free GPU hours/day) — run the real `sagemaker` Python SDK against it |
| Practice hyperparameter tuning (Automatic Model Tuning) | ❌ not emulated | Run **scikit-learn's `GridSearchCV` / `RandomizedSearchCV`** or **Optuna** (free, local, Bayesian-style search) on a small dataset — same concept (systematic search over hyperparameter space), different infra |
| Diagnose overfitting/underfitting on a real training curve | ❌ not emulated | Train any small model locally with **scikit-learn** or **PyTorch** on a public dataset (e.g., `sklearn.datasets`) and plot train vs. validation loss with `matplotlib` — the exact curves `ml-fundamentals-glossary.md` describes |
| Access/fine-tune a foundation model (Bedrock/JumpStart) | ❌ no Bedrock/JumpStart emulation | **Hugging Face free inference** (`transformers` library, small open models like `distilbert`/`flan-t5-small` run on CPU) to practice the *concept* of prompting and lightweight fine-tuning; **SageMaker JumpStart's free-tier-eligible smaller models** via Studio Lab for something closer to the real AWS workflow |
| Register/version models (Model Registry) | ❌ not emulated | Treat a local `models/` folder with a simple CSV/JSON "registry" (model name, version, metrics, approval status) as a stand-in for the concept — or use **MLflow** (free, local or Docker) which has a real, open-source Model Registry with the same approve/stage/version workflow |
| Detect bias in a trained model's predictions (Clarify-style) | ❌ not emulated | **Fairlearn** (free, local, `pip install fairlearn`) — see Domain 1's `labs.md` Lab 3 for a worked example of the same technique |

## Recommended real-AWS free tier path

1. **SageMaker Studio Lab** for the closest free experience to real SageMaker training/tuning
   workflows.
2. **AWS Free Tier account** for a genuinely tiny, cheap Bedrock fine-tuning/inference experiment
   once comfortable with costs (Bedrock has no meaningful free tier — budget a few dollars).
3. **Floci** for S3 artifact staging and IAM role practice around the training job, not the
   training itself.

## Self-check before moving to Domain 3

- Can you look at a `learning_curve.png` from Lab 4 (yours or a colleague's) and immediately say
  whether it shows overfitting, underfitting, or a good fit?
- Can you explain, from the Lab 3 timing output, why Bayesian search reached a comparable score to
  grid search while trying far fewer combinations?
- Can you explain in one sentence why Lab 5's few-shot prompt is a legitimate alternative to
  fine-tuning when only a handful of labeled examples are available?
