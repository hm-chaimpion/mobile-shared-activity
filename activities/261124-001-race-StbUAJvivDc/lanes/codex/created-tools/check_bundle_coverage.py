"""Reject vacuous evidence passes. Usage: python check_bundle_coverage.py LANE."""
import json,pathlib,sys
p=pathlib.Path(sys.argv[1]);v='StbUAJvivDc';rows=[json.loads(l) for l in (p/f'transcript-timed-{v}.jsonl').read_text().splitlines() if l.strip()];g=json.loads((p/f'graph-{v}.json').read_text());fail=[]
if not rows:fail.append('No timed speech: supplied quote gate can pass zero quotes vacuously')
if len([q for q in g.get('quotes',[]) if not q.get('on_screen')])<5:fail.append('Fewer than five checked spoken quotes')
if not g.get('steps'):fail.append('No evidenced timed argument')
if not list((p/f'frames-{v}').glob('*.jpg')):fail.append('No delivered frames; visual layer unverified')
print(json.dumps({'pass':not fail,'failures':fail,'status':'blocked' if fail else 'done'},indent=2));sys.exit(bool(fail))
