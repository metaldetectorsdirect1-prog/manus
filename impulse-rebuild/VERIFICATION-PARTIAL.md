# VERIFICATION-PARTIAL.md

Not the §13 pass — that cannot run until the catalog exists. This records what
was changed on the dev theme and how each change was verified.

**Theme under build:** `158753652968` `IMPULSE-REBUILD-2026-08-24`, role
`UNPUBLISHED`. The live theme `158743363816` was not written to.

## Verification method

`themeFilesUpsert` returns an empty error list whether or not a write lands, so
no result below is taken from a mutation payload. Every file was **re-read** and
compared.

**Checksum comparison does not work on these files.** `config/settings_data.json`
was pushed at 3,977 bytes / md5 `52083b4a…` and stored as 2,999 bytes / md5
`0b36a6d0…` — Shopify re-encodes theme JSON server-side. Verification is
therefore by **parsed value**, not by bytes. The read-back text was confirmed
character-identical to what was sent; only the stored encoding differs.

## Verified

| File | Check | Result |
|---|---|---|
| `config/settings_data.json` | 11 named settings compared by parsed value | **PASS** |
| `config/settings_data.json` | all 10 `social_*` fields empty | **PASS** — was 5× shopify.com demo accounts |
| `templates/product.json` | `testimonials` absent from `sections` and `order` | **PASS** |
| `templates/product.json` | no `sales_point`, no placeholder tabs, no disabled sections | **PASS** |
| `templates/collection.json` | fake-sale `promo-grid` absent | **PASS** |
| `templates/404.json` | `featured-collection` absent | **PASS** |
| `templates/cart.json` | `featured-collection` absent | **PASS** |

## Design-system contrast — measured, not asserted

| Pair | Ratio | Min | |
|---|---:|---:|---|
| body on paper | 18.83:1 | 4.5 | PASS |
| muted on paper | 6.63:1 | 4.5 | PASS |
| paper on ink | 18.83:1 | 4.5 | PASS |
| ink on volt button | 15.75:1 | 4.5 | PASS |
| volt on ink | 15.75:1 | 4.5 | PASS |
| border on paper | 3.07:1 | 3.0 | PASS |
| sale on paper | 6.25:1 | 4.5 | PASS |

The first border I specified failed at **1.38:1** and was replaced. Volt on
paper measures **1.20:1** and is therefore barred from ever being text on light.

## GemPages — monitored, not certified

`appInstallations` is denied to this session's access scopes, so **installation
status cannot be confirmed via API**. What is confirmed:

| File | Live theme | Dev theme |
|---|---|---|
| `assets/gp-global.css` | `23:17:33Z`, md5 `1c742190…` | `09:14:40Z`, md5 `1c742190…` |
| `layout/theme.gempages.header.liquid` | `23:17:34Z`, md5 `074f445d…` | `09:14:40Z`, md5 `074f445d…` |
| `locales/en.default.json` | `23:17:36Z`, md5 `6cef7bac…` | `09:14:40Z`, md5 `6cef7bac…` |

No write to either theme in ~10 hours; the dev timestamps are duplication
artefacts. **An idle app is indistinguishable from an uninstalled one over the
API**, so this is evidence of quiescence, not proof of removal. Confirming it in
Admin → Apps remains an owner action before Phase 3.

`locales/en.default.json` was deliberately not written to.
