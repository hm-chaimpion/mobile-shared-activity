#!/usr/bin/env python3
"""fetch_captions_retry.py - retry YouTube auto-captions (json3) one language at a time with backoff,
then write transcript-timed-<id>.jsonl ({start,end,text} per caption event) and transcript-plain-<id>.txt.
Created by grok-bot 261124 because yt_cloud_extract.py hit HTTP 429 asking for several sub-langs at once.
Usage: python3 fetch_captions_retry.py <video_id> --out <lane> [--langs en-orig,en] [--tries 4]
"""
import argparse, json, pathlib, subprocess, sys, time, tempfile
ap = argparse.ArgumentParser(); ap.add_argument("vid"); ap.add_argument("--out", default=".")
ap.add_argument("--langs", default="en-orig,en"); ap.add_argument("--tries", type=int, default=4)
a = ap.parse_args(); out = pathlib.Path(a.out); url = f"https://www.youtube.com/watch?v={a.vid}"
log = []
for lang in a.langs.split(","):
    for i in range(a.tries):
        tmp = pathlib.Path(tempfile.mkdtemp())
        p = subprocess.run(["yt-dlp", "--no-warnings", "--skip-download", "--write-auto-subs", "--write-subs",
                            "--sub-langs", lang, "--sub-format", "json3", "--sleep-subtitles", "3",
                            "-o", str(tmp / "%(id)s.%(ext)s"), url], capture_output=True, text=True)
        files = list(tmp.glob("*.json3"))
        log.append({"lang": lang, "try": i + 1, "rc": p.returncode, "err": p.stderr.strip()[-200:], "got": bool(files)})
        if files:
            ev = json.load(open(files[0])).get("events", [])
            rows = []
            for e in ev:
                t = "".join(s.get("utf8", "") for s in e.get("segs", []) or []).replace("\n", " ").strip()
                if not t: continue
                st = e.get("tStartMs", 0) / 1000; en = st + e.get("dDurationMs", 0) / 1000
                rows.append({"start": round(st, 2), "end": round(en, 2), "text": t})
            with open(out / f"transcript-timed-{a.vid}.jsonl", "w") as f:
                for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")
            (out / f"transcript-plain-{a.vid}.txt").write_text("\n".join(
                f"[{int(r['start'])//60:02d}:{int(r['start'])%60:02d}] {r['text']}" for r in rows) + "\n")
            (out / f"captions-raw-{a.vid}.{lang}.json3").write_text(files[0].read_text())
            print(json.dumps({"ok": True, "lang": lang, "segments": len(rows), "log": log})); sys.exit(0)
        time.sleep(10 * (i + 1))
print(json.dumps({"ok": False, "log": log})); sys.exit(1)
