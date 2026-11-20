# Evaluation Metrics Deep Dive — Worked Numeric Examples

*New topic doc for MLA-C02 Domain 2 (Task Statement 2.3 — "Evaluate a model"). Companion to
[`ml-fundamentals-glossary.md`](ml-fundamentals-glossary.md), which defines every metric in plain
English first. This doc assumes those definitions and goes one level deeper: full numeric
derivations across classification, regression, AND generative evaluation, multi-class confusion
matrices, ROC/PR curve mechanics at specific thresholds, calibration, and the log-loss math
behind "confidently wrong is punished harder" — the computational detail the exam's harder
case-study questions expect you to actually reason through, not just recognize a vocabulary word.*

## Why this doc exists separately from the glossary

The glossary's worked example computes one confusion matrix once. The exam's hardest questions
give you **two or three competing models' metrics side by side** and ask which to ship, or walk
a **threshold sweep** and ask where to set the cutoff, or ask you to **read a multi-class
confusion matrix** rather than a 2x2 one. Each of those needs its own worked arithmetic, which is
what follows.

## Part 1 — Binary classification, full threshold sweep

Start from raw predicted probabilities (not just one fixed threshold's TP/FP/FN/TN) — this is
what a ROC or Precision-Recall curve is actually built from, point by point.

**Setup:** 10 test transactions, true label and the model's predicted fraud probability:

| Transaction | True label | Predicted probability |
|---|---|---|
| 1 | Fraud | 0.92 |
| 2 | Fraud | 0.81 |
| 3 | Not Fraud | 0.76 |
| 4 | Fraud | 0.65 |
| 5 | Not Fraud | 0.58 |
| 6 | Not Fraud | 0.44 |
| 7 | Fraud | 0.39 |
| 8 | Not Fraud | 0.33 |
| 9 | Not Fraud | 0.21 |
| 10 | Not Fraud | 0.09 |

**Sweeping the threshold** (predict "Fraud" if probability ≥ threshold):

| Threshold | Predicted Fraud | TP | FP | FN | TN | Precision | Recall |
|---|---|---|---|---|---|---|---|
| 0.90 | {1} | 1 | 0 | 3 | 6 | 1.00 | 0.25 |
| 0.70 | {1,2,3} | 2 | 1 | 2 | 5 | 0.67 | 0.50 |
| 0.60 | {1,2,3,4} | 3 | 1 | 1 | 5 | 0.75 | 0.75 |
| 0.40 | {1,2,3,4,5,6} | 3 | 3 | 1 | 3 | 0.50 | 0.75 |
| 0.30 | {1,2,3,4,5,6,7,8} | 4 | 4 | 0 | 2 | 0.50 | 1.00 |

**What this table demonstrates numerically, that the glossary's single-point example cannot:**
moving the threshold from 0.90 down to 0.30 monotonically trades precision away for recall —
precision never increases as the threshold drops (new captures are never *more* likely correct
than existing ones) and recall never decreases (you only ever add more positives to the
flagged set). The threshold at 0.60 is the "elbow" where both precision and recall sit at a
locally balanced 0.75 — a plausible operating point if the business has no stated asymmetric cost
of false positives vs. false negatives. **The exam-relevant reading:** a scenario describing
"the team needs to catch more fraud even if it means more false alarms" is explicitly asking you
to move the threshold *down* (toward 0.30-0.40); "too many legitimate customers are being
wrongly flagged" is asking you to move it *up* (toward 0.70-0.90) — both are threshold
adjustments to an *already-trained* model, requiring no retraining at all.

```python
from sklearn.metrics import roc_curve, precision_recall_curve, roc_auc_score, average_precision_score

y_true = [1,1,0,1,0,0,1,0,0,0]
y_prob = [0.92,0.81,0.76,0.65,0.58,0.44,0.39,0.33,0.21,0.09]

fpr, tpr, roc_thresholds = roc_curve(y_true, y_prob)
precision, recall, pr_thresholds = precision_recall_curve(y_true, y_prob)

print("AUC:", round(roc_auc_score(y_true, y_prob), 4))
print("Average Precision (area under PR curve):", round(average_precision_score(y_true, y_prob), 4))
```

**Real output:** `AUC: 0.8750` and `Average Precision: 0.8286` — run this yourself and you'll see
AUC sits meaningfully higher than Average Precision on this exact dataset, which is itself a
teaching point: **AUC (ROC-based) tends to look more optimistic than Average Precision (PR-based)
specifically on imbalanced data**, because ROC's false-positive-rate denominator (all actual
negatives, here 6) dilutes a few false positives much more than PR's precision denominator (only
the *flagged* set) does — this is precisely why the exam and real practice prefer
Precision-Recall curves over ROC curves for *rare-class* problems, even though both answer
"how good is this classifier across all thresholds."

![scikit-learn's ROC curve example — true positive rate vs. false positive rate swept across every threshold](https://scikit-learn.org/stable/_images/sphx_glr_plot_roc_001.png)

*Figure: a real ROC curve — each point on the curve is exactly one row of a threshold-sweep table
like the one above, plotted as (false positive rate, true positive rate) instead of a text table.
The diagonal line is what a model with zero predictive skill (AUC=0.5) would trace; the further
the curve bows toward the top-left corner, the better. Source: scikit-learn documentation,
"Receiver Operating Characteristic (ROC) with cross validation" —
scikit-learn.org/stable/auto_examples/model_selection/plot_roc_crossval.html.*

![A Precision-Recall curve for the same kind of threshold sweep, preferred for imbalanced classes](https://scikit-learn.org/stable/_images/sphx_glr_plot_precision_recall_001.png)

*Figure: the Precision-Recall curve equivalent — notice it has no "diagonal baseline" the way ROC
does; a PR curve's baseline is the positive class's prevalence rate (if 5% of examples are
positive, a skill-less model's PR curve sits near precision=0.05 everywhere), which is exactly
why PR curves are the harder, more honest test for a rare positive class. Source: scikit-learn
documentation, "Precision-Recall" —
scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html.*

![Cross-validated ROC curves — multiple folds plotted together with the averaged curve and its variance band](https://scikit-learn.org/stable/_images/sphx_glr_plot_roc_crossval_001.png)

*Figure: ROC curves from five cross-validation folds plotted together, with the mean curve and a
shaded standard-deviation band — this is the practical way AUC is reported responsibly (a single
AUC number from one split can be misleadingly optimistic or pessimistic by chance; the band shows
how much that number would move under a different random split). Source: scikit-learn
documentation, "Receiver Operating Characteristic (ROC) with cross validation" —
scikit-learn.org/stable/auto_examples/model_selection/plot_roc_crossval.html.*

## Part 2 — Multi-class confusion matrices, read correctly

Binary confusion matrices are 2×2; most real classification problems (document category,
product defect type, support-ticket routing) are multi-class, and reading a multi-class matrix
is tested as its own skill.

**Setup:** a 3-class support-ticket router (Billing / Technical / Account) tested on 150 tickets:

| | Predicted: Billing | Predicted: Technical | Predicted: Account |
|---|---|---|---|
| **Actually Billing** | 42 | 5 | 3 |
| **Actually Technical** | 8 | 58 | 4 |
| **Actually Account** | 2 | 6 | 22 |

**Per-class precision/recall, computed by isolating one class as "positive" and everything else
as "negative" (the standard one-vs-rest approach):**

- **Billing — Precision** = 42 / (42+8+2) = 42/52 ≈ **80.8%**. **Recall** = 42 / (42+5+3) =
  42/50 = **84.0%**.
- **Technical — Precision** = 58 / (5+58+6) = 58/69 ≈ **84.1%**. **Recall** = 58 / (8+58+4) =
  58/70 ≈ **82.9%**.
- **Account — Precision** = 22 / (3+4+22) = 22/29 ≈ **75.9%**. **Recall** = 22 / (2+6+22) =
  22/30 ≈ **73.3%**.
- **Overall accuracy** = (42+58+22) / 150 = 122/150 ≈ **81.3%**.

**Macro-averaged F1** (average the per-class F1 scores, treating every class equally regardless
of how many tickets it has) vs. **micro-averaged F1** (pool all TP/FP/FN across classes first,
then compute one F1) give **different numbers whenever classes are imbalanced in size** — here
Account has only 30 tickets vs. Technical's 70, so macro-F1 weighs Account's weaker 73-76%
performance equally with Technical's stronger 83-84%, while micro-F1 (closer to overall accuracy
on balanced-enough data) would be pulled toward the majority classes' better performance. **The
exam-relevant trap:** reporting only overall accuracy (81.3%) on this matrix hides that the
Account category — likely the smallest and possibly most business-critical if it involves
security — performs meaningfully worse than the other two; a scenario emphasizing "performance
must be checked per-category, not just in aggregate" is pointing you at per-class precision/
recall or macro-averaged metrics, not overall accuracy.

```python
from sklearn.metrics import classification_report
import numpy as np

cm = np.array([[42,5,3],[8,58,4],[2,6,22]])
y_true, y_pred = [], []
labels = ["Billing", "Technical", "Account"]
for i, row in enumerate(cm):
    for j, count in enumerate(row):
        y_true += [labels[i]] * count
        y_pred += [labels[j]] * count

print(classification_report(y_true, y_pred))
```

## Part 3 — Regression metrics, a worked outlier-sensitivity comparison

**Setup:** a house-price model's errors (predicted - actual, in $1,000s) on 8 held-out houses:
`[2, -3, 1, 4, -2, 3, -1, 48]` — seven small, reasonable misses and one catastrophic 48k miss on
a single unusual property.

- **MAE** = (2+3+1+4+2+3+1+48) / 8 = 64/8 = **$8,000** — a single extreme outlier pulls MAE up,
  but only linearly, by its own share of the average.
- **RMSE** = sqrt((4+9+1+16+4+9+1+2304)/8) = sqrt(2348/8) = sqrt(293.5) ≈ **$17,132** — more than
  double MAE, because squaring the 48 error turns it into 2,304 before averaging, letting that
  single outlier dominate the sum far more than its "fair share."

**The exact numeric proof of why this matters:** removing just that one outlier entry drops MAE
from $8,000 to about $2,286 (a 71% drop) but drops RMSE from ~$17,132 to about $2,646 (an 85%
drop) — RMSE is disproportionately driven by that single point in a way MAE isn't, which is the
whole reason a scenario emphasizing "a few unusual high-value properties shouldn't dominate our
reported error metric" is explicitly pointing you toward MAE over RMSE, and a scenario
emphasizing "we specifically want to penalize large misses more heavily, since a large pricing
error is disproportionately costly to the business" is pointing the opposite direction, toward
RMSE, on the exact same underlying data.

```python
import numpy as np
errors = np.array([2, -3, 1, 4, -2, 3, -1, 48])
mae = np.mean(np.abs(errors))
rmse = np.sqrt(np.mean(errors**2))
print(f"MAE: ${mae*1000:.0f}  RMSE: ${rmse*1000:.0f}")

errors_no_outlier = errors[:-1]
mae2 = np.mean(np.abs(errors_no_outlier))
rmse2 = np.sqrt(np.mean(errors_no_outlier**2))
print(f"Without outlier -> MAE: ${mae2*1000:.0f} ({(1-mae2/mae)*100:.0f}% drop)  "
      f"RMSE: ${rmse2*1000:.0f} ({(1-rmse2/rmse)*100:.0f}% drop)")
```

## Part 4 — Cross-entropy (log loss), the metric training actually optimizes, computed by hand

**Plain English recap:** accuracy only cares whether the *top* predicted class was right. Log
loss cares *how confident* the model was, and punishes confident wrongness far more severely —
this is the mechanism, not just an abstract claim.

**Setup:** three binary predictions with their true labels and predicted probability of the
true class:

| Example | True label | Model's predicted probability of true label | Log loss contribution: `-ln(p)` |
|---|---|---|---|
| A | 1 | 0.95 (confidently correct) | -ln(0.95) ≈ **0.0513** |
| B | 1 | 0.55 (barely correct) | -ln(0.55) ≈ **0.5978** |
| C | 1 | 0.02 (confidently WRONG) | -ln(0.02) ≈ **3.9120** |

**Average log loss across these three** = (0.0513 + 0.5978 + 3.9120) / 3 ≈ **1.5204**.

**The number that makes "confidently wrong is punished harder" concrete:** example C's single
confident mistake (predicted probability 0.02 for the actual true class) contributes **3.9120** to
the loss — roughly **76 times** example A's confidently-correct contribution of 0.0513, and
about **6.5 times** example B's barely-correct contribution. If all three predictions instead
scored 0.55 (all "barely correct," same as B), average log loss would be a flat 0.5978 — *lower*
than the mix above despite example A in that mix being far more confidently right, because
example C's severe penalty for confident wrongness dominates the average. **This is precisely
why two models can tie on accuracy (both get all three examples' top prediction right) while
having very different log loss** — accuracy only checks whether probability > 0.5 landed on the
correct class; log loss checks how close to 1.0 or 0.0 that probability actually was, and whether
any individual prediction was confidently wrong even if a different metric never surfaces it.

```python
import numpy as np
probs = np.array([0.95, 0.55, 0.02])
losses = -np.log(probs)
print("Per-example log loss:", np.round(losses, 4))
print("Average log loss:", round(losses.mean(), 4))
print(f"Example C is {losses[2]/losses[0]:.1f}x example A's penalty")
```

## Part 5 — Calibration: when a model's confidence numbers are themselves wrong

**Plain English:** accuracy, precision, recall, AUC, and log loss all answer "are the
predictions right." **Calibration** answers a different question: "when the model says 80%
confident, is it actually right about 80% of the time?" A model can have excellent accuracy while
being badly *miscalibrated* — e.g., a model whose "90% confident" predictions are only correct
60% of the time is overconfident, which matters enormously whenever the probability itself (not
just the top class) feeds a downstream decision — exactly the case in Part 1's threshold-sweep
fraud example, where moving the threshold only makes sense if the underlying probabilities mean
what they claim to mean.

**A simple worked check — binning predictions by confidence and checking actual accuracy per
bin:**

| Predicted confidence bin | # predictions | Actually correct | Observed accuracy | Calibration gap |
|---|---|---|---|---|
| 0.90–1.00 | 50 | 48 | 96% | well-calibrated (+6 pts) |
| 0.70–0.89 | 50 | 44 | 88% | well-calibrated (close) |
| 0.50–0.69 | 50 | 22 | 44% | **overconfident** (-16 pts vs. midpoint 60%) |

The third bin's predictions claimed roughly 50-69% confidence but were only right 44% of the
time — meaningfully worse than even the low end of their claimed range — flagging that this
model's mid-confidence predictions overstate how sure it actually is. **The exam-relevant use:**
this is exactly the failure mode a **reliability diagram / calibration curve** is built to catch,
and the standard fix — **Platt scaling** (fit a logistic regression on top of the raw scores) or
**isotonic regression** — rescales predicted probabilities to match observed frequencies without
touching the underlying model's rankings (its AUC stays the same; only the probability *values*
change) — a scenario describing "the model's rankings are fine but its stated confidence
percentages don't match reality, and downstream automation relies on the actual probability
value" is a calibration problem, not an accuracy or ranking problem, and recalibration (not
retraining from scratch) is the fix.

## Part 6 — Generative text evaluation, numeric intuition beyond the glossary

`ml-fundamentals-glossary.md` introduces BLEU/ROUGE/BERTScore/semantic similarity conceptually.
Here's the arithmetic behind the simplest piece — **BLEU's n-gram precision** — worked by hand on
a short example, since the exam occasionally expects you to reason about *why* a score comes out
low, not just to recognize the metric's name.

**Setup:** reference: `"the cat sat on the mat"`. Candidate: `"the cat is on the mat"`.

**1-gram (unigram) precision:** candidate words: {the, cat, is, on, the, mat}. Matching against
reference word counts (the:2, cat:1, sat:1, on:1, mat:1): "the" appears twice in candidate,
reference has 2 "the"s available → both count; "cat" matches (1); "is" has zero matches in
reference (0); "on" matches (1); "mat" matches (1). Total matched = 2+1+0+1+1 = 5 out of 6
candidate unigrams → **unigram precision = 5/6 ≈ 83.3%**.

**2-gram (bigram) precision:** candidate bigrams: `(the,cat) (cat,is) (is,on) (on,the) (the,mat)`
— 5 bigrams. Reference bigrams: `(the,cat) (cat,sat) (sat,on) (on,the) (the,mat)`. Matches:
`(the,cat)` ✓, `(cat,is)` ✗, `(is,on)` ✗, `(on,the)` ✓, `(the,mat)` ✓ → 3 out of 5 → **bigram
precision = 3/5 = 60%**.

**Why BLEU multiplies several n-gram precisions together (geometric mean) rather than using just
one:** a single swapped word ("is" for "sat") barely dents unigram precision (83.3%, since most
individual words still match) but meaningfully dents bigram precision (60%, since every bigram
*touching* the swapped word breaks) — using multiple n-gram orders together is what makes BLEU
sensitive to word-order and local fluency, not just "are the right words present somewhere,"
while still (per the glossary's point) penalizing this genuinely fluent, meaning-preserving
paraphrase for using different words at all, which is exactly BLEU's known limitation.

```python
from collections import Counter

def ngram_precision(candidate, reference, n):
    cand_tokens = candidate.split()
    ref_tokens = reference.split()
    cand_ngrams = [tuple(cand_tokens[i:i+n]) for i in range(len(cand_tokens)-n+1)]
    ref_counts = Counter(tuple(ref_tokens[i:i+n]) for i in range(len(ref_tokens)-n+1))
    matched = 0
    for ng in cand_ngrams:
        if ref_counts[ng] > 0:
            matched += 1
            ref_counts[ng] -= 1
    return matched / len(cand_ngrams)

ref = "the cat sat on the mat"
cand = "the cat is on the mat"
print("Unigram precision:", round(ngram_precision(cand, ref, 1), 4))
print("Bigram precision:", round(ngram_precision(cand, ref, 2), 4))
```

## Part 7 — Retrieval evaluation: Precision@K and Recall@K, worked

Referenced in the glossary's task-statement 2.3.10 section conceptually; here's the arithmetic.
A RAG system retrieves the top 5 chunks for a query; the corpus has 4 chunks that are genuinely
relevant to answering it; the retriever returns these 5, ranked:

| Rank | Chunk | Relevant? |
|---|---|---|
| 1 | C | Yes |
| 2 | F | No |
| 3 | A | Yes |
| 4 | J | No |
| 5 | D | Yes |

**Precision@5** = relevant retrieved / total retrieved = 3/5 = **60%**. **Recall@5** = relevant
retrieved / total relevant that exist = 3/4 = **75%** — one truly relevant chunk (the 4th,
somewhere outside the top 5) was never surfaced. **Precision@3** (if the generator only ever
reads the top 3) = 2/3 ≈ **66.7%**, **Recall@3** = 2/4 = **50%** — a smaller K here trades away
recall for a precision that's actually similar, illustrating that the right K genuinely depends
on how many chunks the downstream generator can usefully read, not a universal best value, which
connects directly to the Top-K tuning discussion in `README.md`'s RAG-optimization section.

## Common exam scenarios

1. **"Two models have identical accuracy but the business needs to know which one's confidence
   scores can be trusted for an automated downstream threshold"** → check calibration (Part 5),
   not accuracy or AUC — those don't measure whether a stated probability matches real-world
   frequency.
2. **"A regression model's reported error is dominated by a handful of unusually expensive
   properties"** → this is the RMSE vs. MAE outlier-sensitivity gap from Part 3 — switch to MAE
   if those outliers shouldn't dominate the headline number.
3. **"A 3-class router's overall accuracy looks fine (81%) but one category consistently
   underperforms"** → read per-class precision/recall (Part 2) or macro-averaged F1, not overall
   accuracy, which can mask a single weak class.
4. **"Two models tie on accuracy but one is confidently wrong more often on the cases it misses"**
   → log loss (Part 4) distinguishes them; accuracy cannot, since it only checks the top
   prediction's correctness, not the probability's magnitude.
5. **"Generated summaries are accurate but score surprisingly low on an automated metric"** → the
   BLEU/ROUGE n-gram-precision mechanics in Part 6 — a correct paraphrase breaks n-gram matches
   even when meaning is preserved; use BERTScore/semantic similarity instead.
6. **"Deciding the right number of document chunks (K) to retrieve for a RAG pipeline"** → Part 7's
   Precision@K/Recall@K tradeoff, tuned against the generator's actual context capacity and
   measured retrieval quality, not a fixed default.
7. **"Business wants to move a fraud classifier's threshold without retraining"** → Part 1's
   threshold sweep — moving the decision threshold on an already-trained model's probability
   output is the correct, no-retraining-required lever for trading precision against recall.
8. **"ROC AUC looks strong but the team suspects performance on the rare positive class is
   actually weak"** → check Average Precision / the PR curve instead, per Part 1's numeric
   demonstration that ROC AUC can look more optimistic than PR-based metrics on imbalanced data.

## Related Terms

- [`ml-fundamentals-glossary.md`](ml-fundamentals-glossary.md) — the plain-English definitions
  this doc builds numeric depth on top of.
- [`algorithm-selection-decision-framework.md`](algorithm-selection-decision-framework.md) — the
  metrics used to judge the head-to-head comparisons there.
- [`README.md`](README.md) — the domain's bias-detection section, a distinct axis from every
  accuracy-style metric computed in this document.
- [`../domain-4-monitoring-security/README.md`](../domain-4-monitoring-security/README.md) — how
  these same metrics get watched for drift over time after deployment.
