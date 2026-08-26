"""Sample data for the contractor ERP modules added from the Module Quick Links.

Keeps the Maplewood / Gorge sample story (as-of 24 Aug 2026).
"""

from __future__ import annotations

from datetime import date

TODAY = date(2026, 8, 24)

LOOKUPS_EXTRA = {
    "Client_Type": ["Homeowner", "Investor", "Commercial", "Repeat"],
    "Client_Status": ["Lead", "Active", "On Hold", "Complete", "Inactive"],
    "Comm_Type": ["Meeting", "Call", "Email", "Site Visit", "WhatsApp", "Letter"],
    "Sat_Channel": ["Survey", "Walkthrough", "Review", "Referral"],
    "PO_Status": ["Draft", "Sent", "Confirmed", "Partial", "Received", "Closed", "Cancelled"],
    "Stock_Status": ["In Stock", "Low", "Out", "On Order", "Reserved"],
    "Worker_Status": ["Active", "On Leave", "Terminated"],
    "Attendance_Status": ["Present", "Absent", "Half Day", "Overtime", "Holiday", "Sick"],
    "Skill_Level": ["Apprentice", "Journeyman", "Lead", "Supervisor"],
    "Equip_Status": ["Available", "In Use", "Maintenance", "Retired"],
    "Equip_Condition": ["Excellent", "Good", "Fair", "Poor"],
    "Defect_Severity": ["Critical", "Major", "Minor", "Cosmetic"],
    "Defect_Status": ["Open", "Assigned", "In Progress", "Fixed", "Verified", "Closed"],
    "Safety_Result": ["Pass", "Fail", "N/A", "Corrected"],
    "Incident_Type": ["Near Miss", "First Aid", "Medical", "Property Damage", "Environmental"],
    "Invoice_Status": ["Draft", "Sent", "Partial", "Paid", "Overdue", "Void"],
    "Income_Type": ["Client Payment", "Deposit", "Retention Release", "Other"],
    "Contract_Type": ["GC Agreement", "Design", "Subcontract", "Supply", "Change Order"],
    "Contract_Status": ["Draft", "Sent", "Signed", "Active", "Expired", "Closed"],
    "Service_Type": ["Warranty Claim", "Callback", "Maintenance", "Consultation"],
    "Service_Status": ["Open", "Scheduled", "In Progress", "Closed", "Escalated"],
    "Checklist_Status": ["Not Started", "In Progress", "Complete", "N/A"],
    "Quality_Result": ["Pass", "Fail", "Conditional"],
    "Phase_Status": ["To Do", "Scheduled", "In Progress", "Inspection", "Completed", "Blocked"],
    "Sel_Status": ["Considering", "Sampled", "Approved", "Rejected", "Installed"],
}

HEADERS_EXTRA = {
    "Project Phases": [
        "Phase ID", "Project ID", "Phase", "Start", "End", "Duration (days)",
        "Budget", "Spent", "Remaining", "% Complete", "Status", "Predecessor",
        "Owner", "Milestone", "Notes",
    ],
    "Client Master Data": [
        "Client ID", "Name", "Type", "Email", "Phone", "Street", "City",
        "Property ID", "Project ID", "Status", "Source", "Budget Range",
        "Assigned PM", "Last Contact", "Sat. Score", "Notes",
    ],
    "Client Communication": [
        "Comm ID", "Date", "Client ID", "Project ID", "Type", "Subject",
        "Summary", "Owner", "Follow-up", "Status", "Linked Task",
    ],
    "Client Satisfaction": [
        "Survey ID", "Date", "Client ID", "Project ID", "Phase", "Channel",
        "Overall", "Quality", "Communication", "Schedule", "Budget",
        "NPS", "Comment", "Status",
    ],
    "Contractor Performance": [
        "Contractor ID", "Company", "Trade", "Jobs", "Contract $", "Paid",
        "Balance", "Quality", "On-Time", "Score", "Open Snags", "Rating Band",
    ],
    "Material Estimation": [
        "Est ID", "Project ID", "Room ID", "Category", "Item", "Unit",
        "Qty", "Waste %", "Qty + Waste", "Unit Cost", "Labor Hrs",
        "Labor Rate", "Material $", "Labor $", "Total", "Notes",
    ],
    "Purchase Orders": [
        "PO ID", "Date", "Project ID", "Supplier", "Status", "Subtotal",
        "Tax", "Freight", "Total", "Paid", "Balance", "Expected", "Received", "Notes",
    ],
    "Material Inventory": [
        "Stock ID", "SKU", "Product", "Category", "Location", "On Hand",
        "Reserved", "Available", "Reorder Pt", "Unit Cost", "Stock Value",
        "Status", "Last Count", "Supplier",
    ],
    "Worker Master Data": [
        "Worker ID", "Name", "Trade", "Skill", "Contractor ID", "Phone",
        "Daily Rate", "Hourly Rate", "OT Mult", "Status", "Hire Date",
        "Certifications", "Emergency Contact",
    ],
    "Worker Attendance": [
        "Att ID", "Date", "Worker ID", "Project ID", "Status",
        "Regular Hrs", "OT Hrs", "Hourly", "OT Mult", "Regular Pay",
        "OT Pay", "Total Pay", "Notes",
    ],
    "Labor Cost Calc": [
        "Line ID", "Project ID", "Room ID", "Worker ID", "Task", "Date",
        "Regular Hrs", "OT Hrs", "Hourly", "OT Mult", "Burden %",
        "Regular $", "OT $", "Burden $", "Total $",
    ],
    "Productivity Tracker": [
        "Prod ID", "Date", "Project ID", "Room ID", "Crew", "Activity",
        "Planned Units", "Actual Units", "Unit", "Planned Hrs", "Actual Hrs",
        "Units / Hr", "Variance %", "Status",
    ],
    "Room Work Checklist": [
        "Check ID", "Project ID", "Room ID", "Phase", "Item", "Responsible",
        "Status", "Due", "Done Date", "Photo", "Notes",
    ],
    "Room Cost Summary": [
        "Room ID", "Project ID", "Room Name", "Area (sf)", "Budget",
        "Materials", "Labor", "Other", "Spent", "Committed", "Remaining",
        "$ / sf", "% Used", "Status",
    ],
    "Measurements Specs": [
        "Meas ID", "Project ID", "Room ID", "Element", "Length (ft)",
        "Width (ft)", "Height (ft)", "Area (sf)", "Perimeter (ft)",
        "Openings (sf)", "Net Area", "Finish / Spec", "Tolerance", "Verified",
    ],
    "Material Selection": [
        "Sel ID", "Project ID", "Room ID", "Category", "Product", "Brand",
        "SKU", "Finish", "Supplier", "Unit Cost", "Status", "Sample Date",
        "Approved By", "Photo", "Notes",
    ],
    "Equipment Inventory": [
        "Equip ID", "Name", "Type", "Brand", "Serial", "Own / Rent",
        "Daily Rate", "Status", "Condition", "Assigned To", "Location",
        "In Service", "Value",
    ],
    "Equipment Usage Log": [
        "Use ID", "Date", "Equip ID", "Project ID", "Operator", "Hours",
        "Daily Rate", "Cost", "From", "To", "Notes",
    ],
    "Equipment Maintenance": [
        "EM ID", "Equip ID", "Type", "Service Date", "Next Due", "Cost",
        "Vendor", "Status", "Notes", "Days Until",
    ],
    "Quality Standards": [
        "Std ID", "Category", "Requirement", "Tolerance", "Test Method",
        "Frequency", "Responsible", "Spec Link",
    ],
    "Defect Snagging List": [
        "Snag ID", "Date", "Project ID", "Room ID", "Location", "Description",
        "Severity", "Assigned To", "Due", "Status", "Est. Cost",
        "Closed Date", "Photo", "Open Rank",
    ],
    "Safety Checklist": [
        "Safe ID", "Date", "Project ID", "Item", "Category", "Result",
        "Hazard", "Corrective Action", "Owner", "Due", "Status",
    ],
    "Incident Accident Log": [
        "Inc ID", "Date", "Project ID", "Type", "Person", "Description",
        "Injury", "Treatment", "Reported To", "Recordable", "Status", "Follow-up",
    ],
    "Invoice Management": [
        "Inv ID", "Date", "Client ID", "Project ID", "Description",
        "Subtotal", "Tax", "Total", "Paid", "Balance", "Due", "Status", "Aging",
    ],
    "Payment Receipts": [
        "Rcpt ID", "Date", "Invoice ID", "Client ID", "Amount", "Method",
        "Reference", "Deposited", "Notes",
    ],
    "Income Tracker": [
        "Inc ID", "Date", "Project ID", "Type", "Source", "Description",
        "Amount", "Method", "Status", "Invoice ID", "Notes",
    ],
    "Profit Loss Project": [
        "Project ID", "Name", "Income", "Labor", "Materials", "Other Cost",
        "Total Cost", "Gross Profit", "Margin %", "Status",
    ],
    "Cash Flow Tracker": [
        "Month", "Opening", "Income", "Expenses", "Net", "Closing", "Notes",
    ],
    "Contract Register": [
        "Contract ID", "Project ID", "Type", "Party", "Value", "Start",
        "End", "Status", "Signed", "Retention %", "Doc Link", "Notes",
    ],
    "After-Sales Service": [
        "Svc ID", "Date", "Client ID", "Project ID", "Type", "Issue",
        "Priority", "Assigned", "Due", "Status", "Cost", "Resolution",
    ],
}

# ---------------------------------------------------------------------------
# Project phases (aligned with Timeline)
# ---------------------------------------------------------------------------
PROJECT_PHASES = [
    ["PH-01", "PRJ-001", "Planning", date(2026, 3, 1), date(2026, 3, 31), None, 2000, None, None, 1.00, "Completed", "", "Marcus Webb", "Scope lock", "Kickoff complete"],
    ["PH-02", "PRJ-001", "Design", date(2026, 3, 15), date(2026, 5, 15), None, 4800, None, None, 1.00, "Completed", "PH-01", "Sofia Alvarez", "Drawings approved", "Kitchen v4 signed"],
    ["PH-03", "PRJ-001", "Permits", date(2026, 4, 1), date(2026, 5, 20), None, 1850, None, None, 1.00, "Completed", "PH-01", "Marcus Webb", "Permit issued", "2026-REM-44182"],
    ["PH-04", "PRJ-001", "Demolition", date(2026, 5, 21), date(2026, 6, 5), None, 2800, None, None, 1.00, "Completed", "PH-03", "Marcus Webb", "Demo complete", ""],
    ["PH-05", "PRJ-001", "Electrical", date(2026, 6, 1), date(2026, 7, 10), None, 2620, None, None, 0.95, "Completed", "PH-04", "Jordan Hale", "Rough passed", "Finish pending cabinets"],
    ["PH-06", "PRJ-001", "Plumbing", date(2026, 6, 8), date(2026, 7, 20), None, 5140, None, None, 1.00, "Completed", "PH-04", "Sam Ortiz", "Trim complete", ""],
    ["PH-07", "PRJ-001", "Walls / plaster", date(2026, 7, 15), date(2026, 8, 10), None, 2000, None, None, 1.00, "Completed", "PH-05", "Leo Park", "Walls closed", ""],
    ["PH-08", "PRJ-001", "Flooring", date(2026, 8, 5), date(2026, 8, 28), None, 8600, None, None, 0.75, "In Progress", "PH-07", "Elena Voss", "Finish this week", "No traffic 48 hrs"],
    ["PH-09", "PRJ-001", "Cabinetry", date(2026, 8, 20), date(2026, 9, 15), None, 18400, None, None, 0.55, "In Progress", "PH-08", "Maya Chen", "Boxes set", "Hardware in transit"],
    ["PH-10", "PRJ-001", "Counters / appliances", date(2026, 9, 10), date(2026, 9, 18), None, 12000, None, None, 0.10, "Scheduled", "PH-09", "Heritage Tile", "Template 4 Sep", ""],
    ["PH-11", "PRJ-001", "Painting", date(2026, 9, 10), date(2026, 9, 28), None, 3600, None, None, 0.00, "Scheduled", "PH-07", "Leo Park", "Guest + dining + entry", ""],
    ["PH-12", "PRJ-001", "Furniture", date(2026, 9, 25), date(2026, 10, 20), None, 4200, None, None, 0.00, "To Do", "PH-11", "Sofia Alvarez", "Order sofa by 1 Sep", ""],
    ["PH-13", "PRJ-001", "Exterior / garden", date(2026, 10, 6), date(2026, 10, 24), None, 7400, None, None, 0.00, "To Do", "PH-11", "Theo Brooks", "Hold extras", "Contingency floor"],
    ["PH-14", "PRJ-001", "Final inspection", date(2026, 10, 25), date(2026, 11, 5), None, 650, None, None, 0.00, "To Do", "PH-12", "Riley Grant", "City final", ""],
    ["PH-15", "PRJ-001", "Handover", date(2026, 11, 10), date(2026, 11, 15), None, 500, None, None, 0.00, "To Do", "PH-14", "Marcus Webb", "Walkthrough", ""],
    ["PH-16", "PRJ-002", "Cabin design", date(2026, 8, 1), date(2026, 9, 30), None, 1200, None, None, 0.40, "In Progress", "", "Sofia Alvarez", "Japandi lock", ""],
    ["PH-17", "PRJ-002", "Cabin construction", date(2026, 10, 15), date(2026, 12, 10), None, 16000, None, None, 0.00, "To Do", "PH-16", "Marcus Webb", "After Maplewood", ""],
]

# ---------------------------------------------------------------------------
# Clients / comms / satisfaction
# ---------------------------------------------------------------------------
CLIENTS = [
    ["CL-001", "Alex Rivera", "Homeowner", "alex.rivera@email.example", "+1-503-555-0148",
     "1847 Maplewood Drive", "Portland", "PROP-001", "PRJ-001", "Active",
     "Referral — Luna Interiors", 85000, "Marcus Webb", date(2026, 8, 24), 4.6,
     "Primary client. Also owns Gorge cabin."],
    ["CL-002", "Alex Rivera (Gorge)", "Repeat", "alex.rivera@email.example", "+1-503-555-0148",
     "88 Ridge Trail", "Hood River", "PROP-002", "PRJ-002", "Active",
     "Repeat — Maplewood", 18500, "Marcus Webb", date(2026, 8, 18), 4.8,
     "Bath-only cabin refresh after handover."],
    ["CL-003", "Jordan Hale (neighbor lead)", "Lead", "j.hale.home@email.example", "+1-503-555-0201",
     "1851 Maplewood Drive", "Portland", "", "", "Lead",
     "Site conversation", 22000, "Marcus Webb", date(2026, 8, 12), "",
     "Powder room + porch. Quote after Nov."],
]

CLIENT_COMMS = [
    ["CM-001", date(2026, 3, 4), "CL-001", "PRJ-001", "Meeting", "Kickoff",
     "Locked rooms, $85k budget, modern-warm palette.", "Marcus Webb", date(2026, 3, 8), "Closed", "TSK-001"],
    ["CM-002", date(2026, 5, 18), "CL-001", "PRJ-001", "Email", "Marble vs porcelain",
     "Alex approved porcelain floor swap (CO-001).", "Sofia Alvarez", date(2026, 5, 20), "Closed", ""],
    ["CM-003", date(2026, 8, 20), "CL-001", "PRJ-001", "Call", "Cabinet delivery",
     "Driveway clear 7:30 tomorrow.", "Maya Chen", date(2026, 8, 21), "Closed", "TSK-013"],
    ["CM-004", date(2026, 8, 21), "CL-001", "PRJ-001", "Site Visit", "Island surface",
     "Porcelain island only; quartz on run.", "Sofia Alvarez", date(2026, 8, 25), "Open", "TSK-026"],
    ["CM-005", date(2026, 8, 24), "CL-001", "PRJ-001", "Email", "Contingency floor",
     "Recommend pausing water feature.", "Morgan Ellis", date(2026, 8, 26), "Open", "AI-005"],
    ["CM-006", date(2026, 8, 18), "CL-002", "PRJ-002", "Email", "Cabin Japandi board",
     "Two fixture directions in Design Studio.", "Sofia Alvarez", date(2026, 9, 15), "Open", "TSK-028"],
    ["CM-007", date(2026, 8, 12), "CL-003", " ", "Site Visit", "Neighbor intro",
     "Walked powder + porch. Follow up after Nov handover.", "Marcus Webb", date(2026, 11, 20), "Open", ""],
]

CLIENT_SAT = [
    ["SAT-001", date(2026, 5, 20), "CL-001", "PRJ-001", "Design", "Survey",
     5, 5, 5, 4, 4, 9, "Loved the 3D dusk render.", "Closed"],
    ["SAT-002", date(2026, 7, 15), "CL-001", "PRJ-001", "Construction", "Walkthrough",
     4, 5, 4, 4, 3, 8, "Kitchen overage stings; bath looks great.", "Closed"],
    ["SAT-003", date(2026, 8, 14), "CL-001", "PRJ-001", "Finishes", "Walkthrough",
     5, 5, 5, 4, 4, 9, "Primary bath punch — haze only.", "Closed"],
    ["SAT-004", date(2026, 8, 18), "CL-002", "PRJ-002", "Design", "Survey",
     5, 5, 5, 5, 5, 10, "Cabin board is exactly the brief.", "Open"],
]

# ---------------------------------------------------------------------------
# Materials ERP
# ---------------------------------------------------------------------------
ESTIMATES = [
    ["EST-001", "PRJ-001", "RM-01", "Cabinetry", "Sage shaker + walnut island", "set", 1, 0.00, None, 14800, 32, 85, None, None, None, "Awarded Cascade"],
    ["EST-002", "PRJ-001", "RM-01", "Counters", "Perimeter quartz Frost", "sf", 42, 0.08, None, 59, 8, 95, None, None, None, "Delivered"],
    ["EST-003", "PRJ-001", "RM-01", "Counters", "Island porcelain HT-8841", "sf", 28, 0.10, None, 66.4, 6, 95, None, None, None, "Approved"],
    ["EST-004", "PRJ-001", "RM-01", "Tile", "Zellige backsplash sand", "sf", 48, 0.15, None, 28, 10, 95, None, None, None, "Quoted"],
    ["EST-005", "PRJ-001", "RM-01", "Flooring", "White oak 7in (kitchen share)", "sf", 200, 0.08, None, 8.2, 16, 80, None, None, None, "Installed"],
    ["EST-006", "PRJ-001", "RM-03", "Tile", "Porcelain floor + shower", "sf", 200, 0.10, None, 15.6, 48, 95, None, None, None, "Installed"],
    ["EST-007", "PRJ-001", "RM-03", "Electrical", "Heated floor kit", "kit", 1, 0.00, None, 1680, 6, 110, None, None, None, "Installed"],
    ["EST-008", "PRJ-001", "RM-06", "Hardscape", "Bluestone path", "sf", 220, 0.08, None, 9.5, 24, 70, None, None, None, "On hold"],
    ["EST-009", "PRJ-002", "RM-09", "Cabinetry", "Cedar vanity 36", "ea", 1, 0.00, None, 2100, 8, 85, None, None, None, "Required"],
]

PURCHASE_ORDERS = [
    ["PO-114", date(2026, 6, 10), "PRJ-001", "Tile & Timber Co.", "Received", 3180, 0, 0, None, 3180, None, date(2026, 6, 20), date(2026, 6, 20), "Bath porcelain"],
    ["PO-129", date(2026, 7, 18), "PRJ-001", "Tile & Timber Co.", "Received", 860, 0, 0, None, 860, None, date(2026, 7, 22), date(2026, 7, 18), "Laundry"],
    ["PO-140", date(2026, 7, 1), "PRJ-001", "Timberline Floors", "Received", 6400, 0, 0, None, 6400, None, date(2026, 7, 28), date(2026, 7, 28), "White oak"],
    ["PO-155", date(2026, 8, 22), "PRJ-001", "Heritage Tile & Stone", "Confirmed", 1860, 0, 85, None, 0, None, date(2026, 9, 8), None, "Island slab"],
    ["PO-160", date(2026, 8, 18), "PRJ-001", "BrightPath Lighting", "Sent", 890, 0, 45, None, 0, None, date(2026, 9, 16), None, "Pendants"],
    ["PO-CAB", date(2026, 8, 2), "PRJ-001", "Cascade Cabinets", "Partial", 14800, 0, 420, None, 7400, None, date(2026, 8, 20), date(2026, 8, 20), "Balance on install"],
]

STOCK = [
    ["STK-001", "TL-WO-7", "White oak 7in leftover", "Flooring", "Garage rack", 42, 14, None, 20, 8.2, None, "Reserved", date(2026, 8, 22), "Timberline Floors"],
    ["STK-002", "HT-8841F", "Porcelain floor extra", "Tile", "Bath crate", 5, 0, None, 4, 14.2, None, "In Stock", date(2026, 8, 12), "Tile & Timber Co."],
    ["STK-003", "RJ-BP-128", "Aged brass bar pulls", "Hardware", "In transit", 0, 28, None, 0, 18, None, "On Order", date(2026, 8, 22), "Rejuvenation"],
    ["STK-004", "BM-HC-50", "Interior paint — Clay", "Paint", "Not ordered", 0, 0, None, 2, 62, None, "Out", None, "Sherwin-Williams"],
    ["STK-005", "CLE-Z-14", "Zellige sand", "Tile", "Not ordered", 0, 0, None, 10, 28, None, "Out", None, "Tile & Timber Co."],
    ["STK-006", "CS-5110", "Quartz offcuts", "Counters", "Shop", 6, 0, None, 0, 59, None, "In Stock", date(2026, 8, 16), "Caesarstone"],
    ["STK-007", "GG-BLU-12", "Bluestone pavers", "Hardscape", "Yard hold", 0, 0, None, 40, 9.5, None, "Out", None, "Garden & Gate"],
]

# ---------------------------------------------------------------------------
# Labor
# ---------------------------------------------------------------------------
WORKERS = [
    ["WK-001", "Maya Chen", "Cabinetry", "Lead", "CTR-001", "+1-503-555-0111", 680, None, 1.5, "Active", date(2024, 3, 1), "CCB millwork", "Eli Chen"],
    ["WK-002", "Jordan Hale", "Electrical", "Lead", "CTR-002", "+1-503-555-0133", 880, None, 1.5, "Active", date(2023, 6, 12), "EL-44821", "Pat Hale"],
    ["WK-003", "Sam Ortiz", "Plumbing", "Lead", "CTR-003", "+1-503-555-0140", 960, None, 1.5, "Active", date(2022, 9, 1), "PL-77310", "Ana Ortiz"],
    ["WK-004", "Priya Shah", "Tile & Stone", "Lead", "CTR-004", "+1-503-555-0155", 760, None, 1.5, "Active", date(2021, 4, 18), "CCB-188442", "Dev Shah"],
    ["WK-005", "Leo Park", "Painting", "Journeyman", "CTR-005", "+1-503-555-0122", 520, None, 1.5, "Active", date(2025, 1, 6), "CCB-201774", "Mina Park"],
    ["WK-006", "Elena Voss", "Flooring", "Lead", "CTR-006", "+1-503-555-0166", 640, None, 1.5, "Active", date(2020, 8, 1), "CCB-176330", "Nils Voss"],
    ["WK-007", "Theo Brooks", "Landscaping", "Journeyman", "CTR-010", "+1-503-555-0199", 560, None, 1.5, "Active", date(2024, 2, 14), "LCB-3320", "Kim Brooks"],
    ["WK-008", "Chris Nguyen", "Carpentry", "Apprentice", "CTR-008", "+1-503-555-0174", 360, None, 1.5, "Active", date(2026, 4, 1), "OSHA-10", "Lan Nguyen"],
]

ATTENDANCE = [
    ["AT-001", date(2026, 8, 18), "WK-001", "PRJ-001", "Present", 8, 0, None, 1.5, None, None, None, "Box scribe"],
    ["AT-002", date(2026, 8, 19), "WK-001", "PRJ-001", "Present", 8, 1, None, 1.5, None, None, None, "Island level"],
    ["AT-003", date(2026, 8, 20), "WK-001", "PRJ-001", "Present", 8, 2, None, 1.5, None, None, None, "Delivery day"],
    ["AT-004", date(2026, 8, 21), "WK-001", "PRJ-001", "Present", 8, 0, None, 1.5, None, None, None, ""],
    ["AT-005", date(2026, 8, 22), "WK-001", "PRJ-001", "Overtime", 8, 3, None, 1.5, None, None, None, "Catch hardware delay"],
    ["AT-006", date(2026, 8, 18), "WK-006", "PRJ-001", "Present", 8, 0, None, 1.5, None, None, None, "Sand"],
    ["AT-007", date(2026, 8, 19), "WK-006", "PRJ-001", "Present", 8, 0, None, 1.5, None, None, None, "First coat"],
    ["AT-008", date(2026, 8, 20), "WK-004", "PRJ-001", "Half Day", 4, 0, None, 1.5, None, None, None, "Punch reclean"],
    ["AT-009", date(2026, 8, 21), "WK-008", "PRJ-001", "Present", 8, 0, None, 1.5, None, None, None, "Entry bench"],
    ["AT-010", date(2026, 8, 22), "WK-008", "PRJ-001", "Present", 8, 0, None, 1.5, None, None, None, ""],
    ["AT-011", date(2026, 8, 24), "WK-001", "PRJ-001", "Present", 8, 0, None, 1.5, None, None, None, "As-of Monday"],
    ["AT-012", date(2026, 8, 24), "WK-006", "PRJ-001", "Present", 8, 0, None, 1.5, None, None, None, "Finish prep"],
]

LABOR_COST = [
    ["LC-001", "PRJ-001", "RM-01", "WK-001", "Cabinet box set", date(2026, 8, 20), 8, 2, None, 1.5, 0.18, None, None, None, None],
    ["LC-002", "PRJ-001", "RM-01", "WK-001", "Cabinet scribe", date(2026, 8, 21), 8, 0, None, 1.5, 0.18, None, None, None, None],
    ["LC-003", "PRJ-001", "RM-01", "WK-001", "Hardware delay catch-up", date(2026, 8, 22), 8, 3, None, 1.5, 0.18, None, None, None, None],
    ["LC-004", "PRJ-001", "RM-02", "WK-006", "Floor sand + coat", date(2026, 8, 19), 8, 0, None, 1.5, 0.18, None, None, None, None],
    ["LC-005", "PRJ-001", "RM-03", "WK-004", "Bath punch reclean", date(2026, 8, 20), 4, 0, None, 1.5, 0.18, None, None, None, None],
    ["LC-006", "PRJ-001", "RM-08", "WK-008", "Entry bench", date(2026, 8, 21), 8, 0, None, 1.5, 0.18, None, None, None, None],
    ["LC-007", "PRJ-001", "RM-01", "WK-002", "Island circuit check", date(2026, 8, 15), 3, 0, None, 1.5, 0.18, None, None, None, None],
]

PRODUCTIVITY = [
    ["PR-001", date(2026, 8, 8), "PRJ-001", "RM-03", "Heritage crew", "Shower tile", 40, 38, "sf", 8, 8.5, None, None, "Complete"],
    ["PR-002", date(2026, 8, 12), "PRJ-001", "RM-02", "Timberline", "Oak install", 220, 210, "sf", 8, 9, None, None, "Complete"],
    ["PR-003", date(2026, 8, 20), "PRJ-001", "RM-01", "Cascade", "Cabinet boxes", 18, 16, "ea", 8, 10, None, None, "In Progress"],
    ["PR-004", date(2026, 8, 21), "PRJ-001", "RM-08", "Ironwood", "Entry bench", 1, 1, "ea", 6, 8, None, None, "In Progress"],
    ["PR-005", date(2026, 8, 22), "PRJ-001", "RM-02", "Timberline", "Finish coat prep", 1, 1, "room", 4, 4, None, None, "On Track"],
    ["PR-006", date(2026, 7, 22), "PRJ-001", "RM-07", "Pacific", "Laundry install", 1, 1, "room", 6, 5.5, None, None, "Complete"],
]

# ---------------------------------------------------------------------------
# Rooms / design extras
# ---------------------------------------------------------------------------
ROOM_CHECKS = [
    ["CK-001", "PRJ-001", "RM-01", "Cabinetry", "Boxes level and scribed", "Maya Chen", "In Progress", date(2026, 8, 27), None, "", "Island still moving"],
    ["CK-002", "PRJ-001", "RM-01", "Cabinetry", "Doors hung, gaps even", "Maya Chen", "Not Started", date(2026, 9, 5), None, "", "Wait on pulls"],
    ["CK-003", "PRJ-001", "RM-01", "Counters", "Template after doors", "Heritage Tile", "Not Started", date(2026, 9, 4), None, "", ""],
    ["CK-004", "PRJ-001", "RM-01", "Appliances", "Range / fridge openings", "Marcus Webb", "Not Started", date(2026, 9, 12), None, "", ""],
    ["CK-005", "PRJ-001", "RM-03", "Punch", "Grout haze on niche", "Priya Shah", "In Progress", date(2026, 8, 26), None, "drive/photos/bath-niche", "Reclean Thu"],
    ["CK-006", "PRJ-001", "RM-03", "Punch", "Door alignment", "Priya Shah", "Complete", date(2026, 8, 20), date(2026, 8, 20), "", ""],
    ["CK-007", "PRJ-001", "RM-03", "Punch", "Silicone wet walls", "Priya Shah", "Complete", date(2026, 8, 14), date(2026, 8, 14), "", ""],
    ["CK-008", "PRJ-001", "RM-07", "Closeout", "Utility sink sealed", "Sam Ortiz", "Complete", date(2026, 7, 24), date(2026, 7, 24), "", ""],
    ["CK-009", "PRJ-001", "RM-02", "Flooring", "No traffic 48 hrs after coat", "Elena Voss", "In Progress", date(2026, 8, 30), None, "", "Tue coat"],
    ["CK-010", "PRJ-001", "RM-08", "Carpentry", "Hook rail + bench", "Chris Nguyen", "In Progress", date(2026, 8, 29), None, "", ""],
    ["CK-011", "PRJ-001", "RM-04", "Paint", "Palette lock clay + linen", "Sofia Alvarez", "Not Started", date(2026, 9, 8), None, "", "Awaiting Alex"],
    ["CK-012", "PRJ-002", "RM-09", "Design", "Japandi fixture direction", "Sofia Alvarez", "In Progress", date(2026, 9, 15), None, "drive/mood/cabin", ""],
]

MEASUREMENTS = [
    ["MS-001", "PRJ-001", "RM-01", "Kitchen floor", 16.0, 12.5, 9.0, None, None, 6.0, None, "White oak 7in", "1/8 in", "Yes"],
    ["MS-002", "PRJ-001", "RM-01", "Island", 8.0, 3.5, 3.0, None, None, 0.0, None, "Porcelain slab", "1/16 in", "Yes"],
    ["MS-003", "PRJ-001", "RM-01", "Backsplash run", 14.0, 0.0, 1.5, None, None, 4.5, None, "Zellige sand", "1/8 in", "No"],
    ["MS-004", "PRJ-001", "RM-03", "Bath floor", 10.0, 8.0, 8.5, None, None, 8.0, None, "Porcelain 12x24", "1/16 in", "Yes"],
    ["MS-005", "PRJ-001", "RM-03", "Shower walls", 9.0, 3.5, 8.0, None, None, 0.0, None, "Porcelain 12x24", "1/16 in", "Yes"],
    ["MS-006", "PRJ-001", "RM-02", "Living floor", 20.0, 15.0, 9.5, None, None, 18.0, None, "White oak 7in", "1/8 in", "Yes"],
    ["MS-007", "PRJ-001", "RM-08", "Entry", 8.0, 7.0, 9.5, None, None, 14.0, None, "Paint + oak bench", "1/4 in", "No"],
    ["MS-008", "PRJ-002", "RM-09", "Cabin bath", 8.0, 6.5, 8.0, None, None, 6.0, None, "TBD Japandi", "1/8 in", "No"],
]

SELECTIONS = [
    ["SEL-001", "PRJ-001", "RM-01", "Cabinetry", "Sage shaker inset", "Cascade", "CC-SH-Sage", "Sage / walnut", "Cascade Cabinets", 14800, "Approved", date(2026, 5, 12), "Alex Rivera", "drive/cabs/shaker-sage", ""],
    ["SEL-002", "PRJ-001", "RM-01", "Counters", "Frost quartz", "Caesarstone", "CS-5110", "Frost", "Caesarstone", 59, "Installed", date(2026, 5, 20), "Sofia Alvarez", "drive/counters/frost", "Perimeter"],
    ["SEL-003", "PRJ-001", "RM-01", "Counters", "Island porcelain", "Heritage", "HT-8841", "Soft white", "Heritage Tile & Stone", 66.4, "Approved", date(2026, 8, 21), "", "drive/bath/materials", "Pending sign"],
    ["SEL-004", "PRJ-001", "RM-01", "Tile", "Zellige sand", "Cle", "CLE-Z-14", "Sand", "Tile & Timber Co.", 28, "Sampled", date(2026, 8, 10), "", "drive/tile/zellige", "Layout 8 Sep"],
    ["SEL-005", "PRJ-001", "RM-01", "Hardware", "Bar pull 128", "Rejuvenation", "RJ-BP-128", "Aged brass", "Rejuvenation", 18, "Approved", date(2026, 6, 1), "Sofia Alvarez", "", "In transit"],
    ["SEL-006", "PRJ-001", "RM-03", "Tile", "Porcelain 12x24", "Heritage", "HT-8841F", "Soft white", "Tile & Timber Co.", 14.2, "Installed", date(2026, 5, 18), "Alex Rivera", "", "vs marble"],
    ["SEL-007", "PRJ-001", "RM-02", "Furniture", "Sven sofa", "Article", "ART-SVEN", "Oatmeal", "Article", 2400, "Considering", date(2026, 8, 15), "", "drive/furn/living", "Order by 1 Sep"],
    ["SEL-008", "PRJ-002", "RM-09", "Fixtures", "Matte black set", "Brizo", "BZ-CB-01", "Matte black", "Ferguson", 720, "Considering", date(2026, 8, 18), "", "drive/mood/cabin", "Alt: aged brass"],
]

# ---------------------------------------------------------------------------
# Equipment
# ---------------------------------------------------------------------------
EQUIPMENT = [
    ["EQ-001", "Table saw", "Shop", "DeWalt", "DWE7491-441", "Own", 0, "In Use", "Good", "Maya Chen", "Maplewood garage", date(2023, 4, 1), 650],
    ["EQ-002", "Track saw", "Shop", "Festool", "TS55-9921", "Own", 0, "In Use", "Excellent", "Maya Chen", "Kitchen", date(2024, 2, 1), 780],
    ["EQ-003", "Tile wet saw", "Tile", "MK Diamond", "MK-101-18", "Own", 45, "Available", "Good", "Priya Shah", "Heritage shop", date(2022, 6, 1), 520],
    ["EQ-004", "Floor sander", "Flooring", "Lagler", "HUMMEL-7", "Rent", 95, "In Use", "Good", "Elena Voss", "Living room", date(2026, 8, 5), 0],
    ["EQ-005", "HEPA vac", "Dust", "Festool", "CT26-110", "Own", 0, "In Use", "Excellent", "Elena Voss", "Living room", date(2024, 9, 1), 620],
    ["EQ-006", "Scaffold tower", "Access", "Werner", "WER-10-44", "Own", 35, "Available", "Fair", "Marcus Webb", "Ironwood yard", date(2021, 3, 1), 890],
    ["EQ-007", "Dumpster 20 yd", "Haul", "WasteMgmt", "WM-20-8821", "Rent", 85, "Available", "Good", "Marcus Webb", "Off site", date(2026, 5, 21), 0],
    ["EQ-008", "Laser level", "Layout", "Bosch", "GLL3-330", "Own", 0, "In Use", "Excellent", "Chris Nguyen", "Entry", date(2025, 1, 12), 210],
]

EQUIP_USAGE = [
    ["EU-001", date(2026, 8, 20), "EQ-001", "PRJ-001", "Maya Chen", 6, 0, None, "Garage", "Kitchen", "Island stretchers"],
    ["EU-002", date(2026, 8, 21), "EQ-002", "PRJ-001", "Maya Chen", 4, 0, None, "Kitchen", "Kitchen", "Scribe panels"],
    ["EU-003", date(2026, 8, 18), "EQ-004", "PRJ-001", "Elena Voss", 8, 95, None, "Living", "Living", "Rental day 13"],
    ["EU-004", date(2026, 8, 19), "EQ-004", "PRJ-001", "Elena Voss", 8, 95, None, "Living", "Dining", "Rental day 14"],
    ["EU-005", date(2026, 8, 22), "EQ-005", "PRJ-001", "Elena Voss", 8, 0, None, "Living", "Living", "Finish dust"],
    ["EU-006", date(2026, 8, 21), "EQ-008", "PRJ-001", "Chris Nguyen", 3, 0, None, "Entry", "Entry", "Bench height"],
    ["EU-007", date(2026, 7, 10), "EQ-003", "PRJ-001", "Priya Shah", 8, 0, None, "Bath", "Bath", "Shower walls"],
]

EQUIP_MAINT = [
    ["EM-001", "EQ-001", "Blade + alignment", date(2026, 7, 1), date(2026, 10, 1), 48, "Tool shop", "Upcoming", "Check fence", None],
    ["EM-002", "EQ-004", "Rental return inspect", date(2026, 8, 28), date(2026, 8, 28), 0, "Rental yard", "Scheduled", "After finish coat", None],
    ["EM-003", "EQ-006", "Weld crack on brace", date(2026, 6, 15), date(2026, 9, 15), 120, "Yard fab", "Due Soon", "Do not use until signed", None],
    ["EM-004", "EQ-005", "Filter change", date(2026, 8, 1), date(2026, 11, 1), 35, "Festool", "Upcoming", "", None],
    ["EM-005", "EQ-003", "Pump flush", date(2026, 7, 12), date(2027, 1, 12), 0, "Heritage", "Upcoming", "", None],
]

# ---------------------------------------------------------------------------
# Quality / safety
# ---------------------------------------------------------------------------
QUALITY_STDS = [
    ["QS-001", "Tile", "Lippage max 1/32 in on 12x24", "1/32 in", "Straightedge + feeler", "Each wall", "Priya Shah", "drive/spec/tile.pdf"],
    ["QS-002", "Flooring", "Moisture < 12% before finish", "12%", "Pin meter", "Each room", "Elena Voss", "drive/spec/oak.pdf"],
    ["QS-003", "Paint", "Sheen match within 5 GU", "5 GU", "Gloss meter", "Each elevation", "Leo Park", "drive/spec/paint.pdf"],
    ["QS-004", "Cabinetry", "Reveal 1/8 in ± 1/32", "1/32 in", "Story pole", "Each run", "Maya Chen", "drive/spec/cabs.pdf"],
    ["QS-005", "Counters", "Seam < 1/32, color match", "1/32 in", "Visual + card", "Each seam", "Heritage Tile", "drive/spec/stone.pdf"],
    ["QS-006", "Electrical", "AFCI / GFCI as permitted", "Code", "City inspector", "Rough + final", "Jordan Hale", "NEC 2023"],
    ["QS-007", "Plumbing", "Shower pan holds 24 hrs", "0 leak", "Flood test", "Before tile", "Sam Ortiz", "drive/insp/pan.pdf"],
    ["QS-008", "Safety", "HEPA on all sanding", "Visible dust = fail", "Site walk", "Daily", "Marcus Webb", "drive/spec/dust.pdf"],
]

SNAGS = [
    ["SN-001", date(2026, 8, 18), "PRJ-001", "RM-03", "Niche shelf", "Grout haze remaining",
     "Cosmetic", "Priya Shah", date(2026, 8, 26), "In Progress", 0, None, "drive/photos/bath-niche", None],
    ["SN-002", date(2026, 8, 20), "PRJ-001", "RM-01", "Island", "Island out of level 1/16 after delivery",
     "Minor", "Maya Chen", date(2026, 8, 25), "Assigned", 0, None, "", None],
    ["SN-003", date(2026, 8, 21), "PRJ-001", "RM-02", "Stair nosing", "Factory nosing backordered — site-cut approved",
     "Minor", "Elena Voss", date(2026, 8, 28), "Assigned", 0, None, "", None],
    ["SN-004", date(2026, 8, 12), "PRJ-001", "RM-03", "Shower door", "Strike plate high 2mm",
     "Minor", "Priya Shah", date(2026, 8, 20), "Closed", 0, date(2026, 8, 20), "", None],
    ["SN-005", date(2026, 7, 2), "PRJ-001", "RM-01", "Pantry", "Missing AFCI — added same day",
     "Major", "Jordan Hale", date(2026, 7, 2), "Closed", 0, date(2026, 7, 2), "", None],
    ["SN-006", date(2026, 8, 22), "PRJ-001", "RM-08", "Hook rail", "Wait for wall paint before final screws",
     "Cosmetic", "Chris Nguyen", date(2026, 9, 22), "Open", 0, None, "", None],
    ["SN-007", date(2026, 8, 23), "PRJ-001", "RM-01", "Hardware", "Pulls not on site — do not hang doors",
     "Major", "Maya Chen", date(2026, 8, 29), "Open", 0, None, "", None],
]

SAFETY = [
    ["SF-001", date(2026, 8, 18), "PRJ-001", "PPE on site", "PPE", "Pass", "", "", "Marcus Webb", None, "Complete"],
    ["SF-002", date(2026, 8, 18), "PRJ-001", "HEPA vac during sanding", "Dust", "Pass", "", "", "Elena Voss", None, "Complete"],
    ["SF-003", date(2026, 8, 19), "PRJ-001", "Ladder tied off at stair", "Access", "Fail", "Unsecured 6ft", "Tie and re-brief", "Chris Nguyen", date(2026, 8, 19), "Corrected"],
    ["SF-004", date(2026, 8, 20), "PRJ-001", "Electrical lockout island circuit", "Electrical", "Pass", "", "", "Jordan Hale", None, "Complete"],
    ["SF-005", date(2026, 8, 21), "PRJ-001", "Driveway / public way clear", "Site", "Pass", "", "Cones at cabinet truck", "Maya Chen", None, "Complete"],
    ["SF-006", date(2026, 8, 22), "PRJ-001", "First-aid kit stocked", "Medical", "Pass", "", "", "Marcus Webb", None, "Complete"],
    ["SF-007", date(2026, 8, 24), "PRJ-001", "Finish-coat ventilation", "Air", "N/A", "Coat Tuesday", "Open windows + fan", "Elena Voss", date(2026, 8, 26), "In Progress"],
]

INCIDENTS = [
    ["INC-001", date(2026, 8, 19), "PRJ-001", "Near Miss", "Chris Nguyen",
     "Ladder kicked at stair — no fall.", "None", "Re-brief + tie-off", "Marcus Webb", "No", "Closed", "SF-003"],
    ["INC-002", date(2026, 6, 4), "PRJ-001", "First Aid", "Demo laborer",
     "Cut on plaster lath — cleaned and bandaged.", "Laceration", "On-site first aid", "Marcus Webb", "No", "Closed", "Tetanus current"],
    ["INC-003", date(2026, 7, 18), "PRJ-001", "Property Damage", "Tile crate",
     "Crate corner crushed in driveway — 3 tiles broken.", "None", "Supplier replaced", "Harper Quinn", "No", "Closed", "Extra 5 tiles now stock"],
]

# ---------------------------------------------------------------------------
# Billing / income / contracts / after-sales
# ---------------------------------------------------------------------------
INVOICES = [
    ["INV-001", date(2026, 3, 15), "CL-001", "PRJ-001", "Draw 1 — mobilization + design start", 15000, 0, None, 15000, None, date(2026, 3, 29), "Paid", None],
    ["INV-002", date(2026, 6, 1), "CL-001", "PRJ-001", "Draw 2 — demo + rough-in", 22000, 0, None, 22000, None, date(2026, 6, 15), "Paid", None],
    ["INV-003", date(2026, 8, 1), "CL-001", "PRJ-001", "Draw 3 — finishes progress", 18000, 0, None, 12000, None, date(2026, 8, 15), "Partial", None],
    ["INV-004", date(2026, 9, 15), "CL-001", "PRJ-001", "Draw 4 — cabinets + counters", 16000, 0, None, 0, None, date(2026, 9, 29), "Draft", None],
    ["INV-005", date(2026, 11, 10), "CL-001", "PRJ-001", "Final + retention release", 14000, 0, None, 0, None, date(2026, 11, 24), "Draft", None],
    ["INV-006", date(2026, 8, 1), "CL-002", "PRJ-002", "Cabin design deposit", 1200, 0, None, 600, None, date(2026, 8, 15), "Partial", None],
]

RECEIPTS = [
    ["RCT-001", date(2026, 3, 18), "INV-001", "CL-001", 15000, "ACH", "WIRE-AR-0318", date(2026, 3, 18), "Draw 1"],
    ["RCT-002", date(2026, 6, 8), "INV-002", "CL-001", 22000, "ACH", "WIRE-AR-0608", date(2026, 6, 8), "Draw 2"],
    ["RCT-003", date(2026, 8, 10), "INV-003", "CL-001", 12000, "ACH", "WIRE-AR-0810", date(2026, 8, 10), "Partial draw 3"],
    ["RCT-004", date(2026, 8, 1), "INV-006", "CL-002", 600, "ACH", "WIRE-AR-0801", date(2026, 8, 1), "Cabin deposit"],
]

INCOME = [
    ["INC-001", date(2026, 3, 18), "PRJ-001", "Deposit", "Alex Rivera", "Draw 1 mobilization", 15000, "ACH", "Paid", "INV-001", ""],
    ["INC-002", date(2026, 6, 8), "PRJ-001", "Client Payment", "Alex Rivera", "Draw 2 rough-in", 22000, "ACH", "Paid", "INV-002", ""],
    ["INC-003", date(2026, 8, 10), "PRJ-001", "Client Payment", "Alex Rivera", "Draw 3 partial", 12000, "ACH", "Paid", "INV-003", ""],
    ["INC-004", date(2026, 8, 15), "PRJ-001", "Client Payment", "Alex Rivera", "Draw 3 balance", 6000, "ACH", "Planned", "INV-003", "Awaiting"],
    ["INC-005", date(2026, 9, 29), "PRJ-001", "Client Payment", "Alex Rivera", "Draw 4 cabinets", 16000, "ACH", "Planned", "INV-004", ""],
    ["INC-006", date(2026, 8, 1), "PRJ-002", "Deposit", "Alex Rivera", "Cabin design deposit", 600, "ACH", "Paid", "INV-006", ""],
    ["INC-007", date(2026, 9, 15), "PRJ-002", "Client Payment", "Alex Rivera", "Cabin design balance", 600, "ACH", "Planned", "INV-006", ""],
]

CONTRACTS = [
    ["CON-001", "PRJ-001", "GC Agreement", "Ironwood Construction", 6200, date(2026, 3, 4), date(2026, 11, 15), "Active", "Yes", 0.05, "drive/docs/iw-contract.pdf", "Monthly supervision"],
    ["CON-002", "PRJ-001", "Design", "Luna Interiors", 4800, date(2026, 3, 6), date(2026, 11, 1), "Active", "Yes", 0.00, "drive/docs/luna-contract.pdf", ""],
    ["CON-003", "PRJ-001", "Subcontract", "Cascade Cabinets", 18400, date(2026, 5, 28), date(2026, 9, 15), "Active", "Yes", 0.00, "drive/docs/cascade-contract.pdf", "Includes install"],
    ["CON-004", "PRJ-001", "Subcontract", "Heritage Tile & Stone", 7460, date(2026, 5, 20), date(2026, 8, 26), "Active", "Yes", 0.00, "drive/docs/heritage.pdf", "Punch open"],
    ["CON-005", "PRJ-001", "Supply", "Timberline Floors", 8600, date(2026, 6, 1), date(2026, 8, 28), "Active", "Yes", 0.00, "", "Supply + install"],
    ["CON-006", "PRJ-001", "Change Order", "Island porcelain CO-002", -460, date(2026, 8, 21), date(2026, 9, 11), "Sent", "No", 0.00, "drive/co/co-002.pdf", "Awaiting signature"],
    ["CON-007", "PRJ-002", "Design", "Luna Interiors — cabin", 1200, date(2026, 8, 1), date(2026, 9, 30), "Active", "Yes", 0.00, "", "Concept only"],
]

AFTER_SALES = [
    ["AS-001", date(2026, 8, 18), "CL-001", "PRJ-001", "Callback", "Grout haze on niche shelf",
     "Low", "Priya Shah", date(2026, 8, 26), "Scheduled", 0, "Reclean Thursday"],
    ["AS-002", date(2026, 8, 14), "CL-001", "PRJ-001", "Warranty Claim", "Register WarmFloor + Brizo",
     "Medium", "Jamie Cole", date(2026, 9, 15), "Open", 0, "Need serials"],
    ["AS-003", date(2026, 11, 16), "CL-001", "PRJ-001", "Consultation", "Handover packet walkthrough",
     "Medium", "Marcus Webb", date(2026, 11, 16), "Open", 0, "After city final"],
    ["AS-004", date(2026, 8, 18), "CL-002", "PRJ-002", "Consultation", "Cabin fixture direction",
     "Low", "Sofia Alvarez", date(2026, 9, 15), "In Progress", 0, "Two options out"],
]
