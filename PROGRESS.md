# PULSE Ortho continuation — progress tracker

## Goal
Extend `pulse-ortho-complete.html` (quiz app, Marrow Ortho E8) line-by-line from the
scanned book PDFs until ALL 24 chapters are live. User demands: no quality compromise,
line-by-line questions, first line → last line, strict book order, identical style/schema.

## Sources
- `uploads/Orthopedics Marrow E8-1-100.pdf`  = global pdf pages 1-100  → book pages = pdf-2 (book ≤98)
- `uploads/Orthopedics Marrow E8-101-204.pdf` = global pdf pages 101-204 → book = pdfpage(file2)+98
- Scans have NO text layer → read pages as images (rendered PNGs in work/pages/bNNN.png, 100 dpi).
- **PDFs are NOT stored in this repo (size + copyright). Each new session: ask the user to
  re-upload the PDF part needed for the next chapter.**

## Schema (must match exactly)
- Question: {id:"ORTHO-C{ch}-{nnn}" sequential per chapter from 001, sec, page(book), q, opts[4], ans(idx), exp ends "(Book pX)"}
- Unit: {id:"ORTHO-U{ch}-{n}" sequential per chapter from 1, ch, n, title, sec:"<Heading> · p<page>", qs:[ids contiguous & ordered], guide: vivid 2-3 sentence prose}
- Units must cover every question exactly once, in order.
- Deliverable format inside HTML: `const QUESTIONS = [{...}]`, `const UNITS = [{...}]` (compact JSON, natural key order), `const CHAPTERS = [{n,t,p,live:true}]`.

## Chapter page map (book pages)
12: 90-104 DONE (195 qs, 28 units) | 13: 105-111 DONE (89 qs, 13 units) | 14: 112-122 DONE (108 qs, 13 units) | 15: 123-128 DONE (68 qs, 13 units) | 16: 129-136 DONE (130 qs, 24 units)
17: 137-147 | 18: 148-153 | 19: 154-159 | 20: 160-165 | 21: 166-172 | 22: 173-180 | 23: 181-189 | 24: 190-202
→ ch17 = file2 pdf pages 39-49; ch18 = 50-55; ch19 = 56-61; ch20 = 62-67; ch21 = 68-74; ch22 = 75-82; ch23 = 83-91; ch24 = 92-104.

## Pipeline per chapter
1. user uploads the needed source PDF part(s) into `uploads/`
2. `python3 work/render.py <a> <b> 100`  (renders work/pages/bNNN.png)
3. read_file the pages (batches), transcribe every line mentally
4. write data/chNN_a.json / _b.json / _c.json (last holds "units"), assemble to data/chNN.json
5. `python3 work/validate.py data/chNN.json`
6. `python3 work/merge.py pulse-ortho-complete.html`  (idempotent; appends chapters > max embedded, flips live flags, rewrites data/chapters_live.json)
7. `python3 work/integrity.py` + extract inline JS → `node --check`
8. commit & push to GitHub repo, present_file pulse-ortho-complete.html

## How to CONTINUE in a new session (user says "continue")
1. Clone the repo (user provides GitHub username + PAT, repo is private):
   `git clone https://<TOKEN>@github.com/<user>/<repo>.git` (or via the URL user pastes)
2. Read this PROGRESS.md — it is the single source of truth.
3. Find NEXT chapter below, ask user to upload that part of the source PDF.
4. Run the pipeline above. Commit+push after each chapter so progress is never lost.

## Status
- DONE: ch 1-11 (original 1497 qs), ch12 (195 qs, 28 units), ch13 (89 qs, 13 units),
  ch14 Nerve Injuries: Part 2 (108 qs, 13 units), ch15 Orthopaedic Oncology: Part 1 (68 qs, 13 units),
  ch16 Orthopaedic Oncology: Part 2 (130 qs, 24 units)
  → total 2087 qs, 278 units, 16 live chapters in pulse-ortho-complete.html.
- NEXT: ch17 (book 137-147 → file2 pdf pages 39-49). Then 18..24 per map above.
- NOTE (2026-09-13): PUSHED to https://github.com/Deva20045/ORTHO (main). Token works for Contents
  write but NOT Pages write -> user must enable Pages manually once:
  Repo -> Settings -> Pages -> Source "Deploy from a branch" -> main /(root) -> Save.
  Live link after that: https://deva20045.github.io/ORTHO/pulse-ortho-complete.html
  User asked for the live link + auto-update after EVERY chapter. push.sh default repo = ORTHO.
- Deliverable file: `pulse-ortho-complete.html` (workspace root / repo root).
- GitHub repo: see REMOTE.md (created once user provides PAT; repo kept PRIVATE — copyrighted source).
