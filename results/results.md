# PoultryBot: DALAN experiment results

Development set: 285 queries (263 answerable, 22 out-of-domain; en=119, ceb=89, tl=44, mix=33).
Held-out test set: 147 queries (129 answerable, 18 out-of-domain; en=65, ceb=35, tl=25, mix=22). Written before tuning; used once.
Reader assumptions rho=0.9, rho_d=0.7. eps=delta=0.05 for DALAN.

## Held-out test set (fit on all dev queries, evaluated once)

| Method | Accuracy % | Wrong % | Silent err % | LLM calls % | Abstain % | OOD abstain recall % | Latency GPU ms | Latency CPU ms |
|---|---|---|---|---|---|---|---|---|
| B0 Always-RAG (LLM for every query) | 57.6 | 19.1 | 0.0 | 100.0 | 0.0 | 0.0 | 1500 | 8000 |
| B1 Lexical, fixed thresholds (prototype) | 50.1 | 20.3 | 19.7 | 2.0 | 34.0 | 44.4 | 31 | 163 |
| B2 Hybrid lexical+char, fixed thresholds | 50.1 | 20.3 | 19.7 | 2.0 | 34.0 | 44.4 | 31 | 164 |
| B3 CSN + hybrid, fixed thresholds | 75.3 | 24.2 | 23.8 | 1.4 | 2.0 | 16.7 | 21 | 110 |
| A1 DALAN without CSN | 57.3 | 11.6 | 9.5 | 10.9 | 37.4 | 66.7 | 164 | 872 |
| A2 DALAN without char channel | 82.5 | 7.0 | 4.8 | 14.3 | 17.7 | 66.7 | 215 | 1143 |
| A3 DALAN without code-switch features | 78.8 | 14.4 | 12.9 | 10.2 | 12.2 | 44.4 | 154 | 817 |
| A4 DALAN with global thresholds | 77.4 | 15.1 | 15.0 | 1.4 | 15.6 | 66.7 | 21 | 110 |
| DALAN (full) | 77.7 | 14.4 | 13.6 | 6.1 | 15.6 | 66.7 | 93 | 491 |

### Test accuracy and wrong-answer rate by language (%)

| Method | en acc | ceb acc | tl acc | mix acc | en wrong | ceb wrong | tl wrong | mix wrong |
|---|---|---|---|---|---|---|---|---|
| B0 Always-RAG (LLM for every query) | 84.8 | 18.3 | 19.2 | 83.2 | 13.1 | 27.7 | 27.6 | 13.6 |
| B1 Lexical, fixed thresholds (prototype) | 71.8 | 14.3 | 20.0 | 77.3 | 27.1 | 14.3 | 12.0 | 19.5 |
| B2 Hybrid lexical+char, fixed thresholds | 71.8 | 14.3 | 20.0 | 77.3 | 27.1 | 14.3 | 12.0 | 19.5 |
| B3 CSN + hybrid, fixed thresholds | 71.8 | 74.3 | 80.0 | 81.8 | 27.1 | 25.7 | 20.0 | 18.2 |
| A1 DALAN without CSN | 80.2 | 19.4 | 22.8 | 89.1 | 18.8 | 5.1 | 6.4 | 6.4 |
| A2 DALAN without char channel | 83.8 | 76.3 | 84.4 | 86.4 | 10.5 | 3.7 | 4.8 | 4.5 |
| A3 DALAN without code-switch features | 80.0 | 70.3 | 78.4 | 89.5 | 16.9 | 15.4 | 13.6 | 5.9 |
| A4 DALAN with global thresholds | 75.4 | 76.6 | 72.0 | 90.9 | 21.5 | 9.1 | 16.0 | 4.5 |
| DALAN (full) | 75.4 | 76.3 | 74.0 | 90.9 | 21.5 | 9.4 | 11.2 | 4.5 |

### Paired bootstrap 95% confidence intervals on the test set (DALAN minus comparison, points)

| Compared with | Accuracy difference [95% CI] | Wrong-answer difference [95% CI] |
|---|---|---|
| B0 Always-RAG (LLM for every query) | +20.1 [+10.8, +29.3] | -4.8 [-10.3, +1.2] |
| B1 Lexical, fixed thresholds (prototype) | +27.6 [+19.9, +35.3] | -6.0 [-11.2, -1.1] |
| B2 Hybrid lexical+char, fixed thresholds | +27.6 [+19.9, +35.3] | -6.0 [-11.2, -1.1] |
| B3 CSN + hybrid, fixed thresholds | +2.4 [-2.7, +7.8] | -9.9 [-15.0, -5.4] |
| A1 DALAN without CSN | +20.4 [+12.2, +28.6] | +2.8 [-0.6, +6.5] |
| A2 DALAN without char channel | -4.8 [-9.7, -0.0] | +7.3 [+3.7, +11.5] |
| A3 DALAN without code-switch features | -1.2 [-4.9, +2.5] | +0.0 [-3.3, +3.3] |
| A4 DALAN with global thresholds | +0.3 [-0.6, +1.7] | -0.7 [-2.5, +0.5] |

## Development set, cross-validated

Protocol: 10 x 5-fold stratified CV on the dev set (50 folds). Mean +/- SD over folds.

| Method | Accuracy % | Wrong % | Silent err % | LLM calls % | Skip % | Abstain % | OOD abstain recall % | Latency GPU ms | Latency CPU ms |
|---|---|---|---|---|---|---|---|---|---|
| B0 Always-RAG (LLM for every query) | 57.2 +/- 2.7 | 18.5 +/- 0.6 | 0.0 +/- 0.0 | 100.0 +/- 0.0 | 0.0 +/- 0.0 | 0.0 +/- 0.0 | 0.0 +/- 0.0 | 1500 | 8000 |
| B1 Lexical, fixed thresholds (prototype) | 53.9 +/- 3.1 | 11.4 +/- 3.6 | 11.2 +/- 3.7 | 0.7 +/- 0.9 | 60.4 +/- 3.4 | 38.9 +/- 3.3 | 54.1 +/- 16.1 | 11 | 56 |
| B2 Hybrid lexical+char, fixed thresholds | 54.9 +/- 3.1 | 10.4 +/- 3.5 | 10.1 +/- 3.6 | 0.7 +/- 0.9 | 60.4 +/- 3.4 | 38.9 +/- 3.3 | 54.1 +/- 16.1 | 11 | 57 |
| B3 CSN + hybrid, fixed thresholds | 87.5 +/- 4.3 | 12.5 +/- 4.3 | 12.2 +/- 4.3 | 0.7 +/- 0.9 | 97.2 +/- 1.7 | 2.1 +/- 1.6 | 27.7 +/- 21.0 | 11 | 57 |
| A1 DALAN without CSN | 58.9 +/- 2.8 | 4.3 +/- 1.8 | 2.7 +/- 1.9 | 10.5 +/- 3.1 | 48.0 +/- 3.4 | 41.5 +/- 2.9 | 71.3 +/- 20.9 | 158 | 842 |
| A2 DALAN without char channel | 88.9 +/- 4.1 | 5.9 +/- 2.8 | 4.9 +/- 2.9 | 8.7 +/- 4.0 | 80.0 +/- 5.0 | 11.3 +/- 4.2 | 77.9 +/- 21.3 | 131 | 698 |
| A3 DALAN without code-switch features | 88.4 +/- 3.6 | 6.3 +/- 2.6 | 5.2 +/- 2.9 | 7.8 +/- 4.2 | 83.3 +/- 5.1 | 8.9 +/- 3.8 | 51.4 +/- 22.5 | 117 | 622 |
| A4 DALAN with global thresholds | 89.8 +/- 3.9 | 5.8 +/- 3.3 | 5.1 +/- 3.5 | 4.7 +/- 3.2 | 85.3 +/- 4.2 | 10.0 +/- 4.0 | 72.6 +/- 22.4 | 72 | 378 |
| DALAN (full) | 89.2 +/- 4.0 | 6.0 +/- 3.2 | 5.4 +/- 3.4 | 5.2 +/- 3.4 | 84.6 +/- 5.0 | 10.2 +/- 4.2 | 71.0 +/- 23.2 | 79 | 415 |

Latency = measured routing time + LLM call rate x assumed generation time (1500 ms GPU 7B 4-bit, 8000 ms CPU 3B 4-bit).
Mean routing time for DALAN: 0.89 ms per query (Python, single core).

## Accuracy by language (DALAN vs baselines)

| Method | en acc % | ceb acc % | tl acc % | mix acc % | en wrong % | ceb wrong % | tl wrong % | mix wrong % |
|---|---|---|---|---|---|---|---|---|
| B1 Lexical, fixed thresholds (prototype) | 87.8 | 14.6 | 20.3 | 82.0 | 12.2 | 9.0 | 9.1 | 18.0 |
| B2 Hybrid lexical+char, fixed thresholds | 90.3 | 14.6 | 20.3 | 82.0 | 9.7 | 9.0 | 9.1 | 18.0 |
| B3 CSN + hybrid, fixed thresholds | 90.3 | 87.7 | 84.2 | 82.1 | 9.7 | 12.3 | 15.8 | 17.9 |
| A1 DALAN without CSN | 95.1 | 16.2 | 24.3 | 89.7 | 4.8 | 2.8 | 1.7 | 10.0 |
| DALAN (full) | 90.8 | 87.8 | 90.2 | 86.2 | 5.1 | 6.7 | 3.8 | 10.7 |

## Oracle reader (rho = rho_d = 1)

| Method | Accuracy % | Wrong % | LLM calls % |
|---|---|---|---|
| B0 Always-RAG (LLM for every query) | 65.2 | 0.0 | 100.0 |
| B1 Lexical, fixed thresholds (prototype) | 54.1 | 11.2 | 0.7 |
| B2 Hybrid lexical+char, fixed thresholds | 55.1 | 10.1 | 0.7 |
| B3 CSN + hybrid, fixed thresholds | 87.8 | 12.2 | 0.7 |
| A1 DALAN without CSN | 60.2 | 2.7 | 10.5 |
| A2 DALAN without char channel | 89.8 | 4.9 | 8.7 |
| A3 DALAN without code-switch features | 89.4 | 5.2 | 7.8 |
| A4 DALAN with global thresholds | 90.5 | 5.1 | 4.7 |
| DALAN (full) | 89.9 | 5.4 | 5.2 |

## Paired Wilcoxon signed-rank tests vs DALAN (full), p-values over folds

| Compared with | Accuracy | Wrong-answer rate | LLM call rate |
|---|---|---|---|
| B0 Always-RAG (LLM for every query) | 7.6e-10 | 7.6e-10 | 7.3e-10 |
| B1 Lexical, fixed thresholds (prototype) | 7.6e-10 | 1e-08 | 4.1e-09 |
| B2 Hybrid lexical+char, fixed thresholds | 7.5e-10 | 1.1e-07 | 4.1e-09 |
| B3 CSN + hybrid, fixed thresholds | 0.0039 | 9e-10 | 4.1e-09 |
| A1 DALAN without CSN | 7.6e-10 | 0.00012 | 1.5e-08 |
| A2 DALAN without char channel | 0.18 | 0.65 | 2.8e-05 |
| A3 DALAN without code-switch features | 0.062 | 0.025 | 0.00054 |
| A4 DALAN with global thresholds | 0.04 | 0.59 | 0.54 |

Folds from repeated CV are not independent, so treat these p-values as indicative; confirm on a held-out real-query test set.

## Calibration quality (pooled out-of-fold predictions, first repeat)

| Calibrator | ECE all | Brier all | ECE code-switched | ECE English |
|---|---|---|---|---|
| DALAN (full) | 0.038 | 0.069 | 0.063 | 0.051 |
| A3 without code-switch features | 0.028 | 0.082 | 0.026 | 0.061 |

## Operating points (Pareto sweep, see pareto.png / pareto.csv)

| Method | param | LLM calls % | Wrong % | Accuracy % |
|---|---|---|---|---|
| DALAN (eps sweep) | 0.0 | 19.7 | 3.6 | 91.1 |
| DALAN (eps sweep) | 0.01 | 19.7 | 3.6 | 91.1 |
| DALAN (eps sweep) | 0.02 | 14.6 | 3.8 | 91.0 |
| DALAN (eps sweep) | 0.03 | 10.8 | 4.2 | 90.7 |
| DALAN (eps sweep) | 0.05 | 5.5 | 5.5 | 90.0 |
| DALAN (eps sweep) | 0.08 | 1.5 | 7.6 | 88.5 |
| DALAN (eps sweep) | 0.1 | 0.5 | 9.7 | 88.8 |
| DALAN (eps sweep) | 0.15 | 0.0 | 13.6 | 86.4 |
| DALAN (eps sweep) | 0.2 | 0.0 | 14.2 | 85.8 |
| DALAN (eps sweep) | 0.3 | 0.0 | 14.2 | 85.8 |
| B2 hybrid (threshold sweep) | 3 | 0.0 | 10.8 | 54.4 |
| B2 hybrid (threshold sweep) | 4 | 0.4 | 10.6 | 54.7 |
| B2 hybrid (threshold sweep) | 5 | 0.7 | 10.3 | 54.9 |
| B2 hybrid (threshold sweep) | 6 | 0.7 | 10.3 | 54.9 |
| B2 hybrid (threshold sweep) | 8 | 3.9 | 8.8 | 55.7 |
| B2 hybrid (threshold sweep) | 10 | 4.2 | 8.9 | 55.6 |
| B2 hybrid (threshold sweep) | 12 | 8.1 | 7.5 | 57.0 |
| B2 hybrid (threshold sweep) | 15 | 11.6 | 5.9 | 58.6 |
| B2 hybrid (threshold sweep) | 20 | 12.3 | 5.3 | 59.2 |
| B3 CSN + hybrid (threshold sweep) | 3 | 0.0 | 12.9 | 87.1 |
| B3 CSN + hybrid (threshold sweep) | 4 | 0.4 | 12.7 | 87.3 |
| B3 CSN + hybrid (threshold sweep) | 5 | 0.7 | 12.4 | 87.6 |
| B3 CSN + hybrid (threshold sweep) | 6 | 0.7 | 12.4 | 87.6 |
| B3 CSN + hybrid (threshold sweep) | 8 | 1.8 | 12.0 | 88.0 |
| B3 CSN + hybrid (threshold sweep) | 10 | 2.8 | 11.7 | 88.3 |
| B3 CSN + hybrid (threshold sweep) | 12 | 4.6 | 11.6 | 88.4 |
| B3 CSN + hybrid (threshold sweep) | 15 | 13.0 | 8.6 | 91.2 |
| B3 CSN + hybrid (threshold sweep) | 20 | 15.5 | 7.1 | 92.7 |

Gloss weight gamma chosen on training folds: 0.6: 50 folds.
