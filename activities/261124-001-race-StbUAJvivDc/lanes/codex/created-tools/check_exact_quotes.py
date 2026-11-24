"""Literal written-quote check, supplementing the supplied normalising gate."""
import pathlib,re,json,sys
p=pathlib.Path(sys.argv[1]);q=(p/'quotes-sources-StbUAJvivDc.md').read_text();source=(p/'sources/felix-post.txt').read_text();quotes=re.findall(r'^> (.+)$',q,re.M);rows=[{'quote':x,'literal_match':x in source} for x in quotes];ok=bool(rows) and all(x['literal_match'] for x in rows);print(json.dumps({'pass':ok,'quotes':rows,'source':'sources/felix-post.txt'},indent=2));sys.exit(not ok)
