#!/usr/bin/env python3
"""compare_audio_captions.py - word-level diff between YouTube auto-captions and a Whisper audio transcript.
Lists every place the two disagree (with caption time), plus a similarity ratio, so caption errors the audio
would fix are visible (the gap the SKILL.md says no gate covers). Created by grok-bot 261124.
Usage: python3 compare_audio_captions.py transcript-timed-<id>.jsonl transcript-audio-<id>.jsonl --out audio-vs-captions-<id>.json
Exit 0 always (it reports; it does not judge)."""
import argparse, difflib, json, re
ap = argparse.ArgumentParser(); ap.add_argument("captions"); ap.add_argument("audio"); ap.add_argument("--out"); a = ap.parse_args()
def toks(path):
    out = []
    for l in open(path, encoding="utf-8"):
        if not l.strip(): continue
        r = json.loads(l)
        for w in re.sub(r"[^a-z0-9' ]+", " ", r["text"].lower().replace("’", "'").replace("-", " ")).split():
            out.append((w, r["start"]))
    return out
c, w = toks(a.captions), toks(a.audio)
sm = difflib.SequenceMatcher(a=[x for x, _ in c], b=[x for x, _ in w], autojunk=False)
diffs = []
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op != "equal":
        t = c[i1][1] if i1 < len(c) else (c[-1][1] if c else None)
        diffs.append({"op": op, "t_caption": t, "captions": " ".join(x for x, _ in c[i1:i2]), "audio": " ".join(x for x, _ in w[j1:j2])})
rep = {"caption_words": len(c), "audio_words": len(w), "similarity": round(sm.ratio(), 4), "differences": diffs}
if a.out: open(a.out, "w").write(json.dumps(rep, indent=1, ensure_ascii=False))
print(json.dumps(rep, indent=1, ensure_ascii=False))
