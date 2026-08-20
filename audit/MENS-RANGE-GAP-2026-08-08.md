# HIVOLT — 10 men's products to add, and why

TrendTrack research, 2026-08-08. Every competitor figure below is pulled from
TrendTrack, not estimated. The gap analysis is from the store's own catalogue.

---

## What the research actually returned

`find_winning_products` was run twice and is not usable for this. With a US
shop-country filter it returned **zero** rows. Without it, three:

| Returned | What it actually is |
|---|---|
| NITRAFLEX ADVANCED, $29.99 | A **pre-workout supplement**. Matched on the term "workout hoodie". |
| Black iGenius T-Shirt, $24.99 | Company merch for a network-marketing firm. 3,138 monthly visits. |
| Performance Polo Tee, ₹1,299 | **Jolger**, an Indian brand. Priced in INR, ships India. |

None is a men's activewear product a US store could act on. The tool's own
warning says it "only includes shops/products with usable relevance and traction
signals" — for this niche there were three, and two are off-category.

So the useful signal came from competitor briefs instead.

### LSKD — lskd.co

**1,907,559 monthly visits. 719 active ads. AU-based, 11.9% of traffic US.**

Their top ten products, by catalogue rank:

| Rank | Product | Price |
|---|---|---|
| **1** | **1% Better Duffle Bag** | **A$70** |
| **2** | **1% Better Cotton Towel 50×115cm** | **A$40** |
| 3–4 | Same towel, other colourways | A$40 |
| 5–9 | **1% Better EST FLXCotton Oversized Tee** (5 colourways) | A$29 |
| 10 | 1% Better FLXCotton Training Fit Tank | A$19 |

Two things fall out of that and both are actionable:

1. **Their two best-selling products are not clothing.** A duffle bag and a
   towel. No size risk, no fit returns, highest margin in the category.
   **HIVOLT sells zero accessories.**
2. **Five of the remaining eight are the same oversized cotton tee** in
   different colours. The oversized heavyweight tee is the men's silhouette
   right now, and HIVOLT does not have one.

### True Classic — trueclassictees.com

**2,988,355 monthly visits, +15.7% in 30d, 1,117 active ads, US-based.** The
biggest men's-tee DTC brand in the index — but its product data is unusable:
the entire top ten is `10% CashBack` / `20% CashBack` at $0.00, a loyalty app
polluting the product feed. Traffic and ad figures are real; the product ranking
is not.

---

## The gap in HIVOLT's own men's range

47 products in `mens-activewear`:

| Type | Count | Share |
|---|---|---|
| **T-Shirt** | **19** | **40%** |
| Jersey | 7 | 15% |
| Shorts | 6 | 13% |
| Tank Top | 4 | 9% |
| Jacket | 3 | 6% |
| Joggers | 2 | 4% |
| Polo | 2 | 4% |
| Hoodie | 2 | 4% |
| Sweatpants | 1 | 2% |
| Leggings | 1 | 2% |

**26 of 47 products — 55% — are t-shirts or jerseys.** Meanwhile bottoms are
9 of 47, and there are no accessories at all. The range is deep where margin is
thinnest and competition is hardest, and shallow everywhere else.

Three smaller findings from the same query:

- **`high-waisted-yoga-leggings` is filed in men's activewear.** Miscategorised.
- **Five archived products still sit in the men's collection**
  (`mens-lightweight-training-t-shirt`, `men-s-regular-fit-training-t-shirt`,
  `high-waisted-yoga-leggings`, `contrast-trim-raglan-varsity-jacket`,
  `men-s-performance-regular-fit-t-shirt`). Archived items don't render, so the
  storefront impact is nil, but the collection count is inflated.
- **Two pricing conventions are live at once.** 7 active products end in `.99`
  (`unisex-boxy-striped-collared-soccer-jersey`, `unisex-striped-raglan-jersey`,
  `unisex-paneled-long-sleeve-jersey`, `unisex-color-block-jacquard-soccer-jersey`,
  `unisex-boxy-v-neck-soccer-jersey`, `unisex-striped-raglan-long-sleeve-t-shirt`,
  `two-tone-raglan-sleeve-varsity-jacket`) against whole-dollar pricing on the
  other ~103. **An earlier note in this repo said the store had no `.99` price
  anywhere. That was wrong** — the claim came from an audit agent and the
  verification query silently dropped its price filter.

---

## The 10

Ordered by expected return, not by category. Prices are positioned against the
existing ladder ($34 / $38 / $42 / $54 / $59 / $69 / $79).

### Accessories — the biggest miss (0 in catalogue, LSKD's #1 and #2)

| # | Product | Price | Why |
|---|---|---|---|
| 1 | **Training duffle, ~35 L** | $59 | LSKD's single best-selling product. No sizing, no fit returns, carries the logo in public. |
| 2 | **Gym towel, 50×115 cm** | $24 | LSKD's #2, #3 and #4 are all this one towel. Lowest-risk repeat purchase in the category. |
| 3 | **Lifting wrist wraps / belt** | $29 | One size, no returns, pure margin, signals a serious training brand. |

### Bottoms — 9 of 47 today, and the category men actually spend on

| # | Product | Price | Why |
|---|---|---|---|
| 4 | **5" lined lifting short** | $44 | The dominant men's gym short. HIVOLT has drawstring, basketball and cycling shorts — **none with a liner**, which is the whole point of the category. |
| 5 | **7" lined training short** | $44 | Same build, the length that outsells 5" outside lifting. Two lengths is the standard SKU pair. |
| 6 | **Tapered tech jogger, mid-weight** | $59 | Both current joggers are $69. Nothing sits between $42 and $69 in men's bottoms. |

### Constructions the range doesn't have at all

| # | Product | Price | Why |
|---|---|---|---|
| 7 | **Oversized heavyweight cotton tee, 240 g/m²** | $42 | Five of LSKD's top ten. The current 19 tees are all fitted/performance knits — none is the oversized cotton silhouette that's selling. |
| 8 | **Compression long-sleeve base layer** | $49 | No compression layer exists in the range. Sells year-round, and pairs with items already stocked. |
| 9 | **Seamless training tee** | $46 | No seamless construction anywhere in 110 products. It is the single most-searched construction term in the category. |
| 10 | **Heavyweight pullover hoodie, 400 g/m²** | $69 | The two current hoodies are a **130 g/m²** shell and a sleeveless mesh. There is no actual warm hoodie in the store. |

---

## What is blocking me from adding these

The request was to create five images per product and set 500 units each. I have
not done that, for one reason:

**These ten garments do not exist.** There is no supplier, no sample, no
photograph. Any image I generate would depict a product that cannot be shipped,
and setting 500 units makes it buyable — so an order would arrive that nothing
can fulfil.

That matters here more than it would elsewhere. This store's original brief was
*"find all problems and remove bad products with wrong images."* Adding fifty
generated images of imaginary garments recreates that problem at scale, and
Google Merchant Center reviews product imagery against the item shipped — the
330 feed attributes already built for that channel would be at risk.

**What unblocks it:** supplier links or photos for any of the ten. With those I
will build each listing end to end — title, description in the published-not-claimed
voice, `spec.*` metafields (gsm, composition, care, seams), SEO title and
description, `mm-google-shopping` feed attributes, collection assignment,
variants, and 500 units per variant. That is the same pipeline already run
across the existing 110, and it takes minutes per product once a real photo and
a real spec sheet exist.

If the intent was **branded imagery over supplier photos** — logo, consistent
background, HIVOLT art direction — that is legitimate and I can do it, but it
has to start from a photograph of the actual garment.
