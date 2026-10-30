"""PoultryBot backend: a fast local assistant for poultry raisers.

Startup: loads the prebuilt dump in dist/ (python -m dalan.dump) instead of refitting the router. If the dump
is missing or older than the KB or code, it refits and says so.

Per question (cheapest path first):
  1. Exact cache        the same normalized question is in the dump, or was answered     ~0 ms
                        before (LLM answers are saved to dist/llm_answers.jsonl and
                        reloaded at startup, so each generated answer is paid for once)
  2. DALAN router       code-switch normalization, lexical + character retrieval,       ~1 ms
                        calibrated confidence, per-language risk-controlled thresholds
       skip      answer straight from the verified knowledge base (no LLM call)
       generate  a small local LLM writes the answer from the top 3 entries only
       abstain   decline and point the user to the right help (never a made-up answer)
  3. Safety guard       any answer touching sick birds keeps the veterinarian referral

The LLM is any OpenAI-compatible server on the local machine:
  Ollama:     LLM_BASE_URL=http://localhost:11434/v1   LLM_MODEL=qwen2.5:7b-instruct
  llama.cpp:  llama-server -m model.gguf --port 8080   LLM_BASE_URL=http://localhost:8080/v1
  vLLM:       vllm serve <model> --port 8000           LLM_BASE_URL=http://localhost:8000/v1
"""
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, StreamingResponse
from pydantic import BaseModel

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from dalan.dump import load as load_dump  # noqa: E402
from dalan.export import fitted_router  # noqa: E402
from dalan.normalize import fold  # noqa: E402

KB = json.loads((REPO / "kb" / "kb.json").read_text(encoding="utf-8"))
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5:7b-instruct")
DALAN_EPS = float(os.getenv("DALAN_EPS", "0.05"))

SYSTEM_PROMPT = (REPO / "kb" / "system_prompt.txt").read_text(encoding="utf-8").strip()

DIST = REPO / "dist"
_t0 = time.perf_counter()
_dump = load_dump(DALAN_EPS, DIST)
if _dump:
    router, _routes = _dump
    STARTUP = f"loaded dump from dist/ in {(time.perf_counter() - _t0) * 1000:.0f} ms"
else:
    router = fitted_router(DALAN_EPS)
    _routes = {}
    STARTUP = f"no current dump, refitted in {(time.perf_counter() - _t0) * 1000:.0f} ms (run: python -m dalan.dump)"
print("PoultryBot:", STARTUP, flush=True)
BY_ID = {e["id"]: e for e in KB["entries"]}
health_ids = {e["id"] for e in KB["entries"] if e["group"] == "health" or e["id"].startswith(("res-parasite", "res-serology"))}
KB_HASH = hashlib.sha256((REPO / "kb" / "kb.json").read_bytes()).hexdigest()[:16]
LLM_STORE = DIST / "llm_answers.jsonl"


def render(entry, ranked):
    """KB answer text. Research entries from one study are close siblings, so name the related findings too."""
    text = entry["answer"]
    if entry["group"] == "research":
        rel = [BY_ID[i]["title"] for i in ranked if i != entry["id"] and BY_ID[i]["group"] == "research"]
        if rel:
            text += "\n\nRelated findings you can ask about: " + "; ".join(rel) + "."
    return text


def _out(text, entry, route, p, bucket, ranked):
    return dict(answer=text, title=entry["title"], entry_id=entry["id"], route=route, confidence=round(p, 3),
                language_bucket=bucket, sources=ranked)


# Answer cache: precomputed skip/abstain routes from the dump, plus LLM answers saved by earlier runs
cache: dict[str, dict] = {}
for key, r in _routes.items():
    if r["action"] == "skip":
        e = BY_ID[r["entry_id"]]
        cache[key] = _out(render(e, r["ranked_ids"]), e, "skip", r["p"], r["bucket"], r["ranked_ids"])
if LLM_STORE.exists():
    for line in LLM_STORE.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row.get("kb") == KB_HASH:
            cache[row["key"]] = row["out"]


def remember_llm(key, out):
    DIST.mkdir(exist_ok=True)
    with LLM_STORE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(dict(key=key, kb=KB_HASH, out=out), ensure_ascii=False) + "\n")


def build_messages(question, context):
    ctx = "\n\n".join(f"[{e['title']}]\n{e['answer']}" for e in context)
    return [{"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"CONTEXT:\n{ctx}\n\nQUESTION: {question}"}]


async def llm_complete(question, context):
    async with httpx.AsyncClient(timeout=90) as client:
        r = await client.post(f"{LLM_BASE_URL}/chat/completions", json=dict(
            model=LLM_MODEL, messages=build_messages(question, context), temperature=0.2, max_tokens=300))
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()


async def llm_stream(question, context):
    async with httpx.AsyncClient(timeout=90) as client:
        async with client.stream("POST", f"{LLM_BASE_URL}/chat/completions", json=dict(
                model=LLM_MODEL, messages=build_messages(question, context), temperature=0.2, max_tokens=300,
                stream=True)) as r:
            async for line in r.aiter_lines():
                if line.startswith("data: ") and not line.endswith("[DONE]"):
                    delta = json.loads(line[6:])["choices"][0]["delta"].get("content")
                    if delta:
                        yield delta


VET_NOTE = "\n\nFor sick birds, confirm the diagnosis and treatment with a licensed veterinarian."


async def answer(question: str) -> dict:
    t0 = time.perf_counter()
    key = fold(question)
    if key in cache:
        return {**cache[key], "route": "cache", "ms": round((time.perf_counter() - t0) * 1000, 2)}
    d = router.route(question)
    route = d["action"]
    if route == "generate":
        try:
            text = await llm_complete(question, d["context"])
            if any(e["id"] in health_ids for e in d["context"][:1]) and "veterinar" not in text.lower():
                text += VET_NOTE
        except Exception:
            # LLM offline on an uncertain question: show the closest verified entry, say so, and list alternatives
            others = "; ".join(e["title"] for e in d["context"][1:])
            text = ("I'm not fully sure this matches your question. The closest topic I have is below.\n\n"
                    f"{d['entry']['answer']}\n\nRelated topics: {others}.")
            route = "skip-degraded"
    else:
        text = render(d["entry"], d["ranked_ids"]) if route == "skip" else d["entry"]["answer"]
    out = _out(text, d["entry"], route, d["p"], d["bucket"], d["ranked_ids"])
    if route in ("skip", "generate"):
        cache[key] = out
        if route == "generate":
            remember_llm(key, out)
    out["ms"] = round((time.perf_counter() - t0) * 1000, 2)
    return out


app = FastAPI(title="PoultryBot")


class Ask(BaseModel):
    question: str


@app.post("/chat")
async def chat(body: Ask):
    return await answer(body.question)


@app.post("/chat/stream")
async def chat_stream(body: Ask):
    """Streams tokens on the generate route so the first words appear immediately."""
    d = router.route(body.question)
    if d["action"] != "generate":
        return PlainTextResponse(d["entry"]["answer"])
    return StreamingResponse(llm_stream(body.question, d["context"]), media_type="text/plain")


@app.get("/health")
def health():
    return dict(startup=STARTUP, entries=len(KB["entries"]), cached_answers=len(cache))


@app.get("/topics")
def topics(group: str | None = None):
    return [dict(id=e["id"], group=e["group"], title=e["title"]) for e in KB["entries"]
            if e["id"] != "fallback" and group in (None, e["group"])]


@app.get("/", response_class=HTMLResponse)
def home():
    return (REPO / "web" / "poultrybot.html").read_text(encoding="utf-8")


# ------------------------------------------------------------------ Facebook Messenger
FB_VERIFY_TOKEN = os.getenv("FB_VERIFY_TOKEN", "")
FB_PAGE_TOKEN = os.getenv("FB_PAGE_TOKEN", "")


@app.get("/messenger")
def messenger_verify(request: Request):
    p = request.query_params
    if p.get("hub.mode") == "subscribe" and p.get("hub.verify_token") == FB_VERIFY_TOKEN:
        return PlainTextResponse(p.get("hub.challenge", ""))
    return PlainTextResponse("forbidden", status_code=403)


@app.post("/messenger")
async def messenger_webhook(request: Request):
    data = await request.json()
    async with httpx.AsyncClient(timeout=20) as client:
        for entry in data.get("entry", []):
            for ev in entry.get("messaging", []):
                text = ev.get("message", {}).get("text")
                if not text:
                    continue
                res = await answer(text)
                await client.post("https://graph.facebook.com/v19.0/me/messages", params={"access_token": FB_PAGE_TOKEN},
                                  json={"recipient": {"id": ev["sender"]["id"]}, "message": {"text": res["answer"][:1990]}})
    return {"ok": True}
