"""Verify public unauthenticated HTML, local link targets and source byte equality."""
import pathlib,json,urllib.request,hashlib,html.parser,datetime
P=pathlib.Path(__file__).resolve().parents[1];u='https://hm-chaimpion.github.io/mobile-shared-activity/activities/261124-001-race-StbUAJvivDc/lanes/codex/'
r=urllib.request.urlopen(u,timeout=25);body=r.read();local=(P/'index.html').read_bytes()
class Links(html.parser.HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.external_assets=[]
 def handle_starttag(self,t,a):
  d=dict(a)
  if t=='a' and 'href' in d:self.links.append(d['href'])
  if t in ('script','img','link') and (d.get('src') or d.get('href')):self.external_assets.append(d.get('src') or d.get('href'))
x=Links();x.feed(body.decode());broken=[l for l in x.links if not l.startswith(('https:','#')) and not (P/l).is_file()];o={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'url':u,'http_status':r.status,'authentication':'none; urllib default opener, no cookies','byte_match':body==local,'sha256':hashlib.sha256(body).hexdigest(),'broken_local_targets':broken,'external_assets':x.external_assets,'pass':r.status==200 and body==local and not broken and not x.external_assets};print(json.dumps(o,indent=2));raise SystemExit(not o['pass'])
