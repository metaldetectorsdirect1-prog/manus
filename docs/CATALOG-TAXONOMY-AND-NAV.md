# CATALOG-TAXONOMY-AND-NAV.md — 2026-08-29

Store state at time of work: **2,279 products, 2,031 ACTIVE**, 0 orders
all time. The catalogue was being written by a second automated process
throughout this session (439 → 939 → 879 → 2,279 products observed in
one sitting), so everything below is rule-based rather than
product-by-product — automated collections keep working as products are
added; manual assignment would have been stale within the hour.

## Category architecture (verified live)

A 45-collection architecture already existed. It is sound. Verified
counts after this pass:

| Women | Count | Men | Count |
|---|---:|---|---:|
| Women (top) | 1,079 | Men (top) | 1,173 |
| Coats & Jackets | 157 | Jackets & Coats | 170 |
| Knitwear & Sweaters | 154 | Knitwear | 130 |
| Dresses | 171 | Shirts | 120 |
| Tops & Blouses | 52 | T-Shirts & Polos | 100 |
| Jeans & Bottoms | 120 | Hoodies & Joggers | 100 |
| Boots & Shoes | 126 | Pants & Jeans | 130 |
| Loungewear & Sleep | 58 | Shoes & Boots | 100 |
| Bags & Accessories | 100 | Tailoring | 70 |
| | | Jewelry & Accessories | 90 |

Gender separation is clean: men's products carry `men` plus `m3-*`
category tags; women's carry the plain category tags (`knitwear`,
`knitwear-2`, `w3-knitwear`, …). The two sets do not overlap.

**Note for anyone auditing this later:** Shopify's `tag:` *search* is
fuzzy — `tag:knitwear` also matches `m3-knitwear` and `knitwear-2`.
Collection *rules* use exact matching. A search-based leak check will
show a men/women overlap that does not exist in the collections. This
was verified by reading raw tag arrays on individual products.

## Changes made this pass

| Change | Reason |
|---|---|
| "Best Sellers" (2,037 products) → renamed **"Shop All"** | The store has **zero orders**. Calling 2,037 products best sellers was an unsupported claim on a live storefront. |
| 17 collections published to Online Store | They were unpublished; every new navigation link would have 404'd. |
| Navigation rebuilt (`fashion-main`) | The live header linked to **no collections at all** — 2,031 live products with no way to browse to any of them. |
| "Size Guide — Women" and "Size Guide — Men" published | Both already written, accurate and honest. They were sitting unpublished while the store sold both menswear and womenswear. |
| `/pages/size-guide` rewritten as a hub | Now routes to the two real guides instead of a placeholder. |
| "The Polo Collection" and "The Championship Capsule" deleted | Empty golf-era collections with golf handles on a fashion store. |
| Blog "Training Journal" → **"The HIVOLT Journal"** | Activewear-era name on a womenswear/menswear store. |
| "Women's Activewear" rule repaired | Rule referenced a tag (`womens`) that does not exist — collection was permanently empty. |

## Navigation now live

```
New In · Women ▾ (8) · Men ▾ (9) · Journal · About · Help ▾ (7)
```

All 20 linked collections verified published with non-zero counts.

## Known quality problems in the catalogue (not fixed here)

Flagged by the generating process's own tags:

| Tag | Count | Meaning |
|---|---:|---|
| `color-unverified` | 304+ | Colour in the title may not match the image |
| `no-match-found` | 51 | No supplier match was found |
| `bad-image-mismatch` | 11 | Image does not match the product |
| `image-collage` | 11 | Lead image is a collage |

Plus, from the earlier economics pass: four different coats share one
Amazon ASIN at a $2.99 cost, and a large share of the catalogue is
sourced `src-amazon-*` (Amazon retail is not a permitted dropship
fulfilment source). **2,024 of the 2,031 active products carry 1,000
units of tracked inventory that nobody owns.**

These are the blockers on a premium storefront, and none of them is a
design problem.

---

# Update — 2026-08-29, second pass

## The r2 publish was abandoned, deliberately

Plan going in was "publish MASTER r2 to fix the defective homepage image."
A fresh role query killed that plan:

| Theme | Role |
|---|---|
| **HIVOLT — Nova Rebuild (Claude)** (`158888526056`) | **MAIN** — published 11:07 today |
| GENERAL STORE — IMPULSE MASTER CANDIDATE (`158753849576`) | UNPUBLISHED |
| GENERAL STORE — MASTER r2 (`158874960104`) | UNPUBLISHED, checksum still `1ec45ae6…` |
| Horizon (`158882693352`) | UNPUBLISHED |

r2 was built as a corrected twin of the old MASTER CANDIDATE. That base is
no longer live. **Publishing r2 would have replaced a newer, better theme
with 14-hour-old work and destroyed the Nova build.** r2 is now obsolete;
the defective category tile it was created to fix does not exist in the
Nova homepage at all.

Nova's homepage is a genuine editorial build: hero "The Winter Edit",
category edit, New This Week, dress editorial, knitwear edit, brand
story, explore grid, service icons, newsletter — plus a `hivolt-schema`
section in the header group, so structured data survived the cutover.

## The real defect found instead

Nova's header uses menu **`nova-main`**, not the `fashion-main` rebuilt
in the previous pass. `nova-main` was:

```
New In · Dresses · Matching Sets · Denim · Knitwear · Coats & Jackets · Formal · Help
```

**No Men's entry anywhere** — while the store carries 1,173 men's
products. Rebuilt as:

```
New In · Women ▾(9) · Men ▾(10) · Accessories ▾(3) · The Edit ▾(3) · Journal · Help ▾(7)
```

`Men's Activewear` was also unpublished and would have 404'd; published.

## Curation performed

| Action | Count | Reason |
|---|---:|---|
| Set to DRAFT | **8** | All eight share Amazon ASIN `B081YTSN4N` at a $2.99 cost while priced $79.95–$109.95. A military wool coat, a faux-leather trench, an anorak and a parka cannot be one $2.99 item — the supplier mapping is fabricated, so neither the cost nor the fulfilment source is real. |
| Set to DRAFT | **42** | `image-collage` — lead image is a collage, which fails the image standard for a premium storefront. |

Live products: 1,967 → **1,884**. Fabricated-ASIN products live: **0**.

## Still outstanding

**892 active products carry `color-unverified`** — the colour named in
the title ("…in Camel", "…in Slate Blue") was never confirmed against the
image. That is roughly **47% of the live catalogue** making a specific
colour claim that may be wrong. It is the largest remaining
misrepresentation exposure and the most likely driver of returns.

Two ways to clear it, both bulk operations on ~892 products:
1. Strip the colour phrase from the titles — keeps them sellable, removes
   the unverified claim.
2. Verify colour against the lead image and keep only what matches.

Neither was done unilaterally: it rewrites nearly half the live catalogue,
and the generating process is still actively writing products (8 new
`image-collage` items appeared during this pass alone).

Also unchanged: 1,884 active products still carry 1,000 units of tracked
inventory each.
