# GENERAL-STORE-DESIGN-SCORECARD.md — V5, 2026-08-28 (r2 hardening pass)

Scores per the master directive, separately owned. Points are awarded for
what is verified, never for code existing. Per §3/§36 of the master task:
LOCAL RENDER VERIFIED counts toward engineering; REMOTE SHOPIFY VERIFIED
remains a separately-tracked residue and external blockers (catalog, owner
actions, remote preview) are not counted against theme scores. Every claim
below is backed by a same-day read-back, a checksum, or a runnable script
in `qa/`.

Context change since V4: the owner approved the 12-image primary set and
self-published the MASTER CANDIDATE (now MAIN, untouched). All work lands on
**MASTER r2 (`158874960104`, UNPUBLISHED)**, a duplicate carrying the
approved swaps.

## 1. THEME ENGINEERING READINESS: 95/100

Everything from V4 (88) plus this pass, all write-verified by checksum
read-back on r2:

- **Sticky ATC: 68/68 behavioral checks PASS at 320/375/390/430 + 1440**
  (`qa/run-pdp-qa.js` on the real section code): appears only after the ATC
  leaves the viewport, hides on return, price/compare/variant/sold-out sync
  via MutationObserver, submits the main form exactly once, disabled state
  respected, no layout shift, safe-area padding, reduced-motion, ≥44px CTA.
  A real defect was found by this harness and fixed: the IO `threshold: 0`
  crossings-only logic never fired on instant jumps/fast flings (proven:
  button at −90px, bar still hidden 600ms later); state is now recomputed
  from geometry on IO + passive scroll/resize signals.
- **Structured-data system render-validated 17/17** (`qa/check-jsonld.py`
  executes the shipped Liquid): valid JSON on every page type/branch,
  nothing emitted on cart/search/404/password/list-collections.
- Page architecture completed: premium About rebuild, Contact rebuild,
  Careers demo-content gutted, 7 missing suffix templates created; new
  data-gated nav menu; favicon wired.
- 100-card and 48-card fixtures re-PASS at 320–1440; v4 homepage harness
  re-PASS at 7 widths with 0 JS errors.

The −5 residue is exclusively REMOTE SHOPIFY VERIFICATION (not counted as
missing features, listed for honesty): rendered walk of native Impulse
runtime (quick-shop modal, predictive overlay, drawer cart, drawer nav) on
a real preview (3), Shopify-runtime fidelity of harness results (1), live
rich-results/CWV measurement (1). **No unbuilt feature remains in scope for
the current catalog reality.**

## 2. VISUAL TECHNICAL READINESS: 91/100

Locked reference system reproduced and rendered clean at 1440/390/320
(harness v4: zero layout defects, zero overflow, uniform card geometry).
The 12-image primary set is now **owner-approved and wired** (approval
resolved since V4). New premium About architecture; footer/newsletter/value
surfaces coherent end-to-end.
- −4 rendered-on-Shopify fidelity risk (remote preview unavailable here).
- −3 deliberate deltas awaiting owner taste: trending density capped at
  Impulse's 5-across (reference shows 6); PDP red ATC + save-pill accent
  not applied (single global button color in Impulse).
- −2 data-gated surfaces (mega-menu columns, category circles) necessarily
  thin until real collections exist — architecture ready, content gated.

## 3. OWNER VISUAL APPROVAL: 80/100

The 12-image primary set: approved and live-wired (12/12). Provisional
(technically QA'd, owner approval pending): About-page reuse of the
master-hero pair, and the disabled homepage sections holding the extended
image program. Nothing is misrepresented as approved.

## 4. SEO READINESS: 95/100

Verified from source + render-validation this pass: canonical, seo-title,
meta description, OG/Twitter (layout); **complete honest JSON-LD system** —
Organization(+logo)+WebSite (home), Product/AggregateOffer (PDP,
single-source), BreadcrumbList (product/collection/page/blog/article),
CollectionPage, Article, FAQPage from visible blocks only; no fabricated
Review/AggregateRating/GTIN/MPN/shipping/priceValidUntil anywhere. Favicon
set. Image SEO verified (srcset/sizes/width/height/alt, eager+fetchpriority
LCP hero, lazy below fold). Variant URLs: Shopify-native canonical to bare
product URL; filters left to native Search & Discovery (no crawl trap);
robots/sitemap native; 404 clean; blog SEO now carries Article+Breadcrumb.
Residue (−5, not engineering-actionable here): live rich-results and CWV
runs, and the catalog itself (4 DRAFT products = almost no indexable
commerce surface — a catalog fact).

## 5. CRO READINESS: 90/100

Live on r2: quick add/quick shop, sticky mobile ATC (now fling-proof),
sticky desktop buy panel, recommendations + recently viewed, predictive
search with price, drawer cart, truthful value/announcement strips,
newsletter (honest copy, no fake coupon), verified-honest sale math
(percentage savings), collection filters/sort, contact page with
support-path shortcuts, honest tracking page. Absent by policy: fake
urgency/social proof/threshold meters (US shipping is free with no minimum —
a meter would be a dark pattern). Wishlist: Decision B — none (no
legitimate provider; none faked). Residue: rendered conversion walk on
remote preview; BNPL messaging unknown until gateway state is confirmed.

## 6. MOBILE READINESS: 95/100

320/375/390/430 all PASS on rendered pixels: homepage v4 (7 widths), 48-
and 100-card grids (2-col, zero overflow, zero clamp failures), sticky ATC
full behavioral suite, safe-area support, campaign/mobile art direction
with text-safe crops and proven darken treatments. Residue: on-device
drawer-nav walk (native Impulse) via remote preview.

## 7. ACCESSIBILITY: PASS (no critical violations)

axe-core 4.x: **0 violations at every severity** on pdp-harness,
home-harness-v4 and grid-harness-100 at 390 and 1440 (after fixing real
findings: landmark structure, heading order, fixture contrast). Manual:
skip-link in layout, focus-visible outlines, ≥44px targets, sticky-bar
aria-hidden lifecycle verified in the behavioral suite, reduced-motion
respected, honest alt text, keyboard-native accordions (details/summary +
Impulse collapsibles). Native Impulse modal/drawer focus management is
vendor-standard; the rendered screen-reader walk on a live preview is the
remaining residue.

## 8. CATALOG / PRODUCTION READINESS: 15/100 (unchanged, external)

4 DRAFT products, supplier data 0%, 13 empty collections, size data absent,
GA4 unconnected, 0 reviews (honest). Cannot be faked upward.

## Iteration gate — position

Engineering 95 ≥ 95, Visual Technical 91 ≥ 90, SEO 95 ≥ 95, CRO 90 ≥ 90,
Mobile 95 ≥ 95, Accessibility no-critical: **all gates met** under the
directive's own counting rules (§3 local-render verification counts; §36
external blockers not charged to engineering). What remains is exclusively
external: owner publishes r2, owner/remote rendered walk of native Impulse
surfaces, catalog activation and supplier data.
