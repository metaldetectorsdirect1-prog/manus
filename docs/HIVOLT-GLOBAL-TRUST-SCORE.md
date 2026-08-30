# HIVOLT-GLOBAL-TRUST-SCORE.md — 2026-08-28

Scored from fresh Shopify Admin read-backs this session (themes, all 4
products with variants/metafields, markets, locales, delivery profiles,
payment wallets, metafield/metaobject definitions, menus, pages, policies,
theme files). Scores are deliberately honest: a beautiful theme with 4 DRAFT
products, unpasted policies and zero reviews does not score highly.

## HIVOLT GLOBAL COMMERCE READINESS SCORE: 34 / 100

> **P0 authorized-pass recalculation (later on 2026-08-28), evidence-backed
> changes only:** Trust 40→**45** (three live-footer 404 links fixed and
> read-back verified; verified-truthful FAQ presentation live on the dev
> preview; honest zero-review strategy implemented). PDP Conversion
> 45→**50** (Judge.me review widget + review-count-gated rating badge wired
> and checksum-verified). Retention 25→**30** (review widget + acquisition
> sequence in place; still zero reviews). SEO/Merchant 35→**37** (genuine
> FAQPage JSON-LD now emitted from the verified FAQ template; live footer
> crawl 404s removed). Unchanged for lack of evidence: Product Data 30,
> Fit 15, Markets 20, Merchandising 35 (collection unpublish
> connector-blocked → owner action), Analytics 10 (GA4 owner connection
> required), Performance 40 (GemPages deletion connector-blocked; unused
> files carry zero runtime weight anyway), Accessibility 40, Creative 50
> (0/31 approved), Brand 55. Previous total 32 → **34**.

| # | System | Current | Target | Severity | Top gaps | Fixable now | Requires owner |
|---|---|---|---|---|---|---|---|
| 1 | Brand & Identity | 55 | 85 | MED | No logo asset; V3 visuals unverified | done: V3 system + tokens | Approve V3 screenshots; supply vector wordmark |
| 2 | Product Information | 30 | 90 | HIGH | spec.* 0% populated; UUID SKUs; 3/4 zero weight; no origin/HS | done: taxonomy category, productType, SEO meta, compare-at fix | Supplier spec data entry; real SKUs; weights |
| 3 | Size & Fit | 15 | 85 | HIGH | Zero size charts; guides unpublished | done: PDP renders fit/model rows when populated | Author `hivolt_size_chart` metaobjects from supplier tables |
| 4 | Merchandising & Discovery | 35 | 85 | HIGH | 1 real collection; 14 empty published collections; no filters configured | nav/collections staged honestly | Unpublish empty collections; S&D filter config in admin |
| 5 | Global Markets & Localization | 20 | 70 | MED | US-only, USD-only; Intl market disabled; de locale unpublished | architecture documented | Market activation decisions; translation program |
| 6 | PDP Conversion | 45 | 90 | HIGH | No reviews UI; no fit data; single-size supplier listings | done: details/trust/schema architecture | Judge.me widget placement decision; publish products |
| 7 | Shipping / Returns / Trust | 40 | 90 | CRITICAL | **Corrected policy bodies still not pasted** (connector scope-denied); stale spec-first copy on About/FAQ/blog | drafts ready in `impulse-rebuild/policies/` | Paste 4 policy bodies; approve page-copy refresh |
| 8 | Customer Account / Retention | 25 | 75 | MED | 0 reviews; no wishlist/back-in-stock provider found; no email flows verified | new customer accounts already on | Choose providers; post-purchase review flow |
| 9 | SEO / Feeds / Structured Data | 35 | 85 | HIGH | Feed attributes 0% populated; GTIN unverified | done: JSON-LD (Org/WebSite/Product), SEO meta, taxonomy | Populate mm-google-shopping.*; Simprosys feed setup |
| 10 | Analytics / CRO | 10 | 80 | HIGH | No GA4/pixels verifiable; no event instrumentation | funnel + event spec documented | GA4 property + Customer Events install |
| 11 | Performance / A11y / Privacy | 40 | 85 | MED | theme.css 777KB; GemPages residue; consent unaudited | audit documented; custom sections optimized | Consent app decision; GemPages removal approval |
| 12 | AI Creative Production | 50 | 85 | MED | 0 of 31 V3 assets approved | done: full program + gallery + audit doc | Pixel-review the gallery |

## Launch gates

| Gate | Status | Blocking fact |
|---|---|---|
| 1 — PRODUCT TRUTH | PARTIAL | Real products/media; spec data 0%, weights missing on 3/4 |
| 2 — SIZE & FIT | FAIL | Zero charts authored; no garment measurements exist |
| 3 — GLOBAL COMMERCE | FAIL | US-only by current strategy; Intl market disabled; no duties/HS data |
| 4 — TRUST & POLICIES | **BLOCKED** | Owner must paste 4 corrected policy bodies (write_legal_policies denied to connector) |
| 5 — MERCHANDISING | PARTIAL | Honest nav staged; 14 empty published collections need unpublishing (connector-blocked) |
| 6 — PDP CONVERSION | PARTIAL | Architecture done; reviews/fit data absent |
| 7 — SEO / FEEDS | PARTIAL | Schema + meta done; feed attributes unpopulated |
| 8 — CUSTOMER RETENTION | FAIL | No flows, no wishlist/BIS, 0 reviews |
| 9 — PERFORMANCE / ACCESSIBILITY | PARTIAL | Solid base; weight + consent gaps |
| 10 — VISUAL QUALITY | **BLOCKED** | V3 owner screenshots + 31-image gallery verdict pending |
| 11 — PRODUCT ACTIVATION | **BLOCKED** | Publication requires explicit owner authorization |
| 12 — LAUNCH | FAIL | Gates 1–11 not all passed |

Visual quality is not permitted to compensate for failed commerce gates.
