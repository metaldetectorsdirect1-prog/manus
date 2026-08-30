# HIVOLT-FIT-SYSTEM.md — 2026-08-28

## What exists today

- **Architecture: real.** `hivolt_size_chart` metaobject definition (title,
  measurement_basis, source_unit, columns, rows, note, source_reference) +
  `spec.size_chart` product reference + `spec.fit`, `spec.model_height_cm`,
  `spec.model_wears_size`, rise/inseam fields for bottoms.
- **Data: zero.** No size-chart metaobject instances exist; no product
  carries fit fields; both legacy size-guide pages are unpublished and carry
  spec-first activewear copy.
- **Catalog reality:** 3 of 4 products are single-size supplier listings
  (Small / L / 2XL); only Elena has a real size run (M–XXL). A fit system
  cannot demonstrate value until multi-size products exist.

## Shopper UI (target, theme-side; renders only from real data)

SIZE GUIDE (drawer/modal) → chart title, garment measurements table
(columns/rows from the metaobject), source note. FIT row: supplier's own
wording only. STRETCH: needs `spec.stretch` (define at data entry). MODEL:
"175 cm · wears size S" — renders only when both values exist (implemented).

## Data-entry workflow (owner/ops)

1. Pull the supplier's size table for each product (AutoDS source listing).
2. Create one `hivolt_size_chart` metaobject per shared block, filling
   `source_reference` with where the numbers came from.
3. Link products via `spec.size_chart`; fill `spec.fit` verbatim.
4. Never convert or interpolate measurements; store source_unit as given.

## International conversion approach

Store one source table (source_unit cm or in). Render conversions
(US/UK/EU) in Liquid at display time from the stored basis — never store
both systems by hand (drift risk). Roadmap: fit-recommendation only after
returns data exists (reason-coded returns are the training signal).

## Unavailable-variant rule (already native)

Impulse variant buttons show sold-out/unavailable states; no fake low-stock
messaging anywhere (none configured, none permitted).
