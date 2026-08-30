# Merchant Center feed readiness — 2026-08-10

Merchant Center account **5705286743** now exists. This pass audited all 113
active products against Google's Apparel & Accessories requirements for US
targeting and fixed what Shopify controls.

## The blocker sits above all of it

**Shopify has no Google & YouTube sales channel.** Publications are: Online
Store, Point of Sale, Manus, Shop, Facebook & Instagram, AfterShip for TikTok.
No Google.

So account 5705286743 currently has **no feed source**. Everything below makes
the data correct for the moment a feed exists; none of it puts a product in
front of a shopper on its own. Installing the channel is a two-minute job in
Shopify admin and it is the only step that turns this work into listings.

## What was already right

Worth stating, because it is most of the requirement and it was not obvious:

| Attribute | Source | State |
|---|---|---|
| `brand` | product `vendor` | HIVOLT on all 113 |
| `google_product_category` | Shopify taxonomy `category` | leaf node on all 113 |
| `color` / `size` | variant options | present on all non-set products |
| `gender`, `age_group` | `mm-google-shopping` metafields | present on 109 |
| `identifier_exists` | `custom_product: TRUE` | correct — private label with no manufacturer GTIN |
| image | featured media | 1400×1400, well above the 250 px apparel floor |

Every variant has `barcode: null`, which is fine and not an oversight: HIVOLT
is a private label, no manufacturer GTIN exists, and `custom_product: TRUE` is
exactly how Google is told so. SKUs carry through as `mpn`.

## Fixed — the sets, which were the whole problem

The four multi-piece sets are the store's highest-priced SKUs and every one of
them would have been **disapproved on submission**.

- **Three sets carried no `gender` and no `age_group` at all.** Both are
  required for Apparel in the US. `womens-training-set-bra-ankle-leggings`,
  `womens-yoga-set-halter-bra-yoga-pants` and `mens-training-set-tee-shorts`
  had an empty `mm-google-shopping` namespace. Set to female/female/male,
  all adult, all `custom_product: TRUE`.
- **All four sets had no Color option at all** — only Size. `color` is required
  for Apparel. Added as a single value, Black, verified against each product's
  own description and image alt text ("Matte black", "…in Black — HIVOLT").
  `productOptionsCreate` with `variantStrategy: LEAVE_AS_IS` added the option
  without multiplying variants: 4 in, 4 out.
- **Three sets sat on `> Clothing > Activewear`**, a branch node rather than a
  leaf. Moved to `Apparel & Accessories > Clothing > Outfit Sets` (`aa-1-11`),
  matching the one set that was already there.

## Fixed — a price claim that would have failed policy

`womens-training-set-bra-ankle-leggings` priced at **$79 against a $97
compare-at**, which is correct: cropped bra $38 + ankle leggings $59. But the
page body said *"Bought separately these are $92"* and the meta description
said *"Save $13"*.

$92 is the pre-ladder number — it is the legging at its old $54, before the
weight ladder moved the 230 g/m² pair to $59. **This is the third place that
same stale figure has surfaced**, after the `sets` film and the collection copy.

It matters more here than anywhere else. Google cross-checks the landing page
against the feed; a page claiming $92 behind a feed carrying $97 is the
"mismatched value (price)" disapproval, and a stated saving that does not match
the prices charged is a promotions violation regardless of which way it errs.
Corrected to $97 and "Save $18".

The other three sets check out exactly: yoga $49+$54 = $103, men's $34+$42 =
$76, Voltcore $38+$54 = $92.

**Voltcore had no `compareAtPrice` at all**, so its stated $13 saving had
nothing structured behind it — which is why the earlier SEO pass stripped that
claim from its meta description rather than let it stand. The right fix was the
other direction: set `compareAtPrice: 92.00`, matching the sum its own
description states and the convention the other three sets already follow. The
saving is now real, visible, and verifiable.

## Fixed — colour format on 13 products

Google reads multi-colour values as `Primary/Secondary`, separated by `/`, up
to three. Thirteen products used prose instead:

`White with Green` → `White/Green`, `Black with White` → `Black/White`,
`Black with Apricot` → `Black/Apricot`, `White with Blue` → `White/Blue`,
`White with Black` → `White/Black`, `Black with Red` → `Black/Red`.

Not a disapproval — a free-text colour is accepted — but "Black with White"
does not decompose into two filterable colours, so the item drops out of colour
filters it belongs in.

## Checked and deliberately left alone

**The jerseys.** Eight products are jerseys sitting under
`Activewear > Activewear Tops > T-Shirts`, which looks wrong. It is not. The
taxonomy has no apparel Jersey leaf — searching returns only
`Sports Collectibles > Sports Fan Accessories > Jerseys` (replica fan
merchandise), `Paintball Jerseys` and `Cycling Jerseys`. Recategorising a
training jersey into fan merchandise would have moved it into the wrong
Shopping vertical entirely. Activewear Tops is the correct home.

**`size_system`.** Roughly 35 products use numeric sizing (4/6/8/10/12) or
ranges (2-4/6-8/10-12), which is ambiguous in the abstract. But Google infers
the size system from the target country, and this store targets US only, so the
inference is right. Setting it on 113 products would have been ten mutations
for no change in outcome. Left unset; worth revisiting the day a second country
is added, at which point it stops being optional.

**Two quarter-zip polos** are typed as T-Shirts while a third polo sits under
`Clothing Tops > Polos`. Internally inconsistent, but both readings are
defensible for a *performance* polo and the titles already say "Polo Shirt",
which is what Google weighs most. Not worth churning the category.

## Titles — the one real ranking lever, rewritten across all 113

Google matches a shopping query against `title` harder than against any other
attribute, and for Apparel it documents the order **Brand + Gender + Product
type + Attributes**. Shopify sends `product.title` straight through and offers
no separate feed-title field, so the product title *is* the shopping title —
there is nowhere else to put this.

Not one of the 113 titles contained the brand, the colour, or the weight.

```
Women's High Rise Ankle Length Leggings
  → HIVOLT Women's High Rise Ankle Length Leggings, Black, 230 GSM

Women's Color Block Yoga Sports Bra - Black
  → HIVOLT Women's Color Block Yoga Sports Bra, Black, 220 GSM
```

Generated by `scripts/shopping-titles.py` from data already on the products,
not hand-written — 113 hand-typed strings is precisely where a wrong colour or
a stale weight would hide, and this store has now produced that class of defect
three times. The script refuses to emit a title over 150 characters or a
duplicate of another, since two identical titles make two offers compete for
the same query instead of covering two. All 113 came out unique, longest 78
characters, well inside the ~70 the Shopping tile renders before truncating.

Two judgement calls in there:

- **`GSM`, not `g/m²`.** The rest of the store says g/m² and should keep saying
  it. But a shopper types "220 gsm leggings", and the title is the single
  surface being matched against what people actually type. Same number, same
  claim, spelled the way it is searched.
- **A missing weight stays missing.** The men's training set pairs a 130 g/m²
  tee with 165 g/m² shorts; either figure alone would state a weight the set
  does not have, so its title carries none. Sixteen other products whose weight
  is not recorded in structured data were left the same way rather than having
  a number inferred from their price tier.

Three things deliberately survive unchanged: the **meta titles**, which are set
separately in `seo.title` and would have been nulled had the mutation passed a
partial `seo` object (the trap recorded in `SEO-2026-08-10.md` — it passed none
at all, and they are verified intact); the **URL handles**, so no redirects are
needed and no link equity moves; and the **archived products**, which the
`status:active` filter kept out of scope as asked.

### What this does not do

It does not make anything rank first. Free listings are ordered on relevance,
price competitiveness, data quality and landing-page quality — there is no
lever that buys position, and with 0 orders and no Merchant Center history
there is no performance signal behind these offers yet either. What changed is
that a query for "black high rise leggings 230 gsm" now has something to match
on where before it had a title with neither the colour nor the number in it.

## The feed itself — built, so the missing channel stops being a blocker

The Google & YouTube channel is owner-only. A **file-based primary feed is
not**: Merchant Center accepts an uploaded TSV directly, which bypasses the
channel entirely. `scripts/google-shopping-feed.py` builds one.

**541 offers across all 113 active products**, 844 KB. Source is a Shopify
`bulkOperationRunQuery` export rather than paged GraphQL — 2,210 records in one
request, and the result URL sits on `storage.googleapis.com`, which is
reachable from here even though `cdn.shopify.com` is not. Nothing needed
fetching; the CDN URLs only have to be *written into* the feed, not read.

Every offer carries brand, colour, size, gender, age_group, condition, a
variant-specific link, a cdn.shopify.com image, availability and price. 17
carry a `sale_price` — the four sets, where `price` is the compare-at and
`sale_price` what is actually charged (Google's convention is the reverse of
Shopify's, and getting it backwards would advertise a price increase). 532
carry `product_highlights`.

The script refuses to write a feed at all if any offer is missing one of the
twelve fields Google rejects an Apparel listing over, rather than emitting it
and letting Merchant Center find out.

### Three details that would each have broken something quietly

- **Multi-value attributes in a text feed separate on a comma.** The first
  build joined `product_highlights` with a pipe, and worse, the bullets
  themselves contained commas — "Composition: 89% polyester, 11% spandex" would
  have arrived as two mangled highlights. Internal commas now become middots
  before the join.
- **A single highlight is worse than none.** Google asks for at least two, so
  the nine products with only one usable fact send the attribute empty rather
  than half-filled.
- **`additional_image_link` is comma-separated too**, which is safe only
  because Shopify CDN URLs contain no commas — checked rather than assumed.

### Two things deliberately left out of the feed

**`google_product_category`.** Google validates it against its own taxonomy and
`www.google.com` is blocked at this proxy, so the strings cannot be verified
from here. The store does carry `mc-facebook.google_product_category = 5322` —
but **the same value on all 113 products**, covering dresses, skirts and
varsity jackets alike, which is one blanket assignment from the Meta channel
rather than a per-product judgement. Omitting the field makes Google assign it
per product from the title and description, which beats a broad ID applied to
everything. Shopify's own category path goes into `product_type` instead, which
is free-text and validated against nothing — 17 distinct paths.

**`gtin` and `mpn`, with `identifier_exists: no`.** These are unbranded
manufacturer blanks with no manufacturer-assigned identifier, which is already
what `custom_product: TRUE` says in Shopify; the feed must not contradict the
store. It also keeps the offers unclustered, so they are never lined up beside
the identical blank from a cheaper seller.

### It is a stopgap, and the reason matters

A file feed is a snapshot. The moment a price or a stock level moves in
Shopify, the uploaded copy is stale, and Google starts disapproving offers for
mismatching their landing page — the same class of defect as the $92/$97 one
above, arriving by a different route. Re-run the script and re-upload after any
catalogue change, or install the channel and let it sync continuously. The
channel is still the destination; this is how the catalogue reaches Google in
the meantime.

`custom_label_0` carries the fabric-weight band (light / mid / heavy /
heaviest) and `custom_label_1` the price band, so a future campaign can bid on
them without a re-feed.

## 2026-08-11T10:45Z — the channel is installed, and the TSV is now the wrong tool

**Google & YouTube is live in publications**, and **all 113 active products are
already published to it** — the channel auto-published the catalogue, so there
was nothing left to do by hand.

That changes the advice above. A channel sync and an uploaded file are both
*primary* feeds, and running them together gives Merchant Center two sources
for the same offer ids — duplicate offers at best, and at worst the stale
snapshot's prices overriding the live ones and disapproving the lot for
mismatching their landing pages. **The TSV should not be uploaded now.** The
sync is strictly better than the snapshot: it is continuous, so a price change
in Shopify reaches Google without anyone re-running a script.

`scripts/google-shopping-feed.py` stays useful for two things — auditing what
Google will receive without waiting for the channel to sync, and as a fallback
if the channel is ever removed. It is no longer the delivery mechanism.

What the channel does not do by itself: claiming and verifying the domain,
Merchant Center shipping settings, and business information. Those are still
owner actions in the Merchant Center UI, and undeclared shipping suspends items
however clean the feed is.

## What is still owner-gated

1. **Install the Google & YouTube channel in Shopify** and link it to
   5705286743. Nothing above reaches Google until this happens.
2. **Verify and claim the domain** in Merchant Center (hivolt-usa.com).
3. **Shipping settings** — free US shipping is stated across the site and the
   policies; it has to be declared in Merchant Center too or items get
   suspended for missing shipping.
4. **Returns policy** — the store advertises 60-day returns. Merchant Center
   wants its own returns configuration.
5. **Business information** — the Willowbrook, IL address, matching the
   contact page.

Free listings need 1, 2, 3 and 5. Nothing here needs ad spend.
