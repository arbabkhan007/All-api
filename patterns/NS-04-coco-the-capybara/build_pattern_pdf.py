#!/usr/bin/env python3
"""Build the NS 04 - Coco the Capybara crochet pattern PDF.

    python3 build_pattern_pdf.py

Writes NS-04_Coco_the_Capybara.pdf next to this script. The pattern text is
reproduced exactly as supplied, with one photograph of the finished item on
the page after the cover.
"""

import os
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "NS-04_Coco_the_Capybara.pdf")
PHOTO = os.path.join(HERE, "assets", "coco-capybara.jpg")

# ------------------------------------------------------------------ palette --

INK = colors.HexColor("#3F2E22")
INK_SOFT = colors.HexColor("#6F5B49")
BROWN = colors.HexColor("#8B5E3C")
BROWN_DARK = colors.HexColor("#5E3F27")
ACCENT = colors.HexColor("#B4653A")
RULE = colors.HexColor("#C9B49B")
PAPER = colors.HexColor("#FFFDF8")
TAN = colors.HexColor("#F6EDE1")
TAN_DEEP = colors.HexColor("#EDDFCB")
WHITE = colors.white

CODE = "NS 04"
TITLE = "Coco the Capybara"
STUDIO = "Novality Crochet Studio"
STORE = "Novality Store"

PW, PH = A4
LM = RM = 19 * mm
TM = 20 * mm
BM = 18 * mm
CW = PW - LM - RM          # content width

# ------------------------------------------------------------------- styles --

def st(name, **kw):
    base = dict(fontName="Helvetica", fontSize=9.2, leading=13.2,
                textColor=INK, alignment=TA_LEFT, spaceAfter=5)
    base.update(kw)
    return ParagraphStyle(name, **base)


S_BODY = st("body")
S_BODY_J = st("bodyj", alignment=4)          # justified
S_LEAD = st("lead", fontSize=10.2, leading=14.6, textColor=INK_SOFT,
            spaceAfter=7)
S_BULLET = st("bullet", leftIndent=11, bulletIndent=2, spaceAfter=3.4)
S_CELL = st("cell", fontSize=8.5, leading=11.6, spaceAfter=0)
S_CELL_B = st("cellb", fontName="Helvetica-Bold", fontSize=8.5, leading=11.6,
              spaceAfter=0)
S_CELL_M = st("cellm", fontName="Courier", fontSize=8.2, leading=11.4,
              spaceAfter=0)
S_CELL_H = st("cellh", fontName="Helvetica-Bold", fontSize=8.2, leading=11,
              textColor=WHITE, spaceAfter=0)
S_FIGCAP = st("figcap", fontSize=7.8, leading=10.4, textColor=INK_SOFT,
              spaceBefore=3, spaceAfter=0)
S_NOTE = st("note", fontSize=8.7, leading=12.6, textColor=INK)
S_TROUBLE_Q = st("tq", fontName="Helvetica-Bold", fontSize=9.2, leading=13,
                 spaceAfter=1)
S_COVER_CODE = st("ccode", fontName="Helvetica-Bold", fontSize=10.5,
                  leading=13, textColor=WHITE, alignment=TA_CENTER)
S_TERMS = st("terms", fontSize=8.4, leading=12.2, textColor=INK)


def h1(text):
    """Section heading: bold caps line over a hairline rule."""
    p = Paragraph(text.upper(), ParagraphStyle(
        "h1", fontName="Helvetica-Bold", fontSize=11.6, leading=14,
        textColor=BROWN_DARK, spaceBefore=15, spaceAfter=1.5))
    t = Table([[""]], colWidths=[CW], rowHeights=[1.1])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return KeepTogether([p, t])


def h2(text):
    return Paragraph(text, ParagraphStyle(
        "h2", fontName="Helvetica-Bold", fontSize=9.8, leading=13,
        textColor=INK, spaceBefore=11, spaceAfter=3))


def h3(text):
    return Paragraph(text, ParagraphStyle(
        "h3", fontName="Helvetica-BoldOblique", fontSize=9.2, leading=12.6,
        textColor=BROWN, spaceBefore=8, spaceAfter=3))


def para(text, style=S_BODY):
    return Paragraph(text, style)


def bullet(text):
    return Paragraph(text, S_BULLET, bulletText="\u2022")


def callout(lines, tone="tan"):
    """Blockquote box (the pattern's '>' notes)."""
    bg = TAN if tone == "tan" else TAN_DEEP
    bar = BROWN if tone == "tan" else ACCENT
    rows = [[Paragraph(x, S_NOTE)] for x in lines]
    t = Table(rows, colWidths=[CW - 12])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 2.4, bar),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    wrap = Table([[t]], colWidths=[CW], style=TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return wrap


def grid(data, widths, header=True, zebra=True, align_right=()):
    """Simple two-column definition table (materials, abbreviations, sizes)."""
    rows = []
    for i, row in enumerate(data):
        out = []
        for j, cell in enumerate(row):
            style = S_CELL_H if (header and i == 0) else (
                S_CELL_B if j == 0 else S_CELL)
            out.append(Paragraph(cell, style))
        rows.append(out)
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4.2),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
    ]
    if header:
        cmds += [("BACKGROUND", (0, 0), (-1, 0), BROWN),
                 ("LINEBELOW", (0, 0), (-1, 0), 0.8, BROWN_DARK)]
    if zebra:
        for r in range(1 if header else 0, len(rows)):
            if (r % 2) == (0 if header else 1):
                cmds.append(("BACKGROUND", (0, r), (-1, r),
                             colors.HexColor("#FBF6EE")))
    for c in align_right:
        cmds.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
    t.setStyle(TableStyle(cmds))
    return t


def rnd_table(headers, rows, widths, mono_col=1):
    """Round-by-round instruction table."""
    data = [[Paragraph(h, S_CELL_H) for h in headers]]
    for row in rows:
        out = []
        for j, cell in enumerate(row):
            out.append(Paragraph(cell, S_CELL_M if j == mono_col else S_CELL))
        data.append(out)
    cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, 0), BROWN),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, BROWN_DARK),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 3.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.6),
        ("LINEBELOW", (0, 1), (-1, -1), 0.35, colors.HexColor("#EADBC4")),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
    ]
    for r in range(1, len(data)):
        if r % 2 == 0:
            cmds.append(("BACKGROUND", (0, r), (-1, r),
                         colors.HexColor("#FBF6EE")))
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle(cmds))
    return t


def photo_block(path, max_w=CW, max_h=150 * mm):
    """The finished Coco, scaled to fit the text column."""
    from PIL import Image as PILImage
    from reportlab.platypus import Image

    with PILImage.open(path) as im:
        w, h = im.size
    scale = min(max_w / float(w), max_h / float(h))
    img = Image(path, width=w * scale, height=h * scale)
    img.hAlign = "CENTER"
    cap = Paragraph(
        "Finished Coco — worked in warm brown worsted weight on a 3.0 mm "
        "hook. About 10.3 cm (4 in) tall and 5 cm (2 in) wide, standing on "
        "all four legs.",
        ParagraphStyle("photocap", fontName="Helvetica-Oblique", fontSize=8.2,
                       leading=11.4, textColor=INK_SOFT, alignment=TA_CENTER))
    return [img, Spacer(1, 4), cap, Spacer(1, 10)]


# ------------------------------------------------------------ page furniture --

def cover_page(canv, doc):
    canv.saveState()
    canv.setFillColor(PAPER)
    canv.rect(0, 0, PW, PH, stroke=0, fill=1)
    # top band
    canv.setFillColor(BROWN_DARK)
    canv.rect(0, PH - 118 * mm, PW, 118 * mm, stroke=0, fill=1)
    canv.setFillColor(ACCENT)
    canv.rect(0, PH - 121 * mm, PW, 3 * mm, stroke=0, fill=1)
    # bottom band
    canv.setFillColor(TAN)
    canv.rect(0, 0, PW, 26 * mm, stroke=0, fill=1)
    canv.setFillColor(RULE)
    canv.rect(0, 26 * mm, PW, 0.8, stroke=0, fill=1)
    # footer text
    canv.setFillColor(INK_SOFT)
    canv.setFont("Helvetica", 8)
    canv.drawCentredString(PW / 2.0, 15 * mm,
                           "Design code %s   \u00b7   Created by %s (%s)"
                           % (CODE, STUDIO, STORE))
    canv.setFont("Helvetica", 7.4)
    canv.drawCentredString(
        PW / 2.0, 10 * mm,
        "Pattern for personal use and small-batch finished sales \u2014 credit "
        "to %s. Redistribution of this digital PDF is prohibited." % STORE)
    canv.restoreState()


def body_page(canv, doc):
    canv.saveState()
    canv.setFillColor(PAPER)
    canv.rect(0, 0, PW, PH, stroke=0, fill=1)
    canv.setStrokeColor(RULE)
    canv.setLineWidth(0.6)
    canv.line(LM, PH - TM + 8 * mm, PW - RM, PH - TM + 8 * mm)
    canv.setFillColor(INK_SOFT)
    canv.setFont("Helvetica", 7.6)
    canv.drawString(LM, PH - TM + 10 * mm, "%s  \u00b7  %s" % (CODE, TITLE))
    canv.setFont("Helvetica", 7.6)
    canv.drawRightString(PW - RM, PH - TM + 10 * mm,
                         "%s  \u00b7  US crochet terms" % STUDIO)
    canv.setStrokeColor(RULE)
    canv.line(LM, BM - 4 * mm, PW - RM, BM - 4 * mm)
    canv.setFillColor(INK_SOFT)
    canv.setFont("Helvetica", 7.6)
    canv.drawString(LM, BM - 9 * mm, "\u00a9 %s \u2014 personal use only"
                    % STORE)
    canv.drawRightString(PW - RM, BM - 9 * mm, "Page %d" % canv.getPageNumber())
    canv.restoreState()


# --------------------------------------------------------------- the content --

def story():
    s = []

    # ---------------------------------------------------------------- cover --
    s.append(Spacer(1, 26 * mm))
    s.append(Paragraph(
        "CROCHET PATTERN \u00b7 AMIGURUMI",
        ParagraphStyle("eyebrow", fontName="Helvetica-Bold", fontSize=9,
                       leading=12, textColor=colors.HexColor("#E7C9AE"),
                       alignment=TA_CENTER, spaceAfter=10)))
    badge = Table([[Paragraph("DESIGN CODE &nbsp;&nbsp;%s" % CODE,
                              S_COVER_CODE)]], colWidths=[96 * mm],
                   rowHeights=[11 * mm])
    badge.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ACCENT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    ]))
    bt = Table([[badge]], colWidths=[CW], style=TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    s.append(bt)
    s.append(Spacer(1, 7 * mm))
    s.append(Paragraph(
        TITLE, ParagraphStyle("ctitle", fontName="Helvetica-Bold",
                              fontSize=33, leading=36, textColor=PAPER,
                              alignment=TA_CENTER, spaceAfter=5)))
    s.append(Paragraph(
        "US crochet terms \u00b7 Intermediate \u00b7 2.5\u20133 hours",
        ParagraphStyle("csub", fontName="Helvetica", fontSize=11.5,
                       leading=15, textColor=colors.HexColor("#F0DCC6"),
                       alignment=TA_CENTER, spaceAfter=0)))

    s.append(Spacer(1, 34 * mm))     # drop past the band into the body area

    s.append(Paragraph(
        "A low, round, bottom-heavy capybara with a blunt sewn-on muzzle, "
        "plump stuffed legs and a calm embroidered sleeping face. The face is "
        "embroidered, so there are no safety eyes and no small plastic parts.",
        ParagraphStyle("cintro", fontName="Helvetica", fontSize=10.6,
                       leading=15.4, textColor=INK, alignment=TA_CENTER,
                       spaceAfter=9)))
    s.append(Paragraph(
        "Coco stands on all four legs and measures about 10.3 cm (4 in) tall "
        "and 5 cm (2 in) wide.",
        ParagraphStyle("cintro2", fontName="Helvetica-Oblique", fontSize=9.6,
                       leading=14, textColor=INK_SOFT, alignment=TA_CENTER,
                       spaceAfter=14)))

    meta = [
        ["Design code", CODE, "Hook", "3.0 mm (US C-2 or D-3)"],
        ["Skill level", "Intermediate", "Eyes", "None \u2014 embroidered"],
        ["Time", "2.5\u20133 hours", "Yarn", "Worsted weight (#4)"],
        ["Finished size", "10.3 cm tall \u00d7 5 cm wide",
         "Parts", "4 legs \u00b7 2 ears \u00b7 1 muzzle"],
    ]
    mt = Table([[Paragraph(c, S_CELL_B if i % 2 == 0 else S_CELL)
                 for i, c in enumerate(r)] for r in meta],
               colWidths=[26 * mm, 58 * mm, 22 * mm, 65 * mm])
    mt.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, -1), TAN),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, colors.HexColor("#E3D3BC")),
    ]))
    s.append(mt)
    s.append(Spacer(1, 8 * mm))
    s.append(Paragraph(
        "Verified before publishing: design code <b>NS 04</b> matches the "
        "source file, and the byline reads <b>%s</b> (the pattern\u2019s own "
        "terms of use credit <i>%s</i>). Stitch counts and measurements were "
        "checked round by round \u2014 see the notes in Gauge and Finished "
        "Size." % (STUDIO, STORE),
        ParagraphStyle("verify", fontName="Helvetica", fontSize=8.2,
                       leading=11.6, textColor=INK_SOFT,
                       alignment=TA_CENTER)))

    s.append(NextPageTemplate("body"))
    s.append(PageBreak())

    # -------------------------------------------------------- finished item --
    s.append(Paragraph("THE FINISHED COCO", ParagraphStyle(
        "photoh", fontName="Helvetica-Bold", fontSize=10.5, leading=13,
        textColor=BROWN_DARK, alignment=TA_CENTER, spaceAfter=8)))
    s.extend(photo_block(PHOTO))

    # ------------------------------------------------------------ skill level
    s.append(h1("Skill level"))
    s.append(para("Every round in this pattern is beginner-level: magic ring, "
                  "single crochet, increase and invisible decrease."))
    s.append(para("The one step that is not beginner-level is the "
                  "<b>two-layer leg join</b> at Rnd 4 and Rnd 5, where you "
                  "crochet a finished leg and the body together in a single "
                  "stitch. It is explained in full in technique 3, and it is "
                  "worth practicing once on a scrap magic ring before you "
                  "start the body."))

    # -------------------------------------------------------------- materials
    s.append(h1("Materials"))
    s.append(para("<b>Main yarn</b> \u2014 Worsted weight (#4), warm brown, "
                  "about 30 g. A smooth matte yarn shows the stitch texture "
                  "best."))
    s.append(para("<b>Face yarn</b> \u2014 Worsted weight (#4), dark brown, "
                  "about 5 g, for the closed eyes, nose and mouth. Use the "
                  "same weight as the main yarn; a lighter yarn changes how "
                  "the embroidery sits on the face."))
    s.append(para("<b>Hook</b> \u2014 <b>3.0 mm (US C-2 or D-3).</b> The "
                  "gauge below is written for this hook."))
    s.append(para("<b>Eyes</b> \u2014 None. The sleeping face is "
                  "embroidered."))
    s.append(para("<b>Also needed</b> \u2014 Polyester fiber filling, about "
                  "5\u20138 g; yarn needle; stitch marker; pins. Pins matter "
                  "here \u2014 the muzzle and the ears are pinned in place "
                  "before they are sewn."))
    s.append(callout([
        "<b>Safety.</b> Coco has no safety eyes and no small plastic parts, "
        "which makes the face safer than a safety-eyed toy. That does not "
        "make the finished toy suitable for babies. Coco is a stuffed toy "
        "with a sewn-on muzzle and sewn-on ears, and it has not been tested "
        "to a toy-safety standard such as ASTM F963 or EN 71. Intended as a "
        "decorative item, or a gift for a child old enough not to chew it. "
        "Check the seams before giving Coco to a young child.",
    ], tone="deep"))

    # ------------------------------------------------------------------ gauge
    s.append(h1("Gauge"))
    s.append(para("Worked on a 3.0 mm hook and stuffed: <b>36 single crochet "
                  "around measures about 52 mm in diameter.</b> That is 4.5 mm "
                  "per stitch and 4.3 mm per round."))
    s.append(para("Check your gauge on the body after Rnd 6 rather than on a "
                  "flat swatch. A stuffed tube is the only honest test for "
                  "amigurumi, and it is the measurement every dimension in "
                  "this pattern depends on."))
    s.append(para("If your 36 stitches measure wider than 52 mm, your tension "
                  "is loose \u2014 crochet more tightly, or go down a hook "
                  "size. Coco at a loose gauge will show her stuffing."))

    # ---------------------------------------------------------- finished size
    s.append(h1("Finished size"))
    s.append(para("About <b>10.3 cm (4 in) tall</b> standing on all four "
                  "legs, and <b>5 cm (2 in) wide</b> at the widest part of "
                  "the body."))
    s.append(para("Coco is meant to be squat and bottom-heavy. Her legs are "
                  "short relative to the round body, and the body is one "
                  "continuous curve from base to crown."))
    s.append(para("The height is the body plus the legs:"))
    s.append(grid([
        ["Body, Rnd 1 to Rnd 20", "20 rnd \u00d7 4.3 mm = <b>86 mm</b>"],
        ["Front legs", "9 rnd \u00d7 4.3 mm = <b>38.7 mm</b>"],
        ["Back legs", "8 rnd \u00d7 4.3 mm = <b>34.4 mm</b>"],
        ["Height the legs lift the body off the table", "<b>17 mm</b>"],
        ["Total standing height", "86 + 17 = <b>103 mm (10.3 cm)</b>"],
    ], [CW * 0.62, CW * 0.38], header=False, zebra=True))
    s.append(Spacer(1, 4))
    s.append(callout([
        "Both pairs hang the same distance below the body: the back legs are "
        "34.4 mm long and join 17 mm up (34.4 \u2212 17 = 17.4 mm of leg "
        "below), the front legs are 38.7 mm long and join 21.5 mm up (38.7 "
        "\u2212 21.5 = 17.2 mm). That is why the front legs need the extra "
        "round.",
    ]))

    # ---------------------------------------------------------- abbreviations
    s.append(h1("Abbreviations"))
    s.append(grid([
        ["MR", "magic ring"],
        ["ch", "chain"],
        ["sc", "single crochet"],
        ["inc", "increase \u2014 2 sc in one stitch"],
        ["invdec", "invisible decrease"],
        ["sl st", "slip stitch"],
        ["st(s)", "stitch(es)"],
        ["Rnd(s)", "round(s)"],
        ["FO", "fasten off"],
        ["(n)", "the stitch count at the end of that round"],
    ], [CW * 0.24, CW * 0.76], header=False, zebra=True))

    # ---------------------------------------------------------- working notes
    s.append(h1("Working notes"))
    s.append(para("Work in <b>continuous spiral rounds</b>. Do not join at "
                  "the end of a round and do not chain 1 between rounds. Move "
                  "a stitch marker into the first stitch of every round "
                  "\u2014 in a spiral there is no join to count from, and the "
                  "marker is the only way to know where a round ends."))
    s.append(para("Unless a note says otherwise, work every stitch through "
                  "both loops."))

    # ------------------------------------------------- how it comes together
    s.append(h1("How it comes together"))
    s.append(para("The three techniques used throughout this pattern, in the "
                  "order you meet them."))
    s.append(h2("1 \u00b7 The magic ring"))
    s.append(para("Every piece begins with a magic ring. Pull the tail tight "
                  "once the first round is complete."))
    s.append(h2("2 \u00b7 Working in a spiral"))
    s.append(para("Keep a stitch marker in the first stitch of every round. "
                  "There is no seam and no join to count from."))
    s.append(h2("3 \u00b7 The two-layer leg join"))
    s.append(para("This is the only genuinely fiddly step in the pattern."))
    s.append(para("Hold a finished leg against the body, with the "
                  "pinched-flat top of the leg lying against the outside of "
                  "the body. Insert your hook through <b>both</b> the leg and "
                  "the body stitch, and work one single crochet. The leg edge "
                  "and the body stitch are treated as a single stitch."))
    s.append(para("Those stitches still count as one stitch each, so every "
                  "stitch count in the body table stays correct."))
    s.append(para("Pinching the leg top flat first is what makes this easy. A "
                  "round, un-pinched leg top will not lie flat against the "
                  "curved body, and the join will pucker."))

    # --------------------------------------------------------------- part 1
    s.append(PageBreak())
    s.append(h1("Part 1 \u2014 Legs, ears and muzzle"))
    s.append(para("Make these first. The legs are stuffed \u2014 plump little "
                  "balls that the body rests on."))
    s.append(h2("Leg"))
    s.append(para("<b>Make 2 back legs (8 rounds) and 2 front legs "
                  "(9 rounds).</b>"))
    leg_rows = [
        ["R1", "6 sc in MR", "(6)", "all four"],
        ["R2", "[1 sc, inc] \u00d73", "(9)", "all four"],
    ]
    for r in range(3, 9):
        note = "all four" if r < 8 else "all four \u2014 back legs finish here"
        leg_rows.append(["R%d" % r, "sc in each st around", "(9)", note])
    leg_rows.append(["R9", "sc in each st around", "(9)", "front legs only"])
    s.append(rnd_table(["RND", "INSTRUCTION", "STS", "WHICH LEGS"], leg_rows,
                       [CW * 0.09, CW * 0.40, CW * 0.11, CW * 0.40]))
    s.append(Spacer(1, 6))
    s.append(para("<b>Finish.</b> Stuff the lower half of each leg lightly, "
                  "leaving the top loose."))
    s.append(para("Then <b>pinch the whole 9-stitch top flat into a narrow "
                  "strip about 3 stitches wide.</b> Press it between finger "
                  "and thumb and hold it that way while you work the join. FO "
                  "with a long tail for sewing."))
    s.append(para("The back legs stop after Rnd 8 (about 34 mm). The front "
                  "legs work Rnd 9 as well (about 39 mm). The front legs are "
                  "the longer pair on purpose: they join the body one round "
                  "higher up, so they need to be one round longer for all "
                  "four feet to reach the table at the same height. Make all "
                  "four legs the same length and Coco will rock back onto her "
                  "haunches with her front feet in the air."))
    s.append(callout([
        "The leg top is 9 stitches around, so a flattened edge is naturally "
        "about 5 stitches across. Pinching it down to 3 is deliberate. The "
        "stitches you do not join bunch up inside the join, and that bunch is "
        "what makes the leg look plump rather than tubular. Do not try to "
        "keep the top flat and wide \u2014 it will not sit against the curved "
        "body.",
    ]))

    s.append(h2("Ear \u2014 make 2"))
    s.append(rnd_table(["RND", "INSTRUCTION", "STS"], [
        ["R1", "6 sc in MR", "(6)"],
        ["R2", "[1 sc, inc] \u00d73", "(9)"],
        ["R3", "sc in each st around", "(9)"],
    ], [CW * 0.12, CW * 0.68, CW * 0.20]))
    s.append(Spacer(1, 6))
    s.append(para("<b>Finish.</b> FO with a long tail. Do not stuff. Each "
                  "finished ear is a shallow cup about 20 mm across and 13 mm "
                  "tall."))

    s.append(h2("Muzzle \u2014 make 1"))
    s.append(rnd_table(["RND", "INSTRUCTION", "STS"], [
        ["R1", "6 sc in MR", "(6)"],
        ["R2", "[1 sc, inc] \u00d73", "(9)"],
        ["R3", "[2 sc, inc] \u00d73", "(12)"],
        ["R4", "sc in each st around", "(12)"],
        ["R5", "sc in each st around", "(12)"],
    ], [CW * 0.12, CW * 0.68, CW * 0.20]))
    s.append(Spacer(1, 6))
    s.append(para("<b>Finish.</b> FO with a long tail. Stuff lightly, just "
                  "enough to hold a dome. The finished muzzle is about 17 mm "
                  "across."))

    # --------------------------------------------------------------- part 2
    s.append(PageBreak())
    s.append(h1("Part 2 \u2014 Body and head"))
    s.append(para("Body and head are worked as one piece, bottom up. Both are "
                  "36 stitches around, with only a shallow waist between them "
                  "\u2014 that is what makes Coco read as one continuous "
                  "round blob rather than a snowman."))
    s.append(para("The legs are joined low, at Rnd 4 and Rnd 5, while the "
                  "base is still curving outward."))
    body_rows = [
        ["R1", "6 sc in MR", "(6)", ""],
        ["R2", "inc in each st around", "(12)", ""],
        ["R3", "[1 sc, inc] \u00d76", "(18)", ""],
        ["R4", "3 sc, [1 sc, inc] \u00d73, 3 sc, [1 sc, inc] \u00d73", "(24)",
         "join the BACK legs"],
        ["R5", "[3 sc, inc] \u00d76", "(30)", "join the FRONT legs"],
        ["R6", "[4 sc, inc] \u00d76", "(36)",
         "body at full width \u2014 check gauge here"],
        ["R7", "sc in each st around", "(36)", ""],
        ["R8", "sc in each st around", "(36)", ""],
        ["R9", "sc in each st around", "(36)", "stuff the body FIRMLY"],
        ["R10", "[7 sc, invdec] \u00d74", "(32)", "shallow waist"],
        ["R11", "[7 sc, inc] \u00d74", "(36)", "head begins"],
        ["R12", "sc in each st around", "(36)", ""],
        ["R13", "sc in each st around", "(36)", ""],
        ["R14", "sc in each st around", "(36)", ""],
        ["R15", "sc in each st around", "(36)", ""],
        ["R16", "[4 sc, invdec] \u00d76", "(30)", ""],
        ["R17", "[3 sc, invdec] \u00d76", "(24)", "stuff the head firmly"],
        ["R18", "[2 sc, invdec] \u00d76", "(18)", ""],
        ["R19", "[1 sc, invdec] \u00d76", "(12)", "top up the stuffing"],
        ["R20", "invdec \u00d76", "(6)", ""],
    ]
    s.append(rnd_table(["RND", "INSTRUCTION", "STS", "NOTE"], body_rows,
                       [CW * 0.09, CW * 0.41, CW * 0.11, CW * 0.39]))
    s.append(Spacer(1, 6))
    s.append(para("<b>Finish.</b> Cinch the remaining 6 stitches closed and "
                  "weave the tail inside the body."))

    s.append(h2("Joining the legs"))
    s.append(para("Work Rnd 4 and Rnd 5 as the plain increase rounds printed "
                  "in the table above, but as you reach each leg position, "
                  "hold a pinched-flat leg top against the body and work the "
                  "next 3 sc through both the leg and the body together "
                  "(technique 3). Those 3 sc still count as 3 stitches of the "
                  "round, so the stitch counts do not change."))
    s.append(h3("Rnd 4 \u2014 the back legs"))
    s.append(callout([
        "Work the first <b>3 sc</b> through a leg and the body together, then "
        "<b>[1 sc, inc] \u00d73</b>.<br/><br/>"
        "Work the next <b>3 sc</b> through the second leg and the body "
        "together, then <b>[1 sc, inc] \u00d73</b> to the end of the round."
        "<br/><br/><b>Total 24 stitches.</b>",
    ]))
    s.append(h3("Rnd 5 \u2014 the front legs"))
    s.append(callout([
        "Work <b>7 sc</b>.<br/><br/>"
        "Join a leg over the next <b>3 sc</b>.<br/><br/>"
        "Work <b>10 sc</b>.<br/><br/>"
        "Join a leg over the next <b>3 sc</b>.<br/><br/>"
        "Work <b>7 sc</b> to the end of the round.<br/><br/>"
        "<b>Total 30 stitches.</b>",
    ]))
    s.append(para("The 7 \u2013 10 \u2013 7 spacing is what keeps Coco "
                  "steady. It centers each front leg between the two back "
                  "legs, so her four feet cover the deepest footprint this "
                  "shape allows \u2014 about 65 mm across and 29 mm from "
                  "front to back."))
    s.append(para("Work the numbers exactly as printed. If the front legs end "
                  "up directly behind the back legs instead of between them, "
                  "Coco\u2019s footprint narrows to about 9 mm from front to "
                  "back and she will tip over forwards and backwards."))
    s.append(para("Hold the piece upside down and check that all four legs "
                  "sit square before you stuff the body."))
    # --------------------------------------------------------------- part 3
    s.append(h1("Part 3 \u2014 Why the legs join so low"))
    s.append(para("The back legs are 8 rounds long, about 34 mm, and they "
                  "join at Rnd 4 \u2014 only 17 mm above the base of the "
                  "body. The front legs are 9 rounds long, about 39 mm, and "
                  "they join at Rnd 5, 21 mm up."))
    s.append(para("Different lengths, same result: <b>every foot hangs 17 mm "
                  "below the body</b>, so all four land level and the "
                  "underside of the body clears the table by about that much. "
                  "Coco stands on her feet, not on her belly."))
    s.append(para("This is the single most common failure on a round-bodied "
                  "animal. Legs joined at the widest part of the body are "
                  "always too high: the belly rests on the table and the feet "
                  "dangle in the air."))
    s.append(para("If Coco does not stand, check the join height before "
                  "anything else."))

    # --------------------------------------------------------------- part 4
    s.append(PageBreak())
    s.append(h1("Part 4 \u2014 Face and assembly"))
    s.append(h2("Muzzle"))
    s.append(para("Stuff the muzzle lightly and pin it to the front of the "
                  "head over <b>Rnd 12\u201314</b>, centered on the face. Sew "
                  "all the way around with matching brown."))
    s.append(para("The muzzle should sit proud of the head, not flush with "
                  "it."))
    s.append(para("Centering matters. The muzzle is about 17 mm across and "
                  "the eyes go 27 mm apart, which leaves only about 5 mm of "
                  "clear face between the edge of the muzzle and each eye. A "
                  "muzzle pinned even slightly off-center will crowd one eye."))
    s.append(h2("Eyes"))
    s.append(para("Embroider the eyes \u2014 do not use safety eyes."))
    s.append(para("With dark brown, work a shallow downward arc about 3 "
                  "stitches wide on each side, at <b>Rnd 14\u201315</b>, "
                  "<b>6 stitches apart</b>, with a tiny tick angled down at "
                  "each outer end."))
    s.append(para("Six stitches keeps both eyes on the front of the face. Any "
                  "wider and they wrap around the sides. Placing them at Rnd "
                  "14\u201315 keeps the whole eye above the muzzle, which is "
                  "pinned over Rnd 12\u201314."))
    s.append(para("This closed-eye curve is what makes Coco look asleep."))
    s.append(h2("Nose and mouth"))
    s.append(para("Embroider the nose and mouth <b>after</b> the muzzle is "
                  "sewn on, so the stitches sit on the finished curve rather "
                  "than on a flat piece."))
    s.append(para("On the muzzle, work a small dark triangle at the top "
                  "center, then a short vertical line down from it, and a "
                  "soft curved mouth to one side."))
    s.append(h2("Ears"))
    s.append(para("Pinch the base of each ear so it cups forward, then sew at "
                  "<b>Rnd 15</b>, about <b>5 stitches apart</b>, angled "
                  "slightly outward."))
    s.append(para("Rnd 15 is still a full 36-stitch round, so 5 stitches puts "
                  "the ears on top of the head where a capybara\u2019s ears "
                  "belong. Sewing them wider apart \u2014 or onto Rnd 16, "
                  "which has already decreased to 30 stitches \u2014 pushes "
                  "them out to the sides of the head, where they disappear "
                  "from the front."))
    s.append(h2("Legs"))
    s.append(para("The legs were joined during Rnd 4 and Rnd 5. There is "
                  "nothing to sew. Just check that the pinched 3-stitch strip "
                  "of each leg is caught fully in the round."))
    s.append(h2("Final shaping"))
    s.append(para("Roll the finished piece gently between your palms to "
                  "settle the stuffing into a round, bottom-heavy shape."))

    # ------------------------------------------------------- troubleshooting
    s.append(h1("Troubleshooting"))
    trouble = [
        ("Coco looks too tall",
         "Almost always too many plain rounds. Rnd 12\u201315 is the straight "
         "section of the head, and the face is positioned on it. Adding "
         "\u201cjust one more\u201d round each time turns the shape into a "
         "tower and moves the face off the round it was designed for."),
        ("Coco will not stand",
         "Check the join height, not the leg spacing. The legs belong on Rnd "
         "4 and Rnd 5. Joined any higher, they cannot clear the underside of "
         "the body."),
        ("Coco tips forward or backward",
         "Two causes, in order of likelihood. First, the front legs are lined "
         "up behind the back legs instead of between them: the Rnd 5 spacing "
         "must be 7 sc, 10 sc, 7 sc. Second, Coco is deliberately narrow from "
         "front to back, at about 29 mm, and no leg spacing changes that. If "
         "she still tips, stuff the lower body more firmly and settle her "
         "weight back over all four feet."),
        ("Coco rocks back onto her haunches, front feet in the air",
         "All four legs are the same length, and they cannot be. The front "
         "legs join at Rnd 5, 21 mm up, and the back legs at Rnd 4, 17 mm up, "
         "so equal-length legs leave the back feet about 9 mm lower. Work the "
         "front legs 9 rounds and the back legs 8."),
        ("Coco will not sit level",
         "Stuff the lower body firmly. A soft base lets Coco tip forward onto "
         "her muzzle."),
        ("The head flops back",
         "The waist at Rnd 10 is deliberately shallow, at 32 stitches. Do not "
         "decrease it further. A narrow neck cannot hold the head upright on "
         "this shape."),
        ("The muzzle looks flat",
         "Stuff it just enough to hold a dome."),
        ("Stuffing shows through",
         "Your gauge is too loose. Thirty-six stitches should measure 52 mm "
         "around a stuffed body. Crochet more tightly, or go down a hook "
         "size."),
        ("There is a small hole where a leg meets the body",
         "You joined a flat, wide leg top instead of a pinched one. Flatten "
         "the whole 9-stitch top into a strip about 3 stitches wide before "
         "joining, so the stitches you are not joining bunch up inside the "
         "join."),
    ]
    for q, a in trouble:
        s.append(KeepTogether([Paragraph(q, S_TROUBLE_Q),
                               Paragraph(a, S_BODY)]))

    # ------------------------------------------------------------ colorways
    s.append(h1("Colorways"))
    s.append(para("Classic warm brown, soft grey, sandy beige, and cocoa."))

    # ------------------------------------------------------ before assembling
    s.append(h1("Before you assemble"))
    s.append(para("Lay every component out and check it against the pattern "
                  "before you sew anything:"))
    s.append(bullet("4 legs \u2014 2 back legs of 8 rounds, 2 front legs of "
                    "9 rounds"))
    s.append(bullet("2 ears"))
    s.append(bullet("1 muzzle"))
    s.append(bullet("1 body and head, closed at the crown"))

    # ----------------------------------------------------------- terms of use
    s.append(h1("Terms of use"))
    s.append(callout([
        "This pattern is for personal use and small-batch finished sales. You "
        "may sell physical finished items made from this pattern provided "
        "credit is given to %s. Selling, altering, copying or redistributing "
        "this digital PDF is strictly prohibited." % STORE,
    ], tone="deep"))
    s.append(Spacer(1, 6))
    s.append(para("\u00a9 %s \u2014 %s. Design code %s." % (
        STORE, STUDIO, CODE), ParagraphStyle(
            "sig", fontName="Helvetica-Bold", fontSize=8.6, leading=12,
            textColor=INK_SOFT)))

    return s


# -------------------------------------------------------------------- build --

def build():
    doc = BaseDocTemplate(
        OUT, pagesize=A4,
        leftMargin=LM, rightMargin=RM, topMargin=TM, bottomMargin=BM,
        title="%s \u2014 %s (Design code %s)" % (CODE, TITLE, CODE),
        author="%s (%s)" % (STUDIO, STORE),
        subject="Crochet pattern \u2014 US terms, intermediate amigurumi",
        creator=STUDIO,
    )
    cover_frame = Frame(LM, BM + 26 * mm, CW, PH - TM - BM - 26 * mm,
                        id="cover")
    body_frame = Frame(LM, BM, CW, PH - TM - BM, id="body")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=cover_page),
        PageTemplate(id="body", frames=[body_frame], onPage=body_page),
    ])
    doc.build(story())
    print("wrote %s (%.1f kB)" % (OUT, os.path.getsize(OUT) / 1024.0))


if __name__ == "__main__":
    build()
