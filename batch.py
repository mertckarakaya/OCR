import os
import sys
from pathlib import Path
from pdf2image import convert_from_path
import pytesseract

IN_ROOT = Path("/data/in")
OUT_ROOT = Path("/data/out")

OCR_LANG = os.getenv("OCR_LANG", "tur+eng")
OCR_DPI = int(os.getenv("OCR_DPI", "300"))
OCR_PSM = os.getenv("OCR_PSM", "6")
OCR_FORCE = os.getenv("OCR_FORCE", "0") == "1"

def out_path_for(in_pdf: Path) -> Path:
    rel = in_pdf.relative_to(IN_ROOT) 
    out_dir = OUT_ROOT / rel.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / f"{in_pdf.stem}.OCR.txt"

def ocr_pdf(in_pdf: Path, out_txt: Path):
    config = f"--oem 3 --psm {OCR_PSM}"
    pages = convert_from_path(str(in_pdf), dpi=OCR_DPI)
    parts = []
    for i, page in enumerate(pages, start=1):
        text = pytesseract.image_to_string(page, lang=OCR_LANG, config=config)
        parts.append(f"--- Page {i} ---\n{text}")
    out_txt.write_text("\n".join(parts), encoding="utf-8")
    print(f"[OK] {in_pdf} -> {out_txt}")

def main():
    if not IN_ROOT.exists():
        print(f"[WARN] Giriş klasörü yok: {IN_ROOT}")
        return

    pdfs = [p for p in IN_ROOT.rglob("*.pdf")]
    if not pdfs:
        print(f"[INFO] PDF bulunamadı: {IN_ROOT}")
        return

    processed = skipped = 0
    for pdf in pdfs:
        out_txt = out_path_for(pdf)
        if out_txt.exists() and not OCR_FORCE:
            print(f"[SKIP] Zaten var: {out_txt} (OCR_FORCE=0)")
            skipped += 1
            continue
        try:
            ocr_pdf(pdf, out_txt)
            processed += 1
        except Exception as e:
            print(f"[ERR] {pdf}: {e}", file=sys.stderr)

    print(f"[DONE] İşlenen: {processed}, Atlanan: {skipped}")

if __name__ == "__main__":
    main()