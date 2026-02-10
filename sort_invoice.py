import re
import argparse
import pdfplumber
from pypdf import PdfReader, PdfWriter

# --- Regex SKU & Qty (umum). Kalau invoice kamu beda format, nanti kita tweak.
SKU_RE = re.compile(r"\b[A-Z]{2,10}(?:-[A-Z0-9]{1,20})+\b")
QTY_RE = re.compile(r"(?:Qty|QTY|Jumlah)\s*[:x]?\s*(\d+)", re.IGNORECASE)

def extract_page_info(pdf_path: str):
    infos = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text() or ""
            skus = SKU_RE.findall(text)
            qtys = [int(x) for x in QTY_RE.findall(text)]
            total_qty = sum(qtys) if qtys else 0
            sku_key = min(skus) if skus else "ZZZ-NO-SKU"

            infos.append({
                "page_index": i,
                "total_qty": total_qty,
                "sku_key": sku_key,
                "skus": sorted(set(skus)),
            })
    return infos

def write_sorted_pdf(input_pdf: str, page_order: list[int], output_pdf: str):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    for idx in page_order:
        writer.add_page(reader.pages[idx])
    with open(output_pdf, "wb") as f:
        writer.write(f)

def main():
    parser = argparse.ArgumentParser(description="Sort PDF invoice pages by SKU or total qty.")
    parser.add_argument("--in", dest="input_pdf", required=True, help="Input PDF path")
    parser.add_argument("--out", dest="output_pdf", required=True, help="Output PDF path")
    parser.add_argument("--sort", choices=["sku", "qty"], default="sku", help="Sort mode: sku or qty")
    parser.add_argument("--desc", action="store_true", help="Sort descending (largest first)")
    args = parser.parse_args()

    infos = extract_page_info(args.input_pdf)

    if args.sort == "qty":
        sorted_infos = sorted(infos, key=lambda x: x["total_qty"], reverse=args.desc)
    else:
        sorted_infos = sorted(infos, key=lambda x: x["sku_key"], reverse=args.desc)

    order = [x["page_index"] for x in sorted_infos]
    write_sorted_pdf(args.input_pdf, order, args.output_pdf)

    print("DONE ✅")
    print("Output:", args.output_pdf)

if __name__ == "__main__":
    main()
