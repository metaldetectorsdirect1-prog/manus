# HIVOLT-SEO-AUDIT.md — 2026-08-28

Method: theme-file inspection on the dev theme (storefront HTTP is
egress-blocked from this environment; rendered-page verification is an
owner/GSC task). Impulse 9.2.0.

## Technical

| Item | State |
|---|---|
| Canonical | `<link rel="canonical" href="{{ canonical_url }}">` ✓ |
| Title | seo-title snippet: page title + brand suffix, paginated titles ✓ |
| Meta description | rendered when page_description exists; all 4 products now carry SEO descriptions (set this session) ✓ |
| Robots / sitemap | Shopify-native; not directly fetchable from this environment — verify in GSC | 
| Headings | one h1 per template (Impulse); custom sections use h2 ✓ |
| Pagination | native `current_page` handling in title ✓ |
| Image alt | all V3 uploads carry descriptive alt (set at fileCreate); product media alt from supplier — spot-check at publication |
| 404 | rebuilt template, honest ✓ |
| Internal linking | limited by draft catalog (nav minimal by design) |
| hreflang / localized URLs | single locale published (en); Shopify emits hreflang only with published alternate locales — none yet |

## Structured data (implemented this run, dev theme)

- Before: **no JSON-LD anywhere** (layout audit — only OG/Twitter meta).
- Now: Organization + WebSite(+SearchAction) on the homepage
  (`sections/hivolt-structured-data.liquid` via footer group) and Product +
  AggregateOffer JSON-LD on PDPs (`fashion-pdp-info.liquid`).
- Deliberately absent: AggregateRating (0 reviews — faking it is forbidden),
  gtin (barcodes unverified), FAQ schema (no qualifying page), Breadcrumb
  (breadcrumbs disabled in theme).
- State: IMPLEMENTED + VISUAL REVIEW REQUIRED (validate with Google's Rich
  Results test once the theme is live/preview-shared).

## Duplicate-content risk

Product descriptions are supplier-derived (duplicated across the internet).
Mitigation exists in the model: `hivolt.lede` unique copy field — 0/4
populated. Writing ledes is a content task, not a code task.

## Search Console / Merchant Center

GSC: not verifiable from this connector (mcp-search-console server timed
out this session). GMC 5838274874 verified earlier (verification ≠
misrepresentation clearance). Feed readiness: see
HIVOLT-MERCHANT-FEED-READINESS.md.
