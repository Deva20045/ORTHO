# PULSE · Orthopaedics — Marrow Edition 8 Companion

Single-file quiz app (`pulse-ortho-complete.html`) being extended chapter-by-chapter,
line-by-line from the Marrow Ortho E8 book (24 chapters total).

**Live: 15/24 chapters · 1957 questions · 254 units** (ch 1–15).

## Repo layout
```
pulse-ortho-complete.html   ← the deliverable app (open in any browser)
data/chNN.json              ← per-chapter source data {questions, units}
data/chapters_live.json     ← list of chapters merged into the app
work/render.py              ← render book pages from source PDFs to PNG
work/validate.py            ← schema validator for data/chNN.json
work/merge.py               ← merge data into the HTML (idempotent)
work/integrity.py           ← post-merge integrity check (node-backed)
PROGRESS.md                 ← memory / single source of truth for continuation
```

## Continue work (new session)
1. Say **"continue"** and paste your GitHub username + PAT (repo is private).
2. `git clone https://<PAT>@github.com/<user>/<repo>.git`
3. Read `PROGRESS.md` → it lists the NEXT chapter and the exact pipeline.
4. Upload the required part of the source PDF when asked, then run the pipeline
   (render → transcribe → data/chNN.json → validate → merge → integrity → commit+push).

## Schema contract (see PROGRESS.md for full detail)
- Question: `{id:"ORTHO-C{ch}-{nnn}", sec, page, q, opts[4], ans, exp}` — exp ends `(Book pX)`.
- Unit: `{id:"ORTHO-U{ch}-{n}", ch, n, title, sec:"<Heading> · p<page>", qs:[...], guide}`.
- Units cover every question exactly once, strictly in book order.

## Checks before shipping a chapter
```bash
python3 work/validate.py data/chNN.json
python3 work/merge.py pulse-ortho-complete.html
python3 work/integrity.py
```
