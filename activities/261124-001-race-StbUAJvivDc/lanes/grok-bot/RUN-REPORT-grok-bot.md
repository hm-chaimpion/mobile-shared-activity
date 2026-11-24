# RUN REPORT · grok-bot · activity 261124-001 (Short StbUAJvivDc)

**Page:** https://hm-chaimpion.github.io/mobile-shared-activity/activities/261124-001-race-StbUAJvivDc/lanes/grok-bot/
**Surface:** Grok Bot (cloud box, executor subagent), driven from Hamish's mobile instruction t2518u.

## Clock (NZT, measured)
| Event | Time | Since start |
|---|---|---|
| Start (clone + read AGENTS/SPEC) | 2026-11-24 21:40:36 | 0:00 |
| Skill hashes + zip sha256 MATCH | 21:40:49 | 0:13 |
| Expert post saved | 21:42:15 | 1:39 |
| First ANSWER proved (proof_run pass) | 21:44:07 | 3:31 |
| **First push (ANSWER) commit 913f3c4** | **21:44:45** | **4:09** |
| Full bundle push | see `PUSHES` below | |

Token and cost counts are not visible to this agent: they are `null` in LOG, never estimated.

## What happened
1. **Hashes:** all 7 skill scripts match SPEC section 3. The zip sha256 `22f2c4c86a91dbdd767c139a650cf299d0e47115561764ecc094b4a3f75f0bb8` **matches** for both the repo copy and a fresh download of the raw URL.
2. **Extract:** `yt_cloud_extract.py` returned metadata and 107 keyframes, but captions failed with HTTP 429 (`BLOCKED-StbUAJvivDc.md`). I created `fetch_captions_retry.py` (one language per request), which got en-orig on the first try: 51 segments.
3. **Audio route:** `audio_route.py` was blocked (no Whisper). After installing faster-whisper on the box, it crashed on a PyAV API mismatch. I created `audio_whisper_numpy.py`, which ran Whisper small.en in 18.9 s and produced 31 segments. Captions vs audio: **98.17%** word match, and the 5 differences are spellings of names (Rieseberg/Riesberg, Anthropic/Anthropik, Kelley/Kelly, his/this, role play/roleplay).
4. **Expert:** the video description named Felix Rieseberg and the post URL. Both were fetched and saved, and the text was checked: **VERIFIED**.
5. **Narration vs post:** 23 pairs, each side found word for word in its own source. Results: 2 verbatim, 3 close, 13 paraphrase, 5 narrator-only. The most material difference is P15: the narration makes *red team* one more member, but in the post the short seller and forensic accountant *are* the red team.
6. **Gates:** graph_gate pass (30 nodes, 21 edges, 7 steps, 8 quotes). proof_run pass plus `--check` current. Written quotes: 28 in 11 sources, all found. Knowledge graph: 47 nodes and 50 edges, check pass. Created-tool tests: 7/7, including negative tests.

## Blocks and partial blocks (all resolved or worked around, none open)
| What | Error | Fix used | Would fully fix |
|---|---|---|---|
| Captions in yt_cloud_extract.py | HTTP 429 Too Many Requests | fetch_captions_retry.py | skill: request one sub-lang at a time |
| audio_route.py | no whisper; then `TypeError: open() got an unexpected keyword argument 'metadata_errors'` (PyAV) | audio_whisper_numpy.py | skill: decode with ffmpeg to numpy, or pin `av` |
| blender.org | HTTP 403 (Cloudflare challenge) | Wikipedia Blender page | a browser fetch |
| Wikipedia Tom Kelley (author) | HTTP 404 | publisher bios (Google Books, PRH) | — |
| x.com post text | JS-only for curl | nitter mirror, labelled | the X API |
| The Art of Innovation full text | not public | attribution VERIFIED via the post only; K08 UNVERIFIED | the book |

## Skill hashes actually run
f988f29fbdef47b4 yt_cloud_extract · 759cd0a2fe8ee4a7 quote_gate · e91d6ce05594a1af ocr_frames · ec8b92fb279bd71e graph_gate · 1fd171d098b36d5e render_graph · c00a03d77e437243 proof_run · f5eed8be94202ba8 audio_route.

## Self-score (section 6; your re-run decides)
| Lens | Self | Why |
|---|---|---|
| Result | 5 | Every claim is in CLAIMS with a status, and every quote is gated on both sides. The method card is usable unedited |
| Expert and feature | 4–5 | The expert is primary-sourced, with differences noted. The feature mapping is inferred (the post names subagents, not a product), and confidence is stated |
| Process | 5 | `run_all_grok_bot.sh` re-runs everything. 13 created tools, tested, including negatives |
| Visibility | 5 | The page shows gate badges, the checklist, and a narration-vs-post table; every file is linked |
| Independence | 5 | No questions asked. Every block is logged with its fix |

## Privacy notes (AGENTS rule 4)
Names: Felix Rieseberg, Alex Albert, Tom Kelley, Jonathan Littman, plus the historical figures cited in the post. Companies and orgs: Anthropic, IDEO, Electron, Blender, DIY Smart Code (channel), and Feldspar (named in DERIVATIVES as a possible audience). Local paths: `/workspace/mobile-shared-activity/...` appears in logs. No secrets, tokens or cookies are in the lane. `.gitignore` excludes the audio file.

## PUSHES
- 913f3c4 · 2026-11-24 21:44:45 NZT · first answer
