#!/usr/bin/env python3
"""Render book pages from the source PDFs to PNGs for transcription.

Source mapping (from PROGRESS.md):
- uploads/Orthopedics Marrow E8-1-100.pdf   = global pdf pages 1-100  -> book page = pdf - 2
- uploads/Orthopedics Marrow E8-101-204.pdf = global pdf pages 101-204 -> book = file2 page + 98

Usage: python3 work/render.py <book_page_a> <book_page_b> [dpi=100]
Output: work/pages/bNNN.png (NNN = zero-padded book page)
"""
import glob, os, sys

def find_pdf(second_half):
    pats = ["uploads/Orthopedics*Marrow*E8-101-204.pdf"] if second_half \
        else ["uploads/Orthopedics*Marrow*E8-1-100.pdf", "uploads/Orthopedics*Marrow*E8-1-1*.pdf"]
    for p in pats:
        g = sorted(glob.glob(p))
        if g:
            return g[0]
    return None

def render(a, b, dpi=100):
    try:
        import fitz  # PyMuPDF
    except ImportError:
        os.system("pip3 install -q pymupdf")
        import fitz
    os.makedirs("work/pages", exist_ok=True)
    for book in range(a, b + 1):
        if book <= 98:
            pdf, page = find_pdf(False), book + 2
        else:
            pdf, page = find_pdf(True), book - 98
        if not pdf or not os.path.exists(pdf):
            print(f"!! b{book:03d}: source PDF not found — upload it to uploads/ first")
            continue
        doc = fitz.open(pdf)
        if page < 1 or page > doc.page_count:
            print(f"!! b{book:03d}: page {page} out of range in {pdf}")
            continue
        pix = doc[page - 1].get_pixmap(dpi=dpi)
        out = f"work/pages/b{book:03d}.png"
        pix.save(out)
        print(f"b{book:03d} <- {os.path.basename(pdf)} p{page} -> {out} ({pix.width}x{pix.height})")
        doc.close()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    render(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 100)
