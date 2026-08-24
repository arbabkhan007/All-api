# Novality Store — Home Renovation Management System

A complete renovation operating system in a single workbook. It opens in **Microsoft Excel** and **Google Sheets**.

Every room, material, contractor, expense, document, task, photo, warranty and maintenance activity is tied to a place in the house — a **digital twin of the home**, not a generic construction tracker.

![Brand](https://img.shields.io/badge/Primary-%2316352F-16352F) ![Sand](https://img.shields.io/badge/Sand-%23E8DDCB-E8DDCB) ![Terracotta](https://img.shields.io/badge/Accent-%23C86B4A-C86B4A)

---

## Open it now

| What | Where |
|---|---|
| **Excel / Google Sheets workbook** | [`Novality_Store_Home_Renovation_System.xlsx`](Novality_Store_Home_Renovation_System.xlsx) |
| **Google Sheets companion** | [`google_apps_script/Code.gs`](google_apps_script/Code.gs) |
| **Regenerate** | `python generate_workbook.py` |

### Excel
1. Open the `.xlsx`. Enable editing.
2. Confirm **Formulas → Calculation Options → Automatic**.
3. Start on **Start Here**, then **Dashboard**.

### Google Sheets (this *is* the Google Sheet)
1. Upload the `.xlsx` to [Google Drive](https://drive.google.com).
2. Right-click → **Open with → Google Sheets**.
3. **File → Save as Google Sheets** (keeps formulas, colors, charts, dropdowns).
4. Optional but recommended: **Extensions → Apps Script** → paste `google_apps_script/Code.gs` → Save → reload.
5. A **Novality Store** menu appears: add expenses/tasks, highlight overdue work, email maintenance reminders.

Share the Google Sheet with your designer, GC, and trades. Use **Commenter** for contractors who should not edit budget cells.

---

## What is in the file

**35 sheets**, live formulas, dropdowns, conditional color, Gantt, charts, and a loaded sample project (24 August 2026).

### Homeowner
| Sheet | Role |
|---|---|
| **Start Here** | How to use Excel + Google Sheets, color system, clickable module index |
| **Dashboard** | Progress, budget / spent / committed / remaining, alerts, next tasks, rooms, visits, AI insight, nav |
| **Projects** | Multi-project register. Spent and committed roll up from Expenses |
| **Rooms** | Kitchen, living, bath, bedroom, dining, exterior, laundry, entry — area, budget, style, photos |
| **Design Studio** | Mood boards, palettes, materials, furniture, 2D/3D, AI concepts, style presets |
| **AI Insights** | Budget overruns, material swaps, schedule risk, bid comparison, photo notes, completion prediction |

### Money
| Sheet | Role |
|---|---|
| **Budget** | Category + room plan. Spent / committed / remaining / variance / alert are formulas |
| **Expenses** | Planned · Committed · Paid ledger |
| **Finance** | KPI cards, cost by category, cost by room, monthly cash, pie / bar / line charts, smart alerts |
| **Payments** | Draws, wires, aging |
| **Change Orders** | Scope, cost (negative = savings), schedule impact |

### People & work
| Sheet | Role |
|---|---|
| **Contractors** | Trade, insurance, license, portfolio. **Score** = average of Quality / On-time / Budget / Communication |
| **Quotes** | Request → receive → compare → award |
| **Jobs** | Assignments, milestones, balance, % paid |
| **Tasks** | Kanban statuses, priority, dependencies, days left, health |
| **Timeline** | Phase schedule + **weekly Gantt** (Mar–Nov 2026). Gold header = this week |
| **Users** | Homeowner, Admin, PM, Designer, Contractor, Subcontractor, Supplier, Inspector, Accountant |
| **Roles & Permissions** | F / E / V / A / — matrix for every module |

### Buy, file, talk
| Sheet | Role |
|---|---|
| **Materials** | SKU, qty, supplier, warranty, QR, procurement pipeline |
| **Shopping List** | `FILTER` of anything still Required / Quoted / Approved |
| **Suppliers** | Lead times and terms |
| **Documents** | Vault + signature flag + expiry alert |
| **Messages** | Threads pinned to a room or task, @mentions, unread |
| **Inspections** | City + independent |
| **Permits** | Authority, fees, expiration |
| **Warranties** | Labor and product coverage after handover |

### Aftercare
| Sheet | Role |
|---|---|
| **Inventory** | Everything in the house (serial, warranty end, replacement value) |
| **Maintenance** | HVAC, roof, pest, water, radiant, appliances — due-soon / overdue flags |
| **Calendar** | Visits, deliveries, inspections, holds |
| **Notifications** | In-app / email / SMS queue |

### System
| Sheet | Role |
|---|---|
| **Properties** | Multi-home (Maplewood + Gorge cabin) |
| **Admin** | Portfolio KPIs: homeowners, active projects, value, delays, disputes |
| **Settings** | Active project, currency, contingency %, alert thresholds, brand tokens |
| **Lookups** | Every dropdown list. Add values downward — do not delete the sheet |
| **Audit Log** | Who changed what |

---

## Sample story (already loaded)

**Alex Rivera** is renovating **1847 Maplewood Drive, Portland** (`PRJ-001`).

| | |
|---|---|
| Budget | **$85,000** |
| Phase | Construction · **72%** complete |
| As-of date | **24 August 2026** |
| Kitchen | Boxes landing this week. Island swapping marble → porcelain (AI save ~18% on that category) |
| Primary bath | Punch list. Already under budget after the porcelain swap |
| Contingency | Below the 10% floor — exterior water feature is on hold |
| Second home | Columbia Gorge cabin bath (`PRJ-002`) in design, so multi-property is visible |

Ivory cells are **unlocked inputs**. Sand-grey cells are **locked formulas**.

**Author:** `premium`  
**Unprotect password:** `premium`  
Review → Unprotect Sheet → `premium` if you must edit a formula. Re-protect after.

---

## Color system

| Token | Hex | Use |
|---|---|---|
| Deep Forest | `#16352F` | Headers, primary actions |
| Warm Sand | `#E8DDCB` | Banners, secondary |
| Terracotta | `#C86B4A` | Accents, in-progress, CTAs |
| Soft Ivory | `#F8F6F1` | Sheet background |
| Sage | `#719B7A` | Success, complete, under budget |
| Amber | `#D99A3D` | Watch, due soon |
| Muted red | `#C75C5C` | Over, overdue, critical |

This is an interior-design studio palette, not a blue corporate dashboard.

---

## How the numbers stay honest

All money and status math is ordinary Excel / Google Sheets formulas (no VBA, no Power Query):

- **Projects!Spent** = `SUMIFS` of Expenses where Status = Paid
- **Projects!Committed** = `SUMIFS` where Status = Committed
- **Rooms** roll up the same way by Room ID
- **Budget variance %** and **Alert** (On Track / Watch / Over / Under) use the overrun threshold on Settings
- **Contractor Score** = `AVERAGE(Quality, On-time, Budget, Communication)`
- **Task Health** = Done / On Track / Due Soon / Overdue vs `AsOfDate`
- **Document / permit / warranty** expiry flags use `AsOfDate`
- **Inventory warranty end** = `EDATE(purchase, years*12)`
- **Shopping List** = `FILTER` of Materials still Required / Quoted / Approved
- **Dashboard** and **Finance** read `ActiveProject` from Settings

Change **Settings → Active Project ID** to `PRJ-002` and the homeowner dashboard switches homes.

Named ranges used by formulas: `ActiveProject`, `HomeownerName`, `AsOfDate`, `ContingencyPct`, `ContingencyFloor`, `OverrunAlert`, `CompanyName`, `TaxRate`, plus one named range per Lookups column.

---

## Google Sheets menu (after installing the script)

| Command | What it does |
|---|---|
| Open homeowner dashboard | Jumps to Dashboard |
| Add expense / task / material / message | Prompts, writes a new ID'd row on the right sheet |
| Refresh shopping list | Activates the FILTER sheet |
| Highlight overdue tasks | Paints Tasks!Health |
| Build this-week calendar view | Dialog of the next 7 days |
| Email maintenance reminders | Mails due / overdue lines to you |
| Email unread messages digest | Mails unread threads to you |

---

## Rebuild the workbook

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python generate_workbook.py
```

Output: `Novality_Store_Home_Renovation_System.xlsx`

Edit sample data in `hrms/data.py`, styles in `hrms/styles.py`, sheet layout in `hrms/workbook.py`.

---

## MVP vs later (mapped to the sheets)

**Phase 1 — already here:** Dashboard, Projects, Rooms, Tasks, Budget, Contractors, Materials, Documents, Messages, Notifications.

**Phase 2 — already here as registers:** Design Studio, mood boards, procurement pipeline, Quotes, digital-contract flags, Payments, Finance reporting.

**Phase 3 — structured so a product can sit on top:** AI Insights, photo-analysis notes, before/after concepts, budget/time prediction, post-renovation Maintenance, Inventory (the digital twin). AR visualization is a mobile client; the material / finish rows it would preview are already in Design Studio and Materials.

---

## Roles

Homeowner · Admin · Project Manager · Interior Designer · Contractor · Subcontractor · Supplier · Inspector · Accountant

See **Roles & Permissions** for the access matrix the live product should enforce.

---

Novality Store  ·  Forest, sand, terracotta  ·  A digital twin of the home
