#!/usr/bin/env python3
"""graph_gate.py: semantic gate for a whiteboard-video graph. Uses no tokens.

Usage:
  python3 graph_gate.py <graph.json> <transcript-timed.jsonl> [--ocr ocr.jsonl] [--frames DIR] [--out DIR]

What it checks (rules from the 261124 three-model audit, TPM report section P):
  N  every node carries evidence: source in {ocr, speech, vision} and a frame id or a time.
     ocr    -> the label's words are found in the OCR text of the cited frames
     speech -> the label's words are found in the captions (near t when t is given)
     vision -> needs a vision_note (what was seen) and a cited frame; listed for a human check
     A label with '?' must be marked uncertain, and an uncertain node must say so in its label or note.
     kind is board | spoken | interpretation. A board node must be ocr or vision with a frame.
     A node with no evidence fails. The drawing is rendered from this graph only, and spoken nodes are drawn
     rounded. So a name he only says (Grok's 4th client, "ChatGPT") can't pass as a board mark. If a model
     falsely tags it board + vision with a note, it lands in human_check with the frame to look at.
  E  every edge joins two real nodes and cites at least one real step.
  S  steps are in time order, cite frames that exist, and cite caption text that exists in their window.
  Q  every quote is found word for word in the captions (on_screen quotes must be in OCR or carry a vision_note).
     For every quote it writes the caption excerpt and its start time beside it (quote-evidence-<id>.jsonl),
     so any reviewer can check the quote without re-downloading the video.
  O  onion layers name real nodes only.

Exit 0 = pass, 1 = at least one failure. The report goes to graph-gate-<id>.json.
Version 0.2, 2026-11-24: citing frames without delivering them now fails (CHaiMPION/cloud-runs-os, whiteboard-video-extract).
"""
import argparse, json, pathlib, re, sys

STOP = {"the", "a", "an", "and", "or", "of", "to", "on", "in", "for", "with", "your", "you", "is", "it"}


def norm(s):
    s = s.lower().replace("’", "'").replace("‘", "'")
    s = re.sub(r"\[[^\]]*\]", " ", s)
    s = re.sub(r"[^a-z0-9' ]+", " ", s)
    return " ".join(s.split())


def words(label):
    return [w for w in norm(label.replace("?", " ")).split() if w not in STOP and len(w) >= 2]


def load_jsonl(path):
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def frame_key(fid):
    m = re.search(r"(\d+)", str(fid))
    return int(m.group(1)) if m else None


def caption_index(segs):
    """Join captions into one normalised string, remembering which segment each word came from."""
    toks, owner = [], []
    for i, s in enumerate(segs):
        for w in norm(s["text"]).split():
            toks.append(w)
            owner.append(i)
    return toks, owner


def find_span(qtoks, toks):
    n = len(qtoks)
    for i in range(len(toks) - n + 1):
        if toks[i:i + n] == qtoks:
            return i, i + n - 1
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("graph"); ap.add_argument("transcript")
    ap.add_argument("--ocr"); ap.add_argument("--frames"); ap.add_argument("--out")
    ap.add_argument("--window", type=float, default=20.0, help="seconds either side of t for speech nodes")
    a = ap.parse_args()

    g = json.load(open(a.graph, encoding="utf-8"))
    vid = g.get("video_id", "video")
    segs = load_jsonl(a.transcript)
    toks, owner = caption_index(segs)
    alltext = " ".join(toks)
    ocr = {}
    if a.ocr:
        for r in load_jsonl(a.ocr):
            ocr[frame_key(r["frame"])] = norm(r.get("text", ""))
    frames = None
    if a.frames and pathlib.Path(a.frames).is_dir():
        frames = {frame_key(p.name) for p in pathlib.Path(a.frames).iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg")}

    fails, human, rows = [], [], {"nodes": [], "edges": [], "steps": [], "quotes": [], "onion": []}

    def fail(section, item, why):
        fails.append({"section": section, "id": item, "why": why})

    def frames_ok(section, item, fids):
        if frames is None:
            fail(section, item, f"cites frames {fids} but no --frames folder was given: deliver the frames, "
                                "or use only speech nodes (v0.2)")
            return False
        missing = [f for f in fids if frame_key(f) not in frames]
        if missing:
            fail(section, item, f"cites frames not in {a.frames}: {missing}")
        return not missing

    def text_near(t):
        if t is None:
            return alltext
        return norm(" ".join(s["text"] for s in segs if s["start"] <= t + a.window and s["end"] >= t - a.window))

    # N: nodes
    node_ids = set()
    for n in g.get("nodes", []):
        nid, label, src = n.get("id"), n.get("label", ""), n.get("source")
        fids, t = n.get("frame_ids", []), n.get("t")
        node_ids.add(nid)
        status = "pass"
        if src not in ("ocr", "speech", "vision"):
            fail("nodes", nid, f"source must be ocr, speech or vision, got {src!r} (no evidence = invented node)"); status = "fail"
        elif src in ("ocr", "vision") and not fids:
            fail("nodes", nid, f"source {src} needs at least one frame id"); status = "fail"
        elif src == "speech" and t is None and not fids:
            fail("nodes", nid, "source speech needs a time t or a frame id"); status = "fail"
        if status == "pass" and n.get("kind") == "board" and (src not in ("ocr", "vision") or not fids):
            fail("nodes", nid, "kind board = a mark on the board: needs source ocr or vision and a frame id. "
                               "A name he only says is kind spoken (drawn as a rounded box)"); status = "fail"
        if n.get("kind") not in ("board", "spoken", "interpretation"):
            fail("nodes", nid, f"kind must be board, spoken or interpretation, got {n.get('kind')!r}"); status = "fail"
        if fids:
            frames_ok("nodes", nid, fids)
        if "?" in label and not n.get("uncertain"):
            fail("nodes", nid, "label has '?' but uncertain is not true"); status = "fail"
        if n.get("uncertain") and "?" not in label and "uncertain" not in n.get("note", "").lower():
            fail("nodes", nid, "uncertain node must show it: '?' in the label or 'uncertain' in the note"); status = "fail"
        ws = words(label)
        if status == "pass" and src == "ocr":
            hay = " ".join(ocr.get(frame_key(f), "") for f in fids)
            if not a.ocr:
                fail("nodes", nid, "source ocr but no --ocr file given"); status = "fail"
            else:
                hit = [w for w in ws if w in hay]
                if len(hit) * 2 < max(1, len(ws)):
                    fail("nodes", nid, f"OCR of {fids} does not contain the label words {ws} (found {hit})"); status = "fail"
        if status == "pass" and src == "speech":
            hay = text_near(t)
            hit = [w for w in ws if w in hay.split()]
            if len(hit) * 2 < max(1, len(ws)):
                fail("nodes", nid, f"captions near t={t} do not contain the label words {ws} (found {hit})"); status = "fail"
        if status == "pass" and src == "vision":
            if not n.get("vision_note"):
                fail("nodes", nid, "source vision needs a vision_note saying what was seen and where"); status = "fail"
            else:
                status = "human-check"
                human.append({"node": nid, "label": label, "frames": fids, "vision_note": n["vision_note"]})
        rows["nodes"].append({"id": nid, "label": label, "source": src, "status": status})

    # S: steps
    step_ids, last = set(), -1.0
    for s in g.get("steps", []):
        sid = s.get("id"); step_ids.add(sid)
        st, en = s.get("start"), s.get("end")
        ok = True
        if st is None or en is None or st > en:
            fail("steps", sid, "start/end missing or start after end"); ok = False
        elif st < last:
            fail("steps", sid, "steps are not in time order"); ok = False
        else:
            last = st
            spoken = [x for x in segs if x["start"] < en and x["end"] > st]
            if not spoken:
                fail("steps", sid, f"no caption text between {st}s and {en}s"); ok = False
        if s.get("frame_ids"):
            ok = frames_ok("steps", sid, s["frame_ids"]) and ok
        rows["steps"].append({"id": sid, "status": "pass" if ok else "fail"})

    # E: edges
    for i, e in enumerate(g.get("edges", [])):
        eid = e.get("id") or f"E{i + 1:02d}"
        ok = True
        for end in ("from", "to"):
            if e.get(end) not in node_ids:
                fail("edges", eid, f"{end} node {e.get(end)!r} does not exist"); ok = False
        ev = e.get("evidence_steps", [])
        if not ev:
            fail("edges", eid, "edge cites no step"); ok = False
        elif step_ids and any(x not in step_ids for x in ev):
            fail("edges", eid, f"cites unknown steps {[x for x in ev if x not in step_ids]}"); ok = False
        rows["edges"].append({"id": eid, "status": "pass" if ok else "fail"})

    # Q: quotes, with the caption excerpt and offset written beside each one
    evidence = []
    for q in g.get("quotes", []):
        qid, text = q.get("id"), q.get("text", "")
        if q.get("on_screen"):
            hay = " ".join(ocr.values())
            if ocr and all(w in hay for w in words(text)):
                status = "pass"
            elif q.get("vision_note") and q.get("frame_ids"):
                status = "human-check"
                human.append({"quote": qid, "text": text, "frames": q["frame_ids"], "vision_note": q["vision_note"]})
            else:
                status = "fail"
                fail("quotes", qid, "on-screen quote not in OCR and has no vision_note + frame_ids")
            rows["quotes"].append({"id": qid, "status": status})
            continue
        span = find_span(norm(text).split(), toks)
        if not span:
            fail("quotes", qid, "not found word for word in the captions (invented or altered)")
            rows["quotes"].append({"id": qid, "status": "fail"}); continue
        s0, s1 = owner[span[0]], owner[span[1]]
        excerpt = " ".join(segs[k]["text"] for k in range(s0, s1 + 1))
        evidence.append({"id": qid, "quote": text, "start": segs[s0]["start"], "end": segs[s1]["end"],
                         "caption_excerpt": excerpt, "segments": [s0, s1]})
        rows["quotes"].append({"id": qid, "status": "pass", "start": segs[s0]["start"]})

    # O: onion
    for L in (g.get("onion") or {}).get("layers", []):
        bad = [x for x in L.get("nodes", []) if x not in node_ids]
        if bad:
            fail("onion", L.get("id"), f"names nodes that do not exist: {bad}")
        rows["onion"].append({"id": L.get("id"), "status": "fail" if bad else "pass"})

    out = pathlib.Path(a.out or pathlib.Path(a.graph).parent)
    out.mkdir(parents=True, exist_ok=True)
    with open(out / f"quote-evidence-{vid}.jsonl", "w", encoding="utf-8") as f:
        for r in evidence:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    report = {"video_id": vid, "pass": not fails, "failures": len(fails),
              "counts": {k: len(v) for k, v in rows.items()}, "fails": fails,
              "human_check": human, "rows": rows}
    (out / f"graph-gate-{vid}.json").write_text(json.dumps(report, indent=1, ensure_ascii=False))
    print(json.dumps({k: report[k] for k in ("video_id", "pass", "failures", "counts")} |
                     {"human_check": len(human), "fails": fails[:12]}, indent=1, ensure_ascii=False))
    sys.exit(0 if not fails else 1)


if __name__ == "__main__":
    main()
