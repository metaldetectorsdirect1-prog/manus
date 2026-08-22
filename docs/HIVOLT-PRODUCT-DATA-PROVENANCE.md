# HIVOLT — Product data provenance

**Product:** HIVOLT Classic Cotton Polo — Men's Short Sleeve
**GID:** `gid://shopify/Product/9603121774824`
**Handle:** `hivolt-classic-cotton-polo-mens-short-sleeve`
**Status at time of this pass:** `DRAFT` (unchanged — this pass does not publish)
**Pass date:** 2026-08-22
**Branch:** `claude/hivolt-store-admin-6e3q23`

This document is the audit record for every `spec.*` field on this product. It
exists so that any future person can ask "where did this number come from?" and
get an answer, and so that any field that is *deliberately empty* is on the
record as deliberately empty rather than forgotten.

Governing principle for this pass, stated by the owner:

> **A blank metafield is better than a polished lie.**

---

## 1. Evidence classification scheme

| Class | Meaning | Action |
|-------|---------|--------|
| **A** | Verified against a primary source for *this exact product* — a supplier tech pack, a garment label photograph, or a measured sample in hand. | WRITE |
| **B** | Stated by the supplier for this exact item, on the listing this product was sourced from, but not independently verified against a physical garment or a tech pack. | WRITE, with the caveat recorded |
| **C** | Inferred, generic, category-level, copied from another product, or a marketing attribute with no measurable definition. | **BLANK — do not write** |

A value is only eligible for `spec.*` if it is Class A or Class B **and** it
matches the semantics of the field it would go into. A true fact placed in the
wrong field is still a data defect, so Class B evidence that does not fit the
field's stated contract is recorded as C-by-semantics and left blank.

---

## 2. Evidence inventory

Everything below was read from the store itself on 2026-08-22, not from memory.

### 2.1 Product description bullets (supplier-transcribed)

Verbatim from `descriptionHtml` on `9603121774824`:

```
Material: 100% Cotton
Craft of weaving: Knit
Sleeve length: Short (4 - 16 Inch)
Type: regular
Pattern: Solid, decoration: NONE
Feature: Anti-Pilling
```

These are the marketplace attribute values from the source listing recorded in
`custom.supplier_source` — AliExpress item `1005002281827487`. They are supplier
declarations about this exact item. That makes them **Class B**: specific, but
not verified against a tech pack or a physical garment.

### 2.2 Supplier size table

The description carries a table with two columns — `Size label` and
**`Recommended body weight`** (`EUR S` = 60-70kg … `EUR XXL` = 100-105kg).

This is **wearer body weight, not garment measurement.** No chest, shoulder,
sleeve, or body-length figure exists anywhere in the supplier data for this
product. It cannot be converted into a size chart, and no attempt is made here.
See `docs/HIVOLT-POLO-MEASUREMENT-REQUEST.md` for the open supplier request.

### 2.3 Care line — proven boilerplate

The sentence *"Machine wash cold. Do not bleach or tumble dry."* appears
**verbatim and identically** on all three draft polos:

| Product | Material | Care sentence |
|---------|----------|---------------|
| Classic Cotton Polo | 100% Cotton | Machine wash cold. Do not bleach or tumble dry. |
| Slim-Fit Cotton Polo | Cotton | Machine wash cold. Do not bleach or tumble dry. |
| Anti-Wrinkle Polo | **Polyester** | Machine wash cold. Do not bleach or tumble dry. |

A 100% cotton garment and a 100% polyester garment carrying byte-identical care
text is the signature of copy written once and pasted three times, not of three
garment labels being transcribed. No supplier care statement was captured for
any of them. `spec.care` is therefore **Class C** and stays blank.

### 2.4 The `Type` attribute is a fit vocabulary

Across the three sourced polos the supplier's `Type` values are `regular`,
`Slim`, `regular`. A field whose observed value set is `{regular, Slim}` is
describing how the garment is cut. That is exactly what `spec.fit` holds, and
its definition says *"How the garment is cut, in the supplier's own words."*

### 2.5 Detail media — still unread

Two product images, `hv-h01-detail-1.webp` and `hv-h01-detail-2.webp`, may or
may not contain a printed measurement chart. Every retrieval path was denied by
the network policy (recorded in `docs/HIVOLT-PDP-RELEASE-QA.md`). They remain
**unread**, so they contribute no evidence to this pass in either direction.

### 2.6 Other metafields present (not `spec.*`, untouched by this pass)

`custom.supplier_source`, `custom.supplier_variant_map`,
`mm-google-shopping.gender` / `.age_group` / `.custom_product`,
`judgeme.badge` / `.widget` / `.review_widget_data`.

---

## 3. Proposed provenance table

Built **before** any mutation, per the pass's own rule.

| # | Field | Proposed value | Source | Class | Decision |
|---|-------|----------------|--------|-------|----------|
| 1 | `spec.composition` | `100% Cotton` | Supplier attribute `Material: 100% Cotton` on source item `1005002281827487` | **B** | **WRITE** |
| 2 | `spec.fit` | `Regular` | Supplier attribute `Type: regular` on the same item | **B** | **WRITE** |
| 3 | `spec.knit` | — | Supplier states `Craft of weaving: Knit` | **C (semantics)** | BLANK |
| 4 | `spec.care` | — | Description sentence, identical across three unrelated fabrics | **C** | BLANK |
| 5 | `spec.benefits` | — | Supplier attribute `Feature: Anti-Pilling` | **C** | BLANK |
| 6 | `spec.gsm` | — | No fabric weight in any source | **C** | BLANK |
| 7 | `spec.collar` | — | No collar description in any source | **C** | BLANK |
| 8 | `spec.placket` | — | No button count, placket length or material in any source | **C** | BLANK |
| 9 | `spec.cuff` | — | `Sleeve length: Short (4 - 16 Inch)` is a marketplace bucket, not a finish | **C** | BLANK |
| 10 | `spec.hem` | — | No hem description in any source | **C** | BLANK |
| 11 | `spec.finish` | — | No post-knit treatment stated | **C** | BLANK |
| 12 | `spec.seams` | — | No seam type or thread count stated | **C** | BLANK |
| 13 | `spec.opacity` | — | Never checked on a physical garment | **C** | BLANK |
| 14 | `spec.origin` | — | Country of manufacture not stated on the listing | **C** | BLANK |
| 15 | `spec.model_height_cm` | — | Photo subject unknown | **C** | BLANK |
| 16 | `spec.model_wears_size` | — | Photo subject unknown | **C** | BLANK |
| 17 | `spec.size_chart` | — | Only body-weight ranges exist; no garment measurements | **C** | BLANK (`null`) |

**Eligible for write: 2 of 17.**

### 3.1 Why each blank is blank

- **`spec.knit`** — the definition reads *"Knit or weave structure, e.g. Pique.
  Interlock. Single jersey. Leave blank unless the supplier states it."* The
  supplier states the *class* (knit rather than woven), not the *structure*.
  Writing `Knit` into a field whose examples are all structures would read on
  the PDP as a specification when it is a category. Respect field semantics:
  blank.
- **`spec.care`** — see §2.3. The definition requires text *"from the garment
  label."* No garment label has been read.
- **`spec.benefits`** — the definition is explicit: *"Each one must be traceable
  to a published spec on this same page. If a line cannot be checked against a
  number above it, it does not belong here."* `Anti-Pilling` has no GSM, no
  pilling grade, and no test standard behind it on this page. It is a
  marketplace tag, and it fails the field's own contract.
- **`spec.cuff`** — `Short (4 - 16 Inch)` is a marketplace filter bucket spanning
  a 12-inch range. It describes neither a measurement nor a finish.
- **`spec.origin`** — country of manufacture is a regulated claim. The seller's
  own shipping origin is not the garment's country of manufacture, and no label
  has been read. Guessing here is a compliance risk, not just a data risk.
- **`spec.model_height_cm` / `spec.model_wears_size`** — the pass's default is
  LEAVE BLANK unless the photo subject's height and worn size are actually
  known. They are not.
- **`spec.size_chart`** — no garment measurement exists for this product from any
  source. Creating a chart is explicitly out of scope, and would require
  inventing numbers.

### 3.2 Caveats recorded against the two written values

Both writes are **Class B, not Class A.** Specifically:

1. `100% Cotton` is a marketplace attribute selected by the supplier from a
   dropdown. It is not a tech pack, a fibre-content test report, or a photograph
   of a care label. US textile labelling rules (16 CFR Part 303) hold the seller
   responsible for fibre-content accuracy, so **this value must be verified
   against the physical garment label before this product goes live.**
2. `Regular` is a supplier self-description with no measurement behind it. It is
   accurate as a statement of what the supplier calls the cut; it is not a
   measured grading. It carries no promise about chest circumference or length.

Both caveats are carried into `docs/HIVOLT-MASTER-TASKS.md` as pre-publish
verification items.

---

## 4. Mutation record

### 4.1 Pre-write snapshot

Taken immediately before the mutation, not reused from earlier in the session:

```
product.status      DRAFT
product.updatedAt   2026-08-20T22:17:33Z
variantsCount       20
options             Color (6 values), Size (5 values)
spec.* metafields   0 present
```

### 4.2 Write

Single `metafieldsSet` call, two metafields, both `single_line_text_field`:

| Namespace | Key | Value |
|-----------|-----|-------|
| `spec` | `composition` | `100% Cotton` |
| `spec` | `fit` | `Regular` |

### 4.3 Read-back verification

Per the project rule in `CLAUDE.md`, **`userErrors: []` is not evidence of
persistence.** The write was verified by an independent re-query of the product,
issued after the mutation returned, checking:

- the value actually stored in each field,
- the field's own `updatedAt`,
- that the variant matrix, options, option-value order, status, SKUs, prices and
  inventory are byte-for-byte what the pre-write snapshot recorded.

Results are recorded in §5.

---

## 5. Post-write verification

Filled in from the independent read-back, not from the mutation payload.

The mutation returned `userErrors: []`. Per `CLAUDE.md` that is not evidence,
so everything below comes from a separate `product(id:)` query issued after the
mutation had returned.

| Field | Metafield GID | Expected | Read back | `updatedAt` | Verdict |
|-------|---------------|----------|-----------|-------------|---------|
| `spec.composition` | `…/Metafield/37962343317736` | `100% Cotton` | `100% Cotton` | `2026-08-22T02:35:09Z` | **PASS** |
| `spec.fit` | `…/Metafield/37962343350504` | `Regular` | `Regular` | `2026-08-22T02:35:09Z` | **PASS** |

The product's own `updatedAt` moved from `2026-08-20T22:17:33Z` to
`2026-08-22T02:35:11Z`. That movement is the evidence that a write actually
landed — it is the check that `productOptionsReorder` failed when it reported
success and wrote nothing.

All fifteen fields classified C read back `null`, confirming that nothing was
written beyond the two eligible rows.

| Invariant | Before | After | Verdict |
|-----------|--------|-------|---------|
| `status` | `DRAFT` | `DRAFT` | unchanged |
| `variantsCount` | 20 | 20 | unchanged |
| Variant IDs | 20 ids | same 20 ids | unchanged |
| SKUs | recorded | identical | unchanged |
| Prices | recorded | identical | unchanged |
| Inventory | recorded | identical | unchanged |
| Option names | `Color`, `Size` | `Color`, `Size` | unchanged |
| Option value order | recorded | identical | unchanged |
| `spec.size_chart` | `null` | `null` | unchanged |
| `hivolt_size_chart` metaobjects | 0 | 0 | unchanged |

The 20-variant matrix was captured before and after and compared line by line —
id, SKU, price, barcode, inventory quantity and both selected options for every
row. The two captures are byte-identical (`md5 27c1e249fd97a9e0b19e223189f0eb04`
on both).

The two sibling draft polos were checked for accidental spill-over. Neither has
any `spec.*` value and neither `updatedAt` moved:

| Product | `updatedAt` | `spec.composition` | `spec.fit` |
|---------|-------------|--------------------|------------|
| Slim-Fit Cotton Polo | `2026-08-20T18:51:32Z` (unmoved) | `null` | `null` |
| Anti-Wrinkle Polo | `2026-08-20T18:47:21Z` (unmoved) | `null` | `null` |

### 5.1 Render verification

A new gate, `site/check-hivolt-real-product.py`, renders the real snippet files
against a drop transcribed from the read-back above. **21/21 PASS.** It asserts
both directions:

- the two written values produce exactly two rows, in schema order, with the
  right text;
- each of the fifteen blanks produces no row, no empty `<dd>`, no dash, and no
  placeholder — the list of forbidden strings includes `Pique`, `Anti-Pilling`
  and `Machine wash`, the three values that were tempting and wrong;
- the size guide renders **nothing at all** — no trigger, no dialog;
- no `kg` value reaches the specification or the size guide, so the supplier's
  body-weight ranges cannot be mistaken for garment measurements;
- the template does not re-sort the Size option values, because silently
  sorting them on the storefront would hide the real ordering defect in the
  catalogue.

Both halves were mutation-tested rather than trusted:

- injecting a fabricated `spec.knit = "Pique"` turns 21/21 into **17/21**, with
  four assertions naming the problem;
- binding a valid chart makes the size guide emit 655 and 1,818 characters,
  proving the empty render comes from the guard and not from a harness that can
  never emit anything.

---

## 6. What this pass deliberately did not do

- Did not create a size chart, and did not write `spec.size_chart`.
- Did not retry `productOptionsReorder`. The Size option display order is
  **still wrong** (`S → M → XL → XXL → L`) and is tracked as a separate,
  unresolved issue — see `docs/HIVOLT-PDP-RELEASE-QA.md`.
- Did not change product status, price, inventory, SKU, barcode, or any variant.
- Did not touch swatch or colour data.
- Did not publish anything.

---

## 7. Open items before this product can go live

1. Photograph the garment care label and verify `100% Cotton` against it.
   Until then `spec.composition` is supplier-declared, not verified.
2. Obtain flat garment measurements (chest, body length, shoulder, sleeve) per
   size so a real `hivolt_size_chart` can be created. Request drafted in
   `docs/HIVOLT-POLO-MEASUREMENT-REQUEST.md`.
3. Obtain country of manufacture from the label for `spec.origin`.
4. Correct the Size option display order in the Shopify admin UI by hand. The
   catalogue still reads `S → M → XL → XXL → L`; `productOptionsReorder` reports
   success and writes nothing, and is not to be retried.
