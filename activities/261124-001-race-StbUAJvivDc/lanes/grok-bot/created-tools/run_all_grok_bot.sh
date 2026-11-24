#!/usr/bin/env bash
# run_all_grok_bot.sh - re-runs the whole grok-bot lane pipeline end to end from the repo root. Created by grok-bot 261124.
# Usage (from repo root): bash activities/261124-001-race-StbUAJvivDc/lanes/grok-bot/created-tools/run_all_grok_bot.sh [--fetch]
#   --fetch  also re-downloads video data and sources (network); without it, re-runs every gate/build on saved files only.
set -u; R=$(pwd); L=$R/activities/261124-001-race-StbUAJvivDc/lanes/grok-bot; S=$R/skills/whiteboard-video-extract/scripts; Y=$R/skills/youtube-process-cloud/scripts; V=StbUAJvivDc; C=$L/created-tools
if [ "${1:-}" = "--fetch" ]; then
  python3 $Y/yt_cloud_extract.py "https://www.youtube.com/shorts/$V" --out $L --frames
  python3 $C/fetch_captions_retry.py $V --out $L
  python3 $S/ocr_frames.py $L/frames-$V --out $L/ocr-$V.jsonl --fps 1
  python3 $S/audio_route.py "https://www.youtube.com/shorts/$V" --out $L || python3 $C/audio_whisper_numpy.py $L/audio-$V.m4a $V --out $L
fi
cd $L
python3 $C/compare_audio_captions.py transcript-timed-$V.jsonl transcript-audio-$V.jsonl --out audio-vs-captions-$V.json >/dev/null; echo "audio-vs-captions exit $?"
python3 $C/build_graph_StbUAJvivDc.py . >/dev/null
python3 $S/graph_gate.py graph-$V.json transcript-timed-$V.jsonl --ocr ocr-$V.jsonl --frames frames-$V --out . >/dev/null; echo "graph_gate exit $?"
python3 $S/render_graph.py graph-$V.json >/dev/null
python3 $S/proof_run.py . $V; echo "proof_run exit $?"
python3 $C/narration_vs_post.py . $V; echo "narration_vs_post exit $?"
python3 $C/quotes_sources_gate.py . $V $Y/quote_gate.py; echo "quotes_sources_gate exit $?"
python3 $C/build_knowledge_graph.py . >/dev/null; python3 $C/check_knowledge_graph.py knowledge-graph-$V.json >/dev/null; echo "check_knowledge_graph exit $?"
bash $C/test_created_tools.sh . $R; echo "tool tests exit $?"
python3 $C/build_index_html.py . $V
python3 $S/proof_run.py . $V --check; echo "proof --check exit $?"
