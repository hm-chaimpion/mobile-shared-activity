#!/usr/bin/env python3
"""save_source.py - fetch a public URL (curl, browser UA), keep the raw HTML and write a readable text file
sources/<name>.txt whose header holds name, URL, final URL, HTTP status, fetched time (NZT ISO) and sha256 of raw.
Created by grok-bot 261124 for spec rule: 'Saved text of every page you cite (name, URL, fetched time at the top)'.
Usage: python3 save_source.py <name> <url> [--out sources]   (name = file stem, e.g. src-felix-post)
Exit 0 on HTTP 200 with text, 1 otherwise (a BLOCKED row is printed as JSON).
"""
import argparse, datetime, hashlib, html, json, pathlib, re, subprocess, sys
ap = argparse.ArgumentParser(); ap.add_argument("name"); ap.add_argument("url"); ap.add_argument("--out", default="sources")
a = ap.parse_args(); out = pathlib.Path(a.out); out.mkdir(exist_ok=True)
raw = out / f"{a.name}.raw.html"
p = subprocess.run(["curl", "-sL", "--max-time", "40", "-A", "Mozilla/5.0 (X11; Linux x86_64) Chrome/124 Safari/537.36",
                    "-o", str(raw), "-w", "%{http_code} %{url_effective}", a.url], capture_output=True, text=True)
code, _, final = p.stdout.partition(" ")
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=13))).isoformat(timespec="seconds")
data = raw.read_bytes() if raw.exists() else b""
def to_text(b):
    s = b.decode("utf-8", "replace")
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(s, "html.parser")
        for t in soup(["script", "style", "noscript", "svg"]): t.decompose()
        title = soup.title.get_text(strip=True) if soup.title else ""
        txt = soup.get_text("\n")
    except Exception:
        title = (re.search(r"<title>(.*?)</title>", s, re.S) or [None, ""])[1]
        s = re.sub(r"(?is)<(script|style|noscript|svg).*?</\1>", " ", s)
        txt = html.unescape(re.sub(r"(?s)<[^>]+>", "\n", s))
    lines = [re.sub(r"[ \t\u00a0]+", " ", l).strip() for l in txt.splitlines()]
    return title, "\n".join(l for l in lines if l)
if data[:5] == b"%PDF-":
    import tempfile
    tf = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False); tf.write(data); tf.close()
    body = subprocess.run(["pdftotext", "-layout", tf.name, "-"], capture_output=True, text=True).stdout
    body = "\n".join(re.sub(r"[ \t]+", " ", l).strip() for l in body.splitlines() if l.strip()); title = "(PDF via pdftotext)"
else:
    title, body = to_text(data)
hdr = (f"# SOURCE: {a.name}\n# url: {a.url}\n# final_url: {final}\n# http_status: {code}\n# fetched_at: {now}\n"
       f"# title: {title}\n# raw_sha256: {hashlib.sha256(data).hexdigest()}\n# raw_file: {raw.name}\n# tool: created-tools/save_source.py\n\n")
(out / f"{a.name}.txt").write_text(hdr + body + "\n")
ok = code == "200" and len(body) > 200
print(json.dumps({"name": a.name, "url": a.url, "status": code, "chars": len(body), "title": title, "ok": ok, "fetched_at": now}))
sys.exit(0 if ok else 1)
