# The feature · StbUAJvivDc

**What the Short says (general terms):** [00:17] "Now that multi-agent setups are easier to run, he's seen really interesting results asking Claude to bring in extra fields."

**What the expert wrote (saved post, `sources/src-felix-post.txt`):** he says AI products make it easier to run multi-agent systems, *with multiple threads, orchestrators, or simply subagents*. He adds that every kind of ambition needs the model to have a computer that can install software, and access to data *using MCP connectors or other means*. Exact text and gate result: `quotes-sources-StbUAJvivDc.md`.

## Identification

| Rank | Capability | Official documentation (saved) | Why | Confidence |
|---|---|---|---|---|
| 1 | **Claude subagents.** Specialist workers, each in its own context, that the main agent delegates to. | [Create custom subagents (Claude Code)](https://code.claude.com/docs/en/sub-agents) → `sources/src-doc-cc-subagents.txt`; [Subagents in the SDK](https://code.claude.com/docs/en/agent-sdk/subagents) → `sources/src-doc-sdk-subagents.txt`; [How and when to use subagents](https://claude.com/resources/articles/subagents-in-claude-code) → `sources/src-doc-subagents-article.txt` | The post names *subagents* explicitly. One crew member maps to one subagent with its own instructions and tools, and the SDK runs them in parallel. | **High** that this is the capability the advice relies on. **Medium** on which product surface Felix used: he names none, and he says his advice is not model-specific. |
| 2 | **Agent teams / orchestrators.** A lead session coordinates teammates that message each other. | [Orchestrate teams of Claude Code sessions](https://code.claude.com/docs/en/agent-teams) → `sources/src-doc-cc-agent-teams.txt` | Matches *orchestrators* and *multiple threads*. Teammates can share and challenge each other's findings, which fits the red-team members. | Medium |
| 3 | **MCP connectors + a computer.** A prerequisite, not the crew itself. | [What is MCP](https://modelcontextprotocol.io/introduction) → `sources/src-doc-mcp-intro.txt`; [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp) → `sources/src-doc-cc-mcp.txt` | The post says all ambition types need a computer plus data access through MCP connectors. | High as a prerequisite |
| 4 | **Blender MCP connector.** The 3D example in the Short. | [Claude for Creative Work](https://www.anthropic.com/news/claude-for-creative-work) → `sources/src-anthropic-creative-work.txt`; [Using the Blender Connector in Claude](https://academy.claude.com/tutorials/using-the-blender-connector-in-claude) → `sources/src-blender-connector-academy.txt` | Neither the Short nor the post names it. It is the official route from Claude to Blender. | Low that Alex or Felix used this exact connector (UNVERIFIED). Shown only as how you would reproduce the example. |

## What we did not find
- Felix does not name a product (Claude Code, Cowork, claude.ai) for the crew technique. NOT FOUND in the post.
- No source proves which tool Alex Albert used for the *interior designs* Felix mentions. His 1 Sep 2026 X post shows a house design and walkthrough using *blender headless* (`sources/src-alex-albert-nitter.txt`, a nitter mirror). This is related evidence only.

## How to use the feature for this method (from the docs, not from Felix)
1. Define one subagent per crew role (for example `.claude/agents/short-seller.md`), giving each a *method* to run (what a short seller does to research a position), not a persona voice.
2. Let the main agent delegate in parallel, then merge the findings. Use agent teams when roles must challenge each other.
3. Give the crew the raw data and tools through MCP, as the post's closing paragraph requires.
