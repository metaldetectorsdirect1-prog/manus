# HIVOLT — Master Task Register

Updated 2026-08-20 (second pass). **Authority boundary is enforced in every row.**

## Authority model

| Lane | Meaning |
|---|---|
| **TECH** | Claude proceeds autonomously — code, theme, UX, CRO, analytics, SEO, a11y, perf, docs, tests, drafts/staging |
| **OWNER** | Commercial or irreversible — supplier, product, pricing, publishing, inventory, markets, shipping, tax, payments, policy, claims, discounts |

## Closed this cycle

| # | Item | Lane | Result |
|---|---|---|---|
| C1 | Growth audit against live store state | TECH | Done — `HIVOLT-GROWTH-AUDIT.md` |
| C2 | 8 directive documents | TECH | Done |
| C3 | Polo supplier research (read-only) | TECH | Done — 6 candidates, spec gaps identified |
| C4 | **Boundary breach remediation** | — | **Done** — 3 products → DRAFT, 76,000 artificial units → 0, no channel published |
| C5 | Sourcing spec + supplier matrix | TECH | Done — `HIVOLT-POLO-SOURCING-SPEC.md` |
| C6 | Sourcing path comparison (A–E) | TECH | Done — `HIVOLT-SOURCING-PROPOSAL.md` |
| C7 | $500K quantitative model | TECH | Done — `HIVOLT-500K-MODEL.md` |
| C8 | Legacy logo marked deprecated, preserved | TECH | Done |
| C9 | **T1 — polo data schema** | TECH | Done — 12 product metafields + `hivolt_size_chart` metaobject |
| C10 | **T2 — size-guide system** | TECH | Done — data-driven, cm/in, renders nothing without real measurements |
| C11 | **T3 — colour swatches** | TECH | Done — real swatch data only, no guessed colours |
| C12 | **G6 — feed-title architecture** | TECH | Done — `custom.feed_title` + resolver |
| C13 | **G7 — configurable identifiers** | TECH | Done — per-variant `auto/gtin/brand_mpn/none`, verified before trusted |
| C14 | **G8 — structured data** | TECH | Done — Organization/WebSite/Breadcrumb/Product/Offer, no rating, no fake identifiers |
| C15 | Draft-theme navigation de-linked from empty legacy collections | TECH | Done — new menus, homepage rebuilt |
| C16 | Live policy contradictions documented for approval | TECH | Done — `HIVOLT-POLICY-CORRECTIONS.md`, 7 items, nothing applied |
| C17 | Render-level test suite for the new PDP layer | TECH | Done — `site/check-hivolt-pdp.py` |
| C18 | **Golden PDP fixture + 10 degraded scenarios** | TECH | Done — `site/hivolt_pdp_fixtures.py`, 25-variant matrix, no real data |
| C19 | **Release gate expanded to 113 assertions** | TECH | Done — positive, degradation and negative checks; exits non-zero |
| C20 | **Browser QA across 7 viewports + axe-core** | TECH | Done — `site/check-hivolt-browser.py`, 174/174, 0 WCAG violations |
| C21 | **Four defects found and fixed by the gate** | TECH | Done — see `HIVOLT-PDP-RELEASE-QA.md` |
| C22 | Release readiness report | TECH | Done — `HIVOLT-PDP-RELEASE-QA.md`: **READY FOR HUMAN PREVIEW** |
| C23 | Real size-chart integration attempt | TECH | **BLOCKED, correctly** — no garment measurement exists for any draft polo. Nothing written. Real-data pipeline verified fail-closed, 14/14 |
| C24 | Supplier measurement request | TECH | Done — `HIVOLT-POLO-MEASUREMENT-REQUEST.md`, ready to send |
| C25 | Detail-media evidence recovery | TECH | **Exhausted, unresolved** — 7 retrieval paths tried, all denied by egress policy. Images unread. Zero mutations. Needs a human with Shopify Admin |

## Blocked on OWNER

| # | Decision | Blocks | Doc |
|---|---|---|---|
| O1 | **Sourcing path A/B/C/D/E** | All product work | `HIVOLT-SOURCING-PROPOSAL.md` §4 |
| O2 | **Fulfilment: origin, carrier, cost, transit (US/CA/UK/EU)** | International markets, shipping, delivery promises | `HIVOLT-INTERNATIONALIZATION.md` |
| O3 | Retail pricing + margin floor | Pricing model, bundle design | `HIVOLT-SOURCING-PROPOSAL.md` §3 |
| O4 | Payments active? | Any revenue at all | `HIVOLT-GROWTH-AUDIT.md` P0 |
| O5 | Keep or delete 3 draft polos | Housekeeping | `HIVOLT-SOURCING-PROPOSAL.md` §1 |
| O6 | Authoritative logo asset | Design system finalisation | Owner supplying |
| O7 | E-commerce reference file | §6 classification | Owner supplying → `docs/research/` |
| O8 | Duties model (DDP/DAP), VAT status, EU/UK returns policy | Legal/compliance config | LEGAL review |

## TECH queue — proceeding without owner input

Product-independent storefront infrastructure. Built against **draft/unpublished
theme copies**; nothing touches the live theme without approval.

| # | Item | Priority | Depends on |
|---|---|---|---|
| ~~T1~~ | ~~Metafield schema for polo attributes~~ | **DONE** | — |
| ~~T2~~ | ~~Size-guide modal — dual unit (in/cm), per-product table from metafields~~ | **DONE** | — |
| ~~T3~~ | ~~Colour swatch selector + variant image switching~~ | **DONE** | — |
| T4 | PDP template to directive §9 hierarchy | P1 | T1–T3 |
| T5 | Sticky mobile ATC (suppressed until variants chosen) | P1 | T4 |
| T6 | Product benefit / details accordion architecture | P1 | T1 |
| T7 | Delivery + returns components (data-driven, no invented times) | P1 | O2 for content |
| T8 | Bundle UI architecture (pricing platform-side only) | P1 | O3 for values |
| T9 | Cart drawer + free-shipping progress (threshold configurable) | P1 | — |
| T10 | Cross-sell architecture | P2 | catalogue |
| T11 | Email capture (delayed / exit-intent, frequency-capped) | P1 | — |
| T12 | Analytics event layer per `HIVOLT-ANALYTICS-SCHEMA.md` | P1 | T4 |
| T13 | UTM preservation through navigation → checkout | P1 | — |
| T14 | Country/currency selector UX (inert until markets enabled) | P2 | O2 |
| T15 | Cookie consent scaffold | P2 | LEGAL |
| T16 | Accessibility pass — contrast on volt-yellow, focus states, modal a11y | P1 | design system |
| T17 | Performance: image sizing, font loading, script audit | P1 | — |
| T18 | SEO architecture: schema, canonical, OG, breadcrumbs | P2 | catalogue |


## Google Commerce readiness (added 2026-08-20)

Source: `HIVOLT-GOOGLE-COMMERCE.md`. **No ads, no campaigns, no spend, no
Merchant Center activation, no product activation performed.**

### OWNER — blocking Merchant Center

| # | Item | Why blocking |
|---|---|---|
| G1 | **Approve correction of live policy contradictions** (§2 P0-1…P0-8) | Live text says we sell sports bras/leggings, publish GSM we do not have, and do not ship internationally. Misrepresentation + trust risk |
| G2 | Confirm Merchant Center account claim + domain verification (ref 5838274874) | Not verifiable via Shopify API |
| G3 | Approve product, pricing, fulfilment (see O1–O4) | Gate A + C entirely |
| G4 | Decide fate of `/pages/fabric-weight-index` and `/pages/voltcore` | Stale/orphaned public pages |

### TECH — product-independent, proceeding

| # | Item | Priority | Note |
|---|---|---|---|
| G5 | Google product category metafield + mapping architecture | P1 | `Apparel & Accessories > Clothing > Shirts & Tops` |
| ~~G6~~ | ~~`custom.feed_title` metafield~~ | **DONE** | Resolver falls back to storefront title; consumer is a Merchant Center supplemental feed |
| ~~G7~~ | ~~Identifier handling where no GTIN exists~~ | **DONE** | Rebuilt as configurable per SKU/variant — see Google doc §4a. Not hardcoded to `false` |
| ~~G8~~ | ~~Structured data templates~~ | **DONE** | Organization, WebSite, BreadcrumbList, Product, one Offer per variant. No rating, no invented identifier |
| G9 | Material / pattern / fit metafields (feeds both PDP and feed) | P1 | Depends on T1 |
| G10 | Publish `/pages/size-chart` (currently `isPublished: false`, PDP block points at it) | P1 | Broken reference — size guide cannot render |
| G11 | Feed pre-flight validation checklist as a runnable check | P2 | §7 of Google doc |
| G12 | Seasonality research doc (polo/golf/Father's Day/BFCM by country) | P2 | Research only — authorises no catalogue or pricing change |

### Destination integrity — flagged, not auto-fixed

| # | Finding | Lane |
|---|---|---|
| G13 | **11 of 11 main-menu links resolve to empty collections** | **Fixed in the draft theme only.** New `hivolt-draft-main` / `hivolt-draft-shop` menus contain no empty-collection links. `main-menu` and `footer-shop` are untouched, so the live theme still shows all 11 |
| G14 | Navigation is women's-activewear taxonomy on a men's polo brand | OWNER — polo category taxonomy is a merchandising decision, so the draft nav ships with no category links at all rather than invented ones |
| G15 | `/collections/all` shows 3 DRAFT products → renders empty | Expected; correct state |

## Standing prohibitions

1. No fabricated product imagery.
2. No fabricated reviews, scarcity, counters, or statistics.
3. No performance/fabric claim not literally present in supplier data.
4. No artificial inventory.
5. No publishing to any sales channel without owner approval.
6. No live theme writes without owner approval.
7. No brand redesign from the deprecated legacy logo.
8. No Google Ads, campaigns, ad spend, or Merchant Center activation.
9. No Review/AggregateRating structured data without real review data.
10. No invented GTINs, MPNs, or product identifiers.

---

## Draft theme — what is built and where

**`HIVOLT v7 — DRAFT: PDP data layer`** — theme `158653808872`, UNPUBLISHED.
Duplicated from the current MAIN theme (`158570021096`), which was **not
touched**. Owner previews it in Online Store → Themes.

| File | What it does |
|---|---|
| `snippets/hivolt-identifier.liquid` | Resolves GTIN / brand+MPN / none per variant. One resolver for every consumer |
| `snippets/hivolt-feed-title.liquid` | Feed title, falling back to the storefront title |
| `snippets/hivolt-size-guide.liquid` | Size guide, trigger and dialog. Renders nothing without real measurements |
| `snippets/hivolt-swatches.liquid` | Colour swatches from real swatch data; text fallback, never a guessed colour |
| `snippets/hivolt-spec-table.liquid` | Publishes the `spec.*` metafields that are filled in, and only those |
| `snippets/hivolt-structured-data.liquid` | JSON-LD graph |
| `snippets/hivolt-head.liquid` | Single entry point for the head additions |
| `assets/hivolt-pdp.css`, `assets/hivolt-size-guide.js` | Styles and the dialog / unit-toggle behaviour |
| `snippets/variant-button.liquid` | Theme file — colour branch delegated to the swatch snippet |
| `snippets/social-meta-tags.liquid` | Theme file — one added render of `hivolt-head` |
| `templates/product.json` | Spec table and size guide added; the size-chart block pointing at the unpublished `size-chart` page removed |
| `templates/index.json` | Rebuilt without the deleted catalogue |
| `sections/header-group.json`, `sections/footer-group.json` | Repointed to the new menus |

Source of record is `site/theme-v7/` in this repo. Checks:
`python3 site/parse-liquid.py site/theme-v7/snippets/*.liquid` and
`python3 site/check-hivolt-pdp.py`.

### Release gate

`python3 site/check-hivolt-pdp.py` — 113 assertions, exits non-zero on failure.
`python3 site/render-pdp-preview.py && python3 site/check-hivolt-browser.py` —
174 browser checks at 320/375/390/430/768/1024/1440 plus axe-core WCAG 2.1 AA.

Fixtures are local Python (`site/hivolt_pdp_fixtures.py`), contain no real
product data, and cannot reach the store.

Full evidence, including the structured-data PASS/FAIL table and the
`/pages/fabric-weight-index` audit, is in `HIVOLT-PDP-RELEASE-QA.md`.

### Still owner-gated on this theme

1. **Preview and publish** — Claude cannot publish a theme.
2. **Obtain garment measurements.** Confirmed 2026-08-20: the supplier supplies
   a recommended body weight per size and no garment dimension at all, so no
   chart can be created without new data. Send
   `docs/HIVOLT-POLO-MEASUREMENT-REQUEST.md` to the supplier or measure a
   physical sample. Until then the size guide correctly renders nothing.
3. **Fill the `spec.*` fields** from supplier documentation. Empty fields render
   nothing, so the PDP is honest but thin.
4. **Polo category taxonomy** (G14) before the draft nav can carry category links.
