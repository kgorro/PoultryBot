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


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
