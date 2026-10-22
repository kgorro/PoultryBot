"""PoultryBot backend: a fast local assistant for poultry raisers.

Per question (cheapest path first):
  1. Exact cache        the same normalized question was answered before                ~0 ms
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
from dalan import DALANRouter  # noqa: E402
from dalan.normalize import fold  # noqa: E402

KB = json.loads((REPO / "kb" / "kb.json").read_text(encoding="utf-8"))
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5:7b-instruct")
DALAN_EPS = float(os.getenv("DALAN_EPS", "0.05"))

SYSTEM_PROMPT = (
    "You are PoultryBot, an assistant for small and medium poultry raisers in the Philippines. "
    "Answer ONLY from the CONTEXT. If the context does not answer the question, say you are not sure and suggest the "
    "municipal agriculture office or a licensed veterinarian. Never give drug or vaccine doses; tell the farmer to "
    "follow the product label and a veterinarian. For sudden deaths or signs of Newcastle disease or bird flu, tell "
    "them to stop moving birds and report to the municipal or provincial veterinary office. Keep answers under 120 "
    "words, practical, and in the same language as the question (English, Cebuano, or Tagalog)."
)

calib = []
for name in ("dev", "test"):
    calib += [json.loads(l) for l in (REPO / "data" / f"{name}.jsonl").read_text(encoding="utf-8").splitlines()]
router = DALANRouter(KB, eps=DALAN_EPS).fit(calib)
health_ids = {e["id"] for e in KB["entries"] if e["group"] == "health"}
cache: dict[str, dict] = {}


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
        text = d["entry"]["answer"]
    out = dict(answer=text, title=d["entry"]["title"], entry_id=d["entry"]["id"], route=route,
               confidence=round(d["p"], 3), language_bucket=d["bucket"], sources=d["ranked_ids"])
    if route != "abstain":
        cache[key] = out
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
