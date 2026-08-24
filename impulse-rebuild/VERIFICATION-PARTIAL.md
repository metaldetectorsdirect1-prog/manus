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

---

# Phase 3 queue — every item closed or blocked

| # | Item | Status |
|---|---|---|
| 1 | **Live-theme verification** | ✅ done — 🔴 **defect confirmed present, removal BLOCKED** (below) |
| 2 | GemPages status | ⚠️ **still unverifiable** — `appInstallations` remains scope-denied |
| 3 | Shipping-zone restriction | ⚠️ **not needed as specified** — finding below |
| 4 | Information architecture | ✅ `INFORMATION-ARCHITECTURE.md` — tree, namespaced handles, smart rules, 15-collection disposition |
| 5 | **Both size guides** | ✅ **live and verified** — `size-guide-women`, `size-guide-men` |
| 6 | Returns / 60-day page | ❌ not done |
| 7 | Policy suite rewrite | ❌ not done |
| 8 | FAQ 18+ | ❌ not done |
| 9 | About | ❌ not done |
| 10 | Care guide | ❌ not done — fabric types depend on catalog |
| 11 | Customer account templates | ❌ not done |
| 12 | Empty/utility states | ⚠️ partial — defective sections removed from 404/cart; states not yet designed |
| 13 | Review system | ❌ not done |
| 14 | Non-product imagery | ❌ not done — logo + favicon already live from an earlier session |
| 15 | Footer | ❌ not done |
| 16 | Perf / a11y / SEO scaffolding | ❌ not done |
| — | Collection objects (§5) | ❌ not created |

**Items 6–16 were not reached.** Reported as not done rather than partially done.

## 🔴 Item 1 — live theme still carries the fabricated content

Read from published theme `158743363816`, `templates/product.json`:

| Check | Answer |
|---|---|
| `testimonials` present in `order`? | **YES** — position 5 of 8 |
| All five fabricated reviews present? | **YES** — Leslie M., Rachel F., Sam R., Sharon S., Matt C. |
| "Organic cotton" sales point present? | **YES** — `sales_point-1` |
| *(also)* fake "extra 10% off — limited time" on live `collection.json`? | **YES** |

Last session cleaned **only the dev theme**. My report said "four forbidden
items removed" without distinguishing the two, which was imprecise.

**Removal attempted and refused at the tool layer:**

> `themeFilesUpsert` … blocked. *"This mutation targets the live (published)
> theme. Theme file writes against the live storefront are blocked."*

This is a connector safety policy that task authorization does not override.
Three ways to clear it, all owner actions:

1. **Publish the dev theme** `158753652968` — already clean, already carries the
   corrected design system. Cleanest path.
2. Delete the `testimonials` section in the live theme's editor by hand.
3. Duplicate live → edit the copy → publish.

**Current exposure is latent, not active:** with zero products, no product page
renders, so nobody can see the fake reviews today. It becomes live the moment a
catalog imports. It should be cleared before then, not after.

## ⚠️ Item 3 — the shipping contradiction is narrower than I reported

Last session I reported "shipping says US-only while checkout accepts 71
countries." Checking the actual configuration, that overstated it:

| Market | Enabled | Regions |
|---|---|---|
| **United States** | ✅ enabled, **primary** | US only |
| **International** | ❌ **disabled** | ~71 countries |

**The International market is already disabled**, so checkout is US-only at the
market level — matching the published policy.

The 71-country figure came from `shop.shipsToCountries`, which reflects
*delivery-zone coverage*, not an open checkout. Those zones live on a
**non-default profile named `Tapstitch: Special Line`** — an app-owned
fulfilment profile. The default `General profile` has exactly one zone: United
States.

So the directive's instruction — restrict zones to the US — **would not change
what a customer can do**, and deleting zones from an app-owned profile invites a
resync conflict (a prior repo note records Tapstitch reactivating deactivated US
rates on resync). No change made. Reporting the finding instead, since the
conservative outcome the directive wanted already holds.

## ⚠️ Item 2 — GemPages, third check

`appInstallations` → `access denied` again. Unchanged: **an idle app is
indistinguishable from an uninstalled one over this API.** No GemPages write to
either theme since the original install burst. `locales/en.default.json` still
untouched by me.

## New since last session

A third theme appeared: **`158753849576` "Copy of Impulse"**, UNPUBLISHED,
created by someone other than this session. Not written to. Noted so the theme
count is not a surprise later.

## Still blocked (§7) — unchanged

Hero imagery · category tiles · collection banners · final `product.json` /
`collection.json` population · product-dependent trust content · navigation
wiring · delivery copy and per-market table · duties language · photographic
language lock · §13 zero-empty verification · squint, grid, five-second,
density, speed and 375px criteria.

---

# Phase 4 — queue status

| # | Item | Status |
|---|---|---|
| §1 | Live-theme status check | ✅ reported — **still dirty**, unchanged since `23:17:18Z` |
| §2 | App investigation | ✅ `APP-CONFLICTS.md` — 8+ integrations, 4 categories, 2 languages |
| §3 | Blog audit | ✅ `BLOG-AUDIT.md` — 501 articles, bulk-generated in 13 days |
| §4 | **Blog + article templates** | ✅ **built and verified** |
| 6 | **Returns / 60-day page** | ✅ **rewritten, ships final** — ⚠️ two unverified claims flagged in `ASSUMPTIONS.md` |
| 7 | Policy suite | ⚠️ **partial — Terms only.** Privacy, Accessibility, Contact not done |
| 8 | FAQ 18+ | ❌ not done |
| 9 | About | ❌ not done |
| 10 | Care guide | ❌ not done |
| 11 | Customer account templates | ❌ not done |
| 12 | Empty/utility states | ❌ not done |
| 13 | Review system | ❌ not done |
| 14 | Non-product imagery | ❌ not done |
| 15 | Footer | ❌ not done |
| 16 | Perf / a11y / SEO scaffolding | ⚠️ **partial** — Article JSON-LD ships via the article template; see defect below |

## §1 — live theme, verbatim answer

Read from published `158743363816`:

| Check | Answer |
|---|---|
| `testimonials` in `product.json` `order`? | **YES — still present** |
| "Organic cotton" sales point? | **YES — still present** |
| "extra 10% off — limited time" on `collection.json`? | **YES — still present** |

`product.json` is **6,844 bytes, `updatedAt 2026-08-23T23:17:18Z`** — byte-identical
to install. No manual cleanup has occurred yet. Tool-layer write block stands;
not worked around.

## 🔴 New defect found — duplicate Article schema

`sections/article-template.liquid` emits `Article` JSON-LD for every article.
The audit found that **the articles also carry their own embedded `Article` and
`FAQPage` JSON-LD inside the body HTML.**

Every article therefore publishes **two competing Article schemas**, and the
body-embedded one carries the false product claims. Fixing the template does not
fix this — the bad schema is in the content.

Two further template-level issues:

- The template declares `"author": {"@type": "Person"}` while `article.author` is
  **"HIVOLT Training Team"**, an organization. Type mismatch on all 501.
- Not fixed this session. Recorded for the blog remediation pass, where it is
  the highest-severity, lowest-effort item.

## §4 verification

| File | Check | Result |
|---|---|---|
| `templates/blog.json` | `featured-collections` (4 empty blocks) removed | **PASS** |
| `templates/blog.json` | tag filter, RSS, date, excerpt, landscape ratio set | **PASS** |
| `templates/article.json` | hero image, tags, date, author, sharing on; related posts titled | **PASS** |
| Both | comments disabled | **PASS** |

Verified by parsed-value read-back at `10:02:07Z`.

## Still blocked (§7) — unchanged

Hero imagery · category tiles · collection banners · final `product.json` /
`collection.json` population · product-dependent trust content · navigation
wiring · delivery copy, per-market table, duties language · photographic
language lock · zero-empty verification · squint, grid, five-second, density,
speed and 375px criteria.

---

# Phase 5 status

| Item | Status |
|---|---|
| §1 structural correction absorbed | ✅ pages now treated as production writes |
| §2 live Returns figures corrected | ✅ both applied, read back, verified |
| §2 claims audit of all published pages | ✅ `CLAIMS-REGISTER.md` |
| §2 **third fabrication found** | ✅ **five more unsourced claims, removed** |
| §3.1 JSON-LD scanned | ✅ 50/50 carry it, 42/50 make claims |
| §3.1 JSON-LD stripped | ❌ **deferred behind the prune** — see `BLOG-AUDIT.md` |
| §3.2 per-article traffic | ✅ measured — 14 articles above 4 sessions, blog is 2.2% of traffic |
| §3.3 classification against data | ✅ 13 survivors identified |
| §3.4 prune executed | ❌ **not executed** — designed and handed over |
| §4 Tapstitch conflict documented | ✅ `ASSUMPTIONS.md` |
| 7 Policy suite (Privacy, Accessibility, Contact) | ❌ not done |
| 8 FAQ | ❌ not done |
| 9 About | ❌ not done |
| 10 Care guide | ⚠️ **source identified** — six surviving care articles to consolidate |
| 11–16 | ❌ not done |

## Live theme — session-start status, unchanged

`templates/product.json` on `158743363816`: **6,844 bytes, `updatedAt
2026-08-23T23:17:18Z`.** Byte-identical to install. Testimonials, "Organic
cotton" and the "extra 10% off" banner all still present. Owner-side removal.
