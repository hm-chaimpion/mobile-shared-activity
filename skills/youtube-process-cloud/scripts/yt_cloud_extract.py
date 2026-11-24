#!/usr/bin/env python3
"""yt_cloud_extract.py — code-first YouTube extraction for cloud runs. 0 tokens.

Usage:
  python3 yt_cloud_extract.py <url-or-id> --out runs/<yymmdd>-yt-<id> [--frames] [--lang en]

Writes into --out:
  metadata-<id>.json         trimmed yt-dlp metadata (title, channel, upload date, duration, chapters, views)
  transcript-timed-<id>.jsonl one row per caption word/segment: {start, end, text}  (from json3 captions)
  transcript-plain-<id>.txt  the caption text, one line per segment, with [mm:ss] stamps
  frames-<id>/               (--frames) keyframes after ffmpeg scene dedupe + contact-sheet-<id>.jpg
  cost-<id>.json             wall-clock seconds per step, measured
  BLOCKED-<id>.md            only if a step failed: what, the error, and the domain to allow

Never retries a network policy denial (proxy 403/407): it records it and stops that step.
Needs: yt-dlp (pip), ffmpeg (apt) for --frames. Version 0.1, 2026-11-24 (CHaiMPION/cloud-runs-os).
"""
import argparse, json, pathlib, re, shutil, subprocess, sys, time

def vid(s):
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})", s)
    if m: return m.group(1)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", s): return s
    sys.exit(f"Not a YouTube URL or id: {s}")

def run(cmd, timeout=300):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr

def policy_denied(err):
    # Only the cloud egress proxy's own wording. A bare "HTTP 403" from YouTube usually means yt-dlp is out of date.
    return bool(re.search(r"agent proxy|no rule or network setting|\b407\b", err, re.I))

def err_tail(err):
    lines = [l for l in err.splitlines() if l.startswith("ERROR")] or err.strip().splitlines()[-2:]
    return " ".join(lines)[-400:]

def fix_for(err, domains):
    if policy_denied(err): return f"network policy: allow {domains} in the environment"
    if re.search(r"HTTP Error 403|Sign in to confirm|bot", err): return "YouTube refused: update yt-dlp (`pip install -U yt-dlp`); if it persists, the host IP is bot-checked"
    if re.search(r"429", err): return "rate-limited: wait and retry once, captions and media as separate requests"
    return "see error"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target"); ap.add_argument("--out", required=True)
    ap.add_argument("--frames", action="store_true"); ap.add_argument("--lang", default="en")
    a = ap.parse_args()
    v = vid(a.target); url = f"https://www.youtube.com/watch?v={v}"
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    cost, blocked = {"video_id": v, "steps": {}, "basis": "measured wall clock, seconds"}, []

    if not shutil.which("yt-dlp"):
        blocked.append(("tools", "yt-dlp not installed", "add `pip install yt-dlp` to the setup script"))

    # 1. metadata
    t = time.time()
    if not blocked:
        rc, so, se = run(["yt-dlp", "-j", "--no-warnings", url])
        if rc == 0:
            m = json.loads(so)
            keep = {k: m.get(k) for k in ("id", "title", "channel", "uploader_id", "upload_date", "duration",
                                           "view_count", "like_count", "chapters", "description", "webpage_url")}
            (out / f"metadata-{v}.json").write_text(json.dumps(keep, indent=1, ensure_ascii=False))
        else:
            blocked.append(("metadata", err_tail(se), fix_for(se, "youtube.com")))
    cost["steps"]["metadata"] = round(time.time() - t, 1)

    # 2. captions (json3 has word timings; prefer original-language auto captions)
    t = time.time()
    if not any(b[0] in ("tools", "metadata") for b in blocked):
        tmp = out / f".caps-{v}"; tmp.mkdir(exist_ok=True)
        rc, so, se = run(["yt-dlp", "--no-warnings", "--skip-download", "--write-subs", "--write-auto-subs",
                          "--sub-langs", f"{a.lang}-orig,{a.lang}.*,{a.lang}", "--sub-format", "json3",
                          "-o", str(tmp / "%(id)s.%(ext)s"), url])
        files = sorted(tmp.glob("*.json3"), key=lambda p: ("orig" not in p.name, p.name))
        if files:
            segs = []
            for ev in json.loads(files[0].read_text()).get("events", []):
                text = "".join(s.get("utf8", "") for s in ev.get("segs", []) or []).strip()
                if text and text != "\n":
                    st = ev.get("tStartMs", 0) / 1000; en = st + ev.get("dDurationMs", 0) / 1000
                    segs.append({"start": round(st, 2), "end": round(en, 2), "text": " ".join(text.split())})
            with open(out / f"transcript-timed-{v}.jsonl", "w") as f:
                for s in segs: f.write(json.dumps(s, ensure_ascii=False) + "\n")
            (out / f"transcript-plain-{v}.txt").write_text(
                "\n".join(f"[{int(s['start']//60):02d}:{int(s['start']%60):02d}] {s['text']}" for s in segs) + "\n")
            cost["caption_file"] = files[0].name; cost["segments"] = len(segs)
        else:
            blocked.append(("captions", err_tail(se or "no caption file"),
                            fix_for(se, "youtube.com") if se.strip() else "video may have no captions; try audio transcription"))
        shutil.rmtree(tmp, ignore_errors=True)
    cost["steps"]["captions"] = round(time.time() - t, 1)

    # 3. frames (optional): low-res video, 1 fps, drop near-duplicates, contact sheet
    if a.frames and not any(b[0] in ("tools", "metadata") for b in blocked):
        t = time.time()
        if not shutil.which("ffmpeg"):
            blocked.append(("frames", "ffmpeg not installed", "add `apt-get install -y ffmpeg` to the setup script"))
        else:
            mp4 = out / f".video-{v}.mp4"
            rc, so, se = run(["yt-dlp", "--no-warnings", "-f", "bv*[height<=720][ext=mp4]+ba/b[height<=720]/b", "--merge-output-format", "mp4",
                              "-o", str(mp4), url], timeout=900)
            if rc != 0 or not mp4.exists():
                blocked.append(("frames", err_tail(se), fix_for(se, "googlevideo.com, *.googlevideo.com")))
            else:
                fd = out / f"frames-{v}"; fd.mkdir(exist_ok=True)
                run(["ffmpeg", "-loglevel", "error", "-i", str(mp4), "-vf", "fps=1,mpdecimate=hi=64*24:lo=64*12:frac=0.5,setpts=N/FRAME_RATE/TB",
                     "-vsync", "vfr", str(fd / "frame-%04d.jpg")], timeout=900)
                n = len(list(fd.glob("frame-*.jpg"))); cost["keyframes"] = n
                if n:
                    cols = 6; rows = max(1, -(-n // cols))
                    run(["ffmpeg", "-loglevel", "error", "-pattern_type", "glob", "-i", str(fd / "frame-*.jpg"),
                         "-vf", f"scale=240:-1,tile={cols}x{rows}", "-frames:v", "1", str(out / f"contact-sheet-{v}.jpg")])
                mp4.unlink(missing_ok=True)  # never commit the video
        cost["steps"]["frames"] = round(time.time() - t, 1)

    cost["steps"]["total"] = round(sum(x for x in cost["steps"].values()), 1)
    (out / f"cost-{v}.json").write_text(json.dumps(cost, indent=1))
    if blocked:
        (out / f"BLOCKED-{v}.md").write_text("# Blocked steps\n\n| Step | Error (tail) | Fix |\n|---|---|---|\n" +
            "".join(f"| {s} | {e.replace('|', '/').replace(chr(10), ' ')[:300]} | {fx} |\n" for s, e, fx in blocked))
    print(json.dumps({"video_id": v, "out": str(out), "blocked": [b[0] for b in blocked], **{k: cost.get(k) for k in ("segments", "keyframes")}, "seconds": cost["steps"]}))
    sys.exit(1 if blocked else 0)

if __name__ == "__main__":
    main()
