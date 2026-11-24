#!/usr/bin/env python3
"""build_knowledge_graph.py - writes knowledge-graph-StbUAJvivDc.json (expert graph) and CLAIMS-StbUAJvivDc.md
(every factual claim with status VERIFIED / UNVERIFIED / NOT FOUND and its saved source). url and retrieved_at are
read from each saved source's header, so they can't drift from the evidence. Created by grok-bot 261124.
Usage: python3 build_knowledge_graph.py <lane>"""
import json, pathlib, re, sys
lane = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
def hdr(sf):
    t = (lane / "sources" / f"{sf}.txt").read_text()
    g = lambda k: (re.search(rf"^# {k}: (.*)$", t, re.M) or [None, None])[1]
    return g("url"), g("fetched_at")
# id, label, type, source_file stem, cited_in (short|post|both|context), note
N = [
 ("felix","Felix Rieseberg","person","src-felix-post","both","EM at Anthropic; author of the post; Electron co-maintainer"),
 ("felix_about","Felix Rieseberg: About Me","doc","src-felix-about","context","his own bio page"),
 ("felix_github","felixrieseberg on GitHub","doc","src-felix-github","context","profile lists Anthropic"),
 ("felix_x","@felixrieseberg on X","doc","src-felix-x","context","linked from the post footer"),
 ("felix_linkedin","Felix Rieseberg on LinkedIn","doc","src-felix-linkedin","context","page title: Felix Rieseberg - Anthropic"),
 ("post","How to be more ambitious: A tutorial for humans with models","work","src-felix-post","both","13 Oct 2026, felixrieseberg.com; the Short's source"),
 ("homepage","felixrieseberg.com homepage (3D room)","work","src-felix-homepage","short","WebGL room; on-screen capture 2026-10-21"),
 ("anthropic","Anthropic","org","src-anthropic-company","both","Felix's and Alex Albert's employer"),
 ("electron","Electron","org","src-electron","context","Felix co-maintains it (post footer)"),
 ("art_innov","The Art of Innovation (Kelley with Littman, 2001)","work","src-art-of-innovation-prh","both","source of the nouns-to-verbs trick"),
 ("art_innov_gb","The Art of Innovation (Google Books record)","doc","src-art-of-innovation-gbooks","context","author bios for Kelley and Littman"),
 ("tom_kelley","Tom Kelley","person","src-art-of-innovation-gbooks","both","general manager of IDEO (publisher bio)"),
 ("littman","Jonathan Littman","person","src-art-of-innovation-gbooks","both","co-author (publisher bio)"),
 ("ideo","IDEO","org","src-wiki-ideo","context","Kelley's firm; subject of the book"),
 ("ideo_page","IDEO page on The Art of Innovation","doc","src-art-of-innovation-ideo","context",""),
 ("alex_albert","Alex Albert","person","src-alex-albert-site","both","Claude Relations at Anthropic (his site)"),
 ("alex_post","Alex Albert X post: house + walkthrough via Blender headless (1 Sep 2026)","work","src-alex-albert-nitter","context","related, not proven to be the renders Felix means"),
 ("blender","Blender","org","src-blender-wiki","both","open-source 3D suite (blender.org returned 403, Wikipedia saved)"),
 ("blender_mcp","Blender MCP connector for Claude","feature","src-anthropic-creative-work","context","official Blender connector (Apr 2026)"),
 ("blender_academy","Using the Blender Connector in Claude (Claude Academy)","doc","src-blender-connector-academy","context",""),
 ("subagents","Claude subagents / multi-agent setups","feature","src-doc-cc-subagents","both","the capability the Range advice relies on"),
 ("sdk_subagents","Subagents in the Agent SDK","doc","src-doc-sdk-subagents","context",""),
 ("agent_teams","Claude Code agent teams","doc","src-doc-cc-agent-teams","context","orchestrated multi-session teams"),
 ("subagents_article","How and when to use subagents in Claude Code","doc","src-doc-subagents-article","context",""),
 ("mcp","Model Context Protocol (MCP connectors)","feature","src-doc-mcp-intro","post","post: model needs a computer + MCP connectors"),
 ("cc_mcp","Connect Claude Code to tools via MCP","doc","src-doc-cc-mcp","context",""),
 ("range","Range (ambition type)","concept","src-felix-post","both","one of Speed, Altitude, Depth, Range"),
 ("verbs","Replace the nouns with verbs","concept","src-felix-post","both","trick 1"),
 ("crew","Assemble the crew","concept","src-felix-post","both","trick 2"),
 ("heist","Heist film","concept","src-wiki-heist-film","both","analogy for assembling a crew"),
 ("red_team","Red team","concept","src-wiki-red-team","both","adversarial crew members"),
 ("short_seller","Short seller","concept","src-wiki-short-selling","both","red-team role"),
 ("forensic","Forensic accountant","concept","src-wiki-forensic-accounting","both","red-team role"),
 ("tao","Terence Tao","person","src-wiki-tao","post","quoted on uneven model capability"),
 ("tao_post","Math 2.0 (Terence Tao blog, 10 Oct 2026)","work","src-tao-math2","post","linked as 'a new era of math'"),
 ("gizmodo","Gizmodo: Did Claude help discover a new planet?","work","src-gizmodo-planet","post",""),
 ("collison","Patrick Collison","person","src-wiki-collison","post","Stripe founder"),
 ("fast","Fast (Patrick Collison list)","work","src-collison-fast","post",""),
 ("locke_latham","Locke and Latham, goal-setting 35-year odyssey","work","src-locke-latham-pdf","post","specific hard goals"),
 ("self_eff","Self-efficacy","concept","src-wiki-self-efficacy","post",""),
 ("bannister","Roger Bannister","person","src-wiki-bannister","post","four-minute mile"),
 ("sawe","Sabastian Sawe","person","src-wiki-sawe","post","sub-two-hour marathon"),
 ("inner_game","The Inner Game of Tennis (Timothy Gallwey)","work","src-wiki-inner-game","post","URL redirects to Timothy Gallwey"),
 ("dantzig","George Dantzig","person","src-wiki-dantzig","post",""),
 ("michelangelo","Michelangelo","person","src-wiki-michelangelo","post",""),
 ("linux","Linux ('just a hobby')","work","src-wiki-linux-history","post",""),
 ("goya","Francisco Goya, Modo de volar","work","src-wiki-goya","post","post image"),
]
E = [("felix","anthropic","works at (EM)","src-felix-post"),("felix","post","wrote","src-felix-post"),("felix","homepage","owns","src-felix-homepage"),
 ("felix","electron","co-maintains","src-felix-post"),("felix_about","felix","describes","src-felix-about"),("felix_github","felix","profile of","src-felix-github"),
 ("felix_x","felix","profile of","src-felix-x"),("felix_linkedin","felix","profile of","src-felix-linkedin"),
 ("post","range","defines","src-felix-post"),("range","verbs","technique","src-felix-post"),("range","crew","technique","src-felix-post"),
 ("post","art_innov","cites as source of trick 1","src-felix-post"),("tom_kelley","art_innov","author of","src-art-of-innovation-prh"),
 ("littman","art_innov","co-author of","src-art-of-innovation-gbooks"),("art_innov_gb","art_innov","catalogue record of","src-art-of-innovation-gbooks"),
 ("tom_kelley","ideo","general manager of","src-art-of-innovation-gbooks"),("ideo_page","art_innov","describes","src-art-of-innovation-ideo"),
 ("crew","heist","analogy","src-felix-post"),("crew","red_team","includes","src-felix-post"),("red_team","short_seller","staffed by","src-felix-post"),
 ("red_team","forensic","staffed by","src-felix-post"),("post","alex_albert","cites colleague","src-felix-post"),("alex_albert","anthropic","works at","src-alex-albert-site"),
 ("alex_albert","blender","used to render interior designs (per Felix)","src-felix-post"),("alex_post","alex_albert","posted by","src-alex-albert-nitter"),
 ("alex_post","blender","uses (headless)","src-alex-albert-nitter"),("blender_mcp","blender","connects Claude to","src-anthropic-creative-work"),
 ("blender_academy","blender_mcp","documents","src-blender-connector-academy"),("homepage","blender","inspired by Alex's Blender renders (per post)","src-felix-post"),
 ("range","subagents","made practical by (multi-agent systems)","src-felix-post"),("sdk_subagents","subagents","documents","src-doc-sdk-subagents"),
 ("agent_teams","subagents","sibling feature","src-doc-cc-agent-teams"),("subagents_article","subagents","explains","src-doc-subagents-article"),
 ("post","mcp","requires (connectors)","src-felix-post"),("cc_mcp","mcp","documents","src-doc-cc-mcp"),
 ("post","tao","quotes","src-felix-post"),("post","tao_post","links","src-felix-post"),("tao_post","tao","written by","src-tao-math2"),
 ("post","gizmodo","links","src-felix-post"),("post","collison","cites","src-felix-post"),("collison","fast","maintains","src-collison-fast"),
 ("post","locke_latham","links","src-felix-post"),("post","self_eff","links","src-felix-post"),("post","bannister","cites","src-felix-post"),
 ("post","sawe","cites","src-felix-post"),("post","inner_game","cites","src-felix-post"),("post","dantzig","cites","src-felix-post"),
 ("post","michelangelo","cites","src-felix-post"),("post","linux","cites","src-felix-post"),("post","goya","image credit","src-felix-post")]
nodes = []
for i, l, t, sf, ci, note in N:
    u, at = hdr(sf); nodes.append({"id": i, "label": l, "type": t, "url": u, "source_file": f"sources/{sf}.txt", "retrieved_at": at, "cited_in": ci, "note": note})
g = {"video_id": "StbUAJvivDc", "expert": "felix", "cited_in_key": "short = said or shown in the Short; post = only in Felix's post; both; context = profile/doc we added to verify",
     "nodes": nodes, "edges": [{"from": a, "to": b, "relation": r, "source_file": f"sources/{s}.txt"} for a, b, r, s in E]}
(lane / "knowledge-graph-StbUAJvivDc.json").write_text(json.dumps(g, indent=1, ensure_ascii=False))
print(json.dumps({"nodes": len(nodes), "edges": len(E)}))
