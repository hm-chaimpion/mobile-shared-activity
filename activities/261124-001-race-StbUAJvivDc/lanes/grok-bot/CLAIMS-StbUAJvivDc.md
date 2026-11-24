# Claims register · StbUAJvivDc

Status key: **VERIFIED** = the exact fact is in a saved source we fetched (file named). **UNVERIFIED** = plausible or partly supported, not proven. **NOT FOUND** = we looked and no source has it. We never guess names or facts.

| # | Claim (who makes it) | Status | Evidence (saved file / gate) |
|---|---|---|---|
| K01 | The Short is *Claude Prompts: Replace the Noun With Verbs, Then Assemble a Crew* by DIY Smart Code, uploaded 2026-10-26, 118 s | VERIFIED | `metadata-StbUAJvivDc.json` (yt-dlp) |
| K02 | The expert is Felix Rieseberg | VERIFIED | named in the narration [00:04], on screen (frame-0005), and as author of the post: `sources/src-felix-post.txt` |
| K03 | He is an engineering manager (EM) at Anthropic | VERIFIED | post author box: *I'm an EM at Anthropic*; `src-felix-about.txt`, `src-felix-linkedin.txt` (title: Felix Rieseberg - Anthropic) |
| K04 | He has led engineering for Claude.ai, Cowork and Claude Code Desktop, and co-maintains Electron | VERIFIED | `src-felix-post.txt` (author box), `src-felix-about.txt` |
| K05 | The original post is *How to be more ambitious: A tutorial for humans with models*, felixrieseberg.com, 13 Oct 2026 | VERIFIED | `src-felix-post.txt`; page meta article:published_time 2026-10-13T14:48:44Z, modified 2026-10-16 |
| K06 | The post defines four kinds of ambition: Speed, Altitude, Depth, Range | VERIFIED | quotes-sources gate |
| K07 | Trick 1 (nouns to verbs) comes from *The Art of Innovation* by Tom Kelley and Jonathan Littman | VERIFIED (the attribution is in the post; the book and authors exist) | `src-felix-post.txt`, `src-art-of-innovation-prh.txt`, `src-art-of-innovation-gbooks.txt` |
| K08 | The nouns-to-verbs trick is actually in that book | UNVERIFIED | the book text was not available; the publisher blurb mentions cross-pollinating from other fields, not the verbs trick |
| K09 | Tom Kelley was general manager of IDEO; Littman is co-author | VERIFIED | `src-art-of-innovation-gbooks.txt` (publisher bios) |
| K10 | Alex Albert is a colleague at Anthropic | VERIFIED | post (*my colleague Alex Albert*); `src-alex-albert-site.txt` (*I handle Claude Relations at Anthropic*) |
| K11 | Alex Albert used Blender to render interior designs | VERIFIED as Felix's statement · UNVERIFIED independently | post; the nearest independent evidence is a house and walkthrough using Blender headless (`src-alex-albert-nitter.txt`, a mirror of X) |
| K12 | Felix's homepage is a 3D room now | VERIFIED | homepage raw HTML has a WebGL room (`?room=1`, *room for the curious*): `src-felix-homepage.raw.html`; On-screen capture dated 2026-10-21 at frame-0084 |
| K13 | Felix has made video games before | VERIFIED as his statement | post |
| K14 | Multi-agent setups (threads, orchestrators, subagents) are the enabling feature | VERIFIED as his statement; product mapping is our inference (confidence stated) | post + `feature-docs-StbUAJvivDc.md` |
| K15 | The advice is not model-specific, and it is personal advice, not Anthropic policy | VERIFIED (not model-specific: post) · the not-policy wording is the video description's | post; `metadata-StbUAJvivDc.json` description |
| K16 | The red team is three members (red team, short seller, forensic accountant) | NOT FOUND as stated | in the post, the short seller and forensic accountant *are* the red team: words-vs-sources P15 |
| K17 | The heist line belongs to trick 2 | Partly: the post puts it in the Range intro and the Short puts it before *Assemble the crew* | words-vs-sources P10 |
| K18 | Ask Claude for a deck and you get a deck (the hook) | NOT FOUND in the post (narrator's line) | words-vs-sources P01 |
| K19 | The narration is accurate to the audio | VERIFIED | Whisper small.en vs captions: 98.2% word similarity, 5 differences, all spelling (`audio-vs-captions-StbUAJvivDc.json`) |
| K20 | The video shows no drawn diagram, only typeset cards over blog screenshots | VERIFIED by inspection | `contact-sheet-StbUAJvivDc.jpg`, OCR of 107 frames |
| K21 | Which product Felix used for the crew | NOT FOUND | post names no product |
