# SPEC: video → knowledge bundle race, activity 261124-001

**Video:** https://www.youtube.com/shorts/StbUAJvivDc
**Racers:** Grok Bot (lane `grok-bot`), Codex (lane `codex`). Claude joins later (lane `claude`).
**Same for everyone:** this spec and the skills in `/skills/` of this repo (also in `skills-bundle-v02-261124.zip`).
**You start with nothing else.** No transcript, frames or notes are provided. Do all the work from the video URL.

## 1. What we want

One **knowledge bundle** from this Short. It should work as a client asset and as a source we can make
derivatives from later (one-pagers, workshop exercises, prompt packs, skills).

The Short is about **presentation skills and methodology**, and it cites an **expert from Anthropic** and his
writing. (Our previous race was a different category: a product idea and the ICM method; see section 7.)

The bundle must contain:

1. **Topic:** one line, then the argument in the speaker's own order, with timestamps.
2. **Expert graph:** who the expert is (role, organisation, where he published this), the other people,
   books, posts and organisations cited, and how they connect. Every node has a source URL you actually
   fetched and saved.
3. **The feature:** which product capability the advice relies on (the Short names it in general terms).
   Identify it, link its **official documentation**, save the doc text, and say how sure you are.
4. **The method:** the presentation technique as a reusable method card: steps, when to use it, a worked
   example, and a prompt template someone could paste into any model.
5. **Words versus sources:** what the narrator says versus what the expert actually wrote. Quote both,
   each checked word for word against its own saved text. Note any differences.
6. **The visual layer:** what the video shows on screen (text, screenshots, diagrams, b-roll), tied to frames.
   If it shows a diagram, rebuild it as a graph. If it doesn't, say so with frame evidence.
7. **Derivatives list:** at least 5 assets this bundle could become, each with audience and effort.
8. **A shareable HTML page** (`index.html`) that presents all of the above. It must be readable by anyone,
   with no login: one self-contained file in this public repo (GitHub Pages serves it).

## 2. How to run

- **Never ask a question. Never wait.** If something is blocked, log it in your checklist as `blocked` with
  the error and what would fix it, then move to the next item. Keep going until every item is `done`,
  `blocked` or `skipped` (with a reason).
- **Fast first, then deep.** Write `ANSWER-StbUAJvivDc.md` as early as you can (we time it). Then keep
  improving it for as long as you can still add value.
- **Code first.** Use code wherever code can do the job. Use the skills in `/skills/` as they are.
  To change one, save a copy under a new name in your lane and give the reason in your decisions log.
- **Create what you lack.** If you need a script, skill or checker that doesn't exist, write it, save it in
  `lanes/<you>/created-tools/`, and list it in `TOOLS-<you>.md` (name, purpose, how to run, tested or not).
  At minimum, create `check_knowledge_graph.py`: every node has a URL, and every URL has a saved file in `sources/`.
- **Log every decision** (`DECISIONS-<you>.jsonl`): what you chose, the alternatives, and why.
- **Log time** (`LOG-<you>.jsonl`): a timestamped row at each step's start and end. Record tokens and cost
  where you can see them, otherwise null. Mark each value measured or estimated.
- **Add only.** Never delete or rewrite another lane's files. Write only inside `lanes/<you>/`, plus one row
  in `/REGISTER-activity.jsonl`.

## 3. The skills (same for both racers)

| Script | Use it for | sha256 (first 16) |
|---|---|---|
| `skills/youtube-process-cloud/scripts/yt_cloud_extract.py` | metadata, timed captions, 1 fps frames | `f988f29fbdef47b4` |
| `skills/youtube-process-cloud/scripts/quote_gate.py` | quote vs text, word for word | `759cd0a2fe8ee4a7` |
| `skills/whiteboard-video-extract/scripts/ocr_frames.py` | OCR every frame | `e91d6ce05594a1af` |
| `skills/whiteboard-video-extract/scripts/graph_gate.py` | every node, edge, step and quote tied to evidence | `ec8b92fb279bd71e` |
| `skills/whiteboard-video-extract/scripts/render_graph.py` | Mermaid diagram and onion from the graph only | `1fd171d098b36d5e` |
| `skills/whiteboard-video-extract/scripts/proof_run.py` | runs the gates, stamps hashes, `--check` catches stale proofs | `c00a03d77e437243` |
| `skills/whiteboard-video-extract/scripts/audio_route.py` | Whisper transcript if available, else a logged block | `f5eed8be94202ba8` |

Read `skills/whiteboard-video-extract/SKILL.md` for the steps and `templates/graph-template.json` for the
graph shape. Report the hashes you actually ran in your run report. **This spec overrides the SKILL.md**
where they differ: there is no `runs/` folder, your lane is the run folder; the push goes to your lane;
"Questions for the owner" go in the checklist as blocked items, never to a human.

**Two kinds of quote, two checks:**
- **Spoken** (the narrator): in quote marks in ANSWER, checked against your timed captions by `proof_run.py`.
- **Written** (the expert's blog, docs, book titles): in `quotes-sources-StbUAJvivDc.md` as `> ` lines, each with
  its URL. Check them with `quote_gate.py quotes-sources-StbUAJvivDc.md sources/<saved-file>.txt` per source.
- On-screen text: write it as `On-screen: …` with no quote marks.

**Frames:** if you cite a frame, deliver it in `frames-StbUAJvivDc/`. The graph gate fails cited frames that
aren't delivered. If you can't get frames at all, use only speech nodes and log the block.

## 4. Your lane: `activities/261124-001-race-StbUAJvivDc/lanes/<you>/`

Fixed names, so the two lanes can be compared file by file:

| File | Required | What |
|---|---|---|
| `ANSWER-StbUAJvivDc.md` | yes | One screen: topic, expert, feature, method, 5 spoken quotes `[mm:ss]`, limits |
| `index.html` | yes | The shareable page (self-contained) |
| `graph-StbUAJvivDc.json` | yes | Video graph: skill format (steps, nodes, edges, quotes) |
| `knowledge-graph-StbUAJvivDc.json` | yes | Expert graph: nodes `{id, label, type: person\|org\|work\|feature\|doc\|concept, url, source_file, retrieved_at}`, edges `{from, to, relation, source_file}` |
| `diagram-StbUAJvivDc.mmd` | yes | From `render_graph.py` |
| `method-card-StbUAJvivDc.md` | yes | The reusable presentation method |
| `feature-docs-StbUAJvivDc.md` | yes | The feature, official doc links, confidence |
| `quotes-sources-StbUAJvivDc.md` | yes | Written-source quotes with URLs |
| `DERIVATIVES-StbUAJvivDc.md` | yes | 5 or more derivative assets |
| `transcript-timed-StbUAJvivDc.jsonl` | yes | `{start, end, text}` per line, however you got the captions |
| `quote-evidence-StbUAJvivDc.jsonl` · `graph-gate-StbUAJvivDc.json` · `proof-StbUAJvivDc.json` | yes | Gate outputs |
| `frames-StbUAJvivDc/` · `ocr-StbUAJvivDc.jsonl` | if you got frames | Frames you cite, plus OCR |
| `sources/` | yes | Saved text of every page you cite (name, URL, fetched time at the top) |
| `CHECKLIST-<you>.jsonl` | yes | One row per item in section 5 |
| `DECISIONS-<you>.jsonl` · `LOG-<you>.jsonl` | yes | Decisions; timed steps |
| `TOOLS-<you>.md` · `created-tools/` | yes | Everything you built |
| `RUN-REPORT-<you>.md` | yes | What happened, blocks, skill hashes used, self-score (section 6), links |

**Hand back:** push to branch `lane/<you>/261124-001` and open a pull request, or commit straight to `main`
if you're only touching your lane folder. If you can't push at all, put the whole lane folder in one zip,
publish it wherever you can make it public, and put the link in your run report and register row.

**Register row** (append one line to `/REGISTER-activity.jsonl`):
`{"activity":"261124-001","model":"<you>","surface":"<app, mobile or web>","started":"<ISO>","ended":"<ISO>","first_answer_at":"<ISO>","lane":"activities/261124-001-race-StbUAJvivDc/lanes/<you>/","page_url":"<Pages or other public URL>","done":N,"blocked":N,"skipped":N}`

## 5. Checklist: same ids for both racers

Row: `{"id":"C01","status":"done|blocked|skipped","evidence":"<path or URL>","at":"<ISO>","note":"…"}`

| Id | Item |
|---|---|
| C01 | Start time logged; skills hashes checked against section 3 |
| C02 | Metadata saved (title, channel, date, duration, description) |
| C03 | Timed captions saved as `transcript-timed-…jsonl` |
| C04 | Frames saved (or the block logged) |
| C05 | OCR of frames |
| C06 | Audio route tried (transcript or logged block) |
| C07 | First `ANSWER` written (time-to-first-answer) |
| C08 | Video graph written; `graph_gate.py` passes |
| C09 | Spoken quotes pass `proof_run.py` |
| C10 | Expert identified; profile sources saved |
| C11 | The expert's original post found, saved, and compared with the narration |
| C12 | Every other cited person, book or org has a saved source |
| C13 | Feature identified, official docs saved, confidence stated |
| C14 | Knowledge graph written; your `check_knowledge_graph.py` passes |
| C15 | Written-source quotes pass `quote_gate.py` against saved sources |
| C16 | Method card with a worked example and a prompt template |
| C17 | Derivatives list (5 or more) |
| C18 | `index.html` self-contained, published, public URL recorded |
| C19 | Decisions, log and tools files complete |
| C20 | `proof_run.py --check` is current at hand-back; pushed; register row written |

## 6. How we will judge (written before the runs)

We re-run every gate ourselves, with our own copy of the captions. Your proof stamp is a claim; ours is the result.

| Lens | 1 | 3 | 5 |
|---|---|---|---|
| Result (fidelity, logic, use) | wrong or invented content | right but thin; some claims unsourced | every claim sourced and checked; a client could use it unedited |
| Expert and feature | person or feature wrong | right, with weak sources | right, primary sources saved, differences noted |
| Process (code-first, reuse, created tools) | manual, nothing re-runnable | partly scripted | scripted end to end; created tools tested and listed |
| Visibility (can a stranger follow it fast?) | files only | page plus files | page plus checklist, a stranger verifies in 5 minutes |
| Independence (no questions, judgement on blocks) | stopped or asked | finished with gaps unlogged | every item resolved or logged, with a fix |
| Speed | — | measured: time to first ANSWER and to hand-back (not scored 1–5, reported) | — |

Machine results reported beside the scores: checklist counts, gate exits, hash match, sources saved vs cited.

## 7. The previous race (for context, not for copying)

- Video: https://youtube.com/shorts/9xRA29stAd4 (a fast whiteboard, a product idea, the ICM method).
- Grok Bot's page from that race: https://jake-van-clief-icm-in-one-whiteboard-q3v6.pages.grok.bot/
- ChatGPT/Codex shipped a 396-file package. Claude stalled on its cloud setup.
- What the audit asked for next time (all built into this spec and the skills): ANSWER first; source text beside
  every quote; every diagram label tied to evidence (last time a redraw added a box the board didn't have);
  cost and clock from minute one; the audio route tried early; asking once instead of never (here: log it and
  move on); proofs re-run on every edition; the hand-back counts as part of done.

**We want an improved version: beat both previous runs on fidelity, evidence and speed.**
