# mobile-shared-activity

A shared, **public** workspace for AI models run from a phone or the cloud: Grok Bot, Codex, Claude, or any other.
Each activity gets a folder. Each model works in its own lane inside it, so outputs can be compared side by
side. Work done here is pulled back into the main working environment later.

**Public repo:** secrets (keys, tokens, passwords) never go here. Names, emails, paths and client mentions are
allowed but noted (see `AGENTS.md` rule 4).
HTML pages are served by GitHub Pages: `https://hm-chaimpion.github.io/mobile-shared-activity/<path>`.

## Layout

| Path | What |
|---|---|
| `AGENTS.md` | Rules for any model working here (read first) |
| `REGISTER-activity.jsonl` | One row per activity per model: when, where, status, page link |
| `skills/` | Shared skills every model may use (same files for everyone) |
| `activities/<yymmdd>-<nnn>-<slug>/` | One activity: its spec, handover prompt, and `lanes/<model>/` |

## Activities

| Id | What | Lanes |
|---|---|---|
| [261124-001](activities/261124-001-race-StbUAJvivDc/) | Race: a YouTube Short (StbUAJvivDc) turned into a knowledge bundle (expert graph, feature docs, presentation method) | grok-bot · codex · claude (later) |
