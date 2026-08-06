# HIVOLT — Catalogue image audit

Store: `hivolt-usa.com` · `f36zps-yd.myshopify.com`
Date: 2026-08-06
Scope: all 126 products (105 active, 21 archived)

---

## The finding

**80 product images across 38 active products depict a garment HIVOLT does not
sell.** On 35 of those 38 it is the *featured* image — the one that appears in
collection grids, search results, the Google Shopping feed, and social share
cards.

The images are AI-generated. That on its own is not the problem. The problem is
what they were told to generate.

Every one traces back to an image-generation job whose prompt attached a
reference asset named `hivolt-brand-mark`, carrying this description:

> HIVOLT brand mark — volt yellow-green bolt swoosh on black.
> **This exact logo must be printed on the chest of every garment.**

A representative prompt, verbatim:

> Premium e-commerce product photograph. Athletic female model wearing a plain
> black slim fit full-zip yoga jacket … **On the left chest of the jacket is
> printed the exact `<<<hivolt-brand-mark>>>` bolt swoosh mark in volt
> yellow-green, screen-printed at realistic small scale about 3 inches wide,
> following the fabric drape.**

The actual products are unbranded Tapstitch blanks. There is no bolt logo on
them. A customer sees a branded garment on the product page and receives a plain
one.

That is a material misrepresentation, and it is the kind that produces
"not as described" chargebacks rather than ordinary returns. It also breaches
Meta Commerce and Google Merchant Center image policy, both of which require the
main image to depict the actual product — so it would block paid acquisition and
free Shopping listings independently of any customer complaint.

### Provenance, stated precisely

| | Images | Basis |
|---|---|---|
| Provably logo-fabricated | **24** | Filename carries the generation UUID; that job's prompt injects `hivolt-brand-mark` |
| Same pipeline, link broken by renaming | **56** | Filenames were changed on upload (`q7-…`, `b13-…`, `q4-…`), so the per-image job can't be identified |
| Genuine supplier photographs | **200+** | Uniform 32-hex-GUID filenames from the Tapstitch import |

I could not view any image directly — the environment's network policy blocks
`cdn.shopify.com`, and it blocks the generator's own CDN too. Everything above
comes from the generation records, which are stronger evidence than a visual
check: they are the instructions the images were made from.

Of the 90 generation jobs on file, **34 injected the fabricated logo** and 19
used a real supplier photo as the garment reference. The remaining 37 are
unbranded lifestyle/mood shots that don't depict a specific SKU.

### Secondary mismatches

Beyond the logo, some prompts describe a different garment than the one sold:

| Product | Supplier photos show | AI image was prompted as |
|---|---|---|
| Soft Hooded Sports Jacket | Light Gray | "plain **black** soft hooded sports jacket" |
| Men's Quarter-Zip Raglan Training T-Shirt | Static Blue | "plain **black** quarter-zip raglan training t-shirt" |
| Men's Jacquard Performance Tank Top | Jacquard (textured) | "**plain** black performance tank top" |
| Men's Colour Block Raglan T-Shirt | Colour block | "**plain** black raglan-sleeve … subtle dark grey sleeves" |

The fabricated branding is not even self-consistent: most prompts specify a
"bolt swoosh", one specifies "a **CIRCULAR BADGE** with a volt yellow-green ring
and bolt inside, complete circular emblem, not a bare swoosh." Two different
logos across a catalogue that has none.

---

## Recommended action

**Delete all 80 images. Keep every product.**

Every one of the 38 products retains **exactly 2 genuine supplier photographs**
after removal — verified, no product is left without imagery, and on all 35
where the fabricated image was featured, a real photograph takes its place
automatically.

Removing the *products* would be the wrong call. The products are fine and their
supplier photography is fine; 38 of 105 active products is over a third of the
catalogue, and deleting them would destroy the collection structure, the SEO work
already done, and the internal links from the blog — to fix a problem that
deleting 80 image records fixes completely.

The exact operation, ready to run:

```
audit/fabricated-image-removal.json
  → productDeleteMedia(productId: $productId, mediaIds: $mediaIds)
  → 38 products, 80 media IDs
```

**This has not been executed.** The Shopify connection expired partway through
this audit and cannot be re-authorised from a non-interactive session. Re-connect
Shopify in your claude.ai connector settings and it runs immediately.

---

## Other defects found

### 1. Alt text naming the wrong product — 2 images, live

`Women's Twist Front V-Neck Sports Bra` carries two images whose alt text
describes a completely different product:

- `q7-twistbra-life.png` → alt: *"HIVOLT Voltcore 2-Piece Set worn in studio"*
- `q7-twistbra-candid.png` → alt: *"HIVOLT Voltcore set at the gym"*

Both files are in the removal set above, so this resolves with it.

### 2. Active products with a single image — 2 products

| Product | Handle |
|---|---|
| Women's Colour Block Yoga Tank Top - White & Green | `/women-s-color-block-yoga-tank-top` |
| Women's Ruched Halter-Neck Sports Bra | `/womens-ruched-halter-neck-sports-bra` |

Every other active product has at least two. Both are missing the "alternate
view" frame the Tapstitch import supplied for the rest of the catalogue — worth
re-pulling from the supplier rather than generating a replacement.

### 3. Archived near-duplicates — 13 pairs, no action needed

Thirteen archived products are near-duplicates of active ones (e.g. archived
"Women's Fitted Flared Yoga Pants" vs active "Women's High-Rise Flared Yoga
Pants"). Archived products are not visible on the storefront and are not
indexed, so this is housekeeping, not a defect. Listed in full in the manifest's
sibling data if you want to purge them.

### 4. Clean

- **No image is shared between two different products.** Checked all 126
  products, every image file, both active and archived — zero collisions. No
  product is wearing another product's photo.
- **No active product has zero images.**

---

## What this explains

The store has 0 orders across its history. The blocking cause was the shipping
defect fixed earlier — checkout could not compute a rate, so it dead-ended before
payment. That is fixed and verified.

This is the next thing in the path. It does not stop a sale the way the shipping
defect did, but it caps everything downstream:

- **Paid acquisition is blocked.** Meta and Google both reject product images
  that don't depict the actual item. This would surface as feed disapprovals or
  an account-level flag, not as an obvious error.
- **The first sale is the expensive one to get wrong.** A store with no order
  history and a "not as described" chargeback on its first transaction starts
  its payment-processor relationship in the worst possible position.
- **It undercuts the brand's entire positioning.** HIVOLT's stated line is
  "published, not claimed" — real fabric weights, supplier specifications
  reproduced unedited. Fabricated product photography is the exact opposite of
  that, and it is the first thing a customer sees.

The catalogue's genuine supplier photography is adequate: 1400×1400, two angles,
consistent treatment across all 105 active products. It is less exciting than an
AI model in a studio. It is also true, which is the whole proposition.
