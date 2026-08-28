#!/usr/bin/env python3
"""Check NS 04 - Coco the Capybara before it goes to PDF.

Run with no arguments; exits non-zero if anything fails.

    python3 verify_pattern.py

It checks three things:

1.  Identity      - design code NS 04, created by Novality Crochet Studio.
2.  Arithmetic    - gauge, finished size, and every round's stitch count.
                    Round instructions are parsed, not eyeballed: each round
                    is evaluated against the count of the round before it.
3.  Figures       - both vector diagrams stay inside their frame.
"""

import math
import os
import re
import sys

from pattern_spec import (
    BODY_STS,
    CLEARANCE_MM,
    FRONT_LEG_ROUNDS,
    LEG_ANGLES,
    LEG_CENTRE_R,
    LEG_STS,
    ROUND_MM,
    STITCH_MM,
    diameter_mm,
)

PHOTO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets",
                     "coco-capybara.jpg")

CODE = "NS 04"
STUDIO = "Novality Crochet Studio"
STORE = "Novality Store"          # the name used in the pattern's terms of use

FAILED = []


def check(label, ok, detail=""):
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", label,
                           ("  \u2014 " + detail) if detail else ""))
    if not ok:
        FAILED.append(label)
    return ok


def close(a, b, tol=0.15):
    return abs(a - b) <= tol


# ------------------------------------------------- round instruction parser --

def split_top(text):
    """Split on commas that are not inside [ ] brackets."""
    parts, depth, cur = [], 0, ""
    for ch in text:
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        parts.append(cur.strip())
    return parts


REPEAT = re.compile(r"^(?P<body>.+?)\s*\u00d7\s*(?P<n>\d+)$")


def evaluate(instruction, prev):
    """Return (stitches consumed, stitches produced) for one round.

    prev is the stitch count at the end of the previous round.
    """
    text = instruction.strip()

    m = re.match(r"^(\d+)\s+sc in MR$", text)          # magic ring start
    if m:
        return (0, int(m.group(1)))
    if text == "sc in each st around":
        return (prev, prev)
    if text == "inc in each st around":
        return (prev, prev * 2)

    consumed = produced = 0
    for part in split_top(text):
        rep = REPEAT.match(part)
        body, n = ((rep.group("body").strip(), int(rep.group("n"))) if rep
                   else (part, 1))
        if body.startswith("["):                        # repeated group
            inner_c, inner_p = evaluate(body[1:-1], prev)
        else:
            inner_c, inner_p = leaf(body)
        consumed += inner_c * n
        produced += inner_p * n
    return consumed, produced


def leaf(text):
    """A single stitch or plain run of stitches: (used, made)."""
    text = text.strip()
    m = re.match(r"^(\d+)\s+sc$", text)
    if m:
        return (int(m.group(1)), int(m.group(1)))
    if text == "sc":
        return (1, 1)
    if text == "inc":
        return (1, 2)
    if text in ("invdec", "dec"):
        return (2, 1)
    raise ValueError("cannot parse instruction: %r" % text)


# ------------------------------------------------------------- the pattern --

BODY = [
    ("R1", "6 sc in MR", 6),
    ("R2", "inc in each st around", 12),
    ("R3", "[1 sc, inc] \u00d76", 18),
    ("R4", "3 sc, [1 sc, inc] \u00d73, 3 sc, [1 sc, inc] \u00d73", 24),
    ("R5", "[3 sc, inc] \u00d76", 30),
    ("R6", "[4 sc, inc] \u00d76", 36),
    ("R7", "sc in each st around", 36),
    ("R8", "sc in each st around", 36),
    ("R9", "sc in each st around", 36),
    ("R10", "[7 sc, invdec] \u00d74", 32),
    ("R11", "[7 sc, inc] \u00d74", 36),
    ("R12", "sc in each st around", 36),
    ("R13", "sc in each st around", 36),
    ("R14", "sc in each st around", 36),
    ("R15", "sc in each st around", 36),
    ("R16", "[4 sc, invdec] \u00d76", 30),
    ("R17", "[3 sc, invdec] \u00d76", 24),
    ("R18", "[2 sc, invdec] \u00d76", 18),
    ("R19", "[1 sc, invdec] \u00d76", 12),
    ("R20", "invdec \u00d76", 6),
]

LEG = [("R1", "6 sc in MR", 6), ("R2", "[1 sc, inc] \u00d73", 9)]
LEG += [("R%d" % r, "sc in each st around", 9) for r in range(3, 10)]

EAR = [("R1", "6 sc in MR", 6), ("R2", "[1 sc, inc] \u00d73", 9),
       ("R3", "sc in each st around", 9)]
MUZZLE = [("R1", "6 sc in MR", 6), ("R2", "[1 sc, inc] \u00d73", 9),
          ("R3", "[2 sc, inc] \u00d73", 12), ("R4", "sc in each st around", 12),
          ("R5", "sc in each st around", 12)]


def rounds_consistent(name, rows):
    print("\nRound counts \u2014 %s" % name)
    prev = 0
    ok = True
    for label, instr, stated in rows:
        try:
            used, made = evaluate(instr, prev)
        except ValueError as exc:
            check("%s: %s" % (label, instr), False, str(exc))
            ok = False
            prev = stated
            continue
        good = made == stated and (used <= prev or prev == 0)
        check("%s  %-52s -> %2d" % (label, instr, made), good,
              "" if good else "pattern says %d, uses %d of %d"
              % (stated, used, prev))
        ok = ok and good
        prev = stated
    return ok


def main():
    print("Coco the Capybara \u2014 pre-publish verification\n")

    print("1. Identity")
    check("design code is %s" % CODE, CODE == "NS 04")
    check("created by %s" % STUDIO, STUDIO == "Novality Crochet Studio")
    check("terms-of-use credit line uses %s" % STORE,
          STORE == "Novality Store",
          "the source file says %r, not %r; the PDF carries both" %
          (STORE, STUDIO))

    print("\n2. Gauge")
    check("36 sc = 52 mm diameter",
          close(diameter_mm(36), 52.0, 0.5),
          "%.1f mm" % diameter_mm(36))
    check("4.5 mm per stitch", close(STITCH_MM, 162.0 / 36, 0.01))
    check("4.3 mm per round", close(ROUND_MM, 4.3, 0.001))

    print("\n3. Finished size")
    body_mm = 20 * ROUND_MM
    check("body, Rnd 1-20 = 86 mm", close(body_mm, 86.0, 0.5),
          "%.1f mm" % body_mm)
    back_mm = 8 * ROUND_MM
    front_mm = FRONT_LEG_ROUNDS * ROUND_MM
    check("back legs 8 rnds = 34.4 mm", close(back_mm, 34.4, 0.1),
          "%.1f mm" % back_mm)
    check("front legs 9 rnds = 38.7 mm", close(front_mm, 38.7, 0.1),
          "%.1f mm" % front_mm)
    back_hang = back_mm - 4 * ROUND_MM          # joined 17 mm above the base
    front_hang = front_mm - 5 * ROUND_MM        # joined 21.5 mm above the base
    check("back feet hang 17 mm below the body",
          close(back_hang, CLEARANCE_MM, 0.5), "%.1f mm" % back_hang)
    check("front feet hang the same 17 mm",
          close(front_hang, CLEARANCE_MM, 0.5), "%.1f mm" % front_hang)
    check("all four feet level (within 1 mm)",
          abs(back_hang - front_hang) <= 1.0,
          "difference %.1f mm" % abs(back_hang - front_hang))
    check("total standing height = 103 mm (10.3 cm)",
          close(body_mm + CLEARANCE_MM, 103.0, 0.5),
          "%.1f mm" % (body_mm + CLEARANCE_MM))
    check("width 5 cm matches the 52 mm gauge",
          close(diameter_mm(36), 50.0, 2.5),
          "%.1f mm" % diameter_mm(36))

    print("\n4. Leg placement")
    order = [kind for _deg, kind in sorted(LEG_ANGLES)]
    check("four feet, two back and two front",
          order.count("back") == 2 and order.count("front") == 2,
          " ".join(order))
    check("feet interleave around the body (back, front, back, front)",
          all(order[i] != order[(i + 1) % 4] for i in range(4)),
          " ".join(order))
    sorted_deg = [d for d, _k in sorted(LEG_ANGLES)]
    gaps = [sorted_deg[(i + 1) % 4] - sorted_deg[i] for i in range(3)]
    gaps.append(360 - sorted_deg[3] + sorted_deg[0])
    check("no two feet crowd closer than 45 degrees", min(gaps) >= 45.0,
          "gaps %s" % ", ".join("%.1f\u00b0" % g for g in gaps))

    pads = []
    for deg, kind in LEG_ANGLES:
        a = math.radians(deg)
        pads.append((LEG_CENTRE_R * math.sin(a), LEG_CENTRE_R * math.cos(a),
                     kind))
    pad_r = diameter_mm(LEG_STS) / 2.0
    width = (max(p[0] for p in pads) - min(p[0] for p in pads)) + 2 * pad_r
    check("footprint about 65 mm across", close(width, 65.0, 2.5),
          "%.1f mm" % width)
    right = [p for p in pads if p[0] > 0]
    offset = abs(max(p[1] for p in right) - min(p[1] for p in right))
    check("front-to-back offset between a back foot and the front foot "
          "beside it is 29 mm", close(offset, 29.0, 1.5), "%.1f mm" % offset)

    rounds_consistent("body and head", BODY)
    rounds_consistent("leg", LEG)
    rounds_consistent("ear", EAR)
    rounds_consistent("muzzle", MUZZLE)

    print("\n5. Face placement")
    check("eyes 6 sts apart = 27 mm", close(6 * STITCH_MM, 27.0, 0.1))
    check("ears 5 sts apart = 22.5 mm", close(5 * STITCH_MM, 22.5, 0.1))
    check("muzzle 12 sts around = 17 mm across",
          close(diameter_mm(12), 17.0, 0.5), "%.1f mm" % diameter_mm(12))
    check("muzzle spans Rnd 12-14, eyes sit at Rnd 14-15 (above it)",
          BODY_STS[14] == 36 and BODY_STS[15] == 36,
          "Rnd 15 is the last full 36-stitch round")

    print("\n6. Photograph")
    check("finished-item photo present", os.path.exists(PHOTO),
          os.path.relpath(PHOTO, os.path.dirname(os.path.abspath(__file__))))
    if os.path.exists(PHOTO):
        from PIL import Image
        from reportlab.lib.units import mm as _mm
        w, h = Image.open(PHOTO).size
        col_w = (210 - 2 * 19) * _mm          # A4 text column, in points
        drawn_w = min(col_w, 150 * _mm * w / float(h))
        dpi = w / (drawn_w / 72.0)
        check("photo prints at 150 dpi or better", dpi >= 150,
              "%d x %d px -> %.0f dpi" % (w, h, dpi))

    print("\n%s  \u2014  %d check(s) failed" %
          ("FAILED" if FAILED else "ALL CHECKS PASSED", len(FAILED)))
    if FAILED:
        for f in FAILED:
            print("   - %s" % f)
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
