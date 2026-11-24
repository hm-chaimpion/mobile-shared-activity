# Brief: extract a talk-over-whiteboard video (portable, v2)

Paste this into any model (Claude, ChatGPT/Codex, Grok, Gemini) with the video link. Version 2 of the 261123
prompt Hamish gave all three models, rewritten after the 261124 audits. Script versions of each check live in
`CHaiMPION/cloud-runs-os/.claude/skills/whiteboard-video-extract/`.

---

**Video:** <url>  ·  **Speaker:** <name, and the method they own>  ·  **Return to:** <repo + branch, or Drive folder>

The speaker talks fast over a messy whiteboard. Turn it into a topic, a diagram and an onion I can show a client,
with his words matched to the board. Every step saved separately with proof, so quality, cost and speed can be
checked and improved. Use code wherever code can do it. Look for existing internal tools before building one.
Never delete anything; add only. Work with no further instructions from me.

**Rules**

1. **ANSWER first.** One screen, written as soon as you can: topic in one line, the diagram, the onion,
   at most 5 quotes with `[mm:ss]`, and the limits. Everything else is evidence behind it.
2. **Put the source text beside each quote:** the caption excerpt and its start time, not only an id or hash.
   A reviewer must be able to check each quote without the video.
3. **Every label has evidence.** Build the diagram as data first: nodes (each with source = OCR, speech or vision,
   plus a frame id or time), edges (each citing a step), steps in time order. Draw only from that data. One box per
   mark on the board. Never add one per idea he lists. Mark unsure labels with `?` and keep them unsure in the
   picture too. Quotes are word for word. On-screen text is labelled on-screen, never presented as speech.
4. **Cost and clock from minute one:** a cost file with start, end, active minutes, tokens if visible (else null),
   each value marked measured or estimated.
5. **Audio route early, in parallel.** Auto-captions drop words. Transcribe the audio if you can. If you can't,
   say "audio not checked" in the ANSWER.
6. **Ask once, early,** for inputs you expected and don't have (missing screenshots, better video). If no one
   is there to answer, list the questions in the report and carry on.
7. **Re-run every check on every edition** and stamp the result with file hashes. An old proof on a new edition counts as a failure.
8. **Hand back:** put the output where "Return to" says (push the branch / upload the folder). It isn't done until it's there.

**Deliver:** `ANSWER`, `graph` (nodes/edges/steps/onion/quotes as JSON), the rendered diagram and onion,
`quote-evidence`, the frames or contact sheet you used, `cost`, a run report (what failed, what you'd do
next), and a self-score using these lenses: result, process, visibility, independence, decisions (1–5, with what a 5 needs).
