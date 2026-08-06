# HIVOLT — Deliverables

Everything produced during the store audit and remediation session.
Store: `hivolt-usa.com` · `f36zps-yd.myshopify.com`

---

## What's in here

### `docs/HIVOLT-OPERATIONS-HANDOVER.md` — read this first
The complete record: the root-cause finding, every change made to the live
store, competitive intelligence extracted from 2,365 competitor ads, and the
full list of open items. If you only keep one file, keep this one.

### `docs/SEO-AUDIT.md`
Technical SEO audit. Covers the broken Google Search Console verification
(fixed), the missing structured data, and the domain-reputation problem caused
by eight unrelated businesses having previously occupied this domain.

### `model/HIVOLT-unit-economics.xlsx`
Unit-economics calculator. **Fill the yellow cells on the `Inputs` sheet** from
your Tapstitch account and everything else computes: contribution margin,
breakeven ROAS, allowable CAC, and profit per order for each product, plus a
revenue-target sheet.

Currently the model says you lose about **$35.74 per order** on Meta ads at
industry-default costs. That figure is only provisional until you supply real
Tapstitch numbers — it may be better or considerably worse.

The `Sources` sheet lists every benchmark with a confidence rating. Tapstitch's
activewear base cost is marked **NOT FOUND**, not estimated — their prices
render client-side and are not publicly retrievable.

### `model/build.py`
The generator script for the workbook, kept so the model can be rebuilt or
modified.

### `theme-snippets/*.liquid`
Standalone structured-data snippets. **These are now superseded** — both have
already been applied directly to the `HIVOLT v14` theme in your Shopify admin.
They are kept here as reference, and in case you ever want to apply them to a
different theme.

---

## What is NOT in this folder, and where to get it

**The modified theme files** live in Shopify, not here. Two templates were
rewritten in an unpublished duplicate theme:

- `templates/product.liquid` — fixed the dead mobile "Add to bag" button, added
  Product + BreadcrumbList structured data, corrected the returns policy,
  fixed related-product logic
- `templates/index.liquid` — fixed three 404 links, removed the false "we ship
  to Canada" claim, corrected the delivery estimate and returns policy, added
  Organization + WebSite + FAQPage structured data

To download them:
**Shopify admin → Online Store → Themes → "HIVOLT v14 — schema + PDP fixes"
→ ⋯ (three dots) → Download theme file.** Shopify emails you a zip of the
complete theme. That copy is authoritative.

---

## Outstanding actions — none of which can be done for you

1. **Publish the v14 theme.** Online Store → Themes → Preview → Publish.
   Check one product page on your phone first and tap the sticky "Add to bag";
   that button never worked before and is the only change with behavioural risk.
   Theme publishing is deliberately blocked from automation to prevent
   accidental storefront changes.

2. **Place a real test order with a card.** The store was structurally unable to
   accept an order for months. That is fixed and verified at the shipping-rate
   layer, but the payment gateway itself has never been exercised.

3. **Fill in the seven Tapstitch cost lines** in the workbook. Until then nobody
   knows whether these products can be sold profitably at any volume.

4. **Confirm US-fulfilment eligibility** on your activewear SKUs. Tapstitch's
   activewear line launched March 2026 with only partial US stocking, and orders
   silently fall back to China routing — which would make your 8–14 business day
   delivery promise undeliverable.

5. **Google Search Console** — re-verify (the verification page is now
   published), submit the sitemap, and read the indexing report. That report
   decides whether organic search on this domain is salvageable.

---

## The one-line summary

The store had zero orders in its entire history because **500 of its 504 product
variants had no computable shipping rate**, so checkout dead-ended before
payment. That is fixed. Everything else in this folder is secondary to
confirming, with a real card, that money can now move.
