"""Wedding Planner V2 — Big Picture Planning sheets (Novality Store)."""
from datetime import date
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.hyperlink import Hyperlink

from core import (AUTHOR, VERSION, PRODUCT, MONEY, PCT, DATEF, DAYS, INT,
                  sheet_shell, section, put_input, put_formula, put_label,
                  merged_input, stat_pair, make_table, status_cf, protect,
                  CHECK_OPTS, GREEN, AMBER, RED, TOTAL_FILL, LABEL_FONT,
                  SECTION_FILL, ref)

TAB = "B76E79"

# sheet index shown on the Start Here tab
INDEX = [
    ("BIG PICTURE PLANNING", [
        ("Dashboard", "Wedding overview — date, venue, theme, budget & live counters"),
        ("Countdown Checklist", "12-month, 6-month, 3-month, 1-month, 1-week & day-of tasks"),
        ("Vision Board", "Mood, style keywords and inspiration sources"),
        ("Priority Ranking", "Rank the 3–5 things that matter most"),
    ]),
    ("BUDGET & FINANCE", [
        ("Master Budget", "Estimated vs actual, deposits paid & balance due per category"),
        ("Payment Tracker", "Every vendor payment — due dates, amounts & status"),
        ("Budget Breakdown", "Category totals, % of budget and a live pie chart"),
        ("Contributions", "Cash fund & who is contributing what"),
    ]),
    ("GUEST MANAGEMENT", [
        ("Guest List", "Master list — RSVP, meal choice, +1 and table number"),
        ("Invitations Tracker", "Save-the-dates, invitations and RSVP replies"),
        ("Seating Chart", "Assign confirmed guests to reception tables"),
        ("Hotel & Welcome Bags", "Out-of-town guests, room blocks & welcome bags"),
        ("Meal Count Summary", "Caterer-ready meal & dietary counts (auto-calculated)"),
    ]),
    ("VENDOR MANAGEMENT", [
        ("Vendor Contacts", "All 11 vendor categories — contacts, contracts & balances"),
        ("Vendor Comparison", "Side-by-side comparison of 2–3 options per category"),
    ]),
    ("ATTIRE & BEAUTY", [
        ("Dress Shopping Log", "Stores, styles, prices & alterations timeline"),
        ("Bridesmaid Dresses", "Sizes, colors, orders & delivery status"),
        ("Groom & Groomsmen", "Suit/tux details, rental vs purchase & fittings"),
        ("Hair & Makeup Trials", "Artists, looks, products & trial notes"),
        ("Beauty Timeline", "Skincare, whitening, tanning & nails schedule"),
    ]),
    ("DÉCOR & DESIGN", [
        ("Colors & Theme", "Palette swatches and theme keywords"),
        ("Floral Planner", "Bouquets, centerpieces, ceremony flowers & costs"),
        ("Ceremony Décor", "Arch, aisle, signage & programs checklist"),
        ("Reception Décor", "Centerpieces, lighting, draping & backdrop checklist"),
        ("Stationery Checklist", "Invitations, RSVPs, menus, place cards & signage"),
    ]),
    ("CATERING & MENU", [
        ("Menu Planning", "Appetizers, mains, sides & desserts"),
        ("Cake Design", "Tiers, flavors, fillings & payment balance"),
        ("Bar & Drinks", "Signature cocktails, wine, beer & non-alcoholic"),
        ("Tasting Notes", "Caterer & bakery tasting appointments and ratings"),
        ("Late-Night Snacks", "Ideas, quantities and costs for the midnight run"),
    ]),
    ("TIMELINE & DAY-OF", [
        ("Wedding Day Timeline", "Hour-by-hour from getting ready to send-off"),
        ("Rehearsal Dinner", "Guest list, venue, menu & toasts"),
        ("Ceremony Order", "Processional, readings, vows & recessional"),
        ("Reception Timeline", "Grand entrance, dances, toasts & cake cutting"),
        ("Emergency Kit", "Day-of survival kit checklist"),
        ("Vendor Arrivals", "Who arrives when on the wedding day"),
    ]),
    ("MUSIC & PHOTOS", [
        ("Ceremony Songs", "Processional, interlude & recessional music"),
        ("Reception Playlist", "Must-play and do-not-play lists"),
        ("Special Dances", "First dance, father-daughter & mother-son songs"),
        ("Entertainment Ideas", "Photo booth, live painter, fireworks & more"),
        ("Shot List", "Must-have photos & candid moments"),
        ("Family Photos", "Formal portrait groupings"),
        ("Video Moments", "Video must-capture list"),
    ]),
    ("EXTRAS", [
        ("Honeymoon Planner", "Destination, budget, itinerary & packing list"),
        ("Name Change Checklist", "Social security, license, bank, passport…"),
        ("Favors Tracker", "Favor ideas, quantities & spend"),
        ("Thank You Cards", "Gifts received & thank-you status (auto)"),
        ("Registry Checklist", "Stores, items & purchased status"),
        ("Vow Worksheet", "Guided prompts to write your vows"),
        ("Hashtag & Social", "Hashtag ideas & social media plan"),
        ("Legal & Officiant", "Marriage license, deadlines & witnesses"),
    ]),
]


# ------------------------------------------------------------------ start
def start_here(wb):
    ws = wb.create_sheet("Start Here")
    sheet_shell(ws, "6E4C5B", "✨  WEDDING PLANNER — VERSION 2.0",
                f"{PRODUCT}  •  {AUTHOR}  •  {VERSION}", "H")
    for col, w in zip("BCDEFGH", (24, 18, 18, 18, 18, 18, 14)):
        ws.column_dimensions[col].width = w

    r = 5
    section(ws, r, "ABOUT THIS WORKBOOK", "B", "H")
    facts = [
        ("Workbook", f"{PRODUCT} — {VERSION}"),
        ("Author", AUTHOR),
        ("Tabs", f"{1 + sum(len(s) for _, s in INDEX)} beautifully linked planning sheets"),
        ("Protection", "Every formula cell is locked — sheets are password-protected"),
    ]
    for i, (k, v) in enumerate(facts, start=1):
        put_label(ws, f"B{r + i}", k)
        ws.merge_cells(f"C{r + i}:H{r + i}")
        c = ws[f"C{r + i}"]
        c.value = v
        c.font = Font(size=10, color="2E2A2B")
        c.alignment = Alignment(horizontal="left", vertical="center")
    r += len(facts) + 2

    section(ws, r, "HOW IT WORKS", "B", "H")
    hows = [
        "1.  Start on the Dashboard — set your wedding date and every countdown updates itself.",
        "2.  Fill in the cream cells. Grey cells are formulas — they calculate automatically and are locked.",
        "3.  Each sheet is protected so formulas can't be deleted by accident (Review ▸ Unprotect Sheet to customize).",
        "4.  The Guest List feeds the Invitations Tracker, Meal Counts, Seating Chart and Thank-You Cards.",
        "5.  The Master Budget feeds the Dashboard, Budget Breakdown chart and Contributions tracker.",
    ]
    for i, t in enumerate(hows, start=1):
        ws.merge_cells(f"B{r + i}:H{r + i}")
        c = ws[f"B{r + i}"]
        c.value = t
        c.font = Font(size=10, color="4A3A3F")
        c.alignment = Alignment(horizontal="left", vertical="center")
    r += len(hows) + 2

    section(ws, r, f"WHAT'S INSIDE  —  TAP ANY TAB NAME TO JUMP THERE", "B", "H")
    r += 1
    for group, sheets in INDEX:
        ws.merge_cells(f"B{r}:H{r}")
        for ci in range(2, 9):
            cell = ws.cell(row=r, column=ci)
            cell.fill = PatternFill("solid", start_color="EBD9DD")
        c = ws[f"B{r}"]
        c.value = group
        c.font = Font(size=10, bold=True, color="8A5A66")
        c.alignment = Alignment(horizontal="left", vertical="center")
        ws.row_dimensions[r].height = 17
        r += 1
        for name, desc in sheets:
            link = ws[f"B{r}"]
            link.value = "▸  " + name
            link.font = Font(size=10, bold=True, color="B76E79", underline="single")
            link.hyperlink = Hyperlink(ref=link.coordinate, location=f"'{name}'!A1")
            link.alignment = Alignment(horizontal="left", vertical="center", indent=1)
            ws.merge_cells(f"C{r}:H{r}")
            d = ws[f"C{r}"]
            d.value = desc
            d.font = Font(size=9.5, color="6E5F64")
            d.alignment = Alignment(horizontal="left", vertical="center")
            ws.row_dimensions[r].height = 15
            r += 1
    r += 1
    ws.merge_cells(f"B{r}:H{r}")
    c = ws[f"B{r}"]
    c.value = ("© " + AUTHOR + " — " + VERSION +
               "  •  Thank you for supporting our small store & happy planning! 💐")
    c.font = Font(size=9, italic=True, color="A0707A")
    protect(ws)


# -------------------------------------------------------------- dashboard
def dashboard(wb):
    ws = wb.create_sheet("Dashboard")
    sheet_shell(ws, TAB, "💒  WEDDING OVERVIEW DASHBOARD",
                "Your big picture at a glance  •  updates automatically", "I")
    for col, w in zip("BCDEFGHI", (24, 28, 14, 12, 12, 12, 12, 14)):
        ws.column_dimensions[col].width = w

    section(ws, 5, "THE COUPLE & THE DAY", "B", "I")
    rows = [
        ("Partner 1", "input", "Alex Morgan"),
        ("Partner 2", "input", "Jordan Lee"),
        ("Wedding Date", "date", date(2027, 5, 22)),
        ("Ceremony Time", "input", "4:00 PM"),
        ("Venue", "input", "The Rosewood Estate"),
        ("City / Location", "input", "Asheville, North Carolina"),
        ("Theme / Style", "input", "Romantic garden party"),
        ("Hashtag (auto)", "formula", None),
    ]
    r = 6
    for label, kind, val in rows:
        put_label(ws, f"B{r}", label)
        c = put_input(ws, f"C{r}", val, align=Alignment(horizontal="left", vertical="center"))
        if kind == "date":
            c.number_format = DATEF
        r += 1
    ws.merge_cells("E8:F8")
    for cc in ("E8", "F8"):
        ws[cc].fill = __import__("core").FORMULA_FILL
        ws[cc].border = __import__("core").BORDER
    big = put_formula(ws, "E8", '=IF($C$8="","—",$C$8-TODAY())', numfmt=DAYS,
                      align=Alignment(horizontal="center", vertical="center"), bold=True)
    big.font = Font(size=12, bold=True, color="B76E79")
    put_formula(ws, "C13",
                '=IF(OR($C$6="",$C$7=""),"",'
                '"#"&SUBSTITUTE(LOWER($C$6&$C$7)," ",""))')

    section(ws, 15, "COLOR PALETTE", "B", "I")
    swatches = ["F7D8DE", "E3A6B3", "B76E79", "9CAF88", "D4B483", "FDF8F0"]
    names = ["Blush", "Rose", "Rose Gold", "Sage", "Gold", "Ivory"]
    put_label(ws, "B16", "Swatches")
    put_label(ws, "B17", "Color name")
    put_label(ws, "B18", "Where it's used", bold=False)
    for i, (hexc, nm) in enumerate(zip(swatches, names)):
        cl = chr(ord("C") + i)
        sc = ws[f"{cl}16"]
        sc.fill = PatternFill("solid", start_color=hexc)
        sc.border = __import__("core").BORDER
        sc.protection = __import__("core").UNLOCKED
        put_input(ws, f"{cl}17", nm, align=Alignment(horizontal="center", vertical="center"))
        put_input(ws, f"{cl}18", None, align=Alignment(horizontal="center", vertical="center"))
        ws.row_dimensions[16].height = 26

    section(ws, 20, "BUDGET AT A GLANCE", "B", "I")
    bstats = [
        ("Total estimated", f"={ref('Master Budget', '$C$31')}", MONEY, None),
        ("Actual / committed", f"={ref('Master Budget', '$D$31')}", MONEY, None),
        ("Deposits paid", f"={ref('Master Budget', '$E$31')}", MONEY, None),
        ("Balance remaining", f"={ref('Master Budget', '$F$31')}", MONEY, None),
        ("Budget used", f"=IF(N('Master Budget'!$C$31)=0,\"\","
                        f"N('Master Budget'!$D$31)/'Master Budget'!$C$31)", PCT, MONEY),
    ]
    r = 21
    for label, f, fmt, share_fmt in bstats[:4]:
        put_label(ws, f"B{r}", label)
        put_formula(ws, f"C{r}", f, numfmt=fmt,
                    align=Alignment(horizontal="center", vertical="center"))
        ws.merge_cells(f"E{r}:F{r}")
        for cc in (f"E{r}", f"F{r}"):
            ws[cc].fill = __import__("core").FORMULA_FILL
            ws[cc].border = __import__("core").BORDER
        put_formula(ws, f"E{r}", f"=IF(N($C$21)=0,\"\",N($C{r})/$C$21)",
                    numfmt=PCT, align=Alignment(horizontal="center", vertical="center"))
        r += 1
    put_label(ws, f"B{r}", "Budget used")
    put_formula(ws, f"C{r}", bstats[4][1], numfmt=PCT,
                align=Alignment(horizontal="center", vertical="center"))

    section(ws, 27, "GUEST SNAPSHOT", "B", "I")
    gstats = [
        ("Guests invited", f"={ref('Guest List', '$C$5')}", INT),
        ("Confirmed", f"={ref('Guest List', '$E$5')}", INT),
        ("Declined", f"={ref('Guest List', '$G$5')}", INT),
        ("Awaiting reply", f"={ref('Guest List', '$I$5')}", INT),
        ("Guests with a +1", f"={ref('Guest List', '$C$6')}", INT),
    ]
    r = 28
    for label, f, fmt in gstats:
        put_label(ws, f"B{r}", label)
        put_formula(ws, f"C{r}", f, numfmt=fmt,
                    align=Alignment(horizontal="center", vertical="center"))
        r += 1

    section(ws, 34, "ACTIONS & COUNTDOWNS", "B", "I")
    astats = [
        ("Payments due in 30 days",
         f"=COUNTIFS('Payment Tracker'!$E$9:$E$158,\">=\"&TODAY(),"
         f"'Payment Tracker'!$E$9:$E$158,\"<=\"&TODAY()+30,"
         f"'Payment Tracker'!$H$9:$H$158,\"<>Paid\")", INT),
        ("Next unpaid due date",
         f"=IFERROR(IF(MINIFS('Payment Tracker'!$E$9:$E$158,"
         f"'Payment Tracker'!$H$9:$H$158,\"<>Paid\","
         f"'Payment Tracker'!$E$9:$E$158,\">=\"&TODAY())=0,"
         f"\"All caught up!\",MINIFS('Payment Tracker'!$E$9:$E$158,"
         f"'Payment Tracker'!$H$9:$H$158,\"<>Paid\","
         f"'Payment Tracker'!$E$9:$E$158,\">=\"&TODAY())),\"—\")", DATEF),
        ("Checklist complete", f"={ref('Countdown Checklist', '$E$5')}", PCT),
        ("Vendors booked",
         f"={ref('Vendor Contacts', '$E$5')}&\" of \"&{ref('Vendor Contacts', '$C$5')}", None),
        ("Thank-you cards sent", f"={ref('Thank You Cards', '$C$5')}", INT),
        ("Honeymoon budget", f"={ref('Honeymoon Planner', '$C$17')}", MONEY),
    ]
    r = 35
    for label, f, fmt in astats:
        put_label(ws, f"B{r}", label)
        put_formula(ws, f"C{r}", f, numfmt=fmt,
                    align=Alignment(horizontal="center", vertical="center"))
        r += 1
    note = ws[f"B{r + 1}"]
    note.value = "🔒  Everything on this page is calculated automatically from your other tabs."
    note.font = Font(size=8.5, italic=True, color="B58E96")
    protect(ws)


# ------------------------------------------------------------- countdown
PHASES = [
    ("12 Months Before", -12, [
        "Set the wedding date & book the officiant",
        "Draft the budget & open a wedding savings account",
        "Start the master guest list (use the Guest List tab)",
        "Hire a wedding planner / coordinator",
        "Tour venues & book your favourite",
        "Choose your wedding party",
    ]),
    ("6 Months Before", -6, [
        "Book the caterer & schedule a tasting",
        "Book photographer & videographer",
        "Book DJ / band & extra entertainment",
        "Order the wedding gown (allow alterations time)",
        "Send save-the-dates",
        "Book the florist & lock the décor vision",
        "Reserve hotel room blocks for guests",
        "Set up your gift registry",
    ]),
    ("3 Months Before", -3, [
        "Finalize the guest list & order invitations",
        "Do hair & makeup trials",
        "Order bridesmaid dresses & groom's attire",
        "Plan & book the honeymoon",
        "Do the cake tasting & order the cake",
        "Arrange guest transportation / shuttles",
        "Buy the wedding rings",
    ]),
    ("1 Month Before", -1, [
        "Mail invitations & set the RSVP deadline",
        "Apply for the marriage license (see Legal & Officiant)",
        "Final dress fitting",
        "Confirm every vendor detail in writing",
        "Give caterer preliminary menu counts",
        "Write your vows (use the Vow Worksheet)",
        "Break in your wedding shoes",
        "Build the day-of timeline & share with vendors",
    ]),
    ("1 Week Before", -7, [
        "Confirm the vendor arrival schedule",
        "Pack the wedding emergency kit",
        "Pick up the gown & all attire",
        "Give caterer the final headcount",
        "Assign day-of helpers & walk through the timeline",
        "Practice vows & prepare toast cue cards",
        "Label payment & tip envelopes for vendors",
    ]),
    ("Day-Of", 0, [
        "Eat a real breakfast & hydrate 💧",
        "Hair & makeup",
        "Get dressed — detail photos first",
        "First look & wedding party photos",
        "CEREMONY — you're getting married! 💍",
        "Cocktail hour & family formal photos",
        "Grand entrance, dinner & dancing",
        "Send-off & collect keepsakes",
    ]),
]


def _phase_date_formula(r):
    d = "Dashboard!$C$8"
    return (
        f'=IF($B{r}="","",IF({d}="","",'
        f'IF($B{r}="Day-Of",{d},'
        f'IF($B{r}="1 Week Before",{d}-7,'
        f'IF($B{r}="1 Month Before",EDATE({d},-1),'
        f'IF($B{r}="3 Months Before",EDATE({d},-3),'
        f'IF($B{r}="6 Months Before",EDATE({d},-6),'
        f'IF($B{r}="12 Months Before",EDATE({d},-12),""))))))))'
    )


def countdown(wb):
    ws = wb.create_sheet("Countdown Checklist")
    sheet_shell(ws, TAB, "⏳  COUNTDOWN CHECKLIST",
                "12-month → 6-month → 3-month → 1-month → 1-week → day-of", "F")
    for col, w in zip("BCDEF", (20, 52, 15, 13, 30)):
        ws.column_dimensions[col].width = w

    stat_pair(ws, 5, "B", "TASKS DONE", '=COUNTIF($E$9:$E$120,"Done")', INT)
    stat_pair(ws, 5, "D", "% COMPLETE",
              '=IF(COUNTA($C$9:$C$120)=0,"",COUNTIF($E$9:$E$120,"Done")/COUNTA($C$9:$C$120))',
              PCT, value_col="E")

    sample = []
    for phase, _off, tasks in PHASES:
        for t in tasks:
            sample.append((phase, t))
    cols = [
        dict(key="phase", title="Phase", width=20),
        dict(key="task", title="Task", width=52),
        dict(key="target", title="Target Date (auto)", kind="formula", numfmt=DATEF,
             formula=lambda r, L: _phase_date_formula(r), align=__import__("core").AL_C),
        dict(key="status", title="Status", dv=CHECK_OPTS, align=__import__("core").AL_C),
        dict(key="notes", title="Notes", width=30),
    ]
    first, last, L, _ = make_table(ws, 8, cols, sample, 25)
    status_cf(ws, f"E{first}:E{last}",
              [("Done", GREEN), ("In Progress", AMBER), ("To Do", RED)])
    protect(ws)


# ----------------------------------------------------------- vision board
def vision_board(wb):
    ws = wb.create_sheet("Vision Board")
    sheet_shell(ws, TAB, "🎨  WEDDING VISION BOARD",
                "Mood, style & inspiration", "F")
    for col, w in zip("BCDEF", (26, 30, 26, 22, 26)):
        ws.column_dimensions[col].width = w

    section(ws, 5, "MOOD & FEELING", "B", "F")
    moods = [
        ("Romantic", "Soft light, candles, flowing fabric"),
        ("Whimsical", "Wildflowers, hand-lettered signs"),
        ("Warm", "Candlelight, wood tones, amber glow"),
        ("Intimate", "Long tables, acoustic music"),
        ("Joyful", "Bright florals, upbeat band set"),
    ]
    cols = [
        dict(key="mood", title="Mood word", width=26),
        dict(key="shows", title="How it shows up", width=52),
    ]
    make_table(ws, 6, cols, moods, 3, add_filter=False, freeze=False)

    section(ws, 16, "STYLE KEYWORDS", "B", "F")
    kws = [
        ("Garden party", "Stationery, floral arch"),
        ("Heirloom / vintage", "Rings, tableware, lace"),
        ("Candlelit", "Reception lighting"),
        ("Soft & natural", "Photography edit, linens"),
    ]
    make_table(ws, 17, cols, kws, 3, add_filter=False, freeze=False)

    section(ws, 26, "INSPIRATION SOURCES", "B", "F")
    srcs = [
        ("Pinterest", "pinterest.com/ourwedding", "Colour palettes & arches"),
        ("Instagram", "@greenhouse.florals", "Organic installation styles"),
        ("Magazine", "Brides — spring issue", "Stationery suite ideas"),
    ]
    cols3 = [
        dict(key="src", title="Platform / source", width=26),
        dict(key="link", title="Link / handle", width=30),
        dict(key="love", title="What we love", width=30),
    ]
    make_table(ws, 27, cols3, srcs, 4, add_filter=False, freeze=False)

    section(ws, 36, "THINGS WE LOVE  vs  THINGS TO AVOID", "B", "F")
    put_label(ws, "B37", "We love 💕")
    put_label(ws, "D37", "We'd rather skip 🙅")
    merged_input(ws, "B38:C44", "Unplugged ceremony\nLive acoustic cocktail hour\n"
                                "Late-night snack surprise")
    merged_input(ws, "D38:E44", "Dove releases\nLong gap between ceremony & dinner\n"
                                "Chicken-dance playlist defaults")
    protect(ws)


# -------------------------------------------------------------- priority
def priority(wb):
    ws = wb.create_sheet("Priority Ranking")
    sheet_shell(ws, TAB, "🥇  PRIORITY RANKING",
                "Agree on your top 3–5 before you spend a dollar", "F")
    for col, w in zip("BCDEF", (8, 28, 48, 14, 28)):
        ws.column_dimensions[col].width = w

    sample = [
        (1, "Photography & video", "The one thing we keep forever"),
        (2, "Venue", "Sets the entire atmosphere of the day"),
        (3, "Food & drink", "Guest experience is our love language"),
        (4, "Music & entertainment", "A full dance floor all night"),
        (5, "Guest comfort", "Shuttles, welcome bags, no-long-gaps"),
    ]
    cols = [
        dict(key="rank", title="Rank", width=8, align=__import__("core").AL_C),
        dict(key="what", title="What matters most", width=28),
        dict(key="why", title="Why it matters", width=48),
        dict(key="share", title="Budget share", numfmt=PCT,
             align=__import__("core").AL_C),
        dict(key="notes", title="Notes", width=28),
    ]
    first, last, L, total_row = make_table(
        ws, 8, cols, sample, 5,
        totals=("TOTAL", {"share": "sum"}))
    tip = ws[f"B{total_row + 2}"]
    tip.value = ("💡 Tip: aim for your top 3 priorities to take roughly 60–70% "
                 "of the budget — and let the rest be 'good enough'.")
    tip.font = Font(size=9, italic=True, color="8A5A66")
    protect(ws)


def build(wb):
    start_here(wb)
    dashboard(wb)
    countdown(wb)
    vision_board(wb)
    priority(wb)
