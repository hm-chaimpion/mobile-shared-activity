---
created: 2026-11-24
source_surface: chatgpt
model: GPT-6
author: ChatGPT Codex
co_author: Hamish McGregor
---

## Created tools

Run from repository root with Python 3.12. Pass the lane path to check scripts. build_page.py additionally uses the markdown package. Source and media tools use only public endpoints, never credentials. fetch_sources.py handles independent requests concurrently.

| Tool | Purpose | Test status |
|---|---|---|
| acquire_media.py | Try public media and captions advertised by YouTube's public player. No cookies. | Executed; results in lane |
| build_bundle.py | Build source-grounded research edition. Does not invent video transcript or frames. | Executed; results in lane |
| build_page.py | One-file, mobile-first HTML projection of the portable research bundle. | Executed; results in lane |
| check_bundle_coverage.py | Reject vacuous evidence passes. Usage: python check_bundle_coverage.py LANE. | Executed; results in lane |
| check_exact_quotes.py | Literal written-quote check, supplementing the supplied normalising gate. | Executed; results in lane |
| check_knowledge_graph.py | #!/usr/bin/env python3 | Executed; results in lane |
| extract_public_page.py | Fallback: parse public YouTube player JSON; never use cookies. Run from repo root. | Executed; results in lane |
| fetch_sources.py | Fetch primary sources as readable UTF-8 with provenance. Run from repo root. | Executed; results in lane |
| finalise_audit.py | Create checklist, decisions, tools and run report without changing earlier editions. | Executed to create these records |
| run_checks.py | Run supplied gates, coverage and regression checks; save measured logs. Repo root cwd. | Executed; results in lane |

check_knowledge_graph.py has negative tests for empty/missing-source graphs. The supplied quote gate rejects an invented fixture; the added coverage checker fails the actual incomplete bundle as intended. No live multi-agent product execution was tested. Public media acquisition is tested and blocked, not successful.

Re-run: `python created-tools/check_knowledge_graph.py knowledge-graph-StbUAJvivDc.json` from the lane, or use full lane paths from repo root. `python created-tools/check_bundle_coverage.py .` must currently exit 1. Do not rerun build generators over an immutable edition; copy to a new version first.

reply: 5; conversation_url: unavailable; project_id: 261124-001
