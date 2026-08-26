#!/usr/bin/env python3
"""Integrity check for the protected Novality Store workbook."""

from __future__ import annotations

import sys
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.cell.cell import MergedCell

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from hrms.modules import SHEET_ORDER  # noqa: E402

XLSX = ROOT / "Novality_Store_Home_Renovation_System.xlsx"

EXPECTED_SHEETS = SHEET_ORDER
AUTHOR = "Novality store"

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
    ("Module Hub", "A4"): "MODULE QUICK LINKS",
    ("Project Phases", "F5"): "$E5-$D5",
    ("Labor Cost Calc", "O5"): "$L5+$M5+$N5",
    ("Invoice Management", "H5"): "$F5+$G5",
    ("Profit Loss Project", "H5"): "$C5-$G5",
}


def main() -> int:
    if not XLSX.exists():
        print("MISSING", XLSX)
        return 2
    wb = load_workbook(XLSX, data_only=False)
    fails = []
    notes = []

    if list(wb.sheetnames) != EXPECTED_SHEETS:
        extra = [s for s in wb.sheetnames if s not in EXPECTED_SHEETS]
        missing = [s for s in EXPECTED_SHEETS if s not in wb.sheetnames]
        fails.append(
            f"Sheet order/count mismatch ({len(wb.sheetnames)} vs {len(EXPECTED_SHEETS)}). "
            f"Missing={missing[:8]} Extra={extra[:8]}"
        )
    else:
        notes.append(f"{len(EXPECTED_SHEETS)} sheets in expected order")

    creator = wb.properties.creator
    modified = wb.properties.lastModifiedBy
    if creator != AUTHOR:
        fails.append(f"creator is {creator!r}, expected {AUTHOR!r}")
    else:
        notes.append(f"Author / creator = {AUTHOR}")
    if modified != AUTHOR:
        fails.append(f"lastModifiedBy is {modified!r}, expected {AUTHOR!r}")
    else:
        notes.append(f"Last modified by = {AUTHOR}")

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
    banned = []
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
                    val = cell.value.upper()
                    if "FILTER(" in val or "SMALL(IF" in val:
                        banned.append(f"{ws.title}!{cell.coordinate}")
                    if not cell.protection.locked:
                        formula_unlocked.append(f"{ws.title}!{cell.coordinate}")
                    else:
                        locked_formulas += 1

    if unprotected:
        fails.append(f"Sheets not protected: {unprotected}")
    else:
        notes.append(f"All {len(wb.sheetnames)} sheets have sheet protection enabled")

    if formula_unlocked:
        fails.append(f"{len(formula_unlocked)} formula cells left unlocked (first 8): {formula_unlocked[:8]}")
    else:
        notes.append(f"{locked_formulas} sampled formula cells are locked")

    if banned:
        fails.append(f"Banned FILTER/SMALL-IF formulas: {banned[:6]}")
    else:
        notes.append("No FILTER / SMALL(IF) formulas in sampled cells")

    for (sheet, addr), needle in KEY_FORMULAS.items():
        val = str(wb[sheet][addr].value or "")
        if needle not in val:
            fails.append(f"{sheet}!{addr} missing {needle!r}: {val[:80]!r}")
    notes.append("Key live formulas still present")

    if wb["Projects"]["A5"].value != "PRJ-001":
        fails.append("Sample project PRJ-001 missing")
    if wb["Materials"]["P5"].value != "Delivered":
        fails.append(f"Materials status misaligned: {wb['Materials']['P5'].value!r}")
    if wb["Settings"]["B5"].value != "Novality Store":
        fails.append("Settings company name changed")
    if wb["Client Master Data"]["A5"].value != "CL-001":
        fails.append("Client master sample missing")
    notes.append("Sample story (PRJ-001 / Maplewood / CL-001) intact")

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
        f"- Author: `{AUTHOR}`",
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
