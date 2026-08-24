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

## 2026-08-24 — Track A §3.1 · Legacy contamination sweep

### Shopify changes

**None. This was a read-only sweep.** No shop-level resource was created,
modified or deleted. Every finding below is classification, not action.

The only Shopify write this session preceded the sweep: `/pages/shipping-delivery`
set `isPublished: false` (§2 immediate action), verified by read-back.

### Surfaces enumerated in full

| Surface | Count | Method |
|---|--:|---|
| URL redirects | **331** | `urlRedirectsCount` + full row dump, reconciled |
| Pages | 18 | full enumeration |
| Collections | 15 | full enumeration |
| Menus | 9 | full enumeration |
| Metafield definitions | 38 | 5 owner types |
| Metaobject definitions | 4 | full enumeration |
| Files | 150 | full enumeration, 3 pages |
| Shop policies | 5 | full bodies read |
| Locales · markets · themes | 2 · 2 · 3 | full enumeration |

### Findings that changed the plan

1. **Catalog is empty — `productsCount: 0`**, confirmed three ways (`productsCount`,
   `products(first:5)`, `productVariantsCount`). All 15 collections hold 0 products.
   Makes metafield/menu/file cleanup free of data loss.
2. **Fifth fabrication surface found: shop policies.** The 2–4 / 8–14 shipping
   figures the brand block ruled out for reuse are live in Shipping, Terms §5 and
   Contact. Refund policy says "5-7 business days" where the owner-confirmed page
   says 5. Terms §1 claims the registered entity is "HIVOLT", not **Dn Global
   Trading LLC**. → 7 new open rows in `CLAIMS-REGISTER.md`.
3. **Unpublishing `shipping-delivery` created 4 dead links** in `footer`,
   `footer-help`, `footer-legal` and one redirect target. Fix is menu edits.
4. **`LOCALE-AUDIT.md` corrected** — 170 `/de/blogs/news/*` redirects, not "a
   handful". The German blog *was* a full mirror; it is already redirect-covered.
5. **Three redirect ↔ page handle collisions** (`size-chart`, `fabric-weight-index`,
   `voltcore`) — publishing any of those pages silently disables a redirect.
6. **Four redirects point at non-existent targets**; 14 point women's and perfume
   URLs at an empty men's polo collection.
7. **Build-record correction** — only 2 of the 4 recorded brand files are on the
   store. `hivolt-lockup-light.png` and `hivolt-lockup.png` were never uploaded.

### Repository changes
- `impulse-rebuild/LEGACY-AUDIT.md` — **new**, the §3.1 deliverable
- `impulse-rebuild/CLAIMS-REGISTER.md` — open rows 4–5 closed, rows 7–13 opened;
  Returns reclassified **provisional pending supplier**; house standard codified
  from `size-guide` per §1.6
- `impulse-rebuild/LOCALE-AUDIT.md` — corrected, with method and cause
- `impulse-rebuild/CHANGELOG.md` — this entry

### Blog prune (§3.2) status
**Step 1 complete.** All 331 redirects pulled and reconciled; no conflicts in the
`/blogs/news/*` namespace. Step 2 (deletion map) needs no further reads.

## 2026-08-24 — Track A §3.2 · Blog prune, steps 1–2

### Shopify changes

| Action | Before | After | Verified |
|---|---|---|---|
| `urlRedirectCreate` ×11 (aliased, one request) | 331 redirects | **342** redirects | count +11 exactly; 4 paths spot-read-back with correct target |

The eleven paths were perfume-era article URLs taking **23 measured sessions in
90 days** to hard 404s — no article, no redirect. Confirmed both ways before
writing: `articles(query:"handle:…")` empty, `urlRedirects(query:"path:…")` empty,
against a control path that returned its known redirect. All now → `/blogs/news`,
matching the four that already had redirects.

`userErrors: []` was not treated as proof. No article was deleted. No other
resource changed.

### Repository changes
- `impulse-rebuild/PRUNE-MAP.md` — **new**, the §3.2 step-2 deliverable
- `impulse-rebuild/prune/articles-501.txt` — full corpus, 501 lines, 501 unique
- `impulse-rebuild/prune/classify.py` — deterministic classifier, rules in-file
- `impulse-rebuild/prune/prune-map.json`, `survivors.txt` (79), `deletions.txt` (422)

### Where the prune stands
Steps 1–2 complete. **Stopped at step 3 — "verify" — which is the owner's own
gate.** The map recommends 79 survivors / 422 deletions, retaining 56.2% of
measured blog traffic while removing 84% of the corpus.

`BLOG-AUDIT.md`'s original 13-survivor plan is no longer supportable: it came from
a 26-article sample that file itself flagged as too thin, and measured traffic is
now available for the whole corpus — 112 live articles earn sessions, not 13.

Two findings that reduce the prune's cost:
- The `/de/` arm needs no work. 170 redirects already exist; after deletion each
  chains `/de/blogs/news/X → /blogs/news/X → /blogs/news` and resolves.
- Aliased batch mutations work on this connector (proven by the 11-redirect call),
  so the whole prune is ~20 calls, not the oversized batch job previously assumed.

### Product-independent work remaining (§3.4)
Executable with no supplier and no catalog: the content/template queue (§3.3) —
policy-suite page structure, FAQ, About, care guide, customer-account templates,
empty/utility states, footer, IA, SEO scaffolding — plus the prune once its gate
clears, and the safe cleanups itemised in `LEGACY-AUDIT.md` §11. What is genuinely
blocked is narrower than it looks: every *number* on a policy or shipping page,
and every product, image and size chart.
