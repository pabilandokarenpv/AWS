# ML Fundamentals Glossary

*Machine Learning concept · MLA-C02 Domain 2, Task Statements 2.2–2.3 — this is the single most
foundational, most exam-tested vocabulary in the entire MLA-C02 cert. These terms are
algorithm-agnostic (they apply whether you're using SageMaker's XGBoost, a PyTorch script, or
fine-tuning a Bedrock foundation model), which is why they get their own doc instead of living
inside a SageMaker service page. Every term below is explained in plain English first, then
with the technical/mathematical detail, in that order, deliberately.*

## Epoch and Batch — how a model actually "sees" data during training

**Plain English:** Imagine studying a textbook for an exam. An **epoch** is one complete
read-through of the entire textbook, cover to cover. A **batch** is how many pages you read
before stopping to quiz yourself and adjust your study notes, rather than waiting until you've
finished the whole book.

**Technical:** Training a model (specifically, neural-network-style training using gradient
descent) works by repeatedly: (1) feeding it some training examples, (2) measuring how wrong its
predictions were (the **loss**), and (3) nudging its internal parameters slightly to reduce that
wrongness. Doing this nudge after *every single example* would be extremely slow and noisy;
doing it only after seeing *all* examples would be extremely memory-hungry and slow to improve.
The compromise is the **batch**: a subset of examples (e.g., 32, 64, 128 at a time) processed
together before one parameter update happens. One **epoch** = the model has processed every
training example in the dataset exactly once, which usually means many batches (dataset size ÷
batch size = number of batches per epoch). Models are typically trained for many epochs (seeing
the same data repeatedly), because one pass usually isn't enough to learn the pattern well.

- **Larger batch size** → more stable/accurate gradient estimates per update, faster wall-clock
  training (more parallelism), but requires more memory and can sometimes generalize slightly
  worse.
- **Smaller batch size** → noisier updates (can help escape bad local solutions), less memory,
  but slower overall and less stable.
- **Too few epochs** → the model hasn't seen the data enough times to learn the pattern
  (contributes to underfitting, below).
- **Too many epochs** → the model starts memorizing noise/quirks specific to the training set
  instead of the general pattern (contributes to overfitting, below) — this is exactly what
  **early stopping** (halting training once validation performance stops improving) prevents.

## Overfitting and Underfitting — is the model actually learning the right thing?

**Plain English:** Imagine a student preparing for an exam by memorizing the exact wording of
every practice question's answer, instead of understanding the underlying concept. They'll ace
the practice questions (training data) but fail the real exam, which asks the same concepts in
different words (new/validation data). That's **overfitting**. The opposite — a student who
barely studied at all and does poorly on both the practice questions and the real exam — is
**underfitting**.

**Technical:**
- **Underfitting**: the model performs poorly on *both* the training data and new (validation/
  test) data. This means the model is too simple, hasn't trained long enough, or lacks the
  right features to capture the real pattern in the data at all.
- **Overfitting**: the model performs very well on training data but noticeably worse on
  validation/test data. This means the model has learned noise and incidental quirks specific
  to the training examples (memorization) rather than the general, transferable pattern.
- **Good fit**: training and validation performance are both strong and reasonably close to each
  other.

| Symptom | Training performance | Validation performance | Diagnosis | Common fixes |
|---|---|---|---|---|
| Both bad | Low | Low | Underfitting | More model capacity, more training time/epochs, better/more features, reduce regularization |
| Train great, val bad | High | Low | Overfitting | More training data, regularization, dropout, early stopping, simpler model |
| Both good, close together | High | High | Good fit | Proceed to hyperparameter tuning / deployment |

**How you detect it on the exam:** a question gives you two numbers (training accuracy/loss and
validation accuracy/loss) and asks what's wrong and how to fix it — match the pattern against
the table above. A huge gap between the two numbers (train much better than validation) is the
overfitting signature; both numbers being mediocre is the underfitting signature.

## Bias–Variance Tradeoff — why you can't just always make the model "bigger"

**Plain English:** **Bias** is "the model's basic assumptions are too simple to capture reality"
— like trying to fit a straight line through data that actually curves. **Variance** is "the
model is overly sensitive to the exact training examples it happened to see" — like a model that
gives wildly different answers if you'd trained it on a slightly different random sample of the
same underlying data. A high-bias model underfits; a high-variance model overfits. You cannot
drive both to zero simultaneously with a fixed amount of data — reducing one tends to increase
the other, which is the "tradeoff."

**Technical:** Formally, a model's total expected prediction error can be decomposed into:
**bias²** (error from overly simplistic assumptions), **variance** (error from sensitivity to
the specific training set), and **irreducible error** (noise inherent to the problem that no
model can remove). Simple models (e.g., linear regression) tend to have high bias, low variance.
Complex models (e.g., deep neural networks, unpruned decision trees) tend to have low bias, high
variance. The practical goal is finding the sweet spot — a model complex enough to capture the
real pattern (low bias) but not so flexible that it chases noise (low variance) — which is
exactly what regularization and proper hyperparameter tuning are trying to achieve.

## Regularization — the deliberate "handicap" that prevents overfitting

**Plain English:** Regularization is like giving the student a rule: "you're not allowed to use
more than N index cards of notes." It forces simplicity, which prevents them from just
memorizing everything verbatim and pushes them toward understanding the general concept instead.

**Technical:** Regularization adds a penalty to the training objective that discourages the
model from becoming overly complex/extreme, in exchange for better generalization to new data.
Common forms:
- **L1 regularization (Lasso)** — penalizes the sum of absolute values of model weights; tends
  to push some weights to exactly zero, effectively performing feature selection.
- **L2 regularization (Ridge)** — penalizes the sum of squared weights; shrinks weights toward
  zero smoothly without necessarily eliminating any.
- **Dropout** (neural networks specifically) — randomly "turns off" a fraction of neurons during
  each training step, preventing the network from relying too heavily on any single neuron/path.
- **Early stopping** — halting training once validation performance stops improving, even if
  training performance would keep improving further — a simple, very commonly tested form of
  regularization that doesn't require changing the loss function at all.

## Evaluation Metrics — how do you know if the model is actually good?

**Plain English first, for all of these:** imagine a model that screens emails and flags some as
spam. Every prediction falls into one of four buckets, which together form the **confusion
matrix**:

|  | Predicted: Spam | Predicted: Not Spam |
|---|---|---|
| **Actually Spam** | True Positive (TP) — correctly caught | False Negative (FN) — missed, slipped into inbox |
| **Actually Not Spam** | False Positive (FP) — wrongly flagged, good email blocked | True Negative (TN) — correctly left alone |

The **confusion matrix** is just this 2×2 (or larger, for multi-class) table of counts — it's
called that because it shows you exactly *where* the model gets confused, not just a single
"percent correct" number that can hide serious problems.

- **Accuracy** = (TP + TN) / (everything). Plain English: "what fraction of all predictions were
  correct." **The trap**: with imbalanced classes (e.g., 99% of emails are legitimate), a model
  that predicts "not spam" for literally everything scores 99% accuracy while catching zero spam
  — accuracy alone is dangerously misleading here.
- **Precision** = TP / (TP + FP). Plain English: "of everything the model flagged as spam, what
  fraction actually was spam?" High precision means few false alarms. Matters most when a false
  positive is costly (e.g., blocking a legitimate, important email).
- **Recall** (also called Sensitivity or True Positive Rate) = TP / (TP + FN). Plain English: "of
  all the actual spam that existed, what fraction did the model catch?" High recall means few
  misses. Matters most when a false negative is costly (e.g., a cancer-screening model missing an
  actual case is far worse than a false alarm that gets double-checked).
- **Precision/Recall tradeoff**: raising the model's decision threshold (requiring more
  confidence before flagging "spam") generally increases precision but decreases recall, and
  vice versa — you cannot usually maximize both at once; which one matters more is a business
  decision, not a math one.
- **F1 Score** = the harmonic mean of precision and recall: `2 × (precision × recall) /
  (precision + recall)`. Plain English: "a single number that's only high when BOTH precision
  and recall are reasonably good" — useful when you want one summary metric for an imbalanced
  classification problem and don't want to pick a side between precision and recall.
- **AUC (Area Under the ROC Curve)**: the ROC curve plots true positive rate against false
  positive rate across every possible decision threshold. Plain English: "if you grabbed one
  random actual-positive example and one random actual-negative example, AUC is the probability
  the model correctly ranks the positive one as more likely to be positive." AUC = 1.0 is a
  perfect model; AUC = 0.5 is equivalent to random guessing. It's threshold-independent, which
  makes it useful for comparing models without committing to one cutoff yet.
- **RMSE (Root Mean Squared Error)**: used for **regression** (predicting a number, like a house
  price), not classification. Plain English: "on average, how far off were the model's numeric
  predictions, in the same units as what it's predicting" (e.g., RMSE of $15,000 on house price
  predictions). Technical: square each prediction's error (so bigger misses are punished
  disproportionately more than small ones), average those squared errors, then take the square
  root to bring the units back to the original scale.

### Which metric for which problem — the exam's favorite trap

| Problem type | Classes balanced? | Use |
|---|---|---|
| Classification | Balanced | Accuracy is reasonable |
| Classification | Imbalanced | Precision, Recall, F1, or AUC — NOT plain accuracy |
| Classification, false positives very costly | — | Optimize for Precision |
| Classification, false negatives very costly (missed fraud, missed disease) | — | Optimize for Recall |
| Regression (predicting a number) | n/a | RMSE (or MAE — Mean Absolute Error, a simpler, less-outlier-sensitive cousin) |

## Common exam scenarios

1. **"A fraud detection model has 98% accuracy but the business says it's not catching enough
   fraud"** → fraud is a rare/imbalanced class; the real problem metric is likely low **recall**
   — accuracy is hiding it.
2. **"Training loss keeps decreasing every epoch, but validation loss started increasing several
   epochs ago"** → classic overfitting signature; the fix is **early stopping** at the point
   validation loss was lowest, or adding regularization.
3. **"The model's predictions are consistently far off the true value in the same direction, on
   both training and test data"** → high bias / underfitting, not a variance problem — needs a
   more expressive model or better features, not more data alone.
4. **"A spam filter is blocking too many legitimate business emails"** → a precision problem
   (too many false positives); raise the classification threshold to require more confidence
   before flagging spam.
5. **"Need one single number to report model quality for an imbalanced binary classifier without
   picking between false positives and false negatives"** → F1 score.
6. **"Comparing two candidate models' ranking ability across all possible thresholds, before
   deciding on a cutoff"** → AUC.
7. **"A house-price regression model's errors should be reported in dollars, penalizing large
   misses more than small ones"** → RMSE.
8. **"Batch size was increased and training got faster but final model accuracy slightly dropped"**
   → expected tradeoff; larger batches speed up training (more parallel compute per update) but
   can mildly hurt generalization — not a bug, a known tradeoff to reason about.

## Related Terms

- [`../domain-1-data-preparation/README.md`](../domain-1-data-preparation/README.md) — class
  imbalance is created/fixed upstream in data prep; these metrics are how you detect its effect
  downstream.
- [`services/machine-learning-ai/sagemaker-training-and-tuning.md`](../../../services/machine-learning-ai/sagemaker-training-and-tuning.md)
  — where epochs, batch size, and early stopping are configured in practice.
- [`services/machine-learning-ai/sagemaker-model-monitor-and-registry.md`](../../../services/machine-learning-ai/sagemaker-model-monitor-and-registry.md)
  — these same metrics are what SageMaker Model Monitor watches for *drift* after deployment
  (Domain 4).
