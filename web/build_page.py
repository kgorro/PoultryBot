"""Assembles web/poultrybot.html, a self-contained page (router, model, and knowledge base inline).

    python -m dalan.export && python web/build_page.py
"""
from pathlib import Path

WEB = Path(__file__).parent
ROOT = WEB.parent
page = (WEB / "page.html").read_text(encoding="utf-8")
page = (page.replace("/*__DALAN__*/", (WEB / "dalan.js").read_text(encoding="utf-8"))
            .replace("/*__KB__*/null", (ROOT / "kb" / "kb.json").read_text(encoding="utf-8"))
            .replace("/*__MODEL__*/null", (WEB / "model.json").read_text(encoding="utf-8")))
(WEB / "poultrybot.html").write_text(page, encoding="utf-8")
print("wrote web/poultrybot.html", len(page) // 1024, "KB")
