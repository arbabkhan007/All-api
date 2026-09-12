#!/usr/bin/env python3
"""Build the sellable product from the listing kit.

Substitutes the verified titles, tag sets and description copy from the
per-pattern listing files into the product template, then renders print-ready
PDFs with reportlab.

    /tmp/pdfenv/bin/python build_product.py

Outputs (into ../product/):
    Etsy-Listing-Kit-Crochet.md     final, customer-facing markdown
    Etsy-Listing-Kit-Crochet.pdf    the product itself
    Etsy-Listing-Worksheets.pdf     printable worksheets
"""

import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table,
    TableStyle, PageBreak,
)


HERE = Path(__file__).resolve().parent
PRODUCT = HERE.parent / "product"
KIT = HERE.parent.parent.parent / "etsy-listing-kit"

INK = colors.HexColor("#1f2933")
ACCENT = colors.HexColor("#7b2d26")
MUTED = colors.HexColor("#6b7280")
RULE = colors.HexColor("#d8d2c8")
CODE_BG = colors.HexColor("#f5f2ec")

PRODUCT_TITLE = "Etsy Listing Kit"
PRODUCT_SUB = "for Crochet Pattern Sellers"


# ---------------------------------------------------------------- extraction

def fenced_block_after(lines, marker_re):
    """Return the contents of the first ```fence``` after a marker line."""
    for i, line in enumerate(lines):
        if re.match(marker_re, line):
            for j in range(i, len(lines)):
                if lines[j].strip() == "```":
                    out = []
                    for k in range(j + 1, len(lines)):
                        if lines[k].strip() == "```":
                            return "\n".join(out)
                        out.append(lines[k])
                    break
            break
    raise ValueError(f"no fenced block found after {marker_re!r}")


def tag_set_a(lines):
    """Rows of the 'Set A (primary)' table as (tag, chars)."""
    start = None
    for i, line in enumerate(lines):
        if line.startswith("## Tags") and "Set A" in line:
            start = i
            break
    if start is None:
        raise ValueError("no Set A tag table")
    rows = []
    for line in lines[start:]:
        if not line.strip().startswith("|"):
            if rows:
                break
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells[0] in ("#",) or set(cells[0]) <= set(":- "):
            continue
        if not cells[0].isdigit():
            break
        rows.append((cells[1], cells[2]))
    return rows


def collect(source_path):
    lines = source_path.read_text().split("\n")
    return {
        "title": fenced_block_after(lines, r"^\*\*Title\*\*").strip(),
        "desc": fenced_block_after(lines, r"^### Full description").strip(),
        "tags": tag_set_a(lines),
    }


def tag_table(tags):
    """Render 13 tags as a six-column table: two per row."""
    rows = [["#", "Tag", "Chars", "#", "Tag", "Chars"],
            [":-:", "---", ":-:", ":-:", "---", ":-:"]]
    half = (len(tags) + 1) // 2
    for i in range(half):
        left = tags[i] if i < len(tags) else ("", "")
        right = tags[i + half] if i + half < len(tags) else ("", "")
        rows.append([
            str(i + 1), left[0], left[1],
            str(i + half + 1) if i + half < len(tags) else "",
            right[0], right[1],
        ])
    head, sep, *body = rows
    cells = lambda r: "| " + " | ".join(r) + " |"
    return "\n".join([cells(head), cells(sep)] + [cells(r) for r in body])


def build_markdown():
    template = (PRODUCT / "template.md").read_text()
    sources = {
        "07": KIT / "07-listing-no-sew-gnome.md",
        "08": KIT / "08-listing-bobble-christmas-tree.md",
        "09": KIT / "09-listing-christmas-ornament-bundle.md",
        "10": KIT / "10-listing-bobble-tree-skirt.md",
        "11": KIT / "11-listing-interchangeable-wreath.md",
    }
    for code, path in sources.items():
        data = collect(path)
        template = template.replace("{{TITLE_%s}}" % code, data["title"])
        template = template.replace("{{DESC_%s}}" % code, data["desc"])
        template = template.replace("{{TAGS_%s}}" % code, tag_table(data["tags"]))
    leftover = re.findall(r"\{\{[A-Z_0-9]+\}\}", template)
    if leftover:
        raise SystemExit(f"unresolved placeholders: {set(leftover)}")
    out = PRODUCT / "Etsy-Listing-Kit-Crochet.md"
    out.write_text(template)
    return out, template


# ------------------------------------------------------------------ rendering

def styles():
    return {
        "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=19,
                             leading=23, textColor=ACCENT, spaceAfter=10),
        "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=13,
                             leading=16, textColor=INK, spaceBefore=14,
                             spaceAfter=6),
        "h3": ParagraphStyle("h3", fontName="Helvetica-BoldOblique", fontSize=11,
                             leading=14, textColor=INK, spaceBefore=10,
                             spaceAfter=4),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9.7,
                               leading=13.6, textColor=INK, spaceAfter=6,
                               alignment=TA_LEFT),
        "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.7,
                                 leading=13.4, textColor=INK, leftIndent=16,
                                 bulletIndent=4, spaceAfter=3),
        "quote": ParagraphStyle("quote", fontName="Helvetica-Oblique",
                                fontSize=10.5, leading=14.5,
                                textColor=colors.HexColor("#3f4a56"),
                                leftIndent=10, rightIndent=6, spaceAfter=8),
        "code": ParagraphStyle("code", fontName="Courier", fontSize=7.6,
                               leading=10.2, textColor=INK, spaceBefore=0,
                               spaceAfter=0, leftIndent=8, rightIndent=6,
                               backColor=CODE_BG),
        "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4,
                               leading=11, textColor=INK),
        "cellh": ParagraphStyle("cellh", fontName="Helvetica-Bold", fontSize=8.4,
                                leading=11, textColor=colors.white),
        "cover": ParagraphStyle("cover", fontName="Helvetica-Bold", fontSize=30,
                                leading=35, textColor=ACCENT, spaceAfter=6),
        "coversub": ParagraphStyle("coversub", fontName="Helvetica",
                                   fontSize=17, leading=22, textColor=INK,
                                   spaceAfter=18),
        "covertag": ParagraphStyle("covertag", fontName="Helvetica-Oblique",
                                   fontSize=11.5, leading=17, textColor=MUTED),
    }


def esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def inline(text):
    text = esc(text)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)


def rule():
    """A hairline rule, as a flowable that never blocks pagination."""
    t = Table([[""]], colWidths=[6.9 * inch], rowHeights=[0.6])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def code_block(text, st):
    """Render as one flowable per line so long blocks split across pages."""
    out = [Spacer(1, 4), rule()]
    for line in text.split("\n"):
        html = inline(line).replace("  ", "&nbsp;&nbsp;")
        out.append(Paragraph(html if html.strip() else "&nbsp;", st["code"]))
    out.append(rule())
    out.append(Spacer(1, 8))
    return out


def md_table(rows, st):
    head, body = rows[0], rows[1:]
    data = [[Paragraph(inline(c), st["cellh"]) for c in head]]
    data += [[Paragraph(inline(c), st["cell"]) for c in r] for r in body]
    ncol = len(head)
    avail = 6.9 * inch
    widths = [avail / ncol] * ncol
    t = Table(data, colWidths=widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#faf8f4")))
    t.setStyle(TableStyle(style))
    return t


def flowables(md, st):
    """Turn the markdown subset into reportlab flowables."""
    out, lines = [], md.split("\n")
    i, first_h1 = 0, True
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped == "```":
            block = []
            i += 1
            while i < len(lines) and lines[i].strip() != "```":
                block.append(lines[i])
                i += 1
            i += 1
            out.extend(code_block("\n".join(block), st))
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and \
                set(lines[i + 1].strip().replace("|", "").replace(":", "")
                    .replace("-", "").replace(" ", "")) == set():
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                raw = lines[i].strip().strip("|").split("|")
                rows.append([c.strip() for c in raw])
                i += 1
            if len(rows) >= 2:
                out.append(Spacer(1, 4))
                out.append(md_table(rows, st))
                out.append(Spacer(1, 10))
            continue

        if not stripped:
            i += 1
            continue

        if stripped == "---":
            out.append(Spacer(1, 6))
            i += 1
            continue

        if stripped.startswith("# "):
            if not first_h1:
                out.append(PageBreak())
            first_h1 = False
            out.append(Paragraph(inline(stripped[2:]), st["h1"]))
            i += 1
            continue

        if stripped.startswith("## "):
            out.append(Paragraph(inline(stripped[3:]), st["h2"]))
            i += 1
            continue

        if stripped.startswith("### "):
            out.append(Paragraph(inline(stripped[4:]), st["h3"]))
            i += 1
            continue

        if stripped.startswith("> "):
            quote = Paragraph(inline(stripped[2:]), st["quote"])
            t = Table([[quote]], colWidths=[6.9 * inch])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f7f4ee")),
                ("LINEBEFORE", (0, 0), (0, -1), 2.5, ACCENT),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]))
            out.append(t)
            out.append(Spacer(1, 8))
            i += 1
            continue

        if stripped.startswith("- [ ] "):
            out.append(Paragraph(inline(stripped[6:]), st["bullet"],
                                 bulletText="\u2610"))
            i += 1
            continue

        if stripped.startswith("- "):
            out.append(Paragraph(inline(stripped[2:]), st["bullet"],
                                 bulletText="\u2022"))
            i += 1
            continue

        para = [inline(stripped)]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith(
                ("#", "-", ">", "|", "`", "---")):
            para.append(inline(lines[i].strip()))
            i += 1
        out.append(Paragraph("<br/>".join(para), st["body"]))
        out.append(Spacer(1, 2))

    return out


def cover(st, title, sub, tagline):
    return [
        Spacer(1, 1.7 * inch),
        Paragraph(title, st["cover"]),
        Paragraph(sub, st["coversub"]),
        Spacer(1, 0.2 * inch),
        Paragraph(tagline, st["covertag"]),
        Spacer(1, 2.6 * inch),
        Paragraph("Novality Store", ParagraphStyle(
            "shop", fontName="Helvetica-Bold", fontSize=12,
            textColor=INK, spaceAfter=4)),
        Paragraph("&copy; 2026 &nbsp;·&nbsp; Personal use licence inside",
                  ParagraphStyle("fine", fontName="Helvetica", fontSize=9,
                                 textColor=MUTED)),
        PageBreak(),
    ]


def render(md_path, pdf_path, title, sub, tagline, running_head):
    st = styles()
    doc = BaseDocTemplate(
        str(pdf_path), pagesize=LETTER,
        leftMargin=0.8 * inch, rightMargin=0.8 * inch,
        topMargin=0.75 * inch, bottomMargin=0.8 * inch,
        title=title, author="Novality Store",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  id="body")

    def decorate(canvas, doc_):
        canvas.saveState()
        if doc_.page > 1:
            canvas.setFont("Helvetica", 7.5)
            canvas.setFillColor(MUTED)
            canvas.drawString(doc_.leftMargin, LETTER[1] - 0.5 * inch, running_head)
            canvas.setStrokeColor(RULE)
            canvas.setLineWidth(0.4)
            canvas.line(doc_.leftMargin, LETTER[1] - 0.55 * inch,
                        LETTER[0] - doc_.rightMargin, LETTER[1] - 0.55 * inch)
            canvas.drawCentredString(LETTER[0] / 2.0, 0.5 * inch,
                                     str(doc_.page))
            canvas.drawRightString(LETTER[0] - doc_.rightMargin, 0.5 * inch,
                                   "© 2026 Novality Store")
        canvas.restoreState()

    doc.addPageTemplates([PageTemplate(id="all", frames=[frame],
                                       onPage=decorate)])
    body = flowables(md_path.read_text(), st)
    doc.build(cover(st, title, sub, tagline) + body)


def main():
    PRODUCT.mkdir(parents=True, exist_ok=True)
    md_out, _ = build_markdown()
    print(f"wrote {md_out.name}")

    render(md_out, PRODUCT / "Etsy-Listing-Kit-Crochet.pdf",
           PRODUCT_TITLE, PRODUCT_SUB,
           "Titles, tags and descriptions that fit Etsy's limits — plus five "
           "complete listings you can copy.",
           "Etsy Listing Kit for Crochet Pattern Sellers")
    print("wrote Etsy-Listing-Kit-Crochet.pdf")

    ws = PRODUCT / "worksheets.md"
    render(ws, PRODUCT / "Etsy-Listing-Worksheets.pdf",
           "Listing Worksheets", "Plan every listing before you publish",
           "Print them, or copy them into a notebook. One of each per listing.",
           "Etsy Listing Kit · Worksheets")
    print("wrote Etsy-Listing-Worksheets.pdf")


if __name__ == "__main__":
    main()
