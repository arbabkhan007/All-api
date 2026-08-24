#!/usr/bin/env python3
"""Generate the Novality Store Home Renovation Management System workbook.

Usage:
    python generate_workbook.py
    python generate_workbook.py --out /path/to/file.xlsx
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Allow running from this folder or the repo root
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from hrms.workbook import build_workbook  # noqa: E402


DEFAULT_NAME = "Novality_Store_Home_Renovation_System.xlsx"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / DEFAULT_NAME,
        help="Output .xlsx path",
    )
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)

    wb = build_workbook()
    wb.save(args.out)
    print(f"Wrote {args.out}  ({args.out.stat().st_size:,} bytes)")
    print(f"Sheets ({len(wb.sheetnames)}): {', '.join(wb.sheetnames)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
