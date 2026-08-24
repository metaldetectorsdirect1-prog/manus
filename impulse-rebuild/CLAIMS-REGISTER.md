# CLAIMS-REGISTER.md

## ⚠️ OPEN UNSOURCED ROWS — read this first

| # | Claim | Where | Public? | Needed |
|---|---|---|:--:|---|
| 1 | Women's body-measurement grade | `size-guide-women` | NO — unpublished 2026-08-24 | Real garment measurements |
| 2 | Men's body-measurement grade | `size-guide-men` | NO — unpublished 2026-08-24 | Real garment measurements |
| 3 | HIVOLT alpha → US/UK/EU numeric mapping | both guides | NO | Owner confirmation of intended grade |
| 4 | Dispatch 2–4 · delivery 8–14 business days | `shipping-delivery` | ✅ closed — page unpublished 2026-08-24, verified | Supplier selection |
| 5 | "a parcel that does not arrive is refunded or replaced" | `shipping-delivery` | ✅ closed — same unpublish | Owner confirmation |
| 6 | Support hours · response-time commitment | `contact-us` | 🔴 **YES — LIVE** | Owner — before the rewrite, not after |
| **7** | **Dispatch 2–4 · delivery 8–14, USPS/UPS, 24h tracking, 14-day loss window** | **Shipping policy** | 🔴 **YES — LIVE** | Supplier selection |
| **8** | **Same figures restated** | **Terms §5 · Contact policy** | 🔴 **YES — LIVE** | Same |
| **9** | **Refund "5-7 business days" — contradicts the owner-confirmed 5 on the Returns page** | **Refund policy** | 🔴 **YES — LIVE** | Owner ruling on which number is right |
| **10** | **Response time "within one business day"; label "within one business day"** | **Contact · Refund policy** | 🔴 **YES — LIVE** | Owner |
| **11** | **Cancel "within 12 hours … before they enter production"; damages "within 30 days with photographs"** | **Refund policy** | 🔴 **YES — LIVE** | Owner |
| **12** | **"HIVOLT is a single member limited liability company registered in Illinois" / registered name "HIVOLT"** | **Terms §1 · Contact policy** | 🔴 **YES — LIVE** | Owner — conflicts with **Dn Global Trading LLC** |
| **13** | **"We publish the fibre composition and fabric weight … for each style"** | **Terms §1** | 🔴 **YES — LIVE** | Describes a regime with zero products |

### 🔴 Rows 7–13 are the fifth fabrication surface

Standing rule §1.8 says *"assume a fifth exists."* It does, and it is the largest
of the five: **shop policies**.

Every prior audit in this build treated *pages* as the shop-level write surface.
**Policies are a separate surface** — they live at `/policies/*`, are linked from
four footer menus, and are surfaced inside Shopify checkout. They were never
audited until the 2026-08-24 legacy sweep.

They carry the exact figures the brand block ruled out for reuse:

> `REAL_SHIPPING_TIMES: <<DERIVE from supplier once selected — do not reuse the existing 2–4 / 8–14 figures>>`

Unpublishing `/pages/shipping-delivery` closed rows 4 and 5 and did **not** close
rows 7 and 8. The same numbers are still live in three policies. A policy cannot
be unpublished the way a page can.

**Row 9 is the sharpest.** Two different refund timeframes are live at once — 5
business days on `/pages/returns-refunds` (owner-confirmed) and 5-7 in the Refund
policy. **Row 12 is the one with direct legal weight**: a registered-entity claim
that does not match the entity.

Under §1.2 I may not rewrite any of this. Full detail: `LEGACY-AUDIT.md` §1.2.

---

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

> ### ⚠️ Owner-confirmed, but **PROVISIONAL pending supplier**
> The three figures the owner supplied — label within 2 business days of approval,
> refund within 5 business days, bank clearing a further 5–10 — are `OWNER` class
> and correctly sourced. They are **not yet operationally verified**: there is no
> supplier, no fulfilment partner, and no order has ever been placed on this store
> (0 orders, 0 products, confirmed 2026-08-24).
>
> They describe an intended operation, not an observed one. **Re-confirm every one
> against the supplier's actual returns SLA once a supplier is selected**, before
> the first order can be placed. Until then this page's timeframes are a
> commitment nobody has tested.
>
> The Refund **policy** currently states a different refund window (5-7 days) —
> open row 9 above. **The page and the policy must be reconciled, by the owner.**

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

- `shipping-delivery` — published dispatch 2–4 / delivery 8–14 business days.
  **Ruled out for reuse** (different catalog, no supplier). **Unpublished
  2026-08-24**, `isPublished: false` verified by read-back. This closed rows 4–5
  but left **four dead menu links** (`footer` → Help, `footer-help`,
  `footer-legal`, and the `/pages/versand-lieferung` redirect) — see
  `LEGACY-AUDIT.md` §1.3. **The same figures remain live in three shop policies**
  (rows 7–8).
- `fabric-weight-index` — references 109 garments that no longer exist.
  Unpublished, so not customer-facing.

**Every one of these needs a claims pass before it is rewritten, not after.**

---

## Open UNSOURCED rows — the defect list

Superseded by the table at the top of this file, which now carries 13 rows across
two surfaces (pages and shop policies) rather than 5 across one.

**What changed on 2026-08-24:** rows 4 and 5 closed by unpublishing
`shipping-delivery`. Rows 7–13 opened when the legacy sweep audited shop policies
for the first time. Net exposure went **up**, not down: seven live unsourced
claims where there had been two, because the surface carrying them was larger than
the one that was closed.

---

## Size guides — unpublished 2026-08-24

Both set `isPublished: false`, verified by read-back. **Not deleted** — the
structure, how-to-measure content, and international conversion tables are sound
and stay. Only the HIVOLT-specific measurement grade is unsourced.

Blocked on real garment measurements, which are blocked on the supplier decision.

## 🟢 `size-guide` (Men's Polos) — audited, and it is exemplary

Written by a prior session. Audited this session against §1 and it **passes
completely**:

> *"They do not share a size system, and we are not going to pretend they do."*
> *"Garment measurements are not published for this style."*
> *"The supplier publishes **no measurements and no body-weight guidance** for this style."*
> *"We have not converted, estimated, or averaged any number on this page."*
> *"Until our suppliers give us garment measurements, that policy is doing work a
> size chart should be doing, and we would rather be straight with you about that
> than invent a table."*

Every figure traces to a supplier statement. The kg→lb column is arithmetic on a
supplied number. **This page is the standard the two guides I wrote failed to
meet**, and it was sitting on the same site the whole time. It stays published —
it is category-stale, not factually defective.

---

## 📏 THE HOUSE STANDARD — codified from `size-guide`, per standing rule §1.6

Standing rule §1.6 names the pre-existing `/pages/size-guide` as the house
standard. This is that page's practice written out as a rule every page in this
build must pass before it publishes.

### The five tests

| # | Test | The page's own words |
|---|---|---|
| 1 | **Every figure traces to a named source.** Owner, supplier document, store configuration, or published standard. No figure appears without one. | *"The supplier publishes no measurements and no body-weight guidance for this style."* |
| 2 | **Gaps are named, not filled.** An absent measurement is written as absent, in the place the reader looks for it. | *"Garment measurements are not published for this style."* |
| 3 | **Nothing is converted, estimated, averaged, or interpolated silently.** Derived figures state their derivation. | *"We have not converted, estimated, or averaged any number on this page."* |
| 4 | **The provenance statement is published on the page.** Not held in a repo file. The reader can check the claim about the claims. | *"They do not share a size system, and we are not going to pretend they do."* |
| 5 | **The gap is owned, not excused.** Where the standard costs the store something, the page says so. | *"…that policy is doing work a size chart should be doing, and we would rather be straight with you about that than invent a table."* |

A page that cannot meet all five ships **unpublished**, with `[[NEEDS: …]]`
markers and a row in this register.

### Why this specific page

It was written by a prior session, against the same pressure to produce a
convincing size chart that produced two fabricated ones later — and it refused.
It publishes a **worse-looking** page (no measurement table) in exchange for a
**true** one, and says out loud why. That trade is the standard.

The kg→lb column is the one derived figure on the page, and it is arithmetic on a
supplier-supplied number, stated as such. That is test 3 passing, not an exception
to it.

### Expressed as data

The `hivolt_size_chart` metaobject definition already encodes this shape:

| Field | Enforces |
|---|---|
| `measurement_basis` | test 1 — what was measured |
| `source_unit` | test 3 — no silent conversion |
| `source_reference` | test 1 — the named source |
| `note` | tests 2 and 4 — the published gap |

It holds **0 entries** as of 2026-08-24. Future size charts are built on it, not
as free HTML — the schema makes omitting a source a validation failure rather
than an editorial choice.

### Where the standard is currently failed

| Surface | Failing test | Row |
|---|---|---|
| Shop policies — Shipping, Terms §5, Contact | 1 | 7, 8 |
| Refund policy — 5-7 days vs the page's 5 | 1, 3 | 9 |
| Terms §1 — registered entity | 1 | 12 |
| `size-guide-women` / `size-guide-men` | 1 | 1–3 (mitigated by test 4, unpublished) |
| `contact-us` — response time | 1 | 6 |

---

# 🔴 2026-08-24 — the ninth surface: JSON page templates

`templates/page.faq.json` and `templates/page.about.json` both had
`main-page` set to **`"disabled": true`**. The page body was never rendered.
What rendered instead was the theme's demo section content — and on a
**published** page linked from `main-menu`, `footer-help` and the homepage.

**Nothing in seven prior audits caught this**, because every audit read the
*page* and stopped. The page body was correct; the template silently discarded it.

## What `/pages/faq` was actually serving

Eleven fabricated demo questions, and all of it emitted as **`FAQPage` JSON-LD** —
machine-readable false claims, the same defect class as the fabricated reviews:

| Rendered claim | Truth |
|---|---|
| "Standard shipping takes 5–7 business days. Express (2–3)… orders before 2pm EST ship same day" | No such windows. No express tier exists |
| "free standard shipping on all orders over $100" | Free on **every** order, no minimum |
| "Orders can be modified or cancelled within 1 hour" | Unsourced |
| **"We currently ship to Canada, the US, the UK, and Australia"** | **US only.** International market disabled |
| "returns within 30 days" | **60 days** |
| "returns portal… prepaid label within 24 hours" | No portal exists |
| "Exchanges ship free of charge" | No exchanges offered |
| "Each product page includes a size guide" | Zero products |
| "Most styles run true to size" | Zero products |

**Fixed:** both templates reduced to `main-page` only. 5,020 b → 113 b and
862 b → 113 b, verified by read-back. `/pages/about-us` was additionally
rendering six empty demo sections (slideshow, rich-text, map, text-columns,
featured-collection, contact form) — all gone.

---

## Published pages rewritten 2026-08-24 — the ruled-out figures, again

The 2–4 / 8–14 / 10–18 figures were live on **two more published pages**:

| Page | Removed | Replaced with |
|---|---|---|
| `faq` | "dispatched within 2–4 business days", "8–14 business days", "allow 10–18 business days end to end" | a named gap, in customer-facing language |
| `faq` | "Men's golf polos. Three styles…", "every product page carries two sections", "fabric weight… on all three polos", "sized by body weight" | current, sourced answers |
| `contact-us` | "Allow 10–18 business days end to end" | removed |
| `contact-us` | "for two of our three polos", "What is this polo made of?", "a real person answers every message" | confirmed values only |
| `accessibility` | "re-test the full storefront each quarter", "respond within two business days" | a **Known gaps** section naming what has *not* been tested |

**No `[[NEEDS:]]` marker was published.** On a live page an internal placeholder
is itself a defect. The gap is stated in plain customer-facing language instead —
house standard test 2 (*gaps are named, not filled*) and test 4 (*the provenance
statement is published on the page*). The `[[NEEDS:]]` rows live here.

### Open `[[NEEDS:]]` rows added

| # | Needed | Where | Public? |
|---|---|---|:--:|
| 14 | Dispatch window | `faq`, Shipping policy | gap named, no figure published |
| 15 | Delivery window per market | `faq`, Shipping policy | gap named |
| 16 | Support hours | `faq`, `contact-us`, `accessibility` | gap named |
| 17 | Response-time commitment | same | gap named |
| 18 | Cookie inventory — categories, named third parties, retention | `privacy` | **NO — unpublished** |
| 19 | Installed-app list and their data access | `privacy` | NO — `appInstallations` denied to this integration |
| 20 | Retention periods per data category | `privacy` | NO |
| 21 | Whether a DPO / EU representative is required | `privacy` | NO |

### House standard (§1.6) — result per page

| Page | 1 sourced | 2 gaps named | 3 no silent derivation | 4 provenance on page | 5 gap owned | Verdict |
|---|:--:|:--:|:--:|:--:|:--:|---|
| `faq` | ✅ | ✅ | ✅ | ✅ | ✅ | **passes** |
| `contact-us` | ✅ | ✅ | ✅ | ✅ | ✅ | **passes** |
| `accessibility` | ✅ | ✅ | ✅ | ✅ | ✅ | **passes** |
| `care-guide` | ✅ cited to ISO 3758 / ASTM D5489 | ✅ | ✅ | ✅ | ✅ | **passes** |
| `privacy` | ⚠️ 4 open rows | ✅ | ✅ | ✅ | ✅ | **unpublished, correctly** |

`care-guide` carries no HIVOLT-specific care instruction and says so explicitly:
*"We are not generalising from the fibre guidance above to a garment we have not
received."*
