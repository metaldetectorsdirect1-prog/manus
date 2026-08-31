# PRODUCTION-CUTOVER-PLAN.md — 2026-08-28

Owner-executed publication of **MASTER r2** replacing the current MAIN.
IDs from the certification-session read-back (re-verify roles in the
theme admin immediately before publishing — names are metadata, the role
badge is authoritative):

- Current MAIN: `158753849576` — "GENERAL STORE — IMPULSE MASTER CANDIDATE"
- Candidate: `158874960104` — "GENERAL STORE — MASTER r2 (approved image swaps)"

## PRE-PUBLISH (owner, ~2 minutes)

1. Online Store → Themes: confirm the **Live** badge is on `158753849576`
   and `MASTER r2` sits in the library as unpublished.
2. Optional but recommended: open **Preview** on MASTER r2 and glance at
   Home, About (`/pages/about-us`), FAQ, a product URL
   (`/products/elena-relaxed-merino-wool-mock-neck-sweater` — renders only
   in preview while DRAFT), and the cart drawer. This is the remote
   rendered walk no session could execute (egress blocked); nothing in it
   gates the publish, but it is the last chance to catch a visual surprise.
3. Do not rename either theme during the cutover window.

## PUBLISH (owner, one action)

4. Themes → MASTER r2 → **⋯ → Publish**. Shopify atomically swaps roles:
   r2 becomes MAIN; `158753849576` automatically becomes UNPUBLISHED and
   stays in the library (this is the rollback artifact — do not delete it).

## IMMEDIATE POST-PUBLISH (first 2 minutes)

5. Load `https://hivolt-usa.com/` in a private window:
   - HV favicon appears in the tab (new in r2).
   - Header nav reads **Journal · About · Help** (About/Help open dropdowns).
   - Homepage: hero → strip → Trending tiles → campaigns → newsletter; no
     empty product grid, no broken images.
6. `/pages/about-us` shows the hero image + "Specification over slogan" +
   the mission text (NOT a map/demo skeleton — that is the old MAIN's bug).
7. `/pages/contact-us`, `/pages/faq`, `/pages/track-order` load normally.

## 5-MINUTE CHECK

8. View-source on `/`: one `<title>`, one `rel=canonical`, favicon link,
   two `application/ld+json` blocks (Organization with logo, WebSite).
9. View-source on `/blogs/news` + one article: BreadcrumbList (+ Article
   on the article).
10. Mobile (or narrow window ≤ 430px): drawer opens with Journal/About/
    Help hierarchy; homepage scrolls with no horizontal overflow.
11. Search icon → predictive overlay opens; with zero published products a
    query returns pages/articles only — graceful, no errors.

## 30-MINUTE CHECK

12. Google Search Console: URL-inspect `https://hivolt-usa.com/` (live
    test) — confirm canonical + structured data detected, no errors.
13. Rich Results test on `/` and one article URL.
14. Browser console on Home/About/an article: zero uncaught errors.
15. Confirm checkout still loads from the cart page (drawer → View cart →
    Checkout button; abandon before payment).

## ROLLBACK (if anything above fails badly)

Publish the previous production theme back — **do not rebuild anything**:
Themes → `158753849576` ("GENERAL STORE — IMPULSE MASTER CANDIDATE",
now unpublished) → Publish. One action restores the exact prior
storefront. Both themes persist through any number of publishes (this
store's own 2026-08-21 and 2026-08-28 publishes retained every theme).
Leave MASTER r2 in the library for diagnosis; report what failed.

## AFTER CATALOG ACTIVATION (not part of cutover)

- Re-add shop links to menu `master-storefront-nav` (`254991532264`):
  "New in → /collections/all", "Knitwear → /collections/knitwear" — they
  were removed for cutover because every product is DRAFT and both
  collections would render empty.
- Re-enable the homepage "The latest" featured-collection section
  (`latest`, currently disabled in templates/index.json) once ≥ 8 products
  are ACTIVE, and wire tile links on Trending/category tiles.
- Reconcile the FAQ vs track-order delivery windows and the US-only copy
  vs worldwide shipping zones before paid traffic.
