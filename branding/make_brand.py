#!/usr/bin/env python3
"""NovalityStore — brand system generator.
Palette: warm cream / deep plum ink / coral / sage / gold.
Renders: shop logo (square), icon (badge), wide lockup, shop banner (4:1).
All drawing done at 2x then downscaled for crisp anti-aliasing.
"""
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

S = 2  # supersample factor
FONT = "fonts/Quicksand-{}.ttf"

# ---------- palette ----------
CREAM    = (253, 248, 241)
INK      = (56, 38, 66)
INK_SOFT = (122, 102, 134)
CORAL    = (237, 122, 85)
SAGE     = (148, 174, 143)
GOLD     = (228, 178, 92)
BLUSH    = (246, 226, 210)
WHITE    = (255, 255, 255)

def f(weight, size):
    return ImageFont.truetype(FONT.format(weight), int(round(size * S)))

def px(v):
    return v * S

def sparkle_pts(cx, cy, r, k=0.26):
    return [
        (cx, cy - r), (cx + k * r, cy - k * r), (cx + r, cy), (cx + k * r, cy + k * r),
        (cx, cy + r), (cx - k * r, cy + k * r), (cx - r, cy), (cx - k * r, cy - k * r),
    ]

def draw_sparkle(d, cx, cy, r, color, alpha=255):
    fill = color if len(color) == 4 else color + (alpha,)
    d.polygon(sparkle_pts(px(cx), px(cy), px(r)), fill=fill)

def dtext(d, x, y, txt, font, fill):
    d.text((px(x), px(y)), txt, font=font, fill=fill)

def text_w(d, txt, font):
    return d.textlength(txt, font=font) / S

def tracking_w(d, txt, font, tracking):
    return sum(d.textlength(c, font=font) / S for c in txt) + tracking * (len(txt) - 1)

def draw_tracking(d, xy, txt, font, fill, tracking):
    x, y = xy
    for ch in txt:
        d.text((px(x), px(y)), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) / S + tracking

def soft_blob(img, cx, cy, r, color, alpha):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([px(cx - r), px(cy - r), px(cx + r), px(cy + r)], fill=color + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(px(r * 0.45)))
    img.alpha_composite(layer)

def dot_grid(img, spacing, r, color, alpha):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    w, h = img.size
    for x in range(0, w, int(px(spacing))):
        for y in range(0, h, int(px(spacing))):
            d.ellipse([x - px(r), y - px(r), x + px(r), y + px(r)], fill=color + (alpha,))
    img.alpha_composite(layer)

def rounded_shadow(img, box, radius, color=INK, alpha=55, blur=16, dy=7):
    x0, y0, x1, y1 = [px(v) for v in box]
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([x0, y0 + px(dy), x1, y1 + px(dy)], radius=px(radius), fill=color + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(px(blur)))
    img.alpha_composite(layer)

# ---------- badge (N monogram) ----------
def draw_badge(img, x, y, size, shadow=False):
    if shadow:
        rounded_shadow(img, (x, y, x + size, y + size), size * 0.24)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([px(x), px(y), px(x + size), px(y + size)],
                        radius=px(size * 0.24), fill=INK + (255,))
    inset = size * 0.05
    d.rounded_rectangle([px(x + inset), px(y + inset), px(x + size - inset), px(y + size - inset)],
                        radius=px(size * 0.205), outline=(255, 255, 255, 24), width=int(round(px(2))))
    cw, ch = size * 0.42, size * 0.54
    cx, cy = x + size / 2, y + size / 2
    xl, xr = cx - cw / 2, cx + cw / 2
    yt, yb = cy - ch / 2, cy + ch / 2
    sw = size * 0.115
    def line(p1, p2, color):
        d.line([px(p1[0]), px(p1[1]), px(p2[0]), px(p2[1])], fill=color, width=int(round(px(sw))))
        for p in (p1, p2):
            d.ellipse([px(p[0] - sw / 2), px(p[1] - sw / 2), px(p[0] + sw / 2), px(p[1] + sw / 2)], fill=color)
    line((xl, yb), (xl, yt), CREAM + (255,))
    line((xr, yb), (xr, yt), CREAM + (255,))
    line((xl, yt), (xr, yb), CORAL + (255,))
    draw_sparkle(d, x + size * 0.775, y + size * 0.245, size * 0.072, GOLD + (255,))

# ---------- wordmark with sparkle i-dot ----------
def draw_wordmark(img, word, x, y, size, color=INK, dot_color=CORAL):
    """word drawn at logical (x, y); the i dot is replaced by a four-point sparkle."""
    font = f(700, size)
    d = ImageDraw.Draw(img)
    # mask for the text
    mask = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(mask)
    md.text((px(x), px(y)), word, font=font, fill=255)
    # scan the standalone 'i' glyph to find the dot band (rows)
    cell = Image.new("L", (px(160), px(200)), 0)
    ImageDraw.Draw(cell).text((0, 0), "i", font=font, fill=255)
    rows = []
    data = cell.tobytes()
    cw = cell.width
    for yy in range(cell.height):
        if max(data[yy * cw:(yy + 1) * cw]) > 128:
            rows.append(yy)
    band = [rows[0]]
    for r_ in rows[1:]:
        if r_ - band[-1] <= 1:
            band.append(r_)
        else:
            break
    bbox_i = font.getbbox("i")  # physical px, relative to origin
    prefix = word[:word.index("i")]
    i_left = px(x) + text_w(d, prefix, font) * S
    pad = px(size * 0.05)
    dot_x0 = i_left + px(bbox_i[0]) + pad * 0.35
    dot_x1 = i_left + px(bbox_i[2]) - pad * 0.35
    dot_y0 = px(y) + band[0] - pad
    dot_y1 = px(y) + band[-1] + pad
    ImageDraw.Draw(mask).rectangle([dot_x0, dot_y0, dot_x1, dot_y1], fill=0)
    layer = Image.new("RGBA", img.size, color + (255,))
    layer.putalpha(mask)
    img.alpha_composite(layer)
    draw_sparkle(d, (dot_x0 + dot_x1) / 2 / S, (dot_y0 + dot_y1) / 2 / S,
                 size * 0.150, dot_color + (255,))

def glyph_h(font, word="novality"):
    b = font.getbbox(word)
    return (b[3] - b[1]) / S

# ---------- assets ----------
def make_square_logo():
    CW = 800  # logical; canvas rendered at 2x
    img = Image.new("RGBA", (px(CW), px(CW)), CREAM + (255,))
    d = ImageDraw.Draw(img)
    draw_sparkle(d, CW * 0.088, CW * 0.098, 12, GOLD + (255,))
    draw_sparkle(d, CW * 0.912, CW * 0.125, 8, CORAL + (255,))
    draw_sparkle(d, CW * 0.928, CW * 0.898, 11, SAGE + (255,))
    draw_sparkle(d, CW * 0.078, CW * 0.902, 7, GOLD + (220,))
    badge_s = 320
    bx = (CW - badge_s) / 2
    by = 70
    draw_badge(img, bx, by, badge_s, shadow=True)
    wm_size = 93
    wm_w = text_w(d, "novality", f(700, wm_size))
    wm_x = (CW - wm_w) / 2
    wm_y = by + badge_s + 52
    draw_wordmark(img, "novality", wm_x, wm_y, wm_size)
    tag_size = 25
    tag_font = f(600, tag_size)
    tag = "S T O R E"
    tw = text_w(d, tag, tag_font)
    ty = wm_y + glyph_h(f(700, wm_size)) + 21
    dtext(d, (CW - tw) / 2, ty, tag, tag_font, CORAL + (255,))
    img.resize((800, 800), Image.LANCZOS).save("out/logo-shop-800.png")
    img.resize((400, 400), Image.LANCZOS).save("out/logo-shop-400.png")
    img.resize((200, 200), Image.LANCZOS).save("out/logo-shop-200.png")

def make_icon():
    img = Image.new("RGBA", (px(600), px(600)), (0, 0, 0, 0))
    draw_badge(img, 45, 45, 510, shadow=True)
    img.resize((600, 600), Image.LANCZOS).save("out/logo-icon-600.png")
    img.resize((400, 400), Image.LANCZOS).save("out/logo-icon-400.png")
    img.resize((128, 128), Image.LANCZOS).save("out/logo-icon-128.png")

def make_lockup(path):
    W, H = 1200, 360  # logical
    img = Image.new("RGBA", (px(W), px(H)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    badge_s = H * 0.60
    bx = H * 0.16
    by = (H - badge_s) / 2
    draw_badge(img, bx, by, badge_s)
    tx = bx + badge_s + H * 0.15
    wm_size = H * 0.245
    tag = "SMART DIGITAL GOODS"
    tag_size = H * 0.062
    tag_font = f(600, tag_size)
    tag_track = H * 0.026
    wm_h = glyph_h(f(700, wm_size))
    total_h = wm_h + H * 0.08 + glyph_h(tag_font, "S")
    top = (H - total_h) / 2
    draw_wordmark(img, "novality", tx, top, wm_size)
    draw_tracking(d, (tx, top + wm_h + H * 0.08), tag, tag_font, INK_SOFT + (255,), tag_track)
    img.save(path)

def make_banner():
    BW, BH = 2400, 600
    img = Image.new("RGBA", (BW, BH), CREAM + (255,))
    soft_blob(img, 2200, 20, 400, BLUSH, 190)
    soft_blob(img, 60, 640, 360, (215, 229, 209), 160)
    soft_blob(img, 1200, -80, 280, (250, 236, 205), 140)
    dot_grid(img, 30, 1.7, SAGE, 50)
    d = ImageDraw.Draw(img)
    draw_sparkle(d, 1122, 62, 14, GOLD + (255,))
    draw_sparkle(d, 588, 250, 8, CORAL + (255,))
    draw_sparkle(d, 1080, 256, 8, SAGE + (255,))
    draw_sparkle(d, 646, 56, 6, GOLD + (220,))
    draw_sparkle(d, 1168, 152, 9, CORAL + (170,))
    # dotted divider
    for yy in range(52, 250, 13):
        d.ellipse([px(548) - px(1.8), px(yy) - px(1.8), px(548) + px(1.8), px(yy) + px(1.8)],
                  fill=INK_SOFT + (105,))
    # left lockup
    badge_s = 164
    draw_badge(img, 54, (300 - badge_s) / 2, badge_s, shadow=True)
    tx = 54 + badge_s + 28
    wm_size = 58
    tag = "SMART DIGITAL GOODS"
    tag_size = 15
    tag_font = f(600, tag_size)
    tag_track = 4.0
    wm_h = glyph_h(f(700, wm_size))
    total_h = wm_h + 11 + glyph_h(tag_font, "S")
    top = (300 - total_h) / 2 + 4
    draw_wordmark(img, "novality", tx, top, wm_size)
    draw_tracking(d, (tx, top + wm_h + 11), tag, tag_font, INK_SOFT + (255,), tag_track)
    # right content
    cx = (600 + 1146) / 2
    tagline = "Smart digital solutions for creative minds"
    tl_font = f(600, 24)
    tl_w = text_w(d, tagline, tl_font)
    dtext(d, cx - tl_w / 2, 78, tagline, tl_font, INK + (255,))
    chips = [
        ("Crochet Patterns", CORAL), ("Finance Planners", SAGE),
        ("Kids' Printables", GOLD), ("Travel & Events", (186, 148, 180)),
    ]
    chip_font = f(600, 18)
    def chip(t):
        return text_w(d, t, chip_font) + 42
    for row, yrow in ((chips[:2], 138), (chips[2:], 188)):
        ws = [chip(t) for t, _ in row]
        gap = 20
        x0 = cx - (sum(ws) + gap * (len(row) - 1)) / 2
        for (t, acc), w in zip(row, ws):
            d.rounded_rectangle([px(x0), px(yrow), px(x0 + w), px(yrow + 38)],
                                radius=px(19), fill=WHITE + (232,),
                                outline=acc + (255,), width=int(round(px(2.2))))
            tw = text_w(d, t, chip_font)
            dtext(d, x0 + (w - tw) / 2, yrow + 9.8, t, chip_font, INK + (255,))
            x0 += w + gap
    foot = "Instant digital downloads   •   Washington, USA"
    ft_font = f(500, 14.5)
    fw = text_w(d, foot, ft_font)
    dtext(d, cx - fw / 2, 258, foot, ft_font, INK_SOFT + (255,))
    img.convert("RGB").resize((1200, 300), Image.LANCZOS).save("out/banner-1200x300.png")
    img.convert("RGB").resize((1680, 420), Image.LANCZOS).save("out/banner-1680x420.png")

def main():
    os.makedirs("out", exist_ok=True)
    make_square_logo()
    make_icon()
    make_lockup("out/logo-lockup-2400.png")
    make_banner()
    print("done")

if __name__ == "__main__":
    main()
