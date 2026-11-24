"""Create checklist, decisions, tools and run report without changing earlier editions."""
import pathlib,json,datetime,hashlib
P=pathlib.Path('activities/261124-001-race-StbUAJvivDc/lanes/codex');now=datetime.datetime.now(datetime.timezone.utc).isoformat()
rows=[('done','integrity-skills-codex.json','Bundle and seven hashes match spec; start anchor corrected in timing file'),('done','metadata-StbUAJvivDc.json','Public HTML metadata recovered after yt-dlp failure'),('blocked','transcript-status-StbUAJvivDc.json','Bot-check; timedtext zero bytes. Fix: permitted caption/media access'),('blocked','BLOCKED-StbUAJvivDc.md','Public media HTTP 403. Fix: legitimately downloadable video'),('blocked','visual-layer-StbUAJvivDc.md','No frames to OCR; do not manufacture empty OCR evidence'),('done','BLOCKED-audio-StbUAJvivDc.md','Provided audio route attempted early; no Whisper. No audio verified; fix: install Whisper and obtain permitted media'),('done','first-answer-time-codex.json','First answer is explicitly provisional and description-based'),('blocked','coverage-check-result.json','Supplied graph gate passes empty graph; substantive video graph remains blocked'),('blocked','coverage-check-result.json','Zero checked spoken quotes; supplied empty-input pass is vacuous'),('done','sources/felix-post.txt','Expert identified from his own bio'),('blocked','words-versus-sources-StbUAJvivDc.md','Original post saved; publisher-description comparison complete; narrator comparison blocked by absent transcript'),('done','knowledge-graph-StbUAJvivDc.json','All entities identifiable in publisher description/Range section have saved evidence; no claim of complete speech coverage'),('done','feature-docs-StbUAJvivDc.md','General capability mapped; implementation confidence explicit; two official docs saved'),('done','knowledge-check-result.json','13 nodes, 13 edges, seven distinct graph URLs; checker passes'),('done','exact-quotes-result.json','Five written quotes pass supplied normalised and added literal match'),('done','method-card-StbUAJvivDc.md','Worked example and model-neutral prompt; adaptations labelled'),('done','DERIVATIVES-StbUAJvivDc.md','Seven ideas with audience and estimated effort'),('blocked','publication-status-codex.json','Self-contained page created; Pages URL returns404. Fix: repository Pages publishing/admin configuration'),('done','TOOLS-codex.md','Tools saved, tests recorded, decisions and time logs present; early step timing retrospective'),('done','proof-StbUAJvivDc.json','Current mechanical proof; delivery through connected GitHub attempted separately. This item becomes done only when remote write succeeds; see delivery receipt')]
with (P/'CHECKLIST-codex.jsonl').open('w') as f:
 for i,(status,evidence,note) in enumerate(rows,1):f.write(json.dumps({'id':f'C{i:02d}','status':status,'evidence':evidence,'at':now,'note':note})+'\n')
counts={s:sum(r[0]==s for r in rows) for s in ['done','blocked','skipped']}
first=json.loads((P/'first-answer-time-codex.json').read_text())['first_answer_at'];anchor='2026-11-24T08:40:34.977256+00:00';seconds=(datetime.datetime.fromisoformat(first)-datetime.datetime.fromisoformat(anchor)).total_seconds()
(P/'timing-correction-codex.json').write_text(json.dumps({'anchor':anchor,'anchor_basis':'measured filesystem birth time of .git, clone beginning; excludes initial response/discovery','first_answer_at':first,'seconds_anchor_to_first_answer':seconds,'task_start':'unknown; not measured at initial user instruction','supersedes':'LOG-codex.jsonl initial retrospective 08:39:30Z estimate is not reliable; use this anchor','tokens':None,'usd':None,'as_of':now},indent=2))
(P/'publication-status-codex.json').write_text(json.dumps({'at':now,'url':'https://hm-chaimpion.github.io/mobile-shared-activity/activities/261124-001-race-StbUAJvivDc/lanes/codex/','http_status':404,'status':'blocked','shell_push':'no GitHub username/credential; use connected GitHub write tools','pages_api':'unauthenticated GET /pages returned404; does not establish exact cause','fix':'Enable/configure Pages from main/root with repository administration access; no files outside lane changed'},indent=2))
decisions=[('Keep earliest ANSWER immutable; add v02','Rewrite first answer','Preserve speed evidence and add-only versions'),('Use mandated spec filenames','YYMMDD reply naming','Activity contract needs comparable fixed names'),('Use publisher description as separate evidence class','Call it narrator transcript','Description is not audio; never invent timestamps'),('Leave video graph and timed transcript empty with blocked sidecar','Populate speech nodes from description','No independent time/word evidence'),('Add nonempty coverage gate','Accept supplied empty-input pass as verified','Prevent false success from vacuous checks'),('Use 13-node expert graph, separate from video graph','Present research graph as on-screen diagram','Keep source provenance and reconstruction distinct'),('Map general multi-agent capability to subagents with confidence','Assert agent teams uniquely required','Original offers multiple approaches'),('Compare description to post, mark narrator comparison blocked','Claim full words-versus-speech fidelity','Cannot audit absent speech'),('Fetch all primary text and check literal excerpts','Use search snippets as full saved sources','Make verification reproducible'),('Treat fictional worked example and estimates as adaptations','Attribute them to Felix','Avoid invented source claims'),('Exclude affiliate promotion entities from expert graph','Expand promotional links into method citations','Not part of presentation advice; original description retained'),('Do not install Whisper after media blocked','Download model before obtaining audio','Would not unlock transcription without accessible audio'),('Retain empty generated diagram and clearly label it','Invent visual layer','Missing evidence does not imply no diagram'),('Use connected GitHub write route after shell auth failed','Stop at local commit','User authorised public repository delivery'),('Do not change files outside lane to configure hosting','Add repository workflow','Lane-only restriction; report Pages blocker'),('Exclude generated Python bytecode from remote payload','Ship accidental cache','Not a source artefact; local commit contained cache, remote tree omits it')]
with (P/'DECISIONS-codex.jsonl').open('a') as f:
 for choice,alternative,why in decisions:f.write(json.dumps({'at':now,'recording_basis':'retrospective decision record','decision':choice,'alternatives':[alternative],'why':why})+'\n')
with (P/'LOG-codex.jsonl').open('a') as f:
 f.write(json.dumps({'at':now,'event':'timing-correction','step':'race clock','basis':'measured filesystem anchor; see timing-correction-codex.json','tokens':None,'cost':None})+'\n')
 for step,file in [('metadata fallback','metadata-StbUAJvivDc.json'),('first answer','ANSWER-StbUAJvivDc.md'),('source acquisition','sources-inventory-codex.json'),('research bundle','page-data-codex.json'),('page build','index.html')]:
  end=datetime.datetime.fromtimestamp((P/file).stat().st_mtime,datetime.timezone.utc).isoformat()
  f.write(json.dumps({'at':end,'event':'end','step':step,'basis':'retrospective measured file mtime; start not captured','tokens':None,'cost':None})+'\n')
tools=[]
for f in sorted((P/'created-tools').glob('*.py')):
 tools.append(f'| {f.name} | {f.read_text().splitlines()[0].strip(chr(34))[:100]} | '+('Executed; results in lane' if f.name!='finalise_audit.py' else 'Executed to create these records')+' |')
front='---\ncreated: 2026-11-24\nsource_surface: chatgpt\nmodel: GPT-6\nauthor: ChatGPT Codex\nco_author: Hamish McGregor\n---\n\n'
(P/'TOOLS-codex.md').write_text(front+'## Created tools\n\nRun from repository root with Python 3.12. Pass the lane path to check scripts. build_page.py additionally uses the markdown package. Source and media tools use only public endpoints, never credentials. fetch_sources.py handles independent requests concurrently.\n\n| Tool | Purpose | Test status |\n|---|---|---|\n'+'\n'.join(tools)+'\n\ncheck_knowledge_graph.py has negative tests for empty/missing-source graphs. The supplied quote gate rejects an invented fixture; the added coverage checker fails the actual incomplete bundle as intended. No live multi-agent product execution was tested. Public media acquisition is tested and blocked, not successful.\n\nRe-run: `python created-tools/check_knowledge_graph.py knowledge-graph-StbUAJvivDc.json` from the lane, or use full lane paths from repo root. `python created-tools/check_bundle_coverage.py .` must currently exit 1. Do not rerun build generators over an immutable edition; copy to a new version first.\n\nreply: 5; conversation_url: unavailable; project_id: 261124-001\n')
hashes=json.loads((P/'integrity-skills-codex.json').read_text())
(P/'RUN-REPORT-codex.md').write_text(front+f'''## Outcome
Source-grounded presentation research bundle delivered to codex lane. Checklist: {counts['done']} done, {counts['blocked']} blocked, 0 skipped. Complete video validation is not claimed. C20's delivery status is established by the subsequent remote receipt, not by this pre-publish report.

## Speed and cost
First provisional answer: {first}. Measured clone anchor to first answer: {seconds:.1f} seconds. Task-start-to-answer is unknown because the initial clock was not captured. The initial start estimate in the log is superseded by timing-correction-codex.json. Final publication timing is in the delivery receipt. Model tokens and dollars are null because telemetry is unavailable. Extraction cost file measures only that script's wall clock, not total race cost.

## Evidence and checks
13 expert graph nodes, 13 edges, seven unique graph URLs, all with saved source files. Seven successful primary-page fetches plus YouTube metadata are saved; the Blender official fetch failed403. The Blender node points to the successfully saved original post, and claims only what that post says. Five short written excerpts (22 words total) pass normalised and literal checks. Three negative regression fixtures pass.

The supplied proof and graph gate exit0 over empty video inputs. This is a known vacuous-pass limitation, not a content verification. The added coverage checker exits1 as intended: no timed speech, no five spoken quotes, no frame evidence. proof_run --check is current against the unchanged first answer, graph and transcript. Research edition v02 is not covered by the supplied spoken-quote proof; it contains no narrator quotations and is supported by written sources.

## Blocks and fixes
- YouTube extraction: latest installed yt-dlp2026.11.23 encountered a bot-check. Public HTML yielded metadata; advertised captions returned zero bytes and media403. Stop media attempts. Fix: permitted media/caption access.
- Audio: supplied route found no Whisper. Installing it alone cannot fix unavailable media.
- Frames/OCR: absent media; no assertion about whether a diagram exists.
- Narrator comparison: impossible without speech. Description-to-post comparison is clearly labelled.
- Pages: requested URL currently404; API404 does not identify exact cause. No authenticated CLI or administration tool was available. Fix: configure repository Pages publishing with administration access.
- Shell push: no credential. Connected GitHub write route is used for final delivery; see receipt.

## Self-score (1–5; not independently judged)
| Lens | Score | Reason |
|---|---|---|
| Result | 2 | Useful method, but major video evidence absent |
| Expert and feature | 4 | Primary sources saved; specific product mapping remains inference |
| Process | 4 | Saved deterministic tools and negative checks; early timing incomplete |
| Visibility | 3 | Polished page and audit route; Pages publication unresolved |
| Independence | 5 | No questions; all blockers explicit with fixes |

## Privacy notes
Public professional names include Felix Rieseberg, Alex Albert, Tom Kelley, Jonathan Littman, Hamish McGregor and entities appearing in saved public pages. Public publisher description retains promotional URLs. Saved source pages include other public names and links. Example business data is fictional; no private client data, credentials, cookies or signed media URLs are included. Creator scripts contain scratch paths such as /tmp/race-youtube.html; no private device path is needed. No attribution was added to git commits.

## Skill hashes
Bundle expected and actual: {hashes['bundle_actual']} (MATCH).

'''+ '\n'.join(f'- `{k}`: `{v}`'+(' (hashed; not run because frames absent)' if k.endswith('ocr_frames.py') else ' (used)') for k,v in hashes['scripts'].items())+'''\n
## Links
- Requested page: https://hm-chaimpion.github.io/mobile-shared-activity/activities/261124-001-race-StbUAJvivDc/lanes/codex/
- Lane: https://github.com/hm-chaimpion/mobile-shared-activity/tree/main/activities/261124-001-race-StbUAJvivDc/lanes/codex
- Primary post: https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/

reply: 5; conversation_url: unavailable; project_id: 261124-001
''')
print(counts)
