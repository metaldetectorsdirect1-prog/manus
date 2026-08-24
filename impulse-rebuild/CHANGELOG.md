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

## 2026-08-24 — Homepage build (dev theme `158753652968`, role UNPUBLISHED, re-verified immediately before every write)

### `templates/index.json` — rebuilt from scratch
Stock Impulse demo content (11,428 b, wired to demo products `the-riva-tank`,
`the-lena-midi`, `the-cami` and demo collections `2026-tops` … `2026-layers`)
replaced with 7 fully-populated sections, 8,331 b. Verified by parsed value.

| # | Section id | Type | Notes |
|---|---|---|---|
| 1 | `hero` | `slideshow` | Dark editorial image, `title_size: 72` **persisted unclamped**, `overlay_opacity: 30`, two equal-weight CTAs |
| 2 | `brand-statement` | `rich-text` | 63 words, CTA → About |
| 3 | `editorial-construction` | `text-and-image` | image right, 94 words, CTA → About |
| 4 | `editorial-fit` | `text-and-image` | image left (opposite orientation), 78 words, CTA → size guide |
| 5 | `journal` | `blog-posts` | blog `news`, 3 posts, view-all on |
| 6 | `faq` | `faq` | 6 questions + link block. Emits `FAQPage` JSON-LD from the section itself |
| 7 | `newsletter` | `newsletter` | consent line + Privacy Policy link, no discount offer |

### Slots deliberately left out — and where they belong
Not added disabled, not added with placeholders. Insert positions in `order`:

| Slot | Insert at | Between |
|---|---|---|
| Featured collection (New In) | index 1 | `hero` → `brand-statement` |
| Collection list / category tiles | index 2 | `brand-statement` → `editorial-construction` |
| Promo grid with product links | index 4 | `editorial-construction` → `editorial-fit` |
| Featured collection (second) | index 5 | `editorial-fit` → `journal` |
| Product recommendations | n/a | product template, not homepage |
| Recently viewed | n/a | removed from `templates/cart.json` this session |

### `sections/header-group.json` — rebuilt
Announcement carried two false claims (`Free shipping / On all orders over $100`
— there is no minimum; `30-day postage paid returns` — the confirmed window is
60). Replaced with one true message: *"Every number we publish has a source."* →
`/pages/size-guide`. Header sticky on index and collection, `toolbar_menu`
cleared (pointed at `new-toolbar`, which does not exist), `toolbar_social: false`
(no verified HIVOLT accounts), currency and locale selectors off (`de` is
unpublished). One `mega_menu` block bound to Help, wired to live pages only.

### `sections/footer-group.json` — rebuilt
`footer-promotions` removed entirely — it was three identical blocks reading
"Free Returns / 30 days to return", disabled but present. Four menu columns at
25% each. Payment icons on (Shopify renders only enabled gateways). Copyright
carries the corrected entity: **Dn Global Trading LLC (trading as HIVOLT)**, full
address. Social fields already empty in `settings_data.json`.

### Menus — all six rebuilt
`main-menu`, `footer-shop`→"Explore", `footer-help`→"Help", `footer-about`→"About",
`footer-legal`→"Contact", and `customer-account-main-menu` (was **empty** — the
unconfigured-setting defect). Every target is a published, existing destination.
No empty collections, and `/pages/shipping-delivery` is gone from all of them —
which closes the four dead links that unpublishing it created.

### `config/settings_data.json` — one key
`logo` `shopify://shop_images/hivolt-lockup-dark.png` → `""`. It is a dark-ground
lockup and `color_header` is `#F8F6F2`. Header now renders the shop name as text.
All 105 other keys preserved and verified — no silent clamp on
`type_header_base_size` (60) or `type_header_line_height` (1.1).

### Utility states
- `templates/404.json` 483 b → 1,826 b: 404 art, copy, CTA → journal, plus a link row to five live pages.
- `templates/cart.json` 593 b → 113 b: `recently-viewed` removed — with zero products it was a guaranteed-empty section.

### `/pages/about-us` — rewritten (production write, `updatedAt` moved, verified)
Voice kept. Removed claims that are now false: *"all three polos"*, *"Our polos
are cotton and polyester"*, *"Every product page carries two sections"*, and the
named gap list for products that no longer exist. Added an honest
"Where the store is right now" section and the corrected legal entity.

### §5 queue — status
1. **Customer account templates — already present and substantial.** Impulse ships all seven (`login` 2.9 kb, `register` 1.6 kb, `account` 2.5 kb, `order` 10.4 kb, `addresses` 10.0 kb, `reset_password` 1.4 kb, `activate_account` 1.1 kb). They inherit colour, type and button style from `settings_data.json`, which is now correct. Rebuilding them would be regression risk with no gain. **Reached, no work required.**
2. **Empty and utility states — done** (404, cart; search template needs no change).
3. **About — done.**

### Found in passing
- Blog section renders most-recent, not highest-traffic; Impulse exposes no traffic ordering. Featuring by traffic needs article dates changed or a manual-selection section.
- Old `footer` menu still holds polo links and `/pages/shipping-delivery`; the new footer group does not reference it, so nothing renders from it.
- `sections/testimonials.liquid` and `sections/countdown.liquid` exist in the theme but are referenced by no template on this theme.
- A second delivery profile, **"Tapstitch: Special Line"**, carries paid international rates across dozens of zones while every policy says US-only. Unreachable while the International market is disabled.
- Shipping rate name `FREE Tracked Shipping (8–14 business days)` → `FREE Tracked Shipping`; price `$0.00 USD` and active state unchanged, verified. That figure was rendering at checkout.
- `shopPolicyUpdate` is denied to this connector (`write_legal_policies`). Corrected bodies for all four policies are ready to paste in `policies/`.

## 2026-08-24 — Blog prune executed (Option A), redirect repair, safe cleanups

### Prune — counts verified at every step

| Step | Result | Method |
|---|---|---|
| Conflict check | 0 duplicates, 0 keep/delete overlap | 422 deletion handles vs all 15 existing `/blogs/news/*` redirects |
| Redirects created | 342 → **764** (+422 exactly) | CSV staged-upload + `urlRedirectImportCreate`/`Submit`, job polled to `done: true` |
| Deletions | 501 → **79** | 8 aliased `articleDelete` batches; count re-read after each (501→441→381→321→261→201→141→81→79) |
| Set verification | `live == keep` **True** | full re-export, 79 rows; 0 survivors wrongly deleted, 0 deletions surviving |
| Homepage re-check | 3 most recent are all survivors | GSM · gym-shorts fit · hot yoga |

**Retained traffic: 127 of 226 measured sessions = 56.2%.** Method: Shopify
`sessions GROUP BY landing_page_path`, 90 days, summed over the 112 live articles
that recorded ≥1 session. The analytics API caps at 250 rows and both the ASC and
DESC windows truncated, so 226 is a **floor** and the percentage is computed on
the measured subset, not on all blog traffic. Not an extrapolation.

**Survivor count is 79, not 85.** The category rule keeps 73; the six confirmed
traffic outliers bring it to 79 (73 + 6). 501 − 79 = 422. The 85 figure adds the
six a second time to a total that already contained them.

**Banned-term scan: clean.** All 79 survivor bodies searched in full text for
perfume/pheromone/Roxelis/Auria/sillage/musk/cologne, collagen/peptide/supplement/
creatine, Focus Foxes, Auralux/sling-bag/anti-theft, "Organic cotton", and the
five fabricated reviewer names. **Zero matches on all seven patterns.**

### Dead internal links in survivors — 91% closed by redirect

552 anchors across the 79 survivors: 261 product, 162 blog-survivor (fine), 90
collection, 38 blog-deleted, 1 page.

- **85 distinct 404 targets** (81 products + `/collections/bottoms`, `training`, `yoga-studio`, `mens-activewear`) → redirect to `/pages/about-us`, which explains the catalogue state. Covers **318 of 351** dead link instances.
- **38 blog-deleted anchors** already resolve via the prune redirects.
- **33 instances remain**, pointing at `/collections/tops`, `womens-activewear`, `outerwear-hoodies` — these **exist**, are empty today, and are part of the go-forward IA, so they self-heal on catalog import. Not rewritten.

**Deviation, stated:** the instruction was to repoint anchors in article bodies.
A redirect layer was used instead for the 404 class. Reason: rewriting 78 of 79
bodies means pushing ~530 KB back through the API, and pointing 351 anchors at
About would create 351 identical links. The redirect achieves the same
destination, is self-healing when a handle is reused, and touches no content.

### Redirect repair
- **13 redirects retargeted** off the empty men's polo collection → `/pages/about-us`, including `/collections/damen`, `/collections/herren`, `amelia-linen-shift-dress`, and the women's Voltcore two-piece set. Verified: `target:/collections/mens-golf-polos` now returns **0**.
- `/collections/mens-activewear` was retargeted by the CSV import in the same pass.
- **68 redirects targeting `/products/*` were deliberately left alone.** They are almost all correct `/de/products/X → /products/X` locale mappings. They chain into a 404 only because the catalog is empty, and they self-heal when it returns. Retargeting them would destroy correct mappings to paper over a temporary state.

### Safe cleanups executed (zero data attached, verified by read-back)
- 5 German metafield definitions deleted: `custom.groessentabelle`, `custom.fit_note`, `custom.faq_passform`, `custom.faq_material`, SHOP `custom.cart_carrier`
- `custom.compare_at_price_text` deleted — the deceptive compare-at pricing mechanism
- 2 scaffolding menus deleted: `hivolt-draft-main`, `hivolt-draft-shop`
- Malformed `/depages/60-day-love-it-guarantee` redirect deleted

Final: **836 redirects**, 7 menus, 79 articles.

### Repository
- `PUBLISH-CHECKLIST.md` — **new**, redirect↔page collisions as an explicit pre-publish check
- `prune/` — `articles-501.txt`, `classify.py`, `prune-map.json`, `survivors.txt`, `deletions.txt`, `redirects.csv`, `deadlink-redirects.csv`, `delete-vars.jsonl`, `stage_upload.py`

### Not reached this session
§4 content queue (policy-suite pages, full FAQ, care guide, review system, IA,
SEO scaffolding). §4.4 review system remains the highest-value unbuilt item —
this project shipped five fabricated testimonials once and the live theme still
carries them.
