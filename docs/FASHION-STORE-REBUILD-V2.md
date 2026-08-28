# FASHION-STORE-REBUILD-V2.md — 2026-08-28

V1 was rejected on visual grounds; V2 rebuilds the active homepage to the
reference rhythm described in the rebuild directive (the reference PNG is not
present in the repo — docs/reference/ does not exist — so the written rhythm
in the directive is the design truth used).

## Removed from active (V1 → V2)
- V1 two-tile gateway promo-grid (weak generic composition)
- V1 text-and-image knit editorial (replaced by full-width campaigns)
- Every CTA/nav link into the empty knitwear collection (BLOCKED BY CATALOG;
  restored the moment products publish)
- All V1 campaign assets from active sections — owner reported logo defects
  in the previous program, so the entire active set was REGENERATED

## V2 active homepage (13 sections, 3 disabled)
promo bar (2 true claims) → full-bleed hero (dedicated d+m, no CTA while
catalog is draft) → one-line brand statement → trend report (4 portrait
cards) → full-width campaign 01 → category strip (4 squares) → full-width
campaign 02 (motion) → asymmetric collage (custom section, 1 anchor + 4
tiles) → featured evening moment → [product engine, disabled until products
publish] → newsletter (brand-moment image) → obsidian footer.
Disabled and hidden: master mixed-gender hero, men's hero, men's trend grid.

## Design system V2
Palette: white #FFFFFF dominant · obsidian #0A0A0B · off-white #F7F5F1 ·
light stone #E9E6E0 borders · deep fashion red #C1122F for sale/savings/cart
dot only. Typography: Host Grotesk (n5) headings — the sans commerce
workhorse per directive — over Inter body; uppercase 13px nav; serif dropped
from the global heading role (kept available for future campaign-only use).
Cards: portrait, square corners, hover second image, Quick Add. Grid: 2-col
mobile / 4-col desktop (PLP per_row 4). Tile gaps 8px.

## New custom section
`sections/fashion-collage.liquid` — asymmetric CSS grid (anchor spans 2 rows
on desktop, 2-col mobile), links render only when set, lazy images with
srcset, reduced-motion respected, blank-state safe.

## Impulse native retained
quick shop, product cards/grid, swatches, second-image hover, cart drawer,
predictive search, filters+sort (drawer), recommendations, recently viewed,
section groups, announcement bar, newsletter, footer, image-grid, rich-text.

## Navigation truth
`fashion-main` menu trimmed to Journal / About / Help — the two collection
links removed while the collection is empty. Live `main-menu` untouched.
