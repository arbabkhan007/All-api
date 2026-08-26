"""Reusable PIL components for the Novality Store Etsy listing graphics.

All typography is drawn programmatically (no AI text) so every label is
crisp and typo-free. Table mockups mirror the real workbook's styling.
"""
from PIL import Image, ImageDraw, ImageFont
import math
import os

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
FONTS = "/usr/share/fonts/truetype/dejavu"

# ------------------------------------------------------------ palette
ROSE    = (183, 110, 121)   # B76E79
ROSE_D  = (138, 90, 102)    # 8A5A66
PLUM    = (110, 76, 91)     # 6E4C5B
HEADER  = (201, 145, 156)   # C9919C
CREAM   = (255, 251, 239)   # FFFBEF
GREY    = (243, 239, 239)   # F3EFEF
TOTALBG = (235, 217, 221)   # EBD9DD
BORDERC = (220, 195, 201)   # DCC3C9
INK     = (46, 42, 43)
SUBINK  = (110, 95, 100)
GOLD    = (201, 162, 39)
GOLD_D  = (176, 141, 22)
SAGE    = (156, 175, 136)
WHITE   = (255, 255, 255)
IVORY   = (253, 248, 240)
BLUSH   = (247, 216, 222)
SUBROSE = (246, 231, 234)

_fonts = {}


def font(name, size):
    key = (name, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(os.path.join(FONTS, name), size)
    return _fonts[key]


def serif(size, bold=False):
    return font("DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf", size)


def sans(size, bold=False):
    return font("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", size)


# ------------------------------------------------------------ text ops
def text_w(draw, txt, fnt):
    return draw.textlength(txt, font=fnt)


def spaced(draw, xy, txt, fnt, fill, tracking=0, anchor_left=True):
    """Letter-spaced text. Returns total width."""
    x, y = xy
    total = sum(draw.textlength(c, font=fnt) + tracking for c in txt) - tracking
    if not anchor_left:
        x -= total / 2
    for c in txt:
        draw.text((x, y), c, font=fnt, fill=fill)
        x += draw.textlength(c, font=fnt) + tracking
    return total


def centered(draw, xy, txt, fnt, fill):
    draw.text(xy, txt, font=fnt, fill=fill, anchor="mm")


# ------------------------------------------------------------ shapes
def rrect(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline,
                           width=width)


def card(draw, box, radius=28, fill=WHITE, shadow=True, outline=BORDERC):
    x0, y0, x1, y1 = box
    if shadow:
        # soft offset shadow (solid tint — alpha is ignored on RGB canvases)
        draw.rounded_rectangle((x0 + 10, y0 + 14, x1 + 10, y1 + 14),
                               radius=radius, fill=(224, 204, 212))
    rrect(draw, box, radius, fill=fill, outline=outline, width=3)


def pill(draw, cx, cy, txt, fnt, fg, bg, padx=34, pady=18, outline=None):
    w = draw.textlength(txt, font=fnt)
    asc, desc = fnt.getmetrics()
    h = asc + desc
    box = (cx - w / 2 - padx, cy - h / 2 - pady, cx + w / 2 + padx, cy + h / 2 + pady)
    rrect(draw, box, (box[3] - box[1]) / 2, fill=bg, outline=outline, width=3)
    draw.text((cx, cy), txt, font=fnt, fill=fg, anchor="mm")
    return box


def padlock(draw, cx, cy, scale=1.0, body=ROSE, shackle=ROSE_D):
    s = scale
    bw, bh = 150 * s, 116 * s
    r = 26 * s
    # shackle
    draw.arc((cx - 52 * s, cy - 108 * s, cx + 52 * s, cy + 4 * s),
             start=180, end=360, fill=shackle, width=int(20 * s))
    # body
    rrect(draw, (cx - bw / 2, cy - 18 * s, cx + bw / 2, cy - 18 * s + bh),
          radius=r, fill=body)
    # keyhole
    draw.ellipse((cx - 16 * s, cy + 24 * s, cx + 16 * s, cy + 56 * s), fill=WHITE)
    draw.rectangle((cx - 7 * s, cy + 44 * s, cx + 7 * s, cy + 74 * s), fill=WHITE)


def pie(draw, cx, cy, r, slices):
    """slices: list of (label, value, color). Drawn from 12 o'clock."""
    total = sum(v for _, v, _ in slices)
    start = -90.0
    for label, val, color in slices:
        if val <= 0:
            continue
        sweep = 360.0 * val / total
        draw.pieslice((cx - r, cy - r, cx + r, cy + r), start, start + sweep,
                      fill=color, outline=WHITE, width=4)
        start += sweep
    # donut hole
    hr = int(r * 0.55)
    draw.ellipse((cx - hr, cy - hr, cx + hr, cy + hr), fill=WHITE)


def cover_resize(src_path, w, h):
    """Cover-crop an image to exactly (w, h)."""
    img = Image.open(src_path).convert("RGB")
    sw, sh = img.size
    scale = max(w / sw, h / sh)
    img = img.resize((int(sw * scale + 0.5), int(sh * scale + 0.5)),
                     Image.LANCZOS)
    left = (img.width - w) // 2
    top = (img.height - h) // 2
    return img.crop((left, top, left + w, top + h))


def new_canvas(w, h, bg=WHITE):
    img = Image.new("RGB", (w, h), bg)
    return img, ImageDraw.Draw(img)


# ------------------------------------------------------------ tables
def draw_table(draw, x, y, widths, headers, rows, rh=62, hh=66,
               body=34, header_size=30, grid=True, header_fill=HEADER,
               first_bold=False, last_total=True, max_rows=None):
    """
    widths: list of px widths; headers: list[str];
    rows: list of list[(text, kind)] kind in input/formula/plain/total/center
    Returns (total_w, total_h).
    """
    widths = widths[:len(headers)]
    tw = sum(widths)
    # header row
    rrect(draw, (x, y, x + tw, y + hh), 18, fill=header_fill)
    cx = x
    for wcol, htxt in zip(widths, headers):
        draw.text((cx + 18, y + hh / 2), htxt, font=sans(header_size, True),
                  fill=WHITE, anchor="lm")
        cx += wcol
    yy = y + hh
    nrows = rows if max_rows is None else rows[:max_rows]
    for ri, row in enumerate(nrows):
        is_total = any(k == "total" for _, k in row)
        fill = TOTALBG if is_total else (WHITE if ri % 2 == 0 else IVORY)
        cx = x
        for ci, (val, kind) in enumerate(row):
            draw.rectangle((cx, yy, cx + widths[ci], yy + rh), fill=fill)
            if grid:
                draw.rectangle((cx, yy, cx + widths[ci], yy + rh),
                               outline=(238, 224, 228), width=2)
            if kind == "total":
                fnt, col = sans(body - 4, True), PLUM
            elif kind == "formula":
                fnt, col = sans(body - 4), SUBINK
            elif kind == "plain":
                fnt, col = sans(body - 4), INK
            else:
                fnt, col = sans(body - 4), INK
            pad = 18 if ci == 0 else 14
            align = "lm"
            tx = cx + pad
            if kind in ("center", "formula") and ci > 0 and kind == "center":
                tx = cx + widths[ci] / 2
                align = "mm"
            elif kind == "formula" and ci > 0:
                tx = cx + widths[ci] - pad
                align = "rm"
            draw.text((tx, yy + rh / 2), str(val), font=fnt, fill=col, anchor=align)
            if is_total and ci == len(row) - 1:
                pass
            cx += widths[ci]
        yy += rh
    return tw, yy - y


def draw_statrow(draw, x, y, stats, boxw=330, gap=40, h=150):
    """stats: list of (label, value, accent). Content vertically centred."""
    for i, (lab, val, accent) in enumerate(stats):
        bx = x + i * (boxw + gap)
        card(draw, (bx, y, bx + boxw, y + h), radius=24, fill=WHITE,
             shadow=False, outline=BORDERC)
        draw.rectangle((bx, y + 8, bx + 8, y + h - 8), fill=accent)
        draw.text((bx + 26, y + h * 0.30), lab.upper(), font=sans(22, True),
                  fill=SUBINK)
        draw.text((bx + 26, y + h * 0.62), val, font=serif(44, True),
                  fill=PLUM)
