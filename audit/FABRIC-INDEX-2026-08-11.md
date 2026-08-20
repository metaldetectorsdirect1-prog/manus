# The fabric weight index is live

2026-08-11. `hivolt-usa.com/pages/fabric-weight-index`, page ID 134034981096.

## What it is

One table holding every g/m² figure the catalogue publishes: 109 garments from
91 to 380 g/m², heaviest first, each row linking to its product page, plus four
products listed openly as publishing no weight at all.

The data was already there. It was sitting in `spec.gsm` on 113 separate
product pages, which is the worst possible shape for it — nothing can quote a
number that only exists next to one product, and Google sees 113 unrelated
documents rather than one claim about a range.

Three things it does that the product pages cannot:

* **It is quotable.** An AI asked "what gsm should activewear be" or "how heavy
  are HIVOLT leggings" needs a single passage stating the range and the
  comparison. No competitor publishes the equivalent, so there is nothing for a
  model to prefer over it. This is the only genuinely uncontested asset the
  store has.
* **It is an internal-link hub.** 109 links to product pages out of one
  document. Products currently sit several clicks deep and take roughly one
  session a day between them.
* **It is honest in a way that is hard to fake.** The four products with no
  published weight are listed as such rather than estimated or converted. A gap
  you can see is worth more than a table that looks complete, and it is the
  cheapest available proof that the other 109 numbers are real.

## Shipped alongside it

| Change | Where |
|---|---|
| SEO title — "Activewear Fabric Weight Chart: 109 g/m² Figures \| HIVOLT" | `global.title_tag` |
| SEO description, 155 chars | `global.description_tag` |
| Footer link, third in **About** | menu `footer-about` |
| Contextual link under "Fabric weights, published" | `/pages/materials-sustainability` |

Both metafields were set in the same call. `SEOInput` nulls whatever it is not
given, so a title set alone silently deletes the description — the metafield
route sidesteps that, but the pairing habit is worth keeping.

The page renders through the generic `page.liquid`, which wraps the body in
`.rte`. That already styles tables and gives them their own horizontal scroll,
so a 109-row table does not push the page sideways on a phone.

## Two things left out on purpose

**No price column.** Building this surfaced two varsity jackets, both
**380 g/m²**, priced **$42** and **$74**. The $42 one undercuts a 220 g/m²
legging at $54. That is a real pricing inconsistency, invisible while the
numbers sat on 113 separate pages, and it is the owner's to resolve. Until it
is resolved a weight-versus-price table would publicly disprove the exact
"the number justifies the price" argument the page exists to make. The product
links carry price anyway, so nothing is hidden — it just is not tabulated into
a proof against us.

**No `ItemList` JSON-LD.** It was drafted and removed. Once the item names came
out as duplicates of the visible table it held nothing a crawler could not read
straight off the 109 anchors. Structured data that restates the markup is
weight, not signal. The weights and compositions that matter are already
`Product` schema on each target page.

## Not done

The size guide was the obvious second contextual link — "a legging that feels
thin at your size is a fabric-weight problem, not a fit problem" belongs next
to the between-sizes advice. `pageUpdate` replaces the whole body and that page
is four measurement tables, so the edit meant retyping ~3.5KB of chest and hip
figures by hand into a mutation. Getting one cell wrong there ships a wrong
measurement to a customer. Not worth one internal link, and the site-wide
footer link already appears on that page. It is a clean two-minute edit in the
admin rich-text editor for whoever has the browser.

## Regenerating

`scripts/fabric-index.py` takes the JSONL from a `bulkOperationRunQuery` over
active products with their `spec.*` metafields and writes the page body. Every
number is read, never computed or rounded. It refuses to write an empty index.
Re-run it whenever products are added — the table is only worth citing while
the count in the copy matches the rows underneath it.
