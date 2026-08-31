# PRODUCTION-CUTOVER-BASELINE.md — captured 2026-08-28 ~17:15 UTC

Rollback/cutover baseline for the MASTER r2 certification. Every value below
is a same-session Shopify read-back (not memory, not a prior report). This
file goes stale the moment anything changes — re-query before acting on it.

## Themes (exactly one MAIN verified)

| Theme | ID | Role | updatedAt |
|---|---|---|---|
| GENERAL STORE — IMPULSE MASTER CANDIDATE | `158753849576` | **MAIN** | 2026-08-28T15:41:08Z (unmoved since owner publish) |
| GENERAL STORE — MASTER r2 (approved image swaps) | `158874960104` | UNPUBLISHED | 2026-08-28T16:23:54Z (last verified session write) |
| Impulse (stock) | `158743363816` | UNPUBLISHED | 2026-08-25 |
| IMPULSE-REBUILD-2026-08-24 | `158753652968` | UNPUBLISHED | 2026-08-28T15:41:00Z |

## Catalog

- Products total: **23** — DRAFT **23**, ACTIVE **0**, ARCHIVED **0**,
  published to any channel **0** (`published_status:published` count = 0;
  every `publishedAt` null, every `onlineStoreUrl` null).
- All products use the default product template (templateSuffix null).
- The catalog GREW since the previous session (4 → 23 DRAFT): knitwear,
  cardigans, coats, jeans, lounge sets — an import pipeline is active.
- Anonymous storefront reality at cutover: **zero visible products**.

## Collections (15; all default template)

Populated (products are DRAFT, so all render empty publicly until
activation): all=4, knitwear=14, denim=4, coats-jackets=3, sets=2,
dresses=2, loungewear=1, outerwear-hoodies=1.
Empty: womens-activewear, tops, sports-bras, leggings, shorts,
mens-golf-polos ("The Polo Collection"), long-sleeve-golf-polos
("The Championship Capsule").

## Pages (21; 15 published)

Published: data-sharing-opt-out, about-us (suffix `about`), faq (`faq`),
shipping-delivery (`shipping`), 60-day-love-it-guarantee, contact-us
(default), google-site-verification (`google-verify`), returns-refunds
(`returns`), size-guide (`size-guide` — title still "Size Guide — Men's
Polos", legacy), terms-of-service, accessibility (`accessibility`),
track-order (`track-order`), materials-sustainability (`fabric`),
care-guide, payment-policy.
Unpublished drafts: voltcore, fabric-weight-index, size-chart,
size-guide-women, size-guide-men, privacy.

## Menus

- `master-storefront-nav` (`254991532264`) — referenced ONLY by r2's
  header-group. After the certification repair: Journal / About (4
  children) / Help (6 children); zero collection links while 0 products
  are published. Re-add "New in → /collections/all" and "Knitwear →
  /collections/knitwear" after product activation.
- `fashion-main` — referenced by live MAIN's header-group (checksum
  `68d8436e` verified): Journal / About / Help, flat.
- Footer (both themes): `footer-help`, `footer-about`, `footer-legal` —
  pages, policies, mailto/tel only; all destinations exist and are
  published.
- Unused by either theme: `main-menu`, `footer` ("Footer menu"),
  `footer-shop`, `customer-account-main-menu`.

## Policies (all exist)

PRIVACY (2026-07-01), REFUND (2026-08-10), SHIPPING (2026-08-10),
TERMS (2026-08-10), CONTACT_INFORMATION (2026-08-11). Served at
/policies/* — all footer/announcement policy links resolve.

## Business identity (matches all displayed contact data)

Dn Global Trading LLC / HIVOLT, 10s225 Kaye Ln, Willowbrook IL 60527 US,
+1 914-650-2041, support@hivolt-usa.com, hivolt-usa.com, USD.

## Storefront-affecting apps (theme evidence; API app listing scope denied)

- GemPages: layouts + gp-* assets present, no template assigned to a gp
  template → inert at cutover.
- Judge.me: PDP integration is metafield-gated — renders only when real
  reviews exist (currently zero; nothing renders).
- No hardcoded analytics pixels in the theme; store-level pixels inject
  via `content_for_header`. GA4/Meta/Ads: NOT CONFIGURED per prior audit;
  API scope to re-verify is denied (recorded honestly).

## Known content flags (live today on MAIN, unchanged by r2 — owner items)

1. FAQ delivery estimate (2–6 US / 10–15 intl-stocked) vs track-order
   page (10–18 end-to-end) — two published pages disagree; reconcile.
2. FAQ says US-only selling; shipping zones (`shipsToCountries`) allow
   ~240 countries — align zones or copy.
3. size-guide page title still "Size Guide — Men's Polos" (golf era).
4. /collections (unlinked route) lists empty collections incl. two
   golf-named ones — unpublish or populate before linking anything to it.
