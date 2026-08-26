"""Sample data for the Novality Store Home Renovation Management System.

Scenario: mid-project whole-home refresh on 24 Aug 2026.
Primary project is ~72% complete. A second smaller project shows multi-property.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta

TODAY = date(2026, 8, 24)

# ---------------------------------------------------------------------------
# Lookups (dropdown sources)
# ---------------------------------------------------------------------------
LOOKUPS = {
    "Project_Status": ["Planning", "Active", "On Hold", "Completed", "Cancelled"],
    "Project_Phase": [
        "Planning",
        "Design",
        "Permits",
        "Demolition",
        "Rough-In",
        "Construction",
        "Finishes",
        "Furnishing",
        "Inspection",
        "Handover",
        "Maintenance",
    ],
    "Room_Type": [
        "Kitchen",
        "Living Room",
        "Bedroom",
        "Primary Bedroom",
        "Bathroom",
        "Primary Bathroom",
        "Powder Room",
        "Dining Room",
        "Office",
        "Garage",
        "Exterior",
        "Garden",
        "Laundry",
        "Entry / Foyer",
        "Hallway",
        "Basement",
        "Attic",
        "Custom",
    ],
    "Room_Status": ["Not Started", "Design", "In Progress", "Punch List", "Complete"],
    "Design_Style": [
        "Modern",
        "Minimal",
        "Scandinavian",
        "Luxury",
        "Industrial",
        "Traditional",
        "Transitional",
        "Japandi",
        "Mediterranean",
        "Coastal",
    ],
    "Design_Item": [
        "Mood Board",
        "Color Palette",
        "Material Board",
        "Furniture",
        "Flooring",
        "Wall",
        "Ceiling",
        "Lighting",
        "Cabinetry",
        "Hardware",
        "2D Floor Plan",
        "3D Visualization",
        "AI Concept",
    ],
    "Budget_Category": [
        "Labor",
        "Materials",
        "Design",
        "Permits",
        "Delivery",
        "Contingency",
        "Appliances",
        "Furniture",
        "Inspections",
        "Other",
    ],
    "Expense_Status": ["Planned", "Committed", "Paid", "Void"],
    "Payment_Method": ["ACH", "Check", "Credit Card", "Wire", "Cash", "Financing"],
    "Trade": [
        "General Contractor",
        "Interior Designer",
        "Architect",
        "Cabinetry",
        "Electrical",
        "Plumbing",
        "Tile & Stone",
        "Painting",
        "Flooring",
        "Lighting",
        "HVAC",
        "Carpentry",
        "Roofing",
        "Landscaping",
        "Windows & Doors",
        "Appliance",
        "Inspection",
    ],
    "Task_Status": ["To Do", "Scheduled", "In Progress", "Inspection", "Completed", "Blocked"],
    "Priority": ["Critical", "High", "Medium", "Low"],
    "Material_Status": [
        "Required",
        "Quoted",
        "Approved",
        "Ordered",
        "Shipped",
        "Delivered",
        "Installed",
        "Returned",
        "Backordered",
    ],
    "Doc_Category": [
        "Contract",
        "Invoice",
        "Receipt",
        "Floor Plan",
        "Building Permit",
        "License",
        "Insurance",
        "Warranty",
        "Inspection Report",
        "Product Manual",
        "Photo",
        "Agreement",
        "Change Order",
        "Quote",
    ],
    "Role": [
        "Homeowner",
        "Admin",
        "Project Manager",
        "Interior Designer",
        "Contractor",
        "Subcontractor",
        "Supplier",
        "Inspector",
        "Accountant",
    ],
    "Quote_Status": ["Requested", "Received", "Compared", "Accepted", "Rejected", "Expired"],
    "Job_Status": ["Assigned", "Scheduled", "In Progress", "Milestone Review", "Complete", "Disputed"],
    "Insp_Result": ["Pass", "Conditional", "Fail", "Scheduled"],
    "Payment_Status": ["Draft", "Scheduled", "Paid", "Overdue", "Disputed"],
    "CO_Status": ["Draft", "Submitted", "Approved", "Rejected", "Implemented"],
    "Permit_Status": ["Not Started", "Applied", "In Review", "Approved", "Expired", "Closed"],
    "Maint_Status": ["Upcoming", "Due Soon", "Overdue", "Scheduled", "Complete"],
    "Insight_Severity": ["Info", "Opportunity", "Warning", "Critical"],
    "Insight_Status": ["New", "Accepted", "In Progress", "Dismissed", "Resolved"],
    "Channel": ["App", "Email", "SMS", "Group Chat", "Task Comment", "Photo Comment", "Voice"],
    "Currency": ["USD", "EUR", "GBP", "CAD", "AUD", "INR", "AED"],
    "Language": ["English", "Spanish", "French", "German", "Portuguese", "Arabic", "Hindi"],
    "Property_Type": ["Single Family", "Townhouse", "Condo", "Multi-Family", "Cabin", "Commercial"],
}

from .extra_data import LOOKUPS_EXTRA  # noqa: E402

LOOKUPS.update(LOOKUPS_EXTRA)

# ---------------------------------------------------------------------------
# Settings / company
# ---------------------------------------------------------------------------
SETTINGS = [
    ("Company Name", "Novality Store"),
    ("Product Name", "Home Renovation Management System"),
    ("Version", "2.0.0"),
    ("Homeowner", "Alex Rivera"),
    ("Active Project ID", "PRJ-001"),
    ("Active Property ID", "PROP-001"),
    ("Currency", "USD"),
    ("Currency Symbol", "$"),
    ("Language", "English"),
    ("Contingency %", 0.10),
    ("Fiscal Year Start", date(2026, 1, 1)),
    ("Today (system)", TODAY),
    ("Timezone", "America/Los_Angeles"),
    ("Tax Rate", 0.0),
    ("Default Payment Terms (days)", 14),
    ("Maintenance Reminder (days)", 14),
    ("Document Expiry Reminder (days)", 30),
    ("Low Contingency Threshold", 0.10),
    ("Budget Overrun Alert %", 0.10),
    ("Support Email", "studio@novalitystore.example"),
    ("Primary Color", "#16352F"),
    ("Secondary Color", "#E8DDCB"),
    ("Accent Color", "#C86B4A"),
    ("Background Color", "#F8F6F1"),
    ("Success Color", "#719B7A"),
    ("Warning Color", "#D99A3D"),
    ("Danger Color", "#C75C5C"),
]

# ---------------------------------------------------------------------------
# Properties
# ---------------------------------------------------------------------------
PROPERTIES = [
    [
        "PROP-001",
        "Maplewood Residence",
        "1847 Maplewood Drive",
        "Portland",
        "OR",
        "97214",
        "USA",
        "Single Family",
        1928,
        2480,
        2,
        4,
        2.5,
        "Alex Rivera",
        "HO-001",
        "State Farm HO-34821",
        2027,
        "Craftsman with later additions. Knob-and-tube mostly retired.",
    ],
    [
        "PROP-002",
        "Columbia Gorge Cabin",
        "88 Ridge Trail",
        "Hood River",
        "OR",
        "97031",
        "USA",
        "Cabin",
        1998,
        980,
        1,
        2,
        1,
        "Alex Rivera",
        "HO-001",
        "State Farm HO-34822",
        2027,
        "Weekend cabin. Bath refresh only.",
    ],
]

# ---------------------------------------------------------------------------
# Users (all 9 roles)
# ---------------------------------------------------------------------------
USERS = [
    ["HO-001", "Alex Rivera", "alex.rivera@email.example", "+1-503-555-0148", "Homeowner", "Rivera Household", "Active", date(2026, 8, 24), "Full project visibility, approvals, payments"],
    ["AD-001", "Morgan Ellis", "morgan@novalitystore.example", "+1-503-555-0100", "Admin", "Novality Store", "Active", date(2026, 8, 24), "System admin, all properties"],
    ["PM-001", "Marcus Webb", "marcus@ironwood.build", "+1-503-555-0172", "Project Manager", "Ironwood Construction", "Active", date(2026, 8, 23), "Schedule, contractors, inspections"],
    ["DS-001", "Sofia Alvarez", "sofia@lunainteriors.example", "+1-503-555-0194", "Interior Designer", "Luna Interiors", "Active", date(2026, 8, 22), "Design studio, materials, mood boards"],
    ["CT-001", "Maya Chen", "maya@cascadecabinets.example", "+1-503-555-0111", "Contractor", "Cascade Cabinets", "Active", date(2026, 8, 21), "Kitchen millwork"],
    ["SC-001", "Devon Ruiz", "devon@nw-electric.example", "+1-503-555-0133", "Subcontractor", "Northwest Electric", "Active", date(2026, 8, 20), "Electrical rough and finish"],
    ["SU-001", "Harper Quinn", "orders@tileandtimber.example", "+1-503-555-0160", "Supplier", "Tile & Timber Co.", "Active", date(2026, 8, 18), "Materials, lead times"],
    ["IN-001", "Riley Grant", "r.grant@portland.gov.example", "+1-503-555-0188", "Inspector", "City of Portland", "Active", date(2026, 8, 12), "Building, electrical, plumbing"],
    ["AC-001", "Jamie Cole", "jamie@novalitystore.example", "+1-503-555-0108", "Accountant", "Novality Store", "Active", date(2026, 8, 24), "Invoices, tax, payments"],
]

# ---------------------------------------------------------------------------
# Projects
# ---------------------------------------------------------------------------
PROJECTS = [
    [
        "PRJ-001",
        "PROP-001",
        "Maplewood Whole-Home Refresh",
        "Whole Home",
        "Active",
        "Construction",
        date(2026, 3, 1),
        date(2026, 11, 15),
        None,
        85000,
        "HO-001",
        "PM-001",
        "DS-001",
        "Alex Rivera",
        "1847 Maplewood Drive, Portland, OR",
        0.72,
        "Kitchen, primary bath, living, guest bedroom, exterior paint, garden path.",
    ],
    [
        "PRJ-002",
        "PROP-002",
        "Gorge Cabin Bath Refresh",
        "Bathroom",
        "Planning",
        "Design",
        date(2026, 10, 1),
        date(2026, 12, 15),
        None,
        18500,
        "HO-001",
        "PM-001",
        "DS-001",
        "Alex Rivera",
        "88 Ridge Trail, Hood River, OR",
        0.12,
        "Single bath + vanity lighting. Starts after Maplewood handover.",
    ],
]

# ---------------------------------------------------------------------------
# Rooms
# ---------------------------------------------------------------------------
ROOMS = [
    ["RM-01", "PRJ-001", "Kitchen", "Kitchen", 1, 16.0, 12.5, 9.0, "Fair", "In Progress", 32000, "CTR-001", "Modern", "drive/photos/kitchen-before", "drive/photos/kitchen-wip", "Load-bearing wall stays. Island added."],
    ["RM-02", "PRJ-001", "Living Room", "Living Room", 1, 20.0, 15.0, 9.5, "Good", "In Progress", 12500, "CTR-006", "Scandinavian", "drive/photos/living-before", "", "White oak floors continue from kitchen."],
    ["RM-03", "PRJ-001", "Primary Bathroom", "Primary Bathroom", 2, 10.0, 8.0, 8.5, "Poor", "Punch List", 18500, "CTR-004", "Luxury", "drive/photos/bath-before", "drive/photos/bath-after-draft", "Heated floor. Porcelain in lieu of marble."],
    ["RM-04", "PRJ-001", "Guest Bedroom", "Bedroom", 2, 12.0, 11.0, 8.5, "Fair", "Design", 6200, "CTR-005", "Minimal", "drive/photos/guest-before", "", "Paint, lighting, built-in wardrobe."],
    ["RM-05", "PRJ-001", "Dining Room", "Dining Room", 1, 13.0, 11.0, 9.5, "Good", "In Progress", 4800, "CTR-005", "Transitional", "drive/photos/dining-before", "", "Sconce pair + plaster repair."],
    ["RM-06", "PRJ-001", "Exterior / Garden", "Exterior", 0, 40.0, 22.0, 0.0, "Fair", "Not Started", 7400, "CTR-010", "Traditional", "drive/photos/exterior-before", "", "Front path, porch stain, lighting."],
    ["RM-07", "PRJ-001", "Laundry", "Laundry", 1, 8.0, 6.0, 8.5, "Fair", "Complete", 2100, "CTR-003", "Minimal", "drive/photos/laundry-before", "drive/photos/laundry-after", "Utility sink and tile splash."],
    ["RM-08", "PRJ-001", "Entry / Foyer", "Entry / Foyer", 1, 8.0, 7.0, 9.5, "Good", "In Progress", 1500, "CTR-005", "Transitional", "drive/photos/entry-before", "", "Bench, hook rail, paint."],
    ["RM-09", "PRJ-002", "Cabin Bathroom", "Bathroom", 1, 8.0, 6.5, 8.0, "Poor", "Design", 18500, "CTR-004", "Scandinavian", "drive/photos/cabin-bath-before", "", "Full gut. Starts October."],
]

# ---------------------------------------------------------------------------
# Design studio
# ---------------------------------------------------------------------------
DESIGNS = [
    ["DSN-001", "PRJ-001", "RM-01", "Mood Board", "Kitchen — warm modern", "Modern", "", "#16352F", "drive/mood/kitchen-01", "Approved", 0, "No", "Forest + sand + terracotta. Brass hardware."],
    ["DSN-002", "PRJ-001", "RM-01", "Color Palette", "Kitchen palette v3", "Modern", "Farrow & Ball", "#E8DDCB", "drive/palette/kitchen", "Approved", 0, "Yes", "AI suggested dropping cool gray for sand."],
    ["DSN-003", "PRJ-001", "RM-01", "Cabinetry", "Shaker, painted sage", "Modern", "Cascade", "#719B7A", "drive/cabs/shaker-sage", "Approved", 14800, "No", "Inset doors, walnut island."],
    ["DSN-004", "PRJ-001", "RM-01", "Flooring", "White oak 7in", "Scandinavian", "Timberline", "#D4C6AE", "drive/floor/oak", "Installed", 4200, "No", "Continues into living + dining."],
    ["DSN-005", "PRJ-001", "RM-01", "Lighting", "Aged brass pendants x3", "Luxury", "BrightPath", "#C86B4A", "drive/light/island", "Ordered", 890, "No", "Dimmer on island circuit."],
    ["DSN-006", "PRJ-001", "RM-03", "Material Board", "Bath — porcelain in lieu of marble", "Luxury", "Heritage", "#F8F6F1", "drive/bath/materials", "Approved", 0, "Yes", "AI: porcelain saves ~18% vs marble."],
    ["DSN-007", "PRJ-001", "RM-03", "AI Concept", "Primary bath — spa luxury", "Luxury", "", "", "drive/ai/bath-luxury", "Accepted", 0, "Yes", "Before/after concept set."],
    ["DSN-008", "PRJ-001", "RM-02", "Mood Board", "Living — Scandinavian calm", "Scandinavian", "", "#E8DDCB", "drive/mood/living", "Approved", 0, "No", "Linen, oak, charcoal textiles."],
    ["DSN-009", "PRJ-001", "RM-02", "Furniture", "Modular sofa + oak table", "Scandinavian", "Article", "#202522", "drive/furn/living", "Quoted", 3400, "No", "Lead time 6 weeks — order by Sep 1."],
    ["DSN-010", "PRJ-001", "RM-04", "Color Palette", "Guest — clay + linen", "Minimal", "Benjamin Moore", "#C86B4A", "drive/palette/guest", "In Review", 0, "Yes", "Two accent options pending Alex."],
    ["DSN-011", "PRJ-001", "RM-01", "2D Floor Plan", "Kitchen layout v4", "Modern", "Luna", "", "drive/plans/kitchen-v4", "Approved", 0, "No", "Island 8ft. Fridge wall flipped."],
    ["DSN-012", "PRJ-001", "RM-01", "3D Visualization", "Kitchen dusk render", "Modern", "Luna", "", "drive/3d/kitchen-dusk", "Approved", 0, "Yes", "AI lighting study included."],
    ["DSN-013", "PRJ-002", "RM-09", "Mood Board", "Cabin bath — Japandi", "Japandi", "", "#16352F", "drive/mood/cabin", "Draft", 0, "Yes", "Cedar, plaster, black fixtures."],
]

# ---------------------------------------------------------------------------
# AI insights
# ---------------------------------------------------------------------------
AI_INSIGHTS = [
    ["AI-001", date(2026, 8, 20), "PRJ-001", "RM-01", "Budget", "Warning",
     "Kitchen renovation is currently 12% over the planned budget.",
     "Switch remaining stone from marble to porcelain slab on the island only; keep quartz on perimeter.",
     2100, "Accepted", "Quote requested from Heritage Tile"],
    ["AI-002", date(2026, 8, 18), "PRJ-001", "RM-03", "Materials", "Opportunity",
     "Porcelain tile alternative identified for primary bath floor.",
     "Heritage porcelain (SKU HT-8841) matches the approved palette and saves ~18% versus marble.",
     1640, "Resolved", "Material swapped. Installed."],
    ["AI-003", date(2026, 8, 22), "PRJ-001", "RM-01", "Schedule", "Warning",
     "Cabinet installation is on the critical path and hardware is still in transit.",
     "Confirm hardware ETA. If later than Aug 27, install doors without pulls and return for hardware day.",
     0, "In Progress", "Maya tracking shipment"],
    ["AI-004", date(2026, 8, 15), "PRJ-001", "", "Contractor", "Info",
     "Three lighting bids received. Spread is 22%.",
     "BrightPath is mid-price with the highest communication score. Accept unless value-engineering fixtures.",
     340, "Accepted", "BrightPath awarded"],
    ["AI-005", date(2026, 8, 23), "PRJ-001", "RM-06", "Risk", "Critical",
     "Project contingency has fallen to 9.4%, below the 10% threshold.",
     "Freeze non-critical exterior extras (water feature) until kitchen close-out.",
     1800, "New", ""],
    ["AI-006", date(2026, 8, 10), "PRJ-001", "RM-02", "Design", "Opportunity",
     "Room photo analysis: north-facing living room reads cool and dim after 4pm.",
     "Specify 2700K lamps, add floor lamp at north corner, keep walls in Warm Sand not cool gray.",
     0, "Resolved", "Palette updated"],
    ["AI-007", date(2026, 8, 21), "PRJ-001", "", "Procurement", "Warning",
     "White oak stair nosing is backordered 11 days.",
     "Use matching leftover plank with site-cut nosing, or delay living-room furniture delivery.",
     0, "Accepted", "Site-cut nosing approved"],
    ["AI-008", date(2026, 8, 24), "PRJ-001", "", "Prediction", "Info",
     "Likely completion date given current float: 12 Nov 2026 (3 days ahead of target).",
     "Protect flooring cure time. Do not accelerate furniture move-in before Oct 20.",
     0, "New", ""],
]

# ---------------------------------------------------------------------------
# Budget lines  (planned amounts; spent/committed computed from Expenses)
# ---------------------------------------------------------------------------
BUDGET = [
    ["BL-001", "PRJ-001", "RM-01", "Materials", "Cabinetry & hardware", 14800],
    ["BL-002", "PRJ-001", "RM-01", "Materials", "Counters & backsplash", 6200],
    ["BL-003", "PRJ-001", "RM-01", "Materials", "Appliances", 5400],
    ["BL-004", "PRJ-001", "RM-01", "Labor", "Cabinet install + finish carpentry", 3600],
    ["BL-005", "PRJ-001", "RM-01", "Labor", "Plumbing relocate", 1400],
    ["BL-006", "PRJ-001", "RM-01", "Labor", "Electrical / lighting", 600],
    ["BL-007", "PRJ-001", "RM-02", "Materials", "White oak flooring (share)", 2800],
    ["BL-008", "PRJ-001", "RM-02", "Labor", "Floor install + finish", 2200],
    ["BL-009", "PRJ-001", "RM-02", "Furniture", "Sofa, table, lighting", 4200],
    ["BL-010", "PRJ-001", "RM-02", "Materials", "Paint & plaster", 900],
    ["BL-011", "PRJ-001", "RM-02", "Labor", "Paint labor", 1400],
    ["BL-012", "PRJ-001", "RM-03", "Materials", "Tile, fixtures, vanity", 9200],
    ["BL-013", "PRJ-001", "RM-03", "Labor", "Tile + plumbing + electric", 6800],
    ["BL-014", "PRJ-001", "RM-03", "Materials", "Heated floor system", 1800],
    ["BL-015", "PRJ-001", "RM-04", "Materials", "Paint, lighting, wardrobe", 2800],
    ["BL-016", "PRJ-001", "RM-04", "Labor", "Paint + carpentry", 2200],
    ["BL-017", "PRJ-001", "RM-04", "Furniture", "Bed + textiles", 1200],
    ["BL-018", "PRJ-001", "RM-05", "Materials", "Lighting + plaster", 1600],
    ["BL-019", "PRJ-001", "RM-05", "Labor", "Paint + electric", 2000],
    ["BL-020", "PRJ-001", "RM-05", "Furniture", "Dining table remainder", 1200],
    ["BL-021", "PRJ-001", "RM-06", "Materials", "Path, stain, fixtures", 3400],
    ["BL-022", "PRJ-001", "RM-06", "Labor", "Landscape + paint", 4000],
    ["BL-023", "PRJ-001", "RM-07", "Materials", "Tile + sink", 900],
    ["BL-024", "PRJ-001", "RM-07", "Labor", "Install", 1200],
    ["BL-025", "PRJ-001", "RM-08", "Materials", "Bench + rail + paint", 700],
    ["BL-026", "PRJ-001", "RM-08", "Labor", "Carpentry + paint", 800],
    ["BL-027", "PRJ-001", "", "Design", "Luna Interiors retainer + hours", 4800],
    ["BL-028", "PRJ-001", "", "Permits", "Building, electrical, plumbing", 1850],
    ["BL-029", "PRJ-001", "", "Delivery", "Freight & white-glove", 900],
    ["BL-030", "PRJ-001", "", "Inspections", "City + independent", 650],
    ["BL-031", "PRJ-001", "", "Contingency", "10% project reserve", 8500],
    ["BL-032", "PRJ-001", "RM-01", "Labor", "Demolition (kitchen share)", 0],  # rolled into GC
    ["BL-033", "PRJ-001", "", "Labor", "General contractor / PM", 6200],
    ["BL-034", "PRJ-002", "RM-09", "Materials", "Cabin bath package", 9200],
    ["BL-035", "PRJ-002", "RM-09", "Labor", "Gut and reset", 6800],
    ["BL-036", "PRJ-002", "", "Design", "Concept + drawings", 1200],
    ["BL-037", "PRJ-002", "", "Contingency", "10% reserve", 1300],
]

# ---------------------------------------------------------------------------
# Expenses
# ---------------------------------------------------------------------------
EXPENSES = [
    ["EXP-001", date(2026, 3, 8), "PRJ-001", "", "Design", "Luna Interiors", "Design retainer", 2400, "ACH", "Paid", "INV-LUNA-110", "Alex Rivera"],
    ["EXP-002", date(2026, 4, 2), "PRJ-001", "", "Permits", "City of Portland", "Building permit", 840, "Credit Card", "Paid", "PMT-2026-441", "Marcus Webb"],
    ["EXP-003", date(2026, 4, 18), "PRJ-001", "", "Permits", "City of Portland", "Electrical + plumbing permits", 610, "Credit Card", "Paid", "PMT-2026-478", "Marcus Webb"],
    ["EXP-004", date(2026, 5, 4), "PRJ-001", "", "Design", "Luna Interiors", "Drawings + 3D package", 1800, "ACH", "Paid", "INV-LUNA-126", "Alex Rivera"],
    ["EXP-005", date(2026, 5, 22), "PRJ-001", "", "Labor", "Ironwood Construction", "Demolition + dumpsters", 2800, "Check", "Paid", "INV-IW-204", "Alex Rivera"],
    ["EXP-006", date(2026, 6, 6), "PRJ-001", "RM-01", "Labor", "Northwest Electric", "Kitchen / bath rough-in", 1900, "ACH", "Paid", "INV-NWE-88", "Marcus Webb"],
    ["EXP-007", date(2026, 6, 12), "PRJ-001", "RM-03", "Labor", "Pacific Plumbing", "Bath / laundry rough-in", 2400, "ACH", "Paid", "INV-PP-301", "Marcus Webb"],
    ["EXP-008", date(2026, 6, 20), "PRJ-001", "RM-03", "Materials", "Tile & Timber Co.", "Porcelain floor + wall tile", 3180, "Credit Card", "Paid", "PO-114", "Sofia Alvarez"],
    ["EXP-009", date(2026, 6, 28), "PRJ-001", "RM-03", "Materials", "Ferguson", "Bath fixtures package", 2140, "Credit Card", "Paid", "FERG-9921", "Sofia Alvarez"],
    ["EXP-010", date(2026, 7, 2), "PRJ-001", "RM-03", "Materials", "WarmFloor Co.", "Heated floor kit", 1680, "Credit Card", "Paid", "WF-441", "Marcus Webb"],
    ["EXP-011", date(2026, 7, 8), "PRJ-001", "RM-01", "Labor", "Pacific Plumbing", "Kitchen sink relocate", 1280, "ACH", "Paid", "INV-PP-318", "Marcus Webb"],
    ["EXP-012", date(2026, 7, 15), "PRJ-001", "RM-03", "Labor", "Heritage Tile & Stone", "Primary bath tile labor (50%)", 2100, "ACH", "Paid", "INV-HT-77", "Marcus Webb"],
    ["EXP-013", date(2026, 7, 18), "PRJ-001", "RM-07", "Materials", "Tile & Timber Co.", "Laundry tile + sink", 860, "Credit Card", "Paid", "PO-129", "Sofia Alvarez"],
    ["EXP-014", date(2026, 7, 22), "PRJ-001", "RM-07", "Labor", "Pacific Plumbing", "Laundry install", 980, "ACH", "Paid", "INV-PP-330", "Marcus Webb"],
    ["EXP-015", date(2026, 7, 28), "PRJ-001", "RM-01", "Materials", "Timberline Floors", "White oak 7in — kitchen/living/dining", 6400, "ACH", "Paid", "PO-140", "Sofia Alvarez"],
    ["EXP-016", date(2026, 8, 2), "PRJ-001", "RM-01", "Materials", "Cascade Cabinets", "Cabinet deposit 50%", 7400, "Wire", "Paid", "INV-CC-501", "Alex Rivera"],
    ["EXP-017", date(2026, 8, 5), "PRJ-001", "RM-02", "Labor", "Timberline Floors", "Floor install progress", 1800, "ACH", "Paid", "INV-TF-19", "Marcus Webb"],
    ["EXP-018", date(2026, 8, 8), "PRJ-001", "RM-03", "Labor", "Heritage Tile & Stone", "Bath tile labor remainder", 2100, "ACH", "Paid", "INV-HT-81", "Marcus Webb"],
    ["EXP-019", date(2026, 8, 10), "PRJ-001", "RM-03", "Labor", "Pacific Plumbing", "Bath trim-out", 1460, "ACH", "Paid", "INV-PP-341", "Marcus Webb"],
    ["EXP-020", date(2026, 8, 12), "PRJ-001", "", "Inspections", "City of Portland", "Plumbing + electrical inspection", 240, "Credit Card", "Paid", "INSP-0812", "Marcus Webb"],
    ["EXP-021", date(2026, 8, 14), "PRJ-001", "RM-01", "Materials", "Sub-Zero / Wolf dealer", "Range + fridge deposit", 2700, "Credit Card", "Paid", "APPL-01", "Alex Rivera"],
    ["EXP-022", date(2026, 8, 16), "PRJ-001", "RM-01", "Materials", "Caesarstone", "Perimeter quartz", 2480, "Credit Card", "Paid", "CS-882", "Sofia Alvarez"],
    ["EXP-023", date(2026, 8, 18), "PRJ-001", "", "Labor", "Ironwood Construction", "August PM / supervision", 1550, "ACH", "Paid", "INV-IW-228", "Alex Rivera"],
    ["EXP-024", date(2026, 8, 20), "PRJ-001", "RM-01", "Delivery", "Cascade Cabinets", "Cabinet freight", 420, "Credit Card", "Paid", "FRT-88", "Maya Chen"],
    ["EXP-025", date(2026, 8, 22), "PRJ-001", "RM-05", "Materials", "BrightPath Lighting", "Dining sconces", 380, "Credit Card", "Paid", "BP-204", "Sofia Alvarez"],
    ["EXP-026", date(2026, 8, 25), "PRJ-001", "RM-01", "Materials", "Cascade Cabinets", "Cabinet balance", 7400, "Wire", "Committed", "INV-CC-502", "Alex Rivera"],
    ["EXP-027", date(2026, 8, 28), "PRJ-001", "RM-01", "Labor", "Cascade Cabinets", "Install labor", 3600, "ACH", "Committed", "INV-CC-510", "Marcus Webb"],
    ["EXP-028", date(2026, 9, 4), "PRJ-001", "RM-01", "Materials", "Heritage Tile & Stone", "Island porcelain slab", 1860, "Credit Card", "Committed", "PO-155", "Sofia Alvarez"],
    ["EXP-029", date(2026, 9, 8), "PRJ-001", "RM-01", "Materials", "BrightPath Lighting", "Island pendants", 890, "Credit Card", "Planned", "BP-220", "Sofia Alvarez"],
    ["EXP-030", date(2026, 9, 12), "PRJ-001", "RM-04", "Materials", "Sherwin-Williams", "Guest bedroom paint", 240, "Credit Card", "Planned", "", ""],
    ["EXP-031", date(2026, 9, 18), "PRJ-001", "RM-02", "Furniture", "Article", "Sofa + coffee table", 3400, "Credit Card", "Planned", "", "Sofia Alvarez"],
    ["EXP-032", date(2026, 10, 2), "PRJ-001", "RM-06", "Materials", "Garden & Gate", "Path stone deposit", 1200, "Check", "Planned", "", ""],
    ["EXP-033", date(2026, 8, 1), "PRJ-002", "", "Design", "Luna Interiors", "Cabin bath concept", 600, "ACH", "Paid", "INV-LUNA-140", "Alex Rivera"],
    ["EXP-034", date(2026, 7, 30), "PRJ-001", "RM-01", "Labor", "Northwest Electric", "Finish electrical progress", 720, "ACH", "Paid", "INV-NWE-97", "Marcus Webb"],
    ["EXP-035", date(2026, 8, 19), "PRJ-001", "RM-08", "Materials", "Rejuvenation", "Hook rail + hooks", 186, "Credit Card", "Paid", "REJ-33", "Alex Rivera"],
]

# ---------------------------------------------------------------------------
# Contractors
# ---------------------------------------------------------------------------
CONTRACTORS = [
    ["CTR-001", "Cascade Cabinets", "Maya Chen", "Cabinetry", "Custom millwork, inset doors", "+1-503-555-0111", "maya@cascadecabinets.example", 4.8, 0.92, 0.87, 0.95, 0.90, date(2027, 3, 1), "CCB-210998", "Aug 20–Sep 15", 85, "Active", "drive/portfolio/cascade"],
    ["CTR-002", "Northwest Electric", "Jordan Hale", "Electrical", "Residential remodel, lighting", "+1-503-555-0133", "jordan@nw-electric.example", 4.7, 0.94, 0.91, 0.88, 0.86, date(2026, 12, 15), "EL-44821", "On call", 110, "Active", "drive/portfolio/nwe"],
    ["CTR-003", "Pacific Plumbing", "Sam Ortiz", "Plumbing", "Repipe, fixtures, radiant", "+1-503-555-0140", "sam@pacificplumbing.example", 4.6, 0.90, 0.84, 0.93, 0.88, date(2027, 1, 20), "PL-77310", "Wrap this week", 120, "Active", "drive/portfolio/pp"],
    ["CTR-004", "Heritage Tile & Stone", "Priya Shah", "Tile & Stone", "Porcelain, slab, steam", "+1-503-555-0155", "priya@heritagetile.example", 4.9, 0.96, 0.89, 0.91, 0.93, date(2027, 6, 1), "CCB-188442", "Punch list", 95, "Active", "drive/portfolio/heritage"],
    ["CTR-005", "Greenfield Painting", "Leo Park", "Painting", "Plaster, limewash, cabinets", "+1-503-555-0122", "leo@greenfieldpaint.example", 4.5, 0.88, 0.90, 0.86, 0.91, date(2026, 11, 30), "CCB-201774", "Sep 10–28", 65, "Active", "drive/portfolio/greenfield"],
    ["CTR-006", "Timberline Floors", "Elena Voss", "Flooring", "White oak, site finish", "+1-503-555-0166", "elena@timberlinefloors.example", 4.7, 0.91, 0.83, 0.90, 0.87, date(2027, 2, 14), "CCB-176330", "Through Aug 28", 8, "Active", "drive/portfolio/timberline"],
    ["CTR-007", "Luna Interiors", "Sofia Alvarez", "Interior Designer", "Residential, kitchen, bath", "+1-503-555-0194", "sofia@lunainteriors.example", 4.9, 0.95, 0.94, 0.89, 0.97, date(2026, 10, 1), "ASID-4491", "Ongoing", 145, "Active", "drive/portfolio/luna"],
    ["CTR-008", "Ironwood Construction", "Marcus Webb", "General Contractor", "Remodel GC, historic homes", "+1-503-555-0172", "marcus@ironwood.build", 4.8, 0.93, 0.88, 0.92, 0.94, date(2027, 4, 30), "CCB-154009", "Full project", 0, "Active", "drive/portfolio/ironwood"],
    ["CTR-009", "BrightPath Lighting", "Nina Cho", "Lighting", "Specification + supply", "+1-503-555-0180", "nina@brightpath.example", 4.6, 0.90, 0.92, 0.94, 0.89, date(2026, 9, 30), "SUP-8891", "Lead time 3 wks", 0, "Active", "drive/portfolio/brightpath"],
    ["CTR-010", "Garden & Gate", "Theo Brooks", "Landscaping", "Paths, planting, irrigation", "+1-503-555-0199", "theo@gardengate.example", 4.4, 0.86, 0.80, 0.88, 0.85, date(2027, 5, 1), "LCB-3320", "Oct window", 70, "Active", "drive/portfolio/gg"],
    ["CTR-011", "Alder Inspection Group", "Riley Grant", "Inspection", "Independent punch", "+1-503-555-0188", "riley@alderinspect.example", 4.8, 0.97, 0.95, 1.00, 0.90, date(2026, 12, 31), "OR-INSP-220", "On call", 175, "Active", ""],
]

# ---------------------------------------------------------------------------
# Quotes
# ---------------------------------------------------------------------------
QUOTES = [
    ["Q-001", "PRJ-001", "RM-01", "CTR-001", "Cabinetry", "Full kitchen millwork — sage shaker + walnut island", 14800, 18, date(2026, 5, 30), "Accepted", "Awarded. Deposit paid."],
    ["Q-002", "PRJ-001", "RM-01", "CTR-001", "Cabinetry", "Alternate: all walnut", 18600, 22, date(2026, 5, 30), "Rejected", "Over palette and budget."],
    ["Q-003", "PRJ-001", "RM-03", "CTR-004", "Tile & Stone", "Marble floor + shower", 9100, 14, date(2026, 5, 20), "Rejected", "AI flagged 18% save with porcelain."],
    ["Q-004", "PRJ-001", "RM-03", "CTR-004", "Tile & Stone", "Porcelain floor + shower + slab niche", 7460, 12, date(2026, 5, 20), "Accepted", "Selected."],
    ["Q-005", "PRJ-001", "", "CTR-009", "Lighting", "Whole-home spec package", 4120, 21, date(2026, 6, 15), "Accepted", "Best communication score."],
    ["Q-006", "PRJ-001", "", "CTR-009", "Lighting", "Competitor A package", 3680, 28, date(2026, 6, 15), "Compared", "Cheaper, slower, weaker spec."],
    ["Q-007", "PRJ-001", "", "CTR-009", "Lighting", "Competitor B package", 4490, 18, date(2026, 6, 15), "Compared", "Premium, not needed."],
    ["Q-008", "PRJ-001", "RM-02", "CTR-006", "Flooring", "White oak supply + install", 8600, 16, date(2026, 6, 1), "Accepted", "Shared across 3 rooms."],
    ["Q-009", "PRJ-001", "RM-06", "CTR-010", "Landscaping", "Path + planting + lighting", 7400, 12, date(2026, 9, 15), "Received", "Hold extras until contingency recovers."],
    ["Q-010", "PRJ-002", "RM-09", "CTR-004", "Tile & Stone", "Cabin bath tile package", 5400, 10, date(2026, 10, 30), "Requested", ""],
]

# ---------------------------------------------------------------------------
# Jobs / assignments
# ---------------------------------------------------------------------------
JOBS = [
    ["JOB-001", "PRJ-001", "", "CTR-008", "Q-000", "GC / project management", date(2026, 3, 1), date(2026, 11, 15), "Monthly supervision", "In Progress", 6200, 4350],
    ["JOB-002", "PRJ-001", "RM-01", "CTR-001", "Q-001", "Kitchen cabinetry fabricate + install", date(2026, 8, 20), date(2026, 9, 15), "Boxes set; doors next", "In Progress", 18400, 7400],
    ["JOB-003", "PRJ-001", "RM-03", "CTR-004", "Q-004", "Primary bath tile", date(2026, 7, 8), date(2026, 8, 12), "Complete — punch remaining", "Milestone Review", 7460, 7460],
    ["JOB-004", "PRJ-001", "RM-01", "CTR-002", "Q-000", "Electrical rough + finish", date(2026, 6, 1), date(2026, 9, 20), "Finish pending cabinets", "In Progress", 2620, 2620],
    ["JOB-005", "PRJ-001", "RM-03", "CTR-003", "Q-000", "Plumbing rough + trim", date(2026, 6, 8), date(2026, 8, 14), "Trim complete", "Complete", 5140, 5140],
    ["JOB-006", "PRJ-001", "RM-02", "CTR-006", "Q-008", "Flooring install", date(2026, 8, 5), date(2026, 8, 28), "Sand/finish this week", "In Progress", 8600, 8200],
    ["JOB-007", "PRJ-001", "", "CTR-007", "Q-000", "Interior design services", date(2026, 3, 1), date(2026, 11, 1), "FF&E procurement", "In Progress", 4800, 4200],
    ["JOB-008", "PRJ-001", "RM-04", "CTR-005", "Q-000", "Paint guest + dining + entry", date(2026, 9, 10), date(2026, 9, 28), "Scheduled", "Scheduled", 3600, 0],
    ["JOB-009", "PRJ-001", "RM-06", "CTR-010", "Q-009", "Exterior path + porch", date(2026, 10, 6), date(2026, 10, 24), "Not released", "Assigned", 7400, 0],
    ["JOB-010", "PRJ-001", "", "CTR-009", "Q-005", "Lighting supply", date(2026, 7, 1), date(2026, 9, 20), "Pendants in transit", "In Progress", 4120, 380],
]

# ---------------------------------------------------------------------------
# Tasks
# ---------------------------------------------------------------------------
TASKS = [
    ["TSK-001", "PRJ-001", "", "Kickoff + scope lock", "Confirm rooms, budget, style.", "Marcus Webb", "Project Manager", "Completed", "High", date(2026, 3, 1), date(2026, 3, 8), 0, "", 1, "drive/notes/kickoff"],
    ["TSK-002", "PRJ-001", "RM-01", "Kitchen measured drawings", "Field measure + as-builts.", "Sofia Alvarez", "Interior Designer", "Completed", "High", date(2026, 3, 10), date(2026, 3, 20), 0, "", 1, ""],
    ["TSK-003", "PRJ-001", "", "Submit building permit", "Packet to City of Portland.", "Marcus Webb", "Project Manager", "Completed", "Critical", date(2026, 4, 1), date(2026, 4, 10), 840, "", 1, ""],
    ["TSK-004", "PRJ-001", "RM-01", "Kitchen demolition", "Cabinets, floor, plaster.", "Marcus Webb", "Project Manager", "Completed", "High", date(2026, 5, 21), date(2026, 6, 5), 2800, "TSK-003", 1, "drive/photos/demo"],
    ["TSK-005", "PRJ-001", "RM-01", "Electrical rough-in", "New circuits, island, lighting.", "Jordan Hale", "Subcontractor", "Completed", "High", date(2026, 6, 1), date(2026, 6, 20), 1900, "TSK-004", 1, ""],
    ["TSK-006", "PRJ-001", "RM-03", "Plumbing rough-in", "Bath + laundry + kitchen stub.", "Sam Ortiz", "Contractor", "Completed", "High", date(2026, 6, 8), date(2026, 6, 28), 2400, "TSK-004", 1, ""],
    ["TSK-007", "PRJ-001", "RM-03", "Heated floor install", "WarmFloor mat + thermostat.", "Sam Ortiz", "Contractor", "Completed", "Medium", date(2026, 7, 2), date(2026, 7, 6), 1680, "TSK-006", 1, ""],
    ["TSK-008", "PRJ-001", "RM-03", "Tile primary bath", "Floor, shower, niche.", "Priya Shah", "Contractor", "Completed", "High", date(2026, 7, 8), date(2026, 8, 8), 4200, "TSK-007", 1, ""],
    ["TSK-009", "PRJ-001", "RM-03", "Bath fixture trim", "Valve trims, vanity, toilet, glass.", "Sam Ortiz", "Contractor", "Completed", "High", date(2026, 8, 9), date(2026, 8, 14), 1460, "TSK-008", 1, ""],
    ["TSK-010", "PRJ-001", "RM-03", "Primary bath punch", "Silicone, grout haze, door align.", "Priya Shah", "Contractor", "Inspection", "Medium", date(2026, 8, 18), date(2026, 8, 26), 0, "TSK-009", 0.8, ""],
    ["TSK-011", "PRJ-001", "RM-07", "Laundry complete", "Tile splash + utility sink.", "Sam Ortiz", "Contractor", "Completed", "Low", date(2026, 7, 18), date(2026, 7, 24), 1840, "", 1, ""],
    ["TSK-012", "PRJ-001", "RM-01", "White oak flooring", "Install kitchen/living/dining.", "Elena Voss", "Contractor", "In Progress", "Critical", date(2026, 8, 5), date(2026, 8, 28), 8200, "TSK-005", 0.75, ""],
    ["TSK-013", "PRJ-001", "RM-01", "Cabinet box set", "Set boxes, scribe, level island.", "Maya Chen", "Contractor", "In Progress", "Critical", date(2026, 8, 20), date(2026, 8, 27), 0, "TSK-012", 0.55, ""],
    ["TSK-014", "PRJ-001", "RM-01", "Cabinet doors + hardware", "Hang doors, install pulls.", "Maya Chen", "Contractor", "Scheduled", "Critical", date(2026, 8, 28), date(2026, 9, 5), 0, "TSK-013", 0, "Hardware in transit"],
    ["TSK-015", "PRJ-001", "RM-01", "Counter template", "Quartz + island porcelain.", "Heritage Tile", "Contractor", "Scheduled", "High", date(2026, 9, 4), date(2026, 9, 4), 0, "TSK-014", 0, ""],
    ["TSK-016", "PRJ-001", "RM-01", "Counter install", "Set, seam, sink.", "Heritage Tile", "Contractor", "To Do", "High", date(2026, 9, 10), date(2026, 9, 11), 1860, "TSK-015", 0, ""],
    ["TSK-017", "PRJ-001", "RM-01", "Appliance delivery", "Range, fridge, DW.", "Alex Rivera", "Homeowner", "Scheduled", "High", date(2026, 9, 12), date(2026, 9, 12), 2700, "TSK-016", 0, ""],
    ["TSK-018", "PRJ-001", "RM-01", "Island pendant hang", "Three aged-brass pendants.", "Nina Cho", "Supplier", "To Do", "Medium", date(2026, 9, 16), date(2026, 9, 16), 890, "TSK-017", 0, ""],
    ["TSK-019", "PRJ-001", "RM-04", "Guest bedroom paint", "Clay + linen palette.", "Leo Park", "Contractor", "Scheduled", "Medium", date(2026, 9, 10), date(2026, 9, 16), 240, "", 0, "Awaiting palette lock"],
    ["TSK-020", "PRJ-001", "RM-05", "Dining plaster + paint", "Repair north wall, paint.", "Leo Park", "Contractor", "Scheduled", "Medium", date(2026, 9, 17), date(2026, 9, 22), 0, "", 0, ""],
    ["TSK-021", "PRJ-001", "RM-08", "Entry bench + rail", "White oak bench, brass hooks.", "Marcus Webb", "Project Manager", "In Progress", "Low", date(2026, 8, 18), date(2026, 8, 29), 186, "", 0.4, ""],
    ["TSK-022", "PRJ-001", "RM-02", "Living furniture order", "Sofa + table. 6-week lead.", "Sofia Alvarez", "Interior Designer", "To Do", "High", date(2026, 9, 1), date(2026, 9, 1), 3400, "", 0, "Order by Sep 1"],
    ["TSK-023", "PRJ-001", "RM-06", "Exterior path layout", "Stake path, confirm stone.", "Theo Brooks", "Contractor", "To Do", "Low", date(2026, 10, 6), date(2026, 10, 8), 0, "", 0, "Hold extras"],
    ["TSK-024", "PRJ-001", "", "Final city inspection", "Building final.", "Riley Grant", "Inspector", "To Do", "Critical", date(2026, 10, 25), date(2026, 11, 5), 175, "TSK-018", 0, ""],
    ["TSK-025", "PRJ-001", "", "Homeowner walkthrough", "Punch list + handover packet.", "Marcus Webb", "Project Manager", "To Do", "High", date(2026, 11, 10), date(2026, 11, 15), 0, "TSK-024", 0, ""],
    ["TSK-026", "PRJ-001", "RM-01", "Approve island slab", "Confirm porcelain vs leftover quartz.", "Alex Rivera", "Homeowner", "In Progress", "High", date(2026, 8, 22), date(2026, 8, 25), 0, "AI-001", 0.5, "Pending approval"],
    ["TSK-027", "PRJ-001", "", "Weekly site meeting", "GC + designer + homeowner.", "Marcus Webb", "Project Manager", "Scheduled", "Medium", date(2026, 8, 25), date(2026, 8, 25), 0, "", 0, "Tue 9:00"],
    ["TSK-028", "PRJ-002", "RM-09", "Cabin bath concept", "Japandi mood board lock.", "Sofia Alvarez", "Interior Designer", "In Progress", "Low", date(2026, 8, 1), date(2026, 9, 15), 600, "", 0.4, ""],
    ["TSK-029", "PRJ-001", "RM-01", "Backsplash layout", "Zellige sample on site.", "Sofia Alvarez", "Interior Designer", "Scheduled", "Medium", date(2026, 9, 8), date(2026, 9, 9), 0, "TSK-016", 0, ""],
    ["TSK-030", "PRJ-001", "", "Update insurance inventory", "Photograph new fixtures.", "Alex Rivera", "Homeowner", "To Do", "Medium", date(2026, 11, 12), date(2026, 11, 14), 0, "TSK-025", 0, ""],
]

# ---------------------------------------------------------------------------
# Timeline phases (Gantt)
# ---------------------------------------------------------------------------
TIMELINE = [
    ["PH-01", "PRJ-001", "Planning", date(2026, 3, 1), date(2026, 3, 31), "Completed", ""],
    ["PH-02", "PRJ-001", "Design", date(2026, 3, 15), date(2026, 5, 15), "Completed", "PH-01"],
    ["PH-03", "PRJ-001", "Permits", date(2026, 4, 1), date(2026, 5, 20), "Completed", "PH-01"],
    ["PH-04", "PRJ-001", "Demolition", date(2026, 5, 21), date(2026, 6, 5), "Completed", "PH-03"],
    ["PH-05", "PRJ-001", "Electrical", date(2026, 6, 1), date(2026, 7, 10), "Completed", "PH-04"],
    ["PH-06", "PRJ-001", "Plumbing", date(2026, 6, 8), date(2026, 7, 20), "Completed", "PH-04"],
    ["PH-07", "PRJ-001", "Walls / plaster", date(2026, 7, 15), date(2026, 8, 10), "Completed", "PH-05"],
    ["PH-08", "PRJ-001", "Flooring", date(2026, 8, 5), date(2026, 8, 28), "In Progress", "PH-07"],
    ["PH-09", "PRJ-001", "Cabinetry", date(2026, 8, 20), date(2026, 9, 15), "In Progress", "PH-08"],
    ["PH-10", "PRJ-001", "Counters / appliances", date(2026, 9, 10), date(2026, 9, 18), "Scheduled", "PH-09"],
    ["PH-11", "PRJ-001", "Painting", date(2026, 9, 10), date(2026, 9, 28), "Scheduled", "PH-07"],
    ["PH-12", "PRJ-001", "Furniture", date(2026, 9, 25), date(2026, 10, 20), "To Do", "PH-11"],
    ["PH-13", "PRJ-001", "Exterior / garden", date(2026, 10, 6), date(2026, 10, 24), "To Do", "PH-11"],
    ["PH-14", "PRJ-001", "Final inspection", date(2026, 10, 25), date(2026, 11, 5), "To Do", "PH-12"],
    ["PH-15", "PRJ-001", "Handover", date(2026, 11, 10), date(2026, 11, 15), "To Do", "PH-14"],
    ["PH-16", "PRJ-002", "Cabin design", date(2026, 8, 1), date(2026, 9, 30), "In Progress", ""],
    ["PH-17", "PRJ-002", "Cabin construction", date(2026, 10, 15), date(2026, 12, 10), "To Do", "PH-16"],
]

# ---------------------------------------------------------------------------
# Materials
# ---------------------------------------------------------------------------
MATERIALS = [
    ["MAT-001", "PRJ-001", "RM-01", "Shaker cabinet box set", "Cascade", "CC-SH-Sage", "Cabinetry", 1, "set", 14800, "Cascade Cabinets", 1, 1, 0.6, "Delivered", 60, "INV-CC-501", date(2026, 6, 1), date(2026, 8, 20), "QR-CC-001"],
    ["MAT-002", "PRJ-001", "RM-01", "Aged brass bar pulls", "Rejuvenation", "RJ-BP-128", "Hardware", 28, "ea", 18, "Rejuvenation", 28, 0, 0, "Shipped", 12, "", date(2026, 8, 10), None, "QR-RJ-128"],
    ["MAT-003", "PRJ-001", "RM-01", "White oak 7in engineered", "Timberline", "TL-WO-7", "Flooring", 780, "sf", 8.2, "Timberline Floors", 780, 780, 620, "Installed", 25, "PO-140", date(2026, 7, 1), date(2026, 7, 28), "QR-TL-WO7"],
    ["MAT-004", "PRJ-001", "RM-01", "Perimeter quartz — Frost", "Caesarstone", "CS-5110", "Counters", 42, "sf", 59, "Caesarstone", 42, 42, 0, "Delivered", 15, "CS-882", date(2026, 8, 1), date(2026, 8, 16), "QR-CS-5110"],
    ["MAT-005", "PRJ-001", "RM-01", "Island porcelain slab", "Heritage", "HT-8841", "Counters", 28, "sf", 66.4, "Heritage Tile & Stone", 0, 0, 0, "Approved", 25, "", None, None, "QR-HT-8841"],
    ["MAT-006", "PRJ-001", "RM-01", "Zellige backsplash — sand", "Cle", "CLE-Z-14", "Tile", 48, "sf", 28, "Tile & Timber Co.", 0, 0, 0, "Quoted", 0, "", None, None, "QR-CLE-14"],
    ["MAT-007", "PRJ-001", "RM-01", "Island pendants x3", "BrightPath", "BP-ISL-AB", "Lighting", 3, "ea", 296.67, "BrightPath Lighting", 3, 0, 0, "Ordered", 24, "BP-220", date(2026, 8, 18), None, "QR-BP-ISL"],
    ["MAT-008", "PRJ-001", "RM-01", "Range 36in dual fuel", "Wolf", "DF364C", "Appliances", 1, "ea", 0, "Sub-Zero / Wolf", 1, 0, 0, "Ordered", 24, "APPL-01", date(2026, 8, 14), None, "QR-WF-DF"],
    ["MAT-009", "PRJ-001", "RM-01", "Counter-depth fridge", "Sub-Zero", "DEC3650", "Appliances", 1, "ea", 0, "Sub-Zero / Wolf", 1, 0, 0, "Ordered", 24, "APPL-01", date(2026, 8, 14), None, "QR-SZ-3650"],
    ["MAT-010", "PRJ-001", "RM-03", "Porcelain floor 12x24", "Heritage", "HT-8841F", "Tile", 90, "sf", 14.2, "Tile & Timber Co.", 95, 95, 90, "Installed", 25, "PO-114", date(2026, 6, 10), date(2026, 6, 20), "QR-HT-F"],
    ["MAT-011", "PRJ-001", "RM-03", "Shower wall porcelain", "Heritage", "HT-8841W", "Tile", 110, "sf", 16.8, "Tile & Timber Co.", 115, 115, 110, "Installed", 25, "PO-114", date(2026, 6, 10), date(2026, 6, 20), "QR-HT-W"],
    ["MAT-012", "PRJ-001", "RM-03", "Thermostatic shower set", "Brizo", "BZ-T600", "Fixtures", 1, "set", 890, "Ferguson", 1, 1, 1, "Installed", 60, "FERG-9921", date(2026, 6, 15), date(2026, 6, 28), "QR-BZ-T600"],
    ["MAT-013", "PRJ-001", "RM-03", "Vanity 48in white oak", "Cascade", "CC-VAN-48", "Cabinetry", 1, "ea", 1680, "Cascade Cabinets", 1, 1, 1, "Installed", 24, "INV-CC-440", date(2026, 7, 1), date(2026, 7, 20), "QR-CC-VAN"],
    ["MAT-014", "PRJ-001", "RM-03", "Heated floor kit", "WarmFloor", "WF-240-40", "Electrical", 1, "kit", 1680, "WarmFloor Co.", 1, 1, 1, "Installed", 36, "WF-441", date(2026, 6, 20), date(2026, 7, 2), "QR-WF-240"],
    ["MAT-015", "PRJ-001", "RM-02", "Modular sofa", "Article", "ART-SVEN", "Furniture", 1, "ea", 2400, "Article", 0, 0, 0, "Quoted", 12, "", None, None, "QR-ART-SV"],
    ["MAT-016", "PRJ-001", "RM-02", "Oak coffee table", "Article", "ART-OAK-CT", "Furniture", 1, "ea", 1000, "Article", 0, 0, 0, "Quoted", 12, "", None, None, "QR-ART-CT"],
    ["MAT-017", "PRJ-001", "RM-05", "Dining sconces", "BrightPath", "BP-SCN-02", "Lighting", 2, "ea", 190, "BrightPath Lighting", 2, 2, 0, "Delivered", 24, "BP-204", date(2026, 8, 1), date(2026, 8, 22), "QR-BP-SCN"],
    ["MAT-018", "PRJ-001", "RM-08", "Hook rail 48in", "Rejuvenation", "RJ-HR-48", "Hardware", 1, "ea", 186, "Rejuvenation", 1, 1, 0, "Delivered", 12, "REJ-33", date(2026, 8, 12), date(2026, 8, 19), "QR-RJ-HR"],
    ["MAT-019", "PRJ-001", "RM-04", "Interior paint — Clay", "Benjamin Moore", "BM-HC-50", "Paint", 4, "gal", 62, "Sherwin-Williams", 0, 0, 0, "Required", 0, "", None, None, "QR-BM-CLAY"],
    ["MAT-020", "PRJ-001", "RM-06", "Bluestone path pavers", "Garden & Gate", "GG-BLU-12", "Hardscape", 220, "sf", 9.5, "Garden & Gate", 0, 0, 0, "Quoted", 0, "", None, None, "QR-GG-BLU"],
    ["MAT-021", "PRJ-001", "RM-01", "Undermount sink", "Kohler", "K-5285", "Fixtures", 1, "ea", 420, "Ferguson", 1, 1, 0, "Delivered", 36, "FERG-1002", date(2026, 8, 1), date(2026, 8, 12), "QR-K-5285"],
    ["MAT-022", "PRJ-001", "RM-01", "Bridge faucet — brass", "Brizo", "BZ-K610", "Fixtures", 1, "ea", 640, "Ferguson", 1, 0, 0, "Shipped", 60, "FERG-1002", date(2026, 8, 8), None, "QR-BZ-K610"],
    ["MAT-023", "PRJ-001", "RM-02", "Stair nosing — white oak", "Timberline", "TL-NOS-WO", "Flooring", 14, "lf", 22, "Timberline Floors", 14, 0, 0, "Backordered", 25, "", date(2026, 8, 6), None, "QR-TL-NOS"],
    ["MAT-024", "PRJ-002", "RM-09", "Cedar vanity", "Cascade", "CC-CED-36", "Cabinetry", 1, "ea", 2100, "Cascade Cabinets", 0, 0, 0, "Required", 24, "", None, None, "QR-CC-CED"],
    ["MAT-025", "PRJ-001", "RM-04", "Wardrobe kit", "IKEA / custom face", "PAX-WO", "Cabinetry", 1, "set", 890, "IKEA", 0, 0, 0, "Required", 12, "", None, None, "QR-PAX"],
]

# ---------------------------------------------------------------------------
# Suppliers
# ---------------------------------------------------------------------------
SUPPLIERS = [
    ["SUP-001", "Tile & Timber Co.", "Tile / flooring", "Harper Quinn", "+1-503-555-0160", "orders@tileandtimber.example", "tileandtimber.example", 4.7, "Net 15", 7, "Preferred tile house"],
    ["SUP-002", "Ferguson", "Plumbing fixtures", "Counter desk", "+1-503-555-2000", "pdx@ferguson.example", "ferguson.com", 4.5, "Net 30", 10, "Will-call available"],
    ["SUP-003", "Caesarstone", "Counters", "West desk", "+1-800-555-0199", "west@caesarstone.example", "caesarstoneus.com", 4.6, "Prepaid", 14, "Frost 5110 in stock"],
    ["SUP-004", "Sub-Zero / Wolf dealer", "Appliances", "Aiden Brooks", "+1-503-555-2111", "aiden@swdealer.example", "subzero-wolf.com", 4.8, "50% deposit", 28, "Delivery window Sep 12"],
    ["SUP-005", "Rejuvenation", "Hardware / lighting", "Online + Pearl", "+1-888-401-1900", "hello@rejuvenation.example", "rejuvenation.com", 4.6, "Card", 12, "Hardware in transit"],
    ["SUP-006", "Sherwin-Williams", "Paint", "Hawthorne store", "+1-503-555-2220", "store@sw.example", "sherwin-williams.com", 4.4, "Card", 1, "Color match BM"],
    ["SUP-007", "Article", "Furniture", "Wholesale desk", "+1-888-746-3455", "trade@article.example", "article.com", 4.3, "Prepaid", 42, "Order by Sep 1"],
    ["SUP-008", "WarmFloor Co.", "Radiant", "Support", "+1-800-555-0182", "support@warmfloor.example", "warmfloor.example", 4.5, "Card", 5, "10yr warranty"],
    ["SUP-009", "BrightPath Lighting", "Lighting", "Nina Cho", "+1-503-555-0180", "nina@brightpath.example", "brightpath.example", 4.6, "Net 15", 21, "Also a contractor"],
    ["SUP-010", "Garden & Gate Yard", "Hardscape", "Theo Brooks", "+1-503-555-0199", "yard@gardengate.example", "gardengate.example", 4.4, "50% deposit", 14, "Bluestone seasonal"],
]

# ---------------------------------------------------------------------------
# Documents
# ---------------------------------------------------------------------------
DOCUMENTS = [
    ["DOC-001", "PRJ-001", "", "Contract", "Ironwood GC agreement", "1.2", "drive/docs/iw-contract.pdf", date(2026, 3, 4), None, "Yes", "Alex Rivera", "Signed via DocuSign"],
    ["DOC-002", "PRJ-001", "", "Contract", "Luna Interiors design services", "1.0", "drive/docs/luna-contract.pdf", date(2026, 3, 6), None, "Yes", "Alex Rivera", ""],
    ["DOC-003", "PRJ-001", "RM-01", "Contract", "Cascade Cabinets millwork", "1.1", "drive/docs/cascade-contract.pdf", date(2026, 5, 28), None, "Yes", "Alex Rivera", "Includes install"],
    ["DOC-004", "PRJ-001", "", "Building Permit", "Residential remodel permit", "1.0", "drive/docs/permit-441.pdf", date(2026, 4, 12), date(2027, 4, 12), "Yes", "Marcus Webb", "Expires 12 months"],
    ["DOC-005", "PRJ-001", "", "License", "Ironwood CCB + insurance cert", "2026", "drive/docs/iw-insurance.pdf", date(2026, 3, 4), date(2027, 4, 30), "No", "Marcus Webb", "Remind 30 days prior"],
    ["DOC-006", "PRJ-001", "RM-01", "Floor Plan", "Kitchen layout v4", "4.0", "drive/plans/kitchen-v4.pdf", date(2026, 5, 10), None, "Yes", "Sofia Alvarez", "Supersedes v3"],
    ["DOC-007", "PRJ-001", "RM-03", "Floor Plan", "Primary bath plan", "2.0", "drive/plans/bath-v2.pdf", date(2026, 5, 12), None, "Yes", "Sofia Alvarez", ""],
    ["DOC-008", "PRJ-001", "", "Inspection Report", "Plumbing rough inspection", "1.0", "drive/insp/plumb-rough.pdf", date(2026, 6, 30), None, "No", "Riley Grant", "Pass"],
    ["DOC-009", "PRJ-001", "", "Inspection Report", "Electrical rough inspection", "1.0", "drive/insp/elec-rough.pdf", date(2026, 7, 2), None, "No", "Riley Grant", "Pass"],
    ["DOC-010", "PRJ-001", "RM-03", "Warranty", "Heritage tile labor + material", "1.0", "drive/warr/heritage.pdf", date(2026, 8, 12), date(2028, 8, 12), "No", "Priya Shah", "2 year labor"],
    ["DOC-011", "PRJ-001", "RM-03", "Product Manual", "WarmFloor thermostat", "1.0", "drive/manuals/wf.pdf", date(2026, 7, 6), None, "No", "Sam Ortiz", ""],
    ["DOC-012", "PRJ-001", "RM-01", "Invoice", "Cascade deposit INV-CC-501", "1.0", "drive/inv/cc-501.pdf", date(2026, 8, 2), None, "No", "Jamie Cole", "Paid"],
    ["DOC-013", "PRJ-001", "RM-01", "Photo", "Kitchen before set", "1.0", "drive/photos/kitchen-before", date(2026, 3, 12), None, "No", "Alex Rivera", "20 images"],
    ["DOC-014", "PRJ-001", "", "Insurance", "Homeowner policy declarations", "2026", "drive/docs/ho-policy.pdf", date(2026, 1, 5), date(2027, 1, 5), "No", "Alex Rivera", "Notify carrier of remodel"],
    ["DOC-015", "PRJ-001", "", "Change Order", "CO-002 island porcelain", "1.0", "drive/co/co-002.pdf", date(2026, 8, 21), None, "No", "Alex Rivera", "Awaiting signature"],
    ["DOC-016", "PRJ-002", "RM-09", "Photo", "Cabin bath before", "1.0", "drive/photos/cabin-before", date(2026, 7, 30), None, "No", "Alex Rivera", ""],
]

# ---------------------------------------------------------------------------
# Messages
# ---------------------------------------------------------------------------
MESSAGES = [
    ["MSG-001", datetime(2026, 8, 20, 9, 12), "PRJ-001", "RM-01 / TSK-013", "Maya Chen", "Alex Rivera", "App", "Boxes land tomorrow 7:30. Please keep driveway clear.", "", "@Alex", "Yes"],
    ["MSG-002", datetime(2026, 8, 20, 9, 40), "PRJ-001", "RM-01 / TSK-013", "Alex Rivera", "Maya Chen", "App", "Confirmed. I'll move the car tonight.", "", "@Maya", "Yes"],
    ["MSG-003", datetime(2026, 8, 21, 14, 5), "PRJ-001", "RM-01", "Sofia Alvarez", "Project group", "Group Chat", "AI recommends porcelain on the island only. Mood board updated.", "drive/mood/kitchen-01", "@Alex @Marcus", "Yes"],
    ["MSG-004", datetime(2026, 8, 21, 16, 22), "PRJ-001", "RM-01", "Alex Rivera", "Sofia Alvarez", "App", "Approved — keep quartz on the run, porcelain on the island.", "", "@Sofia", "Yes"],
    ["MSG-005", datetime(2026, 8, 22, 8, 1), "PRJ-001", "MAT-002", "Maya Chen", "Marcus Webb", "SMS", "Pulls still in transit. ETA Friday. Plan hardware day next week.", "", "@Marcus", "Yes"],
    ["MSG-006", datetime(2026, 8, 22, 11, 18), "PRJ-001", "RM-03 / TSK-010", "Priya Shah", "Alex Rivera", "Photo Comment", "Haze on the niche shelf — will reclean Thursday.", "drive/photos/bath-niche", "@Alex", "Yes"],
    ["MSG-007", datetime(2026, 8, 23, 17, 44), "PRJ-001", "JOB-006", "Elena Voss", "Project group", "Group Chat", "Finish coat Tuesday. No traffic 48 hours.", "", "@all", "Yes"],
    ["MSG-008", datetime(2026, 8, 24, 7, 55), "PRJ-001", "TSK-027", "Marcus Webb", "Project group", "App", "Weekly meeting tomorrow 9:00 on site. Agenda in documents.", "drive/docs/agenda-0825.pdf", "@Alex @Sofia @Maya", "No"],
    ["MSG-009", datetime(2026, 8, 24, 8, 10), "PRJ-001", "AI-005", "Morgan Ellis", "Alex Rivera", "Email", "Contingency dropped below 10%. Recommend pausing water feature.", "", "@Alex @Jamie", "No"],
    ["MSG-010", datetime(2026, 8, 12, 15, 2), "PRJ-001", "DOC-009", "Riley Grant", "Marcus Webb", "App", "Electrical rough passed. Final after device install.", "drive/insp/elec-rough.pdf", "@Marcus", "Yes"],
    ["MSG-011", datetime(2026, 8, 18, 19, 30), "PRJ-002", "RM-09", "Sofia Alvarez", "Alex Rivera", "App", "Cabin Japandi board is in Design Studio. Two fixture directions.", "drive/mood/cabin", "@Alex", "Yes"],
    ["MSG-012", datetime(2026, 8, 19, 10, 5), "PRJ-001", "SUP-004", "Harper Quinn", "Sofia Alvarez", "Email", "Wolf range crate confirmed for Sep 12 window.", "", "@Sofia", "Yes"],
]

# ---------------------------------------------------------------------------
# Inventory
# ---------------------------------------------------------------------------
INVENTORY = [
    ["INV-001", "Samsung Refrigerator (existing, to donate)", "Samsung", "RM-01", "Appliance", date(2019, 4, 1), 1200, 1, "RF28R7351SG", "RF28", "drive/rcpt/old-fridge", "Fair", 400, "Pickup scheduled after new fridge arrives"],
    ["INV-002", "Sub-Zero fridge (on order)", "Sub-Zero", "RM-01", "Appliance", date(2026, 9, 12), 0, 2, "TBD", "DEC3650", "APPL-01", "On order", 8900, "Serial on delivery"],
    ["INV-003", "Wolf 36 dual-fuel range (on order)", "Wolf", "RM-01", "Appliance", date(2026, 9, 12), 0, 2, "TBD", "DF364C", "APPL-01", "On order", 7900, ""],
    ["INV-004", "Bosch dishwasher", "Bosch", "RM-01", "Appliance", date(2023, 6, 1), 980, 1, "FD-2291", "SHPM88Z75N", "drive/rcpt/dw", "Good", 900, "Reuse"],
    ["INV-005", "WarmFloor thermostat", "WarmFloor", "RM-03", "System", date(2026, 7, 6), 1680, 3, "WF-T-44190", "WF-STAT-2", "WF-441", "New", 1680, "Program 82F mornings"],
    ["INV-006", "Brizo shower set", "Brizo", "RM-03", "Fixture", date(2026, 8, 14), 890, 5, "BZ-100221", "BZ-T600", "FERG-9921", "New", 890, ""],
    ["INV-007", "Primary bath vanity", "Cascade", "RM-03", "Cabinetry", date(2026, 7, 20), 1680, 2, "CC-VAN-48-09", "CC-VAN-48", "INV-CC-440", "New", 1680, ""],
    ["INV-008", "HVAC furnace", "Trane", "Laundry / mech", "HVAC", date(2021, 9, 1), 4200, 1, "TR-88120", "S9V2", "drive/rcpt/hvac", "Good", 3800, "Filter every 90 days"],
    ["INV-009", "Water heater (heat pump)", "Rheem", "Laundry / mech", "Plumbing", date(2024, 2, 10), 2100, 2, "RH-44019", "PROPH80", "drive/rcpt/wh", "Good", 2000, "Anode 2027"],
    ["INV-010", "Roof — architectural shingle", "Owens Corning", "Exterior", "Envelope", date(2018, 7, 1), 9800, 2, "", "Duration", "drive/rcpt/roof", "Fair", 12000, "Inspect after storms"],
    ["INV-011", "Washer / dryer pair", "LG", "RM-07", "Appliance", date(2022, 11, 1), 1600, 1, "LG-W8821 / LG-D8821", "WM4000 / DLEX4000", "drive/rcpt/ld", "Good", 1400, ""],
    ["INV-012", "Living room rug (existing)", "West Elm", "RM-02", "Furniture", date(2020, 1, 15), 640, 0, "", "Kelim 9x12", "", "Keep", 400, "Clean after flooring"],
    ["INV-013", "Entry hook rail", "Rejuvenation", "RM-08", "Hardware", date(2026, 8, 19), 186, 1, "", "RJ-HR-48", "REJ-33", "New", 186, "Install this week"],
    ["INV-014", "Smoke / CO detectors x6", "First Alert", "Whole home", "Safety", date(2025, 1, 8), 180, 10, "", "SMCO410", "", "Good", 180, "Hush test monthly"],
    ["INV-015", "Cabin water filter", "Berkey", "PROP-002", "Plumbing", date(2023, 5, 1), 320, 2, "", "Royal", "", "Good", 280, "Replace elements 2026-11"],
]

# ---------------------------------------------------------------------------
# Maintenance
# ---------------------------------------------------------------------------
MAINTENANCE = [
    ["MNT-001", "HVAC furnace service", "Laundry / mech", "HVAC", "Annual", date(2025, 10, 12), date(2026, 10, 12), "Allied Heating", 180, "Upcoming", 14, "Replace filter at service"],
    ["MNT-002", "Heat-pump water heater flush", "Laundry / mech", "Plumbing", "Annual", date(2025, 2, 10), date(2026, 9, 10), "Pacific Plumbing", 140, "Due Soon", 14, "Check anode"],
    ["MNT-003", "Gutter clean + roof walk", "Exterior", "Envelope", "Biannual", date(2026, 4, 2), date(2026, 10, 15), "Ironwood / roofer", 220, "Upcoming", 14, "After leaf drop"],
    ["MNT-004", "Paint touch-up interior", "Whole home", "Finishes", "As needed", None, date(2026, 11, 20), "Greenfield Painting", 0, "Upcoming", 7, "Leave labeled quarts"],
    ["MNT-005", "Pest control", "Exterior", "Pest", "Quarterly", date(2026, 6, 1), date(2026, 9, 1), "Oregon Pest", 95, "Due Soon", 7, ""],
    ["MNT-006", "Radiant floor test", "RM-03", "Electrical", "Annual", date(2026, 7, 6), date(2027, 7, 6), "WarmFloor / NWE", 0, "Upcoming", 30, "First winter check"],
    ["MNT-007", "Appliance warranty photo set", "RM-01", "Appliance", "Once", None, date(2026, 9, 20), "Alex Rivera", 0, "Upcoming", 3, "After delivery"],
    ["MNT-008", "Smoke / CO test", "Whole home", "Safety", "Monthly", date(2026, 8, 1), date(2026, 9, 1), "Alex Rivera", 0, "Upcoming", 3, ""],
    ["MNT-009", "Cabin water filter elements", "PROP-002", "Plumbing", "Annual", date(2025, 11, 1), date(2026, 11, 1), "Alex Rivera", 60, "Upcoming", 14, ""],
    ["MNT-010", "Window weatherstrip", "Whole home", "Envelope", "Annual", date(2025, 11, 15), date(2026, 11, 10), "Ironwood", 160, "Upcoming", 14, "Before handover winter"],
    ["MNT-011", "Irrigation blowout", "RM-06", "Landscape", "Annual", date(2025, 10, 20), date(2026, 10, 20), "Garden & Gate", 120, "Upcoming", 14, "After path work"],
    ["MNT-012", "Grout seal — primary bath", "RM-03", "Tile", "Annual", date(2026, 8, 12), date(2027, 8, 12), "Heritage Tile", 0, "Complete", 30, "Sealed at install"],
]

# ---------------------------------------------------------------------------
# Inspections
# ---------------------------------------------------------------------------
INSPECTIONS = [
    ["INS-001", "PRJ-001", "", "Building permit review", "Riley Grant", date(2026, 4, 12), "Pass", "None", "", "Complete", "drive/insp/permit.pdf"],
    ["INS-002", "PRJ-001", "RM-01", "Electrical rough", "Riley Grant", date(2026, 7, 2), "Pass", "Add AFCI in pantry — done same day", "", "Complete", "drive/insp/elec-rough.pdf"],
    ["INS-003", "PRJ-001", "RM-03", "Plumbing rough", "Riley Grant", date(2026, 6, 30), "Pass", "None", "", "Complete", "drive/insp/plumb-rough.pdf"],
    ["INS-004", "PRJ-001", "RM-03", "Waterproofing / shower pan", "Marcus Webb", date(2026, 7, 10), "Pass", "None", "", "Complete", "drive/insp/pan.pdf"],
    ["INS-005", "PRJ-001", "RM-03", "Primary bath punch", "Priya Shah", date(2026, 8, 26), "Scheduled", "Haze on niche", "Reclean + photo", "Scheduled", ""],
    ["INS-006", "PRJ-001", "", "Electrical final", "Riley Grant", date(2026, 10, 28), "Scheduled", "", "After devices", "Scheduled", ""],
    ["INS-007", "PRJ-001", "", "Plumbing final", "Riley Grant", date(2026, 10, 28), "Scheduled", "", "", "Scheduled", ""],
    ["INS-008", "PRJ-001", "", "Building final", "Riley Grant", date(2026, 11, 4), "Scheduled", "", "After electrical/plumbing finals", "Scheduled", ""],
    ["INS-009", "PRJ-001", "", "Independent punch", "Alder Inspection Group", date(2026, 11, 8), "Scheduled", "", "Pre-handover", "Scheduled", ""],
]

# ---------------------------------------------------------------------------
# Payments
# ---------------------------------------------------------------------------
PAYMENTS = [
    ["PAY-001", date(2026, 3, 8), "Designer", "Luna Interiors", "PRJ-001", "INV-LUNA-110", 2400, "ACH", "Paid", date(2026, 3, 15), date(2026, 3, 8)],
    ["PAY-002", date(2026, 4, 2), "Authority", "City of Portland", "PRJ-001", "PMT-2026-441", 840, "Credit Card", "Paid", date(2026, 4, 2), date(2026, 4, 2)],
    ["PAY-003", date(2026, 5, 4), "Designer", "Luna Interiors", "PRJ-001", "INV-LUNA-126", 1800, "ACH", "Paid", date(2026, 5, 18), date(2026, 5, 4)],
    ["PAY-004", date(2026, 5, 22), "Contractor", "Ironwood Construction", "PRJ-001", "INV-IW-204", 2800, "Check", "Paid", date(2026, 6, 5), date(2026, 5, 22)],
    ["PAY-005", date(2026, 8, 2), "Contractor", "Cascade Cabinets", "PRJ-001", "INV-CC-501", 7400, "Wire", "Paid", date(2026, 8, 9), date(2026, 8, 2)],
    ["PAY-006", date(2026, 8, 25), "Contractor", "Cascade Cabinets", "PRJ-001", "INV-CC-502", 7400, "Wire", "Scheduled", date(2026, 9, 8), None],
    ["PAY-007", date(2026, 8, 28), "Contractor", "Cascade Cabinets", "PRJ-001", "INV-CC-510", 3600, "ACH", "Scheduled", date(2026, 9, 11), None],
    ["PAY-008", date(2026, 8, 18), "Contractor", "Ironwood Construction", "PRJ-001", "INV-IW-228", 1550, "ACH", "Paid", date(2026, 9, 1), date(2026, 8, 18)],
    ["PAY-009", date(2026, 8, 8), "Contractor", "Heritage Tile & Stone", "PRJ-001", "INV-HT-81", 2100, "ACH", "Paid", date(2026, 8, 22), date(2026, 8, 8)],
    ["PAY-010", date(2026, 8, 1), "Designer", "Luna Interiors", "PRJ-002", "INV-LUNA-140", 600, "ACH", "Paid", date(2026, 8, 15), date(2026, 8, 1)],
    ["PAY-011", date(2026, 9, 12), "Supplier", "Article", "PRJ-001", "ART-SOFA", 3400, "Credit Card", "Draft", date(2026, 9, 12), None],
]

# ---------------------------------------------------------------------------
# Change orders
# ---------------------------------------------------------------------------
CHANGE_ORDERS = [
    ["CO-001", "PRJ-001", "RM-03", "Swap marble floor for porcelain HT-8841", "Sofia Alvarez / AI", date(2026, 5, 18), -1640, 0, "Implemented", "Alex Rivera"],
    ["CO-002", "PRJ-001", "RM-01", "Island surface: porcelain slab instead of marble", "Sofia Alvarez / AI", date(2026, 8, 21), -460, 2, "Submitted", ""],
    ["CO-003", "PRJ-001", "RM-01", "Add pot-filler at range", "Alex Rivera", date(2026, 6, 10), 480, 1, "Approved", "Alex Rivera"],
    ["CO-004", "PRJ-001", "RM-02", "Site-cut oak nosing in lieu of factory (backorder)", "Elena Voss", date(2026, 8, 21), 0, 0, "Approved", "Marcus Webb"],
    ["CO-005", "PRJ-001", "RM-06", "Hold water feature until contingency recovers", "Morgan Ellis / AI", date(2026, 8, 24), -1800, 0, "Draft", ""],
]

# ---------------------------------------------------------------------------
# Permits
# ---------------------------------------------------------------------------
PERMITS = [
    ["PMT-001", "PRJ-001", "Building — residential remodel", "City of Portland", date(2026, 4, 2), date(2026, 4, 12), "2026-REM-44182", 840, date(2027, 4, 12), "Approved", "drive/docs/permit-441.pdf"],
    ["PMT-002", "PRJ-001", "Electrical", "City of Portland", date(2026, 4, 18), date(2026, 4, 22), "2026-EL-11904", 310, date(2027, 4, 22), "Approved", "drive/docs/permit-el.pdf"],
    ["PMT-003", "PRJ-001", "Plumbing", "City of Portland", date(2026, 4, 18), date(2026, 4, 22), "2026-PL-7731", 300, date(2027, 4, 22), "Approved", "drive/docs/permit-pl.pdf"],
    ["PMT-004", "PRJ-001", "Right-of-way dumpster", "PBOT", date(2026, 5, 10), date(2026, 5, 14), "ROW-5521", 75, date(2026, 6, 14), "Closed", "drive/docs/row.pdf"],
    ["PMT-005", "PRJ-002", "Building — bath remodel", "Hood River County", None, None, "", 0, None, "Not Started", ""],
]

# ---------------------------------------------------------------------------
# Warranties
# ---------------------------------------------------------------------------
WARRANTIES = [
    ["WAR-001", "PRJ-001", "Heritage tile labor + material", "Heritage Tile & Stone", date(2026, 8, 12), date(2028, 8, 12), 24, "Labor + setting materials", "Photo + email Priya", "drive/warr/heritage.pdf"],
    ["WAR-002", "PRJ-001", "WarmFloor system", "WarmFloor Co.", date(2026, 7, 6), date(2029, 7, 6), 36, "Mat + thermostat", "Serial + install photos", "drive/warr/wf.pdf"],
    ["WAR-003", "PRJ-001", "White oak flooring finish", "Timberline Floors", date(2026, 8, 28), date(2027, 8, 28), 12, "Site finish wear", "No steam mops year 1", ""],
    ["WAR-004", "PRJ-001", "Cascade cabinetry", "Cascade Cabinets", date(2026, 9, 15), date(2028, 9, 15), 24, "Boxes, doors, finish", "Maya Chen", ""],
    ["WAR-005", "PRJ-001", "Wolf range (pending delivery)", "Sub-Zero Group", date(2026, 9, 12), date(2028, 9, 12), 24, "Parts + labor", "Register online 30 days", ""],
    ["WAR-006", "PRJ-001", "Sub-Zero fridge (pending)", "Sub-Zero Group", date(2026, 9, 12), date(2028, 9, 12), 24, "Sealed system 5yr", "Register online 30 days", ""],
    ["WAR-007", "PRJ-001", "Brizo fixtures", "Brizo / Ferguson", date(2026, 8, 14), date(2031, 8, 14), 60, "Finish + function", "Proof of purchase", "FERG-9921"],
]

# ---------------------------------------------------------------------------
# Notifications
# ---------------------------------------------------------------------------
NOTIFICATIONS = [
    ["NTF-001", date(2026, 8, 24), "Warning", "Budget", "Kitchen budget is 12% over original target. Island swap pending.", "Open", "HO-001"],
    ["NTF-002", date(2026, 8, 24), "Critical", "Finance", "Project contingency has fallen below 10%.", "Open", "HO-001"],
    ["NTF-003", date(2026, 8, 24), "Success", "Rooms", "Primary bathroom is under budget after porcelain swap.", "Open", "HO-001"],
    ["NTF-004", date(2026, 8, 23), "Warning", "Procurement", "White oak stair nosing backordered 11 days.", "Open", "PM-001"],
    ["NTF-005", date(2026, 8, 22), "Info", "Schedule", "Cabinet hardware still in transit — hardware day next week.", "Open", "CT-001"],
    ["NTF-006", date(2026, 8, 20), "Info", "Visit", "Cascade Cabinets on site Aug 25–27 for box set.", "Open", "HO-001"],
    ["NTF-007", date(2026, 8, 18), "Warning", "Approval", "CO-002 island porcelain awaiting signature.", "Open", "HO-001"],
    ["NTF-008", date(2026, 9, 1), "Info", "Maintenance", "Pest control due in 8 days.", "Scheduled", "HO-001"],
    ["NTF-009", date(2026, 8, 24), "Info", "Message", "Marcus posted tomorrow's site meeting agenda.", "Open", "HO-001"],
    ["NTF-010", date(2026, 8, 12), "Success", "Inspection", "Electrical rough passed.", "Read", "PM-001"],
]

# ---------------------------------------------------------------------------
# Audit log
# ---------------------------------------------------------------------------
AUDIT = [
    ["AUD-001", datetime(2026, 8, 24, 8, 10), "AD-001", "Morgan Ellis", "AI Insights", "AI-005", "Created contingency alert"],
    ["AUD-002", datetime(2026, 8, 21, 16, 22), "HO-001", "Alex Rivera", "Change Orders", "CO-002", "Approved design direction (pending formal sign)"],
    ["AUD-003", datetime(2026, 8, 21, 14, 5), "DS-001", "Sofia Alvarez", "Design Studio", "DSN-006", "Published porcelain material board"],
    ["AUD-004", datetime(2026, 8, 20, 7, 40), "CT-001", "Maya Chen", "Materials", "MAT-001", "Marked cabinets Delivered"],
    ["AUD-005", datetime(2026, 8, 18, 17, 2), "AC-001", "Jamie Cole", "Payments", "PAY-008", "Recorded Ironwood August draw"],
    ["AUD-006", datetime(2026, 8, 14, 11, 0), "PM-001", "Marcus Webb", "Inspections", "INS-002", "Attached electrical rough report"],
    ["AUD-007", datetime(2026, 8, 12, 15, 2), "IN-001", "Riley Grant", "Inspections", "INS-002", "Result = Pass"],
    ["AUD-008", datetime(2026, 8, 2, 9, 15), "HO-001", "Alex Rivera", "Payments", "PAY-005", "Wired Cascade deposit"],
    ["AUD-009", datetime(2026, 5, 18, 10, 0), "DS-001", "Sofia Alvarez", "Change Orders", "CO-001", "Implemented marble→porcelain"],
    ["AUD-010", datetime(2026, 3, 4, 16, 45), "HO-001", "Alex Rivera", "Documents", "DOC-001", "Signed GC agreement"],
]

# ---------------------------------------------------------------------------
# Calendar events
# ---------------------------------------------------------------------------
CALENDAR = [
    [date(2026, 8, 25), "09:00", "Site meeting", "PRJ-001", "Weekly GC / designer / homeowner", "Marcus Webb", "Scheduled"],
    [date(2026, 8, 25), "07:30", "Cabinet install", "PRJ-001", "Cascade — box set continues", "Maya Chen", "Scheduled"],
    [date(2026, 8, 26), "10:00", "Bath punch", "PRJ-001", "Heritage reclean + walk", "Priya Shah", "Scheduled"],
    [date(2026, 8, 27), "All day", "Hardware ETA", "PRJ-001", "Pulls expected — do not hang if late", "Maya Chen", "Watch"],
    [date(2026, 8, 28), "All day", "Floor finish cure", "PRJ-001", "No traffic 48 hours after Tuesday coat", "Elena Voss", "Scheduled"],
    [date(2026, 9, 1), "17:00", "Order sofa", "PRJ-001", "6-week lead — last day to hit Oct move-in", "Sofia Alvarez", "To Do"],
    [date(2026, 9, 1), "All day", "Pest control due", "PROP-001", "Oregon Pest quarterly", "Alex Rivera", "Due Soon"],
    [date(2026, 9, 4), "08:00", "Counter template", "PRJ-001", "After doors hung", "Heritage Tile", "Scheduled"],
    [date(2026, 9, 10), "07:00", "Painting starts", "PRJ-001", "Guest, dining, entry", "Leo Park", "Scheduled"],
    [date(2026, 9, 10), "All day", "Water heater flush due", "PROP-001", "Pacific Plumbing", "Sam Ortiz", "Due Soon"],
    [date(2026, 9, 12), "Window", "Appliance delivery", "PRJ-001", "Wolf + Sub-Zero", "Aiden Brooks", "Scheduled"],
    [date(2026, 10, 6), "07:00", "Exterior path start", "PRJ-001", "Release only if contingency healthy", "Theo Brooks", "Hold"],
    [date(2026, 10, 12), "All day", "HVAC annual service", "PROP-001", "Allied Heating", "Alex Rivera", "Upcoming"],
    [date(2026, 11, 4), "09:00", "Building final", "PRJ-001", "City of Portland", "Riley Grant", "Scheduled"],
    [date(2026, 11, 10), "10:00", "Handover walkthrough", "PRJ-001", "Punch + vault packet", "Marcus Webb", "To Do"],
]

# ---------------------------------------------------------------------------
# Header definitions (used by generator)
# ---------------------------------------------------------------------------
HEADERS = {
    "Properties": [
        "Property ID", "Name", "Street", "City", "State", "Postal", "Country",
        "Type", "Year Built", "Sq Ft", "Stories", "Beds", "Baths", "Owner",
        "Owner User ID", "Insurance Policy", "Insurance Year", "Notes",
    ],
    "Users": [
        "User ID", "Name", "Email", "Phone", "Role", "Company", "Status",
        "Last Login", "Permissions",
    ],
    "Projects": [
        "Project ID", "Property ID", "Name", "Type", "Status", "Phase",
        "Start", "Target End", "Actual End", "Budget", "Homeowner ID",
        "PM ID", "Designer ID", "Homeowner Name", "Address", "Progress", "Notes",
    ],
    "Rooms": [
        "Room ID", "Project ID", "Room Name", "Type", "Floor", "Length (ft)",
        "Width (ft)", "Height (ft)", "Condition", "Status", "Budget",
        "Contractor ID", "Design Style", "Before Photos", "After Photos", "Notes",
    ],
    "Design Studio": [
        "Design ID", "Project ID", "Room ID", "Item Type", "Name", "Style",
        "Brand", "Color Hex", "Link / File", "Status", "Cost Est.", "AI Suggested", "Notes",
    ],
    "AI Insights": [
        "Insight ID", "Date", "Project ID", "Room ID", "Category", "Severity",
        "Insight", "Recommendation", "Est. Impact $", "Status", "Action Taken", "Open Flag",
    ],
    "Budget": [
        "Line ID", "Project ID", "Room ID", "Category", "Subcategory", "Planned",
        "Spent (Paid)", "Committed", "Remaining", "Variance", "Variance %", "Alert",
    ],
    "Expenses": [
        "Expense ID", "Date", "Project ID", "Room ID", "Category", "Vendor",
        "Description", "Amount", "Method", "Status", "Receipt / Invoice", "Approved By", "Dash Rank",
    ],
    "Contractors": [
        "Contractor ID", "Company", "Contact", "Trade", "Skills", "Phone", "Email",
        "Rating", "Quality", "On-Time", "Budget", "Communication", "Score",
        "Insurance Exp", "License", "Availability", "Rate ($/hr)", "Status", "Portfolio",
    ],
    "Quotes": [
        "Quote ID", "Project ID", "Room ID", "Contractor ID", "Trade", "Scope",
        "Amount", "Timeline (days)", "Valid Until", "Status", "Notes",
    ],
    "Jobs": [
        "Job ID", "Project ID", "Room ID", "Contractor ID", "Quote ID", "Scope",
        "Start", "End", "Milestone", "Status", "Amount", "Paid", "Balance", "% Paid",
    ],
    "Tasks": [
        "Task ID", "Project ID", "Room ID", "Title", "Description", "Assignee",
        "Role", "Status", "Priority", "Start", "Deadline", "Cost", "Depends On",
        "% Complete", "Attachments / Comments", "Days Left", "Health", "Dash Rank",
    ],
    "Timeline": [
        "Phase ID", "Project ID", "Phase", "Start", "End", "Duration (days)",
        "Status", "Depends On", "% Elapsed",
    ],
    "Materials": [
        "Material ID", "Project ID", "Room ID", "Product", "Brand", "SKU",
        "Category", "Qty Required", "Unit", "Unit Price", "Line Total", "Supplier",
        "Qty Ordered", "Qty Delivered", "Qty Installed", "Status", "Warranty (mo)",
        "Receipt", "Order Date", "Delivery Date", "QR / Barcode", "Open Qty", "Shop Rank",
    ],
    "Suppliers": [
        "Supplier ID", "Name", "Category", "Contact", "Phone", "Email", "Website",
        "Rating", "Payment Terms", "Lead Time (days)", "Notes",
    ],
    "Documents": [
        "Doc ID", "Project ID", "Room ID", "Category", "Title", "Version",
        "File Link", "Upload Date", "Expiration", "Signed", "Owner", "Notes",
        "Days to Expiry", "Expiry Alert",
    ],
    "Messages": [
        "Msg ID", "Date / Time", "Project ID", "Room / Task", "From", "To",
        "Channel", "Message", "Attachments", "Mentions", "Read",
    ],
    "Inventory": [
        "Item ID", "Item", "Brand", "Room / Location", "Category", "Purchase Date",
        "Cost", "Warranty (yrs)", "Warranty End", "Serial", "Model", "Receipt",
        "Condition", "Replacement Value", "Notes",
    ],
    "Maintenance": [
        "Maint ID", "Item / System", "Room / Location", "Type", "Frequency",
        "Last Service", "Next Due", "Vendor", "Est. Cost", "Status",
        "Remind (days)", "Notes", "Days Until Due", "Reminder",
    ],
    "Inspections": [
        "Insp ID", "Project ID", "Room ID", "Type", "Inspector", "Date",
        "Result", "Issues Found", "Follow-up", "Status", "Report Link",
    ],
    "Payments": [
        "Pay ID", "Date", "Payee Type", "Payee", "Project ID", "Invoice #",
        "Amount", "Method", "Status", "Due Date", "Paid Date", "Aging (days)",
    ],
    "Change Orders": [
        "CO ID", "Project ID", "Room ID", "Description", "Requested By", "Date",
        "Cost Impact", "Schedule Impact (days)", "Status", "Approved By",
    ],
    "Permits": [
        "Permit ID", "Project ID", "Type", "Authority", "Applied", "Approved",
        "Number", "Fee", "Expiration", "Status", "Document Link", "Days to Expiry",
    ],
    "Warranties": [
        "Warranty ID", "Project ID", "Item / Work", "Provider", "Start", "End",
        "Term (months)", "Coverage", "Claim Process", "Doc Link", "Days Remaining",
    ],
    "Notifications": [
        "ID", "Date", "Severity", "Module", "Message", "Status", "Audience",
    ],
    "Audit Log": [
        "Audit ID", "Timestamp", "User ID", "User Name", "Module", "Record ID", "Action",
    ],
    "Calendar": [
        "Date", "Time", "Event", "Project / Property", "Detail", "Owner", "Status",
    ],
}
