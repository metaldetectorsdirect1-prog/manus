# The advertised discount was selling four products at a loss

2026-08-12. Found while pricing the $500k goal. Everything here is fixed except
the last item, which is the owner's.

## The checkout works — first hard evidence

`draftOrderCalculate` against a real Chicago address returned:

```
subtotal      $72.00
shipping      $0.00   "FREE US Shipping (8-14 business days)"  — the only rate
total         $72.00
```

Exactly one shipping rate quotes, and it is the free one — confirming the 89
paid Tapstitch rates are still deactivated. Address validation, rate resolution
and pricing all work. The store has never taken an order, but the failure modes
that would silently kill a first order are ruled out. What remains untested is
the card charge itself, which needs a real order.

## VOLT20 was making four products loss-making

The ticker advertises "20% off your first order · code VOLT20" on **every page**.
Applied to a single-item order, against real `unitCost` data:

| | Contribution |
|---|---|
| No discount | **$22.72** average, 0 of 112 loss-making |
| WELCOME10 (10%) | $18.09 average, **3 loss-making** |
| VOLT20 (20%) | **$13.47** average, **5 loss-making** |

The advertised code cut average contribution by **41%** and pushed five products
below zero. One of those five was the varsity jacket already repriced to $72
earlier today, leaving four:

| Was | Cost | Contribution under VOLT20 | Now |
|---|---|---|---|
| $34 | $22.98 | **−$3.87** | **$54** |
| $34 | $22.98 | **−$3.87** | **$54** |
| $34 | $22.98 | **−$3.87** | **$54** |
| $34 | $19.97 | **−$0.86** | **$48** |

Three colour-block tees and a mesh boxy tee, 20 variants, all repriced. The
catalogue now has **zero loss-making products under any live discount code**.

### This reverses a call made earlier the same day

The $500k note said these five were deliberately left alone, because raising
prices on an unknown brand works against getting a first order. That reasoning
held while the choice was *thin margin versus cheap entry price*. It stops
holding once the number is negative: an order that loses money is not a first
sale worth having, and there is no email list and no repeat-purchase mechanism
to recover it from later. New information, different answer.

The prices are reversible, and $22.98 for a colour-block v-neck is anomalous
against $12.97 for comparable tees in the same catalogue — worth querying with
the supplier rather than absorbing.

### Why not a minimum-spend rule instead

Adding a minimum subtotal to VOLT20 would fix the loss and lift AOV in one
move. It was rejected: the ticker says "20% off your first order" with no
condition attached, the ticker text is a theme setting on the live theme, and
theme-settings writes are blocked here. Adding a hidden condition to a promise
published on every page is the same class of defect as the worn-and-washed
returns conflict. Fixing the price fixes it at source and breaks no promise.

## New: "Two or more — 15% off"

An automatic discount, live, all products, no code needed, and set **not** to
combine with the order-discount class so it cannot stack with VOLT20.

AOV is the cheapest lever on the $500k arithmetic — breakeven ROAS moves from
2.12 on a one-item basket to 1.82 on a two-item basket. The mechanic pays for
itself:

| | One item | Two items, 15% off |
|---|---|---|
| Revenue | $46.90 | $79.73 |
| Contribution | $22.16 (47.2%) | $37.96 (47.6%) |

Same margin percentage, **71% more profit per order**.

**Unverified:** `draftOrderCalculate` does not evaluate automatic discounts, so
it returned the undiscounted $144 on a two-item basket. That is expected
behaviour for draft orders, not evidence the discount is broken — but it does
mean the live cart behaviour has not been confirmed from here, and the storefront
is proxy-blocked. It shows `ACTIVE` in the admin. Worth one look in a real cart.

## Open, and the owner's: no sales tax is being collected

The same draft order returned **$0.00 tax** on an Illinois-to-Illinois shipment.
The shop's billing address is Willowbrook, IL, the shipping policy says orders
dispatch from Illinois, and `taxesIncluded` is false — so an Illinois buyer
should be charged Illinois tax and is not. No tax registration is configured.

It does not block a sale and it is not urgent at zero orders. It becomes serious
quickly: at the $500k/month target, economic nexus thresholds (typically $100k
or 200 transactions) would be crossed in dozens of states within months, and
uncollected tax is a liability that accrues quietly against the business rather
than the customer. Shopify → Settings → Taxes and duties. Not exposed through
the Admin API, so it cannot be set from here.
