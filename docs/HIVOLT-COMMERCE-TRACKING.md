# HIVOLT-COMMERCE-TRACKING.md — 2026-08-28

## Audit

- Theme layout carries **no hardcoded third-party pixels** (clean —
  verified in `layout/theme.liquid`; app pixels load via
  `content_for_header`).
- GA4 / Meta / TikTok / Pinterest / Google Ads pixels: **not verifiable
  through this connector** (app installations read is scope-denied). No
  evidence any is installed. Shopify native analytics only.
- Consent: no consent-management implementation found in the theme; Shopify
  Customer Privacy API availability depends on app/config — unaudited.
- Duplicate-tracking risk today: none (nothing is installed twice because
  almost nothing is installed).

## Required baseline (before any CRO experimentation)

Install via **Shopify Customer Events / Web Pixels** (not theme-injected
script tags): GA4 property + Google Ads linkage. Standard events —
view_item_list, select_item, view_item, search, add_to_cart,
remove_from_cart, view_cart, begin_checkout, purchase (checkout events come
from Shopify's protected pixel context).

HIVOLT-specific custom events (emit from theme interactions once a pixel
exists): size_guide_open, variant_unavailable, back_in_stock_request (when
a provider exists), complete_the_look_add (when relationships exist),
search_no_results, filter_apply.

## Status

BLOCKED BY OWNER AUTHORIZATION (pixel/app installs are global,
customer-facing changes) + BLOCKED BY OPERATIONS (a GA4 property must
exist). Theme-side event emission is a small follow-up once the pixel
layer is chosen. Do not inject random pixels into theme code.
