# Removing the 80 fabricated product images

**38 products. 80 images. Every product keeps 2 genuine supplier photographs.**

Full findings and evidence: `STOREFRONT-IMAGE-AUDIT.md`.

---

## Option A — let Claude do it (preferred)

The Shopify connector's token expired mid-audit, which is the only reason this
isn't already done. Re-authorise it and say "run it":

> claude.ai → Settings → Connectors → Shopify → reconnect

Everything needed is in `fabricated-image-removal.json`. It's one pass.

---

## Option B — run it yourself, 5 minutes

Install the **Shopify GraphiQL App** from the Shopify App Store (it's free and
made by Shopify), open it against `hivolt-3`, then:

### Step 1 — test on one product

Paste `step1-test-one-product.graphql` and run it.

Expected response:

```json
{ "data": { "op1_CroppedZipThroughHoodie": {
    "deletedMediaIds": ["gid://shopify/MediaImage/40182759096552"],
    "mediaUserErrors": [] } } }
```

Then open `hivolt-usa.com/products/cropped-zip-through-hoodie` and confirm the
featured image is now a plain black hoodie with **no volt bolt logo on the
chest**. That's the whole point of the exercise — verify it with your own eyes
before doing the other 37.

### Step 2 — the rest

Paste and run each in turn:

| File | Products | Images |
|---|---|---|
| `step2-batch1.graphql` | 10 | 14 |
| `step2-batch2.graphql` | 10 | 32 |
| `step2-batch3.graphql` | 10 | 12 |
| `step2-batch4.graphql` | 7 | 21 |

Each product is labelled with a comment, so if one fails you'll know which.
`mediaUserErrors` should be `[]` everywhere.

### If `productDeleteMedia` errors as an unknown field

Shopify has been migrating media mutations. If the API version GraphiQL defaults
to doesn't have it, switch the version selector to `2025-01` and re-run. I
couldn't validate this against your live schema — the connector was down when I
generated these.

---

## Option C — by hand, no API

Shopify admin → Products → open each product → hover the offending image →
trash icon. The images to delete are the ones **not** named as a 32-character
hex string (e.g. `hf_20260801_154647_845ff904….png`, `q7-twistbra-life.png`,
`b13-w-raglan-front.png`). Keep every image whose filename looks like
`79f74a1ff0144ad896d49338b56275f9.png` — those are the real supplier
photographs.

`fabricated-image-removal.json` lists the exact filenames per product.

---

## Not fixed by any of the above

**Two active products have only one image**, and neither is affected by the
removal — they're missing the "alternate view" frame the Tapstitch import
supplied for every other product:

- Women's Colour Block Yoga Tank Top - White & Green — `/women-s-color-block-yoga-tank-top`
- Women's Ruched Halter-Neck Sports Bra — `/womens-ruched-halter-neck-sports-bra`

Re-pull these two from Tapstitch rather than generating a replacement. Every
other active product has at least two real photographs.

---

## After it's done

Two things worth checking, in this order:

1. **Any Google Merchant Center or Meta catalogue feed will re-crawl.** If
   either was already flagged for image mismatch, this is what clears it.
2. **Do not regenerate replacements.** The 200+ supplier photographs are
   1400×1400, two angles, consistent across all 105 active products. They are
   less exciting than an AI model in a studio and they are true, which is the
   entire proposition of a brand whose line is "published, not claimed."
