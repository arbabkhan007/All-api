# Novality — Brand Guide (v2 — Eco Pastel)

## Concept
**Novelty × Utility, eco edition.** The sparkle = novelty (fresh, playful, creative). The solid geometric N = utility (structure, organization, function). The leaf accents keep it nature-forward. One mark that says *creative, useful, and kind to the planet* — matching a shop that sells both crochet patterns and finance spreadsheets.

## Color (eco pastel palette)

| Name | Hex | RGB | Use |
|---|---|---|---|
| Oat Cream | `#FAF6EC` | 250, 246, 236 | Primary background |
| Brown Ink | `#5C4B3A` | 92, 75, 58 | Text, primary lines |
| Muted Taupe | `#927C66` | 146, 124, 102 | Secondary text, taglines |
| Pistachio | `#A3C585` | 163, 197, 133 | Accent, chips, dots, leaves |
| Pistachio Deep | `#8CAF68` | 140, 175, 104 | Badge background |
| Light Blue | `#A6D5F0` | 166, 213, 240 | Soft washes, chips, leaves |
| Pink | `#F09EB6` | 240, 158, 182 | Accent 1 — the N diagonal, i-dot sparkle, CTAs |
| Light Brown | `#C9A876` | 201, 168, 118 | Chips, washes, leaves |
| Caramel | `#D9B380` | 217, 179, 128 | Sparkle details on the badge |

Rules:
- Oat cream is the house background.
- Pink is the single "pop" accent per composition — keep it to the N diagonal / i-dot / one CTA element.
- Never place the pistachio badge on dark backgrounds without the cream plate.
- Leaves and sparkles are decoration — at most 2–4 per composition, small.

## Typography
- **Quicksand** (Google Fonts, open license) — weights 400 / 500 / 600 / 700.
  - 700: wordmark, headlines
  - 600: buttons, chips, subheads
  - 500: body, fine print
- Wordmark is lowercase `novality` with a **pink four-point sparkle** in place of the i-dot. Always keep the sparkle — it's the signature.
- Tagline: `SMART DIGITAL GOODS` (letter-spaced caps) or full sentence `Smart digital solutions for creative minds`.

## Logo files

| File | Size | Use |
|---|---|---|
| `out/logo-shop-800.png` | 800×800 | **Etsy shop logo** (also 400 / 200 versions) |
| `out/logo-icon-600.png` | 600×600 transparent | The N badge alone — avatars, favicons, watermarks (400/128 too) |
| `out/logo-lockup-2400.png` | 2400×720 transparent | Wide lockup for headers, About-page images, email signatures |
| `out/lockup-on-cream-2400.png` | 2400×720 | Same lockup on an oat-cream plate |
| `out/banner-1200x300.png` | 1200×300 | Etsy shop banner (minimum spec) |
| `out/banner-1680x420.png` | 1680×420 | Etsy shop banner (4:1, matches current banner ratio) |

## Usage rules
1. Clear space: keep empty space around the mark equal to the badge's corner radius (~24% of badge size).
2. Minimum render size: badge 24 px, wordmark 10 px cap height.
3. Don't recolor the N (cream stems + pink diagonal), don't add drop shadows beyond the soft one already in the badge, don't rotate.
4. On photos/listing mockups: badge or cream plate + wordmark, bottom-left or top-right corner, ~10% of frame width.

## Source
Generated with `make_brand.py` (Python/Pillow, 2× supersampled) using Quicksand from `@fontsource/quicksand` — rerun with `/home/user/.venv/bin/python make_brand.py` from `branding/` to regenerate every asset.
