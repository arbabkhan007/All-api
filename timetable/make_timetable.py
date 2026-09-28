#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Examination-period timetable generator — Grades 9 & 10 (sections 9A, 9B, 10A, 10B).

Period covered : Thursday 01 Oct 2026 -> Friday 09 Oct 2026 (7 school days, Sat/Sun off)
Friday         : 6 periods; all other days: 8 periods.

Teachers
  Math              Sir Amir
  Physics           Sir Sufyan
  English           Miss Masuda
  Urdu              Miss Humaira
  Islamiyat / PakSt Miss Tahira   (Islamiyat for grade 9, Pakistan Studies for grade 10)
  Chemistry         Sir Iftikhar
  Computer          Sir Wilson
  Quran             Qari Umar Hayat (visiting: never Friday, 2-6 lectures/day,
                                   kept inside periods 2-6, single periods only)

Rules enforced by the model
  R1  Every slot of every class is filled (no free student periods).
  R2  Workload: each full-time teacher exactly 27 lectures; Qari 19 (less - visiting).
  R3  A teacher can never be in two classes at the same period.
  R4  Max 7 lectures per teacher per day (non-duty days capped at 6 for balance).
  R5  Every day exactly 2 full-time teachers are on EXAM DUTY:
      zero lectures in periods 1-4, then 2-3 lectures in periods 5-8
      (on 6-period Fridays: 1-2 lectures in periods 5-6).
  R6  Non-Quran subjects may use block lectures (2 consecutive periods);
      a subject meets a class at most once a day (one single or one block).
  R7  Quran: single periods only, periods 2-6, never on Friday, <=1 per day,
      minimum 4 per class (we give 4-5).
  R8  Duty rotates fairly: every full-time teacher has exactly 2 duty days.

Outputs: Exam_Timetable_G9_G10.xlsx and Exam_Timetable_G9_G10.html
"""

from __future__ import annotations

import html as H
import os
import sys

from ortools.sat.python import cp_model

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------- #
#  Configuration
# --------------------------------------------------------------------------- #
DAYS = [
    ("Thursday",  "01 Oct", 8),
    ("Friday",    "02 Oct", 6),
    ("Monday",    "05 Oct", 8),
    ("Tuesday",   "06 Oct", 8),
    ("Wednesday", "07 Oct", 8),
    ("Thursday",  "08 Oct", 8),
    ("Friday",    "09 Oct", 6),
]
ND = len(DAYS)
PERIODS_OF = [d[2] for d in DAYS]
IS_FRIDAY = [d[0] == "Friday" for d in DAYS]
DAY_LABEL = [f"{d[0]} {d[1]}" for d in DAYS]
DAY_SHORT = [f"{d[0][:3]} {d[1].split()[0]}" for d in DAYS]

SECTIONS = ["9A", "9B", "10A", "10B"]
COMMON = ["English", "Urdu", "Math", "Physics", "Chemistry", "Computer"]
GRADE_SUBJ = {"9": "Islamiyat", "10": "Pakistan Studies"}

TEACHER = {
    "English": "Miss Masuda",
    "Urdu": "Miss Humaira",
    "Math": "Sir Amir",
    "Physics": "Sir Sufyan",
    "Chemistry": "Sir Iftikhar",
    "Computer": "Sir Wilson",
    "Islamiyat": "Miss Tahira",
    "Pakistan Studies": "Miss Tahira",
    "Quran": "Qari Umar Hayat",
}
SUBJ_OF_TEACHER = {
    "Sir Amir": "Math", "Sir Sufyan": "Physics", "Miss Masuda": "English",
    "Miss Humaira": "Urdu", "Miss Tahira": "Islamiyat / Pak Studies",
    "Sir Iftikhar": "Chemistry", "Sir Wilson": "Computer",
    "Qari Umar Hayat": "Quran",
}
FULLTIMERS = ["Miss Masuda", "Miss Humaira", "Sir Amir", "Sir Sufyan",
              "Miss Tahira", "Sir Iftikhar", "Sir Wilson"]
QARI = "Qari Umar Hayat"
ALL_TEACHERS = FULLTIMERS + [QARI]

# Lecture counts per class over the whole 7-day period.
# Totals: every full-time teacher = 27, Qari = 19, grand total = 208 (full grid).
COUNTS = {
    "9A":  {"English": 6, "Urdu": 6, "Math": 7, "Physics": 7, "Chemistry": 7,
            "Computer": 7, "Islamiyat": 7, "Quran": 5},
    "9B":  {"English": 7, "Urdu": 7, "Math": 6, "Physics": 6, "Chemistry": 7,
            "Computer": 7, "Islamiyat": 7, "Quran": 5},
    "10A": {"English": 7, "Urdu": 7, "Math": 7, "Physics": 7, "Chemistry": 6,
            "Computer": 6, "Pakistan Studies": 7, "Quran": 5},
    "10B": {"English": 7, "Urdu": 7, "Math": 7, "Physics": 7, "Chemistry": 7,
            "Computer": 7, "Pakistan Studies": 6, "Quran": 4},
}

# Exam-duty roster: day -> the two full-time teachers on duty (each teacher 2 days).
DUTY = {
    0: ("Sir Amir", "Sir Sufyan"),
    1: ("Miss Masuda", "Miss Humaira"),
    2: ("Miss Tahira", "Sir Iftikhar"),
    3: ("Sir Wilson", "Sir Amir"),
    4: ("Sir Sufyan", "Miss Masuda"),
    5: ("Miss Humaira", "Miss Tahira"),
    6: ("Sir Iftikhar", "Sir Wilson"),
}

MAX_PER_DAY = 7      # R4: hard user limit
NON_DUTY_CAP = 6     # balance cap on non-duty days (still <= 7)
Q_WINDOW = (2, 6)    # R7: Quran allowed in periods 2..6 (1-indexed)

SUBJECTS = {s: COMMON + [GRADE_SUBJ["9" if s[0] == "9" else "10"], "Quran"]
            for s in SECTIONS}

# --------------------------------------------------------------------------- #
#  Model
# --------------------------------------------------------------------------- #
def build_model():
    m = cp_model.CpModel()
    x = {}
    for si, sec in enumerate(SECTIONS):
        for d in range(ND):
            for p in range(PERIODS_OF[d]):
                for sub in SUBJECTS[sec]:
                    x[si, d, p, sub] = m.NewBoolVar(f"x_{si}_{d}_{p}_{sub[:3]}")

    # R1: fill every slot exactly once
    for si, sec in enumerate(SECTIONS):
        for d in range(ND):
            for p in range(PERIODS_OF[d]):
                m.AddExactlyOne([x[si, d, p, sub] for sub in SUBJECTS[sec]])

    # R2: per-class subject totals
    for si, sec in enumerate(SECTIONS):
        for sub in SUBJECTS[sec]:
            m.Add(sum(x[si, d, p, sub]
                      for d in range(ND) for p in range(PERIODS_OF[d]))
                  == COUNTS[sec][sub])

    # teacher -> [(section_idx, subject)]
    pairs = {}
    for si, sec in enumerate(SECTIONS):
        for sub in SUBJECTS[sec]:
            pairs.setdefault(TEACHER[sub], []).append((si, sub))

    # R3: no teacher in two places at once
    for t, plist in pairs.items():
        for d in range(ND):
            for p in range(PERIODS_OF[d]):
                m.Add(sum(x[si, d, p, sub] for si, sub in plist) <= 1)

    # R5: exam duty
    for d in range(ND):
        for t in DUTY[d]:
            plist = pairs[t]
            for p in range(min(4, PERIODS_OF[d])):
                for si, sub in plist:
                    m.Add(x[si, d, p, sub] == 0)
            tot = sum(x[si, d, p, sub]
                      for si, sub in plist for p in range(PERIODS_OF[d]))
            if not IS_FRIDAY[d]:
                m.Add(tot >= 2)
                m.Add(tot <= 3)
            else:
                m.Add(tot >= 1)
                m.Add(tot <= 2)

    # R4: daily caps
    for t in FULLTIMERS:
        plist = pairs[t]
        for d in range(ND):
            if t in DUTY[d]:
                continue  # already bounded by duty rule
            tot = sum(x[si, d, p, sub]
                      for si, sub in plist for p in range(PERIODS_OF[d]))
            m.Add(tot <= NON_DUTY_CAP)

    # R7: Quran placement
    lo, hi = Q_WINDOW  # 1-indexed inclusive
    for si, sec in enumerate(SECTIONS):
        for d in range(ND):
            for p in range(PERIODS_OF[d]):
                if IS_FRIDAY[d] or not (lo - 1 <= p <= hi - 1):
                    m.Add(x[si, d, p, "Quran"] == 0)
            m.Add(sum(x[si, d, p, "Quran"] for p in range(PERIODS_OF[d])) <= 1)

    # R6: a subject meets a class at most once a day, as 1 single or 1 block (2 adjacent)
    for si, sec in enumerate(SECTIONS):
        for d in range(ND):
            P = PERIODS_OF[d]
            for sub in SUBJECTS[sec]:
                vs = [x[si, d, p, sub] for p in range(P)]
                m.Add(sum(vs) <= 2)
                for p in range(P):
                    for q in range(p + 2, P):
                        m.Add(vs[p] + vs[q] <= 1)

    # Objective: maximise block (double) periods - fewer, longer sessions.
    blocks = []
    for si, sec in enumerate(SECTIONS):
        for d in range(ND):
            for p in range(PERIODS_OF[d] - 1):
                for sub in SUBJECTS[sec]:
                    if sub == "Quran":
                        continue
                    b = m.NewBoolVar(f"b_{si}_{d}_{p}_{sub[:3]}")
                    a, c = x[si, d, p, sub], x[si, d, p + 1, sub]
                    m.Add(b <= a)
                    m.Add(b <= c)
                    m.Add(b >= a + c - 1)
                    blocks.append(b)
    m.Maximize(sum(blocks))
    return m, x


def solve(model):
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 60.0
    solver.parameters.num_search_workers = 8
    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print("SOLVER FAILED:", solver.StatusName(status))
        sys.exit(1)
    return solver, status


def extract(solver, x):
    grid = [[[None] * PERIODS_OF[d] for d in range(ND)] for _ in SECTIONS]
    for si, sec in enumerate(SECTIONS):
        for d in range(ND):
            for p in range(PERIODS_OF[d]):
                for sub in SUBJECTS[sec]:
                    if solver.Value(x[si, d, p, sub]):
                        grid[si][d][p] = sub
    return grid

# --------------------------------------------------------------------------- #
#  Analysis + verification (independent re-check of every rule)
# --------------------------------------------------------------------------- #
def analyze(grid):
    st = {"sec_counts": {}, "tday": {}, "ttotal": {}, "duty_days": {},
          "qari_day": {}, "blocks": 0}
    for si, sec in enumerate(SECTIONS):
        st["sec_counts"][sec] = {sub: 0 for sub in SUBJECTS[sec]}
        for d in range(ND):
            for p in range(PERIODS_OF[d]):
                st["sec_counts"][sec][grid[si][d][p]] += 1
    for t in ALL_TEACHERS:
        st["tday"][t] = [0] * ND
        st["duty_days"][t] = [d for d in range(ND) if t in DUTY.get(d, ())]
    for si, sec in enumerate(SECTIONS):
        for d in range(ND):
            for p in range(PERIODS_OF[d]):
                t = TEACHER[grid[si][d][p]]
                st["tday"][t][d] += 1
    for t in ALL_TEACHERS:
        st["ttotal"][t] = sum(st["tday"][t])
    st["qari_day"] = st["tday"][QARI]
    for si, sec in enumerate(SECTIONS):
        for d in range(ND):
            for p in range(PERIODS_OF[d] - 1):
                if grid[si][d][p] == grid[si][d][p + 1] != "Quran":
                    st["blocks"] += 1
    return st


def verify(grid, st):
    errs = []
    # R1 + subject validity
    for si, sec in enumerate(SECTIONS):
        for d in range(ND):
            for p in range(PERIODS_OF[d]):
                if grid[si][d][p] not in SUBJECTS[sec]:
                    errs.append(f"R1: bad slot {sec} {DAY_LABEL[d]} P{p+1}")
    # R2 counts + totals
    for sec in SECTIONS:
        for sub in SUBJECTS[sec]:
            if st["sec_counts"][sec][sub] != COUNTS[sec][sub]:
                errs.append(f"R2: {sec} {sub} = {st['sec_counts'][sec][sub]} "
                            f"(want {COUNTS[sec][sub]})")
    for t in FULLTIMERS:
        if st["ttotal"][t] != 27:
            errs.append(f"R2: {t} total {st['ttotal'][t]} != 27")
    if st["ttotal"][QARI] != 19:
        errs.append(f"R2: Qari total {st['ttotal'][QARI]} != 19")
    # R3 conflicts
    for d in range(ND):
        for p in range(PERIODS_OF[d]):
            ts = [TEACHER[grid[si][d][p]] for si in range(4)]
            if len(set(ts)) != 4:
                errs.append(f"R3: clash {DAY_LABEL[d]} P{p+1}: {ts}")
    # R4 caps
    for t in ALL_TEACHERS:
        for d in range(ND):
            n = st["tday"][t][d]
            if n > MAX_PER_DAY:
                errs.append(f"R4: {t} {DAY_LABEL[d]} = {n} > {MAX_PER_DAY}")
            if t in FULLTIMERS and t not in DUTY[d] and n > NON_DUTY_CAP:
                errs.append(f"R4b: {t} {DAY_LABEL[d]} = {n} > {NON_DUTY_CAP}")
    # R5 duty
    for d in range(ND):
        for t in DUTY[d]:
            morning = sum(1 for si in range(4) for p in range(min(4, PERIODS_OF[d]))
                          if TEACHER[grid[si][d][p]] == t)
            if morning:
                errs.append(f"R5: {t} teaches P1-4 on {DAY_LABEL[d]}")
            n = st["tday"][t][d]
            if IS_FRIDAY[d] and not (1 <= n <= 2):
                errs.append(f"R5: {t} Friday duty load {n} not in 1..2")
            if not IS_FRIDAY[d] and not (2 <= n <= 3):
                errs.append(f"R5: {t} duty load {n} not in 2..3")
    # R6 runs
    for si, sec in enumerate(SECTIONS):
        for d in range(ND):
            seen = {}
            for p in range(PERIODS_OF[d]):
                seen.setdefault(grid[si][d][p], []).append(p)
            for sub, ps in seen.items():
                if len(ps) > 2 or (len(ps) == 2 and ps[1] != ps[0] + 1):
                    errs.append(f"R6: {sec} {DAY_LABEL[d]} {sub} at {ps}")
                if sub == "Quran" and len(ps) > 1:
                    errs.append(f"R7: Quran block in {sec} {DAY_LABEL[d]}")
    # R7 Quran rules
    lo, hi = Q_WINDOW
    for si, sec in enumerate(SECTIONS):
        for d in range(ND):
            for p in range(PERIODS_OF[d]):
                if grid[si][d][p] == "Quran":
                    if IS_FRIDAY[d]:
                        errs.append(f"R7: Quran on Friday {sec}")
                    if not (lo <= p + 1 <= hi):
                        errs.append(f"R7: Quran at P{p+1} {sec} {DAY_LABEL[d]}")
    for d in range(ND):
        if not IS_FRIDAY[d] and not (2 <= st["qari_day"][d] <= 6):
            errs.append(f"R7: Qari {DAY_LABEL[d]} = {st['qari_day'][d]} not in 2..6")
    # R8 duty rotation
    for t in FULLTIMERS:
        if len(st["duty_days"][t]) != 2:
            errs.append(f"R8: {t} duty days = {st['duty_days'][t]}")
    if errs:
        print("VERIFICATION FAILED:")
        for e in errs:
            print("  -", e)
        sys.exit(2)
    print("VERIFICATION PASSED — all rules satisfied.\n")

# --------------------------------------------------------------------------- #
#  Console report
# --------------------------------------------------------------------------- #
def print_report(grid, st):
    print("Workload per teacher (lectures/day):")
    print("  Teacher            " + " ".join(f"{s:>6}" for s in DAY_SHORT) + "  total")
    for t in ALL_TEACHERS:
        row = " ".join(f"{n:>6}" for n in st["tday"][t])
        duty = ",".join(str(d + 1) for d in st["duty_days"][t])
        print(f"  {t:<18} {row}  {st['ttotal'][t]:>3}   duty: day {duty or '-'}")
    print(f"\n  Blocks (double periods): {st['blocks']}")
    print("  Lectures per class:")
    for sec in SECTIONS:
        print("   ", sec, {k: v for k, v in st["sec_counts"][sec].items()})

# --------------------------------------------------------------------------- #
#  Excel output
# --------------------------------------------------------------------------- #
FILLS = {
    "English":          ("305496", "FFFFFF"),
    "Urdu":             ("C55A11", "FFFFFF"),
    "Math":             ("548235", "FFFFFF"),
    "Physics":          ("BF9000", "000000"),
    "Chemistry":        ("7030A0", "FFFFFF"),
    "Computer":         ("00B0F0", "000000"),
    "Islamiyat":        ("C00000", "FFFFFF"),
    "Pakistan Studies": ("C00000", "FFFFFF"),
    "Quran":            ("A9D08E", "375623"),
}
DUTY_FILL = "F4B183"
GRAY_FILL = "D9D9D9"
FREE_FILL = "F2F2F2"


def write_excel(path, grid, st):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter

    thin = Side(style="thin", color="808080")
    BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
    CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
    LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)

    wb = Workbook()

    # ---------------- overview ----------------
    ov = wb.active
    ov.title = "Overview"
    ov.sheet_view.showGridLines = False
    ov.column_dimensions["A"].width = 26
    ov.column_dimensions["B"].width = 24
    for c in "CDEFGHI":
        ov.column_dimensions[c].width = 9
    ov.column_dimensions["J"].width = 9
    ov.column_dimensions["K"].width = 34

    def put(cell, value, bold=False, size=11, color="000000", fill=None,
            align=None, italic=False):
        c = ov[cell]
        c.value = value
        c.font = Font(bold=bold, size=size, color=color, italic=italic)
        if fill:
            c.fill = PatternFill("solid", fgColor=fill)
        c.alignment = align or LEFT
        return c

    put("A1", "Grades 9 & 10 — Examination Period Timetable", bold=True, size=15)
    put("A2", "Thursday 01 Oct 2026 – Friday 09 Oct 2026  (7 school days, Sat & Sun off)",
        italic=True, size=10, color="595959")
    rules = [
        ("Days / periods", "Thursday 01, Friday 02, Monday 05, Tuesday 06, Wednesday 07, Thursday 08, Friday 09 Oct. "
                           "Friday = 6 periods; all other days = 8 periods."),
        ("Classes", "9A, 9B (Islamiyat) • 10A, 10B (Pakistan Studies)"),
        ("Exam duty", "2 teachers daily — FREE periods 1–4 for exam duty; they teach only 2–3 lectures in periods 5–8 "
                      "(Friday: 1–2 lectures in periods 5–6). Each teacher gets exactly 2 duty days."),
        ("Workload", "Every full-time teacher: exactly 27 lectures (equal). Qari Umar Hayat (visiting): 19 lectures."),
        ("Daily limit", "Max 7 lectures per teacher per day (balanced to max 6 on non-duty days)."),
        ("Blocks", "All subjects except Quran may use block lectures (2 consecutive periods); "
                   "a subject meets a class once per day (single or block)."),
        ("Quran", "Single periods, periods 2–6 only, never on Friday; 4–5 lectures per class; "
                  "Qari teaches 2–6 lectures per working day."),
        ("Lectures per subject", "6–7 per class over the 7 days (52 periods per class; 8-per-subject "
                                 "would need 60 periods, so 27-per-teacher equal load is the maximum possible)."),
    ]
    r = 4
    put(f"A{r}", "Rules & assumptions", bold=True, size=12)
    r += 1
    for k, v in rules:
        put(f"A{r}", k, bold=True)
        ov.merge_cells(f"B{r}:J{r}")
        put(f"B{r}", v)
        r += 1

    r += 1
    put(f"A{r}", "Exam-duty roster (periods 1–4 free)", bold=True, size=12)
    r += 1
    hdr = ["Day", "Date", "Duty teacher 1", "Duty teacher 2", "Note"]
    for i, h in enumerate(hdr):
        c = ov.cell(row=r, column=1 + i if i < 4 else 9, value=h)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F3864")
        c.alignment = CENTER
    ov.merge_cells(start_row=r, start_column=9, end_row=r, end_column=10)
    r += 1
    for d in range(ND):
        ov.cell(row=r, column=1, value=DAYS[d][0]).font = Font(bold=True)
        ov.cell(row=r, column=2, value=DAYS[d][1])
        for j, t in enumerate(DUTY[d]):
            c = ov.cell(row=r, column=3 + j, value=t)
            c.fill = PatternFill("solid", fgColor=DUTY_FILL)
        c = ov.cell(row=r, column=9,
                    value="Fri: teach max 2 (P5–P6)" if IS_FRIDAY[d]
                    else "Teach 2–3 (P5–P8)")
        ov.merge_cells(start_row=r, start_column=9, end_row=r, end_column=10)
        r += 1

    r += 1
    put(f"A{r}", "Teacher workload", bold=True, size=12)
    r += 1
    head = ["Teacher", "Subject"] + DAY_SHORT + ["Total", "Duty days"]
    for i, h in enumerate(head):
        c = ov.cell(row=r, column=1 + i, value=h)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F3864")
        c.alignment = CENTER
    r += 1
    for t in ALL_TEACHERS:
        ov.cell(row=r, column=1, value=t).font = Font(bold=True)
        ov.cell(row=r, column=2, value=SUBJ_OF_TEACHER[t])
        for d in range(ND):
            c = ov.cell(row=r, column=3 + d, value=st["tday"][t][d])
            c.alignment = CENTER
            if t in DUTY[d]:
                c.fill = PatternFill("solid", fgColor=DUTY_FILL)
        c = ov.cell(row=r, column=10, value=st["ttotal"][t])
        c.font = Font(bold=True)
        c.alignment = CENTER
        ov.cell(row=r, column=11,
                value=", ".join(DAY_LABEL[d] for d in st["duty_days"][t]) or "—")
        r += 1

    r += 1
    put(f"A{r}", "Lectures per class (7-day totals)", bold=True, size=12)
    r += 1
    subs = SUBJECTS["9A"]
    for i, h in enumerate(["Subject"] + SECTIONS + ["Teacher"]):
        c = ov.cell(row=r, column=1 + i, value=h)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F3864")
        c.alignment = CENTER
    r += 1
    for sub in subs:
        name = sub if sub != "Islamiyat" else "Islamiyat (9) / Pak.St (10)"
        ov.cell(row=r, column=1, value=name).font = Font(bold=True)
        for i, sec in enumerate(SECTIONS):
            key = sub
            if sub == "Islamiyat" and sec.startswith("10"):
                key = "Pakistan Studies"
            c = ov.cell(row=r, column=2 + i, value=st["sec_counts"][sec][key])
            c.alignment = CENTER
        ov.cell(row=r, column=6, value=TEACHER[sub])
        ov.cell(row=r, column=1).fill = PatternFill("solid", fgColor=FILLS[sub][0])
        ov.cell(row=r, column=1).font = Font(bold=True, color=FILLS[sub][1])
        r += 1

    # ---------------- class sheets ----------------
    for si, sec in enumerate(SECTIONS):
        ws = wb.create_sheet(sec)
        ws.sheet_view.showGridLines = False
        ws.column_dimensions["A"].width = 15
        for c in range(2, 10):
            ws.column_dimensions[get_column_letter(c)].width = 16.5
        ws.merge_cells("A1:I1")
        t = ws["A1"]
        t.value = f"CLASS {sec} — Exam-period timetable ({DAY_LABEL[0]} – {DAY_LABEL[-1]} 2026)"
        t.font = Font(bold=True, size=13)
        t.alignment = CENTER
        ws.merge_cells("A2:I2")
        s = ws["A2"]
        s.value = ("Blocks = 2 consecutive periods • Friday = 6 periods • "
                   "Quran: single period, P2–P6, Mon–Thu only")
        s.font = Font(italic=True, size=9, color="595959")
        s.alignment = CENTER

        hdr = ws.cell(row=3, column=1, value="Day / Date")
        hdr.font = Font(bold=True, color="FFFFFF")
        hdr.fill = PatternFill("solid", fgColor="1F3864")
        hdr.alignment = CENTER
        hdr.border = BORDER
        for p in range(8):
            c = ws.cell(row=3, column=2 + p, value=f"Period {p+1}")
            c.font = Font(bold=True, color="FFFFFF")
            c.fill = PatternFill("solid", fgColor="1F3864")
            c.alignment = CENTER
            c.border = BORDER
        ws.row_dimensions[3].height = 18

        for d in range(ND):
            row = 4 + d
            ws.row_dimensions[row].height = 32
            dc = ws.cell(row=row, column=1, value=DAY_LABEL[d])
            dc.font = Font(bold=True)
            dc.alignment = CENTER
            dc.border = BORDER
            dc.fill = PatternFill("solid", fgColor="DEEAF6" if not IS_FRIDAY[d] else "FCE4D6")
            p = 0
            while p < PERIODS_OF[d]:
                sub = grid[si][d][p]
                run = 1
                if (p + 1 < PERIODS_OF[d] and grid[si][d][p + 1] == sub
                        and sub != "Quran"):
                    run = 2
                bg, fg = FILLS[sub]
                for k in range(run):
                    c = ws.cell(row=row, column=2 + p + k)
                    c.fill = PatternFill("solid", fgColor=bg)
                    c.border = BORDER
                c = ws.cell(row=row, column=2 + p, value=f"{sub}\n{TEACHER[sub]}")
                c.font = Font(bold=True, size=10, color=fg)
                c.alignment = CENTER
                if run == 2:
                    ws.merge_cells(start_row=row, start_column=2 + p,
                                   end_row=row, end_column=3 + p)
                p += run
            for p in range(PERIODS_OF[d], 8):
                c = ws.cell(row=row, column=2 + p, value="—")
                c.fill = PatternFill("solid", fgColor=GRAY_FILL)
                c.alignment = CENTER
                c.border = BORDER
                c.font = Font(color="808080")
        ws.freeze_panes = "B4"

    # ---------------- teacher sheets ----------------
    ws = wb.create_sheet("Teachers")
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 15
    for c in range(2, 10):
        ws.column_dimensions[get_column_letter(c)].width = 11
    ws.column_dimensions["J"].width = 8
    row = 1
    for t in ALL_TEACHERS:
        title = (f"{t}  —  {SUBJ_OF_TEACHER[t]}  |  {st['ttotal'][t]} lectures  |  "
                 + (", ".join(DAY_LABEL[d] for d in st["duty_days"][t])
                    if st["duty_days"][t] else "no exam duty (visiting)"))
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=10)
        c = ws.cell(row=row, column=1, value=title)
        c.font = Font(bold=True, size=12, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F3864")
        c.alignment = LEFT
        ws.row_dimensions[row].height = 20
        row += 1
        for i, h in enumerate(["Day"] + [f"P{p+1}" for p in range(8)] + ["Total"]):
            c = ws.cell(row=row, column=1 + i, value=h)
            c.font = Font(bold=True)
            c.fill = PatternFill("solid", fgColor="D6DCE4")
            c.alignment = CENTER
            c.border = BORDER
        row += 1
        for d in range(ND):
            dc = ws.cell(row=row, column=1, value=DAY_LABEL[d])
            dc.font = Font(bold=True)
            dc.alignment = CENTER
            dc.border = BORDER
            if IS_FRIDAY[d]:
                dc.fill = PatternFill("solid", fgColor="FCE4D6")
            if t == QARI and IS_FRIDAY[d]:
                ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=9)
                c = ws.cell(row=row, column=2, value="NOT AVAILABLE (Friday)")
                c.fill = PatternFill("solid", fgColor=GRAY_FILL)
                c.alignment = CENTER
                c.font = Font(italic=True, color="808080")
                ws.cell(row=row, column=10, value=0).alignment = CENTER
                row += 1
                continue
            on_duty = t in DUTY[d]
            if on_duty:
                for col in range(2, 6):
                    ws.cell(row=row, column=col).fill = PatternFill(
                        "solid", fgColor=DUTY_FILL)
                    ws.cell(row=row, column=col).border = BORDER
                ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=5)
                c = ws.cell(row=row, column=2, value="EXAM DUTY (P1–P4)")
                c.font = Font(bold=True, color="843C0C")
                c.alignment = CENTER
            for p in range(PERIODS_OF[d]):
                if on_duty and p < 4:
                    continue
                c = ws.cell(row=row, column=2 + p)
                c.alignment = CENTER
                c.border = BORDER
                si = None
                for i in range(4):
                    if TEACHER[grid[i][d][p]] == t:
                        si = i
                        break
                if si is None:
                    c.value = ""
                    c.fill = PatternFill("solid", fgColor=FREE_FILL)
                else:
                    c.value = SECTIONS[si]
                    bg, fg = FILLS[grid[si][d][p]]
                    c.fill = PatternFill("solid", fgColor=bg)
                    c.font = Font(bold=True, color=fg)
            for p in range(PERIODS_OF[d], 8):
                c = ws.cell(row=row, column=2 + p, value="—")
                c.fill = PatternFill("solid", fgColor=GRAY_FILL)
                c.alignment = CENTER
                c.border = BORDER
                c.font = Font(color="808080")
            tot = ws.cell(row=row, column=10, value=st["tday"][t][d])
            tot.font = Font(bold=True)
            tot.alignment = CENTER
            tot.border = BORDER
            if on_duty:
                tot.fill = PatternFill("solid", fgColor=DUTY_FILL)
            row += 1
        row += 2
    wb.save(path)
    print("wrote", path)

# --------------------------------------------------------------------------- #
#  HTML output (printable)
# --------------------------------------------------------------------------- #
def write_html(path, grid, st):
    css_palette = {k: f"background:{('#'+v[0])};color:{('#'+v[1])}"
                   for k, v in FILLS.items()}
    parts = []
    A = parts.append
    A("<!doctype html><html><head><meta charset='utf-8'>")
    A("<title>Grades 9 &amp; 10 — Examination Period Timetable</title>")
    A("""<style>
    body{font-family:'Segoe UI',Arial,sans-serif;margin:16px;color:#222}
    h1{font-size:22px;margin:4px 0} h2{font-size:16px;margin:22px 0 6px}
    .sub{color:#666;font-size:12px;margin-bottom:12px}
    table{border-collapse:collapse;margin-bottom:6px}
    th,td{border:1px solid #9aa5b1;padding:4px 6px;font-size:11px;text-align:center}
    th{background:#1f3864;color:#fff;font-weight:600}
    td.day{background:#deeaf6;font-weight:700;text-align:left;white-space:nowrap}
    tr.fri td.day{background:#fce4d6}
    td.na{background:#d9d9d9;color:#888}
    td.free{background:#f4f6f8}
    td.duty{background:#f4b183;color:#843c0c;font-weight:700}
    td small{display:block;font-weight:400;font-size:9px;opacity:.9}
    .legend span{display:inline-block;padding:3px 8px;margin:2px;font-size:11px;border-radius:3px}
    .note{font-size:11px;color:#555;margin:6px 0 14px}
    .grid{display:flex;flex-wrap:wrap;gap:24px}
    .tb{font-size:11px;color:#666;margin-top:2px}
    @media print{
      @page{size:A4 landscape;margin:8mm}
      body{margin:0}
      .pb{page-break-before:always}
      h2{margin-top:6px}
      table{page-break-inside:avoid}
    }
    </style></head><body>""")
    A("<h1>Grades 9 &amp; 10 — Examination Period Timetable</h1>")
    A("<div class='sub'>Thursday 01 Oct 2026 – Friday 09 Oct 2026 &nbsp;•&nbsp; "
      "7 school days (Sat &amp; Sun off) &nbsp;•&nbsp; Friday = 6 periods, other days = 8 periods</div>")
    A("<div class='legend'>")
    for sub in SUBJECTS["9A"]:
        n = "Islamiyat / Pak. Studies" if sub == "Islamiyat" else sub
        A(f"<span style='{css_palette[sub]}'>{n}</span>")
    A("<span style='background:#f4b183;color:#843c0c'>Exam duty</span></div>")

    # duty roster
    A("<h2>Exam-duty roster — 2 teachers daily, periods 1–4 free</h2>")
    A("<table><tr><th>Day</th><th>Duty teacher 1</th><th>Duty teacher 2</th>"
      "<th>Duty timing</th></tr>")
    for d in range(ND):
        A(f"<tr class='{'fri' if IS_FRIDAY[d] else ''}'><td class='day'>{DAY_LABEL[d]}</td>"
          f"<td>{DUTY[d][0]}</td><td>{DUTY[d][1]}</td>"
          f"<td>Free P1–P4; teach "
          f"{'1–2 in P5–P6' if IS_FRIDAY[d] else '2–3 in P5–P8'}</td></tr>")
    A("</table>")
    A("<div class='note'>Every full-time teacher gets exactly 2 duty days. "
      "Duty teachers have no lectures during periods 1–4 (exam supervision), "
      "then teach 2–3 lectures in the later periods.</div>")

    # section tables
    A("<h2 class='pb'>Class timetables</h2>")
    A("<div class='grid'>")
    for si, sec in enumerate(SECTIONS):
        A(f"<div><h3 style='margin:4px 0'>Class {sec}</h3><table>")
        A("<tr><th>Day</th>" + "".join(f"<th>P{p+1}</th>" for p in range(8)) + "</tr>")
        for d in range(ND):
            A(f"<tr class='{'fri' if IS_FRIDAY[d] else ''}'><td class='day'>{DAY_LABEL[d]}</td>")
            p = 0
            cells = []
            while p < PERIODS_OF[d]:
                sub = grid[si][d][p]
                run = 2 if (p + 1 < PERIODS_OF[d] and grid[si][d][p + 1] == sub
                            and sub != "Quran") else 1
                tshort = TEACHER[sub].replace("Qari Umar Hayat", "Qari U.H.")
                cells.append(f"<td colspan='{run}' style='{css_palette[sub]}'>"
                             f"{sub}<small>{tshort}</small></td>")
                p += run
            for p in range(PERIODS_OF[d], 8):
                cells.append("<td class='na'>–</td>")
            A("".join(cells) + "</tr>")
        A("</table></div>")
    A("</div>")
    A("<div class='note'>Blocks = two consecutive periods of one subject. "
      "Quran is always a single period, scheduled in periods 2–6, Monday–Thursday only.</div>")

    # teacher tables
    A("<h2 class='pb'>Teacher timetables</h2>")
    for t in ALL_TEACHERS:
        duty_txt = (", ".join(DAY_LABEL[d] for d in st["duty_days"][t])
                    if st["duty_days"][t] else "no exam duty (visiting teacher)")
        A(f"<h3 style='margin:12px 0 2px'>{t} — {SUBJ_OF_TEACHER[t]} "
          f"({st['ttotal'][t]} lectures) <span style='color:#843C0C'>• Duty: {duty_txt}</span></h3>")
        A("<table><tr><th>Day</th>" + "".join(f"<th>P{p+1}</th>" for p in range(8))
          + "<th>Total</th></tr>")
        for d in range(ND):
            A(f"<tr class='{'fri' if IS_FRIDAY[d] else ''}'><td class='day'>{DAY_LABEL[d]}</td>")
            if t == QARI and IS_FRIDAY[d]:
                A("<td colspan='8' class='na'>NOT AVAILABLE (Friday)</td>")
            else:
                on_duty = t in DUTY[d]
                if on_duty:
                    A("<td colspan='4' class='duty'>EXAM DUTY</td>")
                for p in range(PERIODS_OF[d]):
                    if on_duty and p < 4:
                        continue
                    si = None
                    for i in range(4):
                        if TEACHER[grid[i][d][p]] == t:
                            si = i
                            break
                    if si is None:
                        A("<td class='free'>Free</td>")
                    else:
                        sub = grid[si][d][p]
                        A(f"<td style='{css_palette[sub]}'>{SECTIONS[si]}</td>")
                for p in range(PERIODS_OF[d], 8):
                    A("<td class='na'>–</td>")
            A(f"<td><b>{st['tday'][t][d]}</b></td></tr>")
        A("</table>")

    # workload table
    A("<h2 class='pb'>Workload summary</h2>")
    A("<table><tr><th>Teacher</th><th>Subject</th>"
      + "".join(f"<th>{s}</th>" for s in DAY_SHORT)
      + "<th>Total</th><th>Duty days</th></tr>")
    for t in ALL_TEACHERS:
        duty = (", ".join(DAY_LABEL[d] for d in st["duty_days"][t])
                if st["duty_days"][t] else "—")
        A(f"<tr><td style='text-align:left'><b>{t}</b></td>"
          f"<td>{SUBJ_OF_TEACHER[t]}</td>"
          + "".join(f"<td{' style=background:#f4b183' if t in DUTY[d] else ''}>"
                    f"{st['tday'][t][d]}</td>" for d in range(ND))
          + f"<td><b>{st['ttotal'][t]}</b></td><td>{duty}</td></tr>")
    A("</table>")
    A("<div class='note'>All full-time teachers: exactly 27 lectures (equal workload). "
      "Qari Umar Hayat: 19 lectures (visiting, fewer by design; never on Friday; "
      "2–6 lectures per working day, periods 2–6 only).<br>"
      "Lectures per subject per class: 6–7 over the 7 days (52 periods per class; "
      "8-per-subject would require 60 periods per class, which is impossible).<br>"
      "Dates assumed: exams start Thursday 01 Oct 2026 — regenerate if different.</div>")
    A("</body></html>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(parts))
    print("wrote", path)

# --------------------------------------------------------------------------- #
def main():
    import json
    cache = os.path.join(HERE, "grid_cache.json")
    if os.path.exists(cache) and os.environ.get("TT_NOCACHE") != "1":
        with open(cache) as f:
            grid = json.load(f)
        print("loaded cached timetable")
    else:
        model, x = build_model()
        solver, status = solve(model)
        print("Solver status:", solver.StatusName(status),
              f"({solver.WallTime():.1f}s, objective={solver.ObjectiveValue():.0f} blocks)")
        grid = extract(solver, x)
        with open(cache, "w") as f:
            json.dump(grid, f)
    st = analyze(grid)
    verify(grid, st)
    print_report(grid, st)
    write_excel(os.path.join(HERE, "Exam_Timetable_G9_G10.xlsx"), grid, st)
    write_html(os.path.join(HERE, "Exam_Timetable_G9_G10.html"), grid, st)


if __name__ == "__main__":
    main()
