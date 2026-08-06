# Removing the 80 fabricated product images

**38 products. 80 images. Every product keeps 2 genuine supplier photographs.**

Full findings and evidence: `STOREFRONT-IMAGE-AUDIT.md`.

Four routes below, easiest first. They all do the same thing — pick one.

---

## Option A — spreadsheet upload, no code (easiest)

Use **Matrixify**, the standard bulk-edit app for Shopify.

1. Shopify admin → Apps → search **Matrixify** → install
2. Matrixify → **Import** → upload the file
3. It shows a preview before committing. Confirm the count, then Import.

**Which file to upload depends on your plan.** Matrixify's free Demo plan is
capped at [10 items per file](https://matrixify.app/pricing/); paid plans start
at $20/month and handle 5,000 per job.

- **Free plan** → upload `matrixify-free-01.csv` … `matrixify-free-10.csv`,
  one at a time. Ten imports, each under the cap. There are no daily or monthly
  limits on import *count*, only on items per file, so this costs nothing.
- **Paid plan** → upload `matrixify-delete-images.csv` once. All 80 rows.

Both contain exactly the same 80 deletions; the split files are just the same
data cut into free-tier-sized pieces, with each product's rows kept together.

The file has four columns — `Handle`, `Command: UPDATE`, `Image Src`,
`Image Command: DELETE` — one row per image, addressed by its exact CDN URL. It
touches nothing else: not titles, prices, inventory, or the supplier photos.

This is the route I'd choose. No API version to worry about, a preview before it
commits, and Matrixify writes an undo file.

---

## Option B — let Claude do it

The Shopify connector's token expired mid-audit, which is the only reason this
isn't already done. Re-authorise and say "run it":

> claude.ai → Settings → Connectors → Shopify → reconnect

Everything needed is in `fabricated-image-removal.json`. One pass.

---

## Option C — GraphQL, 5 minutes

Install the **Shopify GraphiQL App** (free, made by Shopify), open it against
`hivolt-3`.

### Step 1 — test on one product

Paste `step1-test-one-product.graphql` and run it. Expected:

```json
{ "data": { "op1_CroppedZipThroughHoodie": {
    "deletedMediaIds": ["gid://shopify/MediaImage/40182759096552"],
    "mediaUserErrors": [] } } }
```

Then load `hivolt-usa.com/products/cropped-zip-through-hoodie` and confirm the
featured image is a plain black hoodie with **no volt bolt logo on the chest**.
That's the entire point — verify it with your own eyes before doing the other 37.

### Step 2 — the rest

| File | Products | Images |
|---|---|---|
| `step2-batch1.graphql` | 10 | 14 |
| `step2-batch2.graphql` | 10 | 32 |
| `step2-batch3.graphql` | 10 | 12 |
| `step2-batch4.graphql` | 7 | 21 |

Every product is labelled with a comment, so a partial failure tells you exactly
where it stopped. `mediaUserErrors` should be `[]` throughout.

**If `productDeleteMedia` errors as an unknown field**, switch the API version
selector to `2025-01` and re-run. I generated these from memory — the connector
was down, so I could not validate them against your live schema. Option A has no
such caveat.

---

## Option D — by hand, no app

Shopify admin → Products → open each → hover the offending image → trash icon.

The images to delete are the ones **not** named as a 32-character hex string —
e.g. `hf_20260801_154647_845ff904….png`, `q7-twistbra-life.png`,
`b13-w-raglan-front.png`. Keep everything that looks like
`79f74a1ff0144ad896d49338b56275f9.png`; those are the real supplier photographs.

`fabricated-image-removal.json` lists exact filenames per product.

---

## Verifying it worked

Whichever route you take, check these three afterwards. They were the worst
offenders — the AI image was featured *and* showed the wrong colour or fabric:

| Product | Should now show |
|---|---|
| `/products/soft-hooded-sports-jacket` | **Light Gray** jacket, no chest logo (AI version was black) |
| `/products/men-s-quarter-zip-raglan-training-t-shirt` | **Static Blue**, no chest logo (AI version was black) |
| `/products/men-s-jacquard-performance-tank-top` | Visible **jacquard texture**, no chest logo (AI version was plain) |

---

## Not fixed by any of the above

**Two active products have only one image each**, unrelated to the fabrications
— they're missing the "alternate view" frame Tapstitch supplied for every other
product:

- Women's Colour Block Yoga Tank Top - White & Green — `/women-s-color-block-yoga-tank-top`
- Women's Ruched Halter-Neck Sports Bra — `/womens-ruched-halter-neck-sports-bra`

Re-pull these two from Tapstitch. Don't generate replacements — that habit is
what produced all 80 of these.

---

## After it's done

1. **Any Google Merchant Center or Meta catalogue feed will re-crawl.** If either
   was flagged for image mismatch, this is what clears it.
2. **Don't regenerate replacements.** The 200+ supplier photographs are
   1400×1400, two angles, consistent across all 105 active products. Less
   exciting than an AI model in a studio, and true — which is the whole
   proposition of a brand whose line is "published, not claimed."
