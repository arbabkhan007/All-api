"""Verify the generated Wedding Planner V2 workbook (Novality Store)."""
import zipfile

from openpyxl import load_workbook

PATH = "/home/user/All-api/Wedding_Planner_V2_Novality_Store.xlsx"

wb = load_workbook(PATH)
errors = []
total_formulas = 0
total_unlocked_formulas = 0
total_dvs = 0
per_sheet = []

for ws in wb.worksheets:
    # 1. protection on + password present
    if not ws.protection.sheet:
        errors.append(f"{ws.title}: sheet protection OFF")
    if not ws.protection.password:
        errors.append(f"{ws.title}: no protection password set")

    n_f, n_unlocked = 0, 0
    for row in ws.iter_rows():
        for c in row:
            v = c.value
            if isinstance(v, str) and v.startswith("="):
                n_f += 1
                if c.protection is not None and c.protection.locked is False:
                    n_unlocked += 1
    total_formulas += n_f
    total_unlocked_formulas += n_unlocked
    total_dvs += len(ws.data_validations.dataValidation)
    per_sheet.append((ws.title, n_f, len(ws.data_validations.dataValidation)))

    if n_unlocked:
        errors.append(f"{ws.title}: {n_unlocked} UNLOCKED formula cells!")

# 2. metadata
p = wb.properties
if p.creator != "Novality Store":
    errors.append(f"creator={p.creator!r}")
if "Version 2" not in (p.title or ""):
    errors.append(f"title={p.title!r}")

# 3. spot-check key formulas
d = wb["Dashboard"]
checks = [
    ("Dashboard", "C21", "='Master Budget'!$C$31"),
    ("Dashboard", "C28", "='Guest List'!$C$5"),
    ("Dashboard", "E8", '=IF($C$8="","—",$C$8-TODAY())'),
    ("Master Budget", "F9", None),
    ("Budget Breakdown", "C9",
     "=SUMIF('Master Budget'!$B$9:$B$30,$B9,'Master Budget'!$C$9:$C$30)"),
    ("Meal Count Summary", "C9", "=COUNTIF('Guest List'!$H$9:$H$208,$B9)"),
    ("Thank You Cards", "B9", "=IF('Guest List'!$B9=\"\",\"\",'Guest List'!$B9)"),
]
for sheet, coord, expect in checks:
    v = wb[sheet][coord].value
    if not (isinstance(v, str) and v.startswith("=")):
        errors.append(f"{sheet}!{coord}: expected formula, got {v!r}")
    elif expect and v != expect:
        errors.append(f"{sheet}!{coord}: {v!r} != {expect!r}")

# 4. hyperlink on Start Here points inside workbook
sh = wb["Start Here"]
hl = [c for row in sh.iter_rows(min_row=5) for c in row if c.hyperlink is not None]
if len(hl) < 50:
    errors.append(f"Start Here: only {len(hl)} hyperlinks")
bad_hl = [c.hyperlink.location for c in hl
          if c.hyperlink.location and c.hyperlink.location.split("!")[0].strip("'")
          not in wb.sheetnames]
if bad_hl:
    errors.append(f"Start Here: broken hyperlink targets {bad_hl[:3]}")

# 5. protection password is actually hashed in the XML of every sheet
with zipfile.ZipFile(PATH) as z:
    sheet_xml = [n for n in z.namelist() if n.startswith("xl/worksheets/sheet")]
    unhashed = []
    for n in sheet_xml:
        xml = z.read(n).decode("utf-8", "ignore")
        if "<sheetProtection" not in xml:
            unhashed.append(n)
    if unhashed:
        errors.append(f"{len(unhashed)} sheets missing sheetProtection XML")

print(f"sheets: {len(wb.sheetnames)}")
print(f"total locked formula cells: {total_formulas}")
print(f"unlocked formula cells:     {total_unlocked_formulas}")
print(f"dropdown validations:       {total_dvs}")
print(f"file size: {__import__('os').path.getsize(PATH)/1e6:.2f} MB")
print("\nformulas per sheet (top 10):")
for name, n_f, dv in sorted(per_sheet, key=lambda x: -x[1])[:10]:
    print(f"  {name:26s} {n_f:4d} formulas  {dv} dropdowns")
print()
if errors:
    print("PROBLEMS:")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)
print("✅ ALL CHECKS PASSED")
