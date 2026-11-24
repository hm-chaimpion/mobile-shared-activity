#!/usr/bin/env python3
"""render_graph.py: draw the diagram and the onion from graph.json only. Uses no tokens.

Usage: python3 render_graph.py <graph.json> [--out DIR]
Writes: diagram-<id>.mmd (Mermaid flowchart; GitHub renders it) and onion-<id>.md (core-to-outer table).

The drawing can only show what the gated graph holds. That is the fix for Grok's redraw, which was drawn by
separate code and grew a 4th client box the board does not show. Uncertain labels keep their '?'.
Node style by source: board (ocr/vision) = solid box, spoken only = rounded box, edge status 'reconstructed' = dotted.
Version 0.1, 2026-11-24 (CHaiMPION/cloud-runs-os, whiteboard-video-extract).
"""
import argparse, json, pathlib, re


def safe(s):
    return re.sub(r'["\[\]{}()<>|]', " ", s).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("graph"); ap.add_argument("--out")
    a = ap.parse_args()
    g = json.load(open(a.graph, encoding="utf-8"))
    vid = g.get("video_id", "video")
    out = pathlib.Path(a.out or pathlib.Path(a.graph).parent)
    out.mkdir(parents=True, exist_ok=True)

    lines = ["flowchart LR"]
    for n in g.get("nodes", []):
        lab = safe(n["label"])
        lines.append(f'  {n["id"]}("{lab}")' if n.get("source") == "speech" else f'  {n["id"]}["{lab}"]')
    for e in g.get("edges", []):
        rel = safe(e.get("relation", ""))
        arrow = "-.->" if e.get("status") == "reconstructed" else "-->"
        lines.append(f'  {e["from"]} {arrow}|{rel}| {e["to"]}' if rel else f'  {e["from"]} {arrow} {e["to"]}')
    unc = [n["id"] for n in g.get("nodes", []) if n.get("uncertain")]
    if unc:
        lines.append("  classDef unsure stroke-dasharray: 4 3")
        lines.append(f"  class {','.join(unc)} unsure")
    (out / f"diagram-{vid}.mmd").write_text("\n".join(lines) + "\n", encoding="utf-8")

    onion = g.get("onion") or {}
    labels = {n["id"]: n["label"] for n in g.get("nodes", [])}
    rows = [f"# Onion: {vid}", "", f"Status: {onion.get('status', 'not stated')}. Order: core to outer.", "",
            "| # | Layer | What it is | Nodes |", "|---|---|---|---|"]
    for i, L in enumerate(onion.get("layers", []), 1):
        rows.append(f"| {i} | {L.get('title', '')} | {L.get('description', '')} | "
                    f"{', '.join(labels.get(x, x) for x in L.get('nodes', []))} |")
    (out / f"onion-{vid}.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(json.dumps({"diagram": str(out / f"diagram-{vid}.mmd"), "onion": str(out / f"onion-{vid}.md"),
                      "nodes": len(labels), "edges": len(g.get("edges", [])), "uncertain": unc}))


if __name__ == "__main__":
    main()
