# HIVOLT — Master Task Register

Updated 2026-08-20. **Authority boundary is enforced in every row.**

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
| T1 | Metafield schema for polo attributes (fabric, GSM, fit, care, size table) | P1 | — |
| T2 | Size-guide modal — dual unit (in/cm), per-product table from metafields | P1 | T1 |
| T3 | Colour swatch selector + variant image switching | P1 | — |
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
| G6 | `custom.feed_title` metafield — feed titles separate from storefront titles | P1 | Premium PDP naming never degraded for ad relevance |
| G7 | `identifier_exists: false` handling where no GTIN exists | P1 | Own-brand apparel; never invent GTINs |
| G8 | Structured data templates: Product, Offer, BreadcrumbList, Organization | P1 | **No Review/AggregateRating** — no real review data exists |
| G9 | Material / pattern / fit metafields (feeds both PDP and feed) | P1 | Depends on T1 |
| G10 | Publish `/pages/size-chart` (currently `isPublished: false`, PDP block points at it) | P1 | Broken reference — size guide cannot render |
| G11 | Feed pre-flight validation checklist as a runnable check | P2 | §7 of Google doc |
| G12 | Seasonality research doc (polo/golf/Father's Day/BFCM by country) | P2 | Research only — authorises no catalogue or pricing change |

### Destination integrity — flagged, not auto-fixed

| # | Finding | Lane |
|---|---|---|
| G13 | **11 of 11 main-menu links resolve to empty collections** | Resolves when catalogue lands; collection taxonomy still needs polo re-architecture (OWNER decides taxonomy) |
| G14 | Navigation is women's-activewear taxonomy on a men's polo brand | OWNER — merchandising decision |
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
