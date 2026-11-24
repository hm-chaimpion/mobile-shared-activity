# TOOLS · grok-bot · activity 261124-001

## Shared skills used, unmodified (sha256 checked against SPEC section 3, all match)
| Script | sha256 (first 16) | Used for |
|---|---|---|
| skills/youtube-process-cloud/scripts/yt_cloud_extract.py | f988f29fbdef47b4 | metadata, 107 keyframes, contact sheet (captions step hit HTTP 429) |
| skills/youtube-process-cloud/scripts/quote_gate.py | 759cd0a2fe8ee4a7 | spoken quotes (via proof_run) and written quotes per source (via quotes_sources_gate.py) |
| skills/whiteboard-video-extract/scripts/ocr_frames.py | e91d6ce05594a1af | OCR of all frames |
| skills/whiteboard-video-extract/scripts/graph_gate.py | ec8b92fb279bd71e | video graph gate |
| skills/whiteboard-video-extract/scripts/render_graph.py | 1fd171d098b36d5e | diagram-StbUAJvivDc.mmd, onion-StbUAJvivDc.md |
| skills/whiteboard-video-extract/scripts/proof_run.py | c00a03d77e437243 | proof + --check |
| skills/whiteboard-video-extract/scripts/audio_route.py | f5eed8be94202ba8 | tried twice: blocked (no whisper), then crashed (PyAV API); replaced by audio_whisper_numpy.py |

## Created tools (all in `created-tools/`, all tested)
| Tool | Purpose | Run | Tested |
|---|---|---|---|
| `fetch_captions_retry.py` | Captions one language at a time, with backoff (fixes the 429) → transcript-timed/plain | `python3 fetch_captions_retry.py StbUAJvivDc --out <lane>` | yes, real run: en-orig, 51 segments |
| `save_source.py` | Fetch a URL, keep raw HTML/PDF, write `sources/<name>.txt` with a header (url, final url, HTTP status, fetched_at NZT, sha256) | `python3 save_source.py <name> <url> --out sources` | yes: 45 sources, failures reported (403/404) |
| `audio_whisper_numpy.py` | Audio route via ffmpeg → numpy → faster-whisper (avoids the PyAV crash) | `python3 audio_whisper_numpy.py audio.m4a StbUAJvivDc --out <lane>` | yes: 31 segments, 18.9 s |
| `compare_audio_captions.py` | Word diff, captions vs audio transcript | see docstring | yes: self-identity 1.0 (test 6) |
| `narration_vs_post.py` | C11: each narration line in captions + each post line in the saved post, word diff, class | `python3 narration_vs_post.py <lane> StbUAJvivDc` | yes: 23 pairs, 0 failures (test 7) |
| `quotes_sources_gate.py` | C15: runs skill quote_gate.py per source section, checks URL = saved header | `python3 quotes_sources_gate.py <lane> StbUAJvivDc <quote_gate.py>` | yes + negative (altered quote caught) |
| `build_graph_StbUAJvivDc.py` | Writes the video graph from code (diffable, re-buildable) | `python3 build_graph_StbUAJvivDc.py <lane>` | yes: graph_gate pass |
| `build_knowledge_graph.py` | Writes the expert graph; url/retrieved_at read from source headers | `python3 build_knowledge_graph.py <lane>` | yes |
| `check_knowledge_graph.py` | **Spec-required.** Every node has a URL and a saved 200 source whose header URL matches; edges valid | `python3 check_knowledge_graph.py knowledge-graph-StbUAJvivDc.json` | yes + 2 negative tests |
| `build_index_html.py` | Self-contained index.html built only from lane files, with gate badges | `python3 build_index_html.py <lane> StbUAJvivDc` | yes: no external script/css; Pages check in RUN-REPORT |
| `lane_log.py` | Appends timestamped LOG / DECISIONS / CHECKLIST rows with `mmdd:[NNN] h.mmam/pm NZT` stamps | see docstring | yes (used for all rows after 21:44) |
| `test_created_tools.sh` | 7 positive/negative tests of the checkers | `bash test_created_tools.sh <lane> <repo>` | 7/7 PASS (`work/tool-tests.txt`) |
| `run_all_grok_bot.sh` | Re-runs every gate and build end to end (`--fetch` re-downloads too) | from repo root: `bash .../created-tools/run_all_grok_bot.sh` | yes: all exits 0 |

Box-only installs (not in the repo): `pip install --user --break-system-packages faster-whisper markdown`.
