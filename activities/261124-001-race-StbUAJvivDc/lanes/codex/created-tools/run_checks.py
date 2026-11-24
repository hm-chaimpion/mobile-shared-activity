"""Run supplied gates, coverage and regression checks; save measured logs. Repo root cwd."""
import subprocess,sys,pathlib,datetime,json,tempfile,importlib.util,copy
P=pathlib.Path('activities/261124-001-race-StbUAJvivDc/lanes/codex');V='StbUAJvivDc';S=pathlib.Path('skills/whiteboard-video-extract/scripts');Y=pathlib.Path('skills/youtube-process-cloud/scripts')
def log(event,step,**kw):
 with (P/'LOG-codex.jsonl').open('a') as f:f.write(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'event':event,'step':step,'basis':'measured','tokens':None,'cost':None,**kw})+'\n')
def run(name,args,expected=0):
 log('start',name);r=subprocess.run([sys.executable,*map(str,args)],capture_output=True,text=True);log('end',name,exit=r.returncode);(P/(name+'-result.json')).write_text(json.dumps({'exit':r.returncode,'expected':expected,'as_expected':r.returncode==expected,'stdout':r.stdout,'stderr':r.stderr},indent=2));print(name,r.returncode,'expected',expected);return r
run('knowledge-check',[P/'created-tools/check_knowledge_graph.py',P/f'knowledge-graph-{V}.json'])
run('written-quote-check',[Y/'quote_gate.py',P/f'quotes-sources-{V}.md',P/'sources/felix-post.txt'])
run('provided-proof',[S/'proof_run.py',P,V])
run('provided-proof-current',[S/'proof_run.py',P,V,'--check'])
run('coverage-check',[P/'created-tools/check_bundle_coverage.py',P],1)
# Regression: real negative fixtures prove the added checker and supplied quote gate reject bad input.
spec=importlib.util.spec_from_file_location('kg',P/'created-tools/check_knowledge_graph.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
g=json.loads((P/f'knowledge-graph-{V}.json').read_text());tests=[]
with tempfile.TemporaryDirectory(dir=P) as td:
 t=pathlib.Path(td);f=t/'graph.json';f.write_text(json.dumps({'nodes':[],'edges':[]}));tests.append({'case':'empty knowledge graph','pass':not mod.check(f)['pass']})
 f.write_text(json.dumps({'nodes':[{'id':'x','type':'person','url':'https://example.com/','source_file':'../missing.txt','retrieved_at':'2026-11-24T00:00:00Z'}],'edges':[]}));tests.append({'case':'missing source','pass':not mod.check(f)['pass']})
 q=t/'bad-quote.md';q.write_text('> The moon is made entirely of marmalade custard.');r=subprocess.run([sys.executable,str(Y/'quote_gate.py'),str(q),str(P/'sources/felix-post.txt')],capture_output=True,text=True);tests.append({'case':'invented quote rejected','pass':r.returncode==1})
(P/'regression-checks-codex.json').write_text(json.dumps({'pass':all(t['pass'] for t in tests),'tests':tests},indent=2));print(tests)
