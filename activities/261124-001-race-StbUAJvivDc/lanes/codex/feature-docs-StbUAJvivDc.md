---
title: Multi-agent capability and official documentation
created: 2026-11-24
source_surface: chatgpt
model: GPT-6
author: ChatGPT Codex
co_author: Hamish McGregor
---

## Identification
General capability: multi-agent orchestration across specialist tasks. Concrete documented option: Claude Code subagents. Another option: agent teams. These are distinct implementations; the Short's public description and original post do not establish which named feature was intended.

| Capability | How it fits | Confidence |
|---|---|---|
| Subagents | Delegated specialist task with separate context and restricted tools | High as an implementation; medium as the Short's specific reference |
| Agent teams | Coordinated separate sessions | Alternative, not required by the method |
| One model, sequential passes | Can apply disciplines without actual agents | Our portable implementation; not proof of orchestration |

Official documentation fetched on 24 November 2026:
- https://code.claude.com/docs/en/sub-agents — sources/claude-subagents.txt
- https://code.claude.com/docs/en/agent-teams — sources/claude-agent-teams.txt

The saved teams document labels agent teams experimental and disabled by default. Neither a role prompt nor an agent name guarantees the right professional methods. The original post also requires suitable computing tools and access to relevant data. See sources/felix-post.txt. No live Claude execution was tested in this race.

---
reply: 4; conversation_url: unavailable; project_id: 261124-001; lane: codex
