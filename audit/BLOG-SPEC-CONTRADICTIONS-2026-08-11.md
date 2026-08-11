# The blog contradicts the product pages

2026-08-11. Found while building the fabric weight index, which is the reason
it surfaced at all: the index put 109 published g/m² figures in one place, and
that made it possible to check them against everything else the store says.

## The blog is 501 articles, not 25

`blog.articles(first: 25)` returns 25 and gives no hint there are more. A bulk
export returns **501**, all in Training Journal, all substantial (4.5–8.5 KB),
no duplicate titles. That is the largest body of content the store owns and
nothing in the admin surfaces its size.

## What is wrong with it

Every article links products and quotes their fabric weight and fibre
composition. Checked against the `spec.*` metafields those numbers came from:

| Defect | Count | Articles |
|---|---:|---:|
| Links to **archived** products | 180 | 152 |
| Fabric weight disagrees with the metafield | 36 | 30 |
| Composition disagrees with the metafield | 20 | 15 |
| Weight stated for a product whose metafield is **empty** | 137 | — |
| **Correct** weight claims | 1,190 | — |
| **Correct** composition claims | 2,141 | — |

183 of 501 articles carry at least one defect. The great majority of claims are
right, which is what makes the wrong ones expensive: this is a store whose one
argument is *published, not claimed*, and it publishes two different
compositions for the same garment in two places Google reads.

The archived links are the bigger problem and the less visible one. 180 anchors
resolve to 404. Shopify will not accept a redirect for those paths — an
archived product still owns its handle — so the only fix is to move the link.

## The 137 are not the same kind of error

These state a weight for a product that publishes none, and they split in two:

* **`soft-hooded-sports-jacket`** — the article says 130 g/m²; the product page
  says "Weight: Light (3.8 oz/yd²)". 3.8 oz/yd² *is* 129 g/m². The article is
  publishing a conversion of a figure the product does publish. Defensible
  arithmetic, but the fabric index says in as many words that a converted
  number is not a quotation, and lists this jacket as publishing no weight. The
  store cannot hold both positions.
* **`performance-short-sleeve-t-shirt`** — the article says 87% polyester,
  13% spandex at 200 g/m². The product has **no spec metafields at all**, while
  its own description reads "Every HIVOLT product publishes its exact fibre
  composition and fabric weight, taken from the supplier specification."

The second is the sharpest version of the whole problem: a page claiming to
publish a spec it does not publish, while the blog publishes one for it from an
unknown source. Whether the fix is to backfill the metafield or delete the
claim depends on the supplier sheet, which is the owner's. Nothing here guesses.

## What was corrected

`scripts/article-spec-fix.py` rewrites 190 articles — 458 edits:

| Edit | Count |
|---|---:|
| Archived link repointed, anchor text moved with it | 180 |
| Fabric weight corrected to the metafield | 165 |
| Composition phrase replaced with the published one | 113 |

Verified by re-running the audit over the corrected corpus:

```
BEFORE  wrong gsm  36   wrong comp  20   dead links 180
AFTER   wrong gsm   0   wrong comp   0   dead links   0
```

The 137 unsourced figures are deliberately untouched and the count is unchanged.

### Why only 70 of the 278 numeric edits are defect fixes

211 sit inside a window whose link was just repointed. Those numbers were
*correct* descriptions of a garment that has since been archived; once the link
moves to the replacement, they have to describe the replacement. That is the
honest limitation of a mechanical pass: the figures and the product name end up
correct, but an adjective written about the old garment can survive. "Tapered"
in a sentence now linking ankle leggings is the shape of it. A 404 is worse,
and the 152 affected articles are listed in `audit/articles-fix-report.txt` if
anyone wants to read the prose back.

### What the script refuses to do

Rewriting numbers near a link is only safe when the number is a claim about
that product. Three guards, each of which caught a real mistake during
development:

* **Advice, not spec.** "Below about 15% spandex, leggings restrict a squat"
  sits next to a product link and is about knits in general. Without the guard
  it became "Below about 78% polyamide, 22% elastane".
* **Multi-fabric garments.** "Main 61.9% cotton, 38.1% polyester · Contrast
  100% polyester" has no single blend to compare a sentence against. 14
  products are like this and are never touched. An early pass reduced them to
  one fibre and "corrected" correct copy.
* **Decimals.** `\d{1,3}` against "61.9%" matches the fraction as its own
  number and invents a "1% polyester" claim that appears nowhere.

A final check refuses to write the file at all if any substitution left
mangled text behind.

## To apply

`bulkOperationRunMutation` is blocked by this container's MCP policy, so the
corrections could not be pushed from here. Both carriers are committed:

* `audit/articles-fixed-matrixify.csv` — 190 rows, Matrixify **Blog Posts**
  import, matches on ID and rewrites Body HTML only.
* The same corrections as bulk-mutation JSONL are reproducible by re-running
  the script against fresh exports.

Re-run before importing if products have changed since 2026-08-11 — the CSV
encodes the catalogue as it was on that date.
