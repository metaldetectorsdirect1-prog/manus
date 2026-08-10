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
