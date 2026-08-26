"""Wedding Planner V2 — Timeline & Day-Of sheets (Novality Store)."""
from datetime import date
from openpyxl.styles import Alignment

from core import (MONEY, DATEF, INT, sheet_shell, section, put_label,
                  put_input, merged_input, make_table, status_cf, protect,
                  YESNO, DONE_OPTS, GREEN, AMBER)

TAB = "6E4C5B"
AL_C = Alignment(horizontal="center", vertical="center")


def day_timeline(wb):
    ws = wb.create_sheet("Wedding Day Timeline")
    sheet_shell(ws, TAB, "⏰  WEDDING DAY TIMELINE",
                "Hour-by-hour from getting ready to send-off", "G")
    for col, w in zip("BCDEFG", (11, 34, 20, 20, 20, 18)):
        ws.column_dimensions[col].width = w

    sample = [
        ("7:00 AM", "Wake up, breakfast & hydrate", "Couple", "Getting-ready suite", "—"),
        ("7:30 AM", "Hair & makeup begins", "Wedding party", "Getting-ready suite",
         "Glow Studio"),
        ("9:30 AM", "Photographer arrives — detail shots", "Photographer", "Suite",
         "Golden Hour Photo"),
        ("10:30 AM", "Get dressed · first look", "Couple", "Garden", None),
        ("11:00 AM", "Wedding party photos", "Photographer", "Estate grounds", None),
        ("11:45 AM", "Family formal photos", "Families", "Ceremony lawn", "See Family Photos tab"),
        ("12:30 PM", "Light lunch & touch-ups", "Everyone", "Suite", None),
        ("1:30 PM", "Guests arrive · prelude music", "Guests", "Ceremony lawn",
         "Silver Sparrow DJ"),
        ("2:00 PM", "CEREMONY 💍", "Everyone", "Ceremony lawn", None),
        ("2:45 PM", "Cocktail hour · couple portraits", "Guests / couple", "Terrace", None),
        ("4:00 PM", "Grand entrance & first dance", "Couple", "Reception barn", None),
        ("4:15 PM", "Dinner service", "Guests", "Reception barn", "Harvest & Vine"),
        ("5:15 PM", "Toasts", "Best man & MOH", "Reception barn", None),
        ("6:00 PM", "Cake cutting", "Couple", "Cake table", None),
        ("6:15 PM", "Open dance floor", "Everyone", "Reception barn", "DJ"),
        ("8:00 PM", "Bouquet & garter toss", None, "Dance floor", None),
        ("8:30 PM", "Late-night snack surprise", "Everyone", "Reception barn",
         "Slider truck"),
        ("9:30 PM", "Last slow dance", "Everyone", "Reception barn", None),
        ("10:00 PM", "Sparkler send-off ✨", "Everyone", "Estate drive", None),
    ]
    cols = [
        dict(key="time", title="Time", width=11, align=AL_C),
        dict(key="event", title="Event", width=34),
        dict(key="who", title="Who's involved", width=20),
        dict(key="where", title="Location", width=20),
        dict(key="lead", title="Lead / vendor", width=20),
        dict(key="notes", title="Notes", width=18),
    ]
    make_table(ws, 8, cols, sample, 8)
    protect(ws)


def rehearsal(wb):
    ws = wb.create_sheet("Rehearsal Dinner")
    sheet_shell(ws, TAB, "🍝  REHEARSAL DINNER PLANNER",
                "Guest list, venue, menu & toasts", "E")
    for col, w in zip("BCDE", (24, 24, 14, 28)):
        ws.column_dimensions[col].width = w

    section(ws, 5, "THE PLAN", "B", "E")
    fields = [("Date", "Friday 21 May 2027"), ("Time", "6:30 PM"),
              ("Venue", "Copper Kettle Kitchen"), ("Hosted by", "The Lee family"),
              ("Menu theme", "Family-style Italian")]
    for i, (k, v) in enumerate(fields):
        put_label(ws, f"B{6 + i}", k)
        put_input(ws, f"C{6 + i}", v)
        ws.merge_cells(f"C{6 + i}:E{6 + i}")

    section(ws, 12, "GUEST LIST", "B", "E")
    guests = [
        ("Jordan Lee", "The couple"), ("Alex Morgan", "The couple"),
        ("Rev. Harper", "Officiant + spouse"), ("Parents & grandparents", "Both families"),
        ("Wedding party + plus-ones", "Wedding party"),
        ("Readers & ring bearers", "Ceremony roles"),
    ]
    gcols = [
        dict(key="name", title="Guest / group", width=30),
        dict(key="party", title="Party", width=26),
        dict(key="attending", title="Attending?", dv=YESNO, align=AL_C),
        dict(key="notes", title="Notes", width=28),
    ]
    make_table(ws, 13, gcols, guests, 10, add_filter=False, freeze=False)

    section(ws, 28, "TOAST SCHEDULE", "B", "E")
    toasts = [
        ("6:45 PM", "Host welcome", "Mr. Lee"),
        ("7:30 PM", "Parents' toast", "Both sets of parents"),
        ("8:15 PM", "Couple thanks everyone", "Jordan & Alex"),
    ]
    tcols = [
        dict(key="time", title="Time", width=12, align=AL_C),
        dict(key="speaker", title="Speaker", width=26),
        dict(key="topic", title="Topic / notes", width=30),
    ]
    make_table(ws, 29, tcols, toasts, 5, add_filter=False, freeze=False)
    protect(ws)


def ceremony_order(wb):
    ws = wb.create_sheet("Ceremony Order")
    sheet_shell(ws, TAB, "💍  CEREMONY ORDER OF EVENTS",
                "Processional, readings, vows, ring exchange & recessional", "F")
    for col, w in zip("BCDEF", (9, 30, 34, 22, 24)):
        ws.column_dimensions[col].width = w

    sample = [
        (1, "Pre-service prelude", "Canon in D (instrumental)", "DJ", "Starts 30 min before"),
        (2, "Family seating", "Landslide (instrumental)", "Ushers", None),
        (3, "Wedding party processional", "Can't Help Falling in Love — Kina Grannis",
         "Wedding party", None),
        (4, "Bride's processional", "At Last — string quartet version", "Alex & escort",
         None),
        (5, "Words of welcome", None, "Rev. Harper", None),
        (6, "First reading", "The Art of Marriage", "Ava's sister", None),
        (7, "Second reading", "Sonnet 116 — Shakespeare", "Noah's brother", None),
        (8, "Vows", "Handwritten", "The couple", "See Vow Worksheet"),
        (9, "Ring exchange", "Soft instrumental", "The couple", "Ring bearer"),
        (10, "Unity ritual", "Handfasting with family ribbons", "The couple", None),
        (11, "Pronouncement & first kiss", None, "Rev. Harper", None),
        (12, "Recessional", "Signed, Sealed, Delivered — Stevie Wonder", "Everyone",
         None),
    ]
    cols = [
        dict(key="n", title="#", width=9, align=AL_C),
        dict(key="moment", title="Moment", width=30),
        dict(key="music", title="Music / reading", width=34),
        dict(key="who", title="Participants", width=22),
        dict(key="notes", title="Notes", width=24),
    ]
    make_table(ws, 8, cols, sample, 4)
    protect(ws)


def reception_timeline(wb):
    ws = wb.create_sheet("Reception Timeline")
    sheet_shell(ws, TAB, "🕺  RECEPTION TIMELINE",
                "Grand entrance, first dance, toasts, cake cutting & bouquet toss", "F")
    for col, w in zip("BCDEF", (11, 32, 30, 20, 24)):
        ws.column_dimensions[col].width = w

    sample = [
        ("3:30 PM", "Wedding party line-up", "DJ cue — hype track", "Wedding party"),
        ("4:00 PM", "Grand entrance", "DJ cue — couple's entrance song", "The couple"),
        ("4:05 PM", "First dance", "First dance song (see Special Dances)", "The couple"),
        ("4:15 PM", "Welcome & toasts begin", "Mics on", "Best man & MOH"),
        ("4:45 PM", "Dinner service", "Playlist — dinner vibes", "Guests"),
        ("6:00 PM", "Father–daughter & mother–son dances", "DJ cue", "Families"),
        ("6:15 PM", "Cake cutting", "DJ cue — fun song", "The couple"),
        ("6:30 PM", "Open dance floor", "DJ — high energy set", "Everyone"),
        ("8:00 PM", "Bouquet & garter toss", "DJ cues (see Special Dances)", "Singles 😄"),
        ("8:30 PM", "Late-night snacks served", "DJ keeps playing", "Everyone"),
        ("9:30 PM", "Last dance", "DJ cue — final song", "Everyone"),
        ("10:00 PM", "Send-off line-up", "Sparklers outside", "Everyone"),
    ]
    cols = [
        dict(key="time", title="Time", width=11, align=AL_C),
        dict(key="event", title="Event", width=32),
        dict(key="cue", title="DJ cue / song", width=30),
        dict(key="who", title="Who", width=20),
        dict(key="notes", title="Notes", width=24),
    ]
    make_table(ws, 8, cols, sample, 6)
    protect(ws)


def emergency_kit(wb):
    ws = wb.create_sheet("Emergency Kit")
    sheet_shell(ws, TAB, "🩹  DAY-OF EMERGENCY KIT CHECKLIST",
                "The survival kit — assign an owner for the bag", "F")
    for col, w in zip("BCDEF", (28, 14, 10, 14, 24)):
        ws.column_dimensions[col].width = w

    items = [
        ("Sewing kit & safety pins", "Fashion fixes"),
        ("Stain remover pen", "Fashion fixes"),
        ("Double-sided fashion tape", "Fashion fixes"),
        ("Clear nail polish (runs)", "Fashion fixes"),
        ("Scissors & mini toolkit", "Fashion fixes"),
        ("Spare stockings / socks", "Fashion fixes"),
        ("Band-aids & blister plasters", "Health"),
        ("Pain relievers", "Health"),
        ("Antacids", "Health"),
        ("Allergy medication", "Health"),
        ("Prescriptions (if needed)", "Health"),
        ("Blotting papers & powder", "Beauty"),
        ("Touch-up makeup & lipstick", "Beauty"),
        ("Deodorant", "Beauty"),
        ("Hair pins, comb & mini spray", "Beauty"),
        ("Straws (protect lipstick)", "Beauty"),
        ("Emery board & hand cream", "Beauty"),
        ("Mints & gum", "Food & drink"),
        ("Granola bars & crackers", "Food & drink"),
        ("Water bottles & straws", "Food & drink"),
        ("Phone chargers & power bank", "Practical"),
        ("Tissues", "Practical"),
        ("Umbrella & sunscreen", "Practical"),
        ("Bug spray", "Practical"),
        ("Cash in small bills for tips", "Practical"),
        ("Vows & speech cue cards", "Practical"),
        ("Spare ring box & earring backs", "Practical"),
    ]
    sample = list(items)
    cols = [
        dict(key="item", title="Item", width=28),
        dict(key="cat", title="Category", width=14),
        dict(key="packed", title="Packed?", dv=DONE_OPTS, align=AL_C),
        dict(key="owner", title="Owner", width=14),
        dict(key="notes", title="Notes", width=24),
    ]
    first, last, L, _ = make_table(ws, 8, cols, sample, 3)
    status_cf(ws, f"D{first}:D{last}", [("Done", GREEN), ("Not Yet", AMBER)])
    protect(ws)


def vendor_arrivals(wb):
    ws = wb.create_sheet("Vendor Arrivals")
    sheet_shell(ws, TAB, "🚐  VENDOR ARRIVAL SCHEDULE",
                "Who arrives when on the wedding day — share this with your venue", "H")
    for col, w in zip("BCDEFGH", (22, 12, 26, 20, 15, 12, 20)):
        ws.column_dimensions[col].width = w

    sample = [
        ("Glow Studio", "7:30 AM", "Hair & makeup", "Getting-ready suite",
         "(828) 555-0143", "1:00 PM"),
        ("Party Perfect Rentals", "9:00 AM", "Tables, chairs & linens",
         "Barn service entrance", "(828) 555-0176", "11:00 AM"),
        ("Golden Hour Photo", "9:30 AM", "Getting-ready coverage", "Suite",
         "(828) 555-0132", "10:30 PM"),
        ("Bloom & Twine", "10:00 AM", "Arch & centerpiece install",
         "Ceremony lawn + barn", "(828) 555-0166", "3:00 PM"),
        ("Silver Sparrow DJ", "12:00 PM", "Sound check", "Barn stage",
         "(828) 555-0178", "10:30 PM"),
        ("Reel Love Films", "12:30 PM", "Video coverage", "Suite",
         "(828) 555-0155", "10:30 PM"),
        ("Harvest & Vine Co.", "1:00 PM", "Catering load-in", "Kitchen entrance",
         "(828) 555-0187", "11:00 PM"),
        ("Sugarplum Cakery", "1:00 PM", "Cake delivery & setup", "Cake table",
         "(828) 555-0198", "1:45 PM"),
        ("Blue Ridge Limo", "1:45 PM", "Couple transport", "Estate drive",
         "(828) 555-0109", "10:30 PM"),
    ]
    cols = [
        dict(key="vendor", title="Vendor / company", width=22),
        dict(key="arrive", title="Arrival time", width=12, align=AL_C),
        dict(key="task", title="Task", width=26),
        dict(key="where", title="Location / entrance", width=20),
        dict(key="phone", title="On-site phone", width=15),
        dict(key="depart", title="Departure", width=12, align=AL_C),
        dict(key="notes", title="Notes", width=20),
    ]
    make_table(ws, 8, cols, sample, 6)
    protect(ws)


def build(wb):
    day_timeline(wb)
    rehearsal(wb)
    ceremony_order(wb)
    reception_timeline(wb)
    emergency_kit(wb)
    vendor_arrivals(wb)
