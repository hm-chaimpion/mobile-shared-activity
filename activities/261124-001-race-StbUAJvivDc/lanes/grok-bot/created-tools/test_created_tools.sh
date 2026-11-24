#!/usr/bin/env bash
# test_created_tools.sh - positive + negative tests for grok-bot's created checkers. Created by grok-bot 261124.
# Usage: bash created-tools/test_created_tools.sh <lane> <repo-root>   -> prints PASS/FAIL per test, exit 1 on any FAIL
L=${1:-.}; R=${2:-../../../..}; T=$(mktemp -d); fail=0
ok(){ echo "PASS $1"; }; ko(){ echo "FAIL $1"; fail=1; }
cp -r "$L"/{sources,knowledge-graph-StbUAJvivDc.json,quotes-sources-StbUAJvivDc.md,transcript-timed-StbUAJvivDc.jsonl,transcript-audio-StbUAJvivDc.jsonl} "$T"/
# 1 check_knowledge_graph: passes as delivered
python3 "$L/created-tools/check_knowledge_graph.py" "$T/knowledge-graph-StbUAJvivDc.json" >/dev/null && ok "kg-check passes real graph" || ko "kg-check passes real graph"
# 2 negative: node pointing at a missing source file must fail
python3 - "$T" <<'P'
import json,sys; p=sys.argv[1]+"/knowledge-graph-StbUAJvivDc.json"; g=json.load(open(p))
g["nodes"].append({"id":"fake","label":"Invented Person","type":"person","url":"https://example.com/x","source_file":"sources/none.txt","retrieved_at":"2026-11-24"}); json.dump(g,open(p,"w"))
P
python3 "$L/created-tools/check_knowledge_graph.py" "$T/knowledge-graph-StbUAJvivDc.json" >/dev/null && ko "kg-check catches unsaved source" || ok "kg-check catches unsaved source"
# 3 negative: url not matching saved header must fail
cp "$L/knowledge-graph-StbUAJvivDc.json" "$T/"; sed -i 's#"url": "https://alexalbert.me/"#"url": "https://alexalbert.me/wrong"#' "$T/knowledge-graph-StbUAJvivDc.json"
python3 "$L/created-tools/check_knowledge_graph.py" "$T/knowledge-graph-StbUAJvivDc.json" >/dev/null && ko "kg-check catches url mismatch" || ok "kg-check catches url mismatch"
# 4 quotes_sources_gate: passes as delivered; 5 negative: altered quote fails
python3 "$L/created-tools/quotes_sources_gate.py" "$T" StbUAJvivDc "$R/skills/youtube-process-cloud/scripts/quote_gate.py" >/dev/null && ok "quotes gate passes real file" || ko "quotes gate passes real file"
sed -i 's/I work on Claude at Anthropic./I lead all of Claude at Anthropic./' "$T/quotes-sources-StbUAJvivDc.md"
python3 "$L/created-tools/quotes_sources_gate.py" "$T" StbUAJvivDc "$R/skills/youtube-process-cloud/scripts/quote_gate.py" >/dev/null && ko "quotes gate catches altered quote" || ok "quotes gate catches altered quote"
# 6 compare_audio_captions: identical input gives similarity 1.0
python3 "$L/created-tools/compare_audio_captions.py" "$T/transcript-timed-StbUAJvivDc.jsonl" "$T/transcript-timed-StbUAJvivDc.jsonl" | grep -q '"similarity": 1.0' && ok "audio diff self-identity 1.0" || ko "audio diff self-identity 1.0"
# 7 narration_vs_post on the real lane passes
python3 "$L/created-tools/narration_vs_post.py" "$L" StbUAJvivDc >/dev/null && ok "narration_vs_post passes" || ko "narration_vs_post passes"
rm -rf "$T"; exit $fail
