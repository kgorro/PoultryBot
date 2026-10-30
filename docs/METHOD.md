# DALAN for poultry: method and evaluation notes

DALAN (Dual-channel Agreement with Lexicon-Augmented Normalization) decides, for each question, whether to answer from the verified knowledge base (skip), call a small local LLM with the top 3 topics (generate), or decline (abstain). The algorithm is described in full in the Dalan repository (docs/ALGORITHM.md). This file records what changed for poultry and how it was evaluated.

## Changes from the tourism version

- Knowledge base: 63 poultry topics in 12 groups, plus 14 local research topics in a 13th group (see below), written with fixed safety rules: no drug or vaccine doses, reportable-disease instructions for Newcastle disease and avian influenza, and a veterinarian referral on every disease topic.
- Lexicon: 305 Cebuano and Tagalog lemmas (200 Cebuano, 105 Tagalog) for birds, eggs, feed, housing, symptoms, predators, treatment, business, and common verbs. Loanwords that English-speaking farmers also use (balut, penoy, darak, itik, pugo) are left out of the lexicon so they do not count as code-switching.
- Normalization, three additions motivated by dev-set errors:
  - An English stem with a local prefix joined by a hyphen (nag-drop, maka-sell, mag-deworm) is read as the English stem and counted as code-switched.
  - Tagalog syllable reduplication is stripped (nagsisimula to simula, iniinom to inom).
  - More prefixes: gina-, mi-, pagpa-, mai-, makaka-, makakapag-, makapang-.
- Retrieval: the region cues used for North and South Cebu were removed, so the lexical channel is domain-neutral.
- Thresholds: decisions use a 1e-9 tolerance, so the Python and browser routers agree exactly when a score falls on a threshold.

## Evaluation design

- Development set (285 queries) and held-out test set (147 queries), written together before any tuning, with no overlapping questions.
- The lexicon and topic keywords were tuned by reading errors on the development set only.
- Cross-validation (10 × 5 folds) on the development set, as in the tourism study.
- Final evaluation: every method is fitted on the whole development set and run once on the test set, with paired bootstrap 95% confidence intervals.

## Findings

Figures below are from the current run (development set of 327 queries, with the research packs). The first run, before the packs, is in git history.

1. Normalization is what makes local-language queries answerable. On the test set, Cebuano accuracy went from 11% (fixed lexical router) to 71%, and Tagalog from 20% to 74%.
2. Calibrating on tuned data inflates confidence. Top-1 retrieval was 92% on dev and 85% on test. DALAN's skip thresholds, fitted on dev, admitted 15.0% confident wrong answers on test, against 5.4% in dev cross-validation. Cross-validation could not reveal this, because the same queries guided the keyword and lexicon edits.
3. The character channel helped on dev but hurt on test (wrong answers 8.8% without it, 15.7% with it). This comparison was not planned before seeing the test results, so it needs confirmation on new data.
4. DALAN still beat the baselines on the test set while calling the LLM on 4.8% of questions. Against the fixed lexical router it gained 26.4 accuracy points (95% CI +18.8 to +34.2) and had 6.0 points fewer wrong answers (95% CI −11.2 to −1.2). Against always-RAG it gained 18.3 accuracy points (95% CI +8.6 to +27.7); its 3.4-point drop in wrong answers was not significant (95% CI −9.1 to +2.7).

## Local research packs (2026-10)

- Source: four Cebu and Bantayan layer-farm studies, written as markdown packs in kb/sources/ and parsed by kb/ingest_md.py into 14 entries with citations.
- Scope gate: a pack lists cue words (places such as Bantayan and Cebu, and research words such as study, survey, percent); an entry can add its own cues (for example antibody, tapeworm, price). The router zeroes a gated entry's lexical and character scores when the query has none of its cues. Cue words are removed from the entry keywords so they open the gate without deciding between sibling entries.
- Two-tier IDF: terms that occur in ungated entries keep the IDF computed over ungated entries only; terms unique to gated entries use IDF over all entries. With both, top-1 retrieval on the original test set is identical to the run before the packs (checked query by query).
- Effect on the original test set: accuracy 77.7% to 75.9%, wrong answers 14.4% to 15.7%. Retrieval did not change; the 42 new dev questions are easy (about 95% top-1) and shifted the calibrator toward more confidence. This was not corrected using the test set.
- On data/test_research.jsonl (16 questions): top-1 69%, gold in top 3 94%, wrong skips 19%. Most errors choose a sibling finding from the same study; the backend now lists the related findings under every research answer. The set was seen once before the final keyword edits, which were driven by dev errors.
- The Python and browser routers both implement the gate; parity holds on all 498 test queries.

## Recommended protocol for the next round

- Collect real farmer questions and split them three ways: tuning (lexicon and keywords), calibration (calibrator and thresholds), and test.
- Use a finite-sample bound, not raw precision, when choosing the skip threshold. For example, require the lower Wilson or Clopper-Pearson bound on skip precision to stay at or above 1 − ε.
- Measure the local LLM's answer quality on the generate route instead of assuming ρ = 0.9.
- For deployment, a lower error budget (DALAN_EPS = 0.02 to 0.03) is a reasonable default for disease questions, at the cost of more LLM calls.
