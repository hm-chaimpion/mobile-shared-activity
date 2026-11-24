"""Build source-grounded research edition. Does not invent video transcript or frames.
Run once from repo root; existing first answer remains immutable.
"""
import pathlib,json,datetime,html,hashlib
P=pathlib.Path('activities/261124-001-race-StbUAJvivDc/lanes/codex');V='StbUAJvivDc';now=datetime.datetime.now(datetime.timezone.utc).isoformat();inv=json.loads((P/'sources-inventory-codex.json').read_text());sources={r['name']:r for r in inv if 'source_file'in r}
def md(name,title,text):
 (P/name).write_text(f'---\ntitle: {title}\ncreated: 2026-11-24\nsource_surface: chatgpt\nmodel: GPT-6\nauthor: ChatGPT Codex\nco_author: Hamish McGregor\n---\n\n'+text+'\n\n---\nreply: 4; conversation_url: unavailable; project_id: 261124-001; lane: codex\n')
def js(name,obj):(P/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
md(f'ANSWER-v02-{V}.md','Research edition: range for better presentations', '''## Decision first, format second
Use the presentation's intended action to choose the disciplines and checks behind it. This is our synthesis of the publisher's description and Felix Rieseberg's original post, not a verified transcript.

## Expert and original
Felix Rieseberg's personal author bio identifies him as an Anthropic engineering manager who has led Claude.ai, Cowork and Claude Code Desktop. His tutorial was published on 13 October 2026. Its Range section contains the two techniques described by the Short's publisher. Source: sources/felix-post.txt.

## Capability
Multi-agent orchestration is the general capability; Claude Code subagents are a documented implementation. Confidence: high for that general mapping, medium for a specific product match. The post offers multiple implementations and does not require one named feature. Sources: sources/felix-post.txt; sources/claude-subagents.txt; sources/claude-agent-teams.txt.

## Method
Define the audience's decision → express the required actions → choose useful disciplines → specify their real methods and outputs → challenge evidence → assemble the presentation. The last two operational steps are our adaptation.

## Limits
The first answer and this edition are description/post-based. Timed captions, five spoken quotes, audio and frames remain blocked. No visual diagram, timestamp or narrator quotation is asserted. The supplied gates accept empty inputs; our additional coverage gate correctly fails. This is a research bundle with unresolved video evidence, not a fully verified client asset.''')
md(f'feature-docs-{V}.md','Multi-agent capability and official documentation','''## Identification
General capability: multi-agent orchestration across specialist tasks. Concrete documented option: Claude Code subagents. Another option: agent teams. These are distinct implementations; the Short's public description and original post do not establish which named feature was intended.

| Capability | How it fits | Confidence |
|---|---|---|
| Subagents | Delegated specialist task with separate context and restricted tools | High as an implementation; medium as the Short's specific reference |
| Agent teams | Coordinated separate sessions | Alternative, not required by the method |
| One model, sequential passes | Can apply disciplines without actual agents | Our portable implementation; not proof of orchestration |

Official documentation fetched on 24 November 2026:
- https://code.claude.com/docs/en/sub-agents — sources/claude-subagents.txt
- https://code.claude.com/docs/en/agent-teams — sources/claude-agent-teams.txt

The saved teams document labels agent teams experimental and disabled by default. Neither a role prompt nor an agent name guarantees the right professional methods. The original post also requires suitable computing tools and access to relevant data. See sources/felix-post.txt. No live Claude execution was tested in this race.''')
md(f'method-card-{V}.md','Method card: actions then disciplines','''## Purpose and provenance
For presenters who have an output format but need a stronger argument and decision. Adapted from the Range section of Felix Rieseberg's personal post. The operational checklist and example below are our work; they are not a verbatim method prescribed by Anthropic.

## Steps
1. State the audience, decision, time available and source material.
2. Replace the artefact name with observable actions: explain, compare, test, decide.
3. Pick disciplines that improve those actions. Give each a task, input and deliverable.
4. Name a real method for each discipline; reject a change of voice as a substitute.
5. Challenge the strongest claim using an independent check and raw evidence.
6. Integrate the results into the chosen format. Keep uncertainty beside the claim.

Use when a slide deck, memo or report risks becoming a polished container. Start sequentially when independent tasks are small; delegate when separate work and tool access justify the overhead. Our guidance, not a claim that the video states these operating rules.

## Worked example — fictional quarterly review
Audience: an executive committee. Decision: whether to expand a customer onboarding pilot. Time: 20 minutes. Inputs: fictional retention cohorts, interviews and cost data; no client data used here.

| Discipline | Concrete method | Deliverable |
|---|---|---|
| Analyst | Compare cohort retention and check denominators | Reproducible calculation and chart |
| Journalist | Trace each major claim to a primary record | Claim/source ledger |
| Editor | Test each slide title against the decision | Five-part argument outline |
| Forensic accountant | Reconcile pilot cost and reported savings | Exceptions and reconciliation |
| Adversarial reviewer | Test a rival explanation for improvement | Counterargument and missing evidence |

Success: the committee can identify the recommendation, its evidence, its strongest objection and the next decision. This criterion and example are illustrative; no performance benefit was measured.

## Pasteable template
```text
Audience: [who]. Decision: [what]. Time: [limit]. Inputs: [sources].
Describe what this work must achieve using actions rather than an artefact name.
Choose the smallest useful set of disciplines, including a challenger.
For each, specify an actual method, required data, tools and a concrete output.
Apply those methods; do not imitate a persona's voice.
Keep claims, evidence, uncertainty and rival explanations separate.
Use independent checks where possible. State every missing input.
Integrate the findings into [format], and return a claim/source ledger.
```

Source: https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/ (sources/felix-post.txt).''')
md(f'DERIVATIVES-{V}.md','Derivative asset register','''All effort estimates below are our planning estimates, not measured production costs. All derivatives must retain the unresolved video-evidence notice until captions and frames are obtained.

| Asset | Audience | Effort estimate | Inputs / quality check |
|---|---|---|---|
| One-page decision brief | Executives | 20–30 minutes | Method card; ensure adaptation is labelled |
| Workshop exercise | Internal AI champions | 45–60 minutes | Fictional QBR; compare method vs persona prompting |
| Prompt pack | Analysts | 30 minutes | Template; test with a fixed evidence set |
| Reusable skill | Agent builders | 1–2 hours | Task/method/output contract; adversarial fixtures |
| Slide storyboard | Presenters | 45 minutes | Claim ledger; every slide earns a decision role |
| Comparison checklist | Reviewers | 20 minutes | Quote evidence and source inventory |
| Expert explainer | General business readers | 30 minutes | Graph; verify identity and attribution |
''')
md(f'visual-layer-{V}.md','Visual evidence remains blocked','''No frame evidence was obtained. Direct public player media returned HTTP 403; yt-dlp encountered a bot-check. Therefore we cannot say whether the video contains a diagram, screenshots, text overlays or b-roll. We do not equate missing frames with absence of a diagram.

The Mermaid file is an empty reconstruction generated by the supplied renderer from the empty evidence graph. It is not a representation of the video's visuals. The expert relationship table in the page is a research projection from the separate knowledge graph, with portable JSON alongside it.

Fix: provide a legitimately downloadable media copy or run the supplied extractor in an environment where YouTube permits access. Then extract frames with real timestamps, OCR, visually review, populate the video graph and rerun every gate.''')
post=sources['felix-post']['url']
qs=['Drawing on multiple fields','replace the nouns with verbs','bring in additional fields','a journalist, and an editor','to research their position']
md(f'quotes-sources-{V}.md','Checked written-source excerpts','\n\n'.join(f'URL: {post}\nSource: sources/felix-post.txt\n\n> {q}' for q in qs)+'\n\nThese five excerpts are written-source quotes only. They are not verified narrator speech. Combined quoted words from this source: 22.')
md(f'words-versus-sources-{V}.md','Publisher description versus original source','''## Scope
Narrator-to-source comparison is blocked because speech was not recovered. This table compares the publisher's public description to the original post instead. It must not be represented as a word-for-word audio check. Exact short original excerpts are in quotes-sources-StbUAJvivDc.md and pass the provided written quote gate.

| Publisher description | Original post | Assessment |
|---|---|---|
| Describes Range as drawing on multiple fields | Range is one of four types of ambition | Faithful focus; the Short narrows the full article |
| Credits the noun-to-verb trick to Kelley and Littman | Same attribution in Range | Attribution matches; the book itself was not checked for this passage |
| Lists analyst, journalist, editor, designers, short seller and forensic accountant | Same crew in Range | List matches the post; examples are illustrative professions, not identified people |
| Links Alex Albert, Blender and the homepage inspiration | Same anecdote in Range | Post corroborates anecdote; actual Blender work not independently recovered |
| Warns against role play | Same distinction between methods and persona style | Faithful at description level |
| Says advice is personal and model-independent | Author says he primarily uses Claude but advice is not model-specific | Supported; do not present as Anthropic policy |

Sources: sources/youtube-page.txt and sources/felix-post.txt. No statement here establishes the exact narrator wording or timing.''')
# No counterfeit captions. Empty file has an explicit, machine-readable status sidecar.
(P/f'transcript-timed-{V}.jsonl').write_text('')
js(f'transcript-status-{V}.json',{'status':'blocked','segments':0,'not_a_transcript':True,'reason':'YouTube bot-check; public timedtext returned zero bytes','fix':'Legitimate media/caption access, then rerun extraction'})
js(f'graph-{V}.json',{'video_id':V,'source_url':'https://www.youtube.com/shorts/'+V,'status':'blocked','reason':'No timed speech or frames recovered; do not infer visuals','steps':[],'nodes':[],'edges':[],'quotes':[],'onion':{'status':'blocked: no evidenced video reconstruction','layers':[]}})
nodes=[]
def node(id,label,type,key,note):
 r=sources[key];nodes.append({'id':id,'label':label,'type':type,'url':r['url'],'source_file':r['source_file'],'retrieved_at':r['retrieved_at'],'evidence_note':note})
node('felix','Felix Rieseberg','person','felix-post','Author bio identifies Anthropic EM and engineering areas')
node('anthropic','Anthropic','org','anthropic-about','Company self-description; employment edge supported by Felix bio')
node('tutorial','How to be more ambitious: A tutorial for humans with models','work','felix-post','Title, date and Range section')
node('range','Range','concept','felix-post','One of four named types of ambition')
node('tom','Tom Kelley','person','innovation-book','Publisher identifies author')
node('jonathan','Jonathan Littman','person','felix-post','Original post credits the book to Kelley and Littman; publisher URL also names Littman')
node('book','The Art of Innovation','work','innovation-book','Publisher book record; no full-text verification of the technique')
node('alex','Alex Albert','person','alex-profile','Self-description: Claude Relations at Anthropic')
node('blender','Blender','work','felix-post','Software cited in Alex Albert anecdote; official site fetch blocked')
node('homepage','Felix Rieseberg homepage','work','felix-home','Homepage fetched as text; 3D functionality not visually tested')
node('subagents','Claude Code subagents','feature','claude-subagents','Documented implementation of general multi-agent capability; mapping is our inference')
node('subagent-doc','Create custom subagents','doc','claude-subagents','Official documentation')
node('teams','Claude Code agent teams','feature','claude-agent-teams','Alternative coordinated-session implementation; experimental in saved docs')
edges=[]
def edge(a,b,rel,key,inference=False):edges.append({'from':a,'to':b,'relation':rel,'source_file':sources[key]['source_file'],'inference':inference})
for a,b,rel,key,infer in [('felix','anthropic','works at','felix-post',False),('felix','tutorial','authored','felix-post',False),('tutorial','range','defines','felix-post',False),('tutorial','book','credits noun-to-verb trick to','felix-post',False),('tom','book','author','innovation-book',False),('jonathan','book','credited collaborator','felix-post',False),('felix','alex','describes as colleague','felix-post',False),('alex','anthropic','works at','alex-profile',False),('alex','blender','used for interior rendering according to Felix','felix-post',False),('blender','homepage','inspired 3D environment according to Felix','felix-post',False),('subagent-doc','subagents','documents','claude-subagents',False),('range','subagents','can be implemented using','claude-subagents',True),('range','teams','can be implemented using','claude-agent-teams',True)]:edge(a,b,rel,key,infer)
js(f'knowledge-graph-{V}.json',{'scope':'People, works and organisations in publisher description and corresponding Range section; not every reference elsewhere in full tutorial','nodes':nodes,'edges':edges,'author':'ChatGPT Codex','co_author':'Hamish McGregor','created':now})
# deterministic index projection data for subsequent page builder
js('page-data-codex.json',{'title':'Better presentations begin with better actions','subtitle':'Felix Rieseberg · Range · Methods before personas','status':'Research checked. Video evidence blocked.','nodes':nodes,'edges':edges,'sources':list(sources.values()),'created':now})
print('Built research edition and 13-node expert graph')
