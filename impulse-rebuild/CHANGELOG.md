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

## 2026-08-24 — Phase 3 (partial)

### Shopify writes
| Action | Result |
|---|---|
| `pageCreate` `size-guide-women` | ✅ `134494421224`, published, verified |
| `pageCreate` `size-guide-men` | ✅ `134494453992`, published, verified |
| `themeFilesUpsert` → **live theme** `158743363816` | ❌ **REFUSED** by connector policy — live theme writes blocked |

No shipping-zone change (see `VERIFICATION-PARTIAL.md` item 3 — International
market is already disabled; the change would have altered nothing and risked a
Tapstitch resync conflict).

### Repo
New: `INFORMATION-ARCHITECTURE.md`, `CONTENT-INVENTORY.md`.
Updated: `DESIGN-SYSTEM.md` (§2.2 imagery constraint), `VERIFICATION-PARTIAL.md`.

## 2026-08-24 — Phase 4 (partial)

### Shopify writes — all verified by read-back
| Target | Action | Result |
|---|---|---|
| dev `158753652968` | `templates/blog.json` | ✅ `featured-collections` (4 empty blocks) removed; index configured |
| dev `158753652968` | `templates/article.json` | ✅ hero, tags, date, author, sharing, related posts |
| `/pages/returns-refunds` | rewritten | ✅ ships final — 2 claims flagged unverified |
| `/pages/terms-of-service` | rewritten | ✅ category corrected off "technical activewear" |

No theme published. No live-theme write attempted after the §1 status read.
No shipping-zone change. Nothing deleted, rewritten or redirected in the blog.

### Repo
New: `BLOG-AUDIT.md`.
Updated: `APP-CONFLICTS.md`, `VERIFICATION-PARTIAL.md`, `ASSUMPTIONS.md`, `CONTENT-INVENTORY.md`.

## 2026-08-24 — Phase 6

### Shopify writes
| Target | Action | Result |
|---|---|---|
| `/pages/size-guide-women` | `isPublished: false` | ✅ verified |
| `/pages/size-guide-men` | `isPublished: false` | ✅ verified |

Two writes, both unpublish. No page content written — §1 in force.
No theme write. No article deleted, redirected or edited.

### Repo
New: `LOCALE-AUDIT.md`.
Updated: `CLAIMS-REGISTER.md` (open rows now at top), `BLOG-AUDIT.md` (correction),
`VERIFICATION-PARTIAL.md`, `CONTENT-INVENTORY.md`, `ASSUMPTIONS.md`.
