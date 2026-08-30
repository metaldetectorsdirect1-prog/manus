# HIVOLT-MERCHANT-FEED-READINESS.md — 2026-08-28

Apparel feed attributes vs current data (4 DRAFT products). Feed owner per
playbook: Simprosys. GMC 5838274874 (verified; assume 3/3 appeals burned —
zero-defect feed required).

| Attribute | Current coverage | Required? | Blocker | Action |
|---|---|---|---|---|
| title | 4/4 (feed_title override 0/4 — falls back, deliberate) | YES | — | Optional: keyword-front-loaded feed titles later |
| description | 4/4 | YES | supplier-duplicated text | Write hivolt.lede-based unique copy |
| link / image | 4/4 | YES | products DRAFT → no live URLs | Publication authorization |
| availability / price | 4/4 | YES | — | — |
| brand | HIVOLT 4/4 | YES | — | — |
| GTIN | barcodes present 4/4 but **unverified** | Conditional | Cannot confirm they are real GTINs | Verify with supplier or set identifier_mode=none + custom_product TRUE |
| MPN | 0/4 | Conditional | none supplied | Only if manufacturer-real |
| gender | mm-google-shopping.gender 0/4 | YES (apparel) | unpopulated | Set `female` ×4 (womenswear — factual) |
| age_group | 0/4 | YES | unpopulated | Set `adult` ×4 (factual) |
| color | option data 4/4 | YES | supplier names ("Jiahua Green") | Map to standard color names at feed level |
| size | option data 4/4 | YES | casing (2Xl) | Normalize in feed app |
| material | spec.composition 0/4 | Recommended | no supplier spec captured | Data entry |
| pattern | n/a | Optional | — | — |
| item_group_id | native product id | YES | — | Simprosys handles |
| shipping | Free US $0 (config-verified) | YES | GMC shipping settings must mirror policy word-for-word | Owner: after policy paste |
| returns | 60-day config | YES | same mirror requirement | Owner |
| condition | new | YES | — | — |
| google_product_category | Now derivable from taxonomy category set this session (Sweaters/Cardigans) | YES | — | — |

Gate: **do not sync a feed before** (1) policy bodies pasted + mirrored,
(2) gender/age_group populated, (3) identifier stance resolved, (4)
products published with owner authorization, (5) dead-link scan. Per the
playbook, first sync is the misrepresentation trigger — everything above
must be clean first.
