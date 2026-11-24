"""Fallback: parse public YouTube player JSON; never use cookies. Run from repo root."""
import json,re,pathlib,urllib.request,datetime
p=pathlib.Path('activities/261124-001-race-StbUAJvivDc/lanes/codex');s=pathlib.Path('/tmp/race-youtube.html').read_text();d=json.JSONDecoder()
m=re.search(r'var ytInitialPlayerResponse\s*=\s*',s);j=d.raw_decode(s[m.end():])[0];v=j['videoDetails'];now=datetime.datetime.now(datetime.timezone.utc).isoformat()
(p/'sources/youtube-page.txt').write_text('Name: YouTube Short public player metadata\nURL: https://www.youtube.com/shorts/StbUAJvivDc\nFetched: '+now+'\n\n'+json.dumps({'videoDetails':v,'microformat':j.get('microformat')},indent=2))
(p/'metadata-StbUAJvivDc.json').write_text(json.dumps({'id':v['videoId'],'title':v['title'],'channel':v['author'],'duration':v['lengthSeconds'],'description':v['shortDescription'],'microformat':j.get('microformat')},indent=2))
print(v['shortDescription'])
tracks=j['captions']['playerCaptionsTracklistRenderer']['captionTracks'];u=next(t['baseUrl'] for t in tracks if t['languageCode']=='en')+'&fmt=json3'
try:
 b=urllib.request.urlopen(u,timeout=20).read();print('Caption bytes',len(b));(p/'sources/captions-response.txt').write_text('URL: https://www.youtube.com/api/timedtext?v=StbUAJvivDc\nFetched: '+now+'\n\n'+b.decode());c=json.loads(b)
 rows=[]
 for e in c.get('events',[]):
  t=''.join(x.get('utf8','') for x in e.get('segs',[])).strip()
  if t: rows.append({'start':e.get('tStartMs',0)/1000,'end':(e.get('tStartMs',0)+e.get('dDurationMs',0))/1000,'text':t})
 (p/'transcript-timed-StbUAJvivDc.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in rows))
except Exception as e: print(type(e).__name__,str(e))
