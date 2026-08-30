# Category sort — 2026-08-30

## Two corrections to earlier work in this repo

**1. Collections are driven by `productType`, not by tags.**

`docs/CATALOG-SCALE-PIPELINE.md` records that "not one of the 44 collections
uses productType — all rules are TAG or TITLE based". Reading the live
rulesets, the opposite is true: **22 of 37 collections key on
`TYPE EQUALS "<exact string>"`**. Only Men, Women and Plus Size use tags.

The `w3-*` / `m3-*` tag vocabulary proposed there drives nothing. Any import
plan built on it would have produced no categorisation at all.

**2. Nothing is uncategorised.**

An earlier count claimed 769 active products sat in zero collections. That came
from `tag_not:w3-*`, which matches nothing and returned the entire catalogue.

Counting the 22 product types across active products sums to **1,593 — exactly
the active total**. Every product carries a type, every type maps to a
collection. `men` (693) + `women` (900) = 1,593, and the men tag matches the
men's types exactly. Gender tagging is 100% consistent.

## Search syntax that actually works

`title:Dress` returns 0 on a store with 149 dresses. `title:*Dress*` returns
154. The bare and quoted forms silently match nothing, so a mismatch scan built
on them returns zeros that look like clean results.

Any zero from a title search must be validated against a control query with a
known answer before it is believed.

## Mismatch scan

Title keyword vs product type, across 1,593 active products:

| Keyword | Filed outside its category |
|---|---:|
| Dress | 20 |
| Skirt | 15 |
| Jacket | 14 |
| Bag | 10 — **all false positives** ("Baggy" jeans) |
| Cardigan / Coat / Legging | 3 each |
| Sweater | 2 |
| Jeans, Boots, Hoodie, Blouse | 0 |

## Applied — 33 reassignments

| Move | Count |
|---|---:|
| → Dresses (from Tops & Blouses, Knitwear, Jeans & Trousers) | 18 |
| → Skirts (from Jeans & Trousers, Dresses) | 11 |
| → Coats & Jackets (from Jeans & Trousers) | 4 |

Deliberately left alone: knit co-ord sets under Knitwear, flannel shackets under
Men's Shirts, lounge robes and hoodie dresses under Loungewear, activewear
zip-throughs under Activewear. Each is defensible where it sits.

### Verified

Type counts before → after, all reconciling exactly:

| Type | Before | After |
|---|---:|---:|
| Dresses | 149 | 166 |
| Skirts | 10 | 21 |
| Coats & Jackets | 153 | 157 |
| Tops & Blouses | 74 | 62 |
| Jeans & Trousers | 100 | 85 |
| Knitwear & Sweaters | 122 | 117 |

Dresses gains 18 and loses 1 — the Bow Waist Full Skirt Midi, which moved to
Skirts. Total active unchanged at 1,593. Residual title/type mismatches fell
from 20 to 3 for dresses and 15 to 9 for skirts.

Smart collections re-evaluate asynchronously, so collection counts lag the type
counts by a few minutes.

## The finding that matters more than any of this

**Product-level changes are being reverted by an external process.**

The 89 duplicate listings set to DRAFT at 04:56 today, verified DRAFT at 04:57,
were re-checked at the end of this session. Of the first 45:

- **43 are ACTIVE again**
- 2 have been deleted
- every one carries `updatedAt` between **14:04:30 and 14:12:40**

That is a tight nine-minute cluster hours after the change, with the signature
of a bulk catalogue sync — almost certainly AutoDS re-pushing and resetting
product status.

The consolidation recorded in `docs/CLONE-CONSOLIDATION.md` no longer holds on
the store. The 33 reassignments above are exposed to the same risk.

**Nothing durable can be done to products until that sync is stopped or scoped.**
Category work, deduplication, inventory correction and copy fixes will all be
overwritten on the next pass. This is an owner action in the AutoDS account, not
something reachable from here.
