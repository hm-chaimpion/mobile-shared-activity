#!/usr/bin/env python3
"""ocr_frames.py: run tesseract over every frame and write one JSON line per frame. Uses no tokens.

Usage: python3 ocr_frames.py <frames-dir> --out ocr-<id>.jsonl [--fps 1] [--psm 11]

Each line: {"frame": "frame-014.png", "t": 13.0, "text": "...", "words": N}
t = frame number / fps, only when --fps is given (frame-001 = 0 s). Default null: youtube-process-cloud's frames are
deduped with mpdecimate and renumbered, so the frame number is NOT seconds there (known gap, 261124).
Tesseract is weak on handwriting: an empty result is evidence of nothing, not proof a label is absent.
The graph gate therefore also accepts vision reads, with a frame id and a note, for a human to check.
Needs: tesseract (apt-get install tesseract-ocr; already in setup/cloud-setup-script-media.sh).
Version 0.1, 2026-11-24 (CHaiMPION/cloud-runs-os, whiteboard-video-extract).
"""
import argparse, json, pathlib, re, shutil, subprocess, sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("frames"); ap.add_argument("--out", required=True)
    ap.add_argument("--fps", type=float, default=None,
                    help="only for frames cut at a fixed rate with NO dedupe; yt_cloud_extract renumbers after mpdecimate, so leave t null")
    ap.add_argument("--psm", default="11")
    a = ap.parse_args()
    if not shutil.which("tesseract"):
        sys.exit("BLOCKED: tesseract not installed (add `apt-get install -y tesseract-ocr` to the setup script)")
    files = sorted(p for p in pathlib.Path(a.frames).iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg"))
    n_text = 0
    with open(a.out, "w", encoding="utf-8") as f:
        for p in files:
            r = subprocess.run(["tesseract", str(p), "-", "--psm", a.psm], capture_output=True, text=True, timeout=60)
            text = " ".join(r.stdout.split())
            m = re.search(r"(\d+)", p.stem)
            t = round((int(m.group(1)) - 1) / a.fps, 1) if (m and a.fps) else None
            n_text += bool(text)
            f.write(json.dumps({"frame": p.name, "t": t, "text": text, "words": len(text.split())}, ensure_ascii=False) + "\n")
    print(json.dumps({"frames": len(files), "frames_with_text": n_text, "out": a.out}))


if __name__ == "__main__":
    main()
