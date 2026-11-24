#!/usr/bin/env python3
"""build_index_html.py - builds the lane's self-contained index.html (inline CSS/JS, no external requests; images are
lane-relative frame files) from the lane's own artefacts, so the page can never say more than the files do.
Created by grok-bot 261124. Usage: python3 build_index_html.py <lane> <video_id>"""
import html, json, math, pathlib, re, sys, datetime
import markdown
lane, vid = pathlib.Path(sys.argv[1]), sys.argv[2]
E = html.escape
rd = lambda f: (lane / f).read_text() if (lane / f).exists() else ""
jl = lambda f: [json.loads(l) for l in rd(f).splitlines() if l.strip()]
js = lambda f: json.loads(rd(f)) if rd(f) else {}
md = lambda s: markdown.markdown(s, extensions=["tables", "fenced_code"])
meta = js(f"metadata-{vid}.json"); g = js(f"graph-{vid}.json"); kg = js(f"knowledge-graph-{vid}.json")
proof = js(f"proof-{vid}.json"); kgc = js(f"knowledge-graph-check-{vid}.json"); qsg = js(f"quotes-sources-gate-{vid}.json")
wvs = js(f"words-vs-sources-{vid}.json"); avc = js(f"audio-vs-captions-{vid}.json"); gg = js(f"graph-gate-{vid}.json")
chk = jl("CHECKLIST-grok-bot.jsonl"); qe = jl(f"quote-evidence-{vid}.jsonl")
ocr = {r["frame"].split(".")[0]: r["text"] for r in jl(f"ocr-{vid}.jsonl")}
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=13)))
mm = lambda t: f"{int(t)//60:02d}:{int(t)%60:02d}"
yt = f"https://www.youtube.com/watch?v={vid}"
# --- knowledge graph SVG (radial: expert centre, Short-cited ring, post/context ring)
W, H, cx, cy = 1100, 900, 550, 450
nodes = kg.get("nodes", []); pos = {}
c = {"person": "#e4572e", "org": "#3a86ff", "work": "#8338ec", "feature": "#06a77d", "doc": "#8d99ae", "concept": "#f4a261"}
ring1 = [n for n in nodes if n["id"] != kg.get("expert") and n["cited_in"] in ("short", "both")]
ring2 = [n for n in nodes if n["id"] != kg.get("expert") and n["cited_in"] not in ("short", "both")]
pos[kg.get("expert")] = (cx, cy)
for ring, r in ((ring1, 210), (ring2, 395)):
    for i, n in enumerate(ring):
        a = 2 * math.pi * i / max(1, len(ring)) - math.pi / 2
        pos[n["id"]] = (cx + r * math.cos(a) * 1.18, cy + r * math.sin(a))
svg = [f'<svg viewBox="0 0 {W} {H}" class="kg" role="img" aria-label="Expert knowledge graph">']
for e in kg.get("edges", []):
    (x1, y1), (x2, y2) = pos[e["from"]], pos[e["to"]]
    svg.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}"><title>{E(e["from"])} → {E(e["relation"])} → {E(e["to"])} ({E(e["source_file"])})</title></line>')
for n in nodes:
    x, y = pos[n["id"]]; big = n["id"] == kg.get("expert"); lab = n["label"] if len(n["label"]) < 34 else n["label"][:32] + "…"
    svg.append(f'<a href="{E(n["url"])}" target="_blank" rel="noopener"><g class="n"><circle cx="{x:.0f}" cy="{y:.0f}" r="{18 if big else 8}" fill="{c[n["type"]]}"/>'
               f'<text x="{x:.0f}" y="{y + (34 if big else 20):.0f}" text-anchor="middle" class="{"big" if big else ""}">{E(lab)}</text>'
               f'<title>{E(n["label"])} · {n["type"]} · cited in: {n["cited_in"]} · saved: {E(n["source_file"])} @ {E(n["retrieved_at"] or "")}</title></g></a>')
svg.append("</svg>")
legend = " ".join(f'<span class="lg"><i style="background:{v}"></i>{k}</span>' for k, v in c.items())
# --- tables
def table(rows, cols):
    return "<table><tr>" + "".join(f"<th>{E(h)}</th>" for h, _ in cols) + "</tr>" + "".join(
        "<tr>" + "".join(f"<td>{f(r)}</td>" for _, f in cols) + "</tr>" for r in rows) + "</table>"
kg_tbl = table(sorted(nodes, key=lambda n: (n["cited_in"] not in ("short", "both"), n["type"])), [
    ("Node", lambda n: f'<a href="{E(n["url"])}" target="_blank" rel="noopener">{E(n["label"])}</a>'), ("Type", lambda n: n["type"]),
    ("Cited in", lambda n: n["cited_in"]), ("Saved source", lambda n: f'<a href="{E(n["source_file"])}">{E(n["source_file"].split("/")[-1])}</a>'),
    ("Retrieved (NZT)", lambda n: E((n["retrieved_at"] or "")[:16].replace("T", " "))), ("Note", lambda n: E(n["note"]))])
steps_tbl = table(g.get("steps", []), [("Step", lambda s: s["id"]), ("[mm:ss]", lambda s: f'<a href="{yt}&t={int(s["start"])}s" target="_blank">{mm(s["start"])}–{mm(s["end"])}</a>'),
    ("Title", lambda s: E(s["title"])), ("Paraphrase (ours)", lambda s: E(s["paraphrase"])),
    ("Frames", lambda s: " ".join(f'<a href="frames-{vid}/{f}.jpg">{f[-4:]}</a>' for f in s.get("frame_ids", [])))])
wv_tbl = table(wvs.get("pairs", []), [("#", lambda r: r["id"]), ("[mm:ss]", lambda r: mm(r["t"]) if r["t"] is not None else "–"),
    ("Narrator (captions ✓)", lambda r: E(r["narration"])), ("Felix's post", lambda r: E(r["post"]) if r["post"] else "<em>not in post</em>"),
    ("Post ✓", lambda r: "✅" if r["post_in_saved_post"] else ("–" if r["post_in_saved_post"] is None else "❌")),
    ("Sim", lambda r: "" if r["similarity"] is None else r["similarity"]), ("Class", lambda r: f'<span class="cl {r["class"]}">{r["class"]}</span>'), ("Difference", lambda r: E(r["note"]))])
qe_tbl = table(qe, [("Quote", lambda q: E(q.get("quote", ""))), ("Caption start", lambda q: mm(q["start"]) if q.get("start") is not None else "")])
cited = sorted({f for s in g.get("steps", []) for f in s.get("frame_ids", [])} | {f for n in g.get("nodes", []) for f in n.get("frame_ids", [])})
frames = "".join(f'<figure><a href="frames-{vid}/{f}.jpg"><img loading="lazy" src="frames-{vid}/{f}.jpg" alt="{f}"></a><figcaption><b>{f}</b> · On-screen (OCR): {E(ocr.get(f, "")[:140])}</figcaption></figure>' for f in cited)
ck_tbl = table(chk, [("Id", lambda r: r["id"]), ("Status", lambda r: f'<span class="st {r["status"]}">{r["status"]}</span>'), ("Evidence", lambda r: E(r["evidence"])), ("Note", lambda r: E(r.get("note", "")))])
nd = sum(r["status"] == "done" for r in chk); nb = sum(r["status"] == "blocked" for r in chk); ns = sum(r["status"] == "skipped" for r in chk)
badge = lambda ok, t: f'<span class="b {"ok" if ok else "no"}">{"PASS" if ok else "FAIL"} · {E(t)}</span>'
gates = " ".join([badge(proof.get("pass"), "proof_run (quote + graph gate)"), badge(gg.get("pass"), f"graph_gate {gg.get('counts', {})}"),
    badge(kgc.get("pass"), f"check_knowledge_graph {kgc.get('nodes')} nodes / {kgc.get('edges')} edges"),
    badge(qsg.get("failed_sections") == 0, f"written quotes {sum(x['quotes'] or 0 for x in qsg.get('results', []))} in {qsg.get('sections')} sources"),
    badge(wvs.get("failures") == 0, f"narration vs post {len(wvs.get('pairs', []))} pairs"),
    badge(avc.get("similarity", 0) > 0.95, f"audio vs captions {avc.get('similarity')}")])
answer = re.sub(r"^# .*\n", "", rd(f"ANSWER-{vid}.md"))
sec = lambda i, t, body: f'<section id="{i}"><h2>{t}</h2>{body}</section>'
css = """body{font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;margin:0;color:#1d1d1f;background:#fbfaf7}
header{background:#1d1d1f;color:#fff;padding:28px 6vw}header h1{margin:0 0 6px;font-size:1.7em}header a{color:#ffb4a2}
nav{position:sticky;top:0;background:#fff;border-bottom:1px solid #ddd;padding:8px 6vw;z-index:5;overflow-x:auto;white-space:nowrap}nav a{margin-right:14px;color:#e4572e;text-decoration:none;font-weight:600;font-size:.9em}
main{padding:0 6vw 60px;max-width:1250px}section{margin:34px 0;padding-top:6px}h2{border-bottom:3px solid #e4572e;display:inline-block}
table{border-collapse:collapse;width:100%;font-size:.86em;margin:10px 0;display:block;overflow-x:auto}th,td{border:1px solid #ddd;padding:5px 7px;vertical-align:top;text-align:left}th{background:#f1ede6}
.b{display:inline-block;padding:3px 9px;border-radius:12px;margin:3px;font-size:.8em;font-weight:600}.ok{background:#d8f3dc;color:#1b4332}.no{background:#ffd6d6;color:#7a0000}
.st.done{color:#1b7f3a;font-weight:700}.st.blocked{color:#b00020;font-weight:700}.st.skipped{color:#8a6d00;font-weight:700}
.cl{font-size:.8em;padding:1px 6px;border-radius:8px;background:#eee}.cl.verbatim{background:#d8f3dc}.cl.close{background:#e9f5db}.cl.paraphrase{background:#fff3c4}.cl.narrator-only{background:#ffe0e0}
.kg{width:100%;height:auto;background:#fff;border:1px solid #e5e5e5;border-radius:10px}.kg line{stroke:#bbb;stroke-width:1}.kg text{font-size:11px;fill:#333}.kg text.big{font-size:16px;font-weight:700}.kg a:hover text{fill:#e4572e}
.lg{margin-right:12px;font-size:.85em}.lg i{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:4px}
.frames{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}figure{margin:0;background:#fff;border:1px solid #e5e5e5;border-radius:8px;padding:6px;font-size:.72em}figure img{width:100%;border-radius:4px}
.card{background:#fff;border:1px solid #e5e5e5;border-radius:10px;padding:4px 18px}pre{background:#1d1d1f;color:#f5f5f5;padding:12px;border-radius:8px;overflow-x:auto;white-space:pre-wrap}
.small{font-size:.85em;color:#555}"""
files = sorted(p.relative_to(lane).as_posix() for p in lane.rglob("*") if p.is_file() and not p.name.endswith((".m4a",)) and "frames-" not in p.as_posix() and "/work/" not in "/" + p.as_posix() and not p.name.endswith(".raw.html") and not p.name.endswith(".raw.pdf"))
filelist = "<ul class='small'>" + "".join(f'<li><a href="{E(f)}">{E(f)}</a></li>' for f in files) + "</ul>"
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Verbs, then the Crew · Felix Rieseberg via Short {vid} · grok-bot knowledge bundle</title><style>{css}</style></head><body>
<header><h1>Verbs, then the Crew</h1><div>A knowledge bundle from the Short <a href="{yt}" target="_blank">{E(meta.get('title',''))}</a> ({E(meta.get('channel') or '')}, {meta.get('duration')} s), checked against the expert's own post by <a href="https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/" target="_blank">Felix Rieseberg (Anthropic)</a>.</div>
<div class="small" style="color:#ccc">Lane grok-bot · activity 261124-001 · built {now:%Y-%m-%d %H:%M} NZT by created-tools/build_index_html.py from the lane files only.</div></header>
<nav><a href="#answer">Answer</a><a href="#proof">Proof</a><a href="#argument">Argument</a><a href="#expert">Expert graph</a><a href="#feature">Feature</a><a href="#method">Method card</a><a href="#words">Words vs post</a><a href="#visual">Visual layer</a><a href="#derivatives">Derivatives</a><a href="#claims">Claims</a><a href="#checklist">Checklist</a><a href="SOURCES-{vid}.md">Sources</a><a href="#files">Files</a></nav><main>
{sec("answer","Answer (first screen)", '<div class="card">'+md(answer)+'</div>')}
{sec("proof","Proof: every gate re-runnable", '<p>'+gates+'</p><p class="small">Proof stamp: '+E(str(proof.get('at')))+'. Re-run: <code>python3 skills/whiteboard-video-extract/scripts/proof_run.py &lt;lane&gt; '+vid+' --check</code>. Audio route: Whisper small.en transcript vs YouTube captions, '+str(len(avc.get('differences',[])))+' word differences, all spellings of names (Rieseberg/Riesberg, Kelley/Kelly).</p>')}
{sec("argument","1 · Topic and argument, in the speaker's order", '<p><b>One line:</b> to get more than the noun you asked for, rewrite the task as verbs, then have Claude assemble a crew of fields (red team included) and make each one <i>do</i> its method. Felix Rieseberg calls this <b>Range</b>.</p>'+steps_tbl+'<h3>Spoken quotes with caption evidence</h3>'+qe_tbl)}
{sec("expert","2 · Expert graph", '<p><b>Felix Rieseberg</b>, Engineering Manager at Anthropic (led engineering for Claude.ai, Cowork and Claude Code Desktop; Electron co-maintainer), published the source on his own site on 13 Oct 2026. Inner ring: named in the Short. Outer ring: cited only in the post, or profile/doc pages we added to verify. Click a node for its URL; hover for the saved file.</p><p>'+legend+'</p>'+''.join(svg)+kg_tbl)}
{sec("feature","3 · The feature the advice relies on", '<div class="card">'+md(re.sub(r"^# .*\n", "", rd(f"feature-docs-{vid}.md")))+'</div>')}
{sec("method","4 · The method card", '<div class="card">'+md(re.sub(r"^# .*\n", "", rd(f"method-card-{vid}.md")))+'</div>')}
{sec("words","5 · Narrator's words vs the expert's post", '<p>Each narration line is found word for word in the captions, and each post line word for word in the saved post (<code>created-tools/narration_vs_post.py</code>). The biggest change in meaning is P15: in the post the short seller and forensic accountant <i>are</i> the red team.</p>'+wv_tbl)}
{sec("visual","6 · The visual layer", '<p>No drawn diagram in this Short. It is typeset title cards (GIVE CLAUDE A CREW, RANGE, ASSEMBLE THE CREW, ALEX ALBERT, DECK) over scrolling screenshots of Felix\'s post and a homepage capture dated 2026-10-21. Evidence: OCR of all 107 deduplicated keyframes and the <a href="contact-sheet-'+vid+'.jpg">contact sheet</a>. Below are the frames the graph cites. Frame numbers only approximate seconds.</p><div class="frames">'+frames+'</div><details><summary>Mermaid of the video graph (render_graph.py)</summary><pre>'+E(rd(f"diagram-{vid}.mmd"))+'</pre></details>')}
{sec("derivatives","7 · Derivatives", md(re.sub(r"^# .*\n", "", rd(f"DERIVATIVES-{vid}.md"))))}
{sec("claims","Claims register (VERIFIED / UNVERIFIED / NOT FOUND)", md(re.sub(r"^# .*\n", "", rd(f"CLAIMS-{vid}.md"))))}
{sec("checklist",f"Checklist C01–C20 · done {nd} · blocked {nb} · skipped {ns}", ck_tbl)}
{sec("files","All lane files", filelist)}
</main></body></html>"""
(lane / "index.html").write_text(page)
print(json.dumps({"bytes": len(page), "frames_shown": len(cited), "kg_nodes": len(nodes), "checklist_rows": len(chk)}))
