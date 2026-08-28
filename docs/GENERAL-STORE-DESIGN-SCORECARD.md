# GENERAL-STORE-DESIGN-SCORECARD.md — V4, 2026-08-28 (master-reference pass)

Six scores per the master directive (§51), separately owned. Points are
awarded for what is verified, never for code existing. Catalog shortages
are never counted against engineering or design.

History note: V2 stated "74" while its own table summed 84 (arithmetic
error, disclosed in V3). V3 recomputed Engineering to 87 with the same
verification standard used here.

## 1. THEME ENGINEERING READINESS: 88/100

Everything from V3 (87) plus this pass, all write-verified by checksum
read-back on the renamed candidate (`158753849576`):
- 3 new data-gated, editor-configurable sections: category circles, value
  strip, The Edit cards (all ship empty; zero fake content can render).
- Homepage rebuilt to the locked reference rhythm (`templates/index.json`).
- Global heading Title Case via `type_header_capitalize: false`
  (field-verified; sale system and all unrelated settings unchanged).
- Red newsletter band via native settings (no fake discount copy).
- **100-card fixture test PASS** (directive §39): 100 cards at 390/768/1440,
  columns 2→3→4, zero overflow, zero clamp failures, pagination UI
  rendered. Impulse's native page ceiling (5 per row × 20 rows) covers it.

The 12 missing points are Shopify-runtime verification debt, unreachable
from this environment: PDP behaviors (4), search/cart rendered QA (2),
performance measurement (2), accessibility rendered walk (2), rendered
proof of the new + campaign-tile sections on Shopify (1), Impulse-runtime
fidelity of harness results (1). **No unbuilt feature remains in scope for
the current catalog reality.** Gate §52 (≥95) is blocked by remote preview
— a real external blocker, named.

## 2. VISUAL DESIGN READINESS: 80/100

The reference system is locked and reproduced: measured token table and
component map in `MASTER-STORE-VISUAL-SPEC.md`; harness v4 renders the full
architecture (header, circles, value strip, The Edit, dense grids,
campaigns, collage, red band, footer) at 1440/390 with **zero layout
defects** and high system fidelity to the reference (proportions,
hierarchy, density, rhythm — not third-party assets).
- −8: rendered-on-Shopify fidelity unverified (remote preview).
- −7: hero/campaign/tile imagery is technically QA'd but owner-unapproved
  (0/28); nav/mega-menu/circles surfaces empty until real collections
  exist.
- −5: deliberate deltas: trending density capped at Impulse's 5-across
  (reference shows 6); PDP red ATC + save pill styling not yet applied
  (single global button color in Impulse — scoped PDP accent is a candidate
  CSS decision waiting on owner taste).

## 3. SEO READINESS: 82/100

Verified: single-source JSON-LD (Org, WebSite, Product, CollectionPage,
FAQPage), canonical/meta present, honest titles, faceted navigation left to
Shopify Search & Discovery (no crawl traps added, no JS-only browsing),
image SEO in all new sections (srcset, sizes, real alt, lazy below fold,
eager LCP hero), Article schema native, 404/password native, robots/
sitemap Shopify-native. Missing: rich-results validation and CWV
measurement (remote), plus the catalog itself (4 draft products = almost
no indexable commerce surface — catalog fact, listed here only because
crawlers will see it).

## 4. CRO READINESS: 80/100

Live on the candidate: quick add/quick shop (native, on), sticky mobile
ATC + sticky desktop PDP info, recommendations + recently viewed,
predictive search, drawer cart, truthful value/trust strips, newsletter
capture (no fake coupon), verified-honest sale math, collection filtering,
in-grid campaign tiles. Absent by policy: fake urgency/social proof (§41),
free-shipping threshold meter (US shipping has NO minimum — a meter would
be a dark pattern here). Open: wishlist (no legitimate provider — none
faked), cart upsell block (kept native), BNPL messaging (unknown gateway
state). Rendered conversion QA needs remote preview.

## 5. MOBILE READINESS: 88/100

Rendered mobile QA is the strongest-verified area: 48-card and 100-card
fixtures pass at 320–1440; v3/v4 harness at 390 passes with real imagery
(text-safe crops, darken overlays, readable CTAs); circles swipe row,
stacked value strip, 2-col grids, mobile campaign art direction all
verified on pixels. Sticky ATC and drawer nav are write-verified but need
on-device/Shopify-runtime confirmation (−12).

## 6. CATALOG / PRODUCTION READINESS: 15/100

Unchanged: 4 DRAFT products with clean hygiene; supplier data 0%
(CLASS A/B only), size data absent, 11 empty collections pending owner
unpublish, policies unpasted, GA4 unconnected, 0 reviews (honest), AutoDS
payment due 2026-08-30. Cannot be faked upward.

## Iteration gate (§52) — honest position

Engineering 88 < 95 and Visual 80 < 90, so the candidate is **not
finished** by the gate. The blockers are external and named: (1) rendered
Shopify-runtime verification is impossible from this environment — owner
remote preview (or granting a render path) is required; (2) owner visual
approval of the 12-frame shortlist (0/28 approved); (3) catalog reality
(active products, real collections, supplier data) gates every remaining
data surface. No further local iteration can move these three.
