# PULSE · Orthopaedics — Marrow Edition 8 Companion

Single-file quiz app (`pulse-ortho-complete.html`) being extended chapter-by-chapter,
line-by-line from the Marrow Ortho E8 book (24 chapters total).

**Live: 16/24 chapters · 2087 questions · 278 units** (ch 1–16).

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

## ▶ Play
**https://deva20045.github.io/ORTHO/** — opens the quiz directly (index.html redirects).

## Continue work (new session)
1. Say **"continue"** in the Arena session — the agent clones this repo
   (`git clone https://github.com/Deva20045/ORTHO.git`, public) and reads PROGRESS.md.
2. GitHub token (Contents: Read and write) is needed only for pushing; ask the user to paste it.
3. Upload the required part of the source PDF when asked, then run the pipeline
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
