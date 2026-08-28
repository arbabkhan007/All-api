"""Shared measurements for NS 04 - Coco the Capybara.

One home for every number the pattern depends on, so the PDF and the
verification script can never quote different figures:

    gauge      36 sc = 162 mm of circumference -> 51.6 mm diameter (~52 mm)
    stitch     162 / 36 = 4.5 mm per stitch
    round      4.3 mm per round
    legs       9 sts around -> 40.5 mm circumference -> 12.9 mm diameter
"""

import math

STITCH_MM = 4.5          # one single crochet, measured along the circumference
ROUND_MM = 4.3           # one round, measured vertically

# Body: round number -> stitches at the end of that round (pattern, Part 2).
BODY_STS = {
    1: 6, 2: 12, 3: 18, 4: 24, 5: 30, 6: 36, 7: 36, 8: 36, 9: 36, 10: 32,
    11: 36, 12: 36, 13: 36, 14: 36, 15: 36, 16: 30, 17: 24, 18: 18, 19: 12,
    20: 6,
}

# Leg geometry (pattern, Part 1 and Part 3).
LEG_STS = 9              # a finished leg is 9 stitches around
BACK_LEG_ROUNDS = 8      # 34.4 mm long, joined at Rnd 4  (17 mm above base)
FRONT_LEG_ROUNDS = 9     # 38.7 mm long, joined at Rnd 5  (21.5 mm above base)
CLEARANCE_MM = 17        # every foot hangs this far below the body

# Leg placement, read straight off the rounds the legs are joined on.
# Rnd 4 is 24 sts: legs over sts 1-3 and 13-15  -> centres at 22.5 and 202.5.
# Rnd 5 is 30 sts: 7 sc, leg, 10 sc, leg, 7 sc  -> centres at 102 and 258.
LEG_ANGLES = ((22.5, "back"), (202.5, "back"), (102.0, "front"),
              (258.0, "front"))
LEG_CENTRE_R = 25.6      # mm from the body axis out to a leg centre


def diameter_mm(stitches):
    """Circumference -> diameter. A stuffed tube is round, so divide by pi."""
    return stitches * STITCH_MM / math.pi


def radius_mm(stitches):
    return diameter_mm(stitches) / 2.0
