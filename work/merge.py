#!/usr/bin/env python3
"""Merge data/chNN.json chapter files into pulse-ortho-complete.html.

- Base HTML: whatever is at workspace root `pulse-ortho-complete.html`
  (if missing, falls back to newest uploads/pulse-ortho-complete*.html).
- Detects chapters already embedded, appends any data/chNN.json with a higher
  chapter number (ascending), flips CHAPTERS live flags, rewrites
  data/chapters_live.json.
- Idempotent: running twice changes nothing.

Usage: python3 work/merge.py pulse-ortho-complete.html
"""
import glob, json, os, re, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "pulse-ortho-complete.html"

def base_html():
    if os.path.exists(OUT):
        return OUT
    cands = sorted(glob.glob("uploads/pulse-ortho-complete*.html"))
    if not cands:
        sys.exit("no base HTML found")
    return cands[-1]

def compact(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))

src = base_html()
h = open(src, encoding="utf-8").read()

# ---- locate the three arrays -------------------------------------------
q_start = h.find("const QUESTIONS = [")
u_decl = h.find("const UNITS = [")
c_decl = h.find("const CHAPTERS = [")
assert -1 not in (q_start, u_decl, c_decl), "array anchors not found"
q_end = h.rfind("];", q_start, u_decl)          # index of ']' closing QUESTIONS
u_end = h.rfind("];", u_decl, c_decl)           # index of ']' closing UNITS
assert q_end > q_start and u_end > u_decl

# ---- chapters already embedded ------------------------------------------
emb = sorted(set(int(x) for x in re.findall(r"ORTHO-C(\d+)-\d+", h[q_start:u_end])))
print(f"base: {src}  embedded chapters: {emb}")

# ---- new chapter data ----------------------------------------------------
news = []
for f in sorted(glob.glob("data/ch[0-9]*.json"),
                key=lambda p: int(re.search(r"ch(\d+)", p).group(1))):
    ch = int(re.search(r"ch(\d+)", f).group(1))
    if ch in emb or ch <= max(emb, default=0):
        continue
    d = json.load(open(f, encoding="utf-8"))
    news.append((ch, d))
    print(f"merging ch{ch}: {len(d['questions'])} qs, {len(d['units'])} units")

q_add = ("," + ",".join(compact(q) for _, d in news for q in d["questions"])) if news else ""
u_add = ("," + ",".join(compact(u) for _, d in news for u in d["units"])) if news else ""

# splice: do UNITS first (later offset), then QUESTIONS, then CHAPTERS flags
h2 = h[:u_end] + u_add + h[u_end:]
q_end2 = q_end
h2 = h2[:q_end2] + q_add + h2[q_end2:]

# ---- CHAPTERS live flags -------------------------------------------------
live_set = set(emb) | {ch for ch, _ in news}
c_s = h2.find("const CHAPTERS = [")
c_e = h2.find("];", c_s)
block = h2[c_s:c_e]
def fix(m):
    n = int(m.group(1))
    body = m.group(0)
    if n in live_set and "live:true" not in body:
        body = body[:-1] + ",live:true}" + (";" if body.endswith("];") else "")
    return body
block2 = re.sub(r"\{n:(\d+),[^{}]*\}", fix, block)
h2 = h2[:c_s] + block2 + h2[c_e:]

open(OUT, "w", encoding="utf-8").write(h2)

# ---- bookkeeping -----------------------------------------------------------
json.dump(sorted(live_set), open("data/chapters_live.json", "w"))
tq = len(re.findall(r"ORTHO-C\d+-\d+\",", h2[:u_decl + 200])) # rough
nq = len(set(re.findall(r'"id":"ORTHO-C\d+-\d+"', h2)))
nu = len(set(re.findall(r'"id":"ORTHO-U\d+', h2)))
print(f"written {OUT}: ~{nq} question ids, ~{nu} unit ids, live={sorted(live_set)}")
