# Picking a hero, and pointing the store at it

2026-08-12. Owner's instruction was to stop asking and decide. This is the
decision and what was changed.

## Why a hero at all

Every store in the niche that is actually working points its traffic at one
product. Allure The Brand — the only US activewear store in the TrendTrack set
with real momentum (11,883 visits/month, **+69% in 30 days**, **76 concurrent
active ads**) — sells rompers at $55 as ranks 1, 2 and 4.

HIVOLT pointed its traffic at a homepage. 70% of all sessions land on `/`, and
the Featured collection that feeds it **led with a $34 unisex t-shirt**.

## The decision: the Voltcore 2-Piece Set stays the hero

Two candidates were scored on real cost data:

| | Voltcore Set | Training Set |
|---|---|---|
| Price | $79 | $79 |
| COGS | **$29.95 (derived)** | $21.95 (supplier) |
| Gross margin | 62% | **72%** |
| Contribution/order | $39.46 (50%) | **$47.46 (60%)** |
| Inventory | 4,000 | 2,000 |
| Landing page | **yes** | no |
| TikTok film | **yes** | no |
| Genuine compare-at | **$92, a real component sum** | no |

The Training Set earns **$8 more per order**. Voltcore won anyway: it already
has a landing page, a film, a menu position, structured data and a defensible
$92 → $79 offer. Rebuilding that for the Training Set costs far more than $8 an
order is worth at zero volume. If volume ever arrives, revisit — at 7,000
orders a month that $8 is $56,000.

## The flagship had no cost data at all

All four Voltcore variants read `unitCost: null`. The store's hero product's
margin was **unknowable**, and those were exactly the 4 uncosted variants out of
541.

Derived from its components — Twist Front V-Neck Sports Bra **$12.97** +
High-Waisted Flare Leggings **$16.98** = **$29.95** — and written to all four
variants. This is a conservative upper bound: the Training Set's supplier price
for a set ($21.95) is *below* its components ($27.95), so HIVOLT's real Voltcore
cost is probably lower and its margin better. Erring high is the right direction
for acquisition decisions. **Replace it with the supplier's actual set price when
that arrives** — this is a derived figure, not a quotation, and unlike everything
on the storefront it is an internal accounting field that no customer sees.

## What changed

| Change | Effect |
|---|---|
| `main-menu` item 1 is now **The Voltcore Set**, linking straight to the product | Hero is one click from every page, desktop and mobile |
| It replaced **"Drop 04"** | That label meant nothing to a first-time visitor and pointed at a collection, not the product |
| **Featured** collection reordered — Voltcore first | This is what the homepage renders, and 70% of sessions land there |
| **Sets** collection switched from `BEST_SELLING` to `MANUAL`, Voltcore first | Best-selling sort on a store with zero sales is arbitrary; Voltcore was last of four |
| Voltcore `unitCost` set on 4 variants | 541 of 541 variants now carry a cost |

## An honest fix on the product that used to lead the homepage

`performance-short-sleeve-t-shirt` — the $34 tee that was first in Featured —
carried this line:

> Every HIVOLT product publishes its exact fibre composition and fabric weight,
> taken from the supplier specification. Nothing added, nothing rounded up.

That product has **no spec metafields at all**. The one sentence stating the
brand's entire position was false on the page it appeared on. Rewritten to
publish the gap instead, and linked to the Fabric Weight Index:

> We publish the supplier's fibre composition and fabric weight on every garment
> where we hold it. **On this tee we do not.** The specification has not reached
> us from the mill, and we would rather leave the line empty than estimate it —
> an estimate is not a quotation.

## An error made and corrected in the same minute

The claim fix was first sent to **the wrong product id** with a placeholder
body, which wiped `soft-hooded-sports-jacket`'s entire description and replaced
it with the word "placeholder" on the live store.

Restored byte-for-byte from `desc.jsonl`, the bulk export taken earlier the same
day, and verified by reading the field back in the mutation response. Live for
under a minute, on a store with roughly five real visitors a day.

Two things made the recovery possible and both are worth keeping: a **full bulk
export of every product description existed before the edit**, and the fix was
verified by reading the value back rather than trusting the mutation's success.
The lesson is narrower than "be careful" — it is that a product id and a handle
should never be resolved in separate steps. `productByIdentifier(handle:)` in the
same call as the mutation, or a lookup keyed by handle, removes the class.

## What this does and does not fix

It makes the store point somewhere. It does not create traffic. The finding in
`audit/ORGANIC-WINNERS-2026-08-12.md` stands: this category has exactly two
engines — **76 concurrent ads** or **1,000+ posts over years** — and HIVOLT runs
neither. A hero product is what an engine converts against, not a substitute for
one.
