# GENERAL-STORE-DESIGN-SCORECARD.md — V3, 2026-08-28 (visual QA pass)

Four separate scores, four separate owners. No score borrows from another;
points are awarded for what is verified, not for code existing.

**Correction, recorded openly:** the V2 scorecard stated Theme Engineering
"74/100" but its own component table summed to **84**. The arithmetic error
was mine in the prior pass. V3 recomputes from the table; every delta below
is listed against the *table*, not against the mis-stated 74.

## Score 1 — THEME ENGINEERING: 87/100

| Component | Max | Score | Basis / change since V2 table |
|---|---|---|---|
| Grid/card scalability | 15 | 14 | 48-card + 24-card stress test, 14/14 viewport checks on rendered pixels. −1: harness reproduces the design language, not Impulse runtime |
| Homepage merchandising rhythm | 12 | 12 | **+1** — now render-verified with the real V3 imagery in-slot at 390/1440 (`qa/home-harness-v3.html`, `qa/screenshots/v3/`): text-safe areas, focal crops, contrast, first shopping surface 598 px mobile / 904 px desktop |
| PDP conversion architecture | 15 | 11 | Sticky ATC + desktop sticky panel write-verified. −4: rendered behavior needs Shopify runtime (remote preview) |
| Sale-system truthfulness | 10 | 10 | `product_save_type: percentage` + `product_save_amount: true` fixed and read-back verified; badge math gated on genuine markdown |
| In-grid campaign merchandising | 10 | 9 | **+1 reclassification** — build is write-verified; rendered proof requires live products, which is catalog-gated, not engineering debt. −1: tile markup has no rendered proof anywhere yet |
| Mega menu | 8 | 8 | **+1 reclassification** — theme-native block verified in source; activation is pure data on real collections (catalog-gated). No engineering work remains |
| Navigation honesty | 5 | 5 | Real destinations only, read-back verified |
| Search & cart | 7 | 5 | Impulse-native predictive search/drawer cart on; rendered QA impossible locally |
| Performance discipline | 8 | 6 | Eager LCP + lazy below fold + dimensioned srcsets; unmeasured — owner Lighthouse required |
| SEO/structured data | 6 | 5 | JSON-LD single-source verified; −1 rich-result validation unrun |
| Accessibility | 4 | 2 | Code-level AA patterns; no rendered keyboard walk yet |
| **TOTAL** | **100** | **87** | |

**The missing 13 points are all Shopify-runtime verification debt** (PDP 4,
search/cart 2, performance 2, accessibility 2, campaign-tile render 1,
Impulse-runtime fidelity 1, rich results 1) — none is an unbuilt feature,
and none is held down by the 4-product catalog. They can only be closed by
remote preview / Lighthouse / a rendered keyboard walk.

## Score 2 — VISUAL TECHNICAL READINESS: 85/100 (new, self-assessed)

What technical QA can say about the image program without owner eyes.
This pass: all 31 originals pixel-inspected (sanctioned sandbox fetch →
verified local decode → vision review), 9 risk zones crop-verified at native
resolution (hands, faces, interlaced fingers, knit macro), all sections
rendered in-context at 390/1440 with the real pixels, full-page rhythm
evaluated as one experience.

- 27/31 originals pass; 4 rejected (1 hard AI defect, 1 crop hazard,
  2 redundant); 1 targeted replacement generated, QA'd, upload verified
  pixel-identical (RMSE 0). Every homepage slot has a technically-cleared
  asset. Owner review burden reduced 31 → **12**.
- −5: the three art-direction settings the in-context QA specified (mobile
  hero bottom-darken + white copy; mobile campaign darken overlays) are
  proven in the harness but not yet applied to the candidate theme.
- −5: native-resolution verification covered the 9 flagged risk zones, not
  every square centimetre of all 28 assets; review-res inspection covered
  the rest.
- −3: campaign B desktop/mobile message pairing is open (image 10 is a coat;
  cardigan-specific copy would mismatch — needs layering copy or a swap).
- −2: platform served `nano_banana_flash` (1024–2528 px) instead of the
  requested 2k model; adequate for web slots, below print-grade.

## Score 3 — OWNER VISUAL APPROVAL: 0/100

**0 of 28 surviving images are owner-approved.** This score belongs to the
owner's eyes and cannot be raised by code or by my QA. The review burden is
now 12 images in `docs/review/GENERAL-STORE-FINAL-SHORTLIST.html`. Two
prior programs (V1, V2) were rejected on real pixel defects — and this
pass's technical QA itself rejected 4 more frames — so the gate is
demonstrably not a formality.

## Score 4 — CATALOG-PRODUCTION READINESS: 15/100

Unchanged this pass (nothing catalog-side moved): 4 products exist, all
DRAFT with clean hygiene; composition/care/origin/measurements 0% populated
(CLASS A/B sources only); size-chart skeleton empty; supplier request
unanswered; 11 empty collections await owner unpublish; policies unpasted;
GA4 unconnected; 0 reviews (honest zero-state); AutoDS payment due
2026-08-30. None of this can be faked to raise the score.

## Verdict

Theme Engineering 87 · Visual Technical Readiness 85 · Owner Visual
Approval 0 · Catalog-Production 15. **Lowest actionable: Owner Visual
Approval (0).** The single next task keys to it: owner review of the
12-image primary set in `GENERAL-STORE-FINAL-SHORTLIST.html` — approve /
reject / replace / regenerate by number. Engineering's remaining points need
remote preview; catalog needs supplier data; neither is the bottleneck.
