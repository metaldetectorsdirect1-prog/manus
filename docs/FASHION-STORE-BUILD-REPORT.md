# FASHION-STORE-BUILD-REPORT.md — first complete build, 2026-08-27

## Theme safety
Published theme: IMPULSE-REBUILD-2026-08-24 · `158753652968` — **untouched** (read/copy-source only; zero mutations targeted it).
Development theme: Copy of Impulse · `158753849576` — role verified **UNPUBLISHED** before every write and after the final write (03:37Z).
Preview: `https://f36zps-yd.myshopify.com/?preview_theme_id=158753849576` (or admin → Online Store → Themes → Copy of Impulse → Preview / Customize).

## Design system (applied + verified by read-back)
Obsidian `#0A0A0B` text/CTAs · white/ivory grounds · Bordeaux `#A01732` sale-only · Instrument Serif display over Inter body · uppercase nav ·
square buttons · portrait cards, hover second image, Quick Add, round swatches · drawer cart · predictive search with prices · currency/locale selectors off (US-only store).

## Files written to the dev theme (all verified by checksum read-back)
`sections/fashion-hero.liquid` (custom: desktop+mobile art-directed images, srcset 375–2400w, width/height attrs, eager+fetchpriority only when flagged first, HTML overlay, reduced-motion respected)
`config/settings_data.json` · `sections/header-group.json` · `sections/footer-group.json` ·
`templates/index.json` · `collection.json` · `product.json` · `cart.json` · `404.json` · `search.json`
Repo copies: `impulse-rebuild/theme/fashion/`.

## Homepage (active, women-led, catalog-true)
announcement (2 true claims, linked to policies) → fashion-hero (women knitwear campaign, Shop knitwear) → brand statement → 2-tile gateway (dept-women, new-in) → **the single real product row** (knitwear, per_row 4, view-all) → knitwear editorial (links the real care-guide page) → newsletter with brand-editorial image. **Four products are used once — no fake scale.**
Pre-built, `disabled: true`: master mixed-gender hero, men's hero, men's 4-card trend grid — one toggle each in Theme Editor when men's inventory exists.

## Honest-content deletions from stock
Fake "extra 10% off" collection banner · 5 fabricated testimonials · "Organic cotton" sales points · placeholder tabs · demo mega-menus · Shopify demo social links · stock "30 days" promo blocks (our real policy is 60) · currency selector (USD only).

## Navigation
New shop-level menu `fashion-main` (Knitwear · New in · Journal · About · Help — every link real); live `main-menu` untouched. Footer uses the real footer-help / footer-about / footer-legal menus; copyright names Dn Global Trading LLC (trading as HIVOLT).

## QA
JSON validated locally pre-upsert (8/8) · mutation shapes validated pre-execution · every write verified by fresh read-back (checksums + role + updatedAt) · one platform normalization noted (heading line-height 1.15→1.2) · one settings floor hit and fixed (collection font size 15).
**Not possible from this environment:** storefront rendering/screenshots (egress) and image pixel inspection — both owner-side, below.

## Owner actions required
1. **PRODUCT PUBLICATION AUTHORIZATION REQUIRED** — the four products are DRAFT and will not render in preview product rows or /collections/knitwear. To see them: approve flipping to ACTIVE (note: they then also appear on the LIVE theme's knitwear collection page), or preview layout without products for now. IDs: 9613182468328 (Elena) · 9613182435560 (Nora) · 9613182370024 (Ivy) · 9613182402792 (Warm cable).
2. **Image pixel QA** — both galleries rendered in chat; every asset status = OWNER VISUAL APPROVAL REQUIRED (docs/AI-IMAGE-PRODUCTION.md). Reject by number; inpaint or regenerate follows.
3. **Screenshots for refinement pass** — preview URL at 390, 430, 1440.
4. Do NOT publish — publishing stays a human decision.
