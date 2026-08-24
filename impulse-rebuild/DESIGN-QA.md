# DESIGN-QA.md

Against §8 Acceptance Criteria. **Phase 3–4 is not reported complete** — six of
the nine criteria cannot be evaluated without a catalog and rendered pages.

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Squint test | **BLOCKED** | Needs rendered pages. `index.json` is still stock demo content, held pending products |
| 2 | Grid test | **BLOCKED** | Zero products. No grid exists to compare |
| 3 | Five-second test | **BLOCKED** | Homepage not built |
| 4 | **Tell audit** | **PASS (partial)** | See below — the forbidden list was scanned and acted on |
| 5 | **Consistency sweep** | **PASS** | 1 accent on 2 CTA keys · 2 families · 2 weights · radius 0 throughout · no shadows/gradients |
| 6 | **Contrast pass** | **PASS** | 6 pairs measured, all ≥ their floor. Table in `DESIGN-SYSTEM.md` |
| 7 | Speed pass | **BLOCKED** | No egress to the storefront from this environment (403 at CONNECT); Lighthouse cannot run here |
| 8 | 375px walkthrough | **BLOCKED** | Same — cannot render the store |
| 9 | Density check | **BLOCKED** | No product page to check |

## Criterion 4 — tell audit, findings

The §6 forbidden list was scanned across every template. Four hits, all removed:

| Tell | Where | Action |
|---|---|---|
| **Review counts / testimonials without reviews** | `product.json` — 5 fabricated 5-star testimonials with invented names and cities, live in the `order` array | **removed** |
| **Urgency** | `collection.json` — "take an extra 10% off sale items — limited time", for a discount that does not exist | **removed** |
| **Unsubstantiated claim** | `product.json` — sales point "Organic cotton", no supplier documentation | **removed** |
| **Dead social icons** | `settings_data.json` — five links pointing at *Shopify's own* demo accounts | **all 10 fields emptied** |

Not found anywhere: press logos, countdown timers, "X people viewing", spin-to-win,
exit-intent wheels, stock badge graphics. `inventory_enable` is `false`, so no
scarcity cue can render.

Marked partial rather than pass because the audit covered template JSON and theme
settings. Page and product copy cannot be fully swept until they are rewritten for
the women's catalog, which waits on the supplier and the products.

## Screenshots

`/qa-screenshots/design/` is **empty and honestly so.** Rendering the store
requires reaching `f36zps-yd.myshopify.com`, which returns 403 at CONNECT under
this environment's network policy. Playwright is installed but has nothing it can
reach. Screenshot evidence must be captured from a machine with storefront access.
