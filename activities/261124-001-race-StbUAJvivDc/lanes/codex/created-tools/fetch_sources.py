"""Fetch primary sources as readable UTF-8 with provenance. Run from repo root."""
import urllib.request,html.parser,json,pathlib,datetime,concurrent.futures
P=pathlib.Path('activities/261124-001-race-StbUAJvivDc/lanes/codex')
URLS={'felix-post':'https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/','felix-home':'https://felixrieseberg.com/','alex-profile':'https://alexalbert.me/','innovation-book':'https://www.penguinrandomhouse.com/books/91121/the-art-of-innovation-by-thomas-kelley-with-jonathan-littman/9780307423863/','anthropic-about':'https://www.anthropic.com/company','blender-about':'https://www.blender.org/about/','claude-subagents':'https://code.claude.com/docs/en/sub-agents','claude-agent-teams':'https://code.claude.com/docs/en/agent-teams'}
class Text(html.parser.HTMLParser):
 def __init__(self): super().__init__();self.skip=0;self.parts=[]
 def handle_starttag(self,tag,attrs):
  if tag in ('script','style','svg'):self.skip+=1
  if tag in ('p','div','h1','h2','h3','li','br','section'):self.parts.append('\n')
 def handle_endtag(self,tag):
  if tag in ('script','style','svg'):self.skip=max(0,self.skip-1)
 def handle_data(self,data):
  if not self.skip:self.parts.append(data)
def fetch(item):
 name,url=item;now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 try:
  r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=25);b=r.read();t=Text();t.feed(b.decode('utf-8'));body='\n'.join(' '.join(l.split()) for l in ''.join(t.parts).splitlines() if l.strip());path='sources/'+name+'.txt';(P/path).write_text(f'Name: {name}\nURL: {url}\nFinal URL: {r.url}\nFetched: {now}\nHTTP: {r.status}\n\n'+body);return {'name':name,'url':url,'source_file':path,'retrieved_at':now,'status':r.status,'chars':len(body)}
 except Exception as e:return {'name':name,'url':url,'error':str(e),'retrieved_at':now}
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:rows=list(pool.map(fetch,URLS.items()))
 (P/'sources-inventory-codex.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
