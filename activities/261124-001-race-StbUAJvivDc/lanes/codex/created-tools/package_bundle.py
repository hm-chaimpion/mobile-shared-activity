"""Create a deterministic manifest and one review ZIP. No caches or recursive archives.
Usage from repo root: python activities/.../lanes/codex/created-tools/package_bundle.py
"""
import pathlib,hashlib,json,zipfile,datetime
P=pathlib.Path(__file__).resolve().parents[1];files=[f for f in sorted(P.rglob('*')) if f.is_file() and '__pycache__' not in str(f) and f.suffix!='.zip' and f.name!='MANIFEST-codex.json'];rows=[{'path':str(f.relative_to(P)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in files];(P/'MANIFEST-codex.json').write_text(json.dumps({'author':'ChatGPT Codex','co_author':'Hamish McGregor','source_surface':'chatgpt','created':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'All lane files except caches, archive itself and manifest self-hash','files':rows},indent=2));dest=P/'261124-006-codex-review-bundle.zip'
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED) as z:
 for f in files+[P/'MANIFEST-codex.json']:z.write(f,str(f.relative_to(P)))
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None
 for r in rows:assert hashlib.sha256(z.read(r['path'])).hexdigest()==r['sha256']
print(json.dumps({'zip':dest.name,'files':len(rows)+1,'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'crc_and_manifest_pass':True}))
