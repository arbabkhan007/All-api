# Make this a Google Sheet

The `.xlsx` **is** the Google Sheet. Google Sheets opens Excel files with formulas, colors, charts, filters, and dropdowns intact.

```
Google Drive
   └─ upload Hearth_and_Timber_Home_Renovation_System.xlsx
         └─ Open with Google Sheets
               └─ File → Save as Google Sheets
                     └─ share with designer / GC / trades
```

## Recommended share settings

| Person | Access |
|---|---|
| You (homeowner) | Editor |
| Project manager / designer | Editor |
| Contractor / supplier | Commenter (they should not edit Budget formulas) |
| Accountant | Viewer or Editor on Expenses / Payments only (use a filter view) |

Point everyone at **Dashboard**. Change **Settings → Active Project ID** (`PRJ-001` Maplewood, `PRJ-002` cabin) to switch homes.

## Optional: the Hearth & Timber menu

Follow [`google_apps_script/README.md`](google_apps_script/README.md) to add “Add expense”, maintenance emails, and overdue highlighting.

## Keep an Excel copy

**File → Download → Microsoft Excel (.xlsx)** any time. The generator (`python generate_workbook.py`) rebuilds a clean template from `hrms/data.py` if you want to start over.
