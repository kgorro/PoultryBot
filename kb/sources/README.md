# Knowledge packs

Each .md file here adds verified entries to the PoultryBot knowledge base. `python kb/build_kb.py` reads every pack
(except this README), turns each `##` section into a KB entry, and appends the source citation to its answer.
Nothing here is used to fine-tune a model: the bot retrieves these entries at answer time, so editing a pack and
rebuilding is enough to update what the bot knows.

## Format

```
---
source: short-id
citation: Authors. Year. Title. Journal. DOI or status.
status: published | accepted | in press
group: research
---

## entry-id | Entry title
Keywords: word, word, two words
Questions:
- An English question
- A Cebuano question
- A Tagalog question

Answer text. Plain sentences and "- " bullet lines.
```

Rules for answers: no drug or vaccine doses; keep the study's own limits (sample, years, area); end disease topics
with a veterinarian referral. Each entry id must be unique across the whole KB.
