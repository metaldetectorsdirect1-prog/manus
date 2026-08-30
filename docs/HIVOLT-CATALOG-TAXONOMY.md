# HIVOLT-CATALOG-TAXONOMY.md — 2026-08-28

## Live structure (read-back)

- Real, populated collection: **knitwear** (450083651816, title-rule based,
  4 products) + **all** (448200114408).
- **14 published empty collections** remain from the spec-first era —
  GLOBAL-ACTION-REQUIRES-APPROVAL to unpublish (connector-blocked earlier).
- Nav (`fashion-main`): Journal / About / Help — deliberately minimal; no
  collection links while every collection destination is empty of ACTIVE
  products.

## Target taxonomy (architecture; expose only when backed by inventory)

WOMEN: New in · Knitwear · Sweaters · Cardigans · Dresses · Tops · Bottoms ·
Denim · Matching sets · Outerwear · Best sellers · Sale.
MEN: hidden until inventory exists (assets staged, sections disabled).
Phase-5 allocation (PRODUCT-RESEARCH.md §8) feeds this tree.

## Filters (Shopify Search & Discovery — app installed, config is admin-UI only)

| Filter | Source | Coverage | Normalization | Ready? |
|---|---|---|---|---|
| Size | option "Size"/"Clothing Size" | 4/4 (single-size ×3) | casing (2Xl→2XL) at import | PARTIAL |
| Color | option "Color" | 4/4 | supplier names need mapping to base colors | PARTIAL |
| Price | native | 4/4 | — | YES |
| Availability | native | 4/4 | — | YES |
| Category | productType (set this session) | 4/4 | — | YES |
| Fit | spec.fit | 0/4 | — | NO — do not expose |
| Fabric | shopify.fabric | 0/4 | — | NO |
| Style/Occasion/Length/Sleeve/Neckline/Rise/Leg | no data | 0/4 | — | NO |

Rule applied: no filter is exposed while its backing data is empty or
low-quality. S&D filter activation itself happens in the admin app UI
(no Admin API surface) — owner action at publication time.

## Search

Predictive search enabled (settings read-back), price shown, vendor hidden.
Boost/related/complementary metafields exist (empty). Query classes like
"oversized sweater" and "cream cardigan" resolve through title/tags — the
current titles already carry those tokens. No AI semantic search: no
reliable provider present; not justified at 4 SKUs.
