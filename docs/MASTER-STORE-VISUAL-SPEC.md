# MASTER-STORE-VISUAL-SPEC.md — reference reverse-engineering, 2026-08-28

Source: the original generated reference image supplied with the master
directive (a fictional "VELORA" fashion-commerce concept; its brand name,
copy figures and photography are TEMPLATE ARTIFACTS — the visual SYSTEM is
the specification, the content is not). This document is the design
contract for the candidate theme `GENERAL STORE — IMPULSE MASTER CANDIDATE`
(`158753849576`, UNPUBLISHED — role verified live before it was renamed).

**Direction is LOCKED per the directive. No further pivots.**

Reference copy that must NOT carry into the build (template artifacts, not
store truth): "$75+" shipping threshold, "30-day returns", "20K+ customers",
"250+ styles monthly", "Save 27%", star ratings and review counts, Klarna/
Afterpay claims. HIVOLT truth today: free tracked US shipping with NO
minimum, 60-day free returns (owner-ratified), 0 reviews (honest zero
state), BNPL only if the payment config actually enables it.

## 0. Measured system (from the reference pixels)

| Token | Value (measured/derived) |
|---|---|
| Page width | ~1420 px content, 20 px gutters, full-bleed bands |
| Grid | 12-col fluid; product grids 4-col collection / up to 6-col trending row; 8–10 px card gutters |
| White | #FFFFFF page ground |
| Ink | ~#0A0A0B text and solid CTAs |
| Commercial red | ~#C81010 (sale prices, save pill, promo band, primary PDP CTA, SALE nav item) |
| Soft bg | ~#F7F7F5 (image wells, panels) |
| Border | ~#E4E4E4 hairlines (header rule, cards, accordions, footer rule) |
| Secondary text | ~#6B6B6B |
| Type family | Single modern grotesk (Impulse's font_body stack); 2 weights dominant (400/700), occasional 500 |
| Display scale | Hero ~56–64 px Title Case (NOT uppercase), section titles ~22 px Title Case + 13 px gray subtitle, card titles 13–14 px, nav/labels/CTA 11–13 px UPPERCASE +0.08–0.14em tracking |
| Buttons | Rectangular, no radius; solid ink or solid red with white text; ghost white on imagery; 12–13 px uppercase, 12–14 px vertical padding |
| Corner radius | 0 everywhere except circular category thumbs and swatch dots |
| Sale display | Red price + struck gray compare-at + red "Save NN%" pill (PDP) / red percent (cards) |

## 1. Component map — REFERENCE → IMPULSE → DESKTOP → MOBILE → EDITOR

### 1.1 Announcement bar
- REFERENCE: ink bar ~30 px, centered 11 px uppercase microcopy, single line, dismissable not shown.
- IMPULSE: native announcement bar in header group (`sections/header.liquid` settings) — already active.
- DESKTOP/MOBILE: identical; single truthful message ("Free tracked US shipping on every order" — no minimum exists, so no "$75+").
- EDITOR: message, link, color scheme, enable — native.

### 1.2 Header
- REFERENCE: white, ~64 px; logo left (bold uppercase wordmark), center uppercase nav with red SALE item, right icons search/account/wishlist/cart-with-count; 1 px bottom hairline; sticky.
- IMPULSE: native header section (logo position "left-center" layout), sticky enable, predictive search trigger, cart drawer trigger. Wishlist icon only when a wishlist surface exists (see 1.16) — otherwise omitted (no dead icon).
- DESKTOP: compact height setting, nav center; SALE menu item colored via nav-link class hook only when a real sale collection exists.
- MOBILE: hamburger + centered logo + search/cart; drawer nav (native).
- EDITOR: logo image/width, menu pick, sticky toggle, transparent-over-hero off (reference header is opaque white).

### 1.3 Mega menu
- REFERENCE: full-width white panel, hairline border + soft shadow; 4–5 columns of links under bold uppercase column heads; right featured portrait tile with label + CTA.
- IMPULSE: native `mega_menu` header blocks (verified in source earlier): menu-item name match, optional collection images, up to 2 promo units = the featured tile.
- DESKTOP: opens on hover/focus of a top-level item; keyboard accessible natively.
- MOBILE: hierarchical drawer (native).
- EDITOR: per-menu block: menu item name, show images, promo image/heading/link.
- DATA GATE (unchanged): built only when the real collection tree exists. Today the store has 4 draft products and 11 empty collections pending owner unpublish → mega menu stays unactivated; architecture documented in the owner package. No dead links, ever.

### 1.4 Hero
- REFERENCE: full-width panoramic ~2.4–2.6:1 desktop; left-aligned copy block on the image: 13 px uppercase eyebrow absent — instead large 2-line Title Case display (~60 px, regular weight first line, bold second), 14 px subcopy, white solid button (ink text) "SHOP NEW IN". Mobile: dedicated portrait crop, copy bottom-left over darken gradient.
- IMPULSE: native hero/slideshow section — supports desktop+mobile image, text position, overlay opacity ("darken"), buttons.
- DESKTOP: text left-middle; Title Case headline (settings, not code); eager load + fetchpriority (already engineered).
- MOBILE: portrait asset (V3 image 2 once approved), bottom-left, darken overlay ~55% bottom gradient — proven in-harness last pass.
- EDITOR: images D/M, focal point, heading/sub/eyebrow, 2 CTAs, overlay strength, alignment — native.
- CONTENT GATE: imagery remains preview-active pending the 12-frame shortlist approval (0/28 approved).

### 1.5 Category circles row  **← NEW BUILD (this pass)**
- REFERENCE: immediately under hero; 9–10 circular thumbs (~72 px) + 10–11 px uppercase labels (SALE label red); one row, generous spacing.
- IMPULSE: no native circles section → new section `fashion-category-circles.liquid`.
- DESKTOP: single row, centered, up to 10 blocks; circle = square image `object-fit: cover; border-radius: 50%`, hairline ring, hover scale ≤1.04.
- MOBILE: horizontal swipe (overflow-x auto, scroll-snap), ~5 visible.
- EDITOR: per block: collection picker (link + fallback image from collection), optional image override, label override, "highlight red" checkbox (SALE). Section: enable, heading optional, circle size range.
- DATA GATE: blocks render only when their collection exists and is non-empty (`collection != blank and collection.products_count > 0` unless a manual link+image is deliberately set). Ships EMPTY by default — zero fake categories.

### 1.6 Service value strip  **← NEW BUILD (this pass)**
- REFERENCE: 3 columns, small line icon + 13 px bold uppercase label + 12 px gray caption; white band with hairline top/bottom.
- IMPULSE: `text-columns-with-images` exists but is image-based and heavy → new lightweight section `fashion-value-strip.liquid` with inline SVG icon set (truck, returns, payment, shield, tag).
- DESKTOP: 3-up (max 4); MOBILE: 3 stacked rows or 1-per-row — reference mobile shows compact stacked.
- EDITOR: per block: icon select, label, caption, optional link. Section: enable, scheme.
- TRUTH GATE: ships with ZERO blocks configured. The owner package documents the two claims that are true today (free tracked US shipping — no minimum; 60-day free returns) and forbids a BNPL block until the payment gateway actually offers installments.

### 1.7 "The Edit" editorial cards  **← NEW BUILD (this pass)**
- REFERENCE: title-case section head ("The Edit") + gray subtitle + "SHOP ALL EDITS" text link right; 4 portrait (3:4) cards, white uppercase label + tiny caption bottom-left on image over subtle gradient.
- IMPULSE: `collection-list` exists but renders its own card style; the reference treatment (overlay label + caption + gradient) → new section `fashion-edit-cards.liquid`.
- DESKTOP: 4 across, 8 px gutters. MOBILE: 2 across (QA'd) — reference shows 4-in-row shrink; 2×2 is the safer density at 390 px.
- EDITOR: section heading/subheading/link; per block (max 4): image, label, caption, collection/URL.
- DATA GATE: block renders only with image + destination set; ships EMPTY.

### 1.8 Section headings (global pattern)
- REFERENCE: Title Case ~22 px semibold + 13 px gray subtitle under it, optional uppercase text-link right ("VIEW ALL", "SHOP ALL EDITS").
- IMPULSE: `index-section-header` snippet renders section headings — restyle via CSS on the candidate (`.section-header__title` size/case) rather than editing every section.
- IMPLEMENTATION: candidate-level CSS (custom stylesheet already exists from the FN-rhythm build) — no uppercase transform on section titles; keep uppercase for nav/buttons/labels only.

### 1.9 Trending product row
- REFERENCE: 6 dense cards/row desktop (~160 px wide), 3:4 image, black BESTSELLER badge (data-only), title 13 px, red sale price + struck compare, stars + count (real only), swatch dots.
- IMPULSE: native `featured-collection` with per_row up to 5... native max is 5 → set 5 on wide (directive: "Desktop: 4 baseline, evaluate 5"; reference's 6 accepted as density ceiling, 5 is the Impulse-native max without grid surgery — record as deliberate).
- MOBILE: 2-col.
- EDITOR: collection pick, per_row, rows.
- DATA GATE: real products only; renders nothing meaningful until products go ACTIVE (catalog gate).

### 1.10 Campaign banners / Shop-by-category / product grids
- Already built in the FN-rhythm pass (campaigns A/B/C with V3 preview imagery; category strip 6 tiles; collage). Reference rhythm: CAMPAIGN → CATEGORY → PRODUCTS → CAMPAIGN → PRODUCTS. Homepage order updated this pass (1.16 below).

### 1.11 Newsletter band
- REFERENCE: full-width RED band; left bold white headline + small sub; right inline white email input + ink button.
- IMPULSE: native newsletter section supports color scheme; the red band + inline layout → candidate CSS on the newsletter section (scheme option) — no fake "10% off" claim: default copy is promotion-free ("Be first to know…") until the merchant configures a REAL discount.
- EDITOR: heading, sub, scheme (red/soft), Shopify-native email capture.

### 1.12 Footer
- REFERENCE: white, top hairline; brand column (wordmark, 2-line statement, social icons) + SHOP/HELP/ABOUT/LEGAL columns; bottom row copyright + payment icons.
- IMPULSE: native footer section (menu blocks, social, payment icons setting). Existing candidate footer already carries real destinations only.
- ACTION: verify column composition matches SHOP/HELP/ABOUT/LEGAL naming once the real page set exists; payment icons on (native, reflects actual gateways).

### 1.13 Collection page
- REFERENCE desktop: title + count + short description; sort right; left sidebar filters (Category/Size/Color dots/Price/Material) with counts; 4-col dense grid; numeric pagination. Mobile: title + count, Filter + Sort split buttons, 2-col grid, filter drawer.
- IMPULSE: native main-collection (sidebar filters via Shopify Search & Discovery values only — no invented facets), built + campaign-tile block added earlier. per_row 4 default (max 5), rows_per_page up to 20 → 100/page ceiling.
- QA: 48-card fixture PASS (previous pass); 100-card fixture run this pass.

### 1.14 PDP
- REFERENCE desktop: left vertical thumb rail + large image; right sticky info: title, stars (real only), price + red save pill, color swatches, size buttons + size-guide link, qty, RED add-to-cart, dark accelerated-payment button, 3 trust rows, DETAILS/SIZE & FIT/SHIPPING & RETURNS accordions; "You'll love this" 4-up recommendations below.
- REFERENCE mobile: swipe gallery + wishlist heart, purchase block, sticky ATC bar after scroll.
- IMPULSE: native product template + prior-pass work (desktop sticky info column, mobile sticky ATC bar — write-verified). Red primary ATC = candidate button-color setting (settings_data) — pending; save-pill markup exists in sale snippet (percentage display fixed and verified last pass). Accordions = native product blocks fed by metafields; empty metafield → block omits (no fake data). Recommendations + recently-viewed already wired.
- GATE: rendered PDP verification requires remote preview (4 draft products; editor preview only).

### 1.15 Cart drawer + cart page
- REFERENCE: CART (n) header, free-shipping progress meter, line items with qty steppers, recommendation row, subtotal/shipping/total, ink CHECKOUT, View Cart link.
- IMPULSE: native drawer + cart page. TRUTH DELTA: a "$X away from free shipping" METER would be FAKE here — US shipping is free with NO minimum. Implementation: static truthful line "Free tracked US shipping on every order" in the drawer (native cart note/message setting); no meter until a real threshold exists.
- Recommendations in drawer: Impulse-native cart recommendations where supported; otherwise omitted (no custom fake upsell this pass).

### 1.16 Predictive search / wishlist / account
- SEARCH — REFERENCE: overlay with suggestions, products (thumb+title+price), collections, blog posts. IMPULSE: native predictive search covers all four groups. ON already.
- WISHLIST — REFERENCE shows hearts + wishlist grid. No legitimate wishlist app/provider is installed → per directive: NO fake backend. Architecture documented (owner may install Swym/Wishlist Plus later); a device-local localStorage wishlist is NOT built this pass to avoid shipping a surface that silently loses data across devices; header omits the heart icon until a real provider exists.
- ACCOUNT — Shopify-hosted new customer accounts control most surfaces; theme styles what it legitimately owns (classic templates present in Impulse). No override attempts of Shopify-hosted pages.

### 1.17 Content pages (About / FAQ / Contact / Tracking / Size guide / Journal)
- REFERENCE: premium editorial About (statement + stats + 3 value columns), FAQ accordion, contact panel, order-tracking form, journal grid.
- IMPULSE: page templates exist; drafts exist in repo (`HIVOLT-ABOUT-DRAFT.md`, `HIVOLT-FAQ-DRAFT.md`, `HIVOLT-HELP-CENTER-DRAFT.md`) — all owner-gated content (policies connector-blocked: `shopPolicyUpdate`).
- TRUTH GATE: reference stats (20K+/250+/30-day) are template artifacts — never rendered. Stats section renders only merchant-entered real numbers, else omits.
- Tracking: no tracking app installed → merchant-configurable tracking link surface only; no fake shipment lookups.
- Journal: Impulse blog templates native; article schema native.

## 2. Rhythm contract (homepage order, reference-derived)

01 announcement · 02 header · 03 hero · 04 category circles ·
05 value strip · 06 The Edit (4 cards) · 07 Trending products (dense) ·
08 campaign A · 09 shop-by-category tiles · 10 product grid ·
11 campaign B · 12 promotional interrupt (REAL promos only — ships
disabled) · 13 The Latest (long grid) · 14 collage (brand texture,
retained from V3 program) · 15 campaign C · 16 newsletter (red) ·
17 footer.

Products dominate the middle and second half; three campaigns carry
distinct stories; no giant empty luxury whitespace.

## 3. Fidelity measurement

Local harness (`qa/home-harness-v4.html`) mirrors this architecture with
the QA fixture + V3 review pixels and is screenshotted at 1440/390 against
the reference for proportion/hierarchy/density/rhythm comparison each
iteration. Shopify-runtime surfaces (PDP JS, drawer, search) can only be
fidelity-checked in remote preview — listed as verification debt, not
skipped silently.
