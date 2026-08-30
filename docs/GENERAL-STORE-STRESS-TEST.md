# GENERAL-STORE-STRESS-TEST.md — 48-card fixture stress test, 2026-08-28

This closes the prior gap "40-card grid stress test: not executable." It ran
locally, on real rendered pixels, using `playwright-core` against the
preinstalled Chromium (`/opt/pw-browsers/chromium`).

## Honest scope — what this does and does not prove

- **Proves:** the GENERAL STORE card/grid design language survives a
  48-product catalog and a 24-product homepage band at 7 viewports with zero
  layout failures. Theme-design scalability.
- **Does NOT prove:** real catalog data quality, Impulse runtime behavior
  (no Liquid, no theme JS, no Shopify request cycle runs locally), or image
  rendering (image CDNs are egress-blocked here, so media boxes are
  aspect-correct placeholders).
- **Fixture data is QA FIXTURE only.** `qa/fixture-products.json` (48
  records, seed 42) is marked `"qa": "QA FIXTURE"` on every record and never
  touches Shopify. No fake products, reviews, or collections were created
  anywhere. The fixtures live only in `/qa` and must never leak into
  production.

## Fixture coverage (48 products)

16 on sale (compare_at > price, badge shows true rounded percent), 4 sold
out, long and short titles, 0–4 color swatches, ratings on every 4th,
multi-option ("Choose options") every 5th, missing hover image every 6th,
single-image every 9th.

## Results — 14/14 checks PASS

| Harness | Viewport | Cols | Cards | overflowX | Row var | Badge collisions | Clamp fails | JS errors |
|---|---|---|---|---|---|---|---|---|
| grid | 320 | 2 | 48 | none | 0px | 0 | 0 | 0 |
| grid | 375 | 2 | 48 | none | 0px | 0 | 0 | 0 |
| grid | 390 | 2 | 48 | none | 0px | 0 | 0 | 0 |
| grid | 430 | 2 | 48 | none | 0px | 0 | 0 | 0 |
| grid | 768 | 3 | 48 | none | 0px | 0 | 0 | 0 |
| grid | 1024 | 4 | 48 | none | 0px | 0 | 0 | 0 |
| grid | 1440 | 4 | 48 | none | 0px | 0 | 0 | 0 |
| home | 320 | 2 | 24 | none | 0px | 0 | 0 | 0 |
| home | 375 | 2 | 24 | none | 0px | 0 | 0 | 0 |
| home | 390 | 2 | 24 | none | 0px | 0 | 0 | 0 |
| home | 430 | 2 | 24 | none | 0px | 0 | 0 | 0 |
| home | 768 | 2 | 24 | none | 0px | 0 | 0 | 0 |
| home | 1024 | 4 | 24 | none | 0px | 0 | 0 | 0 |
| home | 1440 | 4 | 24 | none | 0px | 0 | 0 | 0 |

First shopping surface (homepage harness, `[data-first-shopping-surface]`):
571px at 320w, 575px at 375w, 592px at 390w, 639px at 430w — roughly 0.7–0.75
viewport heights on phones, comfortably inside the "first 1.5–2 mobile
screens" merchandising target; 844px on ≥768w where the hero is taller.

Column progression verified: 2-col mobile → 3-col tablet → 4-col desktop
(grid); homepage trend tiles 2→4.

## Assertion-integrity note (recorded, not hidden)

The first green run required correcting a mis-specified assertion of mine:
`titleClampFailures` originally counted `scrollHeight > clientHeight`, which
is exactly what a *working* 2-line ellipsis clamp produces on long titles —
it flagged intentional truncation as failure (6 grid / 3 home false
positives). The invariant was redefined to what actually matters: the
**rendered** title box must never exceed the 2-line budget
(`clientHeight > 42px` fails). No layout changed; the metric did. Before
that fix the same run already showed 0 overflow, 0 collisions, 0px row
variance, 0 JS errors.

## Artifacts

- `qa/fixture-products.json`, `qa/fixture-data.js` — QA FIXTURE data
- `qa/grid-harness.html`, `qa/home-harness.html` — harnesses (marked QA
  FIXTURE in title and heading)
- `qa/run-stress.js` — runner; `node qa/run-stress.js` re-runs everything
- `qa/stress-results.json` — machine-readable results
- `qa/screenshots/*.png` — full-page captures at 320/390/1440 for both
  harnesses (first rendered pixels of the engagement)
