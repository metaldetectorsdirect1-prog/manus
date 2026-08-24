# CHANGELOG.md

## 2026-08-24 — Phase 0 + Phase 1

### Shopify changes
| Action | Before | After |
|---|---|---|
| `themeDuplicate` on `158743363816` | 1 theme (Impulse, MAIN) | 2 themes — dev copy `158753652968` `IMPULSE-REBUILD-2026-08-24`, role UNPUBLISHED |

That is the only write. No theme file, product, collection, page, menu, policy
or setting was modified. Nothing published.

### Repository changes
- `impulse-rebuild/AUDIT.md` — new
- `impulse-rebuild/ASSUMPTIONS.md` — new
- `impulse-rebuild/APP-CONFLICTS.md` — new
- `impulse-rebuild/CHANGELOG.md` — new

### Phases not started
2–14. Blocked on B1 (zero products) and B2 (category contradiction). See AUDIT.md.

## 2026-08-24 — Phase 2 + section removals

All writes to **`158753652968` (UNPUBLISHED)**. Live theme untouched.

| File | Before | After |
|---|---|---|
| `config/settings_data.json` | stock Impulse, 4 presets, 5 shopify.com social links, no logo/favicon | HIVOLT design system, 102 keys, all social emptied, real logo + favicon |
| `templates/product.json` | 8 sections incl. **5 fake testimonials**, "Organic cotton", 4 placeholder tabs, 3 disabled sections | 2 sections, 5 blocks, no fabricated content |
| `templates/collection.json` | fake "extra 10% off, limited time" banner; parallax on; header disabled | banner removed; parallax off; header enabled |
| `templates/404.json` | `main` + `featured-collection` (empty collection) | `main` |
| `templates/cart.json` | `main` + `recently-viewed` + `featured-collection` | `main` + `recently-viewed` |

Repo: `DESIGN-SYSTEM.md` new, `VERIFICATION-PARTIAL.md` new, `AUDIT.md`
addendum, `ASSUMPTIONS.md` decisions 7–16.

Not started: Phases 3, 4, 7; product-dependent halves of 5 and 6; imagery
generation; the §13 verification pass. All blocked on B1/B3.
