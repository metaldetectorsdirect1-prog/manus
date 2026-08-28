# GENERAL-STORE-REFERENCE-DECONSTRUCTION.md — 2026-08-28

**Evidence caveat first:** no reference screenshot reached this session (not
attached; `docs/reference/` does not exist in any branch — verified again
today). This deconstruction therefore works from the written description of
the Fashion Nova reference supplied in the earlier V2 rescue directive plus
the general structure of that merchandising model. If the owner commits the
screenshot, this file should be re-scored against real pixels.

## The ecommerce system behind the reference

| Property | Reference pattern | Our implementation |
|---|---|---|
| Page width | Full-bleed campaigns, ~1400px contained grids | `--layout-section-max-inline-size: 1420px` (Impulse) + `index-section--flush` full-bleed heroes |
| Spacing rhythm | Tight; sections nearly touch | `space_above/below: false`, flush strips, 8px card gaps |
| Header | Compact promo bar + dense nav + search/account/cart | Non-compact announcement (2 true claims) + sticky header + predictive search + account + drawer cart |
| Announcement | Rotating promos, urgency | Rotating 2-block announcement, editor-configurable; **true claims only — no invented promotions** |
| Hero | Full-width seasonal campaign, big type, CTA | fashion-hero: dedicated D+M images, uppercase clamp headline, CTA fields (blank while catalog is DRAFT — no dead links) |
| Promo interruption strip | Red sale band | fashion-strip (dark/forest/light schemes, editor text) — carries true claims; a red sale scheme activates only when a real sale exists |
| Category cards | 4–6 portrait tiles | image-grid ×4 portrait ("Trending now") + fashion-category-strip ×6 square with mobile scroll-snap |
| Campaign frequency | A campaign every 2–3 sections | 3 distinct campaigns interleaved (two-model / single-model / studio-motion) |
| Product grid | Dominant, dense, long | featured-collection 4/row ×2 + Quick Add, staged `disabled: true` — **BLOCKED BY PRODUCT DATA (4 DRAFT products; grid flips on at publication)** |
| Card spacing | Compact, consistent crops | portrait fill, 2-col mobile / 4-col desktop, grid_spacing 8 |
| Sale merchandising | -% badges everywhere | Impulse sale tags in #D0021B with **mathematical percent display** (`product_save_type: percent`, derives from compare_at > price only) |
| Footer | Dense multi-column + newsletter + payments | 3 real menus + newsletter + payment icons + legal entity |

## Section mapping (reference → ours, original naming/creative)

Fashion campaign hero → Seasonal campaign hero ("Modern essentials, redefined.")
"Icon Edit"-style edit → Trending now (4 tiles)
Matching-sets campaign → Campaign A ("Two ways to layer")
Denim campaign → Campaign B ("The new season edit")
Current-obsession row → Shop by category (6-tile swipe strip)
Long women's product grid → "The latest" product grid (staged, catalog-gated)
Sale band → omitted until a real sale exists (honest)
Email capture → "Be first to know"

No reference wording, photography, models, logos, or proprietary graphics
were reproduced; only layout function, density and rhythm.

## Catalog-truth constraints on this candidate

The store's real catalog is 4 DRAFT women's-fashion products (fresh read).
So: category tiles are unlinked, the product grid is disabled, nav is
3 real links, and the hero carries no shop CTA — all one-flip staged for
publication day. Categories (Home/Beauty/Tech/Pets…) are architecture in
the section library, not fake tiles: each activates only when a real
collection with products exists (Phase-5 import plan, PRODUCT-RESEARCH §8).
