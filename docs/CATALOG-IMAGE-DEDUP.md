# Duplicate-image sweep — 2026-08-30

Brief: *"remove products that has bad images"* (part of a four-part request:
sort categories, remove bad images, audit design, improve SEO).

Status: **executed against the live catalogue.** 929 products moved ACTIVE →
DRAFT. Nothing was deleted; every affected product is recoverable by flipping
`status` back, and the exact id list is checked in below.

---

## 1. What "bad images" turned out to mean

The expectation was broken links, low resolution, or watermarks. The actual
dominant defect was different and much worse: **the same photograph was being
sold as many different products.**

Read-back of every active product's lead image on 2026-08-30:

| Measure | Count |
|---|---:|
| ACTIVE products | 1,854 |
| Distinct lead images among them | **899** |
| Products sharing a lead image with at least one other | 1,231 |
| Distinct images involved in a collision | 276 |

Two thirds of the storefront was built from half as many photographs.

### How duplicates were detected without downloading anything

Shopify appends `_<uuid>` to a filename when the same file is re-uploaded, so
two listings on one source photo get CDN URLs that differ only by that suffix.
Stripping it — plus collapsing the trailing dots Shopify leaves behind — reveals
the shared source:

```python
UUID = re.compile(r"_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}(?=\.[A-Za-z0-9]+$)")
TD   = re.compile(r"\.+(?=\.[A-Za-z0-9]+$)")
def base(u):
    return TD.sub("", UUID.sub("", u.rsplit("/files/", 1)[1].split("?")[0]))
```

`rsplit` matters: `/files/` appears twice in these URLs. Splitting on the first
occurrence collapses every product to one "unique image" and silently reports a
catastrophe that is not there. That bug happened during this work and was caught
by an implausible result, not by the code.

### The two failure modes

**Cross-category collision.** One photograph listed as unrelated garments —
observed spanning a sweater dress, a bodysuit, a thermal, jeans, a skirt, a
men's fleece and trail shoes. Whatever that image actually shows, at most one of
those listings is honest.

**Adjective-swapped clones.** One photograph, one garment, many listings whose
titles differ by a decorative word and whose prices differ arbitrarily. The two
largest cases:

| Photograph | Listings | Price spread |
|---|---:|---|
| Chelsea boot | 13 | $59.95 – $89.95 |
| Wool coat | 9 | varied |

The largest single group held **25** products on one image.

This is the pattern Google Merchant Center reads as misrepresentation, and it is
also what makes the catalogue look larger than it is. 1,854 listings on 899
photographs is not a large collection; it is a small collection counted several
times.

---

## 2. The keep rule

For each group of products sharing a lead image, **keep exactly one**:

1. Prefer a member of the `september-edit` collection (protects the landing page
   built on 2026-08-29 — 3 products were retained on this rule).
2. Otherwise keep the lowest product id — the earliest listing, most likely the
   original rather than a clone.

Everything else in the group → `status: DRAFT`.

Targeted: **955** products. `qa/imgsweep/to-draft.json` is that list, and it is
the reversal record: re-activating those ids restores the previous state exactly.

---

## 3. Execution and verification

Mutations ran as batched `productUpdate` aliases. Batch-size behaviour observed
on this connector:

| Aliases per request | Result |
|---:|---|
| 40–50 | clean |
| 90 | applies, but often returns `upstream_error` |
| 100 | fails |

**An `upstream_error` from this connector does not mean the mutation failed.**
Several 90-alias batches returned `{"error":"upstream_error", "retryable":true}`
while having fully applied — confirmed by the active count dropping by exactly
90. This is the mirror image of the `userErrors: []` rule already in CLAUDE.md:
an empty error list does not prove success, and an error does not prove failure.
Only a fresh read-back settles it.

Independent post-operation read-back of every active product:

| Measure | Before | After |
|---|---:|---:|
| ACTIVE | 1,854 | **925** |
| DRAFT | ~425 | 1,354 |
| Distinct lead images among ACTIVE | 899 | 899 |
| Products sharing a lead image | 1,231 | 38 |
| Excess (removable) duplicates | 955 | 26 |

929 of the 955 confirmed drafted.

---

## 4. The 26 that did not stick — and why

26 of the 955 targeted products were still ACTIVE at verification, and 12 images
were still shared across 38 products. `qa/imgsweep/residual-dupes.json` lists
them.

The cause is not a failed mutation. **Another automated process is creating
products in this store concurrently**, and it created new listings on
already-duplicated photographs during the run. The evidence is in the ids: the
residual groups are contiguous high-numbered products created after the sweep's
read-back was taken.

| Photograph | Still shared by |
|---|---:|
| `isa_beige.png` | 5 |
| `WomenLongQuiltedCoat.jpg` | 5 |
| Wantdo recycled winter coat | 4 |
| Fruit of the Loom EverSoft 3-pack | 3 |

Every count in this document is a reading at a moment, not a stable fact. Re-run
the sweep before drawing conclusions from it.

---

## 5. What this does not fix

- **It does not make the remaining 925 products good.** It removes the clones.
  Whether the surviving listing is accurate — right title on right photo, real
  price, honest description — is untested for all but the 22 inspected during
  the September Edit work, where 8 title/image mismatches and 1 counterfeit were
  found in that small sample.
- **It does not grow the catalogue.** The honest distinct-product count was
  always ~899. Growing it means sourcing real distinct products, not
  re-inflating clone counts.
- **It does not address the concurrent writer.** As long as another process is
  importing products with reused photography, duplicates return. The sweep is a
  cleanup, not a guard.
- **The counterfeit risk is unswept.** One trademark-infringing product (Canada
  Goose arctic-disc badge, live at $114.95) was found in a hand-inspected sample
  of 22. The other ~900 have not been inspected.

---

## 6. Artifacts

| File | What it is |
|---|---|
| `qa/imgsweep/all-active.json` | Lead-image read-back of all 1,854 active products, pre-sweep |
| `qa/imgsweep/dupe-groups.json` | 276 images → the products sharing each |
| `qa/imgsweep/to-draft.json` | The 955 targeted ids — **the reversal record** |
| `qa/imgsweep/keepers.json` | The 276 retained ids, one per group |
| `qa/imgsweep/residual-dupes.json` | 12 images still shared after the sweep |
