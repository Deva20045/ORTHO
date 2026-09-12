#!/usr/bin/env python3
"""Validator for PULSE Ortho chapter data files.

Schema (must match exactly):
- Question: {id:"ORTHO-C{ch}-{nnn}" sequential per chapter from 001, sec, page(book),
             q, opts[4], ans(idx 0-3), exp ends "(Book pX)"}
- Unit: {id:"ORTHO-U{ch}-{n}" sequential per chapter from 1, ch, n, title,
         sec:"<Heading> · p<page>", qs:[ids contiguous & ordered],
         guide: vivid 2-3 sentence prose}
- Units must cover every question exactly once, in order.

Usage: python3 work/validate.py data/chNN.json [more.json ...]
"""
import json, re, sys

PAGE_MAP = {  # book start-end pages per chapter
    12: (90, 104), 13: (105, 111), 14: (112, 122), 15: (123, 128),
    16: (129, 136), 17: (137, 147), 18: (148, 153), 19: (154, 159),
    20: (160, 165), 21: (166, 172), 22: (173, 180), 23: (181, 189), 24: (190, 202),
}

def fail(msg):
    print("  FAIL:", msg)
    sys.exit(1)

def validate(path):
    print(f"== {path}")
    d = json.load(open(path, encoding="utf-8"))
    qs, units = d["questions"], d["units"]
    if not qs:
        fail("no questions")
    m = re.match(r"ORTHO-C(\d+)-(\d+)", qs[0]["id"])
    ch = int(m.group(1))
    lo, hi = PAGE_MAP.get(ch, (1, 300))

    # ---- questions ----
    for i, q in enumerate(qs, 1):
        if q["id"] != f"ORTHO-C{ch}-{i:03d}":
            fail(f"question order/id: got {q['id']} expected ORTHO-C{ch}-{i:03d}")
        if len(q["opts"]) != 4:
            fail(f"{q['id']}: opts != 4")
        if not (isinstance(q["ans"], int) and 0 <= q["ans"] <= 3):
            fail(f"{q['id']}: bad ans")
        if not (lo <= q["page"] <= hi):
            fail(f"{q['id']}: page {q['page']} outside chapter range {lo}-{hi}")
        if not q["exp"].rstrip().endswith(f"(Book p{q['page']})"):
            fail(f"{q['id']}: exp must end '(Book p{q['page']})' -> ...{q['exp'][-20:]}")
        if not q["q"].strip() or any(not str(o).strip() for o in q["opts"]):
            fail(f"{q['id']}: empty text")
    print(f"  questions OK: {len(qs)} (C{ch}-001 .. C{ch}-{len(qs):03d})")

    # ---- units ----
    covered = []
    for i, u in enumerate(units, 1):
        if u["id"] != f"ORTHO-U{ch}-{i}":
            fail(f"unit order/id: got {u['id']} expected ORTHO-U{ch}-{i}")
        if u["ch"] != ch or u["n"] != i:
            fail(f"{u['id']}: ch/n mismatch")
        if not re.match(r".+ · p\d+$", u["sec"]):
            fail(f"{u['id']}: sec format '{u['sec']}'")
        if not u["qs"] or not u["guide"].strip():
            fail(f"{u['id']}: empty qs/guide")
        covered += u["qs"]
    # units cover every question exactly once, in order
    if covered != [q["id"] for q in qs]:
        want, got = set(q["id"] for q in qs), set(covered)
        missing = [x for x in (q["id"] for q in qs) if x not in got]
        dupes = [x for x in covered if covered.count(x) > 1]
        extra = [x for x in covered if x not in want]
        fail(f"coverage mismatch. missing={missing[:5]} dupes={sorted(set(dupes))[:5]} extra={extra[:5]}")
    print(f"  units OK: {len(units)} cover all {len(qs)} questions in order")
    print(f"  PASS ✓  ({path})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    for p in sys.argv[1:]:
        validate(p)
