# Rewriting the copy that contradicted the brand — and correcting my own number

2026-08-12.

## The 96 was wrong. It is 17.

I told the owner "96 of 113 product descriptions carry dropship superlatives",
repeating the claims agent's figure without checking it. Scanning for the exact
phrases that agent quoted — *unmatched, unparalleled, premium, superior,
luxurious, Elevate your, Transform your, Don't miss, order yours today, say
goodbye, boost your confidence, Experience Ultimate, Unleash, perfect companion,
step up your, flattering fit, enhances your* — returns **19**, and every single
product the agent named by hand is inside those 19. The 96 is not reproducible.

Then two of the 19 turned out to be false positives of my own:

* **`mens-training-set-tee-shorts`** — "premium" appears inside *"we publish them
  rather than describing the fabric as **premium**"*. The sentence is the brand
  position, stated correctly. A negation filter catches it. This is exactly the
  case `check-liquid.py` was built negation-aware for, and I nearly rewrote
  correct copy into worse copy.
* **`two-tone-fleeced-varsity-jacket`** — the only hit was "you'll" in *"the one
  you'll wear most"*. Ordinary prose, not hype.

**True figure: 17 of 113.** 96 clean, not 17 clean. The job was one sixth the
size I reported, and worth measuring before starting.

Also worth recording: **all 13 products in the Featured collection were already
clean** — the copy a homepage visitor actually reads was never the problem.

## What was rewritten

All 17, each grounded in that garment's own `spec.*` metafields rather than in
adjectives. The shape is consistent: what it is, the weight and composition as
published, **the trade-off stated plainly**, then shipping and returns.

The trade-offs are the point, because they are what the superlatives were
covering:

* `mens-drawstring-shorts` — *"At 165 g/m² these breathe well and are not opaque
  under hard stretch the way a 240 g/m² short would be. That is the trade, and it
  is the reason we print the number."*
* `mens-regular-fit-performance-t-shirt` — *"130 g/m² is light enough that it
  will show sweat and is not an opaque layer on its own."*
* `men-s-quarter-zip-raglan-training-t-shirt` — *"At 4% the stretch is minimal, so
  the movement comes from the raglan cut rather than the fabric giving."*
* `womens-halter-neck-yoga-sports-bra` — *"It is a low-to-medium impact bra and we
  would rather say so than let you find out sprinting."*
* `cropped-half-zip-hoodie` — *"The cotton fraction is why it feels softer than a
  pure synthetic at the same weight, and also why it takes longer to dry."*

`soft-hooded-sports-jacket` is the one that had to say something awkward. It
publishes **3.8 oz/yd² and no g/m²**, so the copy now says so, refuses the
conversion in as many words — *"a converted number is not a quotation"* — and
links the Fabric Weight Index where it is listed as publishing no weight. That
matches what the index already says about it, which it did not before.

Every rewrite closes on the corrected returns line: **"60 days to return it,
unworn with tags — free prepaid label."**

## The one that needed care

`performance-long-sleeve-t-shirt` was the only one of the 17 carrying a
measurement table. `productUpdate` replaces the whole body, so fixing the prose
meant re-sending 44 cells of chest, shoulder and length figures — the same class
of risk that stopped the size-guide edit earlier in the day, and the same class
of mistake that wiped a description an hour before.

Done by copying the table verbatim from the day's bulk export and **verifying all
44 cells by reading the field back** afterwards. Every figure matches: Length
23.62/60 → 26.77/68, Shoulder 26.18/66.5 → 28.54/72.5, Chest 15.94/40.5 →
19.09/48.5.

## Verified after

Re-exported all 113 descriptions and re-ran the scan: **0 of 113 carry
superlative copy**, down from 17. No g/m² figure in any description contradicts
its metafield.

## Also closed today

All **8 products advertising sizes they do not sell** are fixed — 3 earlier, 5
here. The remaining five were in SEO descriptions, which is the Google snippet:

| Product | Advertised | Actually sells |
|---|---|---|
| `men-s-jacquard-slim-mesh-t-shirt` | S–4XL | **M–3XL** |
| `classic-stripe-trim-basketball-shorts` | S–4XL | S–3XL |
| `men-s-quarter-zip-raglan-training-t-shirt` | S–2XL | **M–3XL** |
| `soft-hooded-sports-jacket` | S–2XL | **M–2XL** |
| `womens-full-zip-sports-jacket` | S–2XL | S–**XL** |

Someone searching a size they cannot buy is a lost sale that never shows up in
any funnel report, because the visit looks identical to a bounce.
