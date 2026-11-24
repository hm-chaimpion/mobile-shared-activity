#!/usr/bin/env python3
"""audio_whisper_numpy.py - audio route that sidesteps the PyAV/faster-whisper API mismatch
(TypeError: open() got an unexpected keyword argument 'metadata_errors') hit by skills/.../audio_route.py on this box.
Decodes audio with ffmpeg to 16 kHz mono float32 and passes the numpy array to faster_whisper.WhisperModel.
Writes transcript-audio-<id>.jsonl ({start,end,text}) and prints a JSON summary. Created by grok-bot 261124.
Usage: python3 audio_whisper_numpy.py <audio-file> <video_id> --out <lane> [--model small.en]"""
import argparse, json, pathlib, subprocess, time
import numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("audio"); ap.add_argument("vid"); ap.add_argument("--out", default=".")
ap.add_argument("--model", default="small.en"); a = ap.parse_args()
t0 = time.time()
pcm = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", a.audio, "-f", "f32le", "-ac", "1", "-ar", "16000", "-"],
                     capture_output=True, check=True).stdout
x = np.frombuffer(pcm, dtype=np.float32)
from faster_whisper import WhisperModel
segs, info = WhisperModel(a.model, device="cpu", compute_type="int8").transcribe(x, language="en", word_timestamps=False, vad_filter=False)
dest = pathlib.Path(a.out) / f"transcript-audio-{a.vid}.jsonl"; n = 0
with open(dest, "w") as f:
    for s in segs:
        f.write(json.dumps({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip()}, ensure_ascii=False) + "\n"); n += 1
print(json.dumps({"video_id": a.vid, "model": a.model, "segments": n, "audio_seconds": round(len(x) / 16000, 1), "wall_s": round(time.time() - t0, 1), "out": str(dest)}))
