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

## The category ids, and why 24 are blank

eBay needs a **leaf** category id per listing. There is no derivation from a
Shopify product type, and a wrong id either rejects the row or files the
garment where no buyer looks.

Verified from eBay's own browse URLs, so used:

| id | category | mapped from |
|---|---|---|
| 169001 | Activewear Leggings for Women | `womens:Leggings` |
| 260954 | Women's Activewear Pants | `womens:Yoga Pants`, `womens:Pants` |

`185082` (Active Athletic Apparel for Women) and `185098` (Women's Activewear)
also turned up, but they are **browse parents, not leaves**, so listing into
them would fail. Recorded in the config as a warning rather than used.

The other **24 pairs are null**, covering 99 of 113 products. They are not
guessed. `scripts/ebay-listings.py` refuses to emit a row whose category is
still null and prints exactly which pairs need one — the same abort-rather-
than-mangle rule as `article-spec-fix.py`.

Filling them is about fifteen minutes in eBay's category picker: the id is the
number in the resulting `ebay.com/b/<name>/<ID>/` URL.

## What it produces today

    14 listings / 78 rows -> ebay-seller-hub-upload.csv

Verified on the output, not inferred: `*Action` is the first column, 14 parents
carry the matrix with empty price and quantity, 64 variation rows each carry a
price, 0 descriptions contain a URL, an email or an `<a>` tag, 0 titles exceed
80 characters, and all 113 active products have at least one image for `PicURL`.

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
