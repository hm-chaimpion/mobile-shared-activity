#!/usr/bin/env python3
"""proof_run.py: run every gate on a run folder and stamp the result, or check the stamp is still current.

Usage:
  python3 proof_run.py <run-dir> <video-id>            run the gates, write proof-<id>.json
  python3 proof_run.py <run-dir> <video-id> --check    fail if ANSWER or graph changed since the last proof

Gates: youtube-process-cloud/quote_gate.py on ANSWER-<id>.md, then graph_gate.py on graph-<id>.json.
The proof records the sha256 of ANSWER, graph and transcript. A new edition with an old proof fails --check:
that is the stale 02-quote-checks.json problem from the ChatGPT run (audit 261124).
Version 0.1, 2026-11-24 (CHaiMPION/cloud-runs-os, whiteboard-video-extract).
"""
import argparse, datetime, hashlib, json, pathlib, re, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
QUOTE_GATE = HERE.parents[1] / "youtube-process-cloud" / "scripts" / "quote_gate.py"


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("run"); ap.add_argument("vid"); ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    run, v = pathlib.Path(a.run), a.vid
    files = {"answer": run / f"ANSWER-{v}.md", "graph": run / f"graph-{v}.json",
             "transcript": run / f"transcript-timed-{v}.jsonl"}
    proof_path = run / f"proof-{v}.json"
    hashes = {k: sha(p) for k, p in files.items()}

    if a.check:
        if not proof_path.exists():
            sys.exit(f"STALE: no {proof_path.name}; run the gates first")
        old = json.loads(proof_path.read_text())
        changed = [k for k in hashes if old.get("sha256", {}).get(k) != hashes[k]]
        if changed or not old.get("pass"):
            print(json.dumps({"current": False, "changed_since_proof": changed, "last_proof_passed": old.get("pass")}))
            sys.exit(1)
        print(json.dumps({"current": True, "proved_at": old.get("at")}))
        return

    missing = [k for k, p in files.items() if not p.exists()]
    if missing:
        sys.exit(f"missing files: {[str(files[k]) for k in missing]}")
    results = {}
    # The quote gate reads any "double-quoted" text as a quote. Fenced blocks (the embedded Mermaid diagram)
    # are labels, not quotes, so gate a copy of the ANSWER without them (tested 261124: 2 false failures).
    body = re.sub(r"```.*?```", " ", files["answer"].read_text(encoding="utf-8"), flags=re.S)
    tmp = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
    tmp.write(body); tmp.close()
    cmds = {
        "quote_gate": [sys.executable, str(QUOTE_GATE), tmp.name, str(files["transcript"])],
        "graph_gate": [sys.executable, str(HERE / "graph_gate.py"), str(files["graph"]), str(files["transcript"]), "--out", str(run)],
    }
    ocr = run / f"ocr-{v}.jsonl"
    if ocr.exists():
        cmds["graph_gate"] += ["--ocr", str(ocr)]
    fr = run / f"frames-{v}"
    if fr.is_dir():
        cmds["graph_gate"] += ["--frames", str(fr)]
    for name, cmd in cmds.items():
        r = subprocess.run(cmd, capture_output=True, text=True)
        results[name] = {"exit": r.returncode, "tail": r.stdout[-1500:] or r.stderr[-800:]}
    pathlib.Path(tmp.name).unlink(missing_ok=True)
    ok = all(x["exit"] == 0 for x in results.values())
    proof = {"video_id": v, "at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
             "pass": ok, "sha256": hashes, "gates": {k: x["exit"] for k, x in results.items()}, "detail": results}
    proof_path.write_text(json.dumps(proof, indent=1, ensure_ascii=False))
    print(json.dumps({"pass": ok, "gates": proof["gates"], "proof": str(proof_path)}))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
