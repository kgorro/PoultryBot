# PoultryBot

A fast, low-cost assistant for small and medium poultry raisers in the Philippines. It answers questions about broilers, layers, native and free-range chickens, ducks, and quail in English, Cebuano, Tagalog, and mixes of them. It runs on modest hardware with a small local LLM, and most answers never call the LLM.

It uses DALAN (Dual-channel Agreement with Lexicon-Augmented Normalization), the routing algorithm first built for the Sugbo Guide tourism bot ([kgorro/Dalan](https://github.com/kgorro/Dalan)). Here it is adapted to poultry with a new knowledge base, a Cebuano and Tagalog poultry lexicon, and a held-out test set. See [docs/METHOD.md](docs/METHOD.md).

## What it covers

63 verified topics in 12 groups: health and diseases (18), layers (9), business (6), housing (4), feed and water (4), incubation (4), broilers (4), chicks and brooding (3), ducks and quail (3), eggs and meat safety (3), native and free-range (2), and getting started (2).

Safety rules built into the content and the LLM prompt:
- No drug or vaccine doses. Answers point to the product label and a licensed veterinarian.
- Newcastle disease and avian influenza are treated as reportable, with instructions to stop bird movement and call the veterinary office.
- Figures are typical ranges for guidance. Strain guides and suppliers come first.

## How a question is answered

1. Exact cache: a repeated question returns in under 1 ms.
2. DALAN router (about 1 ms, no neural model):
   - Code-switch normalization reduces Cebuano and Tagalog word forms (mangitlog, gitambalan, bumili, nagsisimula, nag-drop) to lexicon roots and adds English farm terms.
   - Lexical and character n-gram retrieval, fused by reciprocal rank.
   - A logistic calibrator estimates the chance the top topic is right.
   - Per-language thresholds decide: skip (verified answer, no LLM), generate (local LLM answers from the top 3 topics only), or abstain (decline and point to help).
3. If the LLM is offline on an uncertain question, the bot shows the closest topic, says it is not sure, and lists related topics.

## Results

Two query sets were written before tuning: a development set (285 queries) for tuning and cross-validation, and a held-out test set (147 queries) used once at the end. Both mix English, Cebuano, Tagalog, code-switched text, and out-of-domain questions such as pig, fish, and human medicine. Full tables are in [results/results.md](results/results.md).

| Method | Dev CV accuracy | Dev CV wrong | Test accuracy | Test wrong | Test LLM calls |
|---|---|---|---|---|---|
| Always-RAG (LLM for every query) | 57.2% | 18.5% | 57.6% | 19.1% | 100% |
| Fixed-threshold lexical router | 53.9% | 11.4% | 50.1% | 20.3% | 2.0% |
| Normalization + fixed thresholds | 87.5% | 12.5% | 75.3% | 24.2% | 1.4% |
| DALAN without character channel | 88.9% | 5.9% | 82.5% | 7.0% | 14.3% |
| **DALAN (full)** | **89.2%** | **6.0%** | **77.7%** | **14.4%** | **6.1%** |

What the held-out test shows:
- Code-switch normalization matters most. On test, accuracy on Cebuano queries rose from 14% to 76%, and on Tagalog from 20% to 74%, over the fixed lexical router.
- DALAN generalized worse than cross-validation suggested. Top-1 retrieval fell from 92% on dev, which the keywords and lexicon were tuned on, to 85% on test. The calibrator learned its confidence from that tuned data, so it skipped too often on new phrasings: 13.6% of test answers were confident wrong answers.
- On test, removing the character channel gave fewer wrong answers (7.0% vs 14.4%) at the cost of more LLM calls. That ablation was not chosen in advance, so treat it as a lead to confirm, not a result.
- The lesson for deployment: tune keywords and the lexicon on one set of queries, and fit the calibrator on a separate set that tuning never saw.

These numbers come from developer-written queries and an assumed LLM accuracy (90% when the right topic is in context). Real farmer questions are needed before any claim about field performance.

![Cost vs safety](results/pareto.png)

## Repository layout

    kb/build_kb.py          Knowledge base source (63 topics). Run it to regenerate kb/kb.json
    dalan/                  DALAN router: normalize.py, lexicon.py (305 Cebuano and Tagalog lemmas),
                            channels.py, calibrate.py, router.py, export.py (model for the browser)
    data/build_queries.py   Builds data/dev.jsonl and data/test.jsonl
    experiments/            run_experiments.py: dev cross-validation, baselines, ablations, Pareto sweep,
                            and the single held-out test evaluation with bootstrap confidence intervals
    results/                Generated tables and charts
    backend/app.py          FastAPI server: cache, DALAN, local LLM, safety note, Messenger webhook
    web/                    Browser demo: dalan.js (JavaScript port), page.html, build_page.py,
                            poultrybot.html (self-contained, opens directly)
    tests/                  test_dalan.py (unit and safety checks), test_parity.py (Python vs JavaScript)

## Quick start

    python -m venv .venv && source .venv/bin/activate      (Windows: .venv\Scripts\activate)
    pip install -r backend/requirements.txt

    python tests/test_dalan.py                  # unit and safety tests
    python tests/test_parity.py                 # browser router matches Python on all 437 queries (needs Node.js)
    python experiments/run_experiments.py       # reproduces results/

Run the bot with a local model (Ollama shown; llama.cpp and vLLM work through their OpenAI-compatible endpoints):

    ollama pull qwen2.5:7b-instruct             # check for newer small multilingual models first
    cd backend && uvicorn app:app --port 8000
    curl -X POST localhost:8000/chat -H "Content-Type: application/json" -d '{"question":"Nganong naay dugo ang iti sa akong manok?"}'

Environment variables: DALAN_EPS (error budget for verified answers, default 0.05; lower is more cautious), LLM_BASE_URL, LLM_MODEL, FB_VERIFY_TOKEN and FB_PAGE_TOKEN for Messenger.

Open web/poultrybot.html in a browser for the demo, no server needed. After changing the knowledge base, lexicon, or queries, rebuild it:

    python kb/build_kb.py && python data/build_queries.py
    python -m dalan.export && python web/build_page.py

## Before using with farmers

- Have a poultry veterinarian or DA extension officer review every topic, especially vaccination schedules and disease entries.
- Collect real farmer questions (Messenger logs, extension office FAQs), label them with two annotators, and split them into tuning, calibration, and test sets.
- Run the local LLM on those questions to measure answer quality instead of assuming it.
- Add contact details for the local agriculture and veterinary offices in each deployment area.

## Author

Ken D. Gorro, Center for Cloud Computing, Big Data and Artificial Intelligence, Cebu Technological University, Carmen Campus.
