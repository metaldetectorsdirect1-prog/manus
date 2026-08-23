# H01 publication gate

**Product:** `HIVOLT Classic Cotton Polo — Men's Short Sleeve`
**GID:** `gid://shopify/Product/9603121774824`
**Status:** `DRAFT` — not published to any of the store's 7 sales channels
**Gate status as of 2026-08-22:** **BLOCKED — 4 hard blockers open.** Two of
them (Gates 2 and 3) are now waiting on one supplier message that is written and
ready to send — see `docs/HIVOLT-SUPPLIER-EVIDENCE-REQUEST.md`. Preparing a
request does not narrow a blocker; only received, validated evidence does.

This document exists to make accidental publication difficult. Publishing this
product means setting `status: ACTIVE` **and/or** creating a
`publicationCreate` / `publishablePublish` against a sales channel. Either of
those is a commercial decision belonging to the owner, and neither is
authorized by any task that merely mentions product data.

**No Claude session may publish this product.** A session may only report which
gates are open. If every gate below is closed, the answer is still "ready for
the owner to publish", never "published".

---

## Verified current publication state

Read back 2026-08-22:

| Field | Value |
|---|---|
| `status` | `DRAFT` |
| `publishedAt` | `null` |
| `onlineStoreUrl` | `null` |
| `resourcePublicationsCount` | **0** |

The store has 7 publications — Online Store, Point of Sale, Manus, Shop,
Facebook & Instagram, AfterShip for TikTok, Google & YouTube. H01 is on **none**
of them. The theme going live on 2026-08-21 did not change this: theme role and
product publication are independent, and a `DRAFT` product is not reachable
regardless of which theme is `MAIN`.

---

## Gate 1 — Product-data integrity

| # | Requirement | State |
|---|---|---|
| 1.1 | **Size option order must read `S → M → L → XL → XXL`** | ❌ **BLOCKER.** Currently `S → M → XL → XXL → L`. `productOptionsReorder` returns `userErrors: []` and performs no write — **do not retry it**. Needs a manual drag in the Shopify admin |
| 1.2 | All 20 variant identities preserved through any fix | ⏳ Verify after 1.1: 20 GIDs, SKUs, prices, barcodes, inventory-item ids unchanged against the snapshot in `HIVOLT-PDP-RELEASE-QA.md` |
| 1.3 | Real inventory state | ❌ **BLOCKER.** `totalInventory 0`, `tracksInventory true`. Publishing with zero stock lists an entirely sold-out product. Artificial inventory is prohibited (`docs/HIVOLT-MASTER-TASKS.md`, standing prohibition 4) |
| 1.4 | Prices reviewed and approved | ⏳ All 20 variants are `49.00`. Owner has not approved this price point for the polo line |
| 1.5 | Product media sufficient | ⏳ Hero + 6 colourways + 2 unreadable detail images. The curation audit flags <5 real supplier images as a known gap |

---

## Gate 2 — Textile composition

**Current Shopify value: `spec.composition = 100% Cotton`**

Classification: **B — supplier-stated, `PUBLISH VERIFICATION REQUIRED`.**

The value came from a marketplace attribute (`Material: 100% Cotton`) on
AliExpress source item `1005002281827487`. That is a dropdown selection made by
the supplier. It is **not** a tech pack, a fibre-content test report, or a
photograph of a care label.

Under 16 CFR Part 303 the **seller** is responsible for fibre-content accuracy.
A wrong composition on a live listing is a regulatory exposure, not just a data
defect.

| Requirement | State |
|---|---|
| Physical care/fibre label read, or another authoritative manufacturing record obtained | ❌ **BLOCKER** — `PHYSICAL LABEL / MANUFACTURING EVIDENCE REQUEST PREPARED — RESPONSE PENDING` (2026-08-22) |

**Evidence request status.** A bilingual request for photographs of the sewn-in
composition and care labels, plus any tech pack or composition certificate, is
prepared and ready to send: `docs/HIVOLT-SUPPLIER-EVIDENCE-REQUEST.md`. It could
not be sent from the automation environment — AliExpress is denied at CONNECT
(403) and the AutoDS integration exposes no messaging tool — so it awaits the
owner sending it through the supplier chat for item `1005002281827487`.

The request deliberately asks for a **photograph**, not a yes/no answer, because
a supplier confirming "yes, 100% cotton" in chat is the same class of evidence
already held and would not clear this gate. Acceptance classes are defined in
that document **before** any reply arrives, so the standard cannot be relaxed to
fit whatever turns up.

**Do not delete `100% Cotton` while the product remains `DRAFT`.** It is the
best available evidence and it is correctly classified. Removing it would lose
information without gaining accuracy. The rule is: it stays, it stays labelled
Class B, and it must be verified before — not after — publication.

---

## Gate 3 — Sizing

| Fact | State |
|---|---|
| Garment measurements available | **None.** No chest, body length, shoulder or sleeve figure exists in any source for this product |
| `spec.size_chart` | `null` |
| `hivolt_size_chart` metaobjects | **0** |
| What the supplier does provide | *Recommended body weight* — `EUR S 60-70kg` … `EUR XXL 100-105kg`. That is a wearer attribute, not a garment dimension |

**Do not fabricate a chart.** Specifically: do not derive garment dimensions
from body weight, do not copy another brand's chart, do not reuse the
Anti-Wrinkle Polo's "Length" column (it grades at a constant 4 cm/size across
92–116 cm, which is chest-circumference grading mislabelled as length), and do
not generate a generic polo chart.

**Is the absent size chart a hard publication blocker?**

**Yes — and this is an existing project requirement, not a new one.**
`docs/HIVOLT-PDP-RELEASE-QA.md`, *Remaining release blockers* §2, already
classifies "No size chart exists, and none can be created yet" as a blocker
under *Store data*. This gate restates that finding; it does not create policy.

The aggravating factor is P-2 below: the live `/pages/size-guide` currently
shows **women's** bust/waist/hip measurements against US 4–18, and it is linked
from the footer on every page. Publishing a men's polo with no product-level
chart sends a shopper to that page. Two wrongs compound.

| Requirement | State |
|---|---|
| Supplier or measured-sample garment measurements obtained | ❌ **BLOCKER** — `EVIDENCE REQUEST PREPARED — RESPONSE PENDING` (2026-08-22) |
| `hivolt_size_chart` metaobject created from those measurements and bound to `spec.size_chart` | ⏳ Depends on the above |

**Evidence request status.** Same message, same blocker on sending. The request
asks for chest, shoulder, body length and sleeve in centimetres against our five
exact Size values, plus the three things that decide whether the numbers are
usable at all: garment-flat vs body basis, flat half-width vs full
circumference, and production tolerance. It also asks what `EUR S 60-70kg`
actually means, which nobody has confirmed.

Reject conditions are written down in advance, including the two that have
already caught bad data once: body weight presented as sizing, and a column
whose label contradicts its own values.

---

## Gate 4 — Policy and business

Only items from `docs/HIVOLT-POLICY-CORRECTIONS.md` that still gate *this
product's* publication. None of the seven has been applied.

| Item | Why it gates H01 |
|---|---|
| **P-2** — `/pages/size-guide` carries women's body measurements on a men's polo brand, reachable from every page | A shopper on a published H01 with no product chart lands here. Directly contradicts the product |
| **P-3** — shipping page says "United States only"; no fulfilment model agreed | An orderable product needs a fulfilment answer |
| **P-4** — returns are US-only in writing, conflicting with UK/EU statutory rights; page implies an Illinois warehouse that does not exist | Same |
| **P-7** — four discounts active simultaneously against unapproved pricing | Interacts with 1.4 |

`P-1` (`/pages/fabric-weight-index`, ~109 dead product links) is a live-site
incident but does **not** gate H01 specifically. Tracked separately.

---

## Gate 5 — Technical

| Requirement | State |
|---|---|
| `python3 site/check-hivolt-real-product.py` passes | ✅ 21/21 as of 2026-08-22 |
| `python3 site/check-hivolt-pdp.py` passes | ✅ 113/113 |
| Structured data truthful — no `aggregateRating`, no `review` without real reviews | ✅ Asserted by the release gate's negative checks |
| No fabricated identifiers | ✅ Every variant `barcode: null`; feed resolves `identifier_exists=no`, which is correct |
| No unapproved claims on the PDP | ✅ 15 `spec.*` fields blank by design; the spec table renders exactly 2 rows |
| Live theme matches tested source | ✅ 15/15 byte-identical by `checksumMd5` |

Gate 5 is the only gate fully closed.

---

## Summary

| Gate | Status |
|---|---|
| 1 — Product-data integrity | ❌ 2 blockers (size order, zero inventory) + 3 pending |
| 2 — Textile composition | ❌ 1 blocker (physical label unverified) — evidence request prepared, response pending |
| 3 — Sizing | ❌ 1 blocker (no measurements, no chart) — evidence request prepared, response pending |
| 4 — Policy and business | ❌ 4 unresolved owner decisions |
| 5 — Technical | ✅ closed |

**Four hard blockers. None is fabricable — each needs a supplier document, a
measured sample, a physical label, or an owner decision.**
