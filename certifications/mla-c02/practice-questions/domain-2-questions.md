# Domain 2 Practice Questions — ML Model and Foundation Model Development (24%)

12 questions covering task statements 2.1–2.4: choosing a modeling approach, training/tuning
(including hyperparameter search and foundation model fine-tuning), evaluation, and model
versioning. See the [Domain 2 README](../domain-2-model-development/README.md) and the
[ML Fundamentals Glossary](../domain-2-model-development/ml-fundamentals-glossary.md) — the
single most heavily tested conceptual doc in this domain.

---

## Q1

A model achieves 99% accuracy on the training set but only 61% accuracy on the validation set.
What is happening, and what is the best fix?

A) Underfitting; train the model for many more epochs without changing anything else
B) Overfitting; apply regularization, gather more training data, or use early stopping
C) The validation set is mislabeled; ignore the validation score
D) The learning rate is too low; increase it substantially

**Correct Answer: B**

**Explanation:** A huge gap between training performance (very high) and validation performance
(much lower) is the textbook **overfitting** signature — the model has memorized noise and
specifics of the training data rather than the general pattern. Standard fixes are
**regularization** (L1/L2, dropout), **more training data**, or **early stopping** (halting once
validation performance stops improving). See the
[ML Fundamentals Glossary's overfitting/underfitting table](../domain-2-model-development/ml-fundamentals-glossary.md#overfitting-and-underfitting--is-the-model-actually-learning-the-right-thing).

**Why the others are wrong:**
- **A:** This is the opposite diagnosis — training more epochs on an already-overfit model
  typically makes the training/validation gap worse, not better, since the model keeps
  memorizing training-specific noise.
- **C:** Jumping to "the validation set is wrong" without evidence ignores the far more common
  and well-documented explanation; the train/validation gap pattern is diagnostic on its own.
- **D:** Learning rate affects convergence speed/stability, not the fundamental overfitting
  problem of a model too complex (or trained too long) relative to available data diversity.

---

## Q2

A regression model performs poorly on both the training set and the validation set, with
similar (low) scores on each. What is the most likely diagnosis and fix?

A) Overfitting; add dropout and early stopping
B) Underfitting; increase model capacity, add more/better features, or train longer
C) The data was not shuffled before splitting
D) The batch size is too large; reduce it to 1

**Correct Answer: B**

**Explanation:** Poor performance on **both** training and validation data, at similar levels, is
the signature of **underfitting** — the model is too simple, hasn't trained long enough, or
lacks the right features to capture the real pattern at all. Fixes are increasing model
capacity (more layers/trees), training longer, adding better features, or reducing excessive
regularization. See the
[ML Fundamentals Glossary's diagnosis table](../domain-2-model-development/ml-fundamentals-glossary.md#overfitting-and-underfitting--is-the-model-actually-learning-the-right-thing).

**Why the others are wrong:**
- **A:** Dropout and early stopping are overfitting remedies; applying them to an already
  underfit model would make the model even less able to learn the pattern, worsening the
  problem.
- **C:** Shuffling issues could cause an unrepresentative split, but the question states
  performance is similarly poor on *both* sets — the diagnostic signature points to model
  capacity/training insufficiency, not a shuffling artifact.
- **D:** Batch size affects training stability and speed, not whether the model fundamentally has
  enough capacity to learn the pattern; shrinking it to 1 doesn't address underfitting.

---

## Q3

Which statement correctly describes the bias-variance tradeoff?

A) Bias and variance can both be driven to zero simultaneously by simply using a bigger model
B) High bias means the model's assumptions are too simple to capture the real pattern (underfitting); high variance means the model is overly sensitive to the specific training sample (overfitting) — reducing one tends to increase the other
C) Bias only applies to regression problems, and variance only applies to classification problems
D) Variance is a property of the data, not the model, and cannot be influenced by model choices

**Correct Answer: B**

**Explanation:** This is the precise, exam-tested definition: **bias** is error from overly
simplistic assumptions (associated with underfitting), **variance** is error from sensitivity to
the exact training data sampled (associated with overfitting), and with a fixed amount of data
you generally cannot minimize both simultaneously — simple models have high bias/low variance,
complex models have low bias/high variance. See the
[Bias–Variance Tradeoff section](../domain-2-model-development/ml-fundamentals-glossary.md#biasvariance-tradeoff--why-you-cant-just-always-make-the-model-bigger).

**Why the others are wrong:**
- **A:** This is the core misconception the tradeoff exists to correct — you cannot drive both
  to zero with a fixed dataset; making a model more complex to reduce bias generally increases
  variance.
- **C:** Bias and variance are general statistical concepts that apply to both regression and
  classification problems equally; they aren't restricted by problem type.
- **D:** Variance is explicitly a property of *the model's* sensitivity to the training sample,
  and model choices (complexity, regularization) directly influence it — it is not solely a data
  property.

---

## Q4

A fraud detection model achieves 98% overall accuracy, but the business reports it is missing
most actual fraud cases. Fraud makes up only 1% of all transactions. What is the core issue and
the better metric to track?

A) The model is fine; 98% accuracy is already excellent
B) Accuracy is misleading on this imbalanced dataset because predicting "not fraud" for everything would already score ~99%; recall (or F1/AUC) better reflects whether actual fraud is being caught
C) The model needs a lower learning rate
D) The issue is underfitting; add more layers to the model

**Correct Answer: B**

**Explanation:** With a 99%/1% class split, a model that predicts the majority class for
everything already achieves ~99% accuracy while catching zero fraud — accuracy is dangerously
misleading here. **Recall** (TP / (TP + FN)) directly measures "of all actual fraud, how much did
we catch," which is what the business cares about; F1 or AUC are also reasonable imbalanced-data
metrics. See the
[Evaluation Metrics section](../domain-2-model-development/ml-fundamentals-glossary.md#evaluation-metrics--how-do-you-know-if-the-model-is-actually-good)
and its ["accuracy trap" exam scenario](../domain-2-model-development/ml-fundamentals-glossary.md#common-exam-scenarios).

**Why the others are wrong:**
- **A:** 98% accuracy sounds good in isolation but is a trap on a 99/1 imbalanced problem — it
  hides the fact the model may be systematically missing the minority (fraud) class, which is
  exactly the business complaint described.
- **C:** Learning rate is a training convergence hyperparameter; it has no direct relationship
  to selecting an appropriate evaluation metric for imbalanced classes.
- **D:** There's no evidence of underfitting here (no train/validation comparison given); the
  stated symptom is a metric-selection problem, not a model-capacity problem.

---

## Q5

A spam filter is blocking too many legitimate business emails (too many false positives), even
though it catches almost all actual spam. What change would most directly address this specific
complaint?

A) Lower the classification decision threshold so more emails get flagged as spam
B) Raise the classification decision threshold, requiring more confidence before flagging an email as spam — trading some recall for higher precision
C) Increase the number of training epochs
D) Switch the evaluation metric to recall only, and optimize purely for that

**Correct Answer: B**

**Explanation:** Too many false positives is a **precision** problem (precision = TP / (TP +
FP)). Raising the decision threshold makes the model require more confidence before flagging
"spam," which generally **increases precision** (fewer false alarms) at the cost of **recall**
(it may now miss a few more actual spam messages) — this is the classic precision/recall
tradeoff. See the
[Precision/Recall tradeoff](../domain-2-model-development/ml-fundamentals-glossary.md#evaluation-metrics--how-do-you-know-if-the-model-is-actually-good)
and the Domain 2 README's [spam classifier scenario](../domain-2-model-development/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A:** Lowering the threshold flags *more* emails as spam, which would increase false
  positives further — the opposite direction of what's needed.
- **C:** More training epochs affects how well the model fits the training data overall; it does
  not directly adjust the precision/recall balance at a fixed threshold.
- **D:** Optimizing purely for recall would push the model toward flagging even more emails as
  spam to catch every last true positive, worsening the false-positive problem the business is
  complaining about.

---

## Q6 (Choose TWO)

A team must run a hyperparameter search for an expensive-to-train model and wants to find a
strong combination of hyperparameters while minimizing the total number of training jobs
launched. Which TWO statements are correct?

A) Bayesian search strategies in SageMaker Automatic Model Tuning use the results of prior training jobs to intelligently choose the next hyperparameter combination to try, making them more sample-efficient than random/grid search
B) Early stopping of individual poorly-performing tuning jobs (based on intermediate metrics) can save compute without sacrificing the quality of the best candidate found
C) Grid search is always more sample-efficient than Bayesian search for expensive models
D) Running every possible combination of hyperparameters guarantees the cheapest total cost
E) Hyperparameter tuning cost is unrelated to the number of training jobs launched

**Correct Answer: A and B**

**Explanation:** **Bayesian search** in SageMaker Automatic Model Tuning builds a probabilistic
model of how hyperparameters affect the objective metric and uses it to pick promising
combinations to try next, converging on good results in fewer total jobs than random or grid
search — exactly what's needed when each training job is expensive. Enabling **early stopping**
within the tuning job lets SageMaker kill clearly underperforming trials early based on
intermediate metrics, saving compute without giving up the best candidate overall. See
[`services/machine-learning-ai/sagemaker-training-and-tuning.md`](../../../services/machine-learning-ai/sagemaker-training-and-tuning.md)
and the Domain 2 README's [hyperparameter search scenario](../domain-2-model-development/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **C:** This is backwards — grid search exhaustively tries every combination in a fixed grid
  and scales poorly; Bayesian search is specifically more sample-efficient for expensive models,
  which is why it's recommended when minimizing total job count matters.
- **D:** Exhaustively running every combination (grid search over a large space) typically
  maximizes, not minimizes, total training cost — the opposite of the stated goal.
- **E:** Each training job launched during tuning consumes real compute time and cost; the total
  tuning cost scales directly with the number of jobs run, which is precisely why sample-
  efficient strategies and early stopping matter.

---

## Q7

A team needs a model that can generate fluent, human-like text for a brand-new use case, and
they have only a handful of labeled examples available — nowhere near enough to train a
competitive model from scratch. What is the best starting approach?

A) Train a custom deep learning model from scratch using SageMaker script mode
B) Start with an existing foundation model via Amazon Bedrock or SageMaker JumpStart, rather than training from zero
C) Collect millions of new labeled examples before attempting any modeling
D) Use a simple linear regression model, since it requires the least data

**Correct Answer: B**

**Explanation:** When the task is general-purpose language generation and labeled data is scarce,
training from scratch is impractical — a pretrained **foundation model** (via Bedrock's
managed API or SageMaker JumpStart's deployable pretrained models) already has broad language
capability baked in from large-scale pretraining, and can be used as-is (optionally combined with
RAG or lightly fine-tuned) with minimal additional data. See the Domain 2 README's
["minimal labeled data" scenario](../domain-2-model-development/README.md#common-exam-scenarios)
and [`services/machine-learning-ai/bedrock.md`](../../../services/machine-learning-ai/bedrock.md).

**Why the others are wrong:**
- **A:** Training a custom deep learning model from scratch typically requires large amounts of
  labeled data to be competitive — directly contradicted by the "handful of labeled examples"
  constraint in the scenario.
- **C:** Waiting to collect millions of new examples is slow and may not even be feasible for a
  brand-new use case; it ignores the far faster option of starting from an existing foundation
  model.
- **D:** Linear regression is a simple, interpretable algorithm for structured numeric
  prediction tasks — it is not designed for generating fluent, human-like free text at all,
  regardless of data volume.

---

## Q8

A company has fine-tuned nothing yet; they are using a Bedrock foundation model as-is for a
customer support assistant. They now require every response to strictly follow a specific JSON
schema and always use their brand's tone of voice, consistently across all responses. Which
approach should they add?

A) Add more documents to a RAG knowledge base
B) Fine-tune the foundation model on labeled examples that demonstrate the desired JSON schema and tone
C) Increase the Guardrails content-filter strength
D) Switch to a larger foundation model with no other changes

**Correct Answer: B**

**Explanation:** Consistently changing a model's **output behavior** — format, schema, tone,
persona — is what **fine-tuning** is for: training the foundation model further on labeled
examples that demonstrate the desired behavior. RAG only changes what *facts* the model has
access to; it does not reliably change output structure or tone. See the Domain 2 README's
["specific JSON schema/company tone" scenario](../domain-2-model-development/README.md#common-exam-scenarios)
and [`embeddings-and-rag-data-prep.md`'s "when not to use RAG" section](../domain-1-data-preparation/embeddings-and-rag-data-prep.md#when-not-to-use-it--alternatives).

**Why the others are wrong:**
- **A:** Adding more documents to a RAG knowledge base improves the *facts* the model can draw
  on, but RAG does not reliably enforce a strict output format or tone across every response —
  that is a behavior-level change, which RAG doesn't control.
- **C:** Guardrails filter/block disallowed or unsafe content; they do not shape a model into
  consistently producing a specific JSON schema or brand tone — that's not their function.
- **D:** A larger model with no behavioral training still has no guarantee of following a
  specific schema/tone consistently; size alone doesn't substitute for fine-tuning on examples
  of the desired behavior.

---

## Q9

A deep learning model is too large to fit on a single GPU's memory during training, even with a
small batch size. Which distributed training strategy directly addresses this specific
constraint?

A) Data parallelism only, replicating the full model on every GPU
B) Model parallelism, splitting the model itself across multiple GPUs so no single GPU needs to hold the entire model
C) Reducing the number of training epochs to one
D) Switching from a GPU instance to a CPU-only instance

**Correct Answer: B**

**Explanation:** When the **model itself** (its parameters) is too large for one GPU's memory,
**model parallelism** splits different layers/parts of the model across multiple GPUs so that
collectively they hold the full model, with each GPU handling only its assigned portion during
the forward/backward pass. This is the correct lever specifically for model-size-exceeds-memory
constraints. See
[`services/machine-learning-ai/sagemaker-training-and-tuning.md`](../../../services/machine-learning-ai/sagemaker-training-and-tuning.md).

**Why the others are wrong:**
- **A:** Data parallelism replicates the *entire* model on each GPU and splits the *data* across
  them — it requires each GPU to hold the full model, which is exactly the constraint that's
  already failing in this scenario.
- **C:** Reducing epochs changes how long training runs, not whether the model's parameters fit
  into a single GPU's memory at all — the out-of-memory problem would still occur.
- **D:** CPUs are generally far slower for deep learning training than GPUs and typically have
  different (often larger, but much slower) memory profiles; this isn't the standard fix for a
  GPU-memory-sizing problem, and it sacrifices training speed substantially.

---

## Q10

Several training jobs over the past month have each produced a different model version. A
compliance audit needs to identify exactly which dataset version and training code version
produced the model currently running in production. Where should the team look?

A) CloudWatch Logs for the training job
B) SageMaker Model Registry, which tracks versioned model artifacts along with lineage metadata (data and code that produced them) and approval status
C) The S3 bucket's default versioning feature alone
D) The IAM policy attached to the training role

**Correct Answer: B**

**Explanation:** **SageMaker Model Registry** is designed exactly for this: every
trained/fine-tuned model version is registered with metadata capturing lineage (which dataset
and code version produced it) and an approval status (pending/approved/rejected), letting a
compliance audit trace the exact production model back to its origins. See
[`services/machine-learning-ai/sagemaker-model-monitor-and-registry.md`](../../../services/machine-learning-ai/sagemaker-model-monitor-and-registry.md)
and the Domain 2 README's [lineage-tracking scenario](../domain-2-model-development/README.md#common-exam-scenarios).

**Why the others are wrong:**
- **A:** CloudWatch Logs capture runtime log output from a training job but aren't structured for
  querying "which exact dataset/code version produced this registered model" the way Model
  Registry's lineage tracking is.
- **C:** S3 versioning tracks changes to individual objects over time but doesn't tie a specific
  dataset version to a specific trained model artifact and code version as a single queryable
  record.
- **D:** An IAM policy defines what the training role is *permitted* to access; it says nothing
  about which specific dataset or code version was actually used for a given training run.

---

## Q11 (Choose TWO)

A model is overfitting its training data. Which TWO of the following are valid, standard
techniques to reduce overfitting?

A) L2 regularization, which shrinks model weights toward zero to discourage overly extreme fitting to training data
B) Dropout, which randomly deactivates a fraction of neurons during each training step so the network doesn't over-rely on any single path
C) Increasing the learning rate substantially
D) Adding more layers to increase model capacity
E) Removing the validation set so training can run longer

**Correct Answer: A and B**

**Explanation:** **L2 regularization** and **dropout** are both standard, well-established
techniques for reducing overfitting: L2 penalizes large weights to keep the model from fitting
training noise too precisely, and dropout prevents the network from becoming overly dependent on
any single neuron/path, both pushing the model toward learning more generalizable patterns. See
the [Regularization section](../domain-2-model-development/ml-fundamentals-glossary.md#regularization--the-deliberate-handicap-that-prevents-overfitting).

**Why the others are wrong:**
- **C:** Increasing the learning rate affects how quickly/stably the model converges; it is not
  a regularization technique and doesn't directly address overfitting (and can destabilize
  training if raised too aggressively).
- **D:** Adding more layers *increases* model capacity and complexity, which typically makes
  overfitting **worse**, not better — this is the opposite of what's needed here.
- **E:** Removing the validation set eliminates your ability to detect overfitting at all (no
  early-stopping signal, no generalization check) — it doesn't fix the underlying overfitting,
  it just blinds you to it.

---

## Q12

A team is comparing two candidate binary classifiers and wants a single metric that evaluates
each model's ability to rank positive examples above negative examples across every possible
decision threshold, without committing to one specific cutoff yet. Which metric should they use?

A) Accuracy at the default 0.5 threshold
B) AUC (Area Under the ROC Curve)
C) RMSE
D) Batch size

**Correct Answer: B**

**Explanation:** **AUC** plots true positive rate against false positive rate across every
possible decision threshold and summarizes ranking quality as a single threshold-independent
number (1.0 = perfect ranking, 0.5 = random guessing) — exactly suited for comparing models
before committing to a specific operating threshold. See the
[AUC definition](../domain-2-model-development/ml-fundamentals-glossary.md#evaluation-metrics--how-do-you-know-if-the-model-is-actually-good)
and its ["comparing two candidate models' ranking ability" exam scenario](../domain-2-model-development/ml-fundamentals-glossary.md#common-exam-scenarios).

**Why the others are wrong:**
- **A:** Accuracy at one fixed threshold (0.5) only evaluates performance at that single cutoff
  — it says nothing about ranking quality across all possible thresholds, and is also
  misleading on imbalanced data.
- **C:** RMSE is a regression metric (measuring numeric prediction error in the original units)
  — it doesn't apply to binary classification ranking quality at all.
- **D:** Batch size is a training hyperparameter controlling how many examples are processed per
  gradient update; it is not an evaluation metric of any kind.
