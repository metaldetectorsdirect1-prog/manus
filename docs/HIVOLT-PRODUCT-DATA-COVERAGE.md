# HIVOLT-PRODUCT-DATA-COVERAGE.md — 2026-08-28

Catalog: 4 products, all DRAFT (fresh read-back). Coverage is per-field
across those 4. TRUST: CONFIG = read from Shopify; SUPPLIER = from the
source listing (unverified against a physical garment); NONE = no source.
**Never invent missing product facts.**

| Field | Source | Coverage | Trust | Missing on | Safe to expose? |
|---|---|---|---|---|---|
| Title | session-authored | 4/4 | HIGH | — | YES |
| Description | session-authored from supplier | 4/4 | MED | — | YES |
| SEO title/description | this session | 4/4 | HIGH | — | YES |
| productType | this session | 4/4 | HIGH | — | YES |
| Taxonomy category | this session (Sweaters ×3, Cardigans ×1) | 4/4 | HIGH | — | YES |
| Price | supplier-derived pricing | 4/4 | HIGH | — | YES |
| Compare-at price | cleared this session (was bogus "0.00") | 4/4 null | HIGH | — | YES (no fake sales) |
| Media | supplier imports (6/9/9/23 images) | 4/4 | MED | — | YES |
| Tags | session SOP pass | 4/4 | HIGH | — | YES |
| Vendor | HIVOLT | 4/4 | HIGH | — | YES |
| Inventory | AutoDS-set (10/10/10/680) | 4/4 | MED | — | YES |
| SKU | AutoDS UUIDs | 4/4 | LOW (not human-readable) | — | NO (sku_enable false on PDP) |
| Barcode | AutoDS-supplied | 4/4 | LOW (unverified as real GTINs) | — | NO — do not send as gtin until verified |
| Weight | supplier | 1/4 (Elena 0.2 kg) | LOW | Ivy, Nora, Cardigan (0) | NO |
| Country of origin | — | 0/4 | NONE | all | NO |
| HS code | — | 0/4 | NONE | all | NO |
| spec.composition / knit / fit / care / gsm | — | 0/4 | NONE | all | Renders only when populated (blank-safe PDP) |
| spec.origin / model_* / size_chart | — | 0/4 | NONE | all | Same |
| hivolt.lede | — | 0/4 | NONE | all | Same |
| mm-google-shopping.gender / age_group / custom_product | — | 0/4 | NONE | all | Feed blocked until populated |
| custom.mpn / feed_title / identifier_mode | — | 0/4 | NONE | all | Feed falls back to defaults |
| Reviews (Judge.me) | app installed | 0 reviews | — | all | Nothing to expose; never fabricate |

Option-value hygiene (recorded, NOT mutated — option/variant rewrites are a
known no-op/risk class on this store; owner decision): "Clothing Size Group:
Women" as an option on the cardigan; casing "2Xl"/"Xl"/"Xxl"; supplier color
names ("Jiahua Green", "A Gray"). Recommended future normalization at import
time in AutoDS, not by mutating existing variants.
