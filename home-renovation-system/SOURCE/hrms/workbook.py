"""Build the Home Renovation Management System workbook.

Sheets are Excel- and Google-Sheets-compatible: no VBA, no structured table
references, formulas use ordinary ranges (SUMIFS, COUNTIFS, INDEX/MATCH, IFERROR).
"""

from __future__ import annotations

from datetime import date, datetime, timedelta

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.series import DataPoint
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.fill import ColorChoice, PatternFillProperties
from openpyxl.formatting.rule import (
    CellIsRule,
    ColorScaleRule,
    FormulaRule,
    IconSetRule,
)
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart.marker import Marker
from openpyxl.chart.legend import Legend
from openpyxl.worksheet.hyperlink import Hyperlink

from . import data as D
from .styles import (
    ACCENT,
    BG,
    CUR,
    CUR2,
    DANGER,
    DANGER_SOFT,
    DATE,
    DEC1,
    FORMULA_BG,
    GANTT,
    GANTT_DONE,
    GANTT_NOW,
    INFO,
    INFO_SOFT,
    INPUT_BG,
    INT,
    PCT,
    PCT1,
    PRIMARY,
    PRIMARY_MID,
    PRIMARY_SOFT,
    ROW_ALT,
    SECONDARY,
    SECONDARY_DEEP,
    SUCCESS,
    SUCCESS_SOFT,
    TEXT,
    TEXT_MUTED,
    WARNING,
    WARNING_SOFT,
    WHITE,
    align,
    apply_cell,
    auto_filter,
    banner,
    fill,
    font,
    freeze,
    header_row,
    hide_grid,
    input_note,
    ivory_sheet,
    kpi_card,
    page_setup,
    paint_range,
    section_label,
    set_col_widths,
    status_fill,
    style_data_row,
    THIN,
    NONE,
)


TODAY = D.TODAY
LAST_DATA = 500  # generous formula range so new rows keep working


def _is_date(v):
    return isinstance(v, (date, datetime)) and not isinstance(v, datetime) or (
        isinstance(v, date) and not isinstance(v, datetime)
    )


def _write_headers(ws, headers, row=4):
    header_row(ws, row, headers)
    return row


def _write_rows(ws, rows, start_row, ncols, date_cols=None, money_cols=None, pct_cols=None):
    date_cols = set(date_cols or [])
    money_cols = set(money_cols or [])
    pct_cols = set(pct_cols or [])
    for i, row in enumerate(rows):
        r = start_row + i
        style_data_row(ws, r, ncols, alt=i % 2 == 1)
        for c, val in enumerate(row, 1):
            cell = ws.cell(r, c, val)
            cell.fill = fill(ROW_ALT if i % 2 else WHITE)
            cell.font = font(10)
            cell.alignment = align("left", "center", wrap=c in (5, 6, 7, 11, 12, 16, 17))
            cell.border = THIN
            if c in date_cols:
                cell.number_format = DATE
            if c in money_cols:
                cell.number_format = CUR
            if c in pct_cols:
                cell.number_format = PCT
    return start_row + len(rows) - 1


def _dv_list(ws, formula, cells, allow_blank=True):
    dv = DataValidation(
        type="list",
        formula1=formula,
        allow_blank=allow_blank,
        showDropDown=False,
        showErrorMessage=True,
        errorTitle="Invalid value",
        error="Pick a value from the list.",
    )
    dv.add(cells)
    ws.add_data_validation(dv)
    return dv


def _status_cf(ws, col_letter, start, end, values):
    for value, color in values.items():
        ws.conditional_formatting.add(
            f"{col_letter}{start}:{col_letter}{end}",
            FormulaRule(
                formula=[f'{col_letter}{start}="{value}"'],
                fill=fill(color),
                font=font(10, True, WHITE if color in (PRIMARY, ACCENT, DANGER, INFO) else TEXT),
            ),
        )


def _sheet(wb, title, tab, last_col=14, subtitle=""):
    ws = wb.create_sheet(title)
    hide_grid(ws)
    ivory_sheet(ws, 8, last_col)
    banner(ws, title.upper(), subtitle or "Novality Store  ·  digital twin of the home", last_col, tab)
    page_setup(ws, title)
    ws.sheet_view.showGridLines = False
    return ws


def _link(cell, target, text=None):
    cell.value = text or target
    cell.hyperlink = target
    cell.font = font(10, False, ACCENT)
    cell.style = "Hyperlink"


# ===========================================================================
# LOOKUPS
# ===========================================================================
def build_lookups(wb):
    ws = _sheet(wb, "Lookups", PRIMARY_SOFT, 28, "Dropdown sources  ·  do not delete  ·  add values downward")
    col = 1
    named = {}
    for name, values in D.LOOKUPS.items():
        ws.cell(4, col, name.replace("_", " "))
        ws.cell(4, col).font = font(9, True, WHITE)
        ws.cell(4, col).fill = fill(PRIMARY)
        ws.cell(4, col).alignment = align("center", "center")
        for i, v in enumerate(values):
            cell = ws.cell(5 + i, col, v)
            cell.font = font(10)
            cell.fill = fill(WHITE if i % 2 == 0 else ROW_ALT)
            cell.border = THIN
        last = 4 + len(values)
        letter = get_column_letter(col)
        # Named range for data validation
        defn = DefinedName(name=name, attr_text=f"Lookups!${letter}$5:${letter}${last}")
        wb.defined_names.add(defn)
        named[name] = f"Lookups!${letter}$5:${letter}${last}"
        col += 1
    set_col_widths(ws, [18] * col)
    freeze(ws, "A5")
    input_note(ws, 3, 1, "These lists power every dropdown in the workbook. Add new items in the first empty cell of a column.", 12)
    ws.row_dimensions[3].height = 18
    return ws, named


# ===========================================================================
# SETTINGS
# ===========================================================================
def build_settings(wb):
    ws = _sheet(wb, "Settings", PRIMARY, 6, "Company, currency, thresholds  ·  change values in column B")
    headers = ["Setting", "Value", "Notes"]
    header_row(ws, 4, headers)
    notes = {
        "Contingency %": "Used by Finance + alerts. Default 10%.",
        "Today (system)": "Dashboard 'today'. Update if you archive this file later.",
        "Active Project ID": "Default filter for dashboard KPIs.",
        "Low Contingency Threshold": "Alert when remaining contingency / budget < this.",
        "Budget Overrun Alert %": "Room/category alert when spent+committed exceeds planned by this.",
        "Tax Rate": "Optional. Applied on Finance tax line if > 0.",
        "Currency": "USD formulas use $ format; change display only.",
    }
    for i, (k, v) in enumerate(D.SETTINGS):
        r = 5 + i
        style_data_row(ws, r, 3, alt=i % 2)
        ws.cell(r, 1, k).font = font(10, True, PRIMARY)
        ws.cell(r, 2, v)
        ws.cell(r, 2).fill = fill(INPUT_BG)
        if isinstance(v, float) and v <= 1:
            ws.cell(r, 2).number_format = PCT
        elif isinstance(v, date):
            ws.cell(r, 2).number_format = DATE
        ws.cell(r, 3, notes.get(k, ""))
        ws.cell(r, 3).font = font(9, False, TEXT_MUTED)
    set_col_widths(ws, [34, 28, 64])
    freeze(ws, "A5")
    # Named cells
    key_map = {k: 5 + i for i, (k, _) in enumerate(D.SETTINGS)}
    for key, name in [
        ("Active Project ID", "ActiveProject"),
        ("Homeowner", "HomeownerName"),
        ("Currency Symbol", "CurSym"),
        ("Contingency %", "ContingencyPct"),
        ("Today (system)", "AsOfDate"),
        ("Low Contingency Threshold", "ContingencyFloor"),
        ("Budget Overrun Alert %", "OverrunAlert"),
        ("Company Name", "CompanyName"),
        ("Tax Rate", "TaxRate"),
    ]:
        row = key_map[key]
        wb.defined_names.add(DefinedName(name=name, attr_text=f"Settings!$B${row}"))
    _dv_list(ws, "=Currency", "B11")
    _dv_list(ws, "=Language", "B13")
    return ws


# ===========================================================================
# Generic list sheet
# ===========================================================================
def build_list_sheet(
    wb,
    title,
    tab,
    subtitle,
    headers,
    rows,
    widths,
    date_cols=None,
    money_cols=None,
    pct_cols=None,
    extra_formulas=None,
    validations=None,
    status_col=None,
    status_map=None,
    last_col=None,
):
    ncols = last_col or len(headers)
    ws = _sheet(wb, title, tab, ncols, subtitle)
    _write_headers(ws, headers, 4)
    last = _write_rows(ws, rows, 5, len(headers), date_cols, money_cols, pct_cols)
    if extra_formulas:
        extra_formulas(ws, 5, last)
    auto_filter(ws, 4, len(headers), max(last, 5))
    freeze(ws, "A5")
    set_col_widths(ws, widths)
    if validations:
        for formula, cells in validations:
            _dv_list(ws, formula, cells)
    if status_col and status_map:
        letter = get_column_letter(status_col)
        _status_cf(ws, letter, 5, max(last, 80), status_map)
    # tint input cells lightly
    return ws, last


# ===========================================================================
# PROPERTIES / USERS / PROJECTS / ROOMS
# ===========================================================================
def build_properties(wb):
    return build_list_sheet(
        wb, "Properties", PRIMARY_MID, "Multi-property digital twin  ·  one row per home",
        D.HEADERS["Properties"], D.PROPERTIES,
        [14, 24, 24, 14, 8, 10, 10, 14, 12, 10, 10, 8, 8, 16, 14, 20, 14, 46],
        date_cols=[], money_cols=[],
        validations=[("=Property_Type", "H5:H80")],
    )


def build_users(wb):
    return build_list_sheet(
        wb, "Users", PRIMARY_SOFT, "Nine roles  ·  each role sees a different dashboard in the product",
        D.HEADERS["Users"], D.USERS,
        [12, 18, 36, 18, 18, 24, 12, 14, 44],
        date_cols=[8],
        validations=[("=Role", "E5:E80")],
        status_col=7,
        status_map={"Active": SUCCESS, "Inactive": TEXT_MUTED},
    )


def build_projects(wb):
    headers = D.HEADERS["Projects"] + ["Spent", "Committed", "Remaining", "Health"]
    # raw rows without computed cols
    raw = [r[:] for r in D.PROJECTS]
    ws, last = build_list_sheet(
        wb, "Projects", ACCENT, "All renovation projects  ·  spent/committed roll up from Expenses",
        headers, [r + [None, None, None, None] for r in raw],
        [12, 12, 32, 14, 12, 14, 12, 12, 12, 12, 12, 12, 12, 16, 36, 10, 40, 12, 12, 12, 14],
        date_cols=[7, 8, 9], money_cols=[10, 18, 19, 20], pct_cols=[16],
        validations=[
            ("=Project_Status", "E5:E80"),
            ("=Project_Phase", "F5:F80"),
        ],
        status_col=5,
        status_map={"Active": SUCCESS, "Planning": INFO, "On Hold": WARNING, "Completed": PRIMARY, "Cancelled": DANGER},
        last_col=21,
    )
    # formulas for spent / committed / remaining / health
    for r in range(5, last + 1):
        # Spent = paid expenses
        ws.cell(r, 18).value = f'=IF($A{r}="","",SUMIFS(Expenses!$H:$H,Expenses!$C:$C,$A{r},Expenses!$J:$J,"Paid"))'
        ws.cell(r, 18).number_format = CUR
        ws.cell(r, 18).fill = fill(FORMULA_BG)
        ws.cell(r, 19).value = f'=IF($A{r}="","",SUMIFS(Expenses!$H:$H,Expenses!$C:$C,$A{r},Expenses!$J:$J,"Committed"))'
        ws.cell(r, 19).number_format = CUR
        ws.cell(r, 19).fill = fill(FORMULA_BG)
        ws.cell(r, 20).value = f'=IF($A{r}="","",$J{r}-$R{r}-$S{r})'
        ws.cell(r, 20).number_format = CUR
        ws.cell(r, 20).fill = fill(FORMULA_BG)
        ws.cell(r, 21).value = (
            f'=IF($A{r}="","",IF($R{r}+$S{r}>$J{r}*(1+OverrunAlert),"Over",'
            f'IF($R{r}+$S{r}>$J{r},"Watch","On Track")))'
        )
        ws.cell(r, 21).fill = fill(FORMULA_BG)
        for c in range(18, 22):
            ws.cell(r, c).font = font(10)
            ws.cell(r, c).border = THIN
            ws.cell(r, c).alignment = align("center", "center")
    ws.conditional_formatting.add(
        f"U5:U{max(last, 80)}",
        FormulaRule(formula=['U5="On Track"'], fill=fill(SUCCESS_SOFT), font=font(10, True, SUCCESS)),
    )
    ws.conditional_formatting.add(
        f"U5:U{max(last, 80)}",
        FormulaRule(formula=['U5="Watch"'], fill=fill(WARNING_SOFT), font=font(10, True, WARNING)),
    )
    ws.conditional_formatting.add(
        f"U5:U{max(last, 80)}",
        FormulaRule(formula=['U5="Over"'], fill=fill(DANGER_SOFT), font=font(10, True, DANGER)),
    )
    ws.conditional_formatting.add(
        f"P5:P{max(last, 80)}",
        ColorScaleRule(start_type="num", start_value=0, start_color=SECONDARY,
                       mid_type="num", mid_value=0.5, mid_color=WARNING,
                       end_type="num", end_value=1, end_color=SUCCESS),
    )
    return ws, last


def build_rooms(wb):
    headers = D.HEADERS["Rooms"] + ["Area (sf)", "Spent", "Committed", "Remaining", "Budget used"]
    raw = [r[:] for r in D.ROOMS]
    ws, last = build_list_sheet(
        wb, "Rooms", PRIMARY_MID, "Every space is a node in the digital twin",
        headers, [r + [None, None, None, None, None] for r in raw],
        [10, 12, 20, 18, 8, 12, 12, 12, 12, 14, 12, 12, 14, 26, 26, 40, 12, 12, 12, 12, 12],
        money_cols=[11, 18, 19, 20], pct_cols=[21],
        validations=[
            ("=Room_Type", "D5:D80"),
            ("=Room_Status", "J5:J80"),
            ("=Design_Style", "M5:M80"),
        ],
        status_col=10,
        status_map={
            "Not Started": TEXT_MUTED,
            "Design": INFO,
            "In Progress": ACCENT,
            "Punch List": WARNING,
            "Complete": SUCCESS,
        },
        last_col=21,
    )
    for r in range(5, last + 1):
        ws.cell(r, 17).value = f'=IF($A{r}="","",ROUND($F{r}*$G{r},1))'
        ws.cell(r, 17).number_format = DEC1
        ws.cell(r, 18).value = f'=IF($A{r}="","",SUMIFS(Expenses!$H:$H,Expenses!$D:$D,$A{r},Expenses!$J:$J,"Paid"))'
        ws.cell(r, 18).number_format = CUR
        ws.cell(r, 19).value = f'=IF($A{r}="","",SUMIFS(Expenses!$H:$H,Expenses!$D:$D,$A{r},Expenses!$J:$J,"Committed"))'
        ws.cell(r, 19).number_format = CUR
        ws.cell(r, 20).value = f'=IF($A{r}="","",$K{r}-$R{r}-$S{r})'
        ws.cell(r, 20).number_format = CUR
        ws.cell(r, 21).value = f'=IF(OR($A{r}="",$K{r}=0),"",($R{r}+$S{r})/$K{r})'
        ws.cell(r, 21).number_format = PCT1
        for c in range(17, 22):
            ws.cell(r, c).fill = fill(FORMULA_BG)
            ws.cell(r, c).border = THIN
            ws.cell(r, c).font = font(10)
    ws.conditional_formatting.add(
        f"U5:U{max(last, 80)}",
        ColorScaleRule(start_type="num", start_value=0, start_color=SUCCESS,
                       mid_type="num", mid_value=0.9, mid_color=WARNING,
                       end_type="num", end_value=1.2, end_color=DANGER),
    )
    return ws, last


# ===========================================================================
# DESIGN / AI
# ===========================================================================
def build_design(wb):
    return build_list_sheet(
        wb, "Design Studio", ACCENT,
        "Mood boards, palettes, materials, 2D/3D, AI concepts  ·  style presets included",
        D.HEADERS["Design Studio"], D.DESIGNS,
        [12, 12, 10, 16, 32, 14, 16, 12, 28, 12, 12, 12, 44],
        money_cols=[11],
        validations=[
            ("=Design_Item", "D5:D80"),
            ("=Design_Style", "F5:F80"),
        ],
    )


def build_ai(wb):
    ws, last = build_list_sheet(
        wb, "AI Insights", INFO,
        "Renovation assistant  ·  budget, materials, schedule, contractor comparison, photo analysis",
        D.HEADERS["AI Insights"], D.AI_INSIGHTS,
        [12, 12, 12, 10, 14, 12, 56, 64, 14, 14, 36],
        date_cols=[2], money_cols=[9],
        validations=[
            ("=Insight_Severity", "F5:F80"),
            ("=Insight_Status", "J5:J80"),
        ],
        status_col=6,
        status_map={"Info": INFO, "Opportunity": SUCCESS, "Warning": WARNING, "Critical": DANGER},
    )
    _status_cf(ws, "J", 5, max(last, 80), {
        "New": INFO, "Accepted": SUCCESS, "In Progress": ACCENT, "Dismissed": TEXT_MUTED, "Resolved": PRIMARY,
    })
    return ws, last


# ===========================================================================
# BUDGET / EXPENSES / FINANCE
# ===========================================================================
def build_budget(wb):
    headers = D.HEADERS["Budget"]
    # planned only in source; rest formulas
    planned_rows = [r + [None] * 6 for r in D.BUDGET]
    ws, last = build_list_sheet(
        wb, "Budget", SUCCESS,
        "Category + room budgets  ·  spent/committed live from Expenses",
        headers, planned_rows,
        [12, 12, 10, 14, 32, 12, 14, 12, 12, 12, 12, 14],
        money_cols=[6, 7, 8, 9, 10], pct_cols=[11],
        validations=[("=Budget_Category", "D5:D200")],
        last_col=12,
    )
    for r in range(5, last + 1):
        # Spent: match project + category + subcategory via SUMIFS on description? 
        # Better: match Project + Category, and if Room ID present also room.
        # Subcategory is more precise — we match Project+Category+Room (room may be blank).
        ws.cell(r, 7).value = (
            f'=IF($A{r}="","",IF($C{r}="",'
            f'SUMIFS(Expenses!$H:$H,Expenses!$C:$C,$B{r},Expenses!$E:$E,$D{r},Expenses!$J:$J,"Paid"),'
            f'SUMIFS(Expenses!$H:$H,Expenses!$C:$C,$B{r},Expenses!$D:$D,$C{r},Expenses!$E:$E,$D{r},Expenses!$J:$J,"Paid")))'
        )
        ws.cell(r, 8).value = (
            f'=IF($A{r}="","",IF($C{r}="",'
            f'SUMIFS(Expenses!$H:$H,Expenses!$C:$C,$B{r},Expenses!$E:$E,$D{r},Expenses!$J:$J,"Committed"),'
            f'SUMIFS(Expenses!$H:$H,Expenses!$C:$C,$B{r},Expenses!$D:$D,$C{r},Expenses!$E:$E,$D{r},Expenses!$J:$J,"Committed")))'
        )
        ws.cell(r, 9).value = f'=IF($A{r}="","",$F{r}-$G{r}-$H{r})'
        ws.cell(r, 10).value = f'=IF($A{r}="","",$F{r}-($G{r}+$H{r}))'
        ws.cell(r, 11).value = f'=IF(OR($A{r}="",$F{r}=0),"",($G{r}+$H{r}-$F{r})/$F{r})'
        ws.cell(r, 12).value = (
            f'=IF($A{r}="","",IF($F{r}=0,"",'
            f'IF(($G{r}+$H{r})>$F{r}*(1+OverrunAlert),"Over",'
            f'IF(($G{r}+$H{r})>$F{r},"Watch",'
            f'IF(($G{r}+$H{r})<$F{r}*0.85,"Under","On Track")))))'
        )
        for c in range(7, 13):
            ws.cell(r, c).fill = fill(FORMULA_BG)
            ws.cell(r, c).border = THIN
            ws.cell(r, c).font = font(10)
            if c <= 10:
                ws.cell(r, c).number_format = CUR
            if c == 11:
                ws.cell(r, c).number_format = PCT1
        ws.cell(r, 6).fill = fill(INPUT_BG)
        ws.cell(r, 6).number_format = CUR
    _status_cf(ws, "L", 5, max(last, 200), {
        "On Track": SUCCESS, "Under": INFO, "Watch": WARNING, "Over": DANGER,
    })
    # totals row
    t = last + 2
    ws.cell(t, 5, "TOTAL (all lines)").font = font(11, True, WHITE)
    ws.cell(t, 6, f"=SUM(F5:F{last})").number_format = CUR
    ws.cell(t, 7, f"=SUM(G5:G{last})").number_format = CUR
    ws.cell(t, 8, f"=SUM(H5:H{last})").number_format = CUR
    ws.cell(t, 9, f"=SUM(I5:I{last})").number_format = CUR
    ws.cell(t, 10, f"=F{t}-G{t}-H{t}").number_format = CUR
    for c in range(5, 11):
        ws.cell(t, c).fill = fill(PRIMARY)
        ws.cell(t, c).font = font(11, True, WHITE)
        ws.cell(t, c).border = THIN
    return ws, last


def build_expenses(wb):
    ws, last = build_list_sheet(
        wb, "Expenses", ACCENT,
        "Every dollar  ·  Planned / Committed / Paid  ·  add rows below, keep Status valid",
        D.HEADERS["Expenses"], D.EXPENSES,
        [12, 12, 12, 10, 14, 24, 36, 12, 14, 12, 16, 16],
        date_cols=[2], money_cols=[8],
        validations=[
            ("=Budget_Category", "E5:E500"),
            ("=Payment_Method", "I5:I500"),
            ("=Expense_Status", "J5:J500"),
        ],
        status_col=10,
        status_map={"Paid": SUCCESS, "Committed": WARNING, "Planned": INFO, "Void": TEXT_MUTED},
    )
    # highlight amount
    ws.conditional_formatting.add(
        f"H5:H{max(last, 200)}",
        ColorScaleRule(start_type="min", start_color="F8F6F1",
                       mid_type="percentile", mid_value=50, mid_color="E8B09A",
                       end_type="max", end_color="C86B4A"),
    )
    return ws, last


def build_finance(wb):
    ws = _sheet(wb, "Finance", SUCCESS, 14,
                "Financial dashboard  ·  planned vs actual, by room, by category, by month")
    # KPI row
    kpi_card(ws, 5, 1, "BUDGET (active project)",
             '=IFERROR(SUMIF(Projects!A:A,ActiveProject,Projects!J:J),0)',
             "Total planned", PRIMARY, 2)
    ws["A6"].number_format = CUR
    kpi_card(ws, 5, 4, "SPENT",
             '=IFERROR(SUMIFS(Expenses!H:H,Expenses!C:C,ActiveProject,Expenses!J:J,"Paid"),0)',
             "Paid to date", ACCENT, 2)
    ws["D6"].number_format = CUR
    kpi_card(ws, 5, 7, "COMMITTED",
             '=IFERROR(SUMIFS(Expenses!H:H,Expenses!C:C,ActiveProject,Expenses!J:J,"Committed"),0)',
             "Approved, not yet paid", WARNING, 2)
    ws["G6"].number_format = CUR
    kpi_card(ws, 5, 10, "REMAINING",
             "=A6-D6-G6",
             "Budget − spent − committed", SUCCESS, 2)
    ws["J6"].number_format = CUR

    kpi_card(ws, 9, 1, "% USED",
             '=IFERROR((D6+G6)/A6,0)',
             "Spent + committed", ACCENT, 2)
    ws["A10"].number_format = PCT1
    kpi_card(ws, 9, 4, "CONTINGENCY LEFT",
             '=IFERROR(SUMIFS(Budget!I:I,Budget!B:B,ActiveProject,Budget!D:D,"Contingency"),0)',
             "Watch the 10% floor", WARNING, 2)
    ws["D10"].number_format = CUR
    kpi_card(ws, 9, 7, "THIS MONTH SPENT",
             '=SUMIFS(Expenses!H:H,Expenses!C:C,ActiveProject,Expenses!J:J,"Paid",Expenses!B:B,">="&DATE(YEAR(AsOfDate),MONTH(AsOfDate),1),Expenses!B:B,"<"&DATE(YEAR(AsOfDate),MONTH(AsOfDate)+1,1))',
             "Paid in current month", PRIMARY, 2)
    ws["G10"].number_format = CUR
    kpi_card(ws, 9, 10, "HEALTH",
             '=IF((D6+G6)>A6*(1+OverrunAlert),"OVER",IF((D6+G6)>A6,"WATCH","ON TRACK"))',
             "Vs overrun threshold", SUCCESS, 2)

    # Category rollup
    section_label(ws, 13, 1, "Cost by category", 6)
    headers = ["Category", "Planned", "Spent", "Committed", "Remaining", "% Used"]
    for i, h in enumerate(headers, 1):
        cell = ws.cell(14, i, h)
        cell.font = font(10, True, WHITE)
        cell.fill = fill(PRIMARY)
        cell.alignment = align("center", "center")
        cell.border = THIN
    cats = D.LOOKUPS["Budget_Category"]
    for i, cat in enumerate(cats):
        r = 15 + i
        ws.cell(r, 1, cat).font = font(10, True, PRIMARY)
        ws.cell(r, 2, f'=SUMIFS(Budget!F:F,Budget!B:B,ActiveProject,Budget!D:D,A{r})')
        ws.cell(r, 3, f'=SUMIFS(Expenses!H:H,Expenses!C:C,ActiveProject,Expenses!E:E,A{r},Expenses!J:J,"Paid")')
        ws.cell(r, 4, f'=SUMIFS(Expenses!H:H,Expenses!C:C,ActiveProject,Expenses!E:E,A{r},Expenses!J:J,"Committed")')
        ws.cell(r, 5, f"=B{r}-C{r}-D{r}")
        ws.cell(r, 6, f'=IF(B{r}=0,"",(C{r}+D{r})/B{r})')
        for c in range(1, 7):
            ws.cell(r, c).fill = fill(WHITE if i % 2 == 0 else ROW_ALT)
            ws.cell(r, c).border = THIN
            ws.cell(r, c).font = font(10)
            if c in (2, 3, 4, 5):
                ws.cell(r, c).number_format = CUR
            if c == 6:
                ws.cell(r, c).number_format = PCT1
    last_cat = 14 + len(cats)

    # Room rollup
    section_label(ws, 13, 8, "Cost by room (active project)", 6)
    rh = ["Room", "Budget", "Spent", "Committed", "Remaining", "% Used"]
    for i, h in enumerate(rh, 8):
        cell = ws.cell(14, i, h)
        cell.font = font(10, True, WHITE)
        cell.fill = fill(PRIMARY)
        cell.alignment = align("center", "center")
        cell.border = THIN
    # pull first 12 rooms of active project via INDEX/MATCH is hard; list known rooms with SUMIF
    # Use Rooms sheet
    for i in range(12):
        r = 15 + i
        # Room name from Rooms where project = active, nth match approximated by listing Rooms!C
        ws.cell(r, 8, f'=IFERROR(INDEX(Rooms!$C:$C,SMALL(IF(Rooms!$B$5:$B$80=ActiveProject,ROW(Rooms!$B$5:$B$80)),{i+1})),"")')
        # Array formulas don't work the same in Excel without CSE; Google Sheets uses ARRAYFORMULA.
        # Safer: reference Rooms rows directly (rooms 5-16 are PRJ-001 mostly).
        # We'll fill static room IDs from data for reliability, formulas for money.
    # overwrite with reliable formulas using Rooms columns
    for i, room in enumerate(D.ROOMS):
        if room[1] != "PRJ-001":
            continue
        # find display index among PRJ-001
    prj_rooms = [rm for rm in D.ROOMS if rm[1] == "PRJ-001"]
    for i, rm in enumerate(prj_rooms):
        r = 15 + i
        ws.cell(r, 8, rm[2])
        rid = rm[0]
        ws.cell(r, 9, f'=SUMIF(Rooms!A:A,"{rid}",Rooms!K:K)')
        ws.cell(r, 10, f'=SUMIFS(Expenses!H:H,Expenses!D:D,"{rid}",Expenses!J:J,"Paid")')
        ws.cell(r, 11, f'=SUMIFS(Expenses!H:H,Expenses!D:D,"{rid}",Expenses!J:J,"Committed")')
        ws.cell(r, 12, f"=I{r}-J{r}-K{r}")
        ws.cell(r, 13, f'=IF(I{r}=0,"",(J{r}+K{r})/I{r})')
        for c in range(8, 14):
            ws.cell(r, c).fill = fill(WHITE if i % 2 == 0 else ROW_ALT)
            ws.cell(r, c).border = THIN
            ws.cell(r, c).font = font(10)
            if c in (9, 10, 11, 12):
                ws.cell(r, c).number_format = CUR
            if c == 13:
                ws.cell(r, c).number_format = PCT1
    last_room = 14 + len(prj_rooms)

    # Monthly spending Mar–Nov 2026
    section_label(ws, last_cat + 3, 1, "Monthly spending (paid)", 6)
    mrow = last_cat + 4
    months = [date(2026, m, 1) for m in range(3, 12)]
    ws.cell(mrow, 1, "Month").font = font(10, True, WHITE)
    ws.cell(mrow, 1).fill = fill(PRIMARY)
    ws.cell(mrow, 2, "Spent").font = font(10, True, WHITE)
    ws.cell(mrow, 2).fill = fill(PRIMARY)
    ws.cell(mrow, 3, "Committed dated").font = font(10, True, WHITE)
    ws.cell(mrow, 3).fill = fill(PRIMARY)
    ws.cell(mrow, 1).border = THIN
    ws.cell(mrow, 2).border = THIN
    ws.cell(mrow, 3).border = THIN
    for i, m in enumerate(months):
        r = mrow + 1 + i
        ws.cell(r, 1, m.strftime("%b %Y"))
        nxt = date(2026, m.month + 1, 1) if m.month < 12 else date(2027, 1, 1)
        ws.cell(r, 2, f'=SUMIFS(Expenses!H:H,Expenses!C:C,ActiveProject,Expenses!J:J,"Paid",Expenses!B:B,">="&DATE({m.year},{m.month},1),Expenses!B:B,"<"&DATE({nxt.year},{nxt.month},1))')
        ws.cell(r, 3, f'=SUMIFS(Expenses!H:H,Expenses!C:C,ActiveProject,Expenses!J:J,"Committed",Expenses!B:B,">="&DATE({m.year},{m.month},1),Expenses!B:B,"<"&DATE({nxt.year},{nxt.month},1))')
        ws.cell(r, 2).number_format = CUR
        ws.cell(r, 3).number_format = CUR
        for c in range(1, 4):
            ws.cell(r, c).fill = fill(WHITE if i % 2 == 0 else ROW_ALT)
            ws.cell(r, c).border = THIN
            ws.cell(r, c).font = font(10)
    last_m = mrow + len(months)

    # Charts
    pie = PieChart()
    pie.title = "Spent by category"
    labels = Reference(ws, min_col=1, min_row=15, max_row=last_cat)
    data = Reference(ws, min_col=3, min_row=14, max_row=last_cat)
    pie.add_data(data, titles_from_data=True)
    pie.set_categories(labels)
    pie.dataLabels = DataLabelList()
    pie.dataLabels.showPercent = True
    pie.dataLabels.showVal = False
    pie.dataLabels.showCatName = False
    pie.width = 12
    pie.height = 8
    ws.add_chart(pie, "A40")

    bar = BarChart()
    bar.type = "col"
    bar.grouping = "clustered"
    bar.title = "Planned vs spent vs committed by category"
    data = Reference(ws, min_col=2, min_row=14, max_col=4, max_row=last_cat)
    cats = Reference(ws, min_col=1, min_row=15, max_row=last_cat)
    bar.add_data(data, titles_from_data=True)
    bar.set_categories(cats)
    bar.shape = 4
    bar.width = 18
    bar.height = 8
    bar.y_axis.numFmt = CUR
    ws.add_chart(bar, "G40")

    line = LineChart()
    line.title = "Monthly cash out (paid)"
    data = Reference(ws, min_col=2, min_row=mrow, max_row=last_m)
    cats = Reference(ws, min_col=1, min_row=mrow + 1, max_row=last_m)
    line.add_data(data, titles_from_data=True)
    line.set_categories(cats)
    line.width = 18
    line.height = 7
    line.y_axis.numFmt = CUR
    line.style = 10
    ws.add_chart(line, "A58")

    # Smart alerts
    section_label(ws, 28, 8, "Smart alerts", 6)
    alerts = [
        (29, '=IF((D6+G6)>A6,"🔴 Project is over planned budget","🟢 Project within planned budget")'),
        (30, '=IF(D10<A6*ContingencyFloor,"🔴 Contingency has fallen below the threshold","🟢 Contingency healthy")'),
        (31, '=IFERROR(IF(SUMIFS(Rooms!R:R,Rooms!B:B,ActiveProject,Rooms!C:C,"Kitchen")+SUMIFS(Rooms!S:S,Rooms!B:B,ActiveProject,Rooms!C:C,"Kitchen")>SUMIFS(Rooms!K:K,Rooms!B:B,ActiveProject,Rooms!C:C,"Kitchen"),"⚠️ Kitchen is over its room budget","🟢 Kitchen within room budget"),"")'),
        (32, '=IFERROR(IF(SUMIFS(Rooms!R:R,Rooms!B:B,ActiveProject,Rooms!C:C,"Primary Bathroom")+SUMIFS(Rooms!S:S,Rooms!B:B,ActiveProject,Rooms!C:C,"Primary Bathroom")<SUMIFS(Rooms!K:K,Rooms!B:B,ActiveProject,Rooms!C:C,"Primary Bathroom"),"🟢 Primary bathroom is under budget","⚠️ Primary bathroom at or over budget"),"")'),
        (33, '="As of "&TEXT(AsOfDate,"YYYY-MM-DD")&"  ·  Active project "&ActiveProject'),
    ]
    for r, f in alerts:
        ws.merge_cells(start_row=r, start_column=8, end_row=r, end_column=13)
        ws.cell(r, 8, f)
        ws.cell(r, 8).font = font(10, False, TEXT)
        ws.cell(r, 8).alignment = align("left", "center", True)
        ws.cell(r, 8).fill = fill(WHITE)
        ws.row_dimensions[r].height = 18

    set_col_widths(ws, [22, 14, 14, 14, 14, 12, 14, 22, 14, 14, 14, 14, 12, 12])
    return ws


# ===========================================================================
# CONTRACTORS / QUOTES / JOBS
# ===========================================================================
def build_contractors(wb):
    headers = D.HEADERS["Contractors"]
    # Score is computed
    rows = []
    for r in D.CONTRACTORS:
        rows.append(r[:12] + [None] + r[12:])
    ws, last = build_list_sheet(
        wb, "Contractors", PRIMARY_MID,
        "Profiles, insurance, licenses  ·  Score = average of Quality / On-time / Budget / Communication",
        headers, rows,
        [12, 24, 16, 18, 28, 18, 32, 10, 10, 10, 10, 14, 10, 14, 14, 18, 12, 12, 24],
        date_cols=[14], pct_cols=[9, 10, 11, 12, 13], money_cols=[17],
        validations=[("=Trade", "D5:D80")],
        status_col=18,
        status_map={"Active": SUCCESS, "Inactive": TEXT_MUTED, "Do Not Use": DANGER},
    )
    for r in range(5, last + 1):
        ws.cell(r, 13).value = f'=IF($A{r}="","",AVERAGE(I{r}:L{r}))'
        ws.cell(r, 13).number_format = PCT
        ws.cell(r, 13).fill = fill(FORMULA_BG)
        ws.cell(r, 13).font = font(10, True, PRIMARY)
        ws.cell(r, 13).border = THIN
    ws.conditional_formatting.add(
        f"M5:M{max(last, 80)}",
        ColorScaleRule(start_type="num", start_value=0.7, start_color=DANGER,
                       mid_type="num", mid_value=0.88, mid_color=WARNING,
                       end_type="num", end_value=1, end_color=SUCCESS),
    )
    return ws, last


def build_quotes(wb):
    return build_list_sheet(
        wb, "Quotes", WARNING,
        "Request → receive → compare → award",
        D.HEADERS["Quotes"], D.QUOTES,
        [10, 12, 10, 12, 16, 52, 12, 14, 12, 12, 36],
        date_cols=[9], money_cols=[7],
        validations=[("=Quote_Status", "J5:J80"), ("=Trade", "E5:E80")],
        status_col=10,
        status_map={
            "Requested": TEXT_MUTED, "Received": INFO, "Compared": WARNING,
            "Accepted": SUCCESS, "Rejected": DANGER, "Expired": TEXT_MUTED,
        },
    )


def build_jobs(wb):
    headers = D.HEADERS["Jobs"]
    rows = [r + [None, None] for r in D.JOBS]
    ws, last = build_list_sheet(
        wb, "Jobs", PRIMARY,
        "Assigned work, milestones, balances",
        headers, rows,
        [12, 12, 10, 12, 10, 40, 12, 12, 28, 16, 12, 12, 12, 10],
        date_cols=[7, 8], money_cols=[11, 12, 13], pct_cols=[14],
        validations=[("=Job_Status", "J5:J80")],
        status_col=10,
        status_map={
            "Assigned": TEXT_MUTED, "Scheduled": WARNING, "In Progress": ACCENT,
            "Milestone Review": INFO, "Complete": SUCCESS, "Disputed": DANGER,
        },
        last_col=14,
    )
    for r in range(5, last + 1):
        ws.cell(r, 13).value = f'=IF($A{r}="","",$K{r}-$L{r})'
        ws.cell(r, 13).number_format = CUR
        ws.cell(r, 14).value = f'=IF(OR($A{r}="",$K{r}=0),"",$L{r}/$K{r})'
        ws.cell(r, 14).number_format = PCT
        ws.cell(r, 13).fill = fill(FORMULA_BG)
        ws.cell(r, 14).fill = fill(FORMULA_BG)
        ws.cell(r, 13).border = THIN
        ws.cell(r, 14).border = THIN
        ws.cell(r, 13).font = font(10)
        ws.cell(r, 14).font = font(10)
    return ws, last


# ===========================================================================
# TASKS / TIMELINE
# ===========================================================================
def build_tasks(wb):
    headers = D.HEADERS["Tasks"]
    rows = [r + [None, None] for r in D.TASKS]
    ws, last = build_list_sheet(
        wb, "Tasks", ACCENT,
        "Kanban fields  ·  To Do → Scheduled → In Progress → Inspection → Completed",
        headers, rows,
        [12, 12, 10, 28, 40, 16, 18, 14, 10, 12, 12, 10, 12, 10, 28, 10, 12],
        date_cols=[10, 11], money_cols=[12], pct_cols=[14],
        validations=[
            ("=Task_Status", "H5:H200"),
            ("=Priority", "I5:I200"),
            ("=Role", "G5:G200"),
        ],
        status_col=8,
        status_map={
            "To Do": TEXT_MUTED, "Scheduled": WARNING, "In Progress": ACCENT,
            "Inspection": INFO, "Completed": SUCCESS, "Blocked": DANGER,
        },
        last_col=17,
    )
    for r in range(5, last + 1):
        ws.cell(r, 16).value = f'=IF(OR($A{r}="",$K{r}=""),"", $K{r}-AsOfDate)'
        ws.cell(r, 17).value = (
            f'=IF($A{r}="","",IF($H{r}="Completed","Done",'
            f'IF($K{r}<AsOfDate,"Overdue",'
            f'IF($K{r}<=AsOfDate+7,"Due Soon","On Track"))))'
        )
        ws.cell(r, 16).fill = fill(FORMULA_BG)
        ws.cell(r, 17).fill = fill(FORMULA_BG)
        ws.cell(r, 16).border = THIN
        ws.cell(r, 17).border = THIN
        ws.cell(r, 16).font = font(10)
        ws.cell(r, 17).font = font(10)
        ws.cell(r, 16).alignment = align("center", "center")
        ws.cell(r, 17).alignment = align("center", "center")
    _status_cf(ws, "Q", 5, max(last, 200), {
        "Done": SUCCESS, "On Track": INFO, "Due Soon": WARNING, "Overdue": DANGER,
    })
    _status_cf(ws, "I", 5, max(last, 200), {
        "Critical": DANGER, "High": ACCENT, "Medium": WARNING, "Low": SUCCESS,
    })
    return ws, last


def build_timeline(wb):
    headers = D.HEADERS["Timeline"]
    rows = []
    for r in D.TIMELINE:
        # insert duration placeholder after End
        rows.append(r[:5] + [None] + r[5:] + [None])
    ws, last = build_list_sheet(
        wb, "Timeline", PRIMARY,
        "Phase schedule  ·  Gantt to the right  ·  each block is one week from 1 Mar 2026",
        headers, rows,
        [10, 12, 22, 12, 12, 14, 14, 12, 12],
        date_cols=[4, 5], pct_cols=[9],
        validations=[("=Task_Status", "G5:G80")],
        status_col=7,
        status_map={
            "To Do": TEXT_MUTED, "Scheduled": WARNING, "In Progress": ACCENT, "Completed": SUCCESS,
        },
        last_col=9,
    )
    for r in range(5, last + 1):
        ws.cell(r, 6).value = f'=IF($A{r}="","",$E{r}-$D{r}+1)'
        ws.cell(r, 9).value = (
            f'=IF($A{r}="","",MAX(0,MIN(1,(AsOfDate-$D{r}+1)/MAX(1,$E{r}-$D{r}+1))))'
        )
        ws.cell(r, 6).fill = fill(FORMULA_BG)
        ws.cell(r, 9).fill = fill(FORMULA_BG)
        ws.cell(r, 6).number_format = INT
        ws.cell(r, 9).number_format = PCT
        ws.cell(r, 6).border = THIN
        ws.cell(r, 9).border = THIN
        ws.cell(r, 6).font = font(10)
        ws.cell(r, 9).font = font(10)

    # Gantt: weekly columns starting 2026-03-01 for 40 weeks
    start = date(2026, 3, 1)
    weeks = 40
    gantt0 = 11  # column K
    ws.cell(3, gantt0, "WEEKLY GANTT  ·  filled cell = phase is active that week  ·  gold column = this week")
    ws.cell(3, gantt0).font = font(9, True, PRIMARY)
    ws.merge_cells(start_row=3, start_column=gantt0, end_row=3, end_column=gantt0 + weeks - 1)
    for w in range(weeks):
        col = gantt0 + w
        d0 = start + timedelta(days=7 * w)
        cell = ws.cell(4, col, d0)
        cell.number_format = "D-MMM"
        cell.font = font(8, True, WHITE)
        cell.fill = fill(PRIMARY)
        cell.alignment = align("center", "center")
        cell.border = THIN
        ws.column_dimensions[get_column_letter(col)].width = 5
        for r in range(5, last + 1):
            # 1 if week overlaps phase
            letter = get_column_letter(col)
            ws.cell(r, col).value = (
                f'=IF(OR($D{r}="",$E{r}=""),"",'
                f'IF(AND({letter}$4<=$E{r},{letter}$4+6>=$D{r}),'
                f'IF($G{r}="Completed","D",IF($G{r}="In Progress","N","P")),""))'
            )
            ws.cell(r, col).alignment = align("center", "center")
            ws.cell(r, col).font = font(8, True, WHITE)
            ws.cell(r, col).border = THIN
    # CF for gantt letters
    g_range = f"K5:{get_column_letter(gantt0+weeks-1)}{last}"
    ws.conditional_formatting.add(g_range, FormulaRule(formula=['K5="D"'], fill=fill(SUCCESS), font=font(8, True, SUCCESS)))
    ws.conditional_formatting.add(g_range, FormulaRule(formula=['K5="N"'], fill=fill(ACCENT), font=font(8, True, ACCENT)))
    ws.conditional_formatting.add(g_range, FormulaRule(formula=['K5="P"'], fill=fill(SECONDARY_DEEP), font=font(8, True, SECONDARY_DEEP)))
    # highlight current week header
    for w in range(weeks):
        col = gantt0 + w
        letter = get_column_letter(col)
        ws.conditional_formatting.add(
            f"{letter}4",
            FormulaRule(
                formula=[f'AND({letter}4<=AsOfDate,{letter}4+6>=AsOfDate)'],
                fill=fill(ACCENT),
                font=font(8, True, WHITE),
            ),
        )
    return ws, last


# ===========================================================================
# MATERIALS / SUPPLIERS / SHOPPING
# ===========================================================================
def build_materials(wb):
    headers = D.HEADERS["Materials"]
    # Source has no Line Total (col 11) or Open Qty (col 22) — both are formulas.
    rows = [r[:10] + [None] + r[10:] + [None] for r in D.MATERIALS]
    ws, last = build_list_sheet(
        wb, "Materials", WARNING,
        "Procurement  ·  Required → Quoted → Approved → Ordered → Shipped → Delivered → Installed",
        headers, rows,
        [12, 12, 10, 28, 16, 14, 12, 12, 8, 12, 12, 22, 12, 12, 12, 12, 12, 14, 12, 12, 14, 10],
        date_cols=[19, 20], money_cols=[10, 11],
        validations=[("=Material_Status", "P5:P200")],
        status_col=16,
        status_map={
            "Required": TEXT_MUTED, "Quoted": INFO, "Approved": SUCCESS, "Ordered": WARNING,
            "Shipped": ACCENT, "Delivered": INFO, "Installed": SUCCESS,
            "Returned": DANGER, "Backordered": DANGER,
        },
        last_col=22,
    )
    for r in range(5, last + 1):
        ws.cell(r, 11).value = f'=IF($A{r}="","",$H{r}*$J{r})'
        ws.cell(r, 11).number_format = CUR
        ws.cell(r, 22).value = f'=IF($A{r}="","",$H{r}-$N{r})'
        ws.cell(r, 11).fill = fill(FORMULA_BG)
        ws.cell(r, 22).fill = fill(FORMULA_BG)
        ws.cell(r, 11).border = THIN
        ws.cell(r, 22).border = THIN
        ws.cell(r, 11).font = font(10)
        ws.cell(r, 22).font = font(10)
    return ws, last


def build_suppliers(wb):
    return build_list_sheet(
        wb, "Suppliers", PRIMARY_SOFT,
        "Vendor book  ·  lead times drive the prediction engine",
        D.HEADERS["Suppliers"], D.SUPPLIERS,
        [12, 24, 18, 16, 18, 32, 24, 10, 14, 16, 28],
    )


def build_shopping(wb):
    ws = _sheet(wb, "Shopping List", ACCENT, 10,
                "Auto-built from Materials still Required / Quoted / Approved  ·  refresh by editing Materials")
    headers = ["SKU / QR", "Product", "Room", "Qty", "Unit", "Est. Unit $", "Est. Total", "Supplier", "Status", "Project"]
    header_row(ws, 4, headers)
    # FILTER is supported in Excel 365 and Google Sheets. Provide a compatible INDEX/SMALL fallback
    # plus a FILTER formula in a note. We'll generate a static-looking live list with INDEX/SMALL.
    for i in range(25):
        r = 5 + i
        # nth material whose status is Required/Quoted/Approved
        ws.cell(r, 10).value = (
            f'=IFERROR(INDEX(Materials!$B:$B,SMALL(IF((Materials!$P$5:$P$200="Required")+(Materials!$P$5:$P$200="Quoted")+(Materials!$P$5:$P$200="Approved"),ROW(Materials!$P$5:$P$200)),{i+1})),"")'
        )
        # Array formulas: Excel 365 and Google Sheets both calculate these as dynamic arrays if entered.
        # To maximize compatibility, also write a Google-friendly FILTER block starting at row 32.
        for c in range(1, 11):
            ws.cell(r, c).fill = fill(WHITE if i % 2 == 0 else ROW_ALT)
            ws.cell(r, c).border = THIN
            ws.cell(r, c).font = font(10)
    # Simpler reliable approach: use helper column already on Materials? 
    # We'll put FILTER formula for Google Sheets / Excel 365 in A5 as a spilled range instruction.
    # Clear the INDEX formulas and use FILTER (works in both modern Excel and Sheets).
    for r in range(5, 30):
        for c in range(1, 11):
            ws.cell(r, c).value = None
    # Place FILTER formulas in row 5 (spill). Google Sheets and Excel 365 support FILTER.
    ws["A5"] = '=IFERROR(FILTER(Materials!F5:F200,(Materials!P5:P200="Required")+(Materials!P5:P200="Quoted")+(Materials!P5:P200="Approved")),"")'
    ws["B5"] = '=IFERROR(FILTER(Materials!D5:D200,(Materials!P5:P200="Required")+(Materials!P5:P200="Quoted")+(Materials!P5:P200="Approved")),"")'
    ws["C5"] = '=IFERROR(FILTER(Materials!C5:C200,(Materials!P5:P200="Required")+(Materials!P5:P200="Quoted")+(Materials!P5:P200="Approved")),"")'
    ws["D5"] = '=IFERROR(FILTER(Materials!H5:H200,(Materials!P5:P200="Required")+(Materials!P5:P200="Quoted")+(Materials!P5:P200="Approved")),"")'
    ws["E5"] = '=IFERROR(FILTER(Materials!I5:I200,(Materials!P5:P200="Required")+(Materials!P5:P200="Quoted")+(Materials!P5:P200="Approved")),"")'
    ws["F5"] = '=IFERROR(FILTER(Materials!J5:J200,(Materials!P5:P200="Required")+(Materials!P5:P200="Quoted")+(Materials!P5:P200="Approved")),"")'
    ws["G5"] = '=IFERROR(FILTER(Materials!K5:K200,(Materials!P5:P200="Required")+(Materials!P5:P200="Quoted")+(Materials!P5:P200="Approved")),"")'
    ws["H5"] = '=IFERROR(FILTER(Materials!L5:L200,(Materials!P5:P200="Required")+(Materials!P5:P200="Quoted")+(Materials!P5:P200="Approved")),"")'
    ws["I5"] = '=IFERROR(FILTER(Materials!P5:P200,(Materials!P5:P200="Required")+(Materials!P5:P200="Quoted")+(Materials!P5:P200="Approved")),"")'
    ws["J5"] = '=IFERROR(FILTER(Materials!B5:B200,(Materials!P5:P200="Required")+(Materials!P5:P200="Quoted")+(Materials!P5:P200="Approved")),"")'
    for c in range(1, 11):
        ws.cell(5, c).fill = fill(INPUT_BG)
        ws.cell(5, c).font = font(10)
    input_note(ws, 32, 1, "Excel 365 and Google Sheets will spill the shopping list from row 5. If you are on Excel 2019 or earlier, filter the Materials sheet for Status = Required / Quoted / Approved and copy those rows here.", 10)
    set_col_widths(ws, [14, 32, 12, 10, 8, 12, 12, 24, 12, 12])
    freeze(ws, "A5")
    return ws


# ===========================================================================
# DOCUMENTS / MESSAGES
# ===========================================================================
def build_documents(wb):
    headers = D.HEADERS["Documents"]
    rows = [r + [None, None] for r in D.DOCUMENTS]
    ws, last = build_list_sheet(
        wb, "Documents", PRIMARY,
        "Project vault  ·  contracts, permits, warranties, photos, signed agreements",
        headers, rows,
        [12, 12, 10, 16, 36, 10, 32, 12, 12, 10, 16, 28, 14, 14],
        date_cols=[8, 9],
        validations=[("=Doc_Category", "D5:D200")],
        last_col=14,
    )
    for r in range(5, last + 1):
        ws.cell(r, 13).value = f'=IF(OR($A{r}="",$I{r}=""),"",$I{r}-AsOfDate)'
        ws.cell(r, 14).value = (
            f'=IF(OR($A{r}="",$I{r}=""),"",IF($I{r}<AsOfDate,"Expired",IF($I{r}<=AsOfDate+30,"Expiring","OK")))'
        )
        ws.cell(r, 13).fill = fill(FORMULA_BG)
        ws.cell(r, 14).fill = fill(FORMULA_BG)
        ws.cell(r, 13).border = THIN
        ws.cell(r, 14).border = THIN
        ws.cell(r, 13).font = font(10)
        ws.cell(r, 14).font = font(10)
    _status_cf(ws, "N", 5, max(last, 200), {"OK": SUCCESS, "Expiring": WARNING, "Expired": DANGER})
    _status_cf(ws, "J", 5, max(last, 200), {"Yes": SUCCESS, "No": TEXT_MUTED})
    return ws, last


def build_messages(wb):
    return build_list_sheet(
        wb, "Messages", INFO,
        "Homeowner ↔ contractor ↔ designer ↔ supplier  ·  keep threads on a room or task",
        D.HEADERS["Messages"], D.MESSAGES,
        [12, 20, 12, 20, 16, 18, 14, 64, 28, 18, 8],
        validations=[("=Channel", "G5:G200")],
        status_col=11,
        status_map={"Yes": SUCCESS, "No": WARNING},
    )


# ===========================================================================
# INVENTORY / MAINTENANCE
# ===========================================================================
def build_inventory(wb):
    headers = D.HEADERS["Inventory"]
    rows = []
    for r in D.INVENTORY:
        # Warranty End is computed
        rows.append(r[:8] + [None] + r[8:])
    ws, last = build_list_sheet(
        wb, "Inventory", PRIMARY_SOFT,
        "Everything in the house  ·  insurance + future maintenance",
        headers, rows,
        [12, 40, 16, 18, 12, 14, 12, 14, 14, 16, 16, 16, 12, 16, 36],
        date_cols=[6, 9], money_cols=[7, 14],
        last_col=15,
    )
    for r in range(5, last + 1):
        ws.cell(r, 9).value = f'=IF(OR($A{r}="",$F{r}="",$H{r}=""),"",EDATE($F{r},$H{r}*12))'
        ws.cell(r, 9).number_format = DATE
        ws.cell(r, 9).fill = fill(FORMULA_BG)
        ws.cell(r, 9).border = THIN
        ws.cell(r, 9).font = font(10)
    return ws, last


def build_maintenance(wb):
    headers = D.HEADERS["Maintenance"]
    rows = [r + [None, None] for r in D.MAINTENANCE]
    ws, last = build_list_sheet(
        wb, "Maintenance", SUCCESS,
        "The system does not end at handover  ·  HVAC, roof, warranties, pest, water, solar",
        headers, rows,
        [12, 32, 18, 12, 12, 14, 12, 20, 12, 12, 12, 28, 14, 16],
        date_cols=[6, 7], money_cols=[9],
        validations=[("=Maint_Status", "J5:J200")],
        status_col=10,
        status_map={
            "Upcoming": INFO, "Due Soon": WARNING, "Overdue": DANGER,
            "Scheduled": ACCENT, "Complete": SUCCESS,
        },
        last_col=14,
    )
    for r in range(5, last + 1):
        ws.cell(r, 13).value = f'=IF(OR($A{r}="",$G{r}=""),"",$G{r}-AsOfDate)'
        ws.cell(r, 14).value = (
            f'=IF($A{r}="","",IF($J{r}="Complete","—",'
            f'IF($G{r}<AsOfDate,"🔔 OVERDUE",'
            f'IF($G{r}<=AsOfDate+$K{r},"🔔 Due soon","OK"))))'
        )
        ws.cell(r, 13).fill = fill(FORMULA_BG)
        ws.cell(r, 14).fill = fill(FORMULA_BG)
        ws.cell(r, 13).border = THIN
        ws.cell(r, 14).border = THIN
        ws.cell(r, 13).font = font(10)
        ws.cell(r, 14).font = font(10)
    return ws, last


# ===========================================================================
# INSPECTIONS / PAYMENTS / CO / PERMITS / WARRANTIES
# ===========================================================================
def build_inspections(wb):
    return build_list_sheet(
        wb, "Inspections", INFO,
        "City + independent  ·  attach reports in the vault",
        D.HEADERS["Inspections"], D.INSPECTIONS,
        [12, 12, 10, 28, 22, 12, 12, 36, 22, 12, 28],
        date_cols=[6],
        validations=[("=Insp_Result", "G5:G80")],
        status_col=7,
        status_map={"Pass": SUCCESS, "Conditional": WARNING, "Fail": DANGER, "Scheduled": INFO},
    )


def build_payments(wb):
    headers = D.HEADERS["Payments"]
    rows = [r + [None] for r in D.PAYMENTS]
    ws, last = build_list_sheet(
        wb, "Payments", SUCCESS,
        "Draws, deposits, scheduled wires  ·  aging for unpaid",
        headers, rows,
        [12, 12, 12, 24, 12, 16, 12, 14, 12, 12, 12, 12],
        date_cols=[2, 10, 11], money_cols=[7],
        validations=[("=Payment_Status", "I5:I80")],
        status_col=9,
        status_map={"Paid": SUCCESS, "Scheduled": WARNING, "Draft": TEXT_MUTED, "Overdue": DANGER, "Disputed": ACCENT},
        last_col=12,
    )
    for r in range(5, last + 1):
        ws.cell(r, 12).value = (
            f'=IF($A{r}="","",IF($I{r}="Paid",0,IF($J{r}="","" ,AsOfDate-$J{r})))'
        )
        ws.cell(r, 12).fill = fill(FORMULA_BG)
        ws.cell(r, 12).border = THIN
        ws.cell(r, 12).font = font(10)
    return ws, last


def build_change_orders(wb):
    return build_list_sheet(
        wb, "Change Orders", ACCENT,
        "Scope, cost, and schedule impacts  ·  negative cost = savings",
        D.HEADERS["Change Orders"], D.CHANGE_ORDERS,
        [10, 12, 10, 56, 22, 12, 12, 18, 14, 16],
        date_cols=[6], money_cols=[7],
        validations=[("=CO_Status", "I5:I80")],
        status_col=9,
        status_map={
            "Draft": TEXT_MUTED, "Submitted": WARNING, "Approved": INFO,
            "Rejected": DANGER, "Implemented": SUCCESS,
        },
    )


def build_permits(wb):
    headers = D.HEADERS["Permits"]
    rows = [r + [None] for r in D.PERMITS]
    ws, last = build_list_sheet(
        wb, "Permits", WARNING,
        "Authority, fees, expiration reminders",
        headers, rows,
        [12, 12, 28, 20, 12, 12, 16, 10, 12, 12, 28, 14],
        date_cols=[5, 6, 9], money_cols=[8],
        validations=[("=Permit_Status", "J5:J80")],
        status_col=10,
        status_map={
            "Not Started": TEXT_MUTED, "Applied": INFO, "In Review": WARNING,
            "Approved": SUCCESS, "Expired": DANGER, "Closed": PRIMARY,
        },
        last_col=12,
    )
    for r in range(5, last + 1):
        ws.cell(r, 12).value = f'=IF(OR($A{r}="",$I{r}=""),"",$I{r}-AsOfDate)'
        ws.cell(r, 12).fill = fill(FORMULA_BG)
        ws.cell(r, 12).border = THIN
        ws.cell(r, 12).font = font(10)
    return ws, last


def build_warranties(wb):
    headers = D.HEADERS["Warranties"]
    rows = [r + [None] for r in D.WARRANTIES]
    ws, last = build_list_sheet(
        wb, "Warranties", SUCCESS,
        "Labor and product coverage after handover",
        headers, rows,
        [12, 12, 32, 22, 12, 12, 14, 24, 28, 24, 14],
        date_cols=[5, 6],
        last_col=11,
    )
    for r in range(5, last + 1):
        ws.cell(r, 11).value = f'=IF(OR($A{r}="",$F{r}=""),"",$F{r}-AsOfDate)'
        ws.cell(r, 11).fill = fill(FORMULA_BG)
        ws.cell(r, 11).border = THIN
        ws.cell(r, 11).font = font(10)
        ws.conditional_formatting.add(
            f"K5:K{max(last, 80)}",
            CellIsRule(operator="lessThan", formula=["90"], fill=fill(WARNING_SOFT), font=font(10, True, WARNING)),
        )
    return ws, last


# ===========================================================================
# NOTIFICATIONS / AUDIT / CALENDAR
# ===========================================================================
def build_notifications(wb):
    return build_list_sheet(
        wb, "Notifications", ACCENT,
        "In-app / email / SMS queue  ·  mark Status = Read when handled",
        D.HEADERS["Notifications"], D.NOTIFICATIONS,
        [12, 12, 12, 14, 64, 12, 10],
        date_cols=[2],
        status_col=3,
        status_map={"Info": INFO, "Success": SUCCESS, "Warning": WARNING, "Critical": DANGER},
    )


def build_audit(wb):
    return build_list_sheet(
        wb, "Audit Log", TEXT_MUTED,
        "Who changed what  ·  append-only in the live product",
        D.HEADERS["Audit Log"], D.AUDIT,
        [12, 20, 12, 16, 16, 12, 48],
    )


def build_calendar(wb):
    return build_list_sheet(
        wb, "Calendar", PRIMARY_MID,
        "Visits, deliveries, inspections, reminders  ·  also subscribe via the Apps Script",
        D.HEADERS["Calendar"], D.CALENDAR,
        [12, 10, 22, 18, 48, 16, 12],
        date_cols=[1],
        status_col=7,
        status_map={
            "Scheduled": SUCCESS, "To Do": INFO, "Due Soon": WARNING,
            "Watch": ACCENT, "Hold": DANGER, "Upcoming": TEXT_MUTED,
        },
    )


# ===========================================================================
# DASHBOARD
# ===========================================================================
def build_dashboard(wb):
    ws = _sheet(wb, "Dashboard", PRIMARY, 14,
                "Homeowner overview  ·  live formulas  ·  switch Active Project on Settings")
    ws.row_dimensions[1].height = 30
    # Greeting
    ws.merge_cells("A4:F4")
    ws["A4"] = '= "Good day, " & HomeownerName & "  ·  " & TEXT(AsOfDate,"DDDD, D MMMM YYYY")'
    ws["A4"].font = font(16, True, PRIMARY)
    ws["A4"].alignment = align("left", "center")
    ws["A4"].fill = fill(BG)
    ws.merge_cells("A5:F5")
    ws["A5"] = '= "YOUR RENOVATION  ·  " & IFERROR(INDEX(Projects!C:C,MATCH(ActiveProject,Projects!A:A,0)),ActiveProject) & "  ·  " & IFERROR(INDEX(Projects!F:F,MATCH(ActiveProject,Projects!A:A,0)),"")'
    ws["A5"].font = font(10, False, TEXT_MUTED)
    ws["A5"].fill = fill(BG)

    # Progress bar (formula text)
    kpi_card(ws, 7, 1, "PROGRESS",
             '=IFERROR(INDEX(Projects!P:P,MATCH(ActiveProject,Projects!A:A,0)),0)',
             '=REPT("█",ROUND(A8*20,0))&REPT("░",20-ROUND(A8*20,0))',
             ACCENT, 3, 3)
    ws["A8"].number_format = PCT
    kpi_card(ws, 7, 5, "PHASE",
             '=IFERROR(INDEX(Projects!F:F,MATCH(ActiveProject,Projects!A:A,0)),"—")',
             '=IFERROR(INDEX(Projects!E:E,MATCH(ActiveProject,Projects!A:A,0)),"")',
             PRIMARY, 2, 3)
    kpi_card(ws, 7, 8, "BUDGET",
             '=IFERROR(INDEX(Projects!J:J,MATCH(ActiveProject,Projects!A:A,0)),0)',
             "Planned", PRIMARY, 2, 3)
    ws["H8"].number_format = CUR
    kpi_card(ws, 7, 11, "SPENT",
             '=IFERROR(SUMIFS(Expenses!H:H,Expenses!C:C,ActiveProject,Expenses!J:J,"Paid"),0)',
             "Paid to date", ACCENT, 2, 3)
    ws["K8"].number_format = CUR

    kpi_card(ws, 11, 1, "COMMITTED",
             '=IFERROR(SUMIFS(Expenses!H:H,Expenses!C:C,ActiveProject,Expenses!J:J,"Committed"),0)',
             "Not yet paid", WARNING, 2, 3)
    ws["A12"].number_format = CUR
    kpi_card(ws, 11, 4, "REMAINING",
             "=H8-K8-A12",
             "Still available", SUCCESS, 2, 3)
    ws["D12"].number_format = CUR
    kpi_card(ws, 11, 7, "OPEN TASKS",
             '=COUNTIFS(Tasks!B:B,ActiveProject,Tasks!H:H,"<>Completed")',
             "Not completed", PRIMARY, 2, 3)
    kpi_card(ws, 11, 10, "OVERDUE",
             '=COUNTIFS(Tasks!B:B,ActiveProject,Tasks!H:H,"<>Completed",Tasks!K:K,"<"&AsOfDate)',
             "Past deadline", DANGER, 2, 3)

    # Attention / alerts
    section_label(ws, 15, 1, "ATTENTION", 6)
    attention = [
        (16, '=IF((K8+A12)>H8,"⚠ Project is over the planned budget.","")'),
        (17, '=IF(Finance!D10<H8*ContingencyFloor,"🔴 Contingency has fallen below 10%. Freeze non-critical extras.","")'),
        (18, '=IF(COUNTIFS(Tasks!B:B,ActiveProject,Tasks!Q:Q,"Overdue")>0,"⚠ "&COUNTIFS(Tasks!B:B,ActiveProject,Tasks!Q:Q,"Overdue")&" overdue task(s).","")'),
        (19, '=IF(COUNTIFS(Materials!B:B,ActiveProject,Materials!P:P,"Backordered")>0,"⚠ Material backorder: "&COUNTIFS(Materials!B:B,ActiveProject,Materials!P:P,"Backordered")&" line(s).","")'),
        (20, '=IF(COUNTIFS(Documents!B:B,ActiveProject,Documents!N:N,"Expiring")+COUNTIFS(Documents!B:B,ActiveProject,Documents!N:N,"Expired")>0,"⚠ Document expiry needs attention.","")'),
        (21, '=IF(COUNTIFS(\'Change Orders\'!B:B,ActiveProject,\'Change Orders\'!I:I,"Submitted")>0,"⚠ Change order awaiting approval.","")'),
        (22, '=IF(COUNTA(A16:A21)=0,"🟢 Nothing urgent. You\'re clear for the week.","")'),
    ]
    for r, fml in attention:
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
        ws.cell(r, 1, fml)
        ws.cell(r, 1).font = font(10, False, TEXT)
        ws.cell(r, 1).fill = fill(WHITE)
        ws.cell(r, 1).alignment = align("left", "center")
        ws.row_dimensions[r].height = 18

    # Next up tasks
    section_label(ws, 15, 8, "NEXT UP", 6)
    nh = ["When", "Task", "Room", "Owner", "Status"]
    for i, h in enumerate(nh, 8):
        cell = ws.cell(16, i, h)
        cell.font = font(9, True, WHITE)
        cell.fill = fill(PRIMARY)
        cell.alignment = align("center", "center")
        cell.border = THIN
    # Pull 6 soonest open tasks with FILTER (Excel 365 / Sheets)
    # Fallback: list known upcoming from Tasks via INDEX on deadline
    # We'll place FILTER spilled formulas
    ws["H17"] = '=IFERROR(FILTER(Tasks!K5:K200,(Tasks!B5:B200=ActiveProject)*(Tasks!H5:H200<>"Completed")),"")'
    ws["I17"] = '=IFERROR(FILTER(Tasks!D5:D200,(Tasks!B5:B200=ActiveProject)*(Tasks!H5:H200<>"Completed")),"")'
    ws["J17"] = '=IFERROR(FILTER(Tasks!C5:C200,(Tasks!B5:B200=ActiveProject)*(Tasks!H5:H200<>"Completed")),"")'
    ws["K17"] = '=IFERROR(FILTER(Tasks!F5:F200,(Tasks!B5:B200=ActiveProject)*(Tasks!H5:H200<>"Completed")),"")'
    ws["L17"] = '=IFERROR(FILTER(Tasks!H5:H200,(Tasks!B5:B200=ActiveProject)*(Tasks!H5:H200<>"Completed")),"")'
    ws["H17"].number_format = DATE
    for c in range(8, 13):
        ws.cell(17, c).fill = fill(WHITE)
        ws.cell(17, c).font = font(9)

    # Recent expenses
    section_label(ws, 24, 1, "RECENT EXPENSES", 6)
    eh = ["Date", "Vendor", "Description", "Amount", "Status"]
    for i, h in enumerate(eh, 1):
        cell = ws.cell(25, i, h)
        cell.font = font(9, True, WHITE)
        cell.fill = fill(PRIMARY)
        cell.border = THIN
    # last 8 expenses for active project via FILTER
    ws["A26"] = '=IFERROR(FILTER(Expenses!B5:B200,Expenses!C5:C200=ActiveProject),"")'
    ws["B26"] = '=IFERROR(FILTER(Expenses!F5:F200,Expenses!C5:C200=ActiveProject),"")'
    ws["C26"] = '=IFERROR(FILTER(Expenses!G5:G200,Expenses!C5:C200=ActiveProject),"")'
    ws["D26"] = '=IFERROR(FILTER(Expenses!H5:H200,Expenses!C5:C200=ActiveProject),"")'
    ws["E26"] = '=IFERROR(FILTER(Expenses!J5:J200,Expenses!C5:C200=ActiveProject),"")'
    ws["A26"].number_format = DATE
    ws["D26"].number_format = CUR

    # Room snapshot
    section_label(ws, 24, 8, "ROOMS", 6)
    rh = ["Room", "Status", "Budget", "Spent", "%"]
    for i, h in enumerate(rh, 8):
        cell = ws.cell(25, i, h)
        cell.font = font(9, True, WHITE)
        cell.fill = fill(PRIMARY)
        cell.border = THIN
    prj_rooms = [rm for rm in D.ROOMS if rm[1] == "PRJ-001"]
    for i, rm in enumerate(prj_rooms):
        r = 26 + i
        ws.cell(r, 8, rm[2])
        ws.cell(r, 9, f'=IFERROR(INDEX(Rooms!J:J,MATCH("{rm[0]}",Rooms!A:A,0)),"")')
        ws.cell(r, 10, f'=IFERROR(INDEX(Rooms!K:K,MATCH("{rm[0]}",Rooms!A:A,0)),0)')
        ws.cell(r, 11, f'=IFERROR(INDEX(Rooms!R:R,MATCH("{rm[0]}",Rooms!A:A,0)),0)')
        ws.cell(r, 12, f'=IF(J{r}=0,"",K{r}/J{r})')
        ws.cell(r, 10).number_format = CUR
        ws.cell(r, 11).number_format = CUR
        ws.cell(r, 12).number_format = PCT
        for c in range(8, 13):
            ws.cell(r, c).fill = fill(WHITE if i % 2 == 0 else ROW_ALT)
            ws.cell(r, c).border = THIN
            ws.cell(r, c).font = font(9)

    # Contractor visits
    section_label(ws, 36, 1, "UPCOMING CONTRACTOR VISITS", 6)
    vh = ["Date", "Event", "Owner", "Status"]
    for i, h in enumerate(vh, 1):
        cell = ws.cell(37, i, h)
        cell.font = font(9, True, WHITE)
        cell.fill = fill(PRIMARY)
        cell.border = THIN
    ws["A38"] = '=IFERROR(FILTER(Calendar!A5:A80,Calendar!A5:A80>=AsOfDate),"")'
    ws["B38"] = '=IFERROR(FILTER(Calendar!C5:C80,Calendar!A5:A80>=AsOfDate),"")'
    ws["C38"] = '=IFERROR(FILTER(Calendar!F5:F80,Calendar!A5:A80>=AsOfDate),"")'
    ws["D38"] = '=IFERROR(FILTER(Calendar!G5:G80,Calendar!A5:A80>=AsOfDate),"")'
    ws["A38"].number_format = DATE

    # Quick actions (as labeled cells — operational in Apps Script)
    section_label(ws, 36, 8, "QUICK ACTIONS  (use the Novality Store menu in Google Sheets)", 6)
    actions = [
        (37, "+ Expense"),
        (38, "+ Task"),
        (39, "Upload photo note"),
        (40, "Message contractor"),
        (41, "Approve change order"),
        (42, "Generate shopping list"),
    ]
    for r, label in actions:
        ws.merge_cells(start_row=r, start_column=8, end_row=r, end_column=10)
        ws.cell(r, 8, label)
        ws.cell(r, 8).font = font(10, True, WHITE)
        ws.cell(r, 8).fill = fill(ACCENT if r % 2 else PRIMARY)
        ws.cell(r, 8).alignment = align("center", "center")
        ws.row_dimensions[r].height = 20

    # AI insight of the day
    section_label(ws, 45, 1, "AI INSIGHT", 12)
    ws.merge_cells("A46:L48")
    ws["A46"] = (
        '=IFERROR(INDEX(\'AI Insights\'!G:G,MATCH(1,(\'AI Insights\'!C:C=ActiveProject)*'
        '((\'AI Insights\'!J:J="New")+(\'AI Insights\'!J:J="In Progress")),0)),'
        '"No open AI insights.")'
    )
    ws["A46"].alignment = align("left", "center", True)
    ws["A46"].font = font(11, False, TEXT)
    ws["A46"].fill = fill(WHITE)
    ws.merge_cells("A49:L50")
    ws["A49"] = (
        '=IFERROR("Recommendation: "&INDEX(\'AI Insights\'!H:H,MATCH(1,(\'AI Insights\'!C:C=ActiveProject)*'
        '((\'AI Insights\'!J:J="New")+(\'AI Insights\'!J:J="In Progress")),0)),"")'
    )
    ws["A49"].alignment = align("left", "center", True)
    ws["A49"].font = font(10, True, ACCENT)
    ws["A49"].fill = fill(WHITE)

    # Nav
    section_label(ws, 52, 1, "NAVIGATION", 12)
    nav = [
        (53, 1, "Projects", "Projects"),
        (53, 3, "Rooms", "Rooms"),
        (53, 5, "Design", "Design Studio"),
        (53, 7, "Budget", "Budget"),
        (53, 9, "Team", "Contractors"),
        (53, 11, "Materials", "Materials"),
        (54, 1, "Tasks", "Tasks"),
        (54, 3, "Messages", "Messages"),
        (54, 5, "Documents", "Documents"),
        (54, 7, "Home", "Inventory"),
        (54, 9, "Maint.", "Maintenance"),
        (54, 11, "Admin", "Admin"),
    ]
    for r, c, label, target in nav:
        cell = ws.cell(r, c, label)
        cell.hyperlink = f"#'{target}'!A1"
        cell.font = font(10, True, WHITE)
        cell.fill = fill(PRIMARY)
        cell.alignment = align("center", "center")
        ws.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c + 1)
        ws.row_dimensions[r].height = 22

    set_col_widths(ws, [16, 16, 16, 14, 16, 16, 14, 16, 14, 14, 14, 12, 12, 12])
    freeze(ws, "A4")
    return ws


# ===========================================================================
# ADMIN
# ===========================================================================
def build_admin(wb):
    ws = _sheet(wb, "Admin", PRIMARY, 12,
                "System administrator  ·  portfolio of all homeowners and projects")
    cards = [
        (5, 1, "HOMEOWNERS", '=COUNTIF(Users!E:E,"Homeowner")', "Active household accounts", PRIMARY),
        (5, 4, "ACTIVE PROJECTS", '=COUNTIF(Projects!E:E,"Active")', "In construction or design", ACCENT),
        (5, 7, "COMPLETED", '=COUNTIF(Projects!E:E,"Completed")', "Renovations handed over", SUCCESS),
        (5, 10, "CONTRACTORS", '=COUNTA(Contractors!A5:A200)', "In the bench", PRIMARY),
        (9, 1, "PORTFOLIO VALUE", "=SUM(Projects!J:J)", "Sum of project budgets", ACCENT),
        (9, 4, "REVENUE (PAID)", '=SUMIF(Expenses!J:J,"Paid",Expenses!H:H)', "Cash out recorded", SUCCESS),
        (9, 7, "DELAYED TASKS", '=COUNTIF(Tasks!Q:Q,"Overdue")', "Across all projects", DANGER),
        (9, 10, "OPEN DISPUTES", '=COUNTIF(Jobs!J:J,"Disputed")+COUNTIF(Payments!I:I,"Disputed")', "Jobs + payments", WARNING),
        (13, 1, "PENDING APPROVALS", '=COUNTIF(\'Change Orders\'!I:I,"Submitted")+COUNTIF(Quotes!J:J,"Received")', "COs + quotes", WARNING),
        (13, 4, "OPEN MESSAGES", '=COUNTIF(Messages!K:K,"No")', "Unread", INFO),
        (13, 7, "PERMITS OPEN", '=COUNTIFS(Permits!J:J,"<>Closed",Permits!J:J,"<>")-1', "Not closed", PRIMARY),
        (13, 10, "MAINT DUE", '=COUNTIF(Maintenance!N:N,"🔔 OVERDUE")+COUNTIF(Maintenance!N:N,"🔔 Due soon")', "Aftercare load", ACCENT),
    ]
    for r, c, label, val, sub, color in cards:
        mid = kpi_card(ws, r, c, label, val, sub, color, 2, 3)
        if "VALUE" in label or "REVENUE" in label:
            mid.number_format = CUR

    section_label(ws, 17, 1, "PROJECT PORTFOLIO", 10)
    ph = ["Project", "Property", "Status", "Phase", "Budget", "Spent", "Health", "Progress"]
    for i, h in enumerate(ph, 1):
        cell = ws.cell(18, i, h)
        cell.font = font(9, True, WHITE)
        cell.fill = fill(PRIMARY)
        cell.border = THIN
    for i, p in enumerate(D.PROJECTS):
        r = 19 + i
        pid = p[0]
        ws.cell(r, 1, f'=IFERROR(INDEX(Projects!C:C,MATCH("{pid}",Projects!A:A,0)),"")')
        ws.cell(r, 2, pid)
        ws.cell(r, 3, f'=IFERROR(INDEX(Projects!E:E,MATCH("{pid}",Projects!A:A,0)),"")')
        ws.cell(r, 4, f'=IFERROR(INDEX(Projects!F:F,MATCH("{pid}",Projects!A:A,0)),"")')
        ws.cell(r, 5, f'=IFERROR(INDEX(Projects!J:J,MATCH("{pid}",Projects!A:A,0)),0)')
        ws.cell(r, 6, f'=IFERROR(INDEX(Projects!R:R,MATCH("{pid}",Projects!A:A,0)),0)')
        ws.cell(r, 7, f'=IFERROR(INDEX(Projects!U:U,MATCH("{pid}",Projects!A:A,0)),"")')
        ws.cell(r, 8, f'=IFERROR(INDEX(Projects!P:P,MATCH("{pid}",Projects!A:A,0)),0)')
        ws.cell(r, 5).number_format = CUR
        ws.cell(r, 6).number_format = CUR
        ws.cell(r, 8).number_format = PCT
        for c in range(1, 9):
            ws.cell(r, c).fill = fill(WHITE if i % 2 == 0 else ROW_ALT)
            ws.cell(r, c).border = THIN
            ws.cell(r, c).font = font(10)

    section_label(ws, 23, 1, "SUPPLIER PERFORMANCE (lead time vs rating)", 8)
    sh = ["Supplier", "Category", "Rating", "Lead days"]
    for i, h in enumerate(sh, 1):
        cell = ws.cell(24, i, h)
        cell.font = font(9, True, WHITE)
        cell.fill = fill(PRIMARY)
        cell.border = THIN
    ws["A25"] = "=Suppliers!B5:B20"
    ws["B25"] = "=Suppliers!C5:C20"
    ws["C25"] = "=Suppliers!H5:H20"
    ws["D25"] = "=Suppliers!J5:J20"

    set_col_widths(ws, [28, 16, 14, 16, 14, 14, 12, 12, 12, 14, 12, 12])
    return ws


# ===========================================================================
# START HERE
# ===========================================================================
def build_start(wb):
    ws = _sheet(wb, "Start Here", ACCENT, 10,
                "Read this first  ·  then open Dashboard  ·  upload this file to Google Drive to get a Google Sheet")
    ws.merge_cells("A4:J4")
    ws["A4"] = "Novality Store  ·  Home Renovation Management System"
    ws["A4"].font = font(20, True, PRIMARY)
    ws["A4"].alignment = align("left", "center")
    ws["A4"].fill = fill(BG)

    ws.merge_cells("A5:J6")
    ws["A5"] = (
        "A digital twin of the home: every room, material, contractor, expense, document, task, "
        "photo, warranty and maintenance activity is connected to a place in the house. "
        "This workbook is the complete operating system for a renovation — from first idea through handover and aftercare."
    )
    ws["A5"].alignment = align("left", "center", True)
    ws["A5"].font = font(11, False, TEXT)
    ws["A5"].fill = fill(BG)
    ws.row_dimensions[5].height = 22
    ws.row_dimensions[6].height = 22

    # How to use
    section_label(ws, 8, 1, "How to use (Excel)", 4)
    steps_xl = [
        "1. Enable editing / calculation (Formulas → Automatic).",
        "2. Open Settings. Set Active Project ID (PRJ-001 or PRJ-002).",
        "3. Work in the yellow-ivory input cells. Grey-sand cells are formulas — don't type over them.",
        "4. Add rows above the last data row; copy the formula cells down.",
        "5. Use column filters on every register. Status columns are color-coded.",
        "6. Dashboard, Finance and Admin recalculate from the registers.",
        "7. File → Print uses tabloid landscape and branded headers.",
    ]
    for i, t in enumerate(steps_xl):
        ws.merge_cells(start_row=9 + i, start_column=1, end_row=9 + i, end_column=5)
        ws.cell(9 + i, 1, t).font = font(10)
        ws.cell(9 + i, 1).fill = fill(WHITE)
        ws.row_dimensions[9 + i].height = 18

    section_label(ws, 8, 6, "How to use (Google Sheets)", 4)
    steps_gs = [
        "1. Upload this .xlsx to Google Drive → Open with Google Sheets.",
        "2. File → Save as Google Sheets (keeps formulas, colors, charts).",
        "3. Extensions → Apps Script → paste google_apps_script/Code.gs.",
        "4. Reload the sheet. A “Novality Store” menu appears.",
        "5. Formula cells stay locked in Excel. Google Sheets: Data → Protect sheets.",
        "6. Share with contractors as Commenter or custom-filtered views.",
        "7. Optional: File → Download to keep an Excel archive.",
    ]
    for i, t in enumerate(steps_gs):
        ws.merge_cells(start_row=9 + i, start_column=6, end_row=9 + i, end_column=10)
        ws.cell(9 + i, 6, t).font = font(10)
        ws.cell(9 + i, 6).fill = fill(WHITE)

    # Color system
    section_label(ws, 18, 1, "Color system", 9)
    swatches = [
        (19, 1, PRIMARY, WHITE, "Primary  #16352F  Forest"),
        (19, 3, SECONDARY, TEXT, "Secondary  #E8DDCB  Sand"),
        (19, 5, ACCENT, WHITE, "Accent  #C86B4A  Terracotta"),
        (19, 7, BG, TEXT, "Background  #F8F6F1  Ivory"),
        (20, 1, SUCCESS, WHITE, "Success  #719B7A  Sage"),
        (20, 3, WARNING, TEXT, "Warning  #D99A3D  Amber"),
        (20, 5, DANGER, WHITE, "Danger  #C75C5C  Muted red"),
        (20, 7, FORMULA_BG, TEXT, "Formula cells  (do not type)"),
    ]
    for r, c, bgc, fg, label in swatches:
        ws.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c + 1)
        cell = ws.cell(r, c, label)
        cell.fill = fill(bgc)
        cell.font = font(9, True, fg)
        cell.alignment = align("center", "center")
        ws.row_dimensions[r].height = 22

    # Module index
    section_label(ws, 22, 1, "Module index  (click to jump)", 9)
    modules = [
        ("Dashboard", "Homeowner overview, KPIs, alerts, next tasks"),
        ("Projects", "Multi-project register with live spend"),
        ("Rooms", "Spaces, measurements, budgets, photos"),
        ("Design Studio", "Mood boards, palettes, 2D/3D, AI concepts"),
        ("AI Insights", "Assistant recommendations and savings"),
        ("Budget", "Category + room plan vs actual"),
        ("Expenses", "Transaction log (Planned / Committed / Paid)"),
        ("Finance", "Charts, monthly cash, smart alerts"),
        ("Contractors", "Profiles + Quality / On-time / Budget / Comms score"),
        ("Quotes", "Bid comparison and award"),
        ("Jobs", "Assignments, milestones, balances"),
        ("Tasks", "Kanban fields + health + dependencies"),
        ("Timeline", "Phase Gantt (weekly)"),
        ("Materials", "Procurement pipeline + QR / SKU"),
        ("Shopping List", "Auto list of items still to buy"),
        ("Suppliers", "Lead times and terms"),
        ("Documents", "Project vault + expiry alerts"),
        ("Messages", "Threaded communication log"),
        ("Inventory", "Home contents for insurance"),
        ("Maintenance", "Aftercare hub + reminders"),
        ("Inspections", "City and independent"),
        ("Payments", "Draws and aging"),
        ("Change Orders", "Scope / cost / schedule deltas"),
        ("Permits", "Authorities and expirations"),
        ("Warranties", "Labor and product coverage"),
        ("Calendar", "Visits and deadlines"),
        ("Notifications", "Alert queue"),
        ("Users", "Nine roles"),
        ("Properties", "Multi-home digital twin"),
        ("Admin", "Portfolio analytics"),
        ("Settings", "Currency, thresholds, brand"),
        ("Lookups", "Dropdown lists"),
        ("Audit Log", "Who changed what"),
        ("Roles & Permissions", "Matrix of who can do what"),
    ]
    ws.cell(23, 1, "Sheet").font = font(9, True, WHITE)
    ws.cell(23, 1).fill = fill(PRIMARY)
    ws.cell(23, 2, "What it holds").font = font(9, True, WHITE)
    ws.cell(23, 2).fill = fill(PRIMARY)
    ws.merge_cells("B23:E23")
    ws.cell(23, 6, "Sheet").font = font(9, True, WHITE)
    ws.cell(23, 6).fill = fill(PRIMARY)
    ws.cell(23, 7, "What it holds").font = font(9, True, WHITE)
    ws.cell(23, 7).fill = fill(PRIMARY)
    ws.merge_cells("G23:J23")
    mid = (len(modules) + 1) // 2
    for i, (name, desc) in enumerate(modules):
        if i < mid:
            r = 24 + i
            c_name, c_desc = 1, 2
            ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
        else:
            r = 24 + (i - mid)
            c_name, c_desc = 6, 7
            ws.merge_cells(start_row=r, start_column=7, end_row=r, end_column=10)
        cell = ws.cell(r, c_name, name)
        cell.hyperlink = f"#'{name}'!A1"
        cell.font = font(10, True, ACCENT)
        cell.fill = fill(WHITE if i % 2 == 0 else ROW_ALT)
        cell.border = THIN
        d = ws.cell(r, c_desc, desc)
        d.font = font(9, False, TEXT)
        d.fill = fill(WHITE if i % 2 == 0 else ROW_ALT)
        d.border = THIN

    # Sample story
    story_row = 24 + mid + 2
    section_label(ws, story_row, 1, "Sample story already loaded", 9)
    ws.merge_cells(start_row=story_row + 1, start_column=1, end_row=story_row + 4, end_column=10)
    ws.cell(story_row + 1, 1, (
        "Alex Rivera is renovating 1847 Maplewood Drive, Portland (PRJ-001, $85,000, 72% complete, Construction phase). "
        "Kitchen boxes are going in this week; primary bath is on punch list after an AI-led swap from marble to porcelain "
        "(about 18% saved on that category). Contingency has dipped under 10%, so the exterior water feature is on hold. "
        "A second property — the Columbia Gorge cabin bath (PRJ-002) — is in design so you can see multi-property. "
        "Today in the file is 24 August 2026. Change Settings → Today if you reopen this later."
    ))
    ws.cell(story_row + 1, 1).alignment = align("left", "top", True)
    ws.cell(story_row + 1, 1).font = font(10, False, TEXT)
    ws.cell(story_row + 1, 1).fill = fill(WHITE)

    # Roles
    section_label(ws, story_row + 6, 1, "Roles in this system", 9)
    roles = D.LOOKUPS["Role"]
    for i, role in enumerate(roles):
        c = 1 + i
        cell = ws.cell(story_row + 7, c, role)
        cell.fill = fill(PRIMARY if i % 2 == 0 else ACCENT)
        cell.font = font(8, True, WHITE)
        cell.alignment = align("center", "center", True)
        ws.row_dimensions[story_row + 7].height = 28

    set_col_widths(ws, [22, 18, 16, 16, 16, 22, 18, 16, 16, 16])
    freeze(ws, "A4")
    return ws


def build_roles(wb):
    ws = _sheet(wb, "Roles & Permissions", PRIMARY_SOFT, 12,
                "Who can see and change what  ·  enforce in the live product; this matrix is the source of truth")
    modules = [
        "Dashboard", "Projects", "Rooms", "Design Studio", "AI Insights", "Budget",
        "Expenses", "Finance", "Contractors", "Quotes", "Jobs", "Tasks", "Materials",
        "Documents", "Messages", "Inventory", "Maintenance", "Inspections", "Payments",
        "Change Orders", "Permits", "Admin", "Settings", "Users",
    ]
    roles = D.LOOKUPS["Role"]
    # permission codes: F full, E edit own, V view, A approve, — none
    matrix = {
        "Homeowner": "F F F F V V E V V V V E V F F F F V V A V — — —".split(),
        "Admin": ["F"] * len(modules),
        "Project Manager": "F F F V V F F F F F F F F F F V F F F A F V V V".split(),
        "Interior Designer": "V V F F F V V V V V V F F F F V V — — V — — — —".split(),
        "Contractor": "V V V V — — E — V V F F E V F — V V V V V — — —".split(),
        "Subcontractor": "V V V — — — — — — — F F E V F — — V — — — — — —".split(),
        "Supplier": "— — — — — — — — — V — — F V E — — — V — — — — —".split(),
        "Inspector": "V V V — — — — — V — V V — F V — — F — — F — — —".split(),
        "Accountant": "V V — — — F F F V V V — V F — — — — F V V V — V".split(),
    }
    ws.cell(4, 1, "Module \\ Role").font = font(9, True, WHITE)
    ws.cell(4, 1).fill = fill(PRIMARY)
    for i, role in enumerate(roles, 2):
        cell = ws.cell(4, i, role)
        cell.font = font(8, True, WHITE)
        cell.fill = fill(PRIMARY)
        cell.alignment = align("center", "center", True)
        ws.column_dimensions[get_column_letter(i)].width = 14
    ws.column_dimensions["A"].width = 20
    colors = {"F": SUCCESS, "E": ACCENT, "V": INFO, "A": WARNING, "—": SECONDARY}
    for r_i, mod in enumerate(modules):
        r = 5 + r_i
        ws.cell(r, 1, mod).font = font(9, True, PRIMARY)
        ws.cell(r, 1).fill = fill(WHITE if r_i % 2 == 0 else ROW_ALT)
        ws.cell(r, 1).border = THIN
        for c_i, role in enumerate(roles):
            code = matrix[role][r_i] if r_i < len(matrix[role]) else "—"
            cell = ws.cell(r, c_i + 2, code)
            cell.fill = fill(colors.get(code, SECONDARY))
            cell.font = font(10, True, WHITE if code != "—" else TEXT_MUTED)
            cell.alignment = align("center", "center")
            cell.border = THIN
    input_note(ws, 5 + len(modules) + 1, 1,
               "F = full  ·  E = edit own records  ·  V = view  ·  A = approve  ·  — = no access", 10)
    return ws


# ===========================================================================
# Build all
# ===========================================================================
def build_workbook() -> Workbook:
    wb = Workbook()
    # default sheet recycled as Start Here later
    default = wb.active
    default.title = "_tmp"

    build_lookups(wb)
    build_settings(wb)
    build_properties(wb)
    build_users(wb)
    build_projects(wb)
    build_rooms(wb)
    build_design(wb)
    build_ai(wb)
    build_budget(wb)
    build_expenses(wb)
    build_finance(wb)
    build_contractors(wb)
    build_quotes(wb)
    build_jobs(wb)
    build_tasks(wb)
    build_timeline(wb)
    build_materials(wb)
    build_suppliers(wb)
    build_shopping(wb)
    build_documents(wb)
    build_messages(wb)
    build_inventory(wb)
    build_maintenance(wb)
    build_inspections(wb)
    build_payments(wb)
    build_change_orders(wb)
    build_permits(wb)
    build_warranties(wb)
    build_calendar(wb)
    build_notifications(wb)
    build_audit(wb)
    build_roles(wb)
    build_admin(wb)
    build_dashboard(wb)
    build_start(wb)

    wb.remove(default)

    # Desired tab order
    order = [
        "Start Here", "Dashboard", "Projects", "Rooms", "Design Studio", "AI Insights",
        "Budget", "Expenses", "Finance", "Contractors", "Quotes", "Jobs",
        "Tasks", "Timeline", "Materials", "Shopping List", "Suppliers",
        "Documents", "Messages", "Inventory", "Maintenance",
        "Inspections", "Payments", "Change Orders", "Permits", "Warranties",
        "Calendar", "Notifications", "Users", "Properties", "Roles & Permissions",
        "Admin", "Settings", "Lookups", "Audit Log",
    ]
    for i, name in enumerate(order):
        wb.move_sheet(name, offset=i - wb.sheetnames.index(name))

    wb.calculation.calcMode = "auto"
    wb.calculation.fullCalcOnLoad = True
    wb.properties.title = "Novality Store — Home Renovation Management System"
    wb.properties.creator = "premium"
    wb.properties.lastModifiedBy = "premium"
    wb.properties.description = (
        "Complete home renovation operating system: projects, rooms, design, "
        "budget, contractors, tasks, materials, documents, inventory, maintenance. "
        "Formula cells locked. Unprotect password: premium."
    )
    wb.properties.subject = "Home Renovation Management System"
    wb.properties.keywords = "premium, home renovation, spreadsheet, google sheets"
    wb.properties.category = "Spreadsheets"

    from .protect import protect_workbook

    protect_workbook(wb, password="premium")
    return wb
