# GENERAL-STORE-CATALOG-SCORECARD.md — 2026-08-28

Covers the HIVOLT sourcing programme: five tranches tagged
`batch-2026-08-28` (28 products) plus the W35 gap-fill tranche tagged
`sourcing-batch-2026-W35` (7 products). **35 sourced drafts total.**

Every number here is derived from supplier data captured at research time
and from post-mutation Shopify read-backs. Nothing is estimated upward.

---

## 1. Store-state finding that dominates this pass

At pre-flight the store held **439 products, 404 of them carrying
non-zero inventory**. Only the 35 products in this programme carry
`totalInventory: 0`.

| Group | Count | Inventory | Images | Supplier attached |
|---|---:|---|---|---|
| This programme (sourced drafts) | 35 | **0** | 1 pixel-reviewed lead each | Yes, item ID recorded |
| Owner knitwear drafts (pre-existing) | 4 | 10 / 10 / 10 / 680 | yes | not recorded |
| Concept catalogue created 17:22 UTC by another process | 400 | **1000 each** | 386 have **none** | 386 tagged `needs-sourcing` |

The 400-product concept catalogue was created after this session's last
verified read. It is a *keyword/concept* catalogue: titles, product
types, retail prices and a 1000-unit inventory figure, but for 386 of
them no images and no supplier. See §5 for the inventory adjudication.

---

## 2. Funnel — W35 gap-fill tranche

| Metric | Value |
|---|---:|
| Supplier listings evaluated | 28 |
| Unique products after de-duplication | 22 |
| Pixel-inspected before any write | 8 |
| Created as drafts | 7 |
| Rejected | 21 |
| **Rejection rate (listings)** | **75%** |

### Rejection reasons — W35

| Reason | Count | Share of rejections |
|---|---:|---:|
| Duplicate listing / same product | 6 | 29% |
| Shipping cost volatility (quotes to $54–75) | 5 | 24% |
| Image gate (watermark, monogram, brand emblem) | 4 | 19% |
| Economics — RED multiple (2.1–2.4×) | 4 | 19% |
| Off-category / supplier-brand risk | 2 | 10% |

### Cumulative across the whole programme

| Metric | Value |
|---|---:|
| Candidates assessed (tranches 1–5 pixel-eyeballed) | 46 |
| Candidates assessed (W35 listings evaluated) | 28 |
| **Total assessed** | **74** |
| Created | 35 |
| Rejected | 39 |
| **Rejection rate** | **53%** |

---

## 3. Category balance — the 35 sourced drafts

The W35 tranche was deliberately spent on **zero-coverage categories**,
not on deepening the categories that were already heavy.

| Category | Before W35 | Added | Now | Note |
|---|---:|---:|---:|---|
| Cardigans | 6 | 0 | 6 | already deepest |
| Dresses | 5 | 0 | 5 | |
| Jeans | 4 | 0 | 4 | |
| Sweaters | 3 | 0 | 3 | |
| Coats | 3 | 0 | 3 | |
| Jackets | 3 | 0 | 3 | |
| Matching sets | 2 | 0 | 2 | |
| Pants | 2 | 0 | 2 | |
| **Skirts** | **0** | **+2** | 2 | new |
| **Blazers** | **0** | **+1** | 1 | new |
| **Denim jackets** | **0** | **+1** | 1 | new |
| **Tops / blouses** | **0** | **+1** | 1 | new |
| **Basics / bodysuits** | **0** | **+1** | 1 | new |
| **Bags** | **0** | **+1** | 1 | new |
| **TOTAL** | **28** | **+7** | **35** | 14 categories, was 8 |

Category count went from 8 to 14. The largest single category is now 17%
of the batch (was 21%).

---

## 4. Economics — W35 tranche (precise supplier data)

Landed = supplier item price (low end) + shipping to US.

| Product | Landed | Retail | Gross $ | Gross % | Multiple | Class | Paid ads |
|---|---:|---:|---:|---:|---:|---|---|
| Double Breasted Tailored Blazer | 20.90 | 79.00 | 58.10 | 73.5% | 3.78× | GREEN | STRONG |
| Relaxed Satin Button-Up Shirt | 10.07 | 39.00 | 28.93 | 74.2% | 3.87× | GREEN | POSSIBLE |
| Square Neck Bodysuit | 6.43 | 29.00 | 22.57 | 77.8% | 4.51× | GREEN | WEAK (AOV) |
| Structured Shoulder Tote | 24.46 | 79.00 | 54.54 | 69.0% | 3.23× | YELLOW | STRONG |
| Cable Detail Knit Midi Skirt | 21.18 | 59.00 | 37.82 | 64.1% | 2.79× | YELLOW | POSSIBLE |
| Full Pleated Midi Skirt | 30.43 | 79.00 | 48.57 | 61.5% | 2.60× | YELLOW | POSSIBLE |
| Fitted Denim Blazer Jacket | 35.28 | 89.00 | 53.72 | 60.4% | 2.52× | YELLOW | POSSIBLE |

**Medians:** landed $21.18 · retail $79.00 · gross $48.57 · gross 69.0%
**Distribution:** GREEN 3 · YELLOW 4 · RED 0 (no RED product was imported)
**Paid ads:** STRONG 2 · POSSIBLE 4 · WEAK 1

### Why three products below the 3.5× floor were still created

Each is tagged `below-3-5x-floor-documented` and carries the reasoning in
its own description:

- **Cable Detail Knit Midi Skirt (2.79×)** — skirts were a zero-coverage
  category; gross dollars ($37.82) still clear a $30 CPA.
- **Full Pleated Midi Skirt (2.60×)** — the constraint is $9.30 shipping
  on a $21.13 item, not the item cost. Renegotiated shipping moves this
  to GREEN without touching retail.
- **Fitted Denim Blazer Jacket (2.52×)** — denim jackets were
  zero-coverage; $53.72 gross dollars is the strongest of the three.

The paid-ads reality check is the reason none of these is a hero: a 2.5×
multiple survives organic and email, but leaves little room once a ~$30
CPA, payment fees and refunds are stacked.

---

## 5. Inventory audit

### The four pre-existing owner drafts

| Product | Variants | Inventory | Tracked | Class | Action |
|---|---:|---:|---|---|---|
| Ivy soft chunky knit turtleneck sweater | 1 | 10 | true | **C — unknown** | INVENTORY VERIFICATION REQUIRED |
| Warm cable knit cardigan with pockets | 1 | 10 | true | **C — unknown** | INVENTORY VERIFICATION REQUIRED |
| Nora oversized chunky knit winter sweater | 1 | 10 | true | **C — unknown** | INVENTORY VERIFICATION REQUIRED |
| Elena relaxed merino wool mock neck sweater | **68** | **680** (10 × 68) | true | **C — unknown** | INVENTORY VERIFICATION REQUIRED |

The 680 figure is not a bulk stock position — it is a uniform 10 units on
each of 68 variants, which is the signature of an import default rather
than a counted shelf quantity. That pattern makes class B (placeholder)
more likely than A, but "likely" is not evidence, so all four are
recorded as **C — unknown**.

**No inventory was mutated.** The task authorises zeroing only where
project authorisation to correct false draft inventory is already
established. It is not: the standing rule prohibits *this session from
creating* artificial inventory, which is not the same as authority to
rewrite quantities on records another party created. Mass-editing 404
products' stock is also hard to reverse. Both point the same way — report,
do not mutate.

### The 400-product concept catalogue

Same adjudication, at scale: **400 products × 1000 units = 400,000
phantom units**, 386 of them on products with no images and no supplier.
All are DRAFT, so nothing is customer-visible today.

**This is the single largest live risk in the store.** If any of these
reach ACTIVE or enter the Merchant Center feed carrying 1000 units and no
image, that is a textbook misrepresentation event on a GMC that has not
yet cleared its first review.

Recommended owner actions, in order:
1. Decide whether the 400 concept records should exist as products at all
   (a spreadsheet or metaobject is the safer home for un-sourced concepts).
2. Whatever survives: zero the inventory, or switch tracking off, before
   any of it is activated.
3. Keep `needs-sourcing` products out of every collection and out of the
   feed until a supplier and images are attached.

---

## 6. Gates applied this pass

| Gate | Outcome |
|---|---|
| Image / pixel | 4 rejections — INSTYLISH watermark; Yogodlns watermark **plus** monogram-style all-over print; NEEDARNA watermark; "STORE TOWN" watermark **plus** chest-embroidered emblem and hangtag |
| Trademark / brand | The Yogodlns monogram tote and the emblem-bearing knit set were rejected under this gate as well as the image gate. No supplier-branded item was renamed to HIVOLT |
| Material claim | "Silk" stripped from the satin shirt (fibre unverified); "PU leather" stated as synthetic on the tote; no cashmere, wool-percentage, thermal or waterproof claim was carried through |
| High-risk product | Real-fur and children's items screened out before pixel review |
| Duplicate | 6 rejections; the bodysuit existed as 4 listings and the beanie as 3 — one listing kept, or none |
| Shipping | 5 rejections where quoted shipping ranged to $54–75 and would destroy conversion economics |
| Economics | 4 rejections at 2.1–2.4× |

---

## 7. Honest supply gaps still open

| Category | Status |
|---|---|
| Fleece-lined leggings | 0-for-3 on image compliance (tranche 3) and no clean source found since |
| Hoodies / sweatshirts | Searches return wearable blankets and menswear; needs a different query strategy |
| Accessories (scarf/beanie/gloves) | Only kids' sets and one supplier-branded beanie with $14 gross — not worth a slot |
| Knit co-ord sets | Both candidates failed the image gate; category still thin at 2 |
| Shoes / boots | Not yet attempted — sizing and returns risk needs its own policy first |
| Shackets / overshirts | Not yet attempted |

These are recorded as gaps rather than filled with weaker product. The
weekly target is a ceiling, not a quota to be met by lowering the bar.
