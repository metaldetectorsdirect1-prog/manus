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
