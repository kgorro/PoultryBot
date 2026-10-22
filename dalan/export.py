"""Exports a fitted DALAN router to JSON for the browser implementation (web/dalan.js).

    python -m dalan.export            # fits on data/dev.jsonl + data/test.jsonl, writes web/model.json

The browser demo then runs the same normalization, channels, calibrator, and thresholds as the Python router;
tests/test_parity.mjs checks that both give the same decisions.
"""
import json
import sys
from pathlib import Path

from . import normalize as N
from .lexicon import CONTRACTIONS, LEXICON, PREFIXES, SUFFIXES
from .router import DALANRouter

ROOT = Path(__file__).resolve().parents[1]


def export(router, path):
    lex, ch = router.lex, router.char
    model = dict(
        gamma=router.norm.gamma, k_ctx=router.k_ctx,
        stop=sorted(N.STOP), en_guard=sorted(N.EN_GUARD), en_vocab=sorted(router.norm.en_vocab),
        lexicon=LEXICON, contractions=CONTRACTIONS, prefixes=PREFIXES, suffixes=SUFFIXES,
        ids=router.ids,
        lex_docs=[dict(title=sorted(d["title"]), kw=sorted(d["kw"]), q=sorted(d["q"]), phrases=d["phrases"]) for d in lex.docs],
        lex_idf=lex.idf, lex_default_idf=lex.default_idf,
        char_idf=ch.idf, char_vecs=ch.vecs,
        cal=dict(mu=router.cal.mu.tolist(), sd=router.cal.sd.tolist(), w=router.cal.w.tolist(), b=float(router.cal.b)),
        thresholds={k: [float(a), float(b)] for k, (a, b) in router.th.t.items()},
    )
    Path(path).write_text(json.dumps(model, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def fitted_router(eps=0.05):
    kb = json.loads((ROOT / "kb" / "kb.json").read_text(encoding="utf-8"))
    rows = []
    for name in ("dev", "test"):
        rows += [json.loads(l) for l in (ROOT / "data" / f"{name}.jsonl").read_text(encoding="utf-8").splitlines()]
    return DALANRouter(kb, eps=eps).fit(rows)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "web" / "model.json")
    export(fitted_router(), out)
    print("wrote", out, Path(out).stat().st_size // 1024, "KB")
