#!/usr/bin/env python3
"""check_knowledge_graph.py - required by the spec. Checks knowledge-graph-<id>.json:
  every node has id, label, allowed type, url, source_file, retrieved_at; every source_file exists in the lane,
  its '# url:' header equals the node url, and its '# http_status:' is 200; every edge joins real nodes and has a
  saved source_file; no duplicate ids. Lists saved sources no node cites (info only).
Writes knowledge-graph-check-<id>.json. Exit 0 pass / 1 fail. Created by grok-bot 261124.
Usage: python3 check_knowledge_graph.py <lane>/knowledge-graph-<id>.json"""
import json, pathlib, re, sys
p = pathlib.Path(sys.argv[1]); lane = p.parent; g = json.loads(p.read_text())
TYPES = {"person", "org", "work", "feature", "doc", "concept"}; fails = []; ids = set()
for n in g["nodes"]:
    nid = n.get("id")
    if nid in ids: fails.append(f"node {nid}: duplicate id")
    ids.add(nid)
    for k in ("id", "label", "type", "url", "source_file", "retrieved_at"):
        if not n.get(k): fails.append(f"node {nid}: missing {k}")
    if n.get("type") not in TYPES: fails.append(f"node {nid}: bad type {n.get('type')}")
    sf = lane / (n.get("source_file") or "-")
    if not sf.is_file(): fails.append(f"node {nid}: source_file not saved: {n.get('source_file')}"); continue
    t = sf.read_text(errors="replace")
    hu = (re.search(r"^# url: (.+)$", t, re.M) or [None, ""])[1].strip()
    if hu != n.get("url"): fails.append(f"node {nid}: url {n.get('url')} != saved header {hu}")
    if not re.search(r"^# http_status: 200$", t, re.M): fails.append(f"node {nid}: saved source is not HTTP 200")
for e in g["edges"]:
    for end in ("from", "to"):
        if e.get(end) not in ids: fails.append(f"edge {e.get('from')}->{e.get('to')}: unknown {end}")
    if not (lane / (e.get("source_file") or "-")).is_file(): fails.append(f"edge {e.get('from')}->{e.get('to')}: source_file not saved")
cited = {n["source_file"] for n in g["nodes"]} | {e["source_file"] for e in g["edges"]}
saved = {f"sources/{x.name}" for x in (lane / "sources").glob("*.txt")}
rep = {"pass": not fails, "nodes": len(g["nodes"]), "edges": len(g["edges"]), "sources_saved": len(saved),
       "sources_cited_by_graph": len(cited), "saved_not_in_graph": sorted(saved - cited), "fails": fails}
(lane / f"knowledge-graph-check-{g.get('video_id','x')}.json").write_text(json.dumps(rep, indent=1))
print(json.dumps(rep, indent=1)); sys.exit(0 if not fails else 1)
