# PULSE Ortho continuation — progress tracker

## Goal
Extend `uploads/pulse-ortho (4).html` (quiz app, Marrow Ortho E8) line-by-line from the
scanned book PDFs until ALL 24 chapters are live. User demands: no quality compromise,
line-by-line questions, first line → last line, strict book order, identical style/schema.

## Sources
- `uploads/Orthopedics Marrow E8-1-100.pdf`  = global pdf pages 1-100  → book pages = pdf-2 (book ≤98)
- `uploads/Orthopedics Marrow E8-101-204.pdf` = global pdf pages 101-204 → book = pdfpage(file2)+98
- Scans have NO text layer → read pages as images (rendered PNGs in work/pages/bNNN.png, 100 dpi).

## Schema (must match exactly)
- Question: {id:"ORTHO-C{ch}-{nnn}" sequential per chapter from 001, sec, page(book), q, opts[4], ans(idx), exp ends "(Book pX)"}
- Unit: {id:"ORTHO-U{ch}-{n}" sequential per chapter from 1, ch, n, title, sec:"<Heading> · p<page>", qs:[ids contiguous & ordered], guide: vivid 2-3 sentence prose}
- Units must cover every question exactly once, in order. Validator: `python3 work/validate.py data/chNN.json`

## Chapter page map (book pages)
12: 90-104 DONE (195 qs, 28 units) | 13: 105-111 | 14: 112-122 | 15: 123-128 | 16: 129-136
17: 137-147 | 18: 148-153 | 19: 154-159 | 20: 160-165 | 21: 166-172 | 22: 173-180 | 23: 181-189 | 24: 190-202

## Pipeline per chapter
1. `python3 work/render.py <a> <b> 100`  (renders work/pages/bNNN.png)
2. read_file the pages (batches), transcribe every line mentally
3. write data/chNN_a.json / _b.json / _c.json (last holds "units"), assemble to data/chNN.json
4. `python3 work/validate.py data/chNN.json`
5. set data/chapters_live.json = list of ALL done chapters, e.g. [12,13,...]
6. `python3 work/merge.py pulse-ortho-complete.html`  (rebuilds from uploads original each time)
7. integrity script (see turn of ch12) + `node --check work/app.js`
8. present_file pulse-ortho-complete.html

## Status
- DONE: ch 1-11 (original 1497 qs), ch12 (195 qs, 28 units), ch13 (89 qs, 13 units)
  → total 1781 qs, 228 units, 13 live chapters in pulse-ortho-complete.html.
- NEXT: ch14 (book 112-122 → file2 pages 14-24). Then 15..24 per map above.
- Deliverable file: `pulse-ortho-complete.html` (workspace root).
