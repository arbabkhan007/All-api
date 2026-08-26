"""Wedding Planner V2 — Vendor Management sheets (Novality Store)."""
from datetime import date
from openpyxl.styles import Alignment

from core import (MONEY, DATEF, INT, sheet_shell, put_label, put_formula,
                  stat_pair, make_table, status_cf, protect,
                  CONTRACT_OPTS, YESNO, GREEN, RED, AMBER, BLUE)

TAB = "9D8189"
AL_C = Alignment(horizontal="center", vertical="center")

CATEGORIES = ["Venue", "Caterer", "Photographer", "Videographer", "Florist",
              "DJ / Band", "Officiant", "Hair & Makeup", "Bakery (Cake)",
              "Transportation", "Rentals"]


def vendor_contacts(wb):
    ws = wb.create_sheet("Vendor Contacts")
    sheet_shell(ws, TAB, "📋  VENDOR CONTACT SHEET",
                "All 11 vendor categories — contacts, contracts & balances", "L")
    for col, w in zip("BCDEFGHIJKL",
                      (16, 22, 16, 14, 24, 15, 12, 12, 11, 13, 18)):
        ws.column_dimensions[col].width = w

    # stat anchors used by the Dashboard: C5 total, E5 booked, G5 total cost
    stat_pair(ws, 5, "B", "TOTAL VENDORS", '=SUMPRODUCT(($C$9:$C$58<>"")*1)', INT)
    stat_pair(ws, 5, "D", "BOOKED",
              '=COUNTIF($G$9:$G$58,"Booked")+COUNTIF($G$9:$G$58,"Contract Signed")', INT)
    stat_pair(ws, 5, "F", "TOTAL COST", '=SUM($I$9:$I$58)', MONEY)

    sample = [
        ("Venue", "The Rosewood Estate", "Ms. Casey Reed", "(828) 555-0114",
         "events@rosewood.com", "Contract Signed", 2000, 8500, date(2027, 3, 1)),
        ("Caterer", "Harvest & Vine Co.", "Mr. Daniel Cho", "(828) 555-0187",
         "hello@harvestvine.co", "Booked", 3000, 12000, date(2027, 4, 15)),
        ("Photographer", "Golden Hour Photo", "Nora Blake", "(828) 555-0132",
         "nora@goldenhour.photo", "Booked", 800, 3200, date(2027, 5, 1)),
        ("Videographer", "Reel Love Films", "Sam Ortiz", "(828) 555-0155",
         "sam@reellove.film", "Quote Received", 500, 2200, None),
        ("Florist", "Bloom & Twine", "Ivy Laurent", "(828) 555-0166",
         "ivy@bloomtwine.com", "Booked", 700, 2800, date(2027, 4, 20)),
        ("DJ / Band", "Silver Sparrow DJ", "Marcus Cole", "(828) 555-0178",
         "book@silversparrow.dj", "Booked", 500, 2500, date(2027, 5, 22)),
        ("Officiant", "Rev. Harper", "Rev. A. Harper", "(828) 555-0121",
         "revharper@officiate.org", "Contract Signed", None, 400, date(2027, 5, 22)),
        ("Hair & Makeup", "Glow Studio", "Priya Nair", "(828) 555-0143",
         "priya@glowstudio.co", "Booked", 150, 600, date(2027, 5, 22)),
        ("Bakery (Cake)", "Sugarplum Cakery", "Lila Park", "(828) 555-0198",
         "orders@sugarplum.co", "Booked", 200, 650, date(2027, 5, 21)),
        ("Transportation", "Blue Ridge Limo", "Tom Vance", "(828) 555-0109",
         "fleet@blueridgelimo.com", "Inquiry", None, 900, None),
        ("Rentals", "Party Perfect Rentals", "Dana Fox", "(828) 555-0176",
         "rent@partyperfect.com", "Negotiating", None, 1200, None),
    ]
    cols = [
        dict(key="cat", title="Category", width=16),
        dict(key="co", title="Company", width=22),
        dict(key="person", title="Contact person", width=16),
        dict(key="phone", title="Phone", width=14),
        dict(key="email", title="Email", width=24),
        dict(key="status", title="Contract status", dv=CONTRACT_OPTS, align=AL_C),
        dict(key="dep", title="Deposit paid", numfmt=MONEY, align=AL_C),
        dict(key="cost", title="Total cost", numfmt=MONEY, align=AL_C),
        dict(key="bal", title="Balance 🔒", kind="formula", numfmt=MONEY, align=AL_C,
             formula=lambda r, L:
                 f'=IF(${L["cost"]}{r}="","",MAX(0,N(${L["cost"]}{r})'
                 f'-N(${L["dep"]}{r})))'),
        dict(key="due", title="Next payment due", numfmt=DATEF, align=AL_C),
        dict(key="notes", title="Notes", width=18),
    ]
    first, last, L, _ = make_table(ws, 8, cols, sample, 39)
    status_cf(ws, f"G{first}:G{last}",
              [("Booked", GREEN), ("Contract Signed", GREEN),
               ("Negotiating", AMBER), ("Quote Received", BLUE),
               ("Declined", RED)])
    protect(ws)


def vendor_comparison(wb):
    ws = wb.create_sheet("Vendor Comparison")
    sheet_shell(ws, TAB, "⚖️  VENDOR COMPARISON CHART",
                "Compare 2–3 options per category — savings calculate automatically", "K")
    for col, w in zip("BCDEFGHIJK",
                      (15, 18, 11, 18, 11, 18, 11, 12, 11, 24)):
        ws.column_dimensions[col].width = w

    sample = [
        ("Venue", "The Rosewood Estate", 8500, "Cedar Hollow Barn", 7200,
         "Glasshouse Downtown", 11000, 8500, "Best all-inclusive package"),
        ("Caterer", "Harvest & Vine Co.", 12000, "Fork & Flame", 10500,
         "Gather Table", 13200, 12000, "Loved the tasting menu"),
        ("Photographer", "Golden Hour Photo", 3200, "North Light Studio", 2800,
         "Ever After Co.", 3900, 3200, "Editing style is dreamy"),
        ("Videographer", "Reel Love Films", 2200, "Promise Films", 1900,
         None, None, 1900, None),
        ("DJ / Band", "Silver Sparrow DJ", 2500, "The Velvet Keys Band", 4800,
         None, None, 2500, None),
        ("Florist", "Bloom & Twine", 2800, "Petal & Stem", 2400,
         "Wildflora", 3100, 2800, None),
    ]
    cols = [
        dict(key="cat", title="Category", width=15),
        dict(key="o1", title="Option 1", width=18),
        dict(key="p1", title="Price 1", numfmt=MONEY, align=AL_C),
        dict(key="o2", title="Option 2", width=18),
        dict(key="p2", title="Price 2", numfmt=MONEY, align=AL_C),
        dict(key="o3", title="Option 3", width=18),
        dict(key="p3", title="Price 3", numfmt=MONEY, align=AL_C),
        dict(key="chosen", title="Chosen price", numfmt=MONEY, align=AL_C),
        dict(key="save", title="You save 🔒", kind="formula", numfmt=MONEY, align=AL_C,
             formula=lambda r, L:
                 f'=IF(${L["chosen"]}{r}="","",'
                 f'MAX(N(${L["p1"]}{r}),N(${L["p2"]}{r}),N(${L["p3"]}{r}))'
                 f'-${L["chosen"]}{r})'),
        dict(key="why", title="Winner & why", width=24),
    ]
    make_table(ws, 8, cols, sample, 6)
    protect(ws)


def build(wb):
    vendor_contacts(wb)
    vendor_comparison(wb)
