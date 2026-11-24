# Test record: whiteboard-video-extract v0.1

Run 2026-11-24 on Hamish's Mac (chat 1124[21]) against the Jake Van Clief Short `9xRA29stAd4`.
Inputs live in `tests/fixtures/`. `make_fixtures.py` rebuilds the Grok and ChatGPT graphs from the lab copies in
`_HQ/_lab/261124-plugin-skill-dataset-3-model-test/_1-inbox/model-outputs/`.

| # | Test | Input | Expected | Result |
|---|---|---|---|---|
| 1 | Captions | `yt_cloud_extract.py 9xRA29stAd4 --frames` | 82 caption segments | 82 segments in 8.7 s (measured). **Frames BLOCKED**: this Mac's yt-dlp (2026.07.04) gets a 403, as already known. Not updated (install = Hamish's call) |
| 2 | OCR | ChatGPT's 86 storyboard frames (low-res) | runs, reads some labels | 86 frames in 5.2 s, 66 with any text. Reads "MCP", "Agent", "mail", most of it noise. Confirms OCR can't be the only label source |
| 3 | Grok quotes | 7 spoken quotes from its "Principles" + opening line, plus the on-screen hook | spoken pass, hook flagged | 7 of 7 found word for word. The hook fails as on-screen with no evidence, which is correct. Agrees with the audit's 10 of 10 |
| 4 | ChatGPT graph | `05-model/261124-005-model.json` converted | quotes checkable now | 3 of 3 quotes found, each now with its caption excerpt and time (the audit couldn't check these). 12 of 12 steps and 10 of 10 edges pass. **9 of 9 nodes fail**: ChatGPT keeps its evidence on steps and edges, not on each node, so this format needs a per-node source added |
| 5 | 4th-box fixtures | Built by hand **from the audit text** (D1, D2). Grok's redraw image was never saved, so this is **not** a test on Grok's own output | see the four rows below | (a) 3 clients: pass, 2 vision nodes to human check. (b) 4th client "ChatGPT" as `kind: board, source: speech`: **fails** (board needs a frame). (c) Same as `kind: spoken`: **passes**. He says the name at 2:13, so the gate can't catch this. The render draws it as a spoken (rounded) box. (d) No source, hidden uncertainty, edge with no step: 3 failures |
| 6 | Render | good fixture, ChatGPT graph | Mermaid plus onion files | Files written, `.md?` styled dashed. **Not yet viewed as a rendered drawing** |
| 7 | Proof stamp | run folder with an ANSWER | altered quote fails, fixed passes, an edit after the proof fails `--check` | All three as expected |
| 7b | Proof with the diagram embedded (step 7) | ANSWER with Mermaid in a fence + on-screen hook | no false failures | First version: 3 false failures (2 Mermaid labels and the quoted hook). Fixed: fences stripped before gating, and on-screen text written without quote marks. Now passes. `tests/fixtures/ANSWER-example-9xRA29stAd4.md` |
| 8 | Audio | `audio_route.py` | BLOCKED, no Whisper | BLOCKED file written. **The transcribe path is untested** |

## Not tested

- Frames from a fresh download (blocked locally; expected to work in the cloud with the latest yt-dlp).
- The audio transcription path (no Whisper anywhere yet).
- A full run of every step by a model on a new video. That run is the real test: do it in the cloud next.
- Frame times: `yt_cloud_extract.py` dedupes with mpdecimate and renumbers (`setpts=N/FRAME_RATE/TB`), so frame
  number is not seconds. `ocr_frames.py` now leaves `t` null unless `--fps` is given for an un-deduped set.
  Fixing this means changing youtube-process-cloud (write a frame-to-time map), which was not done here.
- No gate compares the audio transcript with the captions yet.

## Timings (measured, this Mac, 2026-11-24)

Captions 8.7 s · OCR on 86 frames 5.2 s · each gate under 1 s. There is no before/after baseline yet: the
first cloud run with this skill gives the "after" (ECONOMICS: not_applicable until then).
