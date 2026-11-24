#!/usr/bin/env python3
"""narration_vs_post.py - C11 checker. For each (narration, post) pair: prove the narration is word for word in the
timed captions (and report its caption time), prove the post text is word for word in the saved post, then diff
the two word by word and classify: verbatim | close (>=0.75) | paraphrase | narrator-only (no post text).
Writes words-vs-sources-<id>.md (human) and words-vs-sources-<id>.json (machine). Exit 1 if any cited span is
missing from its own source. Created by grok-bot 261124.
Usage: python3 narration_vs_post.py <lane> <video_id>"""
import difflib, json, pathlib, re, sys
lane, vid = pathlib.Path(sys.argv[1]), sys.argv[2]
POST = lane / "sources/src-felix-post.txt"; POST_URL = "https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/"
def norm(s):
    s = s.lower().replace("’", "'").replace("‘", "'").replace("-", " ")
    return " ".join(re.sub(r"[^a-z0-9' ]+", " ", s).split())
segs = [json.loads(l) for l in open(lane / f"transcript-timed-{vid}.jsonl") if l.strip()]
words, owner = [], []
for i, s in enumerate(segs):
    for w in norm(s["text"]).split(): words.append(w); owner.append(i)
def cap_time(q):
    qt = norm(q).split()
    for i in range(len(words) - len(qt) + 1):
        if words[i:i + len(qt)] == qt: return segs[owner[i]]["start"]
    return None
post = norm(POST.read_text().split("\n\n", 1)[1])
PAIRS = [
 ("P01","Ask Claude for a deck, and you get a deck.",None,"Narrator's hook. The post's nearest line is in the Altitude section (not quoted here): Claude will happily make you some slides."),
 ("P02","Felix Rieseberg, an engineering manager at Anthropic","I'm an EM at Anthropic","EM expanded to engineering manager: faithful."),
 ("P03","would send a short seller after it",None,"Narrator's framing; the post brings in a short seller as part of a red team."),
 ("P04","On his blog, he calls this range drawing on several fields, not just the one the task seems to need.","Drawing on multiple fields rather than just the one the task might need at the surface, using knowledge, tools, and techniques you normally wouldn't.","multiple to several; might need at the surface to seems to need; tail about knowledge, tools and techniques dropped."),
 ("P05","Now that multi-agent setups are easier to run, he's seen really interesting results asking Claude to bring in extra fields.","As AI products make it easier and easier to run multi-agent systems (with multiple threads, orchestrators, or simply subagents), I've seen really interesting results by imploring Claude to bring in additional fields.","Drops the feature detail (threads, orchestrators, subagents) and softens imploring to asking."),
 ("P06","His first trick is an old one from The Art of Innovation by Tom Kelley and Jonathan Littman.","An old trick from The Art of Innovation by Tom Kelley and Jonathan Littman.","Faithful attribution."),
 ("P07","Replace the noun with verbs.","Try to replace the nouns with verbs:","Drops Try to; nouns becomes noun."),
 ("P08","A quarterly review isn't a deck. It's getting busy people to believe a story about cause and effect and to decide under uncertainty in 30 minutes.","A quarterly review isn't \"a deck\". It's \"getting busy people to believe a story about cause and effect, and to decide under uncertainty, in 30 minutes\".","Word for word apart from punctuation and quote marks."),
 ("P09","The verbs make it easier for you and Claude to see which fields could add a useful angle.","Having the verbs makes it easier for both me and Claude to understand which fields might bring in a unique and useful perspective.","Paraphrase; me becomes you; unique dropped."),
 ("P10","His second trick is what every heist movie spends its first half hour on.","every single heist movie spends the first 30 minutes assembling a diverse cast of characters and talents.","30 minutes becomes half hour. In the post the heist line is in the Range intro, not the crew trick."),
 ("P11","Assemble the crew.","Assemble the crew:","Same words."),
 ("P12","Felix pretends the deck has to be amazing, or aliens blow up Earth.","The deck needs to be amazing, otherwise aliens will blow up Earth.","Narrator adds pretends: the post states the stake as a premise."),
 ("P13","For production quality, he'd bring in an analyst, a journalist, and an editor.","For production quality, I'd bring in an analyst, a journalist, and an editor.","Verbatim except I'd becomes he'd."),
 ("P14","If it gets presented, a motion and audio designer, too.","If it has to be presented, probably a motion and audio designer, too.","Drops probably."),
 ("P15","Then a red team to attack it, a short seller, and a forensic accountant.","It might be useful to employ an adversarial \"red team\", too, so let's bring in a short seller and a forensic accountant.","Meaning shift risk: in the post the short seller and forensic accountant ARE the red team; the narration lists three items. Also might be useful becomes a definite step."),
 ("P16","He admits this takes creativity.","Putting this into practice isn't easy; it requires you to be creative.","Paraphrase."),
 ("P17","Until his colleague Alex Albert used Blender to render interior designs, he'd never thought of using Claude for 3D environments on his homepage. And he's made video games before.","Until I saw my colleague Alex Albert use Blender to render interior designs, I never considered using Claude for 3D environments for my homepage - even though I've previously made video games!","Close; I saw dropped (the post says he saw it, not that Alex used Blender with him)."),
 ("P18","His homepage is a 3D room now.",None,"Not in the post. Supported by the homepage HTML (WebGL room, ?room=1) saved in sources/src-felix-homepage.raw.html and On-screen: FELIXRIESEBERG.COM - HOMEPAGE - CAPTURED 2026-10-21 (frame-0084)."),
 ("P19","He says this is where he sees the most magic.","However, this is easily where I see the most magic happen.","Close; easily dropped."),
 ("P20","Before your next big ask, write the verbs, then name the crew.",None,"Narrator's call to action, not in the post."),
 ("P21","And have Claude do what a short seller does to research a position, not write like one.","Don't ask the model to write like a short seller, ask it to do what a short seller does to research their position.","Order swapped, model becomes Claude (the post says the advice is not model-specific)."),
 ("P22","Role-play makes the transcript weirder, not the result better.","It is easy to accidentally engage in role play, which will make your transcript weirder without improving the actual outcome.","Compressed; meaning kept."),
 ("P23","Who joins your crew first? The short seller or the forensic accountant?",None,"Narrator's engagement question."),
]
rows, bad = [], 0
for pid, nar, pst, note in PAIRS:
    t = cap_time(nar); nar_ok = t is not None
    pst_ok = (norm(pst) in post) if pst else None
    if not nar_ok or pst_ok is False: bad += 1
    if pst:
        r = difflib.SequenceMatcher(a=norm(nar).split(), b=norm(pst).split(), autojunk=False).ratio()
        cls = "verbatim" if r >= 0.97 else "close" if r >= 0.75 else "paraphrase"
    else:
        r, cls = None, "narrator-only"
    rows.append({"id": pid, "t": t, "narration": nar, "narration_in_captions": nar_ok, "post": pst,
                 "post_in_saved_post": pst_ok, "similarity": None if r is None else round(r, 3), "class": cls, "note": note})
(lane / f"words-vs-sources-{vid}.json").write_text(json.dumps({"post_url": POST_URL, "post_file": "sources/src-felix-post.txt",
    "pairs": rows, "failures": bad}, indent=1, ensure_ascii=False))
mm = lambda t: f"{int(t)//60:02d}:{int(t)%60:02d}" if t is not None else "--:--"
md = [f"# Words versus sources · {vid}", "", f"Post: {POST_URL} (saved: `sources/src-felix-post.txt`).",
      "Every narration line is checked word for word against `transcript-timed-StbUAJvivDc.jsonl`, and every post line against the saved post, by `created-tools/narration_vs_post.py`. Similarity = difflib word ratio.", "",
      "| # | [mm:ss] | Narration (captions) | ✓ | Post (Felix Rieseberg) | ✓ | Sim | Class | Difference |", "|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    md.append(f"| {r['id']} | {mm(r['t'])} | {r['narration']} | {'✅' if r['narration_in_captions'] else '❌'} | {r['post'] or '— (not in post)'} | "
              f"{'✅' if r['post_in_saved_post'] else ('—' if r['post_in_saved_post'] is None else '❌')} | {r['similarity'] if r['similarity'] is not None else '—'} | {r['class']} | {r['note']} |")
from collections import Counter
md += ["", "Counts: " + ", ".join(f"{k} {v}" for k, v in Counter(r['class'] for r in rows).items()) + f"; failures {bad}."]
(lane / f"words-vs-sources-{vid}.md").write_text("\n".join(md) + "\n")
print(json.dumps({"pairs": len(rows), "failures": bad, "classes": dict(Counter(r['class'] for r in rows))}))
sys.exit(1 if bad else 0)
