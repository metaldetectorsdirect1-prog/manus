# The eBay upload file, and what the tooling search actually found

2026-08-13.

## The research finding first, because it is not what was expected

The brief was to add every skill and repo that would help start getting sales.
The honest answer is that **almost nothing needed adding**.

* `SuggestSkills`, queried for eBay listing, Amazon seller, marketplace
  selling, product feed, ecommerce sales and Shopify, returned **zero
  results**. There is nothing available to install that this account does not
  already have.
* Roughly **sixty marketing skills are already installed and unused** —
  `mk-product-feed-optimizer`, `mk-conversion-ops`, `mk-cro`, `mk-offers`,
  `mk-pricing`, `mk-programmatic-seo`, `mk-directory-submissions`, the whole
  `seo-*` and `geo-*` families, `gsc-*` for Search Console, and eight `tt-*`
  TikTok skills.
* The repository search returned Shopify **export** tools — `shopify-bulk-export`,
  `shopify-product-export-to-csv`, `bulkyOps`. All three do what
  `bulkOperationRunQuery` already does here, which is how every dataset in this
  audit was produced. Adding them buys nothing.

So the constraint was never tool access. Everything still blocking a sale is
either a credential this container does not hold, or a fact only eBay can
supply. What was genuinely missing was a file eBay will actually accept, and
that is what got built.

## What the format research changed

`marketplace-export.py` produced a generic CSV. It would have been rejected.

* **File Exchange is being retired** in favour of **Seller Hub → Reports**,
  same CSV dialect, different home.
* The **`*Action` column must be first** and carries the site header
  `*Action(SiteID=US|Country=US|Currency=USD|Version=1193|CC=UTF-8)`.
* **`C:`-prefixed columns** are the category's Item Specifics.
* Every row needs a **leaf category id**.

### Variations, which is the commercially significant part

The generic export listed 541 variants as 541 rows. As 541 separate eBay
listings that would exceed the free insertion allowance immediately and fill
the store with near-duplicates competing against each other.

eBay's multi-variation format collapses them to **one listing per garment**:

    parent row     Relationship empty, RelationshipDetails "Size=S;M;L|Color=Black",
                   StartPrice and Quantity empty
    variation row  Relationship "Variation", RelationshipDetails "Size=M|Color=Black",
                   its own StartPrice and Quantity, and title/description/pictures
                   left blank so eBay does not treat the row as its own listing

113 garments instead of 541 listings. A garment with a single variant is
emitted flat, because a one-value variation matrix is rejected.

## Three things eBay removes listings for, handled before upload

1. **Links to an off-eBay store.** Three descriptions link to
   `/pages/fabric-weight-index`. Anchors are unwrapped to their text rather
   than deleted wholesale, so the sentence survives: *"It is listed as
   publishing no g/m² in our Fabric Weight Index, alongside every figure we
   can stand behind."* All three were read before and after to confirm nothing
   dangles.
2. **Contact details in the body.** Zero descriptions carry an email, checked
   rather than assumed.
3. **Titles over 80 characters.** None of the 113 exceed it. Over-length
   titles are reported, never silently truncated.

A first pass flagged **80 "dangling fragments"**. Reading them, every one was
ordinary prose — *"on our"*, *"at"*, *"see"* before punctuation. The heuristic
was noise, the same false-positive trap as the "96 of 113 superlatives" figure
that turned out to be 17. The real number is **3 links and 0 emails**.

## The category ids

eBay needs a **leaf** category id per listing. There is no derivation from a
Shopify product type, and a wrong id either rejects the row or files the
garment where no buyer looks.

The first pass verified two and left 24 pairs null, which put 99 of 113
products behind a manual lookup. That was friction I had created, so the
remaining ids were researched rather than left to the owner. **Thirteen are now
verified**, each read off an eBay browse URL of the form
`ebay.com/b/<name>/<ID>/`:

| id | category | covers |
|---|---|---|
| 185076 | Men's Activewear Tops | mens + unisex tees, tanks, 3 generic jerseys |
| 59315 | Women's Sports Bras | 17 products, the largest single bucket |
| 185082 | Women's Activewear Tops | women's tanks and tees |
| 169001 | Activewear Leggings for Women | leggings |
| 260954 / 260955 / 260957 | Women's Pants / Women's Shorts / Men's Shorts | |
| 155226 | Activewear Hoodies & Sweatshirts for Women | |
| 123490 | Men's Soccer Clothing, jerseys | the 4 soccer jerseys |
| 261046 | Women's Activewear Skirts & Skorts | |
| 260956 | Men's Activewear Pants | joggers, sweatpants |
| 185079 | Women's Activewear Jackets | |
| 185708 | Men's Tracksuits & Sets | |

### A correction to my own file

The first version recorded **185082 as a browse parent not to be listed into**.
That was wrong. `/b/Womens-Activewear-Tops/185082/` and
`/b/Active-Athletic-Apparel-for-Women/185082/` are **the same category** —
eBay serves many marketing names off one node, and a different display name is
not a different id. 185082 is the leaf for Women's Activewear Tops and is now
used. `185098` and `185099` do look like true parents and are still avoided.

### Two ids deliberately not used

**2887** — International Club Soccer **Fan** Jerseys. HIVOLT's jerseys are
unbranded blanks. Listing them there puts them in front of people shopping for
a team, which is the wrong audience and arguably a misrepresentation.

### Where the key was not good enough

`unisex:Jersey` covers **two different garments**: four are explicitly soccer
jerseys and belong in Men's Soccer Clothing, three are generic long-sleeve
training jerseys and do not. One id for the pair would have mis-filed three,
so the config gained **per-handle overrides** that win over the
`(gender, productType)` map, rather than stretching one key over both.

`men-s-lightweight-sport-jersey` looked like an eighth jersey and is not —
it is typed **T-Shirt**, so it routes to Men's Activewear Tops correctly. The
handle contains "jersey"; the product type is what decides.

**Seven pairs remain null, covering 12 of 113 products**: women's sets,
rompers, bodysuit and dress, and unisex hoodies, jackets and the polo. They are
not guessed. The script still refuses to emit a row for them — the same
abort-rather-than-mangle rule as `article-spec-fix.py`.

## What it produces today

    101 listings / 588 rows -> ebay-seller-hub-upload.csv

Verified on the output, not inferred: `*Action` is the first column, all **101
parents** carry the matrix with empty price and quantity, all **487 variation
rows** carry a price, 0 descriptions contain a URL, an email or an `<a>` tag,
0 titles exceed 80 characters, 0 parents are missing a category, a picture or a
Department, and all 113 active products have at least one image for `PicURL`.

Terms are set to match what the store already publishes rather than eBay's
defaults: free shipping, `ShippingCostPaidByOption: Seller` because the refund
policy provides the return label, `Days_60`, and condition 1000 — new with
tags, which is the same claim the returns page makes.

**Quantity is 25 per variation, not the 1,000 the store carries.** A new eBay
seller account has a selling limit and 1,000 units on day one would breach it.

## What this does not do

It does not upload. That needs the owner's seller account, and generating a
file is not a sale. It also does not touch Amazon — 541 of 541 variants still
carry a null barcode and Amazon apparel requires a GTIN per variant.
