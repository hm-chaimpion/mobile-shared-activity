---
created: 2026-11-24
source_surface: chatgpt
model: GPT-6
author: ChatGPT Codex
co_author: Hamish McGregor
---

## Outcome
Source-grounded presentation research bundle delivered to codex lane. Checklist: 13 done, 7 blocked, 0 skipped. Complete video validation is not claimed. C20's delivery status is established by the subsequent remote receipt, not by this pre-publish report.

## Speed and cost
First provisional answer: 2026-11-24T08:42:34.532503+00:00. Measured clone anchor to first answer: 119.6 seconds. Task-start-to-answer is unknown because the initial clock was not captured. The initial start estimate in the log is superseded by timing-correction-codex.json. Final publication timing is in the delivery receipt. Model tokens and dollars are null because telemetry is unavailable. Extraction cost file measures only that script's wall clock, not total race cost.

## Evidence and checks
13 expert graph nodes, 13 edges, seven unique graph URLs, all with saved source files. Seven successful primary-page fetches plus YouTube metadata are saved; the Blender official fetch failed403. The Blender node points to the successfully saved original post, and claims only what that post says. Five short written excerpts (22 words total) pass normalised and literal checks. Three negative regression fixtures pass.

The supplied proof and graph gate exit0 over empty video inputs. This is a known vacuous-pass limitation, not a content verification. The added coverage checker exits1 as intended: no timed speech, no five spoken quotes, no frame evidence. proof_run --check is current against the unchanged first answer, graph and transcript. Research edition v02 is not covered by the supplied spoken-quote proof; it contains no narrator quotations and is supported by written sources.

## Blocks and fixes
- YouTube extraction: latest installed yt-dlp2026.11.23 encountered a bot-check. Public HTML yielded metadata; advertised captions returned zero bytes and media403. Stop media attempts. Fix: permitted media/caption access.
- Audio: supplied route found no Whisper. Installing it alone cannot fix unavailable media.
- Frames/OCR: absent media; no assertion about whether a diagram exists.
- Narrator comparison: impossible without speech. Description-to-post comparison is clearly labelled.
- Pages: requested URL currently404; API404 does not identify exact cause. No authenticated CLI or administration tool was available. Fix: configure repository Pages publishing with administration access.
- Shell push: no credential. Connected GitHub write route is used for final delivery; see receipt.

## Self-score (1–5; not independently judged)
| Lens | Score | Reason |
|---|---|---|
| Result | 2 | Useful method, but major video evidence absent |
| Expert and feature | 4 | Primary sources saved; specific product mapping remains inference |
| Process | 4 | Saved deterministic tools and negative checks; early timing incomplete |
| Visibility | 3 | Polished page and audit route; Pages publication unresolved |
| Independence | 5 | No questions; all blockers explicit with fixes |

## Privacy notes
Public professional names include Felix Rieseberg, Alex Albert, Tom Kelley, Jonathan Littman, Hamish McGregor and entities appearing in saved public pages. Public publisher description retains promotional URLs. Saved source pages include other public names and links. Example business data is fictional; no private client data, credentials, cookies or signed media URLs are included. Creator scripts contain scratch paths such as /tmp/race-youtube.html; no private device path is needed. No attribution was added to git commits.

## Skill hashes
Bundle expected and actual: 22f2c4c86a91dbdd767c139a650cf299d0e47115561764ecc094b4a3f75f0bb8 (MATCH).

- `skills/youtube-process-cloud/scripts/yt_cloud_extract.py`: `f988f29fbdef47b4c3ef6de258039937e41b6e352980529e19f21d7fa28f16f2` (used)
- `skills/youtube-process-cloud/scripts/quote_gate.py`: `759cd0a2fe8ee4a70d123bc2d8153cb51761aa355e80dfb8060ef719f5fb9d8a` (used)
- `skills/whiteboard-video-extract/scripts/proof_run.py`: `c00a03d77e437243fc92b2f62c682a3e5fb84802649db6cb86d15af7cb5491d8` (used)
- `skills/whiteboard-video-extract/scripts/graph_gate.py`: `ec8b92fb279bd71e5aeadb445629c60ce74b7db6ca71a3c80a3df1c90a596678` (used)
- `skills/whiteboard-video-extract/scripts/ocr_frames.py`: `e91d6ce05594a1af8a130f3a27fb7ee1d2070c17042571b2eb0ef4bc3d5c159a` (hashed; not run because frames absent)
- `skills/whiteboard-video-extract/scripts/render_graph.py`: `1fd171d098b36d5ebdd4f7055aab78c406d1b6c771ed91fde92be2e36f682131` (used)
- `skills/whiteboard-video-extract/scripts/audio_route.py`: `f5eed8be94202ba880cae10f2ed98279476fd862b067f969f45d06df5beebede` (used)

## Links
- Requested page: https://hm-chaimpion.github.io/mobile-shared-activity/activities/261124-001-race-StbUAJvivDc/lanes/codex/
- Lane: https://github.com/hm-chaimpion/mobile-shared-activity/tree/main/activities/261124-001-race-StbUAJvivDc/lanes/codex
- Primary post: https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/

reply: 5; conversation_url: unavailable; project_id: 261124-001
