---
name: whiteboard-video-extract
description: Turn a talk-over-whiteboard video (a fast, messy board plus speech, e.g. a YouTube Short) into a client-ready topic, a node-and-edge graph, an onion and checked quotes, with every label tied to a frame or a caption and every step re-provable. Use when asked to "extract the whiteboard", "turn this video into a diagram / onion / graph", "match his words to the board", or for the ICM / Jake Van Clief style of video. Builds on youtube-process-cloud (extraction, quote gate). Merged from the 261124 Grok + ChatGPT + Claude test (TPM report section P).
---

# Whiteboard video extract

Code first, tokens last. Every claim points to a frame or a caption line. The drawing is made from the gated
graph only. Works in a cloud run (no approvals) and on the Mac. For ChatGPT, Grok or any other model, paste
`BRIEF-portable-whiteboard-video.md` instead: it describes the same contract without the scripts.

`S=.claude/skills/whiteboard-video-extract/scripts` · `Y=.claude/skills/youtube-process-cloud/scripts` ·
run folder `runs/<yymmdd>-wb-<video-id>/` (copy `runs/_template-run-folder/` in).

## Steps

0. **Ask once, early (rule 6).** List the inputs you expected but don't have (screenshots, a better copy of the
   video, the speaker's own notes). Attended: ask in one message. Unattended: write them under "Questions for
   the owner" in the run report and carry on. Start `cost-<id>.json` now (rule 4).
1. **Extract, 0 tokens.** `python3 $Y/yt_cloud_extract.py "<url>" --out <run> --frames`
   gives metadata, timed captions, 1 fps keyframes and a contact sheet. A `BLOCKED-*.md` means name the domain and carry on.
2. **Audio route, in parallel (rule 5).** `python3 $S/audio_route.py "<url>" --out <run>`.
   Auto-captions drop words (the 261124 Short lost "Skill"). With no Whisper tool installed it writes
   `BLOCKED-audio-<id>.md`: say in the answer that the audio was not checked.
3. **OCR the frames, 0 tokens.** `python3 $S/ocr_frames.py <run>/frames-<id> --out <run>/ocr-<id>.jsonl [--fps 1]`.
   It is weak on handwriting, so treat it as one source among three (ocr, speech, vision).
4. **Read the board (tokens start here).** Look at the contact sheet and the key frames. Write
   `graph-<id>.json` to the shape in `templates/graph-template.json`:
   - `steps`: the argument in time order, each with start/end, a paraphrase and frame ids.
   - `nodes`: one per box or mark **on the board** or idea **spoken**. Each has `source` (ocr | speech | vision),
     `frame_ids` or `t`, and for vision a `vision_note` saying what you saw and where. Unsure? End the label
     with `?` and set `uncertain: true`. **Count the marks: one node per mark, never one per idea he lists.**
   - `edges`: from/to, relation, `evidence_steps`, status drawn | spoken | reconstructed.
   - `onion`: core-to-outer layers that name node ids. Say if it's your interpretation, not his.
   - `quotes`: word for word from the captions. On-screen text goes in with `on_screen: true`.
5. **Gate (rules 2, 3).**
   `python3 $S/graph_gate.py <run>/graph-<id>.json <run>/transcript-timed-<id>.jsonl --ocr <run>/ocr-<id>.jsonl --frames <run>/frames-<id>`
   Fix every failure. Writes `quote-evidence-<id>.jsonl` (caption excerpt and time beside each quote) and
   lists vision nodes under `human_check` with their frames.
6. **Draw from the graph only.** `python3 $S/render_graph.py <run>/graph-<id>.json` writes
   `diagram-<id>.mmd` (Mermaid) and `onion-<id>.md`. Never hand-draw a box that isn't a node.
7. **Answer first (rule 1).** `ANSWER-<id>.md` on one screen: topic in one line, the diagram (embed the
   Mermaid), the onion, up to 5 quotes with `[mm:ss]` taken from quote-evidence, and the limits
   (audio checked or not, uncertain labels, human-check list). Atoms/principles come after, marked as interpretation.
   Only spoken words go in quote marks or `>` lines. Write on-screen text as `On-screen: The less agents…` with no quote
   marks, because the quote gate treats every quoted phrase as speech. Mermaid sits in a fenced block, which the proof step skips.
8. **Prove, and prove again on every edition (rule 7).** `python3 $S/proof_run.py <run> <id>` runs the quote gate and the graph
   gate and stamps `proof-<id>.json` with file hashes. Before handing back: `proof_run.py <run> <id> --check`.
9. **Hand back (rule 8).** Run report + cost, commit, push the branch (AGENTS.md rule 4). Done = pushed.

## What the gates catch, and what they don't

| Caught (tested 261124) | Not caught |
|---|---|
| A quote not in the captions word for word | A caption error the audio would fix. No gate reads the audio transcript yet |
| A node with no source or frame | A spoken name drawn as an extra box. Grok's 4th client ("ChatGPT") is said aloud, so as `kind: spoken` it passes. The drawing makes it a rounded "spoken" box, not a board mark. Tagged `kind: board` without a frame, it fails |
| `kind: board` with no frame (a board mark with no evidence) | A false vision read (a board mark claimed with a frame and a note): it goes to `human_check` and a person looks |
| `?` without `uncertain`, or `uncertain` hidden | A label stated as certain when it isn't (Grok's ".md"). Mark it yourself |
| Edges with no step, onion layers naming missing nodes, steps out of order | Whether the onion is a fair reading of the speaker |
| An ANSWER or graph edited after its proof (ChatGPT's stale quote-check file) | Quote times are caption-segment starts, not the exact word (Grok audit D8) |

**Known gaps:** frames from `youtube-process-cloud` are deduped and renumbered, so a frame number is not a time
(`ocr_frames.py` leaves `t` null). The Mermaid diagram is good enough for review, not polished enough for a client.

Test record: `TEST-RECORD-whiteboard-video-261124.md`.
