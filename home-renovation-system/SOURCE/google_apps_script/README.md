# Google Sheets companion

Turn the Excel workbook into a live Google Sheet with a **Novality Store** menu.

## 5 minutes

1. Upload `Novality_Store_Home_Renovation_System.xlsx` to [Google Drive](https://drive.google.com).
2. Right-click → **Open with → Google Sheets**.
3. **File → Save as Google Sheets**.
4. **Extensions → Apps Script**.
5. Delete the stub `myFunction` and paste [`Code.gs`](Code.gs). Save (Ctrl/Cmd+S).
6. Close the script editor and **reload the spreadsheet**.
7. Allow permissions the first time you run a menu item that sends email.

You now have a Google Sheet with every module, live formulas, and:

| Menu | Action |
|---|---|
| Open homeowner dashboard | Jump to Dashboard |
| Add expense / task / material / message | Prompt → new ID'd row |
| Refresh shopping list | Opens the FILTER sheet |
| Highlight overdue tasks | Colors Tasks health |
| Build this-week calendar view | Next 7 days |
| Email maintenance reminders | Due / overdue lines to you |
| Email unread messages digest | Unread threads to you |

`appsscript.json` declares the two scopes the script needs (this spreadsheet + Gmail send). If you paste only `Code.gs`, Apps Script will still prompt for those scopes on first run.
