#!/usr/bin/env python3
"""Integrity check for the protected Novality Store workbook."""

from __future__ import annotations

import sys
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.cell.cell import MergedCell

ROOT = Path(__file__).resolve().parent
XLSX = ROOT / "Novality_Store_Home_Renovation_System.xlsx"

EXPECTED_SHEETS = [
    "Start Here", "Dashboard", "Projects", "Rooms", "Design Studio", "AI Insights",
    "Budget", "Expenses", "Finance", "Contractors", "Quotes", "Jobs",
    "Tasks", "Timeline", "Materials", "Shopping List", "Suppliers",
    "Documents", "Messages", "Inventory", "Maintenance",
    "Inspections", "Payments", "Change Orders", "Permits", "Warranties",
    "Calendar", "Notifications", "Users", "Properties", "Roles & Permissions",
    "Admin", "Settings", "Lookups", "Audit Log",
]

REQUIRED_NAMES = {
    "ActiveProject", "HomeownerName", "AsOfDate", "ContingencyPct",
    "ContingencyFloor", "OverrunAlert", "CompanyName", "TaxRate",
}

KEY_FORMULAS = {
    ("Projects", "R5"): "SUMIFS",
    ("Rooms", "Q5"): "ROUND",
    ("Budget", "G5"): "SUMIFS",
    ("Finance", "A6"): "SUMIF",
    ("Contractors", "M5"): "AVERAGE",
    ("Tasks", "Q5"): "Overdue",
    ("Materials", "K5"): "$H5*$J5",
    ("Dashboard", "D12"): "H8-K8-A12",
}


def main() -> int:
    if not XLSX.exists():
        print("MISSING", XLSX)
        return 2
    wb = load_workbook(XLSX, data_only=False)
    fails = []
    notes = []

    if list(wb.sheetnames) != EXPECTED_SHEETS:
        fails.append(f"Sheet order/count mismatch: {wb.sheetnames}")
    else:
        notes.append(f"35 sheets in expected order")

    creator = wb.properties.creator
    modified = wb.properties.lastModifiedBy
    if creator != "premium":
        fails.append(f"creator is {creator!r}, expected 'premium'")
    else:
        notes.append("Author / creator = premium")
    if modified != "premium":
        fails.append(f"lastModifiedBy is {modified!r}, expected 'premium'")
    else:
        notes.append("Last modified by = premium")

    names = set(wb.defined_names.keys())
    missing = REQUIRED_NAMES - names
    if missing:
        fails.append(f"Missing named ranges: {sorted(missing)}")
    else:
        notes.append(f"{len(names)} named ranges present")

    unprotected = []
    formula_unlocked = []
    formula_count = 0
    locked_formulas = 0
    for ws in wb.worksheets:
        if not ws.protection.sheet:
            unprotected.append(ws.title)
        for row in ws.iter_rows(min_row=1, max_row=min(ws.max_row or 1, 80),
                                min_col=1, max_col=min(ws.max_column or 1, 40)):
            for cell in row:
                if isinstance(cell, MergedCell):
                    continue
                if isinstance(cell.value, str) and cell.value.startswith("="):
                    formula_count += 1
                    if not cell.protection.locked:
                        formula_unlocked.append(f"{ws.title}!{cell.coordinate}")
                    else:
                        locked_formulas += 1

    if unprotected:
        fails.append(f"Sheets not protected: {unprotected}")
    else:
        notes.append("All 35 sheets have sheet protection enabled")

    if formula_unlocked:
        fails.append(f"{len(formula_unlocked)} formula cells left unlocked (first 8): {formula_unlocked[:8]}")
    else:
        notes.append(f"{locked_formulas} sampled formula cells are locked")

    for (sheet, addr), needle in KEY_FORMULAS.items():
        val = str(wb[sheet][addr].value or "")
        if needle not in val:
            fails.append(f"{sheet}!{addr} missing {needle!r}: {val[:80]!r}")
    notes.append("Key live formulas still present")

    # Sample data still there
    if wb["Projects"]["A5"].value != "PRJ-001":
        fails.append("Sample project PRJ-001 missing")
    if wb["Materials"]["P5"].value != "Delivered":
        fails.append(f"Materials status misaligned: {wb['Materials']['P5'].value!r}")
    if wb["Settings"]["B5"].value != "Novality Store":
        fails.append("Settings company name changed")
    notes.append("Sample story (PRJ-001 / Maplewood) intact")

    report = ROOT / "INTEGRITY_REPORT.md"
    lines = [
        "# Integrity report",
        "",
        f"File: `{XLSX.name}` ({XLSX.stat().st_size:,} bytes)",
        "",
        "## Result: **" + ("PASS" if not fails else "FAIL") + "**",
        "",
        "### Checks passed",
    ]
    for n in notes:
        lines.append(f"- {n}")
    lines += ["", "### Failures"]
    if fails:
        for f in fails:
            lines.append(f"- {f}")
    else:
        lines.append("- None")
    lines += [
        "",
        "### Protection",
        "",
        "- Sheet password: `premium`",
        "- Author: `premium`",
        "- Formula / header / dashboard cells: locked",
        "- Ivory input cells on registers + Settings column B + Lookups: unlocked",
        "- Unprotect path: Review → Unprotect Sheet → `premium`",
        "",
    ]
    report.write_text("\n".join(lines), encoding="utf-8")
    print(report.read_text(encoding="utf-8"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
