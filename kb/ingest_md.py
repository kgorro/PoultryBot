"""Reads markdown knowledge packs (kb/sources/*.md) into knowledge base entries.

Each `## entry-id | Title` section becomes one entry with the pack's group, keywords, sample questions, and
answer text; the pack's citation is appended to every answer so the bot always says where a figure came from.
A pack's `scope:` cue words (plus an entry's optional `Cues:` line) gate its entries: the router only ranks
them when the question contains one of the cues (a place, "study", "survey"...). Without a gate, a local
survey entry that mentions bakuna or bitok would outrank the general how-to entry for an everyday question.
See kb/sources/README.md for the format.
"""
import re
from pathlib import Path

SOURCES = Path(__file__).parent / "sources"


def _front(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise ValueError("missing front matter")
    meta = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    return meta, text[m.end():]


def parse_pack(path):
    meta, body = _front(Path(path).read_text(encoding="utf-8"))
    for key in ("source", "citation", "group"):
        if not meta.get(key):
            raise ValueError(f"{path}: front matter needs '{key}'")
    scope = [c.strip() for c in meta.get("scope", "").split(",") if c.strip()]
    entries = []
    for sec in re.split(r"^## ", body, flags=re.M)[1:]:
        head, _, rest = sec.partition("\n")
        eid, _, title = (s.strip() for s in head.partition("|"))
        kw_m = re.search(r"^Keywords:\s*(.+)$", rest, re.M)
        q_m = re.search(r"^Questions:\s*\n((?:- .+\n?)+)", rest, re.M)
        if not (eid and title and kw_m and q_m):
            raise ValueError(f"{path}: section '{head}' needs id | title, Keywords:, Questions:")
        answer = rest[q_m.end():].strip()
        cue_m = re.search(r"^Cues:\s*(.+)$", answer, re.M)
        extra = []
        if cue_m:
            extra = [c.strip() for c in cue_m.group(1).split(",") if c.strip()]
            answer = (answer[:cue_m.start()] + answer[cue_m.end():]).strip()
        if not answer:
            raise ValueError(f"{path}: section '{eid}' has no answer text")
        cues = {c.lower() for c in scope}
        status = meta.get("status", "")
        note = f" ({status})" if status and status != "published" else ""
        entries.append(dict(
            id=eid, group=meta["group"], category="Local research", title=title,
            # Cue words open the gate; they must not also rank siblings, so keywords containing one are dropped
            keywords=[k for k in (k.strip().lower() for k in kw_m.group(1).split(",")) if k and not (set(k.split()) & cues)],
            questions=[q[2:].strip() for q in q_m.group(1).strip().splitlines()],
            answer=f"{answer}\n\nSource: {meta['citation']}{note}",
            source=meta["source"],
            scope=sorted({c.lower() for c in scope + extra})))
    return meta, entries


def load_all(src=SOURCES):
    packs, entries = [], []
    for p in sorted(Path(src).glob("*.md")):
        if p.name.lower() == "readme.md":
            continue
        meta, es = parse_pack(p)
        packs.append(dict(file=p.name, **meta, entries=[e["id"] for e in es]))
        entries += es
    return packs, entries
