"""Wedding Planner V2 — Guest Management sheets (Novality Store)."""
from datetime import date
from openpyxl.styles import Alignment
from openpyxl.chart import PieChart, Reference

from core import (MONEY, MONEY2, DATEF, INT, sheet_shell, section, put_label,
                  put_formula, stat_pair, make_table, status_cf, protect,
                  YESNO, YESNO_NA, RSVP_OPTS, MEAL_OPTS, GREEN, RED, AMBER,
                  BLUE, GUEST_SHEET, GUEST_FIRST, GUEST_LAST)

TAB = "D98BA3"
AL_C = Alignment(horizontal="center", vertical="center")

G_FIRST, G_LAST = GUEST_FIRST, GUEST_LAST          # rows 9..208


def guest_list(wb):
    ws = wb.create_sheet(GUEST_SHEET)
    sheet_shell(ws, TAB, "💌  GUEST LIST MASTER",
                "RSVP status, meal choice, +1s & table numbers — feeds the other guest tabs",
                "L")
    for col, w in zip("BCDEFGHIJKL",
                      (22, 9, 16, 22, 16, 13, 13, 9, 16, 8, 18)):
        ws.column_dimensions[col].width = w

    # live stat strip (anchored here — Dashboard reads these cells)
    stat_pair(ws, 5, "B", "INVITED",
              f'=SUMPRODUCT(($B${G_FIRST}:$B${G_LAST}<>"")*1)', INT)
    stat_pair(ws, 5, "D", "CONFIRMED",
              f'=COUNTIF($G${G_FIRST}:$G${G_LAST},"Confirmed")', INT)
    stat_pair(ws, 5, "F", "DECLINED",
              f'=COUNTIF($G${G_FIRST}:$G${G_LAST},"Declined")', INT)
    stat_pair(ws, 5, "H", "AWAITING",
              f'=$C$5-$E$5-$G$5', INT)
    stat_pair(ws, 6, "B", "WITH +1",
              f'=COUNTIF($I${G_FIRST}:$I${G_LAST},"Yes")', INT)
    stat_pair(ws, 6, "D", "MEALS SET",
              f'=SUMPRODUCT(($H${G_FIRST}:$H${G_LAST}<>"")*($H${G_FIRST}:$H${G_LAST}<>"TBD"))',
              INT)
    stat_pair(ws, 6, "F", "TABLES USED",
              f'=SUMPRODUCT(($K${G_FIRST}:$K${G_LAST}<>"")*1)', INT)
    stat_pair(ws, 6, "H", "ADDRESSES SET",
              f'=SUMPRODUCT(($E${G_FIRST}:$E${G_LAST}<>"")*1)', INT)

    sample = [
        ("Ava Thompson", "Bride", "College friends", "12 Maple Ave",
         "Asheville, NC", "Confirmed", "Chicken", "Yes", "Chris Thompson", 3),
        ("Noah Bennett", "Groom", "Family", "88 Birch Rd",
         "Raleigh, NC", "Confirmed", "Beef", "No", None, 5),
        ("Olivia Carter", "Bride", "Family", "4 Fern Hollow",
         "Asheville, NC", "Confirmed", "Vegetarian", "No", None, 2),
        ("Liam Nguyen", "Groom", "College friends", "210 Cedar Ct",
         "Durham, NC", "Pending", "TBD", "No", None, None),
        ("Emma Whitfield", "Bride", "Work", "7 Laurel St",
         "Charlotte, NC", "Declined", None, "No", None, None),
        ("Sophia Reyes", "Both", "Neighbors", "150 Rose Ln",
         "Asheville, NC", "Confirmed", "Fish", "Yes", "Mateo Reyes", 7),
        ("Ethan Brooks", "Groom", "Family", "31 Sycamore Way",
         "Greensboro, NC", "Pending", "TBD", "Yes", "Grace Brooks", 5),
        ("Mia Delgado", "Bride", "College friends", "9 Poplar Dr",
         "Wilmington, NC", "Confirmed", "Gluten-Free", "No", None, 3),
    ]
    cols = [
        dict(key="name", title="Guest name", width=22),
        dict(key="side", title="Side", dv=["Bride", "Groom", "Both", "Other"], align=AL_C),
        dict(key="group", title="Group / family", width=16),
        dict(key="addr", title="Street address", width=22),
        dict(key="city", title="City / state", width=16),
        dict(key="rsvp", title="RSVP status", dv=RSVP_OPTS, align=AL_C),
        dict(key="meal", title="Meal choice", dv=MEAL_OPTS, align=AL_C),
        dict(key="plus1", title="+1?", dv=YESNO, align=AL_C),
        dict(key="plus1name", title="+1 name", width=16),
        dict(key="table", title="Table #", align=AL_C),
        dict(key="notes", title="Notes", width=18),
    ]
    first, last, L, _ = make_table(ws, 8, cols, sample, G_LAST - G_FIRST + 1 - len(sample))
    status_cf(ws, f"G{first}:G{last}",
              [("Confirmed", GREEN), ("Declined", RED), ("Pending", AMBER)])
    protect(ws)


def invitations_tracker(wb):
    ws = wb.create_sheet("Invitations Tracker")
    sheet_shell(ws, TAB, "📬  SAVE-THE-DATE & INVITATION TRACKER",
                "Guest names pull in automatically from the Guest List", "I")
    for col, w in zip("BCDEFGHI",
                      (22, 16, 15, 15, 13, 13, 13, 20)):
        ws.column_dimensions[col].width = w

    stat_pair(ws, 5, "B", "STCs SENT",
              f'=SUMPRODUCT(($D${G_FIRST}:$D${G_LAST}<>"")*1)', INT)
    stat_pair(ws, 5, "D", "INVITES SENT",
              f'=SUMPRODUCT(($E${G_FIRST}:$E${G_LAST}<>"")*1)', INT)
    stat_pair(ws, 5, "F", "RSVPs IN",
              f'=COUNTIF($F${G_FIRST}:$F${G_LAST},"Yes")', INT)
    stat_pair(ws, 5, "H", "CONFIRMED",
              f'=COUNTIF($G${G_FIRST}:$G${G_LAST},"Confirmed")', INT)

    sample = [
        (None, None, date(2026, 11, 1), date(2027, 1, 15), "Yes", "Confirmed",
         date(2027, 1, 28)),
        (None, None, date(2026, 11, 1), date(2027, 1, 15), "Yes", "Confirmed",
         date(2027, 2, 2)),
        (None, None, date(2026, 11, 1), date(2027, 1, 15), "No", "Pending", None),
        (None, None, date(2026, 11, 1), date(2027, 1, 15), "No", "Declined", None),
    ]
    cols = [
        dict(key="guest", title="Guest 🔒", kind="formula", width=22,
             formula=lambda r, L:
                 f"=IF('{GUEST_SHEET}'!$B{r}=\"\",\"\",'{GUEST_SHEET}'!$B{r})"),
        dict(key="group", title="Group 🔒", kind="formula", width=16,
             formula=lambda r, L:
                 f"=IF('{GUEST_SHEET}'!$D{r}=\"\",\"\",'{GUEST_SHEET}'!$D{r})"),
        dict(key="stc", title="Save-the-date sent", numfmt=DATEF, align=AL_C),
        dict(key="inv", title="Invitation sent", numfmt=DATEF, align=AL_C),
        dict(key="rcv", title="RSVP received?", dv=YESNO, align=AL_C),
        dict(key="resp", title="Response", dv=["Confirmed", "Declined", "Pending"],
             align=AL_C),
        dict(key="date", title="Reply date", numfmt=DATEF, align=AL_C),
        dict(key="notes", title="Notes", width=20),
    ]
    first, last, L, _ = make_table(ws, 8, cols, sample, G_LAST - G_FIRST + 1 - len(sample))
    status_cf(ws, f"G{first}:G{last}", [("Confirmed", GREEN), ("Declined", RED)])
    protect(ws)


def seating_chart(wb):
    ws = wb.create_sheet("Seating Chart")
    sheet_shell(ws, TAB, "🪑  SEATING CHART PLANNER",
                "Six seats per table — assigned guests count automatically", "J")
    for col, w in zip("BCDEFGHIJ",
                      (9, 22, 18, 18, 18, 18, 18, 18, 18)):
        ws.column_dimensions[col].width = w

    stat_pair(ws, 5, "B", "CONFIRMED", f"='{GUEST_SHEET}'!$E$5", INT)
    stat_pair(ws, 5, "D", "SEATED", '=SUMPRODUCT(($D$9:$I$20<>"")*1)', INT)
    stat_pair(ws, 5, "F", "STILL TO SEAT",
              f"=MAX(0,N('{GUEST_SHEET}'!$E$5)-$E$5)", INT)

    tables = ["Family of the bride", "Family of the groom", "College friends",
              "Work friends", "Childhood friends", "The newlywed nook",
              "Party people", "Sweethearts' table", "Out-of-towners",
              "Vendor table", None, None]
    sample = [(i + 1, t) for i, t in enumerate(tables)]
    cols = [dict(key="table", title="Table #", width=9, align=AL_C),
            dict(key="name", title="Table name", width=22)]
    cols += [dict(key=f"s{i}", title=f"Seat {i}", width=18) for i in range(1, 7)]
    cols.append(dict(key="notes", title="Notes", width=18))
    make_table(ws, 8, cols, sample, 0, add_filter=False, freeze=False)
    note = ws["B22"]
    note.value = "💡  Type guest names into the seats — the SEATED counter up top updates itself."
    note.font = __import__("core").Font(size=9, italic=True, color="8A5A66")
    protect(ws)


def hotel_bags(wb):
    ws = wb.create_sheet("Hotel & Welcome Bags")
    sheet_shell(ws, TAB, "🏨  HOTEL BLOCK & WELCOME BAGS",
                "Out-of-town guests, room blocks & welcome-bag delivery", "N")
    for col, w in zip("BCDEFGHIJKLMN",
                      (20, 12, 18, 14, 13, 13, 8, 12, 12, 12, 24, 11, 16)):
        ws.column_dimensions[col].width = w

    sample = [
        ("Ava Thompson", "Yes", "Rosewood Inn", "RB-2214", date(2027, 5, 21),
         date(2027, 5, 23), 1, 149, "Yes", "Local treats & itinerary", "Yes"),
        ("Ethan Brooks", "Yes", "Rosewood Inn", "RB-2215", date(2027, 5, 21),
         date(2027, 5, 23), 1, 149, "Yes", None, "No"),
        ("Sophia Reyes", "Yes", "Rosewood Inn", "RB-2216", date(2027, 5, 22),
         date(2027, 5, 23), 1, 149, "Yes", "Local treats & itinerary", "Yes"),
        ("Mia Delgado", "No", None, None, None, None, None, None, "No", None, "N/A"),
    ]
    cols = [
        dict(key="guest", title="Guest", width=20),
        dict(key="oot", title="Out of town?", dv=YESNO, align=AL_C),
        dict(key="hotel", title="Hotel / block", width=18),
        dict(key="conf", title="Confirmation #", width=14),
        dict(key="in", title="Check-in", numfmt=DATEF, align=AL_C),
        dict(key="out", title="Check-out", numfmt=DATEF, align=AL_C),
        dict(key="rooms", title="Rooms", align=AL_C),
        dict(key="rate", title="Rate / night", numfmt=MONEY2, align=AL_C),
        dict(key="total", title="Est. total 🔒", kind="formula", numfmt=MONEY2, align=AL_C,
             formula=lambda r, L:
                 f'=IF(OR(${L["rooms"]}{r}="",${L["rate"]}{r}=""),"",'
                 f'${L["rooms"]}{r}*${L["rate"]}{r})'),
        dict(key="bag", title="Welcome bag?", dv=YESNO, align=AL_C),
        dict(key="contents", title="Bag contents", width=24),
        dict(key="delivered", title="Delivered?", dv=YESNO_NA, align=AL_C),
        dict(key="notes", title="Notes", width=16),
    ]
    first, last, L, _ = make_table(ws, 8, cols, sample, 36,
                                   totals=("TOTAL", {"rooms": "sum", "total": "sum"}))
    protect(ws)


def meal_count(wb):
    ws = wb.create_sheet("Meal Count Summary")
    sheet_shell(ws, TAB, "🍽️  MEAL COUNT SUMMARY",
                "Caterer-ready counts — updates from the Guest List meal column", "F")
    for col, w in zip("BCDEF", (18, 17, 15, 12, 26)):
        ws.column_dimensions[col].width = w

    meals = ["Chicken", "Beef", "Fish", "Vegetarian", "Vegan", "Gluten-Free",
             "Kids Meal", "Vendor meals"]
    sample = [(m,) for m in meals]
    first, last = 9, 9 + len(sample) - 1
    cols = [
        dict(key="meal", title="Meal choice", width=18),
        dict(key="count", title="From guest list 🔒", kind="formula", numfmt=INT, align=AL_C,
             formula=lambda r, L:
                 f"=COUNTIF('{GUEST_SHEET}'!$H${G_FIRST}:$H${G_LAST},${L['meal']}{r})"),
        dict(key="extra", title="Extras / +1s", numfmt=INT, align=AL_C),
        dict(key="total", title="Total 🔒", kind="formula", numfmt=INT, align=AL_C,
             formula=lambda r, L:
                 f'=N(${L["count"]}{r})+N(${L["extra"]}{r})'),
        dict(key="notes", title="Notes", width=26),
    ]
    _, _, _, total_row = make_table(ws, 8, cols, sample, 0,
                                    totals=("GRAND TOTAL",
                                            {"count": "sum", "extra": "sum",
                                             "total": "sum"}))
    pie = PieChart()
    pie.title = "Meals at a glance"
    pie.height = 9
    pie.width = 13
    data = Reference(ws, min_col=5, min_row=first, max_row=first + 6)  # guest meals
    cats = Reference(ws, min_col=2, min_row=first, max_row=first + 6)
    pie.add_data(data, titles_from_data=False)
    pie.set_categories(cats)
    ws.add_chart(pie, "H4")
    tip = ws[f"B{total_row + 2}"]
    tip.value = "💡  Extras/+1s: kids' portions, vendor meals or last-minute additions."
    tip.font = __import__("core").Font(size=9, italic=True, color="8A5A66")
    protect(ws)


def build(wb):
    guest_list(wb)
    invitations_tracker(wb)
    seating_chart(wb)
    hotel_bags(wb)
    meal_count(wb)
