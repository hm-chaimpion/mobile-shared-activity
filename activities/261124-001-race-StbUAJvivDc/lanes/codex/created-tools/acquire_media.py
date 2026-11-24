"""Try public media and captions advertised by YouTube's public player. No cookies."""
import json,re,pathlib,urllib.request,subprocess,datetime
p=pathlib.Path('activities/261124-001-race-StbUAJvivDc/lanes/codex');s=pathlib.Path('/tmp/race-youtube.html').read_text();j=json.JSONDecoder().raw_decode(s[re.search(r'var ytInitialPlayerResponse\s*=\s*',s).end():])[0]
for label,url,dest in [('public_mp4',j['streamingData']['formats'][0]['url'],'/tmp/race-video.mp4'),('captions',next(t['baseUrl'] for t in j['captions']['playerCaptionsTracklistRenderer']['captionTracks'] if t['languageCode']=='en')+'&fmt=srv3','/tmp/race-captions.xml')]:
 try:
  b=urllib.request.urlopen(url,timeout=30).read();pathlib.Path(dest).write_bytes(b);print(label,len(b))
 except Exception as e: print(label,type(e).__name__,str(e))
if pathlib.Path('/tmp/race-video.mp4').exists():
 fd=p/'frames-StbUAJvivDc';fd.mkdir(exist_ok=True)
 r=subprocess.run(['ffmpeg','-loglevel','error','-i','/tmp/race-video.mp4','-vf','fps=1','-q:v','5',str(fd/'frame-%04d.jpg')],capture_output=True,text=True);print('ffmpeg',r.returncode,r.stderr[:300])
