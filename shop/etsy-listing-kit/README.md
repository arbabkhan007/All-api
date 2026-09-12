# Shop · Etsy Listing Kit for Crochet Pattern Sellers

The listing kit packaged as a product you can sell, not just use.

```bash
shop/etsy-listing-kit
├── README.md                 # this file
├── tools/
│   └── build_product.py       # assembles the product and renders the PDFs
└── product/
    ├── template.md            # source: prose with {{PLACEHOLDER}} slots
    ├── worksheets.md          # source: printable worksheets
    ├── Etsy-Listing-Kit-Crochet.md    # generated, customer-facing
    ├── Etsy-Listing-Kit-Crochet.pdf   # generated — THE PRODUCT (24 pages)
    └── Etsy-Listing-Worksheets.pdf    # generated — printable pack (4 pages)
```

## Rebuilding

The product pulls its titles, tag sets and description copy straight out of the
per-pattern listing files, so the PDF can never drift from the verified content.

```bash
python3 -m venv /tmp/pdfenv && /tmp/pdfenv/bin/pip install reportlab
cd shop/etsy-listing-kit/tools
/tmp/pdfenv/bin/python build_product.py
```

## Adding a sixth pattern listing

1. Write `etsy-listing-kit/12-…md` (or the next number) in the same format as 07–11.
2. Add a chapter to `product/template.md` with `{{TITLE_XX}}`, `{{TAGS_XX}}`, `{{DESC_XX}}`.
3. Add the file to the `sources` dict in `tools/build_product.py`.
4. Rebuild.

The build fails loudly if any placeholder is left unresolved.

## Selling it

Full listing copy — title, three tag sets and description — is in
`etsy-listing-kit/13-listing-the-kit.md`.

| | |
|---|---|
| Price | $12.00 (floor $7.95, ceiling $17.00) |
| Launch price | $9.60 for days 1–30 |
| Files to upload | the two PDFs in `product/` |
| Licence | Personal use in the buyer's own shop; no resale, sharing or redistribution |
