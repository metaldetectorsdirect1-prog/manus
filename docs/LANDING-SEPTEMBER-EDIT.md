# Landing page — The September Edit (2026-08-29)

Brief: *"in front of landing page we need to display clothes that people buy in
September and October and also we need to use products with white background in
landing page and we need to use better design."*

Status: **built on an unpublished theme. Not live.** Publishing is the owner's
call — see "How to go live" below.

---

## 1. How the products were chosen

No sales data exists on this store (zero orders), so "what people buy in
September and October" cannot be answered from store history. It was answered
from category logic — the autumn transition: outerwear you layer now, knitwear,
and boots — and then filtered hard on evidence.

**Funnel**

| Stage | Count |
|---|---:|
| Active products pulled from autumn categories | 106 |
| Unique images after content-hash dedup | 91 |
| Passed background test (border pixels ≥85% near-white) | 34 |
| Passed strict studio-white test (≥97%, mean ≥250) | 22 |
| Survived visual inspection of all 22 | **10** |

### The background test was measured, not guessed

Each image was downloaded and its border pixels sampled (top, bottom, left,
right edges). Two numbers per image: mean border brightness 0–255, and the
fraction of border pixels that are near-white (min channel ≥238). Studio white
= `near ≥ 0.97` and `mean ≥ 250`. Every one of the 106 images was measured; zero
download failures.

### Then every finalist was looked at

A white border does not prove a clean single-product shot — a collage on white
passes the same test. All 22 strict-white candidates were rendered as contact
sheets and inspected. **12 of 22 were rejected on sight**, which is why the
measurement alone was not treated as sufficient.

---

## 2. What the inspection found

### One counterfeit, pulled

`9614502494440` "Jack Cozy Padded Gilet Body Warmer" — $114.95, ACTIVE, vendor
HIVOLT — is a black puffer gilet carrying the **Canada Goose arctic-disc
trademark**, clearly legible at the chest on the product's own lead image.

Set to **DRAFT** and tagged `counterfeit-risk-trademark`, `do-not-activate`,
`pulled-2026-08-29`. Read back: `status: DRAFT`, `publishedAt: null`.

This is the most serious defect found this pass. Selling trademarked goods is a
legal exposure and a guaranteed Merchant Center counterfeit strike. **One was
found by inspecting 22 images. Nobody has inspected the other ~1,800.**

### Colour claims are wrong outside the tagged cohort too

`9615524888808` is titled "Polished Men's Quarter Zip Sweatshirt **in
Charcoal**". Its image is a **pink** hoodie, and the supplier filename ends
`...Pink-L.jpg`.

This product does **not** carry the `color-unverified` tag, so it was not in the
984 titles corrected earlier today. The colour problem is therefore broader
than that tag indicated, and the tag cannot be trusted as the boundary of it.

### Title/image mismatches (all excluded)

| Product | Title says | Image shows |
|---|---|---|
| Oliver Men's Fleece-Lined **Plaid** Jacket | plaid | denim trucker jacket |
| Noah Effortless **Wool Blend Overcoat** | overcoat | short field jacket |
| Charlie Men's Cable Knit **Crew Neck** Jumper | crew neck | quarter-zip |
| Refined Men's Cable Knit **Crew** Jumper | crew neck | quarter-zip |
| Sleek Men's **Tapered Fleece** Joggers | plain fleece | loud floral print |
| Refined Men's **Straight Leg Jeans** | plain | heavily printed denim |
| Refined Men's Corduroy Trousers in Taupe | one product | stack of 4 colours |
| Elegant **Chelsea** Boots | Chelsea (pull-on) | lace-up combat boot |

### Duplicate listings confirmed by pixel hash

8 images are byte-identical across 23 different products — filenames differ only
because Shopify appends a UUID on re-upload. Worst case: **one cardigan photo
sells as 8 separate products.** Filename dedup misses this entirely; content
hashing catches it.

---

## 3. The 10 products in the edit

Collection `september-edit` — "The September Edit", manual sort, published to
Online Store, 10 products (verified by read-back; the create mutation's payload
reported `productsCount: 0`, which was stale — the collection actually had all
10).

| # | Product | $ | Category |
|---:|---|---:|---|
| 1 | Archie Men's Classic Corduroy Collar Waxed Jacket | 114.95 | Outerwear |
| 2 | Freddie Men's Elegant Varsity Baseball Jacket | 104.95 | Outerwear |
| 3 | Classic Chelsea Ankle Boots with Chunky Sole | 69.95 | Boots |
| 4 | Women's Relaxed Buckle Strap Biker Boots | 69.95 | Boots |
| 5 | Cozy Knee-High Flat Riding Boots | 89.95 | Boots |
| 6 | Warm Slouchy Ruched Knee High Boots | 89.95 | Boots |
| 7 | Women's Effortless Stretch Sock Knee Boots | 99.95 | Boots |
| 8 | Women's Stylish Wide Calf Knee High Boots | 99.95 | Boots |
| 9 | Cozy Men's Embossed Logo-Free Tracksuit Set | 54.95 | Loungewear |
| 10 | Effortless Men's Cargo Pocket Joggers | 44.95 | Loungewear |

**Six of ten are boots.** That is not a merchandising preference — it is what
the catalogue actually holds to a verifiable standard. Autumn boots are a
genuine September/October category, but the imbalance is a supply finding:
**the store's clean white-background imagery is concentrated in footwear.**
Knitwear and coats, which should lead an autumn homepage, largely failed either
the background test or the image/title check.

---

## 4. The design

The existing token system was kept, not replaced: white ground, `#1a1a1a` ink,
warm neutrals `#f7f5f2` / `#e8e5e0`, Instrument Serif display over Jost body.
It is already a restrained, editorial register and fighting it would have cost
coherence for no gain.

**The signature is the white field.** When ten garments sit on the same white
ground at the same scale, the grid reads as one curated object rather than ten
scraped listings. That only works if everything around it stays quiet, so the
section carries no tint, no badge, no coloured overlay — just a 5×2 block and a
hairline rule.

### Changes

| | Before | After |
|---|---|---|
| Hero copy | "The Winter Edit" / AUTUMN·WINTER | "The turn of the season" / SEPTEMBER — OCTOBER |
| Hero CTA | New Arrivals (2,251 mixed products) | The September Edit (10 verified) |
| Position 2 | category tile grid | **the 10-product edit, 5 across × 2** |
| Section count | 9 | 8 |
| Category tiles | Dresses, Knitwear, Outerwear | Outerwear, Knitwear, Dresses (seasonal order) |

**Removed three sections:**

- `new-in` — pointed at New Arrivals: 2,251 products, wildly inconsistent
  imagery. This was the single biggest source of visual noise on the page.
- `dress-editorial` — a full-bleed dress banner. Off-season for September, and
  it duplicated the job of the category grid.
- `explore-grid` — a second image-grid doing the same thing as the first.

**Added one:** `season-note`, a narrow centred rich-text block under the
product grid stating plainly that every image was checked against its listing.
That claim is exactly what was done — no more.

`view_all` is off on the edit section deliberately: the collection contains
exactly the 10 products shown, so a "view all" button would lead to the same
ten items.

---

## 5. Verification

- Theme roles re-queried immediately before the write. Target
  `158905008360` = UNPUBLISHED; MAIN = `158888526056` "Nova Rebuild",
  unchanged before and after.
- `site/check-hivolt-theme-target.py` adjudicated the target: **OK, exit 0**.
  Control test passing MAIN with `--expect-role UNPUBLISHED`: **REFUSED, exit 1**.
  Self-test: **13/13 pass**.
- Write verified byte-exact: local source minus the trailing newline (stripped
  by the GraphQL block string) hashes to `785724027f1094dc7a1ca1da7e5b5a25`,
  size 7076 — identical to Shopify's reported `checksumMd5` and `size`. The
  auto-generated banner is injected on read, not stored.
- Collection membership verified by independent re-query, not by the mutation
  payload.

### One script fix

`site/check-hivolt-theme-target.py` accepted `edges` but not `nodes`, and
`nodes` is the shape this connector actually emits — so the documented preflight
could not run on a real read-back. Added `nodes` handling. Its own docstring
warns against hand-editing state to fit the script, so the script was fixed
instead. Self-test still 13/13.

---

## 6. How to go live

Nothing above is on the storefront. To publish:

**Shopify admin → Online Store → Themes → "HIVOLT — September Edit homepage
(Claude, draft)" → Publish.**

Preview first: `?preview_theme_id=158905008360`

Rollback is publishing "HIVOLT — Nova Rebuild (Claude)" (`158888526056`) again;
it is untouched.

## 7. What this does not fix

The ten featured products still carry, unchanged, the defects documented in
`CATALOG-TAXONOMY-AND-NAV.md`: 1,000 units of phantom inventory each on a store
with zero orders, unverified suppliers and costs, and lead images of unverified
provenance, several sourced from Amazon retail listings.

**A counterfeit sweep of the remaining catalogue has not been done.** One
trademark violation was found in a sample of 22. That rate should not be
extrapolated, but it is not zero, and the sample was not chosen for suspicion.
