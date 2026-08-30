# HIVOLT-PRODUCT-DATA-MODEL.md — 2026-08-28

Decision: **reuse the existing architecture — no new definitions were
created.** The audit found a complete fashion PIM already defined on this
store (built for the earlier spec-first era, garment-generic in design).
Creating parallel `fit.*`/`material.*`/`care.*` namespaces would duplicate
it, which the directive forbids.

## The model, as it exists on the store (all PRODUCT-owner)

**Core (native Shopify)** — title, handle, SKU, barcode, vendor,
productType, taxonomy category (now set: Clothing Tops > Sweaters /
Cardigans), options (size/color), price, compare-at, inventory, weight,
media, SEO title/description.

**Editorial** — `hivolt.lede` (unique opening copy; the anti-duplicate-
content field for supplier imports).

**Material / construction / fit / care — `spec.*`** (18 definitions):
composition, gsm, knit, finish, fit, rise, inseam, seams, gusset, opacity,
collar, placket, cuff, hem, care, origin, benefits (list), size_chart
(→ `hivolt_size_chart` metaobject).

**Model context — `spec.model_height_cm`, `spec.model_wears_size`** (the
PDP renders them only as a pair).

**Merchant feed — `mm-google-shopping.*`**: gender, age_group,
custom_product; plus `custom.mpn`, `custom.feed_title`,
`custom.identifier_mode` (documented resolver: gtin / brand_mpn / none).

**Shopify standard taxonomy attributes** — `shopify.fabric`,
`shopify.age-group`, `shopify.target-gender` (metaobject-referenced;
preferred over custom equivalents, already defined).

**Discovery — `shopify--discovery--*`**: product_search_boost.queries,
product_recommendation.related_products / related_products_display /
complementary_products (Search & Discovery app installed).

**Customs** — native `inventoryItem.countryCodeOfOrigin` and
`inventoryItem.harmonizedSystemCode` (both empty; see
HIVOLT-CUSTOMS-READINESS.md).

## Gaps in the model (define only when data will exist)

- `spec.stretch` (None/Slight/Medium/High) — not yet defined; add at first
  data-entry pass rather than as an empty definition.
- Garment measurements per size — carried by the `hivolt_size_chart`
  metaobject (columns/rows), not per-product fields. Correct design; needs
  charts authored.
- Return eligibility / final-sale flag — not defined; all products
  currently share the 60-day policy, so a per-product flag is premature.

## Rendering contract (implemented on dev theme 158753849576)

`sections/fashion-pdp-info.liquid` renders Details rows for composition,
knit, fit, gsm, care, origin and the model pair — each row blank-safe.
Empty fields render nothing. Populating a field lights it up with no theme
change. Never populate a value that is not supplier-documented.
