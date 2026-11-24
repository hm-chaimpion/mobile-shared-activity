#!/usr/bin/env python3
"""Check nonempty graph, URL-to-saved-source provenance, ids, types and edge evidence.
Usage: python check_knowledge_graph.py lane/knowledge-graph-StbUAJvivDc.json
Exit 1 on broken evidence. Does not establish semantic truth or link availability.
"""
import json,pathlib,sys,urllib.parse,datetime

def check(path):
 path=pathlib.Path(path);base=path.parent.resolve();g=json.loads(path.read_text());errors=[];ids=set();urls=set()
 if not g.get('nodes'):errors.append('no nodes')
 def source(rel,url=None):
  if not rel:return 'missing source_file'
  p=(base/rel).resolve()
  if not p.is_relative_to(base):return 'source escapes lane'
  if not p.is_file():return 'source missing: '+rel
  text=p.read_text()
  if len(text.split('\n\n',1)[-1].strip())<20:return 'empty source body: '+rel
  if url and ('URL: '+url+'\n') not in text:return 'URL not recorded in source header: '+url
 for n in g.get('nodes',[]):
  if n.get('id') in ids:errors.append('duplicate id: '+str(n.get('id')))
  ids.add(n.get('id'));u=n.get('url','');urls.add(u)
  if urllib.parse.urlparse(u).scheme!='https':errors.append('invalid URL: '+u)
  if n.get('type') not in ('person','org','work','feature','doc','concept'):errors.append('invalid type')
  try:datetime.datetime.fromisoformat(n['retrieved_at'].replace('Z','+00:00'))
  except Exception:errors.append('invalid retrieved_at')
  e=source(n.get('source_file'),u)
  if e:errors.append(e)
 for e in g.get('edges',[]):
  if e.get('from') not in ids or e.get('to') not in ids:errors.append('dangling edge')
  if not e.get('relation'):errors.append('missing relation')
  err=source(e.get('source_file'))
  if err:errors.append(err)
 return {'pass':not errors,'nodes':len(ids),'unique_urls':len(urls),'edges':len(g.get('edges',[])),'errors':errors,'scope':'structural provenance, not semantic verification'}
if __name__=='__main__':
 r=check(sys.argv[1]);print(json.dumps(r,indent=2));sys.exit(0 if r['pass'] else 1)
