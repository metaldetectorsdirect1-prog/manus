# V3-REFERENCE-COMPARISON.md — reference rhythm vs HIVOLT V3

The named primary reference file `docs/reference/fashion-store-reference.png`
is **not present in the repository** (verified against the working tree and
every origin branch on 2026-08-28); no owner V2 screenshot is committed
either. This matrix therefore maps V3 against the reference structure as
written in the V3 directive (Fashion-Nova-style merchandising rhythm), which
is the best evidence available. If the owner commits the screenshot, this
matrix should be re-scored against real pixels.

| Reference section | HIVOLT V3 equivalent | Similarity goal | Why different | Status |
|---|---|---|---|---|
| Promotion bar | Announcement bar, 2 rotating true claims, black/white, non-compact | Strong top promo line | Only true claims (free shipping, 60-day returns) — no fake discounts allowed | BUILT |
| Main hero | fashion-hero, 86vh desktop, dedicated 4:5 mobile frame, uppercase HTML headline | Full-bleed campaign scale | No shopping CTA — every commerce destination is empty while products are DRAFT | BUILT |
| Thin promo/brand strip | fashion-strip (obsidian band, uppercase 13px) | Momentum divider | Claims restricted to verified facts | BUILT |
| Trending now | image-grid, 4 portrait cards, one campaign family (same studio/light/grade) | Editorial card row | Tiles unlinked until collections are live | BUILT |
| Large campaign 01 | campaign-a: two models / architecture, 74vh | Campaign scale + variety | — | BUILT |
| Large campaign 02 | campaign-b: single model / plain facade, 74vh | Second distinct composition | — | BUILT |
| Shop by category | fashion-category-strip: 6 square tiles, desktop grid, mobile swipe | Compact category discovery | 6 tiles not 8 — only categories with real/imminent Phase-5 inventory; unlinked until live | BUILT |
| Large campaign 03 | campaign-c: studio movement, 70vh | Third distinct composition | — | BUILT |
| Category/look collage | fashion-collage: dominant left tile + 4 complementary right, one shoot world | Deliberate merchandising composition | Labels descriptive, unlinked | BUILT |
| Promotional / sale band | **Omitted** | — | No legitimate sale exists; fake urgency is forbidden | OMITTED (honest) |
| Product discovery | featured-collection, 4-per-row ×2, quick add, mobile scroll — `disabled: true` | Dense product grid | 4 products are DRAFT; publication requires owner authorization | READY, DISABLED |
| Second discovery / recommendations | **Omitted** | — | Not enough products to power it honestly | OMITTED (honest) |
| Newsletter | Rebuilt: "Be first to know", still-life crop, off-white, real Shopify form | Clean capture block | No fake discount incentive | BUILT |
| Footer | Obsidian bg / white type (settings), 3 menus + newsletter, real contact | Clear column hierarchy | Groups limited to real destinations; no social links (none exist) | BUILT |

## Density / rhythm scoring vs the directive's targets

- **Header density**: promo bar non-compact + sticky header; nav has 3 links
  (Journal/About/Help) not a 10-item category nav — every category link
  would be a dead commerce destination while the catalog is DRAFT. The full
  nav is staged to appear with product publication. Text logo (no image
  logo asset exists; wordmark-as-image would require generated typography,
  which the zero-generated-text rule forbids from the AI pipeline — a real
  vector wordmark is an owner-supplied asset).
- **Hero height**: 86vh desktop, ~117vw-capped 4:5 mobile — full-bleed.
- **Card density**: trend 4-across desktop / 2-col mobile; categories
  6-across desktop / 38vw swipe tiles mobile.
- **Campaign frequency**: 3 large campaigns interleaved between card rows —
  matches the reference alternation (full-bleed ↔ contained).
- **Product density**: grid staged at 4/row ×2 rows + quick add; activates
  with publication.
- **Spacing**: stock section top/bottom spacing suppressed
  (`space_above/space_below: false`), strip and campaign sections flush
  (`index-section--flush`), tighter mobile paddings in custom sections.
- **Footer hierarchy**: 3 titled columns + newsletter at 20/20/20/40 widths
  on obsidian.

Visible section count: V2 had 8 visible content sections, 3 of them
near-identical editorial heroes; V3 has 10 visible sections with three
distinct campaign compositions, two card systems, a collage and a strip —
the editorial-image / editorial-image / editorial-image monotony is gone.

**Not verified visually.** This matrix records intent and implementation,
not rendered pixels. Status of the whole rebuild: VISUAL REVIEW REQUIRED.
