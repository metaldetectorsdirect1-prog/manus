# $500,000 a month: what the numbers actually say

2026-08-12. Goal set by the owner. This is the arithmetic against the real
catalogue, not an estimate.

## The unit economics support it

Pulled from `inventoryItem.unitCost` on all 541 active variants — **537 carry a
cost**, so contribution margin is scoreable. (The PR body's claim that the
supplier cost lines are blank is stale; they are populated.)

| | |
|---|---|
| Catalogue-weighted gross margin | **65.7%** |
| Average price / cost / gross profit | $46.90 / $16.08 / $30.82 |
| Gross margin range | 32% – 83% |
| Variants priced below cost | **0** |

After COGS, $7 domestic shipping (the store advertises free US shipping with no
minimum) and 2.9% + 30¢ processing:

| AOV | Orders/month | Orders/day | Contribution | Breakeven ROAS |
|---|---|---|---|---|
| $46.90 (1 item) | 10,661 | 355 | 47.2% | 2.12 |
| $65.66 (1.4 items) | 7,615 | 254 | 51.7% | 1.93 |
| $93.80 (2 items) | 5,330 | 178 | 55.0% | 1.82 |

**This is a good structure.** Plenty of apparel brands run a business on 50%
contribution. The unit economics are not what is stopping this.

## The traffic requirement is the whole problem

At $65.66 AOV, $500k/month means **7,615 orders — 254 a day**.

| Conversion rate | Sessions/month | Sessions/day |
|---|---|---|
| 1% | 761,499 | 25,383 |
| 2% | 380,749 | 12,692 |
| 3% | 253,833 | 8,461 |

Real non-bot traffic today is **about 5 sessions a day**. Two percent is a
healthy apparel conversion rate, so the requirement is roughly a **2,500×
increase in real traffic**. Not 25% better. Two and a half thousand times.

Nothing about the store — copy, schema, page speed, fabric index — moves a
number by that factor. Only distribution does.

## There are two routes and only two

### Paid

Breakeven is ROAS 1.93, so it has to run above ~2.5 blended to make money. A
brand with no creative library, no pixel history and no purchase data does not
start there — 1.0 to 1.5 for the first 60–90 days is the normal experience,
which means paying to learn before paying to earn.

At a mature ROAS of 2.5:

* ~$200,000/month in ad spend to produce $500,000 in revenue
* ~$122,000/month in inventory at cost (7,615 × $16.08)
* leaves roughly **$58,000/month** in contribution after media

So the machine needs something like **$320,000 of working capital in float**
before the revenue lands, and months of losses while the account learns.

This also directly contradicts the standing instruction to grow **without ads**.
It is not being recommended around that instruction — it is being priced so the
choice is made with the number visible.

### Organic

The comparables already researched: `sidemenclothing.com` runs 200–330k monthly
visits on zero ad spend with **784,500 TikTok followers**; `yeoreo.com` posted
**1,249 times over four years**. That is the mechanism and that is the
timescale.

Twelve films are live on @hivoltusa and have produced **zero** referrals,
because typography films are not what wins — the top 15 organic `leggings` posts
run 6.9M–34.5M views and every one is a person on camera. That is the missing
input, and it cannot be produced from inside a container.

## The honest timeline

$500k/month is a **12–24 month** target with capital behind it, and longer
without. There is no version where a store with zero orders reaches it this
quarter, and any plan that implies otherwise is selling something.

## The milestone that actually matters now

**The first 100 orders.** Everything needed for scale is downstream of it:

* **Reviews.** There are none. Apparel converts materially worse without them,
  and no amount of traffic fixes a page with zero social proof.
* **Which products sell.** 113 SKUs, no demand data. Buying traffic across all
  of them is how money disappears.
* **Whether the gateway works.** It has never been exercised. A ~$34
  self-purchase settles it.
* **Pixel and audience data.** Every paid channel needs conversion events to
  optimise against. Zero orders means zero signal.

## What is structurally in the way — found today

**1. Five products cannot fund their own acquisition.** Contribution after
shipping and processing:

| Contribution | Price | Cost | Product |
|---|---|---|---|
| **8.0%** ($2.73) | $34 | $22.98 | Unisex Color Block Raglan T-Shirt, Army Green |
| **8.0%** ($2.73) | $34 | $22.98 | Unisex Color Block V-Neck T-Shirt, Black/Red |
| **8.0%** ($2.73) | $34 | $22.98 | Unisex Color Block V-Neck T-Shirt, White |
| 16.9% ($5.74) | $34 | $19.97 | Unisex Raglan Sleeve Mesh Boxy T-Shirt |
| 22.7% ($7.73) | $34 | $17.98 | four tank tops at this cost |

$2.73 an order does not pay for a click on any channel. These need repricing to
about $49, or excluding from paid promotion. Deliberately **not** repriced here:
raising prices on an unknown brand works directly against the near-term goal of
a first order, and that trade is the owner's to make.

**2. Free shipping with no minimum is the largest single drag.** At a $46.90
average item price, $7 of shipping is **15% of revenue**, and on the $34 items
it is 21%. A **$60 free-shipping threshold** raises AOV and protects margin at
the same time, and AOV is the cheapest lever on breakeven ROAS — the table above
shows it moving from 2.12 to 1.82 between a one-item and a two-item basket.
Shipping lives in an app-managed Tapstitch profile, so a Tapstitch resync can
revert edits to it; that is why this is flagged rather than changed.

**3. Fixed today.** `two-tone-raglan-sleeve-varsity-jacket` was $42 against
`two-tone-fleeced-varsity-jacket` at $74 — both 380 g/m², costs $25.98 and
$27.97. The $42 was a pricing miss, not a positioning choice, and it ran at
17.9% contribution. Raised to **$72**, which puts it beside its twin and at
50.9% contribution.

## Ranked by effect on the goal

1. **Merchant Center: claim the domain and configure shipping** in the Google &
   YouTube channel's account. Free Shopping listings put products in front of
   people already searching to buy. Highest-intent traffic available, zero
   media cost, and it is one screen of work.
2. **Free-shipping threshold at $60.** Lifts AOV and cuts breakeven ROAS.
3. **Reprice or retire the five sub-20% products** before any paid traffic.
4. **One real order** to prove the gateway.
5. **A reviews mechanism**, so the first 100 orders compound into conversion.
6. **A person on camera** for TikTok. This is the only organic channel with a
   demonstrated path to the traffic volumes above.
