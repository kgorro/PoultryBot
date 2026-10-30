"""Checks that the browser router (web/dalan.js + web/model.json) makes the same decisions as the Python router.

    python tests/test_parity.py      (needs Node.js)
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from dalan.export import export, fitted_router  # noqa: E402


def main():
    router = fitted_router()
    model_path = ROOT / "web" / "model.json"
    export(router, model_path)
    queries = []
    for name in ("dev", "test", "test_research"):
        queries += [json.loads(l)["q"] for l in (ROOT / "data" / f"{name}.jsonl").read_text(encoding="utf-8").splitlines()]
    queries += ["", "???", "Unsaon pag-atiman sa piso nga nag-ubo-ubo?", "BROILER feed!!!", "nag-drop ang eggs",
                "Pila ang presyo sa ipot sa Bantayan?", "bantayan", "study"]
    js = """
const fs=require('fs'); const D=require(process.argv[1]);
const M=JSON.parse(fs.readFileSync(process.argv[2],'utf8')); const kb=JSON.parse(fs.readFileSync(process.argv[3],'utf8'));
const r=D.create(M,kb); const qs=JSON.parse(fs.readFileSync(0,'utf8'));
console.log(JSON.stringify(qs.map(q=>{const o=r.route(q);return [o.action,o.p,o.ranked_ids];})));
"""
    out = subprocess.run(["node", "-e", js, str(ROOT / "web" / "dalan.js"), str(model_path), str(ROOT / "kb" / "kb.json")],
                         input=json.dumps(queries), capture_output=True, text=True, check=True).stdout
    js_res = json.loads(out)
    mism = 0
    for q, (a, p, ids) in zip(queries, js_res):
        r = router.route(q)
        if r["action"] != a or r["ranked_ids"] != ids or abs(r["p"] - p) > 1e-6:
            mism += 1
            print("MISMATCH", repr(q), r["action"], a, r["ranked_ids"], ids, r["p"], p)
    print(f"parity: {len(queries) - mism}/{len(queries)} identical")
    assert mism == 0


if __name__ == "__main__":
    main()
