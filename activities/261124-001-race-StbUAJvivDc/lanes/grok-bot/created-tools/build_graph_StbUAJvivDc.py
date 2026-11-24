#!/usr/bin/env python3
"""build_graph_StbUAJvivDc.py - writes graph-StbUAJvivDc.json (video graph, skill format) from data held in code,
so the graph is re-buildable and diffable. Created by grok-bot 261124. Usage: python3 created-tools/build_graph_StbUAJvivDc.py <lane>
Frame ids are keyframe file numbers (frame-NNNN.jpg). yt_cloud_extract dedupes frames, so NNNN is roughly but
not exactly seconds (107 keyframes for a 118 s video); every step carries that caution."""
import json, pathlib, sys
lane = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
F = lambda *n: [f"frame-{i:04d}" for i in n]
C = "keyframes are deduped, so frame numbers approximate seconds; times come from captions"
steps = [
 {"id":"S01","start":0.0,"end":9.9,"title":"Hook: ask for a deck, get a deck","paraphrase":"Asking Claude for a noun gets that noun; Felix Rieseberg (Anthropic EM) would add a short seller.","frame_ids":F(1,2,5),"caution":C},
 {"id":"S02","start":10.0,"end":24.9,"title":"Range","paraphrase":"Range = drawing on several fields; multi-agent setups make extra fields cheap to bring in.","frame_ids":F(13,19),"caution":C},
 {"id":"S03","start":25.0,"end":50.9,"title":"Trick 1: nouns to verbs","paraphrase":"From The Art of Innovation (Kelley, Littman): restate the deliverable as verbs to reveal which fields help.","frame_ids":F(27,40),"caution":C},
 {"id":"S04","start":51.0,"end":77.9,"title":"Trick 2: assemble the crew","paraphrase":"Heist-movie crew under an absurd stake: analyst, journalist, editor; motion/audio designer; red team incl. short seller and forensic accountant.","frame_ids":F(53,60,67,70),"caution":C},
 {"id":"S05","start":78.0,"end":97.9,"title":"It takes creativity: Alex Albert, Blender, 3D homepage","paraphrase":"A colleague's Blender renders led Felix to a 3D homepage; range is where he sees the most magic.","frame_ids":F(72,75,84),"caution":C},
 {"id":"S06","start":98.0,"end":111.9,"title":"Do it: verbs, crew, no role-play","paraphrase":"Before the next big ask write the verbs, name the crew, and have Claude do the field's work rather than imitate its voice.","frame_ids":F(90,94),"caution":C},
 {"id":"S07","start":112.0,"end":118.0,"title":"Close: who joins first?","paraphrase":"Viewer question plus source card felixrieseberg.com, 13 Oct 2026.","frame_ids":F(105,107),"caution":C},
]
nodes = [
 {"id":"hook_card","label":"Nouns to verbs, then the crew","kind":"board","source":"ocr","frame_ids":F(1)},
 {"id":"deck_board","label":"Deck","kind":"board","source":"ocr","frame_ids":F(2)},
 {"id":"felix_card","label":"Felix Rieseberg","kind":"board","source":"ocr","frame_ids":F(5)},
 {"id":"range_board","label":"Range","kind":"board","source":"ocr","frame_ids":F(13)},
 {"id":"trick1_board","label":"his first trick","kind":"board","source":"ocr","frame_ids":F(27)},
 {"id":"crew_board","label":"Assemble the crew","kind":"board","source":"ocr","frame_ids":F(53)},
 {"id":"redteam_board","label":"Red team","kind":"board","source":"ocr","frame_ids":F(67)},
 {"id":"albert_board","label":"Alex Albert","kind":"board","source":"ocr","frame_ids":F(75)},
 {"id":"homepage_capture","label":"Homepage captured 2026","kind":"board","source":"vision","frame_ids":F(84),
  "vision_note":"frame-0084: header strip reads FELIXRIESEBERG.COM - HOMEPAGE - CAPTURED 2026-10-21 over a screenshot of a rendered 3D room"},
 {"id":"nextask_board","label":"before your next big ask","kind":"board","source":"ocr","frame_ids":F(90)},
 {"id":"source_card","label":"Source felixrieseberg.com 13 Oct 2026","kind":"board","source":"vision","frame_ids":F(105),
  "vision_note":"frame-0105 bottom line: SOURCE: FELIXRIESEBERG.COM - 13 OCT 2026 (OCR reads .CON on some frames)"},
 {"id":"felix","label":"Felix Rieseberg","kind":"spoken","source":"speech","t":4},
 {"id":"anthropic","label":"Anthropic","kind":"spoken","source":"speech","t":6},
 {"id":"range","label":"range","kind":"spoken","source":"speech","t":10},
 {"id":"multiagent","label":"multi-agent setups","kind":"spoken","source":"speech","t":17},
 {"id":"art_innovation","label":"The Art of Innovation","kind":"spoken","source":"speech","t":25},
 {"id":"kelley","label":"Tom Kelley","kind":"spoken","source":"speech","t":27},
 {"id":"littman","label":"Jonathan Littman","kind":"spoken","source":"speech","t":30},
 {"id":"verbs","label":"Replace the noun with verbs","kind":"spoken","source":"speech","t":31},
 {"id":"crew","label":"Assemble the crew","kind":"spoken","source":"speech","t":55},
 {"id":"heist","label":"heist movie","kind":"spoken","source":"speech","t":51},
 {"id":"production","label":"analyst, journalist, editor","kind":"spoken","source":"speech","t":63},
 {"id":"presenters","label":"motion and audio designer","kind":"spoken","source":"speech","t":68},
 {"id":"redteam","label":"red team","kind":"spoken","source":"speech","t":72},
 {"id":"short_seller","label":"short seller","kind":"spoken","source":"speech","t":72},
 {"id":"forensic","label":"forensic accountant","kind":"spoken","source":"speech","t":72},
 {"id":"alex_albert","label":"Alex Albert","kind":"spoken","source":"speech","t":80},
 {"id":"blender","label":"Blender","kind":"spoken","source":"speech","t":82},
 {"id":"homepage3d","label":"His homepage is a 3D room","kind":"spoken","source":"speech","t":91},
 {"id":"no_roleplay","label":"Role-play makes the transcript weirder","kind":"spoken","source":"speech","t":108},
]
edges = [
 ("felix","anthropic","works at (engineering manager)",["S01"],"spoken"),
 ("felix","range","names the ambition type",["S02"],"spoken"),
 ("multiagent","range","makes cheap to practise",["S02"],"spoken"),
 ("kelley","art_innovation","co-author of",["S03"],"spoken"),
 ("littman","art_innovation","co-author of",["S03"],"spoken"),
 ("art_innovation","verbs","source of trick 1",["S03"],"spoken"),
 ("verbs","range","reveals which fields to add",["S03"],"spoken"),
 ("heist","crew","analogy for trick 2",["S04"],"spoken"),
 ("crew","production","production-quality members",["S04"],"spoken"),
 ("crew","presenters","if presented",["S04"],"spoken"),
 ("crew","redteam","adversarial members",["S04"],"spoken"),
 ("redteam","short_seller","includes",["S04"],"spoken"),
 ("redteam","forensic","includes",["S04"],"spoken"),
 ("alex_albert","blender","used to render interior designs",["S05"],"spoken"),
 ("blender","homepage3d","inspired Claude for 3D environments",["S05"],"spoken"),
 ("no_roleplay","crew","guardrail on how to use the crew",["S06"],"spoken"),
 ("verbs","crew","step 1 then step 2",["S06"],"spoken"),
 ("range_board","range","on-screen title for",["S02"],"drawn"),
 ("crew_board","crew","on-screen title for",["S04"],"drawn"),
 ("albert_board","alex_albert","on-screen title for",["S05"],"drawn"),
 ("homepage_capture","homepage3d","screen evidence for",["S05"],"drawn"),
]
quotes = [
 {"id":"Q01","text":"Ask Claude for a deck, and you get a deck."},
 {"id":"Q02","text":"Replace the noun with verbs."},
 {"id":"Q03","text":"A quarterly review isn't a deck. It's getting busy people to believe a story about cause and effect and to decide under uncertainty in 30 minutes."},
 {"id":"Q04","text":"Then a red team to attack it, a short seller, and a forensic accountant."},
 {"id":"Q05","text":"And have Claude do what a short seller does to research a position, not write like one."},
 {"id":"Q06","text":"Role-play makes the transcript weirder, not the result better."},
 {"id":"Q07","text":"Now that multi-agent setups are easier to run, he's seen really interesting results asking Claude to bring in extra fields."},
 {"id":"Q08","text":"Nouns to verbs, then the crew","on_screen":True,"frame_ids":F(1),"vision_note":"frame-0001 title card under GIVE CLAUDE A CREW"},
]
g = {"video_id":"StbUAJvivDc","source_url":"https://www.youtube.com/watch?v=StbUAJvivDc","frames_dir":"frames-StbUAJvivDc",
 "steps":steps,"nodes":nodes,
 "edges":[{"from":a,"to":b,"relation":r,"evidence_steps":s,"status":st} for a,b,r,s,st in edges],
 "onion":{"status":"interpretation (grok-bot's), not the speaker's own layer model","layers":[
   {"id":"O1","title":"Core: change the ask","description":"verbs not nouns","nodes":["verbs"]},
   {"id":"O2","title":"Crew of fields","description":"who would make it amazing / attack it","nodes":["crew","production","presenters","redteam","short_seller","forensic"]},
   {"id":"O3","title":"Guardrail","description":"methods, not voices","nodes":["no_roleplay"]},
   {"id":"O4","title":"Enabler","description":"multi-agent setups make many fields affordable","nodes":["multiagent"]},
   {"id":"O5","title":"Frame: ambition as range","description":"one of Felix's four ambition types","nodes":["range","felix","anthropic"]}]},
 "quotes":quotes}
(lane/"graph-StbUAJvivDc.json").write_text(json.dumps(g, indent=1, ensure_ascii=False))
print(json.dumps({"steps":len(steps),"nodes":len(nodes),"edges":len(edges),"quotes":len(quotes)}))
