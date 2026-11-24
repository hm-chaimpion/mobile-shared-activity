#!/usr/bin/env python3
"""quotes_sources_gate.py - runs the shared skill quote_gate.py once per source section of quotes-sources-<id>.md.
Sections start with '## SRC: <source_file> | <url>'. Also checks the url equals the '# url:' header in the saved file.
Writes quotes-sources-gate-<id>.json. Exit 1 if any quote is not found or a url mismatches. Created by grok-bot 261124.
Usage: python3 quotes_sources_gate.py <lane> <video_id> <path-to-quote_gate.py>"""
import json, pathlib, re, subprocess, sys, tempfile
lane, vid, qg = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
md = (lane / f"quotes-sources-{vid}.md").read_text()
secs = re.split(r"^## SRC: ", md, flags=re.M)[1:]
out, bad = [], 0
for s in secs:
    head, body = s.split("\n", 1); src, url = [x.strip() for x in head.split("|", 1)]
    saved = (lane / src).read_text(); hu = re.search(r"^# url: (.+)$", saved, re.M)
    url_ok = bool(hu) and hu.group(1).strip() == url
    tf = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False); tf.write("\n".join(l for l in body.splitlines() if l.startswith("> "))); tf.close()
    p = subprocess.run([sys.executable, qg, tf.name, str(lane / src), "--min-words", "1"], capture_output=True, text=True)
    r = json.loads(p.stdout) if p.stdout.strip().startswith("{") else {"error": p.stderr[-300:]}
    ok = p.returncode == 0 and url_ok; bad += not ok
    out.append({"source_file": src, "url": url, "url_matches_saved_header": url_ok, "quote_gate_exit": p.returncode,
                "quotes": r.get("quotes"), "not_found": r.get("not_found"), "rows": r.get("rows")})
rep = {"video_id": vid, "sections": len(out), "failed_sections": bad, "quote_gate": qg, "results": out}
(lane / f"quotes-sources-gate-{vid}.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False))
print(json.dumps({k: rep[k] for k in ("sections", "failed_sections")} | {"quotes": sum(x["quotes"] or 0 for x in out)}))
sys.exit(1 if bad else 0)
