# PoultryBot: DALAN experiment results

Development set: 327 queries (305 answerable, 22 out-of-domain; en=147, ceb=97, tl=50, mix=33).
Held-out test set: 147 queries (129 answerable, 18 out-of-domain; en=65, ceb=35, tl=25, mix=22). Written before tuning; used once.
Reader assumptions rho=0.9, rho_d=0.7. eps=delta=0.05 for DALAN.

## Held-out test set (fit on all dev queries, evaluated once)

| Method | Accuracy % | Wrong % | Silent err % | LLM calls % | Abstain % | OOD abstain recall % | Latency GPU ms | Latency CPU ms |
|---|---|---|---|---|---|---|---|---|
| B0 Always-RAG (LLM for every query) | 57.6 | 19.1 | 0.0 | 100.0 | 0.0 | 0.0 | 1500 | 8000 |
| B1 Lexical, fixed thresholds (prototype) | 49.5 | 21.7 | 21.1 | 2.0 | 32.7 | 38.9 | 31 | 163 |
| B2 Hybrid lexical+char, fixed thresholds | 49.5 | 21.7 | 21.1 | 2.0 | 32.7 | 38.9 | 31 | 164 |
| B3 CSN + hybrid, fixed thresholds | 75.3 | 24.2 | 23.8 | 1.4 | 2.0 | 16.7 | 21 | 110 |
| A1 DALAN without CSN | 55.3 | 13.5 | 11.6 | 10.2 | 36.1 | 55.6 | 154 | 817 |
| A2 DALAN without char channel | 81.6 | 9.5 | 6.8 | 16.3 | 13.6 | 50.0 | 245 | 1306 |
| A3 DALAN without code-switch features | 74.4 | 17.0 | 16.3 | 5.4 | 12.9 | 38.9 | 82 | 436 |
| A4 DALAN with global thresholds | 76.0 | 16.1 | 15.6 | 2.7 | 14.3 | 55.6 | 42 | 218 |
| DALAN (full) | 75.9 | 15.7 | 15.0 | 4.8 | 14.3 | 55.6 | 72 | 382 |

### Test accuracy and wrong-answer rate by language (%)

| Method | en acc | ceb acc | tl acc | mix acc | en wrong | ceb wrong | tl wrong | mix wrong |
|---|---|---|---|---|---|---|---|---|
| B0 Always-RAG (LLM for every query) | 84.8 | 18.3 | 19.2 | 83.2 | 13.1 | 27.7 | 27.6 | 13.6 |
| B1 Lexical, fixed thresholds (prototype) | 71.8 | 11.4 | 20.0 | 77.3 | 27.1 | 20.0 | 12.0 | 19.5 |
| B2 Hybrid lexical+char, fixed thresholds | 71.8 | 11.4 | 20.0 | 77.3 | 27.1 | 20.0 | 12.0 | 19.5 |
| B3 CSN + hybrid, fixed thresholds | 71.8 | 74.3 | 80.0 | 81.8 | 27.1 | 25.7 | 20.0 | 18.2 |
| A1 DALAN without CSN | 80.2 | 14.0 | 22.8 | 84.5 | 18.8 | 10.6 | 6.4 | 10.9 |
| A2 DALAN without char channel | 80.0 | 78.6 | 88.0 | 83.6 | 11.7 | 8.0 | 8.0 | 7.3 |
| A3 DALAN without code-switch features | 73.8 | 70.9 | 74.0 | 81.8 | 20.0 | 15.7 | 14.0 | 13.6 |
| A4 DALAN with global thresholds | 76.8 | 71.1 | 71.6 | 86.4 | 20.2 | 12.6 | 16.4 | 9.1 |
| DALAN (full) | 75.4 | 71.1 | 74.4 | 86.4 | 21.5 | 12.6 | 10.8 | 9.1 |

### Paired bootstrap 95% confidence intervals on the test set (DALAN minus comparison, points)

| Compared with | Accuracy difference [95% CI] | Wrong-answer difference [95% CI] |
|---|---|---|
| B0 Always-RAG (LLM for every query) | +18.3 [+8.6, +27.7] | -3.4 [-9.1, +2.7] |
| B1 Lexical, fixed thresholds (prototype) | +26.4 [+18.8, +34.2] | -6.0 [-11.2, -1.2] |
| B2 Hybrid lexical+char, fixed thresholds | +26.4 [+18.8, +34.2] | -6.0 [-11.2, -1.2] |
| B3 CSN + hybrid, fixed thresholds | +0.5 [-4.2, +5.4] | -8.5 [-13.2, -4.4] |
| A1 DALAN without CSN | +20.5 [+12.3, +28.8] | +2.2 [-1.5, +6.1] |
| A2 DALAN without char channel | -5.7 [-10.3, -1.4] | +6.2 [+2.7, +10.3] |
| A3 DALAN without code-switch features | +1.5 [-1.8, +5.0] | -1.3 [-4.8, +2.2] |
| A4 DALAN with global thresholds | -0.1 [-1.9, +1.7] | -0.3 [-2.3, +1.5] |

## Development set, cross-validated

Protocol: 10 x 5-fold stratified CV on the dev set (50 folds). Mean +/- SD over folds.

| Method | Accuracy % | Wrong % | Silent err % | LLM calls % | Skip % | Abstain % | OOD abstain recall % | Latency GPU ms | Latency CPU ms |
|---|---|---|---|---|---|---|---|---|---|
| B0 Always-RAG (LLM for every query) | 61.4 +/- 2.7 | 17.4 +/- 0.6 | 0.0 +/- 0.0 | 100.0 +/- 0.0 | 0.0 +/- 0.0 | 0.0 +/- 0.0 | 0.0 +/- 0.0 | 1500 | 8000 |
| B1 Lexical, fixed thresholds (prototype) | 58.2 +/- 3.5 | 11.8 +/- 3.3 | 11.6 +/- 3.4 | 0.6 +/- 0.9 | 66.1 +/- 3.0 | 33.3 +/- 3.2 | 49.6 +/- 20.6 | 9 | 49 |
| B2 Hybrid lexical+char, fixed thresholds | 59.7 +/- 3.1 | 10.3 +/- 3.2 | 10.1 +/- 3.2 | 0.6 +/- 0.9 | 66.1 +/- 3.0 | 33.3 +/- 3.2 | 49.6 +/- 20.6 | 10 | 50 |
| B3 CSN + hybrid, fixed thresholds | 88.5 +/- 3.5 | 11.5 +/- 3.5 | 11.3 +/- 3.6 | 0.6 +/- 0.9 | 97.6 +/- 1.7 | 1.8 +/- 1.5 | 27.2 +/- 22.9 | 10 | 50 |
| A1 DALAN without CSN | 62.4 +/- 3.2 | 4.8 +/- 2.7 | 3.6 +/- 2.8 | 8.0 +/- 3.1 | 55.3 +/- 3.8 | 36.8 +/- 3.3 | 69.3 +/- 18.8 | 120 | 637 |
| A2 DALAN without char channel | 89.2 +/- 3.2 | 6.0 +/- 2.8 | 5.0 +/- 2.9 | 8.8 +/- 3.6 | 81.4 +/- 3.9 | 9.8 +/- 3.1 | 75.1 +/- 19.2 | 132 | 701 |
| A3 DALAN without code-switch features | 89.6 +/- 3.3 | 5.7 +/- 2.7 | 4.7 +/- 2.9 | 8.3 +/- 3.8 | 83.2 +/- 5.3 | 8.6 +/- 3.3 | 59.3 +/- 24.1 | 125 | 662 |
| A4 DALAN with global thresholds | 89.4 +/- 3.6 | 5.7 +/- 2.8 | 5.4 +/- 2.9 | 2.9 +/- 2.3 | 87.6 +/- 3.4 | 9.5 +/- 2.7 | 69.6 +/- 20.3 | 45 | 234 |
| DALAN (full) | 89.7 +/- 3.1 | 5.9 +/- 2.6 | 5.4 +/- 2.7 | 4.3 +/- 3.1 | 86.8 +/- 3.6 | 9.0 +/- 2.5 | 69.2 +/- 21.9 | 65 | 342 |

Latency = measured routing time + LLM call rate x assumed generation time (1500 ms GPU 7B 4-bit, 8000 ms CPU 3B 4-bit).
Mean routing time for DALAN: 0.92 ms per query (Python, single core).

## Accuracy by language (DALAN vs baselines)

| Method | en acc % | ceb acc % | tl acc % | mix acc % | en wrong % | ceb wrong % | tl wrong % | mix wrong % |
|---|---|---|---|---|---|---|---|---|
| B1 Lexical, fixed thresholds (prototype) | 87.3 | 20.6 | 30.0 | 82.0 | 12.7 | 10.3 | 8.0 | 18.0 |
| B2 Hybrid lexical+char, fixed thresholds | 90.7 | 20.6 | 30.0 | 82.0 | 9.3 | 10.3 | 8.0 | 18.0 |
| B3 CSN + hybrid, fixed thresholds | 90.7 | 88.7 | 86.0 | 82.0 | 9.3 | 11.3 | 14.0 | 18.0 |
| A1 DALAN without CSN | 94.7 | 21.2 | 29.0 | 90.5 | 5.0 | 5.0 | 0.9 | 9.5 |
| DALAN (full) | 91.0 | 87.1 | 92.6 | 87.1 | 5.3 | 7.2 | 3.0 | 9.6 |

## Oracle reader (rho = rho_d = 1)

| Method | Accuracy % | Wrong % | LLM calls % |
|---|---|---|---|
| B0 Always-RAG (LLM for every query) | 69.7 | 0.0 | 100.0 |
| B1 Lexical, fixed thresholds (prototype) | 58.4 | 11.6 | 0.6 |
| B2 Hybrid lexical+char, fixed thresholds | 59.9 | 10.1 | 0.6 |
| B3 CSN + hybrid, fixed thresholds | 88.7 | 11.3 | 0.6 |
| A1 DALAN without CSN | 63.4 | 3.6 | 8.0 |
| A2 DALAN without char channel | 90.2 | 5.0 | 8.8 |
| A3 DALAN without code-switch features | 90.5 | 4.7 | 8.3 |
| A4 DALAN with global thresholds | 89.8 | 5.4 | 2.9 |
| DALAN (full) | 90.2 | 5.4 | 4.3 |

## Paired Wilcoxon signed-rank tests vs DALAN (full), p-values over folds

| Compared with | Accuracy | Wrong-answer rate | LLM call rate |
|---|---|---|---|
| B0 Always-RAG (LLM for every query) | 7.5e-10 | 7.6e-10 | 7.4e-10 |
| B1 Lexical, fixed thresholds (prototype) | 7.6e-10 | 9.1e-10 | 3.6e-08 |
| B2 Hybrid lexical+char, fixed thresholds | 7.6e-10 | 2.7e-09 | 3.6e-08 |
| B3 CSN + hybrid, fixed thresholds | 0.0031 | 1.8e-15 | 3.6e-08 |
| A1 DALAN without CSN | 7.6e-10 | 0.012 | 6.4e-06 |
| A2 DALAN without char channel | 0.19 | 0.58 | 9e-08 |
| A3 DALAN without code-switch features | 0.68 | 0.54 | 1.9e-07 |
| A4 DALAN with global thresholds | 0.22 | 0.023 | 0.0034 |

Folds from repeated CV are not independent, so treat these p-values as indicative; confirm on a held-out real-query test set.

## Calibration quality (pooled out-of-fold predictions, first repeat)

| Calibrator | ECE all | Brier all | ECE code-switched | ECE English |
|---|---|---|---|---|
| DALAN (full) | 0.041 | 0.069 | 0.052 | 0.056 |
| A3 without code-switch features | 0.040 | 0.075 | 0.039 | 0.052 |

## Operating points (Pareto sweep, see pareto.png / pareto.csv)

| Method | param | LLM calls % | Wrong % | Accuracy % |
|---|---|---|---|---|
| DALAN (eps sweep) | 0.0 | 23.4 | 3.9 | 91.0 |
| DALAN (eps sweep) | 0.01 | 19.4 | 4.2 | 90.9 |
| DALAN (eps sweep) | 0.02 | 12.8 | 4.4 | 90.7 |
| DALAN (eps sweep) | 0.03 | 8.9 | 4.7 | 90.4 |
| DALAN (eps sweep) | 0.05 | 4.1 | 6.3 | 89.2 |
| DALAN (eps sweep) | 0.08 | 0.9 | 7.8 | 88.8 |
| DALAN (eps sweep) | 0.1 | 0.2 | 9.7 | 89.1 |
| DALAN (eps sweep) | 0.15 | 0.0 | 12.7 | 87.3 |
| DALAN (eps sweep) | 0.2 | 0.0 | 13.1 | 86.9 |
| DALAN (eps sweep) | 0.3 | 0.0 | 13.1 | 86.9 |
| B2 hybrid (threshold sweep) | 3 | 0.0 | 10.7 | 59.3 |
| B2 hybrid (threshold sweep) | 4 | 0.3 | 10.5 | 59.5 |
| B2 hybrid (threshold sweep) | 5 | 0.6 | 10.3 | 59.7 |
| B2 hybrid (threshold sweep) | 6 | 0.6 | 10.3 | 59.7 |
| B2 hybrid (threshold sweep) | 8 | 3.3 | 9.0 | 60.4 |
| B2 hybrid (threshold sweep) | 10 | 3.6 | 9.0 | 60.4 |
| B2 hybrid (threshold sweep) | 12 | 7.0 | 7.8 | 61.6 |
| B2 hybrid (threshold sweep) | 15 | 10.7 | 5.9 | 63.4 |
| B2 hybrid (threshold sweep) | 20 | 11.3 | 5.4 | 64.0 |
| B3 CSN + hybrid (threshold sweep) | 3 | 0.0 | 11.9 | 88.1 |
| B3 CSN + hybrid (threshold sweep) | 4 | 0.3 | 11.7 | 88.3 |
| B3 CSN + hybrid (threshold sweep) | 5 | 0.6 | 11.5 | 88.5 |
| B3 CSN + hybrid (threshold sweep) | 6 | 0.6 | 11.5 | 88.5 |
| B3 CSN + hybrid (threshold sweep) | 8 | 1.5 | 11.1 | 88.9 |
| B3 CSN + hybrid (threshold sweep) | 10 | 2.7 | 10.9 | 89.1 |
| B3 CSN + hybrid (threshold sweep) | 12 | 4.0 | 11.0 | 89.0 |
| B3 CSN + hybrid (threshold sweep) | 15 | 12.2 | 8.2 | 91.6 |
| B3 CSN + hybrid (threshold sweep) | 20 | 14.4 | 6.9 | 92.9 |

Gloss weight gamma chosen on training folds: 0.6: 50 folds.

## Local research packs (data/test_research.jsonl)

16 questions on the 14 entries from kb/sources/*.md, written with the dev questions for those entries. DALAN fitted on all dev queries. The set was looked at once before the last keyword edits (which were driven by dev errors), so treat it as a check, not a clean held-out estimate.

| Top-1 % | Gold in top 3 % | Skip % | Wrong skips (of all) % | Generate % | Abstain % |
|---|---|---|---|---|---|
| 68.8 | 93.8 | 87.5 | 18.8 | 0.0 | 12.5 |
