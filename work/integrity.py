#!/usr/bin/env python3
"""Integrity check on the built pulse-ortho-complete.html.

Extracts QUESTIONS / UNITS / CHAPTERS by evaluating them in node, then checks:
- every unit's qs ids exist and are in order, contiguous coverage per chapter
- CHAPTERS live flags match chapters that actually have questions
- per-chapter question counts are sane (>= 60)
Usage: python3 work/integrity.py [pulse-ortho-complete.html]
"""
import json, re, subprocess, sys

HTML = sys.argv[1] if len(sys.argv) > 1 else "pulse-ortho-complete.html"
h = open(HTML, encoding="utf-8").read()
m = re.search(r"<script>(.*?)</script>\s*</body>", h, re.S)
js = m.group(1)

# pull out just the three arrays and evaluate them
grab = []
for name in ("QUESTIONS", "UNITS", "CHAPTERS"):
    i = js.find(f"const {name} = [")
    j = js.find("];", i)
    grab.append(js[i:j + 1])
    js = js[:i] + "/*removed*/" + js[j + 1:]

probe = grab + ["""
const out = {};
out.nq = QUESTIONS.length;
out.nu = UNITS.length;
out.qids = QUESTIONS.map(q => q.id);
out.uids = UNITS.map(u => u.id);
out.badUnitRefs = [];
UNITS.forEach(u => u.qs.forEach(id => {
  const i = out.qids.indexOf(id);
  if (i < 0) out.badUnitRefs.push(u.id + ' -> ' + id);
}));
const byCh = {};
QUESTIONS.forEach(q => { const c = q.id.match(/ORTHO-C(\\d+)-/)[1]; (byCh[c] = byCh[c] || []).push(q.id); });
out.byChCounts = {};
Object.keys(byCh).forEach(c => out.byChCounts[c] = byCh[c].length);
out.coverage = [];
Object.keys(byCh).forEach(c => {
  const ids = byCh[c];
  const got = [];
  UNITS.filter(u => u.ch == c).forEach(u => got.push(...u.qs));
  if (JSON.stringify(got) !== JSON.stringify(ids)) out.coverage.push('ch' + c + ' mismatch');
});
out.live = CHAPTERS.filter(c => c.live).map(c => c.n);
out.chWithQ = Object.keys(byCh).map(Number).sort((a,b)=>a-b);
console.log(JSON.stringify(out));
"""]
import tempfile, os
with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
    f.write("\n".join(probe)); tmp = f.name
try:
    r = subprocess.run(["node", tmp], capture_output=True, text=True)
finally:
    os.unlink(tmp)
if r.returncode != 0:
    print(r.stderr); sys.exit(1)
o = json.loads(r.stdout)

print("questions:", o["nq"], "| units:", o["nu"])
print("per-chapter:", o["byChCounts"])
print("live chapters:  ", o["live"])
print("chapters w/ qs:", o["chWithQ"])
assert o["nq"] == len(set(o["qids"])), "duplicate question ids!"
assert o["nu"] == len(set(o["uids"])), "duplicate unit ids!"
assert not o["badUnitRefs"], f"unit refs missing: {o['badUnitRefs'][:5]}"
assert not o["coverage"], f"coverage: {o['coverage']}"
assert o["live"] == o["chWithQ"], "live flags != chapters with questions"
for c, n in o["byChCounts"].items():
    assert n >= 60, f"ch{c} has only {n} questions"
print("INTEGRITY PASS ✓")
