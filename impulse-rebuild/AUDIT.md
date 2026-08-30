# AUDIT.md — Impulse rebuild, Phase 1

Store `f36zps-yd.myshopify.com` / `hivolt-usa.com`. Audited 2026-08-24 via the
Shopify Admin API. No Shopify CLI exists in this environment and direct egress
to the store is denied at CONNECT, so every fact below was read through the MCP
connector.

## Phase 0 result

| | |
|---|---|
| Published theme | `158743363816` **Impulse**, `themeStoreId 857`, role `MAIN` |
| Created | `2026-08-23T23:16:56Z` — a **fresh install**, hours old |
| Dev copy | `158753652968` **IMPULSE-REBUILD-2026-08-24**, role `UNPUBLISHED` |
| Theme files | 250+ enumerated; stock Impulse plus GemPages injections |

The store was reset shortly before this run: every theme that existed on
2026-08-23 (v35, v7, v6, v5, v30, v37, two Impulse copies) has been **deleted**,
leaving one fresh Impulse install.

---

## ⛔ BLOCKER B1 — The catalog is empty. The build cannot complete.

```
productsCount           0
productsCount(active)   0
collectionsCount       15   ← every one of them contains 0 products
```

**There are no products in this store.** Not zero active — zero total. The three
HIVOLT polos and two sourcing drafts that existed at 08:41 on 2026-08-23 are
gone.

This is not a defect that can be closed by rebuilding a theme. The build spec's
own success criteria require products to exist:

| Spec requirement | Status with 0 products |
|---|---|
| §5 E6 — no URL may point to an empty collection | **All 15 collections are empty.** Every nav link is a defect |
| §7.5 "Featured collection — New In — points to a real, populated collection" | impossible |
| §7.6 "Collection list — one tile per real category" | every tile links to an empty page |
| §7.8 Bestsellers / Staff Picks | impossible |
| §8 `product.json` rebuilt with accordions from product metafields | no product to render |
| §8 `collection.json` with filters | nothing to filter |
| §9.4 "rewrite every product description… every product ≥3 images" | nothing to rewrite |
| §13 "Every collection referenced by a section has ≥1 product" | **fails on all 15** |

§3 forbids fabricated product data, so inventing products to fill the store is
not an available route. **The catalog must be restored or rebuilt before Phases
3–14 can run.**

---

## ⛔ BLOCKER B2 — The BRAND BLOCK was submitted unfilled

Every field in §0 arrived as its placeholder. §0 says "FILL THIS IN FIRST".

Most values were recoverable from the live store and are recorded in
`ASSUMPTIONS.md`. **One field is not recoverable and one is contradicted.**

### Contradiction: CATEGORY

The prompt specifies **"Women's apparel (global DTC)"** across `US, DE, UK, AU,
CA`. The live store is:

- **Men's golf polos** — every menu item, the two lead collections
  (`mens-golf-polos`, `long-sleeve-golf-polos`), the Size Guide page ("Size
  Guide — Men's Polos"), and the FAQ ("What HIVOLT sells: Men's golf polos").
- **US-only** — Shipping page and Terms both state "We ship within the United
  States only."

Building a global women's apparel store over this would orphan every existing
page, menu and collection — creating defects E8 and E14 wholesale rather than
closing them.

### Not recoverable: none

Legal entity, address, support channels, shipping and returns were all found in
the live store. See `ASSUMPTIONS.md`.

---

## Defect list

Products and their templates cannot be assessed at all — there are none. What
follows is everything assessable today.

| # | Code | Defect | Evidence |
|---|---|---|---|
| 1 | **E6** | All 15 collections contain 0 products | `productsCount.count == 0` on every collection |
| 2 | **E6** | `main-menu` — all 4 items resolve to empty collections or pages | `/collections/mens-golf-polos`, `/collections/long-sleeve-golf-polos` |
| 3 | **E6** | `footer`, `footer-shop`, `footer-about`, `footer-help`, `footer-legal`, `hivolt-draft-main`, `hivolt-draft-shop` — every Shop link lands on an empty collection | 8 menus audited |
| 4 | **E4** | `The Polo Collection` has `image: null` | collection query |
| 5 | **E4** | `The Championship Capsule` has `image: null` | collection query |
| 6 | **E14** | 13 of 15 collections are unreachable from any menu | menu vs collection diff |
| 7 | **E15** | Collection copy describes a catalog that does not exist — leggings, sports bras, dresses, denim, knitwear, coats, loungewear | e.g. `womens-activewear` describes "Sizes 2XS–2XL across the range" |
| 8 | **E13** | Shipping policy says "United States only" while `shipsToCountries` lists **71 countries** | shop query vs `/pages/shipping-delivery` |
| 9 | **E13** | Terms say HIVOLT sells "technical activewear and gym apparel"; every other surface says men's golf polos | `/pages/terms-of-service` |
| 10 | **E9** | `/pages/google-site-verification` — 1 line of body content, publicly published | page query |
| 11 | **E14** | 3 pages unpublished but still referenced in repo docs: `voltcore`, `fabric-weight-index`, `size-chart` | `isPublished: false` |
| 12 | **E14** | `size-chart` (unpublished) duplicates `size-guide` (published) | page list |
| 13 | **APP** | GemPages writes theme files — see `APP-CONFLICTS.md` | 5 files, timestamps after base install |
| 14 | **E12** | 7 locale pairs shipped (`de/es/fr/it/pt-BR/pt-PT`) with no evidence any are enabled markets | `locales/*` |
| 15 | **E1/E3** | Stock Impulse demo content in `settings_data.json`, `index.json`, `footer-group.json`, `header-group.json` — untouched since install | checksums match install time |
| 16 | **RISK** | `sections/testimonials.liquid`, `countdown.liquid`, `logo-list.liquid` present. §3 forbids populating these with fabricated content | theme files |

### Blog

`Training Journal` — **501 articles**. Not audited article-by-article; at 501
items that is its own pass. The §9.5 requirement to seed 3 articles is already
satisfied many times over.

---

## What is genuinely good and should be preserved

The content layer is strong and was clearly written to the same honesty standard
§3 demands. Do not overwrite it:

- `/pages/about-us` — "We publish the numbers. Including the ones that aren't flattering."
- `/pages/faq`, `/pages/size-guide`, `/pages/materials-sustainability`,
  `/pages/track-order`, `/pages/accessibility`
- `/pages/terms-of-service` — names a real LLC, real address, real phone
- `/pages/60-day-love-it-guarantee`, `/pages/returns-refunds`,
  `/pages/shipping-delivery`

Ten policy and help pages already exist with specific, non-generic content. §9's
main job is mostly done — except that they describe products the store no longer
has.

---

# Addendum — template-level defects (added 2026-08-24, Phase 2 pass)

The Phase 1 pass audited store data. This addendum audits the theme's own
template JSON, which turned out to carry the most serious defect in the build.

## 🔴 D-CRIT — Five fabricated customer testimonials, live on every product page

`templates/product.json` shipped a `testimonials` section **in its `order`
array** — not disabled, not a preset, active on every PDP:

| Author | Location | Rating |
|---|---|---|
| Leslie M. | Toronto, ON | 5 stars |
| Rachel F. | Los Angeles, CA | 5 stars |
| Sam R. | Brooklyn, NY | 5 stars |
| Sharon S. | New Orleans, LA | 5 stars |
| Matt C. | Montreal, QC | 5 stars |

Invented names, invented cities, invented quotes, fake star icons. This is a
direct breach of §3's first three prohibitions. **Removed.**

## Other template defects found and closed

| Code | File | Defect | Action |
|---|---|---|---|
| §3 | `product.json` | `sales_point-1` claims **"Organic cotton"** — unsubstantiated material claim, no supplier documentation | removed |
| E7 | `product.json` | `sales_point-2` text: `"Something something"` | removed |
| E7 | `product.json` | `tab-1`, `tab-2`: `<p>[connect via dynamic source]</p>` | removed |
| E7 | `product.json` | `tab-3`: `<p>[connect certification badges/images via dynamic source]</p>` | removed |
| E7 | `product.json` | `tab-4`: `<p>something something</p>` | removed |
| E7/E5 | `product.json` | `slideshow` — `top_subheading: "something something"`, `link_text: "Leads to sustainability page"`, `link: ""` | removed |
| E1 | `product.json` | `collection-return`, `sub`, `apps` all `disabled: true` | removed |
| E6 | `product.json` | `size_chart` pointed at page `size-chart`, which is **unpublished** | repointed to `size-guide` |
| §3 | `collection.json` | `promo-grid` banner: *"Save on Select Styles — take an extra 10% off sale items, limited time"* with `link: ""`. Fake urgency **and** a discount that does not exist | removed |
| §6 | `collection.json` | `parallax: true` on the collection header | set `false` |
| E3 | `collection.json` | `collection-header` `enable: false` — header suppressed | set `true` |
| E4/E6 | `404.json` | `featured-collection` "Popular picks" → every collection is empty | removed |
| E4/E6 | `cart.json` | same `featured-collection` | removed |
| §3/E4 | `settings_data.json` | All five social links pointed at **Shopify's own demo accounts** (`facebook.com/shopify`, `instagram.com/shopify`, `tiktok.com/@shopify`, `pinterest.com/shopify`, `youtube.com/user/shopify`) | all 10 social fields emptied |
| E4 | `settings_data.json` | `favicon: ""`, no logo set | both set to the real brand marks |

## Still open — `templates/index.json` (Phase 3, blocked on products)

Left untouched because the homepage rebuild waits on the catalog. Every one of
these is a defect:

- `shoppable-hero` — 3 hotspots bound to products `the-riva-tank`,
  `the-lena-midi`, `the-cami`. **None exist.** `image: ""`, `button_link: ""`.
- `featured-collections` — 4 tiles → `2026-tops`, `2026-bottoms`,
  `2026-dresses`, `2026-layers`. **None of those collections exist.**
- `featured-collection` → `2026-new`; `featured-collection-2` →
  `2026-the-linen-edit`. Neither exists.
- `hero-video` — a **YouTube demo video** (`kAaV5gfdsG0`), `link: ""`.
- `promo-grid` — 2 blocks, both `image: ""`, both CTAs labelled but unlinked.
- `slideshow` — `image: ""`, `link: ""`, `parallax: true` (breaches §6),
  `autoplay: true`.
- `image-grid` — **7 blocks**, several `image: ""`, all `link: ""`.
- `text-with-icons` — `button_label: "boop"`.
- `text-and-image` — `image: ""`, `image2: ""`, `title: ""`, `button_link: ""`.

## Section-removal ruling — closed

`testimonials`, `countdown`, `logo-list` across all 7 JSON templates:

| Template | Contained any of the three? |
|---|---|
| `product.json` | **yes — `testimonials`. Removed.** |
| `index.json` | no |
| `collection.json` | no |
| `404.json`, `cart.json`, `search.json`, `page.json` | no |

The three `.liquid` section files remain on disk but are now referenced by **no
template**, so they cannot render. Deleting the files themselves is deferred —
Impulse's theme editor lists them as available presets, and removing section
files from a theme that the editor may re-add is a separate, riskier change.
