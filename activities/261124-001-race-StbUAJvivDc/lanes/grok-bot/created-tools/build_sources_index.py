#!/usr/bin/env python3
"""build_sources_index.py - writes SOURCES-<id>.md: one row per saved source (name, url, HTTP status, fetched_at NZT,
raw sha256, which graph nodes cite it). Created by grok-bot 261124. Usage: python3 build_sources_index.py <lane> <id>"""
import json, pathlib, re, sys
lane, vid = pathlib.Path(sys.argv[1]), sys.argv[2]
kg = json.loads((lane / f"knowledge-graph-{vid}.json").read_text())
use = {}
for n in kg["nodes"]: use.setdefault(n["source_file"], []).append(n["id"])
rows = []
for f in sorted((lane / "sources").glob("*.txt")):
    t = f.read_text(errors="replace"); g = lambda k: (re.search(rf"^# {k}: (.*)$", t, re.M) or [None, ""])[1].strip()
    rows.append(f"| `{f.name}` | {g('url')} | {g('http_status')} | {g('fetched_at')} | `{g('raw_sha256')[:16]}` | {', '.join(use.get('sources/' + f.name, [])) or '— (saved, not a graph node: failed fetch or spare)'} |")
md = [f"# SOURCES · {vid}", "", "Every page cited, saved by `created-tools/save_source.py` (raw file beside each .txt). Status 200 = usable evidence; any other status is a logged block, never cited as evidence.", "",
      "| File | URL | HTTP | Fetched (NZT) | raw sha256 (16) | Graph nodes citing it |", "|---|---|---|---|---|---|"] + rows
(lane / f"SOURCES-{vid}.md").write_text("\n".join(md) + "\n"); print(json.dumps({"sources": len(rows)}))
