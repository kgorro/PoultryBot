"""Run with:  python tests/test_dalan.py   (or python -m pytest tests)"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dalan import DALANRouter, Normalizer, kb_vocab  # noqa: E402
from dalan.normalize import lemmatize  # noqa: E402

KB = json.loads((ROOT / "kb" / "kb.json").read_text(encoding="utf-8"))
DEV = [json.loads(l) for l in (ROOT / "data" / "dev.jsonl").read_text(encoding="utf-8").splitlines()]


def test_affix_stripping():
    assert lemmatize("mangitlog") == "itlog"        # Cebuano prefix
    assert lemmatize("gitambalan") == "tambal"      # prefix + suffix
    assert lemmatize("bumili") == "bili"            # Tagalog infix
    assert lemmatize("nagsisimula") == "simula"     # Tagalog reduplication
    assert lemmatize("sip-on") == "sipon"           # hyphen joining
    assert lemmatize("broiler") is None             # English words are not damaged


def test_code_switched_morphology():
    n = Normalizer(kb_vocab(KB))
    nq = n("nganong nag-drop ang egg production")
    assert "drop" in nq.tokens and nq.csi > 0


def test_kb_safety_rules():
    """No entry may prescribe a drug dose; disease entries must point to a veterinarian or report."""
    for e in KB["entries"]:
        assert "mg/" not in e["answer"] and "ml per" not in e["answer"].lower(), e["id"]
    for eid in ("newcastle", "avian-flu", "gumboro", "medication", "sudden-death"):
        text = next(e for e in KB["entries"] if e["id"] == eid)["answer"].lower()
        assert "veterinar" in text or "report" in text, eid


def test_router_actions():
    r = DALANRouter(KB).fit(DEV)
    assert r.route("Nganong naay dugo ang iti sa akong manok?")["entry"]["id"] == "coccidiosis"
    assert r.route("How many days do duck eggs take to hatch?")["entry"]["id"] == "hatch-days"
    assert r.route("how to raise pigs")["action"] == "abstain"
    tau_skip, tau_abs = r.th.get("cs")
    assert tau_abs <= tau_skip


def test_markdown_packs():
    """Every research entry comes from a pack, cites it, has a scope gate, and keeps the safety rules."""
    sys.path.insert(0, str(ROOT / "kb"))
    from ingest_md import load_all
    packs, entries = load_all()
    assert len(packs) == 4 and len(entries) == 14
    kb_ids = {e["id"] for e in KB["entries"]}
    pack_cues = {c.strip() for p in packs for c in p["scope"].split(",")}
    for e in entries:
        assert e["id"] in kb_ids and "Source:" in e["answer"] and e["scope"], e["id"]
        assert not any(set(k.split()) & pack_cues for k in e["keywords"]), e["id"]
    for eid in ("res-serology-results", "res-parasite-deworming", "res-cebu-health-practices"):
        assert "veterinarian" in next(e for e in entries if e["id"] == eid)["answer"], eid


def test_scope_gate():
    """Research entries answer local-study questions but never take everyday questions."""
    r = DALANRouter(KB).fit(DEV)
    assert r.route("Pila ang presyo sa ipot sa manok kada sako sa Bantayan?")["ranked_ids"][0] == "res-manure-uses"
    assert r.route("gumboro antibody levels in bantayan layers")["ranked_ids"][0] == "res-serology-results"
    for q in ("Naay bitok ang manok, unsay tambal?", "Kanus-a bakunahan ang broiler?", "Paano gumawa ng kulungan ng manok?"):
        assert not r.route(q)["ranked_ids"][0].startswith("res-"), q


def test_dump_roundtrip(tmp=None):
    """A dump loads, reproduces the fitted router's decisions, and is rejected when the KB hash changes."""
    import tempfile
    from dalan import dump
    with tempfile.TemporaryDirectory() as d:
        out = Path(d)
        dump.build(out=out)
        router, cache = dump.load(path=out)
        fresh = dump.fitted_router()
        for q in ["Unsaon pagbuhi og pugo?", "how common are worms in bantayan layers", "how to raise pigs"]:
            a, b = router.route(q), fresh.route(q)
            assert (a["action"], a["ranked_ids"]) == (b["action"], b["ranked_ids"]) and abs(a["p"] - b["p"]) < 1e-12
        assert cache and all(v["entry_id"] for v in cache.values())
        m = json.loads((out / "manifest.json").read_text())
        m["files"]["kb/kb.json"] = "stale"
        (out / "manifest.json").write_text(json.dumps(m))
        assert dump.load(path=out) is None


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
