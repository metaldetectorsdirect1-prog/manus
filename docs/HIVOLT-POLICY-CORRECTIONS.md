# HIVOLT — Live policy & content corrections

Created 2026-08-20. **Nothing in this file has been applied.** Every item below
is live text on hivolt-usa.com right now, quoted verbatim. Each one is a
commercial, legal or factual claim, which puts it on the OWNER side of the
authority boundary — so this document proposes replacements and stops there.

Two things make this urgent rather than tidy-up:

1. Six of these pages describe a catalogue that no longer exists. The 95
   women's activewear products were deleted; the pages that sold them were not.
2. Google Merchant Center reviews the destination site, not just the feed. A
   shipping policy that says "United States only" and a fabric page whose 109
   product links all 404 are grounds for disapproval before a single product is
   submitted (`HIVOLT-GOOGLE-COMMERCE.md` §2).

How to use it: read the **SAFE REPLACEMENT DRAFT**, answer the **OWNER INPUT
REQUIRED** question, and the change can be applied in one pass. Where the owner
input is unresolved, the replacement draft is written so it is true *today* and
does not need revisiting when the answer arrives.

---

## P-1 — `/pages/fabric-weight-index` — 109 dead product links

**CURRENT TEXT** (opening, verbatim)

> **Every fabric weight HIVOLT sells, in one table.** 109 garments, from 91 to
> 380 g/m², each figure taken from the supplier's specification sheet rather
> than estimated or rounded.
>
> […] Almost no activewear brand publishes it. We publish all of it, including
> the numbers that are not flattering.

Followed by a 109-row table, every row linking to a deleted product
(`/products/womens-yoga-sports-bra`, `/products/voltcore-2-piece-set-...`, and
107 more).

**WHY IT IS WRONG**

- Every one of the 109 product links now returns 404. The page is published and
  indexable.
- "Every fabric weight HIVOLT sells" describes zero live products.
- It is the single strongest trust asset on the site and currently the single
  strongest signal that the site is abandoned. A crawler that samples this page
  sees a soft-404 farm.
- The footer `Fabric` menu still points at it, and the earlier audit recorded a
  dead link from the Materials page.

**SAFE REPLACEMENT DRAFT**

Two options, and the choice is genuinely open:

*Option A — retire the page.* Unpublish it and 301 `/pages/fabric-weight-index`
to `/pages/materials-sustainability`. The index rebuilds itself once polos ship
with real g/m² figures, because the same `spec.gsm` metafield that feeds the
product page can generate it.

*Option B — reset the page.* Replace the body with:

> **Every fabric weight we publish, in one table.**
>
> This index lists the measured g/m² of every HIVOLT garment currently on sale.
> The polo line is in development and none of it has shipped yet, so the table
> is empty — a gap you can see is worth more than a table that looks complete.
>
> When a garment goes on sale, its weight appears here on the same day, taken
> from the supplier's specification sheet. We do not convert from another unit
> and we do not estimate.

**OWNER INPUT REQUIRED** — Retire (A) or reset (B)? A is lower risk; B keeps the
URL's existing equity and matches the brand's stated position.

**MARKETS AFFECTED** — All. This is the page most likely to be sampled by
Merchant Center review in any country.

---

## P-2 — `/pages/size-guide` — women's body measurements on a men's polo brand

**CURRENT TEXT** (verbatim extracts)

> Most HIVOLT pieces use US letter sizing (S–2XL). Denim uses standard US
> numeric sizes.
>
> **Letter sizing — body measurements**
> | Size | US | Bust (in) | Waist (in) | Hip (in) |
> | S | 4–6 | 35–36 | 27–28 | 37–38 |
> … through 2XL / US 18 …
>
> **Bust:** around the fullest point, tape level under the arms.

**WHY IT IS WRONG**

- Bust/waist/hip against US 4–18 is a women's size chart. The brand is now
  men's and unisex polos.
- "Denim uses standard US numeric sizes" — there is no denim.
- The figures are body measurements with no stated source. Nothing on the polo
  line has been measured yet, so they cannot be re-badged for polos.
- The page is linked from the footer in two places and from the header toolbar
  menu, so it is reachable from every page of the site.

**SAFE REPLACEMENT DRAFT**

> **Sizing**
>
> Each product page carries the size chart measured for that specific garment.
> Where a garment has not been measured, its page shows no chart rather than a
> generic one — a chart that does not match the item in the box is worse than
> no chart at all.
>
> Open a product and use the **Size guide** button next to the size selector.
> Measurements can be switched between centimetres and inches.
>
> Between sizes, or the chart does not answer your question? Email
> support@hivolt-usa.com with your measurements and we will tell you which size
> to order.

This is already true of the draft theme: the size guide is driven by the
`spec.size_chart` metaobject and renders nothing when no chart is attached
(`site/theme-v7/snippets/hivolt-size-guide.liquid`, T2).

**OWNER INPUT REQUIRED** — None for the replacement text itself. It stops
promising specific numbers, which is the only claim in the current version.
Confirm the support address is the one to publish.

**MARKETS AFFECTED** — All. EU/UK shoppers will additionally expect EU numeric
sizing alongside letter sizing; that is a follow-on once real charts exist.

---

## P-3 — `/pages/shipping-delivery` — "United States only"

**CURRENT TEXT** (verbatim)

> We ship to the **United States** only.
>
> **United States — FREE Tracked Shipping**
> - **Cost:** FREE on every order — no minimum
> - **Production and dispatch:** 2–4 business days
> - **Delivery time:** 8–14 business days after dispatch

**WHY IT IS WRONG**

- It directly contradicts the stated objective of selling into Canada, the UK
  and the EU. Shopify Markets confirms it: the "International" market covering
  GB, FR, IT, ES, NL, BE, CH, IE, PL, PT, CZ, SE, NO, DK, FI, CA and AU is
  `enabled: false` (`HIVOLT-INTERNATIONALIZATION.md`).
- Google Merchant Center reads the shipping policy per target country. Submit a
  UK or DE feed against this page and the account is disapproved.
- "Production and dispatch: 2–4 business days" describes a make-to-order model
  that has not been agreed. It is also inconsistent with the returns page,
  which gives a US warehouse address.
- "8–14 business days after dispatch" is a transit window for direct-from-Asia
  shipping. If fulfilment moves to a US or EU 3PL, it becomes wrong in the
  other direction — a promise slower than the service.

**SAFE REPLACEMENT DRAFT** — cannot be written yet, and should not be guessed.
The page needs one row per shipping destination and every number in it is a
commercial commitment:

| Destination | Cost | Dispatch | Transit | Duties/VAT |
|---|---|---|---|---|
| United States | ? | ? | ? | n/a |
| Canada | ? | ? | ? | DDP or DAP? |
| United Kingdom | ? | ? | ? | VAT at checkout? |
| EU (per zone) | ? | ? | ? | IOSS registered? |

Until those are answered, the honest interim edit is to delete the two
unverifiable specifics and keep the rest:

> We currently ship within the **United States**. International shipping is in
> preparation — join the list and we will tell you when your country opens.

That removes the invented dispatch window while staying accurate.

**OWNER INPUT REQUIRED** — O2 in the master task register: fulfilment origin,
carrier, cost and realistic transit for US / CA / UK / EU. Nothing on this page
can be corrected without it.

**MARKETS AFFECTED** — US (accuracy), CA / UK / EU (blocks selling entirely).

---

## P-4 — `/pages/returns-refunds` — US-only returns, and an Illinois dispatch claim

**CURRENT TEXT** (verbatim)

> **Return shipping cost**
> **Free.** We ship within the United States only, and every US return comes
> with a prepaid label — there is nothing to pay and nothing to arrange.
>
> **Where we accept returns**
> HIVOLT sells and ships within the United States only. Returns are accepted
> from United States addresses only.
>
> **Refund timing**
> We process refunds within **2 business days** of the return arriving at our
> warehouse.
>
> Dn Global Trading LLC
> 10s225 Kaye Ln, Willowbrook, IL 60527, United States

**WHY IT IS WRONG**

- "Returns are accepted from United States addresses only" is a legal
  statement. In the UK it conflicts with the Consumer Contracts Regulations
  14-day right to cancel, and in the EU with the Consumer Rights Directive.
  Publishing it and then selling into those markets is not a copy problem, it
  is an enforcement problem.
- "our warehouse" plus an Illinois address states that HIVOLT dispatches and
  receives returns from Illinois. No fulfilment model has been agreed; if goods
  ship from a supplier in Asia, this is false and the 2-business-day refund
  clock is unachievable.
- The shipping page says "production and dispatch 2–4 business days" (made to
  order); this page says returns arrive at a warehouse in Illinois. Both cannot
  be true.

**SAFE REPLACEMENT DRAFT**

Change the two US-only clauses to describe where we *currently* sell rather
than where we will *ever* sell:

> **Where we accept returns**
> We accept returns from any address we ship to. HIVOLT currently ships within
> the United States; as each new country opens, returns open with it.

And, until the fulfilment model is settled, replace "arriving at our warehouse"
with a fact that does not depend on it:

> We process refunds within **2 business days of the return being delivered to
> the address on your prepaid label**.

The registered-company block at the foot of the page must stay — it is a
required trader identity — but it should be labelled as the company address,
not implied to be the warehouse:

> Registered company: Dn Global Trading LLC, 10s225 Kaye Ln, Willowbrook,
> IL 60527, United States

**OWNER INPUT REQUIRED**
1. O2 again: where do returns physically go?
2. LEGAL: EU/UK statutory withdrawal rights are 14 days minimum and run
   alongside, not instead of, the 60-day commercial guarantee. Confirm the
   60-day policy is offered in those markets before any EU/UK launch.
3. Confirm Dn Global Trading LLC is the trading entity for EU/UK sales, or name
   the entity that is.

**MARKETS AFFECTED** — UK and EU (legal exposure), US (internal contradiction).

---

## P-5 — `/pages/60-day-love-it-guarantee` — activewear framing

**CURRENT TEXT** (verbatim extracts)

> Buying **activewear** online means guessing at fit from a size chart.
>
> Sixty days is a long window precisely because we are asking you to decide
> before you **train in it** rather than after.
>
> If a seam gives, a zip fails or the fabric pills abnormally **under normal
> training use** […]

**WHY IT IS WRONG**

- The whole page is written for training gear. A polo brand does not sell to
  someone deciding whether it "earns a place in your rotation".
- "a zip fails" — polos do not have zips.
- The returns condition itself is correct and consistent with
  `/pages/returns-refunds` (unworn, unwashed, tags attached). Only the framing
  is stale, which makes this the cheapest fix on the list.

**SAFE REPLACEMENT DRAFT** — keep the structure and the 60-day terms exactly as
they are; swap the four activewear phrases:

| Current | Replacement |
|---|---|
| "Buying activewear online means guessing at fit from a size chart." | "Buying a shirt online means guessing at fit from a size chart." |
| "whether it earns a place in your rotation" | "whether it earns a place in your wardrobe" |
| "before you train in it rather than after" | "before you wear it out rather than after" |
| "If a seam gives, a zip fails or the fabric pills abnormally under normal training use" | "If a seam gives, a button fails or the fabric pills abnormally under normal wear" |

**OWNER INPUT REQUIRED** — Confirm the 60-day window survives the pivot. It was
set for a $29–79 activewear catalogue; at polo price points with international
transit it is a materially larger liability (`HIVOLT-UNIT-ECONOMICS.md` prices
returns at 8%).

**MARKETS AFFECTED** — All.

---

## P-6 — `/pages/materials-sustainability` — a promise with nothing behind it

**CURRENT TEXT** (verbatim)

> HIVOLT publishes what we actually know about each garment — no more, no less.
>
> **Composition**
> Where our suppliers publish fabric composition — knit elastane, polyester
> blends, cotton mixes — it appears on the product page. Where a figure isn't
> published, we don't invent one.

**WHY IT IS WRONG**

- Narrowly: it is the most honest page on the site and its rule is the right
  one. It is listed here only because "it appears on the product page" is not
  currently true of anything — there are no live products.
- "knit elastane, polyester blends" is activewear vocabulary.
- The earlier audit removed a dead Fabric Weight Index link from this page; if
  P-1 resolves as *retire*, check nothing points back here in a loop.

**SAFE REPLACEMENT DRAFT** — one paragraph, no structural change:

> **Composition**
> Where a supplier publishes fabric composition and weight, it appears on the
> product page, in the specification table, exactly as the supplier states it.
> Where a figure is not published, the row is left out rather than filled in.

**OWNER INPUT REQUIRED** — None. This is a wording correction inside an existing
true claim.

**MARKETS AFFECTED** — All.

---

## P-7 — Overlapping active discounts

**CURRENT STATE** (from the Admin API, not from page copy)

| Discount | Type | Status |
|---|---|---|
| Two or more — 15% off | Automatic | ACTIVE since 2026-08-12 |
| Welcome 10% off first order | Code | ACTIVE |
| Abandoned Cart — 10% Comeback Offer | Code | ACTIVE |
| Launch Offer — 20% Off First Order | Code | ACTIVE |

The announcement bar advertises the 15%, and the theme's (disabled) newsletter
popup advertises "Save 10% on your first order".

**WHY IT IS FLAGGED** — Not a contradiction: every claim on the site is backed
by a real, active discount. It is flagged because three first-order discounts
are live simultaneously against a catalogue with no approved retail price, and
a 20% launch discount would consume most of the modelled contribution margin
before any acquisition cost (`HIVOLT-UNIT-ECONOMICS.md`: break-even CAC at $69
single-unit is $33.43 *before* discounting beyond the 5% already assumed).

**SAFE REPLACEMENT DRAFT** — none proposed. Discounts are explicitly
owner-approval-only.

**OWNER INPUT REQUIRED** — Which of the four survives the pivot? The other three
should be deactivated before the polo line is published, not after.

**MARKETS AFFECTED** — All.

---

## What was changed instead, and where

Nothing above was applied. The equivalent corrections **inside the unpublished
draft theme** (`HIVOLT v7 — DRAFT: PDP data layer`, theme `158653808872`) were:

| Change | Why it was safe to make |
|---|---|
| Homepage rebuilt: removed the hero CTAs to `coats-jackets` and `womens-activewear`, six empty category tiles and five empty product rows | Unpublished theme; removes links, adds no claim |
| Main menu repointed to a new `hivolt-draft-main` menu (Shop all / About / Help) | New menu; `main-menu` untouched, so the live theme is unaffected |
| Footer "Shop" column repointed to `hivolt-draft-shop` | Same |
| Homepage trust block reworded from "measurements in the size guide" to describe what the new size guide actually does | Describes our own code, not a policy |

The announcement bar's shipping and returns lines were **left exactly as they
are**, because they restate the live policy — and the live policy is what this
document is asking about.
