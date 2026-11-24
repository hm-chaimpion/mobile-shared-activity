---
name: youtube-process-cloud
description: Process a YouTube video in a cloud run — code-first extraction (metadata, timed captions, optional keyframes), then a one-screen answer and summary, with a quote gate so no quote is invented. Use when a cloud session is asked to "process", "summarise", "extract" or "explain" a YouTube video or Short. Cloud port of the HQ youtube:process command (261124).
---

# YouTube process (cloud)

Code first, tokens last. Never needs approval: no connectors, no remote sandboxes.

## Steps

1. **Run folder:** `runs/<yymmdd>-yt-<video-id>/` (copy `runs/_template-run-folder/` files in).
2. **Extract (0 tokens):**
   ```bash
   python3 .claude/skills/youtube-process-cloud/scripts/yt_cloud_extract.py "<url>" --out runs/<yymmdd>-yt-<id> [--frames]
   ```
   Add `--frames` only when the video shows a board, slides or screen. The video file is deleted after frames are cut.
   If it exits 1, read `BLOCKED-<id>.md`. **A network-policy block: stop that step, name the domain in the run
   report, carry on with what you have.** Never route around the proxy.
3. **Answer first:** write `ANSWER-<id>.md` from `transcript-plain-<id>.txt` (+ `contact-sheet-<id>.jpg` if made):
   one-liner, the thesis, a diagram or table if the video draws one, up to 5 quotes with `[mm:ss]`, limits.
   Mark board-only words or caption gaps as `[word]` and say where they came from.
4. **Quote gate (0 tokens):**
   ```bash
   python3 .claude/skills/youtube-process-cloud/scripts/quote_gate.py runs/<run>/ANSWER-<id>.md runs/<run>/transcript-timed-<id>.jsonl
   ```
   Every quote must be found. On-screen text that was not spoken is not a quote: label it "on-screen".
5. **Summary file** `summary-<id>.md`: summary (2–3 paragraphs), 5–10 insights, people and tools mentioned,
   action items, who it's relevant to. Only what code couldn't extract.
6. **Run report + cost**, then commit and push the run folder.

## Limits

- Captions are auto-generated: they drop words. Audio transcription is not in this version.
- Keyframe dedupe (ffmpeg mpdecimate) is not tuned for handheld footage yet.
- Needs the environment's allowed domains: youtube.com, googlevideo.com (see `setup/`).
