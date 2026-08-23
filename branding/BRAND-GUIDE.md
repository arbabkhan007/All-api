# Novality — Brand Guide

## Concept
**Novelty × Utility.** The sparkle = novelty (fresh, playful, creative). The solid geometric N = utility (structure, organization, function). One mark that says *creative and useful* — matching a shop that sells both crochet patterns and finance spreadsheets.

## Color

| Name | Hex | RGB | Use |
|---|---|---|---|
| Cream | `#FDF8F1` | 253, 248, 241 | Primary background |
| Plum Ink | `#382642` | 56, 38, 66 | Text, badge, primary lines |
| Coral | `#ED7A55` | 237, 122, 85 | Accent 1 — the N diagonal, i-dot sparkle, CTAs |
| Sage | `#94AE8F` | 148, 174, 143 | Accent 2 — chips, dots, secondary sparkles |
| Gold | `#E4B25C` | 228, 178, 92 | Sparkle details, small highlights |
| Blush | `#F6E2D2` | 246, 226, 210 | Soft background washes |
| Muted Plum | `#7A6686` | 122, 102, 134 | Secondary text, taglines |

Rules: cream is the house background; never place the plum badge on dark backgrounds without the cream plate; coral is reserved for one accent per composition.

## Typography
- **Quicksand** (Google Fonts, open license) — weights 400 / 500 / 600 / 700.
  - 700: wordmark, headlines
  - 600: buttons, chips, subheads
  - 500: body, fine print
- Wordmark is lowercase `novality` with a coral four-point sparkle in place of the i-dot. Always keep the sparkle — it's the signature.
- Tagline: `SMART DIGITAL GOODS` (letter-spaced caps) or full sentence `Smart digital solutions for creative minds`.

## Logo files

| File | Size | Use |
|---|---|---|
| `out/logo-shop-800.png` | 800×800 | **Etsy shop logo** (also 400 / 200 versions) |
| `out/logo-icon-600.png` | 600×600 transparent | The N badge alone — avatars, favicons, watermarks (400/128 too) |
| `out/logo-lockup-2400.png` | 2400×720 transparent | Wide lockup for headers, About-page images, email signatures |
| `out/lockup-on-cream-2400.png` | 2400×720 | Same lockup on a cream plate |
| `out/banner-1200x300.png` | 1200×300 | Etsy shop banner (minimum spec) |
| `out/banner-1680x420.png` | 1680×420 | Etsy shop banner (4:1, matches current banner ratio) |

## Usage rules
1. Clear space: keep empty space around the mark equal to the badge's corner radius (~24% of badge size).
2. Minimum render size: badge 24 px, wordmark 10 px cap height.
3. Don't recolor the N (cream stems + coral diagonal), don't add drop shadows beyond the soft one already in the badge, don't rotate.
4. On photos/listing mockups: badge or cream plate + wordmark, bottom-left or top-right corner, ~10% of frame width.

## Source
Generated with `make_brand.py` (Python/Pillow, 2× supersampled) using Quicksand from `@fontsource/quicksand` — rerun with `/home/user/.venv/bin/python make_brand.py` from `branding/` to regenerate every asset.
