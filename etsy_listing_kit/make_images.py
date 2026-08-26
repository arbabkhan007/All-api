"""Compose the full Etsy listing kit for Wedding Planner V2 (Novality Store).

Outputs 10 listing images (2700x2025, Etsy's 4:3), 2 Pinterest pins
(1000x1500) and a contact sheet — all brand-consistent, all typography
drawn programmatically from the real workbook's data.
"""
import os
from datetime import date, timedelta

from PIL import Image, ImageDraw

import mockups as M
from mockups import (ROSE, ROSE_D, PLUM, HEADER, CREAM, GREY, TOTALBG,
                     BORDERC, INK, SUBINK, GOLD, GOLD_D, SAGE, WHITE, IVORY,
                     BLUSH, SUBROSE, serif, sans, spaced, centered, pill,
                     rrect, card, padlock, pie, cover_resize, new_canvas,
                     draw_table, draw_statrow)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "images")
os.makedirs(OUT, exist_ok=True)

W, H = 2700, 2025
BG_MAIN = os.path.join(M.ASSETS, "bg_floral_main.png")
BG_SOFT = os.path.join(M.ASSETS, "bg_floral_soft.png")
BG_TALL = os.path.join(M.ASSETS, "bg_floral_tall.png")

WED_DATE = date(2027, 5, 22)
DAYS_TO_GO = (WED_DATE - date.today()).days

# --------------------------------------------------------------- data ---
BUDGET_ROWS = [
    ("Venue & rental",        8500,  8000, 2000),
    ("Catering & bar",       12000, 11500, 3000),
    ("Wedding cake",           650,   650,  200),
    ("Bridal attire",         1800,  1750,  600),
    ("Groom & party attire",   950,   900,  300),
    ("Hair & makeup",          600,   550,  150),
    ("Flowers & décor",       2800,  None,  700),
    ("Photography",           3200,  None,  800),
]
EST_TOTAL = 45450
ACT_TOTAL = 23350
DEP_TOTAL = 8750
BAL_TOTAL = 35550

GUESTS = [
    ("Ava Thompson",  "Bride",  "College friends", "Confirmed", "Chicken",     "Yes", "3"),
    ("Noah Bennett",  "Groom",  "Family",          "Confirmed", "Beef",        "No",  "5"),
    ("Olivia Carter", "Bride",  "Family",          "Confirmed", "Vegetarian",  "No",  "2"),
    ("Liam Nguyen",   "Groom",  "College friends", "Pending",   "TBD",         "No",  "—"),
    ("Emma Whitfield","Bride",  "Work",            "Declined",  "—",           "No",  "—"),
    ("Sophia Reyes",  "Both",   "Neighbors",       "Confirmed", "Fish",        "Yes", "7"),
    ("Ethan Brooks",  "Groom",  "Family",          "Pending",   "TBD",         "Yes", "5"),
    ("Mia Delgado",   "Bride",  "College friends", "Confirmed", "Gluten-Free", "No",  "3"),
]

MEALS = [("Chicken", 1, (201, 145, 156)), ("Beef", 1, (138, 90, 102)),
         ("Fish", 1, (156, 175, 136)), ("Vegetarian", 1, (212, 180, 131)),
         ("Vegan", 0, (183, 110, 121)), ("Gluten-Free", 1, (110, 76, 91)),
         ("Kids Meal", 0, (220, 195, 201))]

COUNTDOWN = [
    ("12 Months Before", "Set the date & book the officiant",
     (WED_DATE - timedelta(days=365)), "To Do"),
    ("6 Months Before", "Book caterer, photographer & DJ",
     (WED_DATE - timedelta(days=183)), "To Do"),
    ("3 Months Before", "Final guest list · order invitations",
     (WED_DATE - timedelta(days=91)), "In Progress"),
    ("1 Month Before", "Mail invitations · apply for license",
     (WED_DATE - timedelta(days=30)), "To Do"),
    ("1 Week Before", "Confirm vendors · pack emergency kit",
     (WED_DATE - timedelta(days=7)), "To Do"),
    ("Day-Of", "CEREMONY — you're getting married!",
     WED_DATE, "To Do"),
]

TIMELINE = [
    ("7:00 AM", "Wake up, breakfast & hydrate", "Suite"),
    ("9:30 AM", "Photographer arrives — details", "Suite"),
    ("10:30 AM", "Get dressed · first look", "Garden"),
    ("11:45 AM", "Family formal photos", "Ceremony lawn"),
    ("2:00 PM", "CEREMONY", "Ceremony lawn"),
    ("2:45 PM", "Cocktail hour · portraits", "Terrace"),
    ("4:15 PM", "Dinner service", "Reception barn"),
    ("10:00 PM", "Sparkler send-off", "Estate drive"),
]

CATEGORY_CARDS = [
    ("Big Picture",  4, "Dashboard · Countdown · Vision", ROSE),
    ("Budget",       4, "Master budget · Payments", SAGE),
    ("Guests",       5, "Guest list · Seating · Meals", (217, 139, 163)),
    ("Vendors",      2, "Contacts · Comparison", (157, 129, 137)),
    ("Attire",       5, "Dresses · Groom · Beauty", (195, 137, 155)),
    ("Décor",        5, "Florals · Stationery · Theme", (212, 180, 131)),
    ("Catering",     5, "Menu · Cake · Bar", (201, 123, 99)),
    ("Day-Of",       6, "Timeline · Emergency kit", PLUM),
    ("Music & Photos", 7, "Songs · Shot list", (142, 154, 175)),
    ("Extras",       8, "Honeymoon · Vows · Legal", (127, 166, 160)),
]


def money(v):
    return "$" + format(int(v), ",")


def fmt_date(d):
    return d.strftime("%d %b %Y").lstrip("0")


# ----------------------------------------------------------- templates ---
def brand_footer(d, idx, total=10):
    spaced(d, (170, H - 92), "NOVALITY STORE", sans(26, True), ROSE_D, 8)
    d.text((W - 170, H - 92), f"{idx:02d} / {total}", font=sans(26),
           fill=SUBINK, anchor="rm")


def feature_header(d, eyebrow, title, subtitle=None):
    spaced(d, (170, 110), eyebrow.upper(), sans(34, True), ROSE, 10)
    d.text((166, 160), title, font=serif(128, True), fill=PLUM)
    if subtitle:
        d.text((170, 330), subtitle, font=sans(46), fill=SUBINK)


def browser_frame(img, d, box, url="novality.store/wedding-planner-v2"):
    x0, y0, x1, y1 = box
    card(d, box, radius=30, fill=WHITE)
    bar_h = 84
    d.rounded_rectangle((x0, y0, x1, y0 + bar_h + 2), radius=30,
                        fill=SUBROSE)
    d.rectangle((x0, y0 + bar_h - 24, x1, y0 + bar_h + 2), fill=SUBROSE)
    d.rounded_rectangle((x0, y0, x1, y0 + bar_h), radius=30, fill=None)
    for i, c in enumerate(((234, 132, 132), (240, 197, 128), (150, 206, 137))):
        d.ellipse((x0 + 34 + i * 52, y0 + bar_h / 2 - 12,
                   x0 + 34 + i * 52 + 24, y0 + bar_h / 2 + 12), fill=c)
    pill(d, (x0 + x1) / 2, y0 + bar_h / 2, url, sans(26), SUBINK, WHITE,
         padx=40, pady=12, outline=BORDERC)
    return y0 + bar_h + 10


def sheet_banner(d, x, y, w, title):
    d.rounded_rectangle((x, y, x + w, y + 56), radius=14, fill=ROSE)
    d.text((x + 24, y + 28), title, font=serif(30, True), fill=WHITE,
           anchor="lm")


# ================================================================ slides
def slide01_hero():
    img = cover_resize(BG_MAIN, W, H)
    d = ImageDraw.Draw(img)
    cx = W / 2
    spaced(d, (cx, 330), "NOVALITY STORE", sans(40, True), ROSE_D, 14,
           anchor_left=False)
    d.text((cx, 470), "Wedding Planner", font=serif(215, True), fill=PLUM,
           anchor="mm")
    spaced(d, (cx, 640), "S P R E A D S H E E T", sans(66), ROSE, 10,
           anchor_left=False)

    pill(d, cx - 640, 810, "52 TABS", sans(40, True), WHITE, ROSE)
    pill(d, cx, 810, "AUTO FORMULAS", sans(40, True), PLUM, WHITE,
         outline=BORDERC)
    pill(d, cx + 640, 810, "INSTANT DOWNLOAD", sans(40, True), WHITE, SAGE)

    # mini dashboard teaser card
    card(d, (cx - 900, 990, cx + 900, 1660), radius=34, fill=WHITE)
    y = 990 + 84
    d.rounded_rectangle((cx - 900, 990, cx + 900, 990 + 86), radius=34,
                        fill=SUBROSE)
    d.rectangle((cx - 900, 990 + 60, cx + 900, 990 + 86), fill=SUBROSE)
    d.text((cx, 990 + 43), "LIVE DASHBOARD — EVERYTHING UPDATES ITSELF",
           font=sans(30, True), fill=PLUM, anchor="mm")
    stats = [("Days to go", str(DAYS_TO_GO), ROSE),
             ("Budget", money(EST_TOTAL), SAGE),
             ("Guests", "8 invited", (201, 123, 99)),
             ("Vendors", "8 of 11 booked", (142, 154, 175))]
    bw = 1650
    for i, (lab, val, accent) in enumerate(stats):
        bx = cx - bw / 2 + i * (bw / 4)
        draw_statrow(d, bx, y + 60, [(lab, val, accent)], boxw=bw / 4 - 60,
                     gap=0, h=300)
    d.line((cx - 780, 1520, cx + 780, 1520), fill=(238, 224, 228), width=3)
    d.text((cx, 1585), "Budget  ·  Guest list  ·  Countdown  ·  Seating  ·  "
                       "Vendors  ·  Honeymoon", font=sans(38), fill=SUBINK,
           anchor="mm")
    spaced(d, (cx, 1770), "VERSION 2", serif(52, True), GOLD_D, 12,
           anchor_left=False)
    img.save(os.path.join(OUT, "01_main_hero.jpg"), quality=92)


def slide02_dashboard():
    img, d = new_canvas(W, H, (250, 240, 242))
    d.rectangle((0, 0, W, 14), fill=ROSE)
    feature_header(d, "The command centre", "Wedding Overview Dashboard",
                   "Date, venue, theme & color palette — with live counters "
                   "for budget, guests and to-dos.")
    fx0, fy0, fx1, fy1 = 170, 470, W - 170, H - 190
    y = browser_frame(img, d, (fx0, fy0, fx1, fy1))
    iw = fx1 - fx0 - 120
    x0 = fx0 + 60

    sheet_banner(d, x0, y, iw, "WEDDING OVERVIEW DASHBOARD")
    y += 86
    labels = [("Partner 1", "Alex Morgan"), ("Partner 2", "Jordan Lee"),
              ("Wedding Date", "22 May 2027"), ("Ceremony Time", "4:00 PM"),
              ("Venue", "The Rosewood Estate"),
              ("Theme / Style", "Romantic garden party")]
    col1 = 420
    for lab, val in labels:
        d.text((x0 + 20, y + 30), lab, font=sans(30, True), fill=SUBINK)
        d.rounded_rectangle((x0 + col1, y, x0 + col1 + 640, y + 60),
                            radius=10, fill=CREAM, outline=BORDERC)
        d.text((x0 + col1 + 20, y + 30), val, font=sans(30), fill=INK,
               anchor="lm")
        y += 74
    # days-to-go block
    card(d, (x0 + col1 + 690, 470 + 84 + 16, x0 + iw - 20, 470 + 84 + 16 + 380),
         radius=24, fill=SUBROSE, shadow=False, outline=BORDERC)
    d.text((x0 + col1 + 690 + 210, 470 + 84 + 16 + 120),
           str(DAYS_TO_GO), font=serif(150, True), fill=PLUM, anchor="mm")
    d.text((x0 + col1 + 690 + 210, 470 + 84 + 16 + 260),
           "DAYS TO GO", font=sans(34, True), fill=ROSE_D, anchor="mm")

    # stats row
    y += 24
    stats = [("Estimated", money(EST_TOTAL), SAGE),
             ("Deposits paid", money(DEP_TOTAL), GOLD),
             ("Balance due", money(BAL_TOTAL), ROSE),
             ("Confirmed", "5 guests", (217, 139, 163)),
             ("Checklist", "0% done", (142, 154, 175))]
    bw = (iw - 4 * 30) / 5
    for i, s in enumerate(stats):
        draw_statrow(d, x0 + i * (bw + 30), y, [s], boxw=bw, gap=0, h=170)

    brand_footer(d, 2)
    img.save(os.path.join(OUT, "02_dashboard.jpg"), quality=92)


def budget_table_rows(n=8, total=True):
    rows = []
    for name, est, act, dep in BUDGET_ROWS[:n]:
        base = act if act is not None else est
        rows.append([
            (name, "plain"),
            (money(est), "formula"),
            (money(act) if act else "—", "formula"),
            (money(dep) if dep else "—", "formula"),
            (money(base - dep), "formula"),
        ])
    if total:
        rows.append([("TOTAL", "total"), (money(EST_TOTAL), "total"),
                     (money(ACT_TOTAL), "total"), (money(DEP_TOTAL), "total"),
                     (money(BAL_TOTAL), "total")])
    return rows


def slide03_budget():
    img, d = new_canvas(W, H, (243, 245, 238))
    d.rectangle((0, 0, W, 14), fill=SAGE)
    feature_header(d, "Money, mastered", "Master Budget & Payments",
                   "Estimated vs actual, deposits paid, balance due — every "
                   "figure calculates itself, nothing gets deleted.")
    # left: master budget table in browser frame
    fx0, fy0, fx1, fy1 = 170, 480, 1660, H - 180
    y = browser_frame(img, d, (fx0, fy0, fx1, fy1))
    widths = [520, 220, 220, 220, 230]
    headers = ["Category", "Estimated", "Actual", "Deposit", "Balance"]
    rows = budget_table_rows(8)
    draw_table(d, fx0 + 50, y + 30, widths, headers, rows, rh=88, hh=90,
               body=36, header_size=32)
    d.text((fx0 + 50, fy1 - 120),
           "🔒  Grey cells = protected formulas — cream cells are yours to "
           "type in".replace("🔒", ""), font=sans(32), fill=SUBINK)

    # right: breakdown donut card
    cx0, cy0, cx1, cy1 = 1720, 480, W - 170, H - 180
    card(d, (cx0, cy0, cx1, cy1), radius=30, fill=WHITE)
    d.text(((cx0 + cx1) / 2, cy0 + 70), "BUDGET BREAKDOWN", font=sans(34, True),
           fill=ROSE_D, anchor="mm")
    slices = [("Venue", 8000, (183, 110, 121)), ("Catering", 11500, (138, 90, 102)),
              ("Cake", 650, (212, 180, 131)), ("Attire", 1750, (156, 175, 136)),
              ("Groom", 900, (110, 76, 91)), ("Hair & makeup", 550, (201, 145, 156))]
    pie(d, cx0 + 330, cy0 + 430, 240, slices)
    d.text((cx0 + 330, cy0 + 430), money(ACT_TOTAL), font=sans(38, True),
           fill=PLUM, anchor="mm")
    ly = cy0 + 220
    for label, val, color in slices:
        d.rounded_rectangle((cx0 + 640, ly, cx0 + 680, ly + 40), radius=8,
                            fill=color)
        d.text((cx0 + 706, ly + 20), f"{label} — {money(val)}",
               font=sans(30), fill=INK, anchor="lm")
        ly += 66
    pill(d, (cx0 + cx1) / 2, cy1 - 90, "LIVE PIE CHART INCLUDED", sans(32, True),
         WHITE, PLUM)
    brand_footer(d, 3)
    img.save(os.path.join(OUT, "03_budget.jpg"), quality=92)


def slide04_guests():
    img, d = new_canvas(W, H, (250, 240, 244))
    d.rectangle((0, 0, W, 14), fill=(217, 139, 163))
    feature_header(d, "Everyone accounted for", "Guest Management Hub",
                   "One master list feeds the invitations tracker, meal "
                   "counts, seating chart and thank-you cards.")
    fx0, fy0, fx1, fy1 = 170, 480, W - 170, 1440
    y = browser_frame(img, d, (fx0, fy0, fx1, fy1))
    widths = [430, 210, 400, 300, 330, 190, 210]
    headers = ["Guest", "Side", "Group", "RSVP", "Meal", "+1", "Table"]
    rows = [[(n, "plain"), (s, "center"), (g, "plain"), (r, "center"),
             (m, "center"), (p, "center"), (t, "center")]
            for n, s, g, r, m, p, t in GUESTS]
    rows.append([("LIVE STATS", "total"), ("8 invited", "total"),
                 ("5 confirmed", "total"), ("1 declined", "total"),
                 ("2 awaiting", "total"), ("2 with +1", "total"),
                 ("", "total")])
    draw_table(d, fx0 + 50, y + 26, widths, headers, rows, rh=78, hh=84,
               body=33, header_size=30)

    y2 = 1520
    stats = [("Invited", "8", (217, 139, 163)),
             ("Confirmed", "5", SAGE),
             ("Awaiting reply", "2", GOLD),
             ("Meals auto-counted", "7 types", PLUM),
             ("Tables in use", "6", (142, 154, 175))]
    bw = (W - 340 - 4 * 36) / 5
    for i, (lab, val, acc) in enumerate(stats):
        draw_statrow(d, 170 + i * (bw + 36), y2, [(lab, val, acc)],
                     boxw=bw, gap=0, h=180)
    d.text((W / 2, 1800),
           "Meal Count Summary tab — caterer-ready counts with a live chart",
           font=sans(36), fill=SUBINK, anchor="mm")
    brand_footer(d, 4)
    img.save(os.path.join(OUT, "04_guests.jpg"), quality=92)


def slide05_whats_inside():
    img, d = new_canvas(W, H, (250, 242, 238))
    d.rectangle((0, 0, W, 14), fill=GOLD)
    feature_header(d, "Take a peek inside", "52 Beautifully Linked Tabs",
                   "Ten organised sections cover every single part of "
                   "planning — from the first mood board to the last thank-you.")
    gx0, gy0 = 170, 500
    cw, ch = (W - 340 - 4 * 40) / 5, 560
    for i, (cat, ntabs, detail, accent) in enumerate(CATEGORY_CARDS):
        r, c = divmod(i, 5)
        x = gx0 + c * (cw + 40)
        y = gy0 + r * (ch + 40)
        card(d, (x, y, x + cw, y + ch), radius=30, fill=WHITE, shadow=False)
        d.rounded_rectangle((x, y, x + cw, y + 22), radius=8, fill=accent)
        d.text((x + 30, y + 90), f"{ntabs} tabs", font=sans(28, True),
               fill=ROSE)
        d.text((x + 30, y + 150), cat, font=serif(48, True), fill=PLUM)
        # wrapped detail
        words, line, ly = detail.split(), "", y + 260
        fnt = sans(31)
        for wd in words:
            t = (line + " " + wd).strip()
            if d.textlength(t, font=fnt) > cw - 60:
                d.text((x + 30, ly), line, font=fnt, fill=SUBINK)
                ly += 46
                line = wd
            else:
                line = t
        d.text((x + 30, ly), line, font=fnt, fill=SUBINK)
        d.text((x + 30, y + ch - 90), "✓ auto-formulas", font=sans(26),
               fill=GOLD_D)
    d.text((W / 2, gy0 + 2 * ch + 150),
           "+ Start Here index with clickable links to every tab",
           font=sans(38, True), fill=ROSE_D, anchor="mm")
    brand_footer(d, 5)
    img.save(os.path.join(OUT, "05_whats_inside.jpg"), quality=92)


def slide06_how():
    img, d = new_canvas(W, H, (238, 242, 250))
    d.rectangle((0, 0, W, 14), fill=(142, 154, 175))
    feature_header(d, "Effortless by design", "How It Works",
                   "No setup, no formulas to write — open, type, done.")
    steps = [
        ("1", "Download instantly", "Your file arrives right after "
         "checkout — no waiting, no shipping."),
        ("2", "Type in the cream cells", "Guests, vendors, payments, "
         "dates — just like a normal spreadsheet."),
        ("3", "Formulas do the rest", "Balances, counts, countdowns and "
         "charts update automatically."),
    ]
    cw = (W - 340 - 2 * 60) / 3
    for i, (num, head, body) in enumerate(steps):
        x = 170 + i * (cw + 60)
        y = 520
        card(d, (x, y, x + cw, y + 640), radius=36, fill=WHITE)
        d.ellipse((x + cw / 2 - 90, y - 60, x + cw / 2 + 90, y + 120),
                  fill=ROSE)
        d.text((x + cw / 2, y + 26), num, font=serif(96, True), fill=WHITE,
               anchor="mm")
        d.text((x + cw / 2, y + 240), head, font=serif(56, True), fill=PLUM,
               anchor="mm")
        words, line, ly = body.split(), "", y + 340
        fnt = sans(34)
        for wd in words:
            t = (line + " " + wd).strip()
            if d.textlength(t, font=fnt) > cw - 100:
                d.text((x + 50, ly), line, font=fnt, fill=SUBINK)
                ly += 50
                line = wd
            else:
                line = t
        d.text((x + 50, ly), line, font=fnt, fill=SUBINK)
    # legend demo
    y = 1350
    d.text((170, y), "THE COLOR CODE:", font=sans(34, True), fill=SUBINK)
    d.rounded_rectangle((170 + 470, y - 30, 170 + 470 + 620, y + 60),
                        radius=14, fill=CREAM, outline=BORDERC)
    d.text((170 + 490, y + 15), "Cream = your input", font=sans(34),
           fill=INK)
    d.rounded_rectangle((170 + 1150, y - 30, 170 + 1150 + 620, y + 60),
                        radius=14, fill=GREY, outline=BORDERC)
    d.text((170 + 1170, y + 15), "Grey = locked formula", font=sans(34),
           fill=SUBINK)
    d.text((W / 2, y + 200), "Works in Microsoft Excel  ·  opens in Google "
           "Sheets", font=sans(38), fill=ROSE_D, anchor="mm")
    brand_footer(d, 6)
    img.save(os.path.join(OUT, "06_how_it_works.jpg"), quality=92)


def slide07_locked():
    img, d = new_canvas(W, H, (244, 240, 250))
    d.rectangle((0, 0, W, 14), fill=PLUM)
    feature_header(d, "Premium template, protected", "Lock-Down Formulas",
                   "Every calculation is password-protected, so your planner "
                   "never breaks — no matter who edits it.")
    padlock(d, 480, 1000, scale=2.2)
    bx = 900
    items = [
        "1,390+ formulas calculating balances, countdowns & counts",
        "Sheets protected with a password — totals can't be broken",
        "Your input cells stay fully editable (cream cells)",
        "Perfect for sharing with a partner or planner",
    ]
    ly = 700
    for it in items:
        d.ellipse((bx, ly + 8, bx + 44, ly + 52), fill=ROSE)
        d.text((bx + 22, ly + 30), "✓", font=sans(30, True), fill=WHITE,
               anchor="mm")
        d.text((bx + 80, ly + 30), it, font=sans(42), fill=INK, anchor="lm")
        ly += 110
    # demo mini-table
    fx0, fy0 = bx, 1210
    y = browser_frame(img, d, (bx, 1210, W - 170, 1720))
    widths = [560, 340, 340, 330]
    headers = ["Category", "Deposit", "Balance", "Status"]
    rows = [
        [("Venue & rental", "plain"), ("$2,000", "formula"),
         ("$6,000", "formula"), ("Signed", "center")],
        [("Catering & bar", "plain"), ("$3,000", "formula"),
         ("$8,500", "formula"), ("Booked", "center")],
        [("Photography", "plain"), ("$800", "formula"),
         ("$2,400", "formula"), ("Booked", "center")],
    ]
    draw_table(d, bx + 50, y + 20, widths, headers, rows, rh=82, hh=84,
               body=34, header_size=30)
    pill(d, (bx + (W - 170)) / 2, 1790, "PASSWORD-PROTECTED PREMIUM BUILD",
         sans(34, True), WHITE, ROSE)
    brand_footer(d, 7)
    img.save(os.path.join(OUT, "07_locked_formulas.jpg"), quality=92)


def slide08_dayof():
    img, d = new_canvas(W, H, (250, 241, 243))
    d.rectangle((0, 0, W, 14), fill=PLUM)
    feature_header(d, "Never miss a deadline", "Countdown to “I Do”",
                   "A 12-month checklist with automatic target dates, plus "
                   "an hour-by-hour wedding day timeline.")
    fx0, fy0, fx1, fy1 = 170, 490, 1600, H - 170
    y = browser_frame(img, d, (fx0, fy0, fx1, fy1))
    sheet_banner(d, fx0 + 50, y + 20, fx1 - fx0 - 100, "COUNTDOWN CHECKLIST")
    widths = [420, 640, 320]
    headers = ["Phase", "Task", "Target date"]
    rows = [[(p, "plain"), (t, "plain"), (fmt_date(dt), "formula")]
            for p, t, dt, _s in COUNTDOWN]
    draw_table(d, fx0 + 50, y + 100, widths, headers, rows, rh=86, hh=88,
               body=34, header_size=30)

    gx0, gy0, gx1, gy1 = 1660, 490, W - 170, H - 170
    y2 = browser_frame(img, d, (gx0, gy0, gx1, gy1))
    sheet_banner(d, gx0 + 50, y2 + 20, gx1 - gx0 - 100, "WEDDING DAY TIMELINE")
    widths2 = [260, 560]
    headers2 = ["Time", "Event"]
    rows2 = [[(t, "center"), (e, "plain")] for t, e, _l in TIMELINE]
    draw_table(d, gx0 + 50, y2 + 100, widths2, headers2, rows2, rh=80, hh=84,
               body=33, header_size=30)
    d.text(((fx0 + fx1) / 2, fy1 - 10),
           "6 phases · 44 pre-written tasks", font=sans(30), fill=SUBINK,
           anchor="rm")
    brand_footer(d, 8)
    img.save(os.path.join(OUT, "08_dayof.jpg"), quality=92)


def slide09_extras():
    img, d = new_canvas(W, H, (243, 247, 243))
    d.rectangle((0, 0, W, 14), fill=(127, 166, 160))
    feature_header(d, "The finishing touches", "Every Extra You Need",
                   "Vows, hashtags, honeymoon, registry, legal deadlines — "
                   "the details other planners forget.")
    # palette strip card
    card(d, (170, 500, W - 170, 800), radius=30, fill=WHITE)
    d.text((230, 560), "COLOR PALETTE BUILDER", font=sans(32, True),
           fill=ROSE_D)
    swatches = [(247, 216, 222), (227, 166, 179), (183, 110, 121),
                (156, 175, 136), (212, 180, 131), (234, 216, 195),
                (253, 248, 240), (110, 76, 91)]
    names = ["Blush", "Dusty rose", "Rose gold", "Sage", "Gold",
             "Champagne", "Ivory", "Plum"]
    sx = 230
    for (c, nm) in zip(swatches, names):
        d.rounded_rectangle((sx, 610, sx + 250, 720), radius=18, fill=c,
                            outline=BORDERC)
        d.text((sx + 125, 750), nm, font=sans(28), fill=SUBINK, anchor="mm")
        sx += 280
    # three mini cards
    cw = (W - 340 - 2 * 60) / 3
    x = 170
    # vows
    card(d, (x, 880, x + cw, 1560), radius=30, fill=WHITE)
    d.text((x + 40, 950), "VOW WORKSHEET", font=sans(34, True), fill=ROSE_D)
    d.rounded_rectangle((x + 40, 1020, x + cw - 40, 1120), radius=12,
                        fill=CREAM, outline=BORDERC)
    d.text((x + 64, 1070), "How we met & my first", font=sans(32), fill=INK)
    d.rounded_rectangle((x + 40, 1140, x + cw - 40, 1240), radius=12,
                        fill=CREAM, outline=BORDERC)
    d.text((x + 64, 1190), "The moment I knew…", font=sans(32), fill=INK)
    d.rounded_rectangle((x + 40, 1260, x + cw - 40, 1360), radius=12,
                        fill=CREAM, outline=BORDERC)
    d.text((x + 64, 1310), "I promise to always…", font=sans(32), fill=INK)
    d.text((x + 40, 1450), "6 guided prompts", font=sans(30), fill=SUBINK)
    x += cw + 60
    # honeymoon
    card(d, (x, 880, x + cw, 1560), radius=30, fill=WHITE)
    d.text((x + 40, 950), "HONEYMOON BUDGET", font=sans(34, True), fill=ROSE_D)
    widths = [300, 180, 160]
    headers = ["Item", "Est.", "Actual"]
    rows = [[("Flights", "plain"), ("$2,400", "formula"), ("", "formula")],
            [("Lodging", "plain"), ("$2,100", "formula"), ("", "formula")],
            [("Activities", "plain"), ("$700", "formula"), ("", "formula")],
            [("TOTAL", "total"), ("$6,600", "total"), ("", "total")]]
    draw_table(d, x + 40, 1020, widths, headers, rows, rh=76, hh=80,
               body=28, header_size=26, max_rows=4)
    d.text((x + 40, 1450), "Itinerary & packing list included",
           font=sans(30), fill=SUBINK)
    x += cw + 60
    # legal
    card(d, (x, 880, x + cw, 1560), radius=30, fill=WHITE)
    d.text((x + 40, 950), "LEGAL DEADLINES", font=sans(34, True), fill=ROSE_D)
    rows = [[("Apply for license", "plain"), ("26 Mar 2027", "formula")],
            [("Pick up license", "plain"), ("01 May 2027", "formula")],
            [("Return signed", "plain"), ("29 May 2027", "formula")]]
    draw_table(d, x + 40, 1020, [370, 276], ["Requirement", "By"],
               rows, rh=76, hh=80, body=28, header_size=26, max_rows=3)
    d.text((x + 40, 1450), "Auto-set from your wedding date",
           font=sans(30), fill=SUBINK)
    d.text((W / 2, 1700), "Plus: name-change checklist · registry · favors · "
           "thank-you tracker · hashtag planner",
           font=sans(38, True), fill=ROSE_D, anchor="mm")
    brand_footer(d, 9)
    img.save(os.path.join(OUT, "09_extras.jpg"), quality=92)


def slide10_delivery():
    img = cover_resize(BG_MAIN, W, H)
    d = ImageDraw.Draw(img)
    cx = W / 2
    spaced(d, (cx, 260), "THANK YOU & HAPPY PLANNING", sans(44, True),
           ROSE_D, 12, anchor_left=False)
    d.text((cx, 420), "Start planning in minutes", font=serif(120, True),
           fill=PLUM, anchor="mm")
    steps = [
        ("Instant download", "Files arrive the moment your order completes"),
        ("Open in Excel", "One .xlsx file — nothing to install"),
        ("Begin at Start Here", "A clickable index walks you through it all"),
    ]
    cw = 700
    for i, (head, body) in enumerate(steps):
        x = cx - (3 * cw + 2 * 60) / 2 + i * (cw + 60)
        card(d, (x, 620, x + cw, 1120), radius=34, fill=WHITE)
        d.ellipse((x + cw / 2 - 60, 580, x + cw / 2 + 60, 700), fill=GOLD)
        d.text((x + cw / 2, 640), str(i + 1), font=serif(70, True),
               fill=WHITE, anchor="mm")
        d.text((x + cw / 2, 790), head, font=serif(52, True), fill=PLUM,
               anchor="mm")
        words, line, ly = body.split(), "", 880
        fnt = sans(32)
        for wd in words:
            t = (line + " " + wd).strip()
            if d.textlength(t, font=fnt) > cw - 80:
                d.text((x + 50, ly), line, font=fnt, fill=SUBINK)
                ly += 46
                line = wd
            else:
                line = t
        d.text((x + 50, ly), line, font=fnt, fill=SUBINK)
    pill(d, cx, 1320, "YOU GET:  52-TAB PLANNER (.XLSX)  +  FRIENDLY SUPPORT",
         sans(34, True), WHITE, PLUM)
    d.text((cx, 1480),
           "This is a digital product — no physical item will be shipped.",
           font=sans(34), fill=SUBINK, anchor="mm")
    spaced(d, (cx, 1650), "NOVALITY STORE", serif(60, True), ROSE_D, 14,
           anchor_left=False)
    d.text((cx, 1730), "Wedding Planner Spreadsheet · Version 2 · "
           "© Novality Store — personal use",
           font=sans(30), fill=SUBINK, anchor="mm")
    img.save(os.path.join(OUT, "10_delivery.jpg"), quality=92)


# ---------------------------------------------------------------- pins ---
def pin_one():
    img = cover_resize(BG_TALL, 1000, 1500)
    d = ImageDraw.Draw(img)
    pill(d, 500, 250, "NOVALITY STORE", sans(26, True), WHITE, ROSE)
    d.text((500, 400), "Wedding Planner", font=serif(92, True), fill=PLUM,
           anchor="mm")
    d.text((500, 490), "Spreadsheet", font=serif(92, True), fill=PLUM,
           anchor="mm")
    d.text((500, 580), "52 tabs · auto formulas · instant download",
           font=sans(28), fill=SUBINK, anchor="mm")
    card(d, (100, 660, 900, 1180), radius=30, fill=WHITE)
    widths = [360, 200, 180]
    headers = ["Category", "Est.", "Deposit"]
    rows = [[("Venue", "plain"), ("$8,500", "formula"), ("$2,000", "formula")],
            [("Catering", "plain"), ("$12,000", "formula"), ("$3,000", "formula")],
            [("Photography", "plain"), ("$3,200", "formula"), ("$800", "formula")],
            [("Florals", "plain"), ("$2,800", "formula"), ("$700", "formula")],
            [("TOTAL", "total"), ("$45,450", "total"), ("", "total")]]
    draw_table(d, 140, 700, widths, headers, rows, rh=64, hh=66, body=26,
               header_size=24, max_rows=5)
    pill(d, 500, 1290, "SAVE THIS PIN", sans(30, True), WHITE, SAGE)
    img.save(os.path.join(OUT, "pin_01_save.jpg"), quality=92)


def pin_two():
    img = cover_resize(BG_TALL, 1000, 1500)
    d = ImageDraw.Draw(img)
    d.text((500, 300), "Plan your entire", font=serif(76, True), fill=PLUM,
           anchor="mm")
    d.text((500, 390), "wedding in ONE", font=serif(76, True), fill=PLUM,
           anchor="mm")
    d.text((500, 480), "spreadsheet", font=serif(76, True), fill=ROSE,
           anchor="mm")
    cats = ["Budget & payments", "Guest list & seating", "Countdown checklists",
            "Vendors & contracts", "Meals, cake & bar", "Vows & honeymoon"]
    y = 610
    for c in cats:
        d.rounded_rectangle((150, y, 850, y + 84), radius=42, fill=WHITE,
                            outline=BORDERC)
        d.ellipse((176, y + 26, 216, y + 66), fill=SAGE)
        d.text((196, y + 46), "✓", font=sans(26, True), fill=WHITE,
               anchor="mm")
        d.text((240, y + 42), c, font=sans(34), fill=INK, anchor="lm")
        y += 108
    pill(d, 500, y + 60, "INSTANT DOWNLOAD", sans(30, True), WHITE, ROSE)
    spaced(d, (500, y + 150), "NOVALITY STORE", sans(24, True), ROSE_D, 8,
           anchor_left=False)
    img.save(os.path.join(OUT, "pin_02_checklist.jpg"), quality=92)


# -------------------------------------------------------- contact sheet --
def contact_sheet():
    files = sorted(f for f in os.listdir(OUT)
                   if f.startswith(("0", "1")) and f.endswith(".jpg"))
    tw, th, gap = 530, 398, 18
    cols = 5
    rows = (len(files) + cols - 1) // cols
    img = Image.new("RGB", (cols * tw + (cols + 1) * gap,
                            rows * th + (rows + 1) * gap + 90), (245, 240, 242))
    d = ImageDraw.Draw(img)
    d.text((gap + 4, 18), "ETSY LISTING KIT — Wedding Planner V2 (Novality "
           "Store)", font=sans(34, True), fill=PLUM)
    for i, f in enumerate(files):
        r, c = divmod(i, cols)
        x = gap + c * (tw + gap)
        y = 90 + r * (th + gap)
        thumb = Image.open(os.path.join(OUT, f)).resize((tw, th),
                                                        Image.LANCZOS)
        img.paste(thumb, (x, y))
        d.rectangle((x, y, x + tw, y + th), outline=BORDERC, width=2)
        d.text((x + 8, y + th + 2), f, font=sans(20), fill=SUBINK)
    img.save(os.path.join(HERE, "contact_sheet.jpg"), quality=90)
    print("contact sheet:", len(files), "slides")


if __name__ == "__main__":
    slide01_hero()
    slide02_dashboard()
    slide03_budget()
    slide04_guests()
    slide05_whats_inside()
    slide06_how()
    slide07_locked()
    slide08_dayof()
    slide09_extras()
    slide10_delivery()
    pin_one()
    pin_two()
    contact_sheet()
    print("done →", OUT)
