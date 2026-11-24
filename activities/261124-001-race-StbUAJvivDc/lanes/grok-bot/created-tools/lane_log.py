#!/usr/bin/env python3
"""lane_log.py - append one timestamped JSON row to LOG-/DECISIONS-/CHECKLIST-grok-bot.jsonl. Created by grok-bot 261124.
Usage:
  lane_log.py log <step> <start|end> [note] [--tokens N --cost USD --basis measured|estimated]
  lane_log.py decision <id> "<chose>" "<alternatives>" "<why>"
  lane_log.py check <C01..C20> <done|blocked|skipped> <evidence> "<note>"
Rows carry ISO time in NZT (+13:00) and a stamp mmdd:[NNN] h.mmam/pm NZT (NNN = running row number in that file)."""
import datetime, json, pathlib, sys
tz = datetime.timezone(datetime.timedelta(hours=13)); now = datetime.datetime.now(tz)
kind, args = sys.argv[1], sys.argv[2:]
fn = {"log": "LOG-grok-bot.jsonl", "decision": "DECISIONS-grok-bot.jsonl", "check": "CHECKLIST-grok-bot.jsonl"}[kind]
p = pathlib.Path(fn); n = (len(p.read_text().splitlines()) if p.exists() else 0) + 1
stamp = f"{now:%m%d}:[{n:03d}] {now.hour % 12 or 12}.{now:%M}{'am' if now.hour < 12 else 'pm'} NZT"
def opt(k):
    return args[args.index(k) + 1] if k in args else None
if kind == "log":
    row = {"at": now.isoformat(timespec="seconds"), "stamp": stamp, "step": args[0], "phase": args[1],
           "note": args[2] if len(args) > 2 and not args[2].startswith("--") else "",
           "tokens": opt("--tokens"), "cost_usd": opt("--cost"), "basis": opt("--basis") or "not visible to the agent: null"}
elif kind == "decision":
    row = {"at": now.isoformat(timespec="seconds"), "stamp": stamp, "id": args[0], "chose": args[1], "alternatives": args[2], "why": args[3]}
else:
    row = {"id": args[0], "status": args[1], "evidence": args[2], "at": now.isoformat(timespec="seconds"), "note": args[3] if len(args) > 3 else "", "stamp": stamp}
with p.open("a") as f: f.write(json.dumps(row, ensure_ascii=False) + "\n")
print(json.dumps(row, ensure_ascii=False))
