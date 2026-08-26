"""Wedding Planner V2 — Budget & Finance sheets (Novality Store)."""
from datetime import date
from openpyxl.styles import Alignment
from openpyxl.chart import PieChart, Reference

from core import (MONEY, PCT, DATEF, INT, sheet_shell, section, put_label,
                  put_formula, stat_pair, make_table, status_cf, protect,
                  PAY_OPTS, YESNO, GREEN, RED, AMBER, BLUE, ref,
                  MBUD_FIRST, MBUD_LAST, MBUD_TOTAL, PAY_FIRST, PAY_LAST)

TAB = "88A47C"

CATEGORIES = [
    ("Venue & rental",            8500, 8000, 2000, "The Rosewood Estate"),
    ("Catering & bar",           12000, 11500, 3000, "Harvest & Vine Co."),
    ("Wedding cake",               650,  650,  200, "Sugarplum Cakery"),
    ("Bridal attire",             1800, 1750,  600, "Ivory & Oak Bridal"),
    ("Groom & party attire",       950,  900,  300, "The Black Tie Co."),
    ("Hair & makeup",              600,  550,  150, "Glow Studio"),
    ("Flowers & décor",           2800, None,  700, "Bloom & Twine"),
    ("Photography",               3200, None,  800, "Golden Hour Photo"),
    ("Videography",               2200, None,  500, "Reel Love Films"),
    ("Music / DJ / band",         2500, None,  500, "Silver Sparrow DJ"),
    ("Ceremony & officiant",       400, None,  None, "Rev. Harper"),
    ("Stationery & postage",       700, None,  None, None),
    ("Favors & gifts",             350, None,  None, None),
    ("Rings",                     2400, None,  None, None),
    ("Transportation",             900, None,  None, None),
    ("Honeymoon",                 4500, None,  None, None),
    ("Other / contingency",       1000, None,  None, None),
]

AL_C = Alignment(horizontal="center", vertical="center")


def master_budget(wb):
    ws = wb.create_sheet("Master Budget")
    sheet_shell(ws, TAB, "💰  MASTER BUDGET",
                "Estimated vs actual — deposits & balance due (balance auto-calculates)",
                "I")
    for col, w in zip("BCDEFGHI", (26, 13, 13, 13, 13, 11, 22, 24)):
        ws.column_dimensions[col].width = w

    sample = [(c[0], c[1], c[2], c[3], c[4]) for c in CATEGORIES]
    cols = [
        dict(key="cat", title="Category", width=26),
        dict(key="est", title="Estimated cost", numfmt=MONEY, align=AL_C),
        dict(key="act", title="Actual cost", numfmt=MONEY, align=AL_C),
        dict(key="dep", title="Deposit paid", numfmt=MONEY, align=AL_C),
        dict(key="bal", title="Balance due 🔒", kind="formula", numfmt=MONEY, align=AL_C,
             formula=lambda r, L:
                 f'=IF(AND(${L["cat"]}{r}="",${L["est"]}{r}="",${L["act"]}{r}="",'
                 f'${L["dep"]}{r}=""),"",'
                 f'MAX(0,N(IF(${L["act"]}{r}="",${L["est"]}{r},${L["act"]}{r}))'
                 f'-N(${L["dep"]}{r})))'),
        dict(key="pct", title="% of est. 🔒", kind="formula", numfmt=PCT, align=AL_C,
             formula=lambda r, L:
                 f'=IF(OR(${L["est"]}{r}="",N($C$31)=0),"",N(${L["est"]}{r})/$C$31)'),
        dict(key="vendor", title="Vendor", width=22),
        dict(key="notes", title="Notes", width=24),
    ]
    make_table(ws, 8, cols, sample, 5,
               totals=("TOTAL", {"est": "sum", "act": "sum", "dep": "sum",
                                 "bal": "sum",
                                 "pct": lambda r, L: f"=SUM(G{MBUD_FIRST}:G{MBUD_LAST})"}))
    tip = ws["B33"]
    tip.value = ("💡  Balance due uses the actual cost if entered, otherwise the "
                 "estimate — minus deposits already paid.")
    tip.font = __import__("core").Font(size=9, italic=True, color="8A5A66")
    protect(ws)


def payment_tracker(wb):
    ws = wb.create_sheet("Payment Tracker")
    sheet_shell(ws, TAB, "🧾  PAYMENT TRACKER",
                "Every payment — amount, due date & paid status", "I")
    for col, w in zip("BCDEFGHI", (24, 16, 13, 14, 13, 12, 15, 22)):
        ws.column_dimensions[col].width = w

    sample = [
        ("The Rosewood Estate", "Venue", 6500, date(2027, 3, 1), 2000, "Deposit Paid"),
        ("Harvest & Vine Co.", "Catering", 3000, date(2027, 4, 15), 0, "Unpaid"),
        ("Golden Hour Photo", "Photography", 3200, date(2027, 5, 1), 800, "Deposit Paid"),
        ("Silver Sparrow DJ", "Music", 2500, date(2027, 5, 22), 0, "Unpaid"),
        ("Bloom & Twine", "Florist", 1500, date(2027, 4, 20), 750, "Partially Paid"),
        ("Ivory & Oak Bridal", "Attire", 1750, date(2027, 2, 10), 1750, "Paid"),
    ]
    cols = [
        dict(key="vendor", title="Vendor", width=24),
        dict(key="cat", title="Category", width=16),
        dict(key="amt", title="Amount due", numfmt=MONEY, align=AL_C),
        dict(key="due", title="Due date", numfmt=DATEF, align=AL_C),
        dict(key="paid", title="Amount paid", numfmt=MONEY, align=AL_C),
        dict(key="bal", title="Balance 🔒", kind="formula", numfmt=MONEY, align=AL_C,
             formula=lambda r, L:
                 f'=IF(AND(${L["amt"]}{r}="",${L["paid"]}{r}=""),"",'
                 f'MAX(0,N(${L["amt"]}{r})-N(${L["paid"]}{r})))'),
        dict(key="status", title="Status", dv=PAY_OPTS, align=AL_C),
        dict(key="notes", title="Notes", width=22),
    ]
    first, last, L, _ = make_table(ws, 8, cols, sample, PAY_LAST - PAY_FIRST + 1 - len(sample),
                                   totals=("TOTAL", {"amt": "sum", "paid": "sum",
                                                     "bal": "sum"}))
    status_cf(ws, f"H{first}:H{last}",
              [("Paid", GREEN), ("Unpaid", RED), ("Deposit Paid", AMBER),
               ("Partially Paid", BLUE)])
    protect(ws)


def budget_breakdown(wb):
    ws = wb.create_sheet("Budget Breakdown")
    sheet_shell(ws, TAB, "📊  BUDGET BREAKDOWN BY CATEGORY",
                "Auto-totals from the Master Budget — with a live chart", "G")
    for col, w in zip("BCDEFG", (26, 15, 15, 14, 14, 20)):
        ws.column_dimensions[col].width = w

    mb = "'Master Budget'"
    sample = [(c[0],) for c in CATEGORIES]
    first, last = 9, 9 + len(sample) - 1
    cols = [
        dict(key="cat", title="Category", width=26),
        dict(key="est", title="Estimated 🔒", numfmt=MONEY, align=AL_C, kind="formula",
             formula=lambda r, L:
                 f"=SUMIF({mb}!$B${MBUD_FIRST}:$B${MBUD_LAST},${L['cat']}{r},"
                 f"{mb}!$C${MBUD_FIRST}:$C${MBUD_LAST})"),
        dict(key="act", title="Actual 🔒", numfmt=MONEY, align=AL_C, kind="formula",
             formula=lambda r, L:
                 f"=SUMIF({mb}!$B${MBUD_FIRST}:$B${MBUD_LAST},${L['cat']}{r},"
                 f"{mb}!$D${MBUD_FIRST}:$D${MBUD_LAST})"),
        dict(key="share", title="% of actual 🔒", numfmt=PCT, align=AL_C, kind="formula",
             formula=lambda r, L:
                 f'=IF(SUM($D${first}:$D${last})=0,"",'
                 f'IF(${L["act"]}{r}=0,"",${L["act"]}{r}/SUM($D${first}:$D${last})))'),
        dict(key="notes", title="Notes", width=20),
    ]
    make_table(ws, 8, cols, sample, 0,
               totals=("TOTAL", {"est": "sum", "act": "sum",
                                 "share": lambda r, L:
                                     f"=SUM(E{first}:E{last})"}))

    pie = PieChart()
    pie.title = "Actual spend by category"
    pie.height = 10.5
    pie.width = 15
    data = Reference(ws, min_col=4, min_row=first, max_row=last)
    cats = Reference(ws, min_col=2, min_row=first, max_row=last)
    pie.add_data(data, titles_from_data=False)
    pie.set_categories(cats)
    ws.add_chart(pie, "H4")
    protect(ws)


def contributions(wb):
    ws = wb.create_sheet("Contributions")
    sheet_shell(ws, TAB, "🤝  CASH FUND & CONTRIBUTIONS",
                "Who is contributing what towards the wedding", "G")
    for col, w in zip("BCDEFG", (24, 24, 14, 13, 14, 24)):
        ws.column_dimensions[col].width = w

    sample = [
        ("Mom & Dad Morgan", "Bride's parents", 5000, "Yes", date(2026, 9, 12)),
        ("Mom & Dad Lee", "Groom's parents", 5000, "Yes", date(2026, 10, 3)),
        ("Grandma Rose", "Bride's grandmother", 500, "Pending", None),
        ("Self-funded", "The couple", 6000, "No", None),
    ]
    cols = [
        dict(key="who", title="Contributor", width=24),
        dict(key="rel", title="Side / relationship", width=24),
        dict(key="amt", title="Amount", numfmt=MONEY, align=AL_C),
        dict(key="got", title="Received?", dv=["Yes", "No", "Pending"], align=AL_C),
        dict(key="date", title="Date received", numfmt=DATEF, align=AL_C),
        dict(key="notes", title="Notes", width=24),
    ]
    first, last, L, total_row = make_table(ws, 8, cols, sample, 26,
                                           totals=("TOTAL", {"amt": "sum"}))
    status_cf(ws, f"E{first}:E{last}", [("Yes", GREEN), ("Pending", AMBER)])

    r = total_row + 2
    put_label(ws, f"B{r}", "Total wedding budget")
    put_formula(ws, f"C{r}", f"={ref('Master Budget', '$C$31')}", numfmt=MONEY, align=AL_C)
    put_label(ws, f"B{r + 1}", "Still needed to fund")
    put_formula(ws, f"C{r + 1}",
                f"=MAX(0,N('Master Budget'!$C$31)-N($D${total_row}))",
                numfmt=MONEY, align=AL_C)
    protect(ws)


def build(wb):
    master_budget(wb)
    payment_tracker(wb)
    budget_breakdown(wb)
    contributions(wb)
