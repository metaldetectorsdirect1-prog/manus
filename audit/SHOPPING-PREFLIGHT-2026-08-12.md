# Merchant Center pre-flight: what happens when the claim lands

2026-08-12. Everything Google checks before it will serve an offer, checked
here first — so that if offers get held after the domain claim, the cause is
known to be inside Merchant Center rather than in the catalogue.

## Clean

| Check | Result |
|---|---|
| Products published to Google & YouTube | **113 / 113**, none missing |
| Products with an image | **113 / 113** |
| Image size | **every image 1400×1400** — Google's apparel minimum is 250×250, recommendation 800×800 |
| Images below the minimum | **0** |
| Images below the recommendation | **0** |
| `availableForSale` | true, inventory 1,000/variant, policy `CONTINUE` |
| `productType` | populated on 113 / 113 |
| `vendor` | HIVOLT on 113 / 113 |
| Products priced at or below cost | **0** |
| Products loss-making under any live discount code | **0** (was 5 this morning) |

Images were the biggest disapproval risk and they are not a risk at all —
1400×1400 square is comfortably past what Google asks for.

## The description audit came back clean, and my first flag was wrong

Every `g/m²` and every fibre percentage in all 113 product descriptions,
checked against the `spec.*` metafields they are supposed to agree with:

```
g/m²        correct 211   wrong 0
composition correct 326   wrong 0
```

The checker initially reported one mismatch, on the Voltcore set — description
"200", metafield "220". Reading the sentence killed it:

> Most leggings sit at **180–200 g/m²**. At 220 the knit carries enough density…

That is a comparison against the market, not a claim about the garment. Same
false-positive class as "below about 15% spandex" in the blog script, caught the
same way — by reading the sentence instead of trusting the regex. **The product
descriptions contain no incorrect specification.**

Three further hits were `mens-training-set-tee-shorts` stating 130 and 165 for
its two pieces while carrying no single `gsm` metafield. Correct behaviour for a
two-fabric set, not a defect.

This matters beyond tidiness: the blog needed 56 figure corrections. The product
pages needed none. The pages a buyer actually reads are the accurate ones.

## The flagship's arithmetic holds

`voltcore-2-piece-set` claims "the bra is $38 and the leggings $54 — $92. The
set is $79, so you save $13." Checked against live prices:

* Twist Front V-Neck Sports Bra — **$38.00**
* High-Waisted Flare Leggings — **$54.00**
* Set — **$79.00**, `compareAtPrice` **$92.00**

$38 + $54 = $92. $92 − $79 = $13. Every number is right, and the $92 compare-at
is a genuine component sum rather than an invented reference price — which is
the version Google's pricing rules require.

Worth noting because this exact claim has drifted three times before, each time
on a stale legging price.

## Minor, not blocking

* **2 products carry a single image.** Google accepts it; `additional_image_link`
  improves the listing. Both need the alternate view from the supplier.
* **17 of 113 descriptions use templated hype** — "Elevate Your Workout",
  "Don't miss out", "Say goodbye to… hello to". 96 are clean. It costs nothing
  in Merchant Center, but it is the opposite of the brand's stated position, and
  the worst six are `womens-performance-crop-t-shirt` (7 markers),
  `womens-topstitching-yoga-tank-top`, `womens-u-neck-yoga-romper`,
  `women-s-cropped-sports-bra`, `men-s-quarter-zip-raglan-training-t-shirt`,
  `men-s-lightweight-sport-jersey`.
* **No product ratings.** Zero reviews store-wide. Shopping listings with star
  ratings outperform those without, and this cannot be fixed without orders.

## A query filter that lies

`productsCount(query: "status:active AND -available_for_sale:true")` returns
**113** — i.e. it claims every product is unavailable — while the same products
read `availableForSale: true` with 1,000 units each. The filter is silently
ignored, exactly like `metafields.mm-google-shopping.gender:female` returning
110 for every gender value, and like the `has_image` filter before it.

**Never conclude anything from a Shopify product query filter without reading
the field back on an individual product.** Three separate filters have now
lied in this store.
