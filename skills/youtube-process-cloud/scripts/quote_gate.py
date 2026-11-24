#!/usr/bin/env python3
"""quote_gate.py — semantic gate: every quote in an answer file must appear in the transcript. 0 tokens.

Usage: python3 quote_gate.py <answer.md> <transcript-plain-or-timed-file> [--min-words 4]

Quotes = text inside "double quotes" / “curly quotes”, and markdown blockquote lines (> ...).
Words in [square brackets] are treated as declared editorial fills (e.g. [Skill]) and must be marked, not hidden:
they are dropped before matching and listed in the report.
Exit 0 = all quotes found; 1 = at least one quote not in the transcript (an invented or altered quote).
From the 261124 audits: neither Grok nor ChatGPT had a check that quotes match the source.
"""
import json, re, sys

def norm(s):
    s = s.lower().replace("’", "'").replace("‘", "'")
    s = re.sub(r"\[[^\]]*\]", " ", s)              # editorial fills
    s = re.sub(r"\[\d\d:\d\d\]", " ", s)            # timestamps
    s = re.sub(r"[^a-z0-9' ]+", " ", s)
    return " ".join(s.split())

def transcript_text(path):
    raw = open(path, encoding="utf-8").read()
    if path.endswith(".jsonl"):
        raw = " ".join(json.loads(l)["text"] for l in raw.splitlines() if l.strip())
    return norm(raw)

def quotes(md, min_words):
    qs = re.findall(r"[\"“]([^\"”\n]{8,})[\"”]", md) + re.findall(r"^>\s*(.+)$", md, re.M)
    return [q.strip() for q in qs if len(norm(q).split()) >= min_words]

def main():
    if len(sys.argv) < 3: sys.exit(__doc__)
    mw = int(sys.argv[sys.argv.index("--min-words") + 1]) if "--min-words" in sys.argv else 4
    md = open(sys.argv[1], encoding="utf-8").read()
    tx = transcript_text(sys.argv[2])
    rows, bad = [], 0
    for q in quotes(md, mw):
        ok = norm(q) in tx
        bad += not ok
        rows.append({"found": ok, "fills": re.findall(r"\[([^\]]+)\]", q), "quote": q[:160]})
    print(json.dumps({"quotes": len(rows), "not_found": bad, "rows": rows}, indent=1, ensure_ascii=False))
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
