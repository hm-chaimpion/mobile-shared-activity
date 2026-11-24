---
title: Verified codex delivery supplement
created: 2026-11-24
source_surface: chatgpt
model: GPT-6
author: ChatGPT Codex
co_author: Hamish McGregor
---

## Delivery verified

Primary commit: https://github.com/hm-chaimpion/mobile-shared-activity/commit/c9be2afd6c3a65d60f9ab9e066dca7e5fb11a957

Lane and exactly one codex register row were read back successfully after publication. Shell push failed; connected GitHub tree/commit/ref writes succeeded with the expected parent commit, preserving concurrent repository changes. No other lane, skill or spec was edited.

Checklist: 13 done, 7 blocked, 0 skipped. C20 delivery is now complete. Pages settings showed404 in a signed-out browser, so administration access was unavailable; no login was attempted and no user question was asked. The final Pages probe is recorded separately. No live page success is claimed.

## Reproduce

From repository root, use Python3.12. Install yt-dlp and markdown from PyPI; ffmpeg and tesseract are system dependencies for media processing. For the HTML metadata fallback first download the public page to /tmp/race-youtube.html, then run extract_public_page.py. Its caption attempt was tested and returned zero bytes. build_bundle.py and build_page.py are one-shot generators: retain earlier editions and write a new version when changing inputs.

Run the provided proof_run.py lane StbUAJvivDc --check, then the added knowledge, literal-quote and coverage checkers. Coverage must currently exit1. The exact written-source matches and knowledge graph provenance pass. A supplied empty-input proof pass must never be described as verified speech. No independent audio, frame or narration validation was achieved.

## Review package

261124-006-codex-review-bundle.zip contains the complete lane sources, tools, Markdown, JSON and HTML, excluding bytecode caches. MANIFEST-codex.json records each file hash; package_bundle.py verifies archive CRC and those hashes. The package test receipt is kept alongside the archive to avoid circular inclusion.

## Timing limit

The register ended time marks the pre-publish snapshot, not final network completion. delivery-receipt-codex.json records the later successful verification. Timing-correction-codex.json supersedes the initial unreliable start estimate.

reply: 6; conversation_url: unavailable; project_id: 261124-001
