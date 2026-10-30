"""Builds the PoultryBot knowledge dump: everything the backend needs, precomputed, so it starts in milliseconds
and most questions need no routing work at all.

    python -m dalan.dump            # writes dist/

dist/router.pkl              fitted DALAN router (normalizer, both channel indexes, calibrator, thresholds)
dist/answer_cache.json       every known question (KB sample questions + dev/test queries) -> routed answer
dist/manifest.json           hashes of the KB, query sets, and code the dump was built from
dist/poultrybot_knowledge.md the whole KB as one markdown file, for a system prompt or a fine-tuning corpus
dist/finetune_chat.jsonl     question/answer pairs in chat format, if you later want to fine-tune a local model

The backend checks the manifest; if the KB or code changed since the dump was built it refits instead of
serving stale answers. Only load router.pkl files you built yourself: pickle files can run code.
"""
import hashlib
import json
import pickle
import sys
import time
from pathlib import Path

from .export import fitted_router
from .normalize import fold

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
HASHED = ["kb/kb.json", "kb/system_prompt.txt", "data/dev.jsonl", "data/test.jsonl", "dalan/normalize.py", "dalan/channels.py",
          "dalan/calibrate.py", "dalan/router.py", "dalan/lexicon.py"]


def fingerprint():
    h = {}
    for rel in HASHED:
        h[rel] = hashlib.sha256((ROOT / rel).read_bytes()).hexdigest()[:16]
    return h


def known_questions(kb):
    qs = []
    for e in kb["entries"]:
        qs += e["questions"]
    for name in ("dev", "test", "test_research"):
        p = ROOT / "data" / f"{name}.jsonl"
        if p.exists():
            qs += [json.loads(l)["q"] for l in p.read_text(encoding="utf-8").splitlines()]
    return list(dict.fromkeys(qs))


def build_cache(router, questions):
    cache = {}
    for q in questions:
        key = fold(q)
        if not key or key in cache:
            continue
        d = router.route(q)
        cache[key] = dict(action=d["action"], entry_id=d["entry"]["id"], p=round(d["p"], 4), bucket=d["bucket"],
                          ranked_ids=d["ranked_ids"])
    return cache


def kb_markdown(kb):
    lines = [f"# {kb['name']} (verified {kb['verified']})", "",
             "Rules: never give drug or vaccine doses; Newcastle disease and avian influenza are reportable; "
             "refer sick flocks to a licensed veterinarian.", ""]
    group = None
    for e in kb["entries"]:
        if e["id"] == "fallback":
            continue
        if e["group"] != group:
            group = e["group"]
            lines += [f"## {group}", ""]
        lines += [f"### {e['title']}", f"id: {e['id']}"]
        if e["questions"]:
            lines.append("Sample questions: " + " | ".join(e["questions"]))
        lines += ["", e["answer"], ""]
    return "\n".join(lines)


def finetune_rows(kb, system):
    for e in kb["entries"]:
        for q in e["questions"]:
            yield dict(messages=[{"role": "system", "content": system}, {"role": "user", "content": q},
                                 {"role": "assistant", "content": e["answer"]}])


def build(eps=0.05, out=DIST):
    t0 = time.perf_counter()
    router = fitted_router(eps)
    fit_s = time.perf_counter() - t0
    out.mkdir(exist_ok=True)
    with (out / "router.pkl").open("wb") as f:
        pickle.dump(router, f, protocol=pickle.HIGHEST_PROTOCOL)
    cache = build_cache(router, known_questions(router.kb))
    (out / "answer_cache.json").write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    (out / "poultrybot_knowledge.md").write_text(kb_markdown(router.kb), encoding="utf-8")
    system = (ROOT / "kb" / "system_prompt.txt").read_text(encoding="utf-8").strip()
    with (out / "finetune_chat.jsonl").open("w", encoding="utf-8") as f:
        for row in finetune_rows(router.kb, system):
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    manifest = dict(built=time.strftime("%Y-%m-%d %H:%M"), eps=eps, entries=len(router.kb["entries"]),
                    cached_questions=len(cache), fit_seconds=round(fit_s, 2), files=fingerprint())
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    return manifest


def load(eps=0.05, path=DIST):
    """Returns (router, cache) from the dump, or None if it is missing, stale, or built with another eps."""
    try:
        m = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
        if m["files"] != fingerprint() or abs(m["eps"] - eps) > 1e-12:
            return None
        with (path / "router.pkl").open("rb") as f:
            router = pickle.load(f)
        cache = json.loads((path / "answer_cache.json").read_text(encoding="utf-8"))
        return router, cache
    except (OSError, KeyError, ValueError, pickle.UnpicklingError):
        return None


if __name__ == "__main__":
    eps = float(sys.argv[1]) if len(sys.argv) > 1 else 0.05
    print(json.dumps(build(eps), indent=1))
