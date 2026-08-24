# CLAIMS-REGISTER.md

Every factual claim published at shop level, with its source. Maintained for the
rest of the build; every new page adds rows.

**Source classes:** `OWNER` (supplied in a brief) · `CONFIG` (read from store
configuration) · `STANDARD` (published external standard) · `UNSOURCED` (**a
defect**).

> ### Why this file exists
> The dev theme was treated as the isolation boundary for this build. **It never
> covered pages.** Shopify pages are shop-level and publish immediately, so every
> page written in the last two sessions has been publicly readable on a domain
> drawing ~4,458 sessions a quarter. Two invented figures were live for roughly
> 24 hours before being caught.

---

## Returns & Refunds — `/pages/returns-refunds`

| Claim | Source | Status |
|---|---|---|
| 60-day return window | OWNER | ok |
| Free prepaid return label | OWNER | ok |
| No restocking fee | OWNER | ok |
| Refund to original payment method | STANDARD (Shopify default) | ok |
| **Label sent within 2 business days of approval** | **OWNER** (supplied this session) | ✅ **corrected** |
| **Refund processed within 5 business days of arrival** | **OWNER** (supplied this session) | ✅ **corrected** |
| **Bank clearing a further 5–10 days** | **OWNER** (supplied this session) | ✅ **corrected** |
| Return address — Dn Global Trading LLC, Willowbrook IL | CONFIG (`shop.billingAddress`) + Terms | ok |
| Condition: unworn, unwashed, tags attached | OWNER-implied by "any reason" + STANDARD | ok |
| Faulty goods have no 60-day limit | STANDARD (statutory) | ok |
| Discount recalculated on partial return | CONFIG (Shopify default behaviour) | ok |

### 🔴 Removed this session — three more UNSOURCED claims I had written

Found by self-audit, not supplied by anyone, now **deleted from the live page**:

| Claim removed | Why it was a defect |
|---|---|
| *"underwear, swimwear and pierced jewellery cannot be returned … stated on those product pages as well as here"* | No such exclusion was ever given. **And it asserts content on product pages that do not exist** — there are zero products |
| *"say so and we will send a QR code you can scan at the carrier counter"* | Depends on carrier capability nobody confirmed |
| *"email us and we will arrange a straight swap manually"* | An operational commitment nobody authorised |
| *"we do not ask for the faulty item back unless there is a reason to inspect it"* | A process commitment nobody authorised |
| *"If we sent you the wrong item, the replacement ships before the original comes back"* | Same |

**This was the third fabrication.** The instruction to assume one existed and go
looking was correct.

---

## Size Guide — Women `/pages/size-guide-women` · Men `/pages/size-guide-men`

| Claim | Source | Status |
|---|---|---|
| **Body-measurement tables** (bust/waist/hip; chest/waist/neck/sleeve) | **UNSOURCED** | ⚠️ **flagged + framed** |
| US/UK/EU/AU/JP conversions | STANDARD | ok |
| **Mapping HIVOLT XS → US 2 / US 34** | **UNSOURCED** | ⚠️ flagged |
| How-to-measure method | STANDARD | ok |
| Sizing advice (size up for layers, etc.) | STANDARD | ok |
| 60-day returns reference | OWNER | ok |
| ~~"Every product page carries that garment's laid-flat measurements"~~ | **was UNSOURCED and false** | ✅ **corrected** |

### 🔴 The size charts are the largest unsourced claim on the site

**I generated both tables.** They are the conventional alpha-size grade, not
invented arbitrarily — but nobody supplied them, and there is no catalog to
check them against. Published without qualification, they read as HIVOLT's
sizing.

They were **not deleted**, because a size guide with no measurements is not a
size guide, and the pages carry real value. Instead both now open with an
explicit provenance statement:

> *"The table below is the standard alpha-size grade used across womenswear. It
> is not derived from measuring HIVOLT garments — it is the grade our sizing is
> built to. Once a garment is in production, its own laid-flat measurements are
> published on its product page, and those measurements govern."*

That converts an implicit claim into an explicit, checkable one. **It does not
make the numbers sourced.** They must be confirmed against the first production
garments, and the register keeps that open.

Also corrected: both pages said product pages **carry** measurements, present
tense. There are no product pages. Now conditional.

---

## Terms of Service — `/pages/terms-of-service`

| Claim | Source | Status |
|---|---|---|
| Dn Global Trading LLC, Illinois LLC | OWNER + pre-existing page | ok |
| Address, phone, email | OWNER + CONFIG | ok |
| Ships within the United States only | CONFIG (International market disabled) | ok |
| Payment via Shopify Payments | CONFIG | ok |
| No subscriptions | Pre-existing page | ok |
| Governing law: Illinois, DuPage County | Pre-existing page | ok |
| "We do not **currently** sell supplements" | CONFIG (store history shows it did) | ok — qualified this session |
| Category: women's and men's apparel | OWNER (brand block) | ok |

---

## Pages inherited, not written by this build

`about-us` · `faq` · `shipping-delivery` · `60-day-love-it-guarantee` ·
`contact-us` · `accessibility` · `track-order` · `materials-sustainability` ·
`data-sharing-opt-out` · `size-guide` · `size-chart` · `voltcore` ·
`fabric-weight-index`

**Not audited claim-by-claim this session.** They were written by a prior
session against the men's-polo positioning and are all scheduled for rewrite.
Two are known to carry live defects:

- `shipping-delivery` — publishes dispatch 2–4 / delivery 8–14 business days.
  **Ruled out for reuse** (different catalog, no supplier). Currently live and
  unsourced for the new catalog.
- `fabric-weight-index` — references 109 garments that no longer exist.
  Unpublished, so not customer-facing.

**Every one of these needs a claims pass before it is rewritten, not after.**

---

## Open UNSOURCED rows — the defect list

| # | Claim | Page | Needed |
|---|---|---|---|
| 1 | Women's body-measurement table | `size-guide-women` | Measurements from first production garments |
| 2 | Men's body-measurement table | `size-guide-men` | Same |
| 3 | HIVOLT alpha → US/UK/EU numeric mapping | both guides | Owner confirmation of the intended grade |
| 4 | Dispatch 2–4 / delivery 8–14 business days | `shipping-delivery` | Supplier selection |
| 5 | Support hours and response-time commitment | `contact-us` | Owner — page not yet rewritten, gap recorded in advance |

Rows 1–3 are live now. Row 4 is live and inherited. Row 5 is pre-recorded so the
Contact rewrite cannot introduce it silently.
