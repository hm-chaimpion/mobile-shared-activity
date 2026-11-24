#!/usr/bin/env python3
"""audio_route.py: transcribe the audio with Whisper, if a Whisper tool is installed. Otherwise record a block.

Usage: python3 audio_route.py <url-or-id> --out <run-dir>

UNTESTED (2026-11-24): no Whisper tool is installed on the Mac or in setup/cloud-setup-script-media.sh.
Installing one is the owner's call. Until then this script only detects that and writes BLOCKED-audio-<id>.md,
so the run report says plainly that the audio was not checked.
Why it exists: auto-captions dropped a key word in the 261124 Short ("Skill" was only on the board), and
neither Grok nor ChatGPT checked the audio. Run it early, in parallel with frames.
Order tried: the `faster_whisper` Python module, then the `whisper` CLI.
Version 0.1, 2026-11-24 (CHaiMPION/cloud-runs-os, whiteboard-video-extract).
"""
import argparse, importlib.util, json, pathlib, re, shutil, subprocess, sys


def vid(s):
    m = re.search(r"(?:v=|shorts/|youtu\.be/)([\w-]{11})", s)
    return m.group(1) if m else s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target"); ap.add_argument("--out", required=True); ap.add_argument("--model", default="small")
    a = ap.parse_args()
    v, out = vid(a.target), pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    have_fw = importlib.util.find_spec("faster_whisper") is not None
    have_cli = shutil.which("whisper") is not None
    if not (have_fw or have_cli):
        (out / f"BLOCKED-audio-{v}.md").write_text(
            "# Blocked: audio route\n\nNo Whisper tool installed (faster-whisper module or whisper CLI).\n"
            "The audio was NOT checked: quotes rest on auto-captions only.\n"
            "Fix (needs the owner's OK): add `pip install -q faster-whisper` to setup/cloud-setup-script-media.sh.\n")
        print(json.dumps({"video_id": v, "audio": "blocked", "reason": "no whisper tool"}))
        sys.exit(1)
    audio = out / f"audio-{v}.m4a"
    r = subprocess.run(["yt-dlp", "-q", "-f", "bestaudio[ext=m4a]/bestaudio", "-o", str(audio),
                        f"https://www.youtube.com/watch?v={v}"], capture_output=True, text=True, timeout=600)
    if r.returncode or not audio.exists():
        (out / f"BLOCKED-audio-{v}.md").write_text(f"# Blocked: audio download\n\n```\n{r.stderr[-800:]}\n```\n")
        sys.exit(1)
    dest = out / f"transcript-audio-{v}.jsonl"
    if have_fw:
        from faster_whisper import WhisperModel
        segs, _ = WhisperModel(a.model, compute_type="int8").transcribe(str(audio))
        with open(dest, "w", encoding="utf-8") as f:
            for s in segs:
                f.write(json.dumps({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()}) + "\n")
    else:
        subprocess.run(["whisper", str(audio), "--model", a.model, "--output_format", "json", "--output_dir", str(out)],
                       check=True, timeout=1800)
        data = json.loads((out / f"audio-{v}.json").read_text())
        with open(dest, "w", encoding="utf-8") as f:
            for s in data.get("segments", []):
                f.write(json.dumps({"start": s["start"], "end": s["end"], "text": s["text"].strip()}) + "\n")
    print(json.dumps({"video_id": v, "audio": "ok", "out": str(dest)}))


if __name__ == "__main__":
    main()
